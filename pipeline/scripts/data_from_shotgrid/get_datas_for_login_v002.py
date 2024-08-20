import json
from shotgun_api3 import shotgun

URL = "https://4thacademy.shotgrid.autodesk.com"
SCRIPT_NAME = "test_hyo"
API_KEY = "ljbgffxqg@cejveci5dQebhdx"

def connect_sg():
    """
    샷그리드 연결
    """
    sg = shotgun.Shotgun(URL, SCRIPT_NAME, API_KEY)
    return sg

def get_user_by_email(sg, email):
    """
    입력된 이메일 정보로 유저 정보 가져오기
    """
    filters = [["email", "is", email]]
    fields = ["id", "name", "email", "permission_rule_set"]
    users = sg.find("HumanUser", filters=filters, fields=fields)
    
    if users:
        return users[0]
    return None

def get_project_details(sg, project_id):
    """
    특정 프로젝트의 해상도와 상태 정보를 가져오는 함수
    """
    filters = [["id", "is", project_id]]
    fields = ["sg_resolutin_width", "sg_resolution_height", "sg_status"]
    project = sg.find_one("Project", filters=filters, fields=fields)

    if project:
        return {
            "resolution_width": project.get("sg_resolutin_width", "N/A"),
            "resolution_height": project.get("sg_resolution_height", "N/A"),
            "status": project.get("sg_status", "N/A")
        }
    return None

# def get_sequences_by_task(sg, user_id):
#     """
#     사용자에게 할당된 태스크에서 시퀀스와 그 시퀀스의 코드 가져오기
#     """
#     filters = [["task_assignees", "is", {"type": "HumanUser", "id": user_id}]]
#     fields = ["entity"]
#     tasks = sg.find("Task", filters=filters, fields=fields)

#     # 태스크에서 할당된 시퀀스 ID를 수집
#     sequence_ids = set()
#     for task in tasks:
#         entity = task.get("entity")
#         if entity:
#             entity_name = entity.get("name")
#             sequence_ids.add(entity_name)

#     print (list(sequence_ids))
#     # 시퀀스 ID로 시퀀스 코드 조회
#     sequences_dict = {}
#     if sequence_ids:
#         filters = [["id", "in", list(sequence_ids)]]
#         fields = ["id", "code"]
#         sequences = sg.find("Sequence", filters=filters, fields=fields)
#         for seq in sequences:
#             seq_id = seq.get("id")
#             seq_code = seq.get("code", "Unnamed Sequence")
#             if seq_id:
#                 sequences_dict[seq_id] = seq_code

#     print(f"Sequences found: {sequences_dict}")  # 디버깅을 위한 출력

#     return sequences_dict

def get_sequences_by_task(sg, user_id):
    """
    사용자에게 할당된 태스크에서 시퀀스와 그 시퀀스의 코드 가져오기
    """
    # 태스크 필터 설정
    filters = [["task_assignees", "is", {"type": "HumanUser", "id": user_id}]]
    fields = ["entity", "project"]
    tasks = sg.find("Task", filters=filters, fields=fields)

    # 프로젝트별 엔티티 이름 수집
    project_entities = {}
    for task in tasks:
        entity = task.get("entity")
        project = task.get("project")
        
        if entity and project:
            project_id = project.get("id")
            entity_name = entity.get("name")
            
            if project_id:
                if project_id not in project_entities:
                    project_entities[project_id] = {"project_name": project.get("name"), "entities": set()}
                
                project_entities[project_id]["entities"].add(entity_name)

    for project_id, info in project_entities.items():
        info["entities"] = list(info["entities"])

    print (project_entities)

    return project_entities

def get_projects_by_userID(sg, user_id, project_entities):
    """
    userID로 할당된 프로젝트 가져오기 및 각 shot_code에 step을 할당하기
    """
    filters = [["task_assignees", "is", {"type": "HumanUser", "id": user_id}]]
    fields = ["project", "step", "entity"]
    tasks = sg.find("Task", filters=filters, fields=fields)

    project_data = {}
    # sequences_dict = get_sequences_by_task(sg, user_id)

    for task in tasks:
        project = task.get("project")
        entity = task.get("entity")
        step = task.get("step")
        
        # Entity 이름 가져오기
        entity_name = entity.get("name") if entity else "Unknown Entity"

        if project and project.get("id"):
            project_id = project.get("id")
            project_name = project.get("name")

            if project_id not in project_data:
                project_details = get_project_details(sg, project_id)

                project_data[project_id] = {
                    "id": project_id,
                    "name": project_name,
                    **project_details,
                    "shot_code": {}, 
                }

            # shot code에 맞는 step 추가
            if entity_name:
                if entity_name not in project_data[project_id]["shot_code"]:
                    project_data[project_id]["shot_code"][entity_name] = {
                        "steps": []  # Initialize steps as a list for each shot_code
                    }

                # step 리스트에 step 추가
                if step:
                    step_name = step.get("name")
                    if step_name and step_name not in project_data[project_id]["shot_code"][entity_name]["steps"]:
                        project_data[project_id]["shot_code"][entity_name]["steps"].append(step_name)

    for project_id in project_data:
        if project_id in project_entities:
            
            for entity_name in project_entities[project_id]["entities"]:
                if entity_name not in project_data[project_id]["shot_code"]:
                    project_data[project_id]["shot_code"][entity_name] = {
                        "steps": []
                    }

    return list(project_data.values())

def arrange_user_data_for_json(user, projects):
    """
    유저 정보와 할당된 프로젝트 정보 json 출력을 위한 정리
    """
    user_data = {
        "user_id": user["id"],
        "user_name": user["name"],
        "user_email": user["email"],
        "user_permission_group": user.get("permission_rule_set", {}).get("name"),
        "projects": projects
    }
    print (user_data)
    return user_data

def save_user_data_to_json(user_data, json_path):
    """
    user_data를 json에 저장
    """
    with open(json_path, "w") as f:
        json.dump(user_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    sg = connect_sg()
    
    email = input("이메일 입력: ")
    user = get_user_by_email(sg, email)
    if user:
        user_id = user.get("id")
        if user_id:
            project_entities = get_sequences_by_task(sg, user_id)
            projects = get_projects_by_userID(sg, user_id, project_entities)
            user_data = arrange_user_data_for_json(user, projects)
            save_user_data_to_json(user_data, "login_user_data.json")
            print(user_data)
    else:
        print("유저 정보를 찾을 수 없습니다")
