import ffmpeg

class Mov_info():
    
    def get_size_info(file_path):

            file_validation_info = {}
            probe = ffmpeg.probe(file_path)

            # extract video_stream
            video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
            codec_name = video_stream['codec_name']
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            # a = video_stream.keys()
            # print(a)

            resolution = f"{width}x{height}"

            if file_path.split(".")[-1] == "mov":
                frame = int(video_stream['nb_frames'])
                colorspace = video_stream['color_space']

            elif file_path.split(".")[-1] == "exr":
                frame = 1
                colorspace = video_stream.get('color_space', "N/A")

            # file_validation dictionary
            file_validation_info = {
                 "file_path": file_path,
                 "codec_name": codec_name
            }
            # file_validation_info["file_path"] = file_path
            # file_validation_info["codec_name"] = codec_name
            # file_validation_info["colorspace"] = colorspace
            # file_validation_info["resolution"] = resolution
            # file_validation_info["frame"] = frame
            # print(file_validation_info)

            print(file_validation_info)

    get_size_info("/home/rapa/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/source/mov/test_v001.mov")