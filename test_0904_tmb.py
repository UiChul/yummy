import os
import sys

sys.path.append("/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages")
from shotgun_api3 import shotgun

link = "https://4thacademy.shotgrid.autodesk.com/"
script_name = "test_park"
script_key = "snljjtxjfyfdxQfpnh7lgyf!f"

def connect_sg():
# 샷그리드 연결
    sg = shotgun.Shotgun(link, script_name, script_key) #Shotgun 다시 불러와야?
    return sg


def sg_upload_data_ver(): 
    description = input ("description? : ")
    shot = "PKG_030"
    code = shot + "_mm_v007"
    file_type = ".mov"
    file_path = '/Users/lucia/Desktop/sub_server/project/YUMMIE/seq/PKG/PKG_030/mm/dev/mov/PKG_030_mm_v001.mov'
    version_nk = "15v2"
    colorspace = "sRGB"
    user_name = "UICHUL SHIN"

    ver_data = {
        "project" : {"type": "Project", "id" : 222},
        "code" : code,
        # "image" : , =preview ; 썸네일, mov 올라갈 수 있도록
        "sg_status_list" : "wip",           #pub, sc
        "user": {"type" : "HumanUser", "name" : user_name, "id" : 93},
        "description" : description,
        "sg_extension" : file_type,         #exr, mov, nk
        "sg_path" : file_path,
        "sg_nk_version" : version_nk,
        "sg_colorspace_1" : colorspace
    }
    # sg.upload('Version', entity_id = "")
    # mov_file = '/Users/lucia/Desktop/4Codes/1Project/test_v001.mov'
    # sg.upload('Version', entity_id = "Content", path = mov_file, field_name = "sg_ddd", display_name = None)
    # print(ver_data)
    return ver_data


def sg_create_ver(ver_data):
    # ver_data = sg_upload_data_ver()
    new_version = sg.create('Version', ver_data)
    new_version_id = new_version['id']
    print ("version 생성이 완료되었습니다.")
    return new_version_id

def sg_tmb_upload(tmb_id):
    path = "/Users/lucia/Downloads/IMG_9196.JPG"
    field_name = "image"
    sg.upload("Version", tmb_id, path, field_name = field_name)
    print("thumbnail도 잘 올라갔습니다.")


sg = connect_sg()
ver_data = sg_upload_data_ver()
tmb_id = sg_create_ver(ver_data)
sg_tmb_upload(tmb_id)