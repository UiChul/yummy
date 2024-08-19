import os
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
    
    return users[0]

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

def get_projects_by_userID(sg, user_id):
    """
    userID로 할당된 프로젝트 가져오기
    """
    filters =[["task_assignees", "is", {"type": "HumanUser", "id": user_id}]]
    fields = ["project", "step", "id"]
    tasks = sg.find("Task", filters=filters, fields=fields)

    project_data = {}

    for task in tasks:
        project = task.get("project")
        step = task.get("step")

        if project and project.get("id"):
            project_id = project.get("id")
            project_name = project.get("name")

            project_details = get_project_details(sg, project_id)

            if project_id not in project_data:
                project_data[project_id] = {
                    "name": project_name,
                    "step": set(),
                    "id" : project_id,
                    **project_details
                }

            if step:
                step_name = step.get("name")
                if step_name:
                    project_data[project_id]["step"].add(step_name)

    for project_id in project_data:
        project_data[project_id]["step"] = list(project_data[project_id]["step"])

    return list(project_data.values())

def arrange_user_data_for_json(user, projects):
    """
    유저 정보와 할당된 프로젝트 정보 json 출력을 위한 정리
    """
    user_data = {

        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "permission_group": user.get("permission_rule_set", {}).get("name"),
        "projects": projects
    }

    return user_data

def save_user_data_to_json(user_data, json_path):
    """
    user_data를 json에 저장
    """
    with open(json_path, "w") as f:
        json.dump(user_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    sg = connect_sg()
    
    user_list = []

    email = input("이메일 입력: ")

    user= get_user_by_email(sg, email)

    if user:
        user_id = user.get("id")

        if user_id:
            projects = get_projects_by_userID(sg, user_id)

            user_data = arrange_user_data_for_json(user, projects)

            save_user_data_to_json(user_data, "login_user_data.json")

            print (user_data)
    else:
        print("유저 정보를 찾을 수 없습니다")