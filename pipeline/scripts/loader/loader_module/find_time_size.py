from datetime import datetime
import os

class File_data:
    
    def file_info(path):
        size = os.path.getsize(path)
        timestamp = os.path.getmtime(path)
        mod_time = datetime.fromtimestamp(timestamp)
        mod_time = mod_time.strftime('%Y-%m-%d %H:%M')

        if size >= 1000000000:
            size /= 1000000000
            size = round(size,1)
            output = f"{size} GB"
            
        elif size >= 1000000:
            size /= 1000000
            size = round(size,1)
            output = f"{size} MB"
             
        elif size >= 1000:
            size /= 1000
            size = round(size,1)
            output = f"{size} KB"
        
        else:
            size
            output = f"{size} Byte"
        
        return output,mod_time
    
    def dir_info(path):
        size = 0
        filenames = os.listdir(path)
        for filename in filenames:
            filepath = os.path.join(path, filename)
            size += os.path.getsize(filepath)
            
        timestamp = os.path.getmtime(path)
        mod_time = datetime.fromtimestamp(timestamp)
        mod_time = mod_time.strftime('%Y-%m-%d %H:%M')
        
        if size >= 1000000000:
            size /= 1000000000
            size = round(size,1)
            output = f"{size} GB"
            
        elif size >= 1000000:
            size /= 1000000
            size = round(size,1)
            output = f"{size} MB"
            
            
        elif size >= 1000:
            size /= 1000
            size = round(size,1)
            output = f"{size} KB"
        
        else:
            size
            output = f"{size} Byte"


        return output,mod_time
        
if __name__ == "__main__":
    my = File_data
    a,b = my.file_info("/home/rapa/YUMMY/project/Marvelous/seq/OPN/OPN_0010/ani/dev/work/OPN_0010_ani_v003.nknc")
    c,d = my.dir_info("/home/rapa/YUMMY/project/Marvelous/seq/OPN/OPN_0010/ani/dev/exr/OPN_0010_ani_v003")

    print(f"파일 {a},{b}")
    print(f"디렉토리 {c},{d}")

        
    