import json
from shotgun_api3 import shotgun
from datetime import datetime

URL = "https://4thacademy.shotgrid.autodesk.com"
SCRIPT_NAME = "test_hyo"
API_KEY = "ljbgffxqg@cejveci5dQebhdx"

class OpenLoaderData():
    def __init__(self):
        print ("hello world")
        
    def connect_sg(self):
        """
        샷그리드 연결
        """
        self.sg = shotgun.Shotgun(URL, SCRIPT_NAME, API_KEY)
        return self.sg

    def read_data_from_login_json(self):
        """
        로그인 단계에서 저장된 json 데이터 중
        project_id, project_name 가져오기
        """
        selected_project = input("프로젝트 이름: ")
        json_load_path = "/home/rapa/yummy/pipeline/json/login_user_data.json"

        with open(json_load_path, "r", encoding="utf-8") as f:
            user_data = json.load(f)

        for project in user_data.get("projects", []):
            project_name = project.get("name")
            project_id = project.get("id")

            if project_name == selected_project:
                    return project_id

        return None

    def get_asset_datas(self, project_id):
        """
        project_id로 어셋 템플릿 패스 가져오기
        """
        asset_datas = []

        if project_id:
            filters = [["project", "is", {"type": "Project", "id": project_id}]]
            fields = ["code", "sg_asset_path", "tasks"]
            try:
                assets = self.sg.find("Asset", filters=filters, fields=fields)
            except Exception as e:
                print(f"Failed to retrieve assets: {e}")
                return []

            for asset in assets:
                asset_name = asset.get("code", "N/A")
                asset_path = asset.get("sg_asset_path", "N/A")
                asset_tasks = asset.get("tasks", [])

                asset_task = "N/A"
                asset_assignees = "N/A"
                asset_step = "N/A"

                if asset_tasks:
                    for task in asset_tasks:
                        task_id = task.get("id")

                        task_data = self.sg.find_one("Task", [["id", "is", task_id]], ["content", "task_assignees", "step"])

                        # 태스크 디테일
                        task_content = task_data.get("content", "N/A")
                        task_assignees = task_data.get("task_assignees", [])
                        task_step = task_data.get("step", "N/A")

                        assignee_names = []
                        for assignee in task_assignees:
                            assignee_name = assignee.get("name", "Unknown")
                            assignee_names.append(assignee_name)

                        asset_task = task_content
                        asset_assignees = ", ".join(assignee_names)
                        asset_step = task_step.get("name")

                asset_datas.append({
                    "asset_name": asset_name,
                    "asset_path": asset_path,
                    "asset_task": asset_task,
                    "asset_assignees": asset_assignees,
                    "asset_step": asset_step
                })

        return asset_datas

    
    def get_versions_data(self, project_id):
        """
        프로젝트의 versions 데이터 가져오기
        """
        ver_datas = []

        if project_id:
            filters = [["project", "is", {"type": "Project", "id": project_id}]]
            fields = ["code", "entity", "sg_version_type", "description", "sg_status_list", "user"]
            versions = self.sg.find("Version", filters=filters, fields=fields)

            for version in versions:
                code = version.get("code", "N/A")
                entity = version.get("entity", {}).get("name", "N/A")
                version_type = version.get("sg_version_type", "N/A")
                description = version.get("description", "N/A")
                sg_status_list = version.get("sg_status_list", "N/A")
                user = version.get("user", {})

                # 사용자 정보 가져오기
                user_name = user.get("name", "N/A") if isinstance(user, dict) else "N/A"

                ver_datas.append({
                    "version_code": code,
                    "entity_name": entity,
                    "version_type": version_type,
                    "description": description,
                    "sg_status_list": sg_status_list,
                    "artist": user_name
                })

        return ver_datas

    def save_to_json(self, asset_data, version_data):
        """
        데이터를 JSON 파일로 저장하기
        """
        json_save_path = "/home/rapa/yummy/pipeline/json/open_loader_datas.json"
        
        datas = {
            "assets": asset_data,
            "versions": version_data
        }

        with open(json_save_path, "w", encoding="utf-8") as f:
            json.dump(datas, f, indent=4, ensure_ascii=False)

        print(f"{json_save_path}가 저장되었습니다.")

if __name__ == "__main__":
    loader = OpenLoaderData() 
    sg = loader.connect_sg()
    project_id = loader.read_data_from_login_json()
    asset_data = loader.get_asset_datas(project_id)
    version_data = loader.get_versions_data(project_id)
    loader.save_to_json(asset_data, version_data)
    
    