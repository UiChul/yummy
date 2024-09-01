import os
import sys
import json
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages")
from shotgun_api3 import shotgun


link = "https://4thacademy.shotgrid.autodesk.com/"
script_name = "test_park"
script_key = "snljjtxjfyfdxQfpnh7lgyf!f"
#로그인 한 사람 기준으로 올라감

class Set():
    def __init__(self):
        self.json_file_path = '/Users/lucia/Downloads/login_user_data-2.json'
        self.key = 'project'
        self.json_data = self._read_paths_from_json()

    def _read_paths_from_json(self):
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def data_needed(self, data_json): 
        self.user_id = data_json['user_id']
        self.user_name = data_json['user_name']
        # self.project_value = data_json[self.key]
        for self.project_value in data_json['projects']:
            self.project_id = self.project_value['id']
            self.project_name = self.project_value['name']
            self.project_res_width = self.project_value['resolution_width']
            self.project_res_height = self.project_value['resolution_height']
            #어떻게 원하는 프로젝트 이름만 뽑아내지? 현재는 모든 프로젝트를 한번씩 읽어옴
            print(self.user_id, self.user_name, self.project_id, self.project_name, self.project_res_width, self.project_res_height)
            return self.user_id, self.user_name, self.project_id, self.project_res_width, self.project_res_height

    def connect_sg(self):
        # 샷그리드 연결
        sg = shotgun.Shotgun(link, script_name, script_key)
        return sg
    
    def sg_upload_data(self, project_id): 
        ver_data  =[]
        if project_id:
            filters = [["project", "is", {"type": "Project", "id": project_id}]]
            fields = ["code", "entity", "sg_version_type", "sg_status_list", "user"]
            sg.find("Version", filters=filters, fields=fields)

            #code, shot, shot_id빼서 정리
            shot = "PKG_030"
            code = shot + "_mm_v006"
            file_type = ".mov"
            file_path = '/Users/lucia/Desktop/4Codes/1Project/test_v001.mov'
            version_nk = "15v2"
            colorspace = "sRGB"

            ver_data = {
                "project" : {"type": "Project", "id" : project_id},
                "code" : code,
                # "image" : , =preview ; 썸네일, mov 올라갈 수 있도록
                "sg_status_list" : "wip",           #pub, sc
                "user": {"type" : "HumanUser", "name" : user_name, "id" : user_id},
                "description" : "testing",
                "sg_extension" : file_type,         #exr, mov, nk
                "sg_path" : file_path,
                "sg_nk_version" : version_nk,
                "sg_colorspace_1" : colorspace
            }
            # sg.upload('Version', entity_id = "")
            # mov_file = '/Users/lucia/Desktop/4Codes/1Project/test_v001.mov'
            # sg.upload('Version', entity_id = "Content", path = mov_file, field_name = "sg_ddd", display_name = None)
            print(ver_data)
            return ver_data

    def create_sg(self, sg, ver_data):
        sg.create('Version', ver_data)
        print ("version 생성이 완료되었습니다.")


if __name__ == "__main__" : 
    set = Set()
    sg = set.connect_sg()
    data_json = set._read_paths_from_json()
    set.data_needed(data_json)

    # # user_id = data_json['user_id']
    # # user_name = data_json['user_name']
    # for projects in data_json['projects']:
    #     project_id = projects['id']
    # #     project_res_width = projects['resolution_width']
    # #     project_res_height = projects['resolution_height']

    # sg_ver_data= set.sg_upload_data(project_id)
    # print(sg_ver_data)
    # set.create_sg(sg, sg_ver_data)

