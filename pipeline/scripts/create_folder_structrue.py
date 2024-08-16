import os

# base setting
base_path = "/home/rapa/YUMMY"
project_name = "project_name"

# folder_name
exr_folder = "exr"
mov_folder = "mov"
IO_folder = "I_O"
input_folder = "input"
output_folder = "output"
plate_folder = "plate"
asset_folder = "asset"
cha_folder = "cha"
env_folder = "env"
prop_folder = "prop"
weapon_folder = "weapon"
matte_folder = "matte"
seq_folder = "seq"
scene_folder = "scene"
shot_folder = "shot"
shot_code_folder = "shot_code"
match_folder = "mm"
ani_folder = "ani"
lookdev_folder = "ldv"
lgt_folder = "lgt"
comp_folder = "comp"
dev_folder = "dev"
pub_folder = "pub"
work_folder = "work"
source_folder = "source"
pipeline_folder = "pipeline"
scripts_folder = "scripts"

# folder_structure
folders = [
    f"project/{project_name}/{input_folder}/{plate_folder}/{exr_folder}",
    f"project/{project_name}/{input_folder}/{plate_folder}/{mov_folder}",
    f"project/{project_name}/{output_folder}/{plate_folder}/{exr_folder}",
    f"project/{project_name}/{output_folder}/{plate_folder}/{mov_folder}",

    f"project/{project_name}/{asset_folder}/{cha_folder}/{dev_folder}",
    f"project/{project_name}/{asset_folder}/{cha_folder}/{pub_folder}",
    f"project/{project_name}/{asset_folder}/{env_folder}/{dev_folder}",
    f"project/{project_name}/{asset_folder}/{env_folder}/{pub_folder}",
    f"project/{project_name}/{asset_folder}/{prop_folder}/{dev_folder}",
    f"project/{project_name}/{asset_folder}/{prop_folder}/{pub_folder}",
    f"project/{project_name}/{asset_folder}/{weapon_folder}/{dev_folder}",
    f"project/{project_name}/{asset_folder}/{weapon_folder}/{pub_folder}",
    f"project/{project_name}/{asset_folder}/{matte_folder}/{dev_folder}",
    f"project/{project_name}/{asset_folder}/{matte_folder}/{pub_folder}",

    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{match_folder}/{pub_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{match_folder}/{dev_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{match_folder}/{dev_folder}/{work_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{match_folder}/{dev_folder}/{source_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{ani_folder}/{pub_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{ani_folder}/{dev_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{ani_folder}/{dev_folder}/{work_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{ani_folder}/{dev_folder}/{source_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lookdev_folder}/{pub_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lookdev_folder}/{dev_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lookdev_folder}/{dev_folder}/{work_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lookdev_folder}/{dev_folder}/{source_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lgt_folder}/{pub_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lgt_folder}/{dev_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lgt_folder}/{dev_folder}/{work_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lgt_folder}/{dev_folder}/{source_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{comp_folder}/{pub_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{comp_folder}/{dev_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{comp_folder}/{dev_folder}/{work_folder}",
    f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{comp_folder}/{dev_folder}/{source_folder}",    

    f"{pipeline_folder}/{scripts_folder}"
]

# create or update folder
def create_or_update_folders(base_path, folders):
    for folder in folders:
        path = os.path.join(base_path, folder)
        
        if os.path.exists(path):
            print(f"Folder already exists: {path}")
        else:
            os.makedirs(path, exist_ok=True)
            print(f"Created: {path}")
            
# excute
create_or_update_folders(base_path, folders)
