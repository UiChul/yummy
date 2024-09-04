import json
from shotgun_api3 import shotgun
from datetime import datetime

URL = "https://4thacademy.shotgrid.autodesk.com"
SCRIPT_NAME = "test_hyo"
API_KEY = "ljbgffxqg@cejveci5dQebhdx"

"""
로그인 할 때 생성된 json 파일로부터 데이터를 가져와
loader를 실행할 때 활용되는 스크립트이며
로그인 단계에서 선택된 프로젝트의 
asset과 version 데이터가 저장되어 있습니다.
"""

class OpenLoaderData():
    def __init__(self):
        print ("It operates and gets selected project datas for Loader")
        
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
        selected_project = input("프로젝트 이름: ") #loader 로그인 단계에서 설정
        json_load_path = "/home/rapa/sub_server/pipeline/json/login_user_data.json"

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
            fields = ["code", "sg_asset_type", "sg_asset_path", "tasks", "description"]
            assets = self.sg.find("Asset", filters=filters, fields=fields)

            
        for asset in assets:
            asset_name = asset.get("code", "N/A")
            asset_type = asset.get("sg_asset_type", "N/A")
            asset_path = asset.get("sg_asset_path", "N/A")
            asset_tasks = asset.get("tasks", [])

            task_details = []

            for task in asset_tasks:
                task_id = task.get("id")

                # 태스크 데이터 가져오기
                task_data = self.sg.find_one("Task", [["id", "is", task_id]], ["content", "task_assignees", "step"])

                if not task_data:
                    return
                    # 태스크 디테일
                task_content = task_data.get("content", "N/A")
                task_assignees_data = task_data.get("task_assignees", [])
                task_step = task_data.get("step", {})

                # assignee 이름
                assignee_names = [assignee.get("name", "Unknown") for assignee in task_assignees_data]

                # assigee 마다 태스크 디테일
                for assignee_name in assignee_names:
                    task_details.append({
                        "assignee_name": assignee_name,
                        "task_content": task_content,
                        "task_step": task_step.get("name", "N/A")
                        })

            asset_datas.append({
                "asset_name": asset_name,
                "asset_type": asset_type,
                "asset_path": asset_path,
                "task_details": task_details
                })

        return asset_datas

    def get_asset_versions_data(self, project_id, asset_names):
        """
        특정 어셋 이름에 맞는 버전 데이터 가져오기
        """
        asset_ver_datas = []

        if project_id and asset_names:
            # 특정 어셋들에 맞는 버전만 필터링
            filters = [
                    ["project", "is", {"type": "Project", "id": project_id}],
                    ["entity.Asset.code", "in", asset_names]  # 어셋 이름에 맞는 버전 필터링
                    ]
            fields = ["code", "sg_status_list", "user", "description", "updated_at", "entity"]
            versions = self.sg.find("Version", filters=filters, fields=fields)
          
            for version in versions:
                code = version.get("code", "N/A")
                sg_status_list = version.get("sg_status_list", "N/A")
                description = version.get("description", "N/A")
                updated_at = version.get("updated_at", "N/A")
                user = version.get("user", {})
                linked_asset = version.get("entity", {})

                user_name = user.get("name", "N/A") if isinstance(user, dict) else "N/A"

                linked_asset_name = linked_asset.get("name", "N/A") if isinstance(linked_asset, dict) else "N/A"

                # updated_at이 존재하고 datetime 객체라면 문자열로 변환
                if isinstance(updated_at, datetime):
                    updated_at = updated_at.strftime("%Y-%m-%d %H:%M")

                asset_ver_datas.append({
                    "version_code": code,
                    "sg_status_list": sg_status_list,
                    "description": description,
                    "updated_at": updated_at,
                    "artist": user_name,
                    "linked_asset": linked_asset_name
                    })
        
        return asset_ver_datas


##############################################################################
########################## Version from here #################################
##############################################################################

    def get_project_versions_data(self, project_id):
        """
        프로젝트의 versions 데이터 가져오기
        """
        project_ver_datas = []

        if not project_id:
            return
        filters = [["project", "is", {"type": "Project", "id": project_id}]]
        fields = ["code", "id", "sg_version_type", "description", "sg_status_list", "user", "updated_at"]
        versions = self.sg.find("Version", filters=filters, fields=fields)

        for version in versions:
            code = version.get("code", "N/A")
            version_id = version.get("id", "N/A")
            version_type = version.get("sg_version_type", "N/A")
            description = version.get("description", "N/A")
            sg_status_list = version.get("sg_status_list", "N/A")
            user = version.get("user", {})
            updated_at = version.get("updated_at", None)

            user_name = user.get("name", "N/A") if isinstance(user, dict) else "N/A"

            # updated_at이 존재하고 datetime 객체라면 문자열로 변환
            if isinstance(updated_at, datetime):
                updated_at = updated_at.strftime("%Y-%m-%d %H:%M")

            project_ver_datas.append({
                "version_code": code,
                "version_id": version_id,
                "version_type": version_type,
                "description": description,
                "sg_status_list": sg_status_list,
                "artist": user_name,
                "updated_at": updated_at
            })

        return project_ver_datas

    def save_to_json(self, asset_data, asset_ver_data, project_version_data):
        """
        데이터를 json 파일로 저장하기
        """
        json_save_path = "/home/rapa/sub_server/pipeline/json/open_loader_datas.json"
        
        # 어셋별 버전 데이터를 그룹화하여 저장
        assets_with_versions = []
        
        for asset in asset_data:
            asset_name = asset["asset_name"]
            
            # 해당 어셋에 맞는 버전 필터링
            linked_versions = []

            for version in asset_ver_data:
                # linked_asset의 타입을 확인하고, 이름을 비교
                linked_asset = version.get("linked_asset", {})
                
                # linked_asset이 딕셔너리인지 문자열인지 확인
                if isinstance(linked_asset, dict):
                    linked_asset_name = linked_asset.get("name", "")
                elif isinstance(linked_asset, str):
                    # 만약 linked_asset이 문자열이라면, 단순히 문자열을 사용
                    linked_asset_name = linked_asset
                else:
                    # linked_asset이 예상하지 못한 타입일 경우 처리
                    linked_asset_name = ""

                if linked_asset_name == asset_name:
                    # updated_at이 존재하고 datetime 객체라면 문자열로 변환
                    if "updated_at" in version and isinstance(version["updated_at"], datetime):
                        version["updated_at"] = version["updated_at"].isoformat()
                    
                    linked_versions.append(version)
            
            # asset_info 딕셔너리 안에 linked_versions를 포함시킴
            asset_info = {
                "asset_name": asset["asset_name"],
                "asset_type": asset["asset_type"],
                "asset_path": asset["asset_path"],
                "task_details": asset["task_details"],
                "linked_versions": linked_versions  # linked_versions를 asset_info 안에 포함
                }
            
            assets_with_versions.append({
                "asset_info": asset_info
                })

        # 전체 데이터 구조
        datas = {
            "assets_with_versions": assets_with_versions,
            "project_versions": project_version_data
            }

        # json 저장
        with open(json_save_path, "w", encoding="utf-8") as f:
            json.dump(datas, f, indent=4, ensure_ascii=False)

        print(f"{json_save_path}가 저장되었습니다.")

if __name__ == "__main__":
    loader = OpenLoaderData() 
    sg = loader.connect_sg()
    project_id = loader.read_data_from_login_json()
    asset_data = loader.get_asset_datas(project_id)
    asset_names = []
    for asset in asset_data:
        asset_names.append(asset["asset_name"])
    asset_ver_data = loader.get_asset_versions_data(project_id, asset_names)
    project_ver_data = loader.get_project_versions_data(project_id)
    loader.save_to_json(asset_data, asset_ver_data, project_ver_data)
    
    