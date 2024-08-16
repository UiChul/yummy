#!/bin/bash

# base setting
base_path="/home/rapa/YUMMY" 
project_name="project_name"   

# folder_name
exr_folder="exr"
mov_folder="mov"
IO_folder="I_O"
input_folder="input"
output_folder="output"
plate_folder="plate"
asset_folder="asset"
cha_folder="cha"
env_folder="env"
prop_folder="prop"
weapon_folder="weapon"
matte_folder="matte"
seq_folder="seq"
scene_folder="scene"
shot_folder="shot"
shot_code_folder="shot_code"
match_folder="mm"
ani_folder="ani"
lookdev_folder="ldv"
lgt_folder="lgt"
comp_folder="comp"
dev_folder="dev"
pub_folder="pub"
work_folder="work"
source_folder="source"
pipeline_folder="pipeline"
scripts_folder="scripts"

# folder_structure
folders=(
    "$base_path/project/$project_name/$IO_folder/$input_folder/$plate_folder/$exr_folder"
    "$base_path/project/$project_name/$IO_folder/$input_folder/$plate_folder/$mov_folder"
    "$base_path/project/$project_name/$IO_folder/$output_folder/$plate_folder/$exr_folder"
    "$base_path/project/$project_name/$IO_folder/$output_folder/$plate_folder/$mov_folder"    

    "$base_path/project/$project_name/$asset_folder/$cha_folder/$dev_folder"
    "$base_path/project/$project_name/$asset_folder/$cha_folder/$pub_folder"
    "$base_path/project/$project_name/$asset_folder/$env_folder/$dev_folder"
    "$base_path/project/$project_name/$asset_folder/$env_folder/$pub_folder"
    "$base_path/project/$project_name/$asset_folder/$prop_folder/$dev_folder"
    "$base_path/project/$project_name/$asset_folder/$prop_folder/$pub_folder"
    "$base_path/project/$project_name/$asset_folder/$weapon_folder/$dev_folder"
    "$base_path/project/$project_name/$asset_folder/$weapon_folder/$pub_folder"
    "$base_path/project/$project_name/$asset_folder/$matte_folder/$dev_folder"
    "$base_path/project/$project_name/$asset_folder/$matte_folder/$pub_folder"
    
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$match_folder/$pub_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$match_folder/$dev_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$match_folder/$dev_folder/$work_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$match_folder/$dev_folder/$source_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$ani_folder/$pub_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$ani_folder/$dev_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$ani_folder/$dev_folder/$work_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$ani_folder/$dev_folder/$source_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$lookdev_folder/$pub_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$lookdev_folder/$dev_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$lookdev_folder/$dev_folder/$work_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$lookdev_folder/$dev_folder/$source_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$lgt_folder/$pub_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$lgt_folder/$dev_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$lgt_folder/$dev_folder/$work_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$lgt_folder/$dev_folder/$source_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$comp_folder/$pub_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$comp_folder/$dev_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$comp_folder/$dev_folder/$work_folder"
    "$base_path/project/$project_name/$seq_folder/$scene_folder/$shot_folder/$shot_code_folder/$comp_folder/$dev_folder/$source_folder"
    "$base_path/$pipeline_folder/$scripts_folder"
)

# create or update folder
create_or_update_folders() {
    for folder in "${folders[@]}"; do
        if [ -d "$folder" ]; then
            echo "Folder already exists: $folder"
        else
            mkdir -p "$folder"
            echo "Created: $folder"
        fi
    done
}

# execute
create_or_update_folders
