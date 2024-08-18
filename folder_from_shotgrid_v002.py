import os, sys
# sys.path.append("/home/rapa/python-api")
from shotgun_api3 import shotgun

URL = "https://4thacademy.shotgrid.autodesk.com"
SCRIPT_NAME = "test_hyo"
API_KEY = "ljbgffxqg@cejveci5dQebhdx"

# base path
base_path = "home/rapa/YUMMY"
project_name = "Yummy"

def connect_sg():
    global sg
    sg = shotgun.Shotgun(URL, SCRIPT_NAME, API_KEY)

    return sg

def get_project_id(sg, project_name):
    """
    프로젝트 이름을 키워드로 프로젝트 id 가져오기
    """

    filters = [["name", "is", project_name]]
    fields = ["id"]
    project = sg.find_one("Project", filters=filters, fields=fields)
 
    return project["id"]

def get_sequences_from_project(sg, project_id):
    """
    프로젝트 id를 키워드로 시퀀스를 가져오기
    """

    filters = [["project", "is", {"type": "Project", "id": project_id}]]
    fields = ["id", "code"]
    sequences = sg.find("Sequence", filters=filters, fields=fields)
 
    return sequences

def get_shots_from_sequence(sg, sequence):
    """
    특정 시퀀스에서 샷 가져오기
    """
    sequence_id = sequence["id"]

    filters = [["sg_sequence", "is", {"type": "Sequence", "id": sequence_id}]]
    fields = ["id", "code", "sg_sequence.Sequence.code"]
    shots = sg.find("Shot", filters=filters, fields=fields)

    return shots

def get_tasks_from_project(sg, project_id):
    """
    프로젝트 이름 키워드로 tasks 가져오기
    tasks로 steps(팀 이름)을 가져오기 위함
    """

    if not project_id:
        return []
    
    filters = [["project", "is", {"type": "Project", "id": project_id}]]
    fields = ["id", "content", "step.Step.short_name"]  # "task_assignees.HumanUser.name"
    tasks = sg.find("Task", filters=filters, fields=fields)

    return tasks

def get_steps_from_tasks(tasks):
    """
    tasks의 데이터 중에서 steps(팀 이름) 가져오기
    """
    steps = set()

    for task in tasks:
        step = task.get("step.Step.short_name")
        if step:
            steps.add(step)

    return steps

def get_asset_types_from_project(sg, project_id):
    """
    프로젝트 id 키워드로 asset_type 가져오기
    """
    filters = [["project", "is", {"type": "Project", "id": project_id}]]
    fields = [["id", "code", "sg_asset_type"]]
    asset_types = sg.find("Asset", filters=filters, fields=fields)
    
    return asset_types

def generate_project_folders(project_name, sequences, steps, asset_types):

# folder_name
    exr_folder = "exr"
    mov_folder = "mov"
    IO_folder = "I_O"
    tem_folder = "template"
    clip_lib_foler = "clip_lib"
    node_tem_foler = "node_tem"
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

# {I/O}, {asset}, {pipeline} folder_structure
    folders = [
        f"project/{project_name}/{IO_folder}/{input_folder}/{plate_folder}/{exr_folder}",
        f"project/{project_name}/{IO_folder}/{input_folder}/{plate_folder}/{mov_folder}",
        f"project/{project_name}/{IO_folder}/{output_folder}/{plate_folder}/{exr_folder}",
        f"project/{project_name}/{IO_folder}/{output_folder}/{plate_folder}/{mov_folder}",
        f"project/{project_name}/{tem_folder}/{asset_folder}",
        f"project/{project_name}/{tem_folder}/{shot_folder}/{clip_lib_foler}",
        f"project/{project_name}/{tem_folder}/{shot_folder}/{node_tem_foler}",

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

        f"{pipeline_folder}/{scripts_folder}"
        ]
    
    for asset_type in asset_types:
        folders.append(f"project/{project_name}/{asset_type}")

# {seq}_{shot}_{step}_folder_structure
    for sequence in sequences:
        seq_name = sequence.get("code")
        
        shots = get_shots_from_sequence(sg, sequence)
        
        for shot in shots:
            shot_name = shot.get("code")
            for step_name in steps:
                folders.append(f"project/{project_name}/{seq_folder}/{seq_name}/{shot_name}/{step_name}/dev")
                folders.append(f"project/{project_name}/{seq_folder}/{seq_name}/{shot_name}/{step_name}/pub")
    
    return folders

# create or update folder
def create_or_update_folders(base_path, folders):
    for folder in folders:
        path = os.path.join(base_path, folder)
        
        if os.path.exists(path):
            print(f"{path} 폴더가 이미 존재합니다")
        else:
            os.makedirs(path, exist_ok=True)
            print(f"{path} 폴더가 생성되었습니다")

if __name__ == "__main__":
    sg = connect_sg()
    # 프로젝트 id 한 번만 가져오기
    project_id = get_project_id(sg, project_name)
    
    if project_id:
        sequences = get_sequences_from_project(sg, project_id)
        tasks = get_tasks_from_project(sg, project_id)
        steps = get_steps_from_tasks(tasks)
        asset_types = get_asset_types_from_project(sg, project_id)
        # 폴더 생성 및 업데이트
        folders = generate_project_folders(project_name, sequences, steps, asset_types)
        create_or_update_folders(base_path, folders)
    else:
        print(f"'{project_name}'를 찾을 수 없습니다")