
import ffmpeg
import os
import json

class Potato:

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
      
    #==================================================================================================================
    # jpg에 slate 넣기
    #==================================================================================================================
    def start_jpg(self,jpg_path,output):
        
        exr_file_name = exr_path.split("/")[-1]
        
        self.find_exr_frame(jpg_path)
        self.input_jpg_slate()
        
        self.gamma = "eq=gamma=1.4,"
        
        self.render_jpg_slate(jpg_path,output)
        
    def find_exr_frame(self,input):
        probe = ffmpeg.probe(input)
        video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
        self.width = int(video_stream['width'])
        self.height = int(video_stream['height'])
    
    def render_jpg_slate(self,input,output):
        (
            ffmpeg
            .input(input)    
            .output(output,vf=f"{self.box}"f"{self.gamma}"f"{self.top_Left},{self.top_Middel},{self.top_Right},{self.bot_Left},{self.bot_Middle},{self.bot_Right}")
            .run()
        )    

    def input_jpg_slate(self):
        
        font_size = self.height/18 - 5
        box_size = self.height/18
        self.top_Left = f"drawtext=fontfile=Arial.ttf:text   = '감자': : x=5:y=2           :fontcolor=white@0.7:fontsize={font_size}"
        self.top_Middel = f"drawtext=fontfile=Arial.ttf:text = '고구마': : x=(w-tw)/2:y=2   :fontcolor=white@0.7:fontsize={font_size}"
        self.top_Right = f"drawtext=fontfile=Arial.ttf:text  = '구황작물': : x=w-tw-5:y=2      :fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Left = f"drawtext=fontfile=Arial.ttf:text   = '당근': : x=5:y=h-th        :fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Middle = f"drawtext=fontfile=Arial.ttf:text = '토끼': : x=(w-tw)/2:y=h-th :fontcolor=white@0.7:fontsize={font_size}"
        self.bot_Right = f"drawtext=fontfile=Arial.ttf: text = '당끼?':start_number = 1001 : x=w-tw-5:y=h-th     :fontcolor=white@0.7:fontsize={font_size}"
        self.box = f"drawbox = x=0: y=0: w={self.width}: h={box_size}: color = black: t=fill,drawbox = x=0: y={self.height-box_size}: w={self.width}: h={self.height}: color = black: t=fill,"
      
      
        
if __name__ == "__main__": 
    render = Potato()
    #===========================================
    # 여기는 exr slate
    # exr 경로에 ABC_0010_LGT_v001처럼
    # 샷_넘버_테스크_버전 맞춰주면 잘 들어감
    exr_path = "/home/rapa/다운로드/ABC_0010_LGT_v001"  
    exr_output = "/home/rapa/다운로드/gamza_001.mov"     
    render.start_exr(exr_path,exr_output)
    
    #===========================================
    # 여기는 jpg slate
    jpg_path = "/home/rapa/xgen/gamza3.jpg"  
    jpg_output = "/home/rapa/다운로드/gamza004.jpg"     
    # render.start_jpg(jpg_path,jpg_output)
    