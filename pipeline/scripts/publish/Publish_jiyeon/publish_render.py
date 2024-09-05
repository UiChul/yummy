import os
import nuke
import ffmpeg
import os
import json
from publish_module2 import PathFinder


class Render:
    def __init__(self):
        self.find_write_node()

    def find_write_node(self):
        select_nodes = nuke.selectedNodes()
        if not select_nodes:
            print("선택된 write노드가 없습니다.")
            return
        
        for node in select_nodes:
            if node.Class() == "Write":
                self.write_node = node
                if self.write_node.inputs() == 0:
                    nuke.message("write노드를 렌더링할 노드에 연결해주세요.")
                else:
                    a = nuke.message("렌더링 하시겠습니까?")
                    if a == 1:
                        pass
                    else:
                        self.start_render()
                        nuke.message("렌더링이 완료되었습니다.")
                        self.put_the_slate_in_file()
                        
            else:
                nuke.message("write노드를 선택해주세요.")
    
    def start_render(self):
        self.render_exr()
        print("Hello")

    def render_exr(self):
        exr_path = self.set_the_file_path()[0]
        exr_folder_path = os.path.dirname(exr_path)
        print(exr_path)

        self.write_node["file"].setValue(exr_path)
        self.write_node["file_type"].setValue("exr")
        self.write_node['first'].setValue(1000)

        if os.path.exists(exr_folder_path):
            nuke.execute(self.write_node)
        else:
            os.makedirs(exr_folder_path)
            nuke.execute(self.write_node)

    def set_the_file_path(self):
        
        # json_file_path = '/home/rapa/sub_server/pipeline/scripts/project_data.json'
        json_file_path = 'C:/Users/LEE JIYEON/Desktop/sub_server/pipeline/scripts/project_data.json'
        path_finder = PathFinder(json_file_path)

        # start_path = '/home/rapa/sub_server/project'
        start_path = 'C:/Users/LEE JIYEON/Desktop/sub_server/project'
        project_path = path_finder.append_project_to_path(start_path)

        seq_path = f"{project_path}seq/"

        nuke_path = nuke.scriptName()
        nuke_file_name = os.path.basename(nuke_path)
        base, _ = os.path.splitext(nuke_file_name)
        print(base)
        item = nuke_file_name.split("_")
        shot = item[0]
        code = item[1]
        team_name = item[2]
        
        a = "####"
        exr_file_path = f"{seq_path}{shot}/{shot}_{code}/{team_name}/dev/exr/{base}/{base}.{a}.exr"
        mov_file_path = f"{seq_path}{shot}/{shot}_{code}/{team_name}/dev/mov/{base}.mov"
       
        return exr_file_path, mov_file_path
    
    def put_the_slate_in_file(self):
        exr_file_path, mov_file_path = self.set_the_file_path()
        exr_dir = os.path.dirname(exr_file_path)
        mov_path = mov_file_path
        print("ffmpeg 시작")
        self.start_exr(exr_dir,mov_path)
        
    def start_exr(self,exr_path,output):
        
        exr_file_name = exr_path.split("/")[-1]
        
        # exr 들어있는 폴더 이름이 ABC_0020_LGT_v001이면 
        # 폴더 이름 바탕으로 slate에 넣는 정보 세팅 해줌
        slate_dic = self.set_slate_info(exr_path)
        
        self.input_slate(slate_dic)
        a = "%4d"
        input = f"{exr_path}/{exr_file_name}.{a}.exr"
        
        self.gamma = "eq=gamma=1.4,"
        self.render_exr_slate(input,output)
        
    # slate에 넣을 정보 딕셔너리에 넣기  
    def set_slate_info(self,exr_path):
        import datetime
        time = datetime.datetime.now()
        exr_file_name = exr_path.split("/")[-1]
        time_min = time.strftime('%Y.%m.%d')
        
        slate_dic = {}
        
        slate_info = exr_file_name.split("_")
        
        # 첫 프레임 마지막 프레임 계산 해주는 함수
        start_frame,end_frame,frame = self.get_frame_count_from_directory(exr_path)
        
        invert_text = '%{n}/'
        invert_text += f"{start_frame} - {end_frame}"
        
        slate_dic["ShotNum"] = "_".join([slate_info[0],slate_info[1]])
        slate_dic["Project"] = "Baked"
        slate_dic["Date"] = time_min
        slate_dic["Task"] = slate_info[2]
        slate_dic["Version"] = slate_info[3]
        slate_dic["Frame"] = invert_text
        
        return slate_dic
    
    #frame수 계산하기
    def get_frame_count_from_directory(self,directory):
        # 디렉토리에서 EXR 파일 목록 가져오기
        exr_files = [f for f in os.listdir(directory) if f.endswith('.exr')]
        exr_files.sort()
        self.find_exr_frame(f"{directory}/{exr_files[0]}")
        
        start_frame = int(exr_files[0].split(".")[-2])
        end_frame   = int(exr_files[-1].split(".")[-2])

        # 프레임 수 계산
        frame_count = end_frame - start_frame + 1
        return start_frame,end_frame,frame_count
    
    def find_exr_frame(self,input):
        probe = ffmpeg.probe(input)
        video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
        self.width = int(video_stream['width'])
        self.height = int(video_stream['height'])
        
        
    def render_exr_slate(self,input,output):
        (
            ffmpeg
            .input(input,start_number = 1001)    
            .output(output,vcodec="prores",vf=f"{self.box}"f"{self.gamma}"f"{self.top_Left},{self.top_Middel},{self.top_Right},{self.bot_Left},{self.bot_Middle},{self.bot_Right}")
            .run()
        )    

    def input_slate(self,slate_dic):
        
        shot_num = slate_dic["ShotNum"]
        project = slate_dic["Project"]
        date = slate_dic["Date"]
        task = slate_dic["Task"]
        version = slate_dic["Version"]
        frame = slate_dic["Frame"]
        
        font_size = self.height/18 - 5
        box_size = self.height/18
        
        self.top_Left = f"drawtext=fontfile=Arial.ttf:text   = '{shot_num}': : x=5:y=5           :fontcolor=white@0.7:fontsize={font_size}"
        self.top_Middel = f"drawtext=fontfile=Arial.ttf:text = '{project}': : x=(w-tw)/2:y=5   :fontcolor=white@0.7:fontsize={font_size}"
        self.top_Right = f"drawtext=fontfile=Arial.ttf:text  = '{date}': : x=w-tw-5:y=5      :fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Left = f"drawtext=fontfile=Arial.ttf:text   = '{task}': : x=5:y=h-th        :fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Middle = f"drawtext=fontfile=Arial.ttf:text = '{version}': : x=(w-tw)/2:y=h-th :fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Right = f"drawtext=fontfile=Arial.ttf: text = '{frame}':start_number = 1001 : x=w-tw-5:y=h-th     :fontcolor=white@0.7:fontsize={font_size}"
        self.box = f"drawbox = x=0: y=0: w={self.width}: h={box_size}: color = black: t=fill,drawbox = x=0: y={self.height-box_size}: w={self.width}: h={self.height}: color = black: t=fill,"

def start_render_in_nuke():
    from importlib import reload
    # import sys
    global win
    # sys.path.append("/home/rapa/sub_server/pipeline/scripts")
    import publish_render
    reload(publish_render)
    win = publish_render.Render()      