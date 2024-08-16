import os, sys

sys.path.append("/home/rapa/python-api")
from shotgun_api3 import shotgun

URL = "https://4thacademy.shotgrid.autodesk.com"
SCRIPT_NAME = "test_hyo"
API_KEY = "ljbgffxqg@cejveci5dQebhdx"

# connect shotgrid
def connect_sg():

    sg = shotgun.Shotgun(URL,
                         SCRIPT_NAME,
                         API_KEY)
    return sg

def get_shot(shot_name):
    """
    샷 이름을 키워드로 
    샷정보를 가져온다
    """
    sg = connect_sg()

    filters = [["code", "is", shot_name]]
    fields = ["type", "id", "code", "sg_cut_in", "sg_cut_out"]

    datas = sg.find_one("Shot", filters=filters, fields=fields)
    if isinstance(datas, dict):
        return datas

print (get_shot(shot_name="gamja"))

def get_shots_from_sequence(sequence_name):
    """
    시퀀스 이름을 키워드로 시퀀스에 연결된 샷들을 가져온.
    """
    sg = connect_sg()

    filters = [["sg_sequence.Sequence.code", "is", sequence_name]]
    fields = ["type", "id", "code", "sg_cut_in", "sg_cut_out"]
    datas = sg.find("Shot", filters=filters, fields=fields)
    return datas

def get_userprofile(keyword, value):
    """
    이메일을 키워드로 유저정보를 불러오는 스크립트당
    keyword 는 정보를 조회할 키워드를 넣어주세여
    lastname 으로 할거면 lastname
    email로 찾아볼꺼면 email

    value는 해당하는 값을 넣어주면 된당.
    lastname 일때는 seonil을 넣어주시고
    email 일때는 이메일 주소를 넣어주시면 되겠졈?

    # ex1 user_data = get_userprofile("email", "apen1112@gmail.com")
    # ex2 user_data = get_userpfofile("lastname", "seonil")
    """
    sg = connect_sg()

    filters = [[keyword, "is", value]]
    fields = ["id", "login", "lastname", "firstname", "name"]
    datas = sg.find_one("HumanUser", filters=filters, fields=fields)

    if isinstance(datas, dict):
        return datas
print (get_userprofile(keyword="email", value="dlgyrl5759@gmail.com"))

def get_shot_data_from_sequence(sequence_name):
    """
    get_shots_from_sequence랑 사실 비슷한대 이 코드는 샷에서
    테스크 정보를 더 찾아오기 때문에 각 테스크에 어싸인된 유저이름과 아이디가 추가됨.
    근대 아직 수정중이긴함, 근대 되긴함
    """
    shots = get_shots_from_sequence(sequence_name)
    sg = connect_sg()
    for shot in shots:
        filters = [["entity", "is", {"type" : "Shot", "id" : shot["id"]}]]
        fields = ["content", "task_assignees"]
        tasks = sg.find("Task", filters=filters, fields=fields)

        if tasks:
            for task in tasks:
                print (task)
                task_name = task["content"]
                print (task_name)
                assignees = task.get("task_assignees")
                print (assignees)

    print(f"Shot ID: {shot['id']}, Code: {shot['code']}")

print(get_shot_data_from_sequence(sequence_name="talking potato"))


#sg.find_one(entity_type, filters, fields=None, order=None, filter_operator="all", retired_only=False)