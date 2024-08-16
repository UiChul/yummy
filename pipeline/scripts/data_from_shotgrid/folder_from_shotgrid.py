import os, sys
sys.path.append("/home/rapa/python-api")
from shotgun_api3 import shotgun

URL = "https://4thacademy.shotgrid.autodesk.com"
SCRIPT_NAME = "test_hyo"
API_KEY = "ljbgffxqg@cejveci5dQebhdx"

# base path
base_path = "/home/rapa/YUMMY"
project_name = "project_name"

def connect_sg():

    sg = shotgun.Shotgun(URL,
                         SCRIPT_NAME,
                         API_KEY)
    return sg

def get_project_id(project_name):
    sg = connect_sg()
    filters = [["name", "is", project_name]]
    fields = [["id"]]
    project = sg.find_one("Project", filters, fields)
    return project["id"]

# def create_sequence_in_shotgrid(sequence_name, project_id):
#     sg = connect_sg()
#     data = {
#         "project": {"type": "Project", "id": project_id},
#         "code" : sequence_name,
#     }
#     sequence = sg.create("Sequence", data)
#     return sequence

# def create_shot_in_shotgrid(shot_name, sequence_id, project_id):
#     sg = connect_sg()
#     data = {
#         "project": {"type": "Project", "id": project_id},
#         "code": shot_name,
#         "sg_sequence": {"type": "Sequence", "id": sequence_id},
#     }
#     shot = sg.create("Shot", data)
#     return shot

# # local to shotgrid (sequence, shot)
# def create_folders_connect_shotgrid(sequence_name, shot_name):
#     project_id = get_project_id(project_name)

#     sequence_path = os.path.join(base_path, "project", project_name, sequence_name)
#     shot_path = os.path.join(sequence_path, shot_name)

#     os.makedir(shot_path, exist_ok=True)
#     print (f"Created local folders: {sequence_path}, {shot_path}")

#     sequence = create_sequence_in_shotgrid(sequence_name, project_id)
#     print (f"Created sequence in Shotgrid: {sequence["code"]}")

#     shot = create_shot_in_shotgrid(shot_name, sequence["id"])

def get_sequence_data_from_shots(project_name):
    """
    get_shots_from_sequence랑 사실 비슷한대 이 코드는 샷에서
    테스크 정보를 더 찾아오기 때문에 각 테스크에 어싸인된 유저이름과 아이디가 추가됨.
    근대 아직 수정중이긴함, 근대 되긴함
    """
    sg = connect_sg()
    filters = [["project.Project.name", "is", project_name]]
    fields = ["id", "code"]
    sequences = sg.find("Sequence", filters=filters, fields=fields)

    return sequences

def get_shots_from_project(project_name):
    """
    시퀀스 이름을 키워드로 시퀀스에 연결된 샷들을 가져온.
    """
    sg = connect_sg()

    filters = [["project.Project.name", "is", project_name]]
    fields = ["id","code"]
    shots = sg.find("Shot", filters=filters, fields=fields)
    print (shots)
    return shots
def generate_project_folders(project_name, sequences, shots):

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

        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{match_folder}/{pub_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{match_folder}/{dev_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{match_folder}/{dev_folder}/{work_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{match_folder}/{dev_folder}/{source_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{ani_folder}/{pub_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{ani_folder}/{dev_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{ani_folder}/{dev_folder}/{work_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{ani_folder}/{dev_folder}/{source_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lookdev_folder}/{pub_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lookdev_folder}/{dev_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lookdev_folder}/{dev_folder}/{work_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lookdev_folder}/{dev_folder}/{source_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lgt_folder}/{pub_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lgt_folder}/{dev_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lgt_folder}/{dev_folder}/{work_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{lgt_folder}/{dev_folder}/{source_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{comp_folder}/{pub_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{comp_folder}/{dev_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{comp_folder}/{dev_folder}/{work_folder}",
        # f"project/{project_name}/{seq_folder}/{scene_folder}/{shot_folder}/{shot_code_folder}/{comp_folder}/{dev_folder}/{source_folder}",    

        f"{pipeline_folder}/{scripts_folder}"
        ]

    for seq in sequences:
        seq_name = seq.get("code")
        for shot in shots:
            shot_name = shot.get("code")
            folders.append(f"project/{project_name}/{seq_name}/{shot_name}/shot_000")
            folders.append(f"project/{project_name}/{seq_name}/{shot_name}/shot_010")
            folders.append(f"project/{project_name}/{seq_name}/{shot_name}/shot_020")   
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
            
shots = get_shots_from_project(project_name="Yummy")
sequences = get_sequence_data_from_shots(project_name="Yummy")
print (shots)
print (sequences)

folders = generate_project_folders(project_name="Yummy", sequences=sequences, shots=shots)
create_or_update_folders(base_path, folders)