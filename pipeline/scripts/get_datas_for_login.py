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

def get_projects_by_userID(sg, user_id):
    """
    userID로 할당된 프로젝트 가져오기
    """
    filters =[["task_assignees", "is", {"type": "HumanUser", "id": user_id}]]
    fields = ["project", "step"]
    tasks = sg.find("Task", filters=filters, fields=fields)
    print (tasks)

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
                    "step": set()
                }

            if step:
                step_name = step.get("name")
                if step_name:
                    project_data[project_id]["step"].add(step_name)

    for project_id in project_data:
        project_data[project_id]["step"] = list(project_data[project_id]["step"])

    print (f"프로젝트 데이터는 : {project_data}")
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
    
    user_list = []

    email = input("이메일 입력: ")

    user= get_user_by_email(sg, email)

    if user:
        print(user)
        user_id = user.get("id")

        if user_id:
            projects = get_projects_by_userID(sg, user_id)

            user_data = arrange_user_data_for_json(user, projects)
            user_list.append(user_data)

            save_user_data_to_json(user_data, "login_user_data.json")

    else:
        print("유저 정보를 찾을 수 없습니다")

    

            # if projects:
            #     print (projects)
            #     for project in projects:
            #         print (project["name"])

""" print_result
{'type': 'HumanUser', 'id': 102, 'name': 'hyogi lee', 'email': 'dlgyrl5759@gmail.com', 'permission_rule_set': {'id': 5, 'name': 'Admin', 'type': 'PermissionRuleSet'}}
[{'type': 'Task', 'id': 6225, 'project': {'id': 122, 'name': 'Marvelous', 'type': 'Project'}}, {'type': 'Task', 'id': 6237, 'project': {'id': 192, 'name': 'Yummy', 'type': 'Project'}}]
[]
[{'type': 'Project', 'id': 122, 'name': 'Marvelous'}, {'type': 'Project', 'id': 192, 'name': 'Yummy'}]
Marvelous
Yummy
json 정리 어떻게??
"""
