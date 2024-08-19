import os, sys
sys.path.append("/home/rapa/python-api")
from shotgun_api3 import Shotgun

URL = "https://4thacademy.shotgrid.autodesk.com"
SCRIPT_NAME = "test_hyo"
API_KEY = "ljbgffxqg@cejveci5dQebhdx"

def connect_sg():
    sg = Shotgun(URL, SCRIPT_NAME, API_KEY)
    return sg

# def get_entity_list():
#     sg = connect_sg()
#     try:
#         # 모든 엔티티의 스키마를 조회
#         entities = sg.schema_read()
        
#         # 엔티티 이름 출력
#         for entity_name in entities.keys():
#             print(f"Entity: {entity_name}")
    
#     except Exception as e:
#         print(f"Error retrieving schema entities: {e}")

# # ShotGrid에서 사용 가능한 모든 엔티티 조회
# get_entity_list()

###################################################################################################################

def get_entity_fields(entity_name):
    sg = connect_sg()
    try:
        # 엔티티의 필드 스키마 조회
        fields = sg.schema_field_read(entity_name)
        
        # 필드 이름과 타입 출력
        for field_name, field_info in fields.items():
            print(f"Field Name: {field_name}, Type: {field_info['data_type']['value']}")
    
    except Exception as e:
        print(f"Error retrieving schema fields: {e}")

# 예: Shot 엔티티의 필드 확인
get_entity_fields("Task")

