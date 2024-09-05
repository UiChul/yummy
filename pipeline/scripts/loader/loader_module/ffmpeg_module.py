
import ffmpeg
import os
import re

def change_to_png(input,output):
    (
        ffmpeg
        .input(input)
        .output(output,vf="eq=gamma=1.7")
        .run()
    )
    
def find_resolution_frame(input):
    probe = ffmpeg.probe(input)
    video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    
    if input.split(".")[-1] == "mov" or input.split(".")[-1] == "mp4":
        frame = int(video_stream['nb_frames'])
    else:
        frame = 0
    
    return width,height,frame

def get_frame_count_from_directory(directory):
    # 디렉토리에서 EXR 파일 목록 가져오기
    exr_files = [f for f in os.listdir(directory) if f.endswith('.exr')]
    exr_files.sort()
    
    start_frame = int(exr_files[0].split(".")[-2])
    end_frame   = int(exr_files[-1].split(".")[-2])


    # 프레임 수 계산
    frame_count = end_frame - start_frame + 1

    return start_frame,end_frame,frame_count

def change_codec(input,output):
    (
        ffmpeg
        .input(input)
        .output(output,vcodec="prores")
        .run()
    )