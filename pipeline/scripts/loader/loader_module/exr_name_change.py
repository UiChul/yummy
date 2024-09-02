import os

# 변경할 폴더 경로를 입력하세요

def exr_name_change():

    folder_path = "/home/rapa/다운로드/ABC_0020_LGT_v001"

    folder_name = folder_path.split("/")[-1]
    print(folder_name)

    # 폴더 내 모든 파일을 가져옵니다
    files = os.listdir(folder_path)

    # 파일 이름 변경 및 삭제 작업을 수행합니다
    for filename in files:
        file_path = os.path.join(folder_path, filename)

        if filename.startswith('rs_pSuperShape2.') and filename.endswith('.exr'):
            # 기존 파일 번호 추출
            file_number = filename.split('.')[1]
            new_filename = f'{folder_name}.{file_number}.exr'

            # 새로운 파일 경로 생성
            new_file_path = os.path.join(folder_path, new_filename)

            # 파일 이름 변경
            os.rename(file_path, new_file_path)

        elif not filename.endswith('.exr'):
            # 확장자가 .exr가 아닌 파일 삭제
            os.remove(file_path)


exr_name_change()
       
import ffmpeg

mp4_dir = os.listdir("/home/rapa/다운로드/project_source")

def video_mov(input,output):
        (
            ffmpeg
            .input(input)
            .output(output,vcodec="prores")
            .run()
        )
        
for mp4 in mp4_dir:
    
    if os.path.isfile("/home/rapa/다운로드/project_source/"+mp4):
        mov = mp4.split(".")[0]
        mov = mov+".mov"
        # video_mov("/home/rapa/다운로드/project_source/"+mp4 , "/home/rapa/다운로드/project_source/mov/"+mov)
     

        
        





