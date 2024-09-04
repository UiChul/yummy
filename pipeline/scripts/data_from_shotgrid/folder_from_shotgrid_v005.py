import os
from shotgun_api3 import Shotgun

# Shotgun API 설정
URL = "https://4thacademy.shotgrid.autodesk.com"
SCRIPT_NAME = "test_hyo"
API_KEY = "ljbgffxqg@cejveci5dQebhdx"

base_path = "/home/rapa/YUMMY"

def connect_sg():
    """
    Shotgun에 연결하고 Shotgun API 객체를 반환합니다.
    """
    sg = Shotgun(URL, SCRIPT_NAME, API_KEY)
    return sg

def get_user_by_email(sg, email):
    """
    이메일을 사용하여 유저 정보를 가져옵니다.
    
    :param sg: Shotgun API 객체
    :param email: 검색할 유저의 이메일
    :return: 유저 정보가 담긴 딕셔너리 또는 None
    """
    filters = [["email", "is", email]]
    fields = ["id", "name", "email"]
    users = sg.find("HumanUser", filters=filters, fields=fields)
    
    if users:
        return users[0]
    return None

def get_tasks_by_user(sg, user_id):
    """
    유저에게 할당된 태스크를 가져옵니다.
    
    :param sg: Shotgun API 객체
    :param user_id: 유저의 ID
    :return: 유저에게 할당된 태스크의 리스트
    """
    filters = [["task_assignees", "is", {"type": "HumanUser", "id": user_id}]]
    fields = ["project"]  # 태스크의 프로젝트 정보
    tasks = sg.find("Task", filters=filters, fields=fields)
    print (tasks)
    return tasks

def get_project_names_from_tasks(sg, tasks):
    """
    태스크에서 프로젝트 이름을 가져옵니다.
    
    :param sg: Shotgun API 객체
    :param tasks: 태스크의 리스트
    :return: 프로젝트 ID와 이름이 담긴 딕셔너리
    """
    project_ids = set()
    for task in tasks:
        project = task.get("project")
        if project:
            project_ids.add(project.get("id"))

    print (list(project_ids))
    # 프로젝트 이름을 가져옴
    if project_ids:
        filters = [["id", "in", list(project_ids)]]
        fields = ["name"]
        projects = sg.find("Project", filters=filters, fields=fields)
        print (projects)
        project_names = {}
        for project in projects:
            project_id = project.get("id")
            project_name = project.get("name")
            if project_id and project_name:
                project_names[project_id] = project_name

        print (project_names)
        return project_names
    
    return project_ids, project_names

def get_sequences_from_projects(sg, project_ids):
    """
    프로젝트 ID 리스트에서 시퀀스를 가져옵니다.
    
    :param sg: Shotgun API 객체
    :param project_ids: 프로젝트 ID 리스트
    :return: 프로젝트 ID와 시퀀스 데이터가 담긴 딕셔너리
    """
    project_sequences = {}
    for project_id in project_ids:
        filters = [["project", "is", {"type": "Project", "id": project_id}]]
        fields = ["id", "code", "shots"]
        sequences = sg.find("Sequence", filters=filters, fields=fields)
        print ("nooooooo", sequences)
        seq_data = []
        for seq in sequences:
            seq_id = seq.get("id")
            seq_code = seq.get("code")
            seq_shots = seq.get("shots", [])
            seq_data.append({"id": seq_id, "code": seq_code, "shots": seq_shots})
        
        project_sequences[project_id] = seq_data
    print ("yssss", project_sequences)
    return project_sequences

def get_shot_codes_for_sequences(sequences):
    """
    시퀀스의 shots 필드에서 샷 코드를 가져옵니다.
    
    :param sequences: 시퀀스 데이터 리스트 [{id: 시퀀스 ID, code: 시퀀스 코드, shots: 샷들}]
    :return: 시퀀스 코드와 샷 코드가 담긴 딕셔너리
    """
    seq_shot_codes = {}
    for sequences in project_sequences.values():
        print ("heyyyyyyyyyyyyy", sequences)
        for sequence in sequences:
            seq_code = sequence.get("code")
            print ("시퀀스 코오오오드", seq_code)
            if seq_code:
                shots = sequence.get("shots", [])
                print ("샤아아아아아앗", shots)
                shot_codes = []
                for shot in shots:
                    shot_code = shot.get("name")
                    shot_codes.append(shot_code)
                print ("샷코오오오오드", shot_codes)            
                seq_shot_codes[seq_code] = shot_codes

    print ("시퀀스 샷 코드으으으으", seq_shot_codes)
    
    return seq_shot_codes

def create_folders(base_path, project_names, project_sequences, seq_shot_codes):
    """
    프로젝트, 시퀀스, 샷 데이터를 바탕으로 폴더 구조를 생성합니다.
    
    :param base_path: 기본 경로
    :param project_names: 프로젝트 ID와 이름이 담긴 딕셔너리
    :param project_sequences: 프로젝트 ID와 시퀀스 데이터가 담긴 딕셔너리
    :param seq_shot_codes: 시퀀스 코드와 샷 코드가 담긴 딕셔너리
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

            f"{pipeline_folder}/{scripts_folder}"
        ]
        
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
    # Shotgun에 연결
    sg = connect_sg()
    
    # 사용자 이메일 입력 및 유저 정보 가져오기
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
            
            # 폴더 생성
            create_folders(base_path, project_names, project_sequences, seq_shot_codes)
        else:
            print("유저 ID를 찾을 수 없습니다.")
    else:
        print("유저 정보를 찾을 수 없습니다.")