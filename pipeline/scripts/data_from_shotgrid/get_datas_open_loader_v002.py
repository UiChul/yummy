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
        json_load_path = "/home/rapa/YUMMY/pipeline/json/login_user_data.json"

        with open(json_load_path, "r", encoding="utf-8") as f:
            user_data = json.load(f)

        for project in user_data.get("projects", []):
            project_name = project.get("name")
            project_id = project.get("id")

            if project_name == selected_project:
                    return project_id

        return None

    def get_tem_asset_path(self, project_id):
        """
        project_id로 어셋 템플릿 패스 가져오기
        """
        asset_datas = []

        if project_id:
            filters = [["project", "is", {"type": "Project", "id": project_id}]]
            fields = ["code", "sg_asset_path"]
            assets = self.sg.find("Asset", filters=filters, fields=fields)

            asset_datas = []

            for asset in assets:
                asset_name = asset.get("code")
                asset_path = asset.get("sg_asset_path")
                if asset_name and asset_path:
                    asset_datas.append(("asset_name:", asset_name, "asset_path:", asset_path))

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
        json_save_path = "/home/rapa/YUMMY/pipeline/json/open_loader_datas.json"
        
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
    asset_data = loader.get_tem_asset_path(project_id)
    version_data = loader.get_versions_data(project_id)
    loader.save_to_json(asset_data, version_data)
    
    