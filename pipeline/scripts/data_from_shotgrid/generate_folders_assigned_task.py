import os
import sys
from shotgun_api3 import Shotgun

# ShotGrid API 정보 설정
URL = "https://4thacademy.shotgrid.autodesk.com"
SCRIPT_NAME = "test_hyo"
API_KEY = "ljbgffxqg@cejveci5dQebhdx"

# 기본 경로 설정
base_path = "/home/rapa/YUMMY"

def connect_sg():
    """
    샷그리드 연결
    """
    sg = Shotgun(URL, SCRIPT_NAME, API_KEY)
    return sg

def get_user_by_email(sg, email):
    """
    이메일로 유저 정보 가져오기
    """
    filters = [["email", "is", email]]
    fields = ["id", "name", "email", "permission_rule_set"]
    users = sg.find("HumanUser", filters=filters, fields=fields)
    return users[0] if users else None

def get_projects_by_userID(sg, user_id):
    """
    유저 ID로 할당된 프로젝트 가져오기
    """
    filters = [["task_assignees", "is", {"type": "HumanUser", "id": user_id}]]
    fields = ["project", "step", "id"]
    tasks = sg.find("Task", filters=filters, fields=fields)
    
    project_data = {}

    for task in tasks:
        project = task.get("project")
        step = task.get("step")

        if project and project.get("id"):
            project_id = project.get("id")
            project_name = project.get("name")

            if project_id not in project_data:
                project_data[project_id] = {
                    "name": project_name,
                    "steps": set(),
                    "id": project_id
                }

            if step:
                step_name = step.get("name")
                if step_name:
                    project_data[project_id]["steps"].add(step_name)

    # 중복 제거 후 리스트로 변환
    for project_id in project_data:
        project_data[project_id]["steps"] = list(project_data[project_id]["steps"])

    return list(project_data.values())

def get_asset_types_from_project(sg, project_id):
    """
    프로젝트 ID로 Asset Type 가져오기
    """
    filters = [["project", "is", {"type": "Project", "id": project_id}]]
    fields = ["id", "code", "sg_asset_type"]
    try:
        asset_types = sg.find("Asset", filters=filters, fields=fields)
        print(f"Asset Types for project {project_id}: {asset_types}")  # 디버깅
    except Exception as e:
        print(f"Asset 타입을 가져오는 중 오류 발생: {e}")
        asset_types = []
    
    return asset_types

def get_shots_from_sequence(sg, sequence):
    """
    특정 시퀀스에서 샷 가져오기
    """
    sequence_id = sequence["id"]
    filters = [["sg_sequence", "is", {"type": "Sequence", "id": sequence_id}]]
    fields = ["id", "code"]
    try:
        shots = sg.find("Shot", filters=filters, fields=fields)
        print(f"Shots for sequence {sequence_id}: {shots}")  # 디버깅
    except Exception as e:
        print(f"샷을 가져오는 중 오류 발생: {e}")
        shots = []
    
    return shots

def get_sequences_from_project(sg, project_id):
    """
    프로젝트 ID를 통해 시퀀스를 가져오는 함수
    """
    if not project_id:
        raise ValueError("프로젝트 ID가 제공되지 않았습니다.")
    
    filters = [["project", "is", {"type": "Project", "id": project_id}]]
    fields = ["id", "code"]
    try:
        sequences = sg.find("Sequence", filters=filters, fields=fields)
        print(f"Sequences for project {project_id}: {sequences}")  # 디버깅
    except Exception as e:
        print(f"시퀀스를 가져오는 중 오류 발생: {e}")
        sequences = []
    
    return sequences

def get_steps_from_assets(sg, project_id):
    """
    프로젝트 ID로 Asset에서 step 이름 가져오기
    """
    filters = [["project", "is", {"type": "Project", "id": project_id}]]
    fields = ["id", "sg_asset_type", "step.Step.short_name"]
    try:
        assets = sg.find("Asset", filters=filters, fields=fields)
        print(f"Assets for project {project_id}: {assets}")  # 디버깅
    except Exception as e:
        print(f"Asset에서 스텝을 가져오는 중 오류 발생: {e}")
        assets = []
    
    steps = set()
    for asset in assets:
        step_info = asset.get("step")
        if step_info:
            step_name = step_info.get("short_name")
            if step_name:
                steps.add(step_name)

    return steps

def generate_project_folders(project_name, sequences, steps, asset_types, asset_steps):
    """
    프로젝트 이름과 스텝 정보로 폴더 구조 생성
    """
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
    
    folders = [
        f"project/{project_name}/{IO_folder}/{input_folder}/{plate_folder}/{exr_folder}",
        f"project/{project_name}/{IO_folder}/{input_folder}/{plate_folder}/{mov_folder}",
        f"project/{project_name}/{IO_folder}/{output_folder}/{plate_folder}/{exr_folder}",
        f"project/{project_name}/{IO_folder}/{output_folder}/{plate_folder}/{mov_folder}",
        f"project/{project_name}/{tem_folder}/{asset_folder}",
        f"project/{project_name}/{tem_folder}/{shot_folder}/{clip_lib_foler}",
        f"project/{project_name}/{tem_folder}/{shot_folder}/{node_tem_foler}",
        f"{pipeline_folder}/{scripts_folder}"
    ]

    # 모든 유저가 접근할 수 있는 Asset 폴더 생성 (asset_type 뒤에 각 asset의 step_name 추가)
    for asset_type in asset_types:
        asset_type_name = asset_type.get("sg_asset_type")
        if asset_type_name:
            for step_name in asset_steps:
                folders.append(f"project/{project_name}/{asset_folder}/{asset_type_name}/{step_name}/")
                print(f"Adding folder: project/{project_name}/{asset_folder}/{asset_type_name}/{step_name}/")  # 디버깅

    # 유저가 할당된 Step에 따른 폴더 생성
    for sequence in sequences:
        seq_name = sequence.get("code")
        shots = get_shots_from_sequence(sg, sequence)
        
        for shot in shots:
            shot_name = shot.get("code")
            for step_name in steps:
                folders.append(f"project/{project_name}/{seq_folder}/{seq_name}/{shot_name}/{step_name}/{dev_folder}/{work_folder}")
                folders.append(f"project/{project_name}/{seq_folder}/{seq_name}/{shot_name}/{step_name}/{dev_folder}/{source_folder}")
                folders.append(f"project/{project_name}/{seq_folder}/{seq_name}/{shot_name}/{step_name}/{pub_folder}")
    
    print(f"Generated folders: {folders}")  # 디버깅
    return folders

def create_or_update_folders(base_path, folders):
    """
    폴더 생성 또는 업데이트
    """
    for folder in folders:
        path = os.path.join(base_path, folder)
        if os.path.exists(path):
            print(f"{path} 폴더가 이미 존재합니다")
        else:
            os.makedirs(path, exist_ok=True)
            print(f"{path} 폴더가 생성되었습니다")

if __name__ == "__main__":
    sg = connect_sg()

    # 이메일 입력 받기
    email = input("이메일 입력: ")

    user = get_user_by_email(sg, email)

    if user:
        user_id = user.get("id")
        projects = get_projects_by_userID(sg, user_id)

        for project in projects:
            project_name = project.get("name")
            steps = project.get("steps")
            print(f"프로젝트: {project_name}, 스텝: {steps}")

            # Asset 타입과 관련 스텝 가져오기
            project_id = project.get("id")
            asset_types = get_asset_types_from_project(sg, project_id)
            asset_steps = get_steps_from_assets(sg, project_id)
            sequences = get_sequences_from_project(sg, project_id)

            # 유저가 할당된 스텝만 폴더 생성
            folders = generate_project_folders(project_name, sequences, steps, asset_types, asset_steps)
            create_or_update_folders(base_path, folders)
    else:
        print("유저 정보를 찾을 수 없습니다.")
