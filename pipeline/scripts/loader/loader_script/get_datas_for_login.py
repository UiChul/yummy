import os
import json
from shotgun_api3 import shotgun

class Signinfo():
    URL = "https://4thacademy.shotgrid.autodesk.com"
    SCRIPT_NAME = "test_hyo"
    API_KEY = "ljbgffxqg@cejveci5dQebhdx"
    
    def __init__(self,email):
        sg = self.connect_sg()
        user= self.get_user_by_email(sg, email)

        user_id = user.get("id")
        if user_id:
            project_entities = self.get_sequences_by_task(sg, user_id)
            projects = self.get_projects_by_userID(sg, user_id,project_entities)
            user_data = self.arrange_user_data_for_json(user, projects)
            self.save_user_data_to_json(user_data, "/home/rapa/yummy/pipeline/json/login_user_data.json")
            print (user_data)

    def connect_sg(self):
        """
        샷그리드 연결
        """
        sg = shotgun.Shotgun(Signinfo.URL, Signinfo.SCRIPT_NAME, Signinfo.API_KEY)

        return sg

    def get_user_by_email(self,sg, email):
        """
        입력된 이메일 정보로 유저 정보 가져오기
        """
        filters = [["email", "is", email]]
        fields = ["id", "name", "email", "permission_rule_set"]
        users = sg.find("HumanUser", filters=filters, fields=fields)
        
        return users[0]

    def get_project_details(self,sg, project_id):
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
    
    def get_sequences_by_task(self,sg, user_id):
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
            
        return project_entities
            

    def get_projects_by_userID(self,sg, user_id,project_entities):
        """
        userID로 할당된 프로젝트 가져오기
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
                    project_details = self.get_project_details(sg, project_id)

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

    def arrange_user_data_for_json(self,user, projects):
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

    def save_user_data_to_json(self,user_data, json_path):
        """
        user_data를 json에 저장
        """
        with open(json_path, "w") as f:
            json.dump(user_data, f, indent=4, ensure_ascii=False)
