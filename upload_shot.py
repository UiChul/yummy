#upload shot


import os
import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages")
from shotgun_api3 import shotgun


link = "https://4thacademy.shotgrid.autodesk.com/"
script_name = "test_park"
script_key = "snljjtxjfyfdxQfpnh7lgyf!f"

def connect_sg():
    """
    샷그리드 연결
    """
    sg = shotgun.Shotgun(link, script_name, script_key)
    return sg

def make_data():
    #있는 seq_num에서 알아서 하나 더 추가하는 것은 디벨롭 할 것
    data = {
        "project" : {"type" : "Project", "id" : 222},
        "sg_sequence" : {"type" : "Sequence", "id" : 263},
        "code" : "TEST"
    }
    print(data)
    return data

def create_sg(sg, data):
    created = sg.create('Shot', data)
    # entity_id = created['id']
    # w_fields = sg.find_one("Sequence", [["id", "is", entity_id]])


    print ("shot 생성이 완료되었습니다.")
    # return w_fields


if __name__ == "__main__" : 
    sg = connect_sg()
    made_data = {}
    made_data = make_data()
    create_sg(sg, made_data)