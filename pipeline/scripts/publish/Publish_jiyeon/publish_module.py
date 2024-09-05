import ffmpeg
import os
import json


class Slate:
    def __init__(self):
        self.make_json_dic()
        
    def make_json_dic(self):
        with open("/home/rapa/yummy/pipeline/json/project_data.json","rt",encoding="utf-8") as r:
            info = json.load(r)
        
        self.project = info["project"]
        
    #===========================================================================================
    # exr에 slate넣기
    #===========================================================================================
        
    def start_exr(self,exr_path,output):
        
        exr_file_name = exr_path.split("/")[-1]
        
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
        
        start_frame,end_frame,frame = self.get_frame_count_from_directory(exr_path)
        
        invert_text = '%{n}/'
        invert_text += f"{start_frame} - {end_frame}"
        
        slate_dic["ShotNum"] = "_".join([slate_info[0],slate_info[1]])
        slate_dic["Project"] = self.project
        slate_dic["Date"] = time_min
        slate_dic["Task"] = slate_info[2]
        slate_dic["Version"] = slate_info[3]
        slate_dic["Frame"] = invert_text
        
        print(slate_dic)
        return slate_dic
    
    #frame수 계산하기
    def get_frame_count_from_directory(self,directory):
        # 디렉토리에서 EXR 파일 목록 가져오기
        exr_files = [f for f in os.listdir(directory) if f.endswith('.exr')]
        exr_files.sort()

        start_frame = int(exr_files[0].split(".")[-2])
        end_frame   = int(exr_files[-1].split(".")[-2])

        # 프레임 수 계산
        frame_count = end_frame - start_frame + 1

        return start_frame,end_frame,frame_count
    
    def render_exr_slate(self,input,output):
        (
            ffmpeg
            .input(input,start_number = 1001)    
            .output(output,vcodec="prores",vf=f"{self.box}"f"{self.gamma}"f"{self.top_Left},{self.top_Middel},{self.top_Right},{self.bot_Left},{self.bot_Middle},{self.bot_Right}")
            .run()
        )
    
    #===========================================================================================
    # mov에 slate넣기
    #===========================================================================================
    
    def start_mov(self,mov_path,output):
        
        self.gamma = "eq=gamma=1.4,"
        slate_dic = self.set_mov_slate_info(mov_path)
        self.input_slate(slate_dic)
        self.render_mov_slate(mov_path,output)
        
        
    def set_mov_slate_info(self,mov_path):
        
        import datetime
        time = datetime.datetime.now()
        
        mov_file = mov_path.split("/")[-1]
        
        mov_name, ext = os.path.splitext(mov_file)
        
        time_min = time.strftime('%Y.%m.%d')
        
        slate_dic = {}
        
        slate_info = mov_name.split("_")
        
        frame = self.find_mov_frame(mov_path)
        
        invert_text = '%{n}/'
        invert_text += f"1001 - {1000+frame}"
        
        slate_dic["ShotNum"] = "_".join([slate_info[0],slate_info[1]])
        slate_dic["Project"] = self.project
        slate_dic["Date"] = time_min
        slate_dic["Task"] = slate_info[2]
        slate_dic["Version"] = slate_info[3]
        slate_dic["Frame"] = invert_text
        
        return slate_dic

    def find_mov_frame(self,input):
        probe = ffmpeg.probe(input)
        video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
        frame = int(video_stream['nb_frames'])
        return frame
        
    def render_mov_slate(self,input,output):
        (
            ffmpeg
            .input(input)    
            .output(output,vcodec="prores",vf=f"{self.box}"f"{self.gamma}"f"{self.top_Left},{self.top_Middel},{self.top_Right},{self.bot_Left},{self.bot_Middle},{self.bot_Right}")
            .run()
        )
            
    #===========================================================================================
    # slate 정보 위치 박스 넣기
    #===========================================================================================

    def input_slate(self,slate_dic):
        print(slate_dic)
        shot_num = slate_dic["ShotNum"]
        project = slate_dic["Project"]
        date = slate_dic["Date"]
        task = slate_dic["Task"]
        version = slate_dic["Version"]
        frame = slate_dic["Frame"]
        
        self.top_Left = f"drawtext=fontfile=Arial.ttf:text   = '{shot_num}': : x=5:y=5           :fontcolor=white@0.7:fontsize=50"
        self.top_Middel = f"drawtext=fontfile=Arial.ttf:text = '{project}': : x=(w-tw)/2:y=5   :fontcolor=white@0.7:fontsize=50"
        self.top_Right = f"drawtext=fontfile=Arial.ttf:text  = '{date}': : x=w-tw-5:y=5      :fontcolor=white@0.7:fontsize=50"
        self.bot_Left = f"drawtext=fontfile=Arial.ttf:text   = '{task}': : x=5:y=h-th        :fontcolor=white@0.7:fontsize=50"
        self.bot_Middle = f"drawtext=fontfile=Arial.ttf:text = '{version}': : x=(w-tw)/2:y=h-th :fontcolor=white@0.7:fontsize=50"
        self.bot_Right = f"drawtext=fontfile=Arial.ttf: text = '{frame}':start_number = 1001 : x=w-tw-5:y=h-th     :fontcolor=white@0.7:fontsize=50"
        self.box = f"drawbox = x=0: y=0: w=1920: h=60: color = black: t=fill,drawbox = x=0: y=1020: w=1920: h=1080: color = black: t=fill,"
       
if __name__ == "__main__": 
    exr_path = "/home/rapa/YUMMY/project/YUMMIE/seq/FNL/FNL_010/lgt/dev/exr/FNL_010_lgt_v002"  
    exr_output = "/home/rapa/YUMMY/project/YUMMIE/seq/FNL/FNL_010/lgt/dev/mov/FNL_010_lgt_v002.mov"     
    render = Slate()
    # render.start_exr(exr_path,exr_output)
    
    mov_path = "/home/rapa/YUMMY/project/YUMMIE/seq/FNL/FNL_010/lgt/dev/mov/FNL_010_lgt_v002.mov"  
    mov_output = "/home/rapa/다운로드/FNL_010_lgt_v001.mov"     
    
    render.start_mov(mov_path,mov_output)
    