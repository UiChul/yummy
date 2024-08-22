import ffmpeg

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
    
