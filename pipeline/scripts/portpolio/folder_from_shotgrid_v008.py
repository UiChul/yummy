import os
from shotgun_api3 import Shotgun

# Shotgun API 설정
URL = "https://4thacademy.shotgrid.autodesk.com"
SCRIPT_NAME = "test_hyo"
API_KEY = "ljbgffxqg@cejveci5dQebhdx"

"""
로그인 하는 유저에게 할당된 프로젝트와 태스크에 따라 필요한 폴더만 생성하도록 만든 스크립트
"""

base_path = "/home/rapa/test" #폴더구조를 생성할 경로

def connect_sg():
    
    sg = Shotgun(URL, SCRIPT_NAME, API_KEY)
    return sg

def get_user_by_email(sg, email):
    """
    이메일을 사용하여 유저 정보를 가져오기
    
    email: 검색할 유저의 이메일
    return: 유저 정보가 담긴 딕셔너리 또는 None
    """
    filters = [["email", "is", email]]
    fields = ["id", "name", "email"]
    users = sg.find("HumanUser", filters=filters, fields=fields)
    
    if users:
        return users[0]
    return None

def get_tasks_by_user(sg, user_id):
    """
    유저에게 할당된 태스크 가져오기
    
    user_id: 유저의 ID
    return: 유저에게 할당된 태스크의 리스트
    """
    filters = [["task_assignees", "is", {"type": "HumanUser", "id": user_id}]]
    fields = ["project", "entity", "step", "content"]  # 태스크의 프로젝트 정보
    tasks = sg.find("Task", filters=filters, fields=fields)

    return tasks

def get_project_names_from_tasks(sg, tasks):
    """
    태스크에서 프로젝트 이름을 가져오기
    tasks: 태스크의 리스트
    return: 프로젝트 ID와 이름이 담긴 딕셔너리
    """
    project_ids = set()
    for task in tasks:
        project = task.get("project")
        if project:
            project_ids.add(project.get("id"))

    # 프로젝트 이름을 가져옴
    if project_ids:
        filters = [["id", "in", list(project_ids)]]
        fields = ["name"]
        projects = sg.find("Project", filters=filters, fields=fields)

        project_names = {}
        for project in projects:
            project_id = project.get("id")
            project_name = project.get("name")
            if project_id and project_name:
                project_names[project_id] = project_name

        return project_names
    
    return project_ids, project_names

def get_asset_types_from_projects(sg, project_ids):
    """
    프로젝트 ID 리스트에서 자산 타입과 자산 코드를 가져오기
    project_ids: 프로젝트 ID 리스트
    return: 프로젝트 ID와 자산 타입 및 자산 코드가 담긴 딕셔너리
    """
    project_asset_types = {}
    project_asset_names = {}
    
    for project_id in project_ids:
        filters = [["project", "is", {"type": "Project", "id": project_id}]]
        fields = ["id", "code", "sg_asset_type"]
        assets = sg.find("Asset", filters=filters, fields=fields)
        
        asset_types = set()
        asset_names = set()
        
        for asset in assets:
            asset_type = asset.get("sg_asset_type")
            asset_name = asset.get("code")
            
            if asset_type:
                asset_types.add(asset_type)
            if asset_name:
                asset_names.add(asset_name)
        
        project_asset_types[project_id] = list(asset_types)
        project_asset_names[project_id] = list(asset_names)
    
    return project_asset_types

def get_shots_and_steps_from_tasks(tasks):
    """
    유저에게 할당된 태스크에서 샷과 steps 가져오기
    """
    shot_steps = {}
    for task in tasks:
        entity = task.get("entity")  # ex) {'id': 1306, 'name': 'hyo_010', 'type': 'Shot'}
        step = task.get("step")
        task_name = task.get("content")

        if entity and entity.get("type") == "Shot":
            shot_code = entity.get("name")
            step_name = step.get("name") 

            if shot_code not in shot_steps:
                shot_steps[shot_code] = []

            shot_steps[shot_code].append({"step": step_name, "task": task_name})

    return shot_steps

def display_shot_steps(shot_steps):
    """
    각 샷에 대한 스텝, 태스크 정보를 출력합니다.
    샷 코드와 스텝, 태스크 정보가 담긴 딕셔너리
    """
    for shot_code, steps in shot_steps.items():
        print(f"Shot: {shot_code}")
        for step_info in steps:
            print(f"  Step: {step_info['step']} | Task: {step_info['task']}")
        print("-" * 40)
    """
    Shot: FIN_0010
    Step: mm | Task: FIN_0010_mm
    """

def get_sequences_from_projects(sg, project_ids):
    """
    프로젝트 ID 리스트에서 시퀀스를 가져오기
    project_ids: 프로젝트 ID 리스트
    return: 프로젝트 ID와 시퀀스 데이터가 담긴 딕셔너리
    """
    project_sequences = {}  
    # ex) {122(프로젝트 id): [{'id': 41, 'code': 'OPN', 'shots': [{'id': 1174, 'name': 'OPN_0010', 'type': 'Shot'}
    for project_id in project_ids:
        filters = [["project", "is", {"type": "Project", "id": project_id}]]
        fields = ["id", "code", "shots"]
        sequences = sg.find("Sequence", filters=filters, fields=fields)
        

        seq_data = []
        for seq in sequences:
            seq_id = seq.get("id")
            seq_code = seq.get("code")
            seq_shots = seq.get("shots", [])
            seq_data.append({"id": seq_id, "code": seq_code, "shots": seq_shots})
    
        project_sequences[project_id] = seq_data
    return project_sequences

def get_shot_codes_for_sequences(sequences):
    """
    시퀀스의 shots 필드에서 샷 코드를 가져오기
    sequences: 시퀀스 데이터 리스트 [{id: 시퀀스 ID, code: 시퀀스 코드, shots: 샷들}]
    return: 시퀀스 코드와 샷 코드가 담긴 딕셔너리
    """
    seq_shot_codes = {} # ex) 'OPN': ['OPN_0010', 'OPN_0020', 'OPN_0030']

    for sequence in sequences:
        seq_code = sequence.get("code")
       
        if seq_code:
            shots = sequence.get("shots", [])

            shot_codes = []
            for shot in shots:
                shot_code = shot.get("name")
                shot_codes.append(shot_code)

            seq_shot_codes[seq_code] = shot_codes
    
    return seq_shot_codes

def create_folders(base_path, project_names, project_asset_types, project_sequences, seq_shot_codes, shot_steps):
    """
    프로젝트, 시퀀스, 샷 데이터를 바탕으로 폴더 구조 생성하기
    base_path: 기본 경로
    project_names: 프로젝트 ID와 이름이 담긴 딕셔너리
    project_asset_types: 프로젝트 ID와 자산 타입이 담긴 딕셔너리
    project_sequences: 프로젝트 ID와 시퀀스 데이터가 담긴 딕셔너리
    seq_shot_codes: 시퀀스 코드와 샷 코드가 담긴 딕셔너리
    shot_step: 샷 코드와 그에 따른 스텝 정보가 담긴 딕셔너리
    """
    exr_folder = "exr"
    mov_folder = "mov"
    IO_folder = "I_O"
    tem_folder = "template"
    clip_lib_folder = "clip_lib"
    node_tem_folder = "node_tem"
    input_folder = "input"
    output_folder = "output"
    plate_folder = "plate"
    asset_folder = "asset"
    cha_folder = "cha"
    env_folder = "env"
    prop_folder = "prop"
    weapon_folder = "weapon"
    matte_folder = "matte"
    mod_folder = "mod"
    rig_folder = "rig"
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
    json_folder = "json"

    folders = []
    for project_id, project_name in project_names.items():
        # I_O 폴더와 tem, pipeline 폴더 생성
        folders = [
            f"project/{project_name}/{IO_folder}/{input_folder}/{plate_folder}/{exr_folder}",
            f"project/{project_name}/{IO_folder}/{input_folder}/{plate_folder}/{mov_folder}",
            f"project/{project_name}/{IO_folder}/{output_folder}/{plate_folder}/{exr_folder}",
            f"project/{project_name}/{IO_folder}/{output_folder}/{plate_folder}/{mov_folder}",
            f"project/{project_name}/{tem_folder}/{asset_folder}",
            f"project/{project_name}/{tem_folder}/{shot_folder}/{clip_lib_folder}",
            f"project/{project_name}/{tem_folder}/{shot_folder}/{node_tem_folder}",

            f"{pipeline_folder}/{scripts_folder}",
            f"{pipeline_folder}/{json_folder}"
            ]
        
        # 어셋 타입 폴더 생성
        asset_types = project_asset_types.get(project_id, [])
        for asset_type in asset_types:
            asset_type_path = f"project/{project_name}/{asset_folder}/{asset_type}"
            folders.append(asset_type_path)

            # asset_type 폴더 아래에 mod와 rig 폴더 추가
            mod_path = os.path.join(asset_type_path, mod_folder)
            rig_path = os.path.join(asset_type_path, rig_folder)
            folders.append(mod_path)
            folders.append(rig_path)

            # mod와 rig 폴더 아래에 각각 dev와 pub 폴더 추가
            mod_dev_path = os.path.join(mod_path, dev_folder)
            mod_pub_path = os.path.join(mod_path, pub_folder)
            rig_dev_path = os.path.join(rig_path, dev_folder)
            rig_pub_path = os.path.join(rig_path, pub_folder)
            folders.append(mod_dev_path)
            folders.append(mod_pub_path)
            folders.append(rig_dev_path)
            folders.append(rig_pub_path)

        # 각 시퀀스별로 폴더 생성
        sequences = project_sequences.get(project_id, [])
        for sequence in sequences:
            seq_code = sequence.get("code")
            if seq_code:
                seq_path = f"project/{project_name}/{seq_folder}/{seq_code}" #step 추가, dev_pub 추가
                folders.append(seq_path)
                
                # 각 시퀀스의 샷별로 폴더 생성
                shot_codes = seq_shot_codes.get(seq_code, [])
                for shot_code in shot_codes:
                    shot_path = os.path.join(seq_path, shot_code)
                    folders.append(shot_path)
                    
                    # 샷 코드에 해당하는 step 폴더 생성
                    steps_for_shot = shot_steps.get(shot_code, [])
                    for step_info in steps_for_shot:
                        step_name = step_info.get("step")
                        if step_name:
                            step_path = os.path.join(shot_path, step_name)
                            folders.append(step_path)
                            
                            # 추가적으로 work, pub 폴더 생성
                            shot_dev_path = os.path.join(step_path, dev_folder)
                            shot_pub_path = os.path.join(step_path, pub_folder)
                            folders.append(shot_dev_path)
                            folders.append(shot_pub_path)

                            step_dev_exr_path = os.path.join(shot_dev_path, exr_folder)
                            step_dev_mov_path = os.path.join(shot_dev_path, mov_folder)
                            step_dev_work_path = os.path.join(shot_dev_path, work_folder)
                            folders.append(step_dev_exr_path)
                            folders.append(step_dev_mov_path)
                            folders.append(step_dev_work_path)
        
        # 폴더 생성
        for folder in folders:
            path = os.path.join(base_path, folder)
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                print(f"{path} 폴더가 생성되었습니다.")
            else:
                print(f"{path} 폴더가 이미 존재합니다.")
    
    return folders

if __name__ == "__main__":
    
    sg = connect_sg()
    
    # 사용자 이메일 입력 및 유저 정보 가져오기(로그인할 때 받는 유저 이메일)
    email = input("이메일 입력: ")
    user = get_user_by_email(sg, email)
    
    if user:
        user_id = user.get("id")
        if user_id:
            tasks = get_tasks_by_user(sg, user_id)
            project_names = get_project_names_from_tasks(sg, tasks)
            project_ids = list(project_names.keys())
            project_sequences = get_sequences_from_projects(sg, project_ids)
            all_sequences = [seq for sequences in project_sequences.values() for seq in sequences]
            seq_shot_codes = get_shot_codes_for_sequences(all_sequences)
            shot_steps = get_shots_and_steps_from_tasks(tasks)
            project_asset_types = get_asset_types_from_projects(sg, project_ids)
            display_shot_steps(shot_steps)
            # 폴더 생성
            create_folders(base_path, project_names, project_asset_types, project_sequences, seq_shot_codes, shot_steps)
        else:
            print("유저 ID를 찾을 수 없습니다.")
    else:
        print("유저 정보를 찾을 수 없습니다.")