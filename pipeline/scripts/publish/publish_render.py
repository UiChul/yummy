import os
import nuke
import subprocess
from publish_pathfinder import PathFinder

class Render:
    def __init__(self):
        self.write_node = None
        self.find_write_node()

    # ==================================================================
    """Rendering Process"""
    
    def find_write_node(self):
        select_nodes = nuke.selectedNodes()
        if not select_nodes:
            nuke.message("선택된 Write 노드가 없습니다. 생성하시겠습니까?")
            nuke.createNode("Write")
            
            return
        
        for node in select_nodes:
            if node.Class() == "Write":
                self.write_node = node
                if self.write_node.inputs() == 0:
                    nuke.message("Write 노드를 렌더링할 노드에 연결해주세요.")
                    return
                else:
                    if nuke.ask("렌더링 하시겠습니까?"):
                        self.start_render()
                        nuke.message("렌더링이 완료되었습니다.")
                        self.put_the_slate_in_file()
                        nuke.message("slate 생성이 완료되었습니다.")
            else:
                nuke.message("Write 노드를 선택해주세요.")
    
    def start_render(self):
        self.render_exr()

    def render_exr(self):
        exr_path = self._set_the_file_path()[0]
        exr_folder_path = os.path.dirname(exr_path)
        print(f"EXR 파일 경로: {exr_path}")

        self.write_node["file"].setValue(exr_path)
        self.write_node["file_type"].setValue("exr")

        if not os.path.exists(exr_folder_path):
            os.makedirs(exr_folder_path)

        try:
            nuke.execute(self.write_node)
        except Exception as e:
            print(f"Nuke 실행 중 오류 발생: {e}")
        
    # =====================================================
    """Making Slate"""
    
    def start_exr(self, exr_dir, output):
        exr_files = [f for f in os.listdir(exr_dir) if f.endswith('.exr')]
        if not exr_files:
            print(f"EXR 파일이 디렉토리에 없습니다: {exr_dir}")
            return
        
        exr_file_name = os.path.join(exr_dir, exr_files[0])  # 첫 EXR 파일을 찾음
        slate_dic = self.set_slate_info(exr_file_name)
        self.input_slate(slate_dic)
        exr_one = exr_files[0].split(".")[0]
        input_pattern = os.path.join(exr_dir, f"{exr_one}.%4d.exr")
        ffmpeg_cmd = (
            f"ffmpeg -start_number 1001 -i \"{input_pattern}\" "
            f"-vf \"eq=gamma=2.2, {self.box}{self.top_Left},{self.top_Middel},{self.top_Right},{self.bot_Left},{self.bot_Middle},{self.bot_Right}\" "
            f"-vcodec prores \"{output}\" -y"
        )
        print("FFmpeg 명령어 실행:", ffmpeg_cmd)
        try:
            subprocess.run(ffmpeg_cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg 명령어 실행 중 오류 발생: {e}")
            print(f"명령어: {e.cmd}")
            print(f"출력: {e.output}")
            print(f"오류: {e.stderr}")

    def set_slate_info(self, exr_path):
        import datetime
        time = datetime.datetime.now()
        exr_file_name = os.path.basename(exr_path)
        time_min = time.strftime('%Y.%m.%d')
        
        slate_dic = {}
        slate_info = exr_file_name.split("_")
        
        start_frame, end_frame, _ = self.get_frame_count_from_directory(os.path.dirname(exr_path))
        
        invert_text = f'%{{n}}/{start_frame} - {end_frame}'
        
        slate_dic["ShotNum"] = "_".join([slate_info[0], slate_info[1]])
        slate_dic["Project"] = "Baked"
        slate_dic["Date"] = time_min
        slate_dic["Task"] = slate_info[2]
        slate_dic["Version"] = slate_info[3]
        slate_dic["Frame"] = invert_text
        
        return slate_dic
    
    def get_frame_count_from_directory(self, directory):
        all_files = os.listdir(directory)

        exr_files = []
        for file in all_files:
            if file.endswith('.exr'):
                exr_files.append(file)
        
        exr_files.sort()
        
        if not exr_files:
            print(f"EXR 파일이 디렉토리에 없습니다: {directory}")
            return 0, 0, 0
        
        start_frame = int(exr_files[0].split(".")[-2])
        end_frame = int(exr_files[-1].split(".")[-2])

        return start_frame, end_frame, end_frame - start_frame + 1
    
    def input_slate(self, slate_dic):
        shot_num = slate_dic["ShotNum"]
        project = slate_dic["Project"]
        date = slate_dic["Date"]
        task = slate_dic["Task"]
        version = slate_dic["Version"]
        frame = slate_dic["Frame"]
        
        self.height = 1080
        self.width = 1920
        
        font_size = self.height / 18
        box_size = self.height / 18
        
        self.top_Left = f"drawtext=fontfile=Arial.ttf:text='{shot_num}':x=5:y=5:fontcolor=white@0.7:fontsize={font_size}"
        self.top_Middel = f"drawtext=fontfile=Arial.ttf:text='{project}':x=(w-tw)/2:y=5:fontcolor=white@0.7:fontsize={font_size}"
        self.top_Right = f"drawtext=fontfile=Arial.ttf:text='{date}':x=w-tw-5:y=5:fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Left = f"drawtext=fontfile=Arial.ttf:text='{task}':x=5:y=h-th:fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Middle = f"drawtext=fontfile=Arial.ttf:text='{version}':x=(w-tw)/2:y=h-th:fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Right = f"drawtext=fontfile=Arial.ttf:text='{frame}':x=w-tw-5:y=h-th:fontcolor=white@0.7:fontsize={font_size}"
        self.box = f"drawbox=x=0:y=0:w={self.width}:h={box_size}:color=black:t=fill,drawbox=x=0:y={self.height-box_size}:w={self.width}:h={self.height}:color=black:t=fill,"

    # ======================================================================
    """Putting Slate in Rendering output"""
    
    def put_the_slate_in_file(self):
        exr_file_path, mov_file_path = self._set_the_file_path()
        exr_dir = os.path.dirname(exr_file_path)
        mov_path = mov_file_path
        print(f"{exr_dir}: 디렉토리")
        print(f"{mov_path}: MOV 패스")
        self.start_exr(exr_dir, mov_path)
        
    # ======================================================================
    """Setting Path"""
    
    def _set_the_file_path(self):
        json_file_path = '/home/rapa/yummy/pipeline/json/project_data.json'
        path_finder = PathFinder(json_file_path)

        start_path = '/home/rapa/sub_server/project'
        project_path = path_finder.append_project_to_path(start_path)

        seq_path = f"{project_path}seq/"

        nuke_path = nuke.scriptName()
        nuke_file_name = os.path.basename(nuke_path)
        base, _ = os.path.splitext(nuke_file_name)
        item = nuke_file_name.split("_")
        shot = item[0]
        code = item[1]
        team_name = item[2]
        
        a = "%4d"
        exr_file_path = f"{seq_path}{shot}/{shot}_{code}/{team_name}/dev/exr/{base}/{base}.{a}.exr"
        mov_file_path = f"{seq_path}{shot}/{shot}_{code}/{team_name}/dev/mov/{base}.mov"
       
        return exr_file_path, mov_file_path



def start_render_in_nuke():
    from importlib import reload
    import sys
    global win
    sys.path.append("/home/rapa/sub_server/pipeline/scripts")
    import publish_render
    reload(publish_render)
    win = publish_render.Render()

