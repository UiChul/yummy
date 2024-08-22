import ffmpeg

def get_size_info(input):
        probe = ffmpeg.probe(input)
        video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
        width = int(video_stream['width'])
        height = int(video_stream['height'])

        if input.split(".")[-1] == "mov" or input.split(".")[-1] == "mp4":
            frame = int(video_stream['nb_frames'])
        else:
            frame = 0
        # print(width,height)
        return width,height,frame

w,h,f = get_size_info("/home/rapa/YUMMY/project/Marvelous/template/shot/clip_lib/OpenfootageNET_00268_Fluid_lowres.mov")
print(f)