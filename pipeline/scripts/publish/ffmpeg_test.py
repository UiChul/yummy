import ffmpeg

class Mov_info():
    def get_size_info(input):
            probe = ffmpeg.probe(input)
            video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            if input.split(".")[-1] == "mov":
                frame = int(video_stream['nb_frames'])
            else:
                frame = 0
            print(width,height)
            return width,height,frame