import ffmpeg
import os
import subprocess

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

def change_codec(input,output):
    (
        ffmpeg
        .input(input)
        .output(output,vcodec="prores")
        .run()
    )
    
def auto_change(path):
    clip_list = os.listdir(path)
    # print(clip_list)
    for clip in clip_list:
        clip_path = path + "/" + clip
        out_path = path +"/new"+ "/" + clip
    # print(clip_path)
        if "H264" in clip_path :
            change_codec(clip_path,out_path)
        

def extract_thumbnail_ffmpeg(video_path, thumbnail_path, time="00:00:02"):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-ss', time,
        '-vframes', '1',
        '-q:v', '2', 
        thumbnail_path 
    ]

    subprocess.run(command, check = True)

def auto_extract(path):
    clip_list = os.listdir(path)
    
    numb = 0
    for clip in clip_list:
        
        clip_path = path + "/" + clip
        
        extract_thumbnail_ffmpeg(clip_path, f'/home/rapa/YUMMY/project/Marvelous/template/shot/clip_thumbnail/{clip}.jpg')
        numb += 1



