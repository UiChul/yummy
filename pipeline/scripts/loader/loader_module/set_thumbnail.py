import os

def find_file_path(input):
    
    pub_len = input.split(".")
        
    nuke_name, ext = os.path.splitext(input)
    img_path = nuke_name.split("_")
    
    
    
    return f" /{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/{input}"