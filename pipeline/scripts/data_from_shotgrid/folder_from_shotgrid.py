import os, sys
sys.path.append("/home/rapa/python-api")
from shotgun_api3 import shotgun

URL = "https://4thacademy.shotgrid.autodesk.com"
SCRIPT_NAME = "test_hyo"
API_KEY = "ljbgffxqg@cejveci5dQebhdx"

# base path
base_path = "/home/rapa/YUMMY"
project_name = "Marvelous"

def connect_sg():
    global sg
    sg = shotgun.Shotgun(URL,
                         SCRIPT_NAME,
                         API_KEY)

    return sg

def get_project_id(project_name):
    sg = connect_sg()

    filters = [["name", "is", project_name]]
    fields = ["id"]
    project = sg.find_one("Project", filters=filters, fields=fields)

    return project["id"]

def get_sequences_from_project(project_name):
    """
    프로젝트 이름을 키워드로 시퀀스를 가져옴
    """
    sg = connect_sg()
    project_id = get_project_id(project_name)

    if not project_id:
        return []

    filters = [["project.Project.name", "is", project_name]]
    fields = ["id", "code"]
    sequences = sg.find("Sequence", filters=filters, fields=fields)

    return sequences

def get_shots_from_project(project_name):
    """
    프로젝트 이름을 키워드로 시퀀스에 연결된 샷들을 가져옴
    """
    sg = connect_sg()
    project_id = get_project_id(project_name)

    if not project_id:
        return []

    filters = [["project.Project.name", "is", project_name]]
    fields = ["id","code"]
    shots = sg.find("Shot", filters=filters, fields=fields)


    return shots

def get_tasks_from_project(project_name):
    """
    프로젝트 이름 키워드로 tasks를 가져옴
    tasks로 steps(팀 이름)을 가져오기 위함
    """
    sg = connect_sg()
    project_id = get_project_id(project_name)

    if not project_id:
        return []
    
    filters = [["project", "is", {"type": "Project", "id": project_id}]]
    fields = ["id", "content", "step.Step.short_name"]  # "task_assignees.HumanUser.name"

    tasks = sg.find("Task", filters=filters, fields=fields)

    return tasks

def get_steps_from_tasks(project_name):
    """
    tasks의 데이터 중에서 step을 가져옴
    """

    tasks = get_tasks_from_project(project_name)
    steps = set()

    for task in tasks:
        step = task.get("step.Step.short_name")
        if step:
            steps.add(step)

    return steps

def generate_project_folders(project_name, sequences, shots, steps):

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

# {I/O}_{asset}_{pipeline}_folder_structure
    folders = [
        f"project/{project_name}/{IO_folder}/{input_folder}/{plate_folder}/{exr_folder}",
        f"project/{project_name}/{IO_folder}/{input_folder}/{plate_folder}/{mov_folder}",
        f"project/{project_name}/{IO_folder}/{output_folder}/{plate_folder}/{exr_folder}",
        f"project/{project_name}/{IO_folder}/{output_folder}/{plate_folder}/{mov_folder}",

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

# {seq}_{shot}_{step}_folder_structure
    for seq in sequences:
        seq_name = seq.get("code")
        for shot in shots:
            shot_name = shot.get("code")
            for step_name in steps:
                folders.append(f"project/{project_name}/{seq_name}/{shot_name}/{step_name}/dev")
                folders.append(f"project/{project_name}/{seq_name}/{shot_name}/{step_name}/pub")

    return folders

# create or update folder
def create_or_update_folders(base_path, folders):
    for folder in folders:
        path = os.path.join(base_path, folder)
        
        if os.path.exists(path):
            print(f"Folder already exists: {path}")
        else:
            os.makedirs(path, exist_ok=True)
            print(f"Created: {path}")

# 변수 및 폴더 생성 스크립트 실행
sequences = get_sequences_from_project(project_name)
shots = get_shots_from_project(project_name)
tasks = get_tasks_from_project(project_name)
steps = get_steps_from_tasks(project_name) #steps = 각 팀이름

folders = generate_project_folders(project_name, sequences, shots, steps)
create_or_update_folders(base_path, folders)