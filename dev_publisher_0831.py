#dev_publisher_0830

import os
import sys
import json
import nuke
# import ffmpeg
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages")
from shotgun_api3 import shotgun


link = "https://4thacademy.shotgrid.autodesk.com/"
script_name = "test_park"
script_key = "snljjtxjfyfdxQfpnh7lgyf!f"

class Set:
    def __init__(self):
        self.json_file_path = '/Users/lucia/Downloads/login_user_data-2.json'
        self.key = 'project'
        self.json_data = self._read_paths_from_json()

    def _read_paths_from_json(self):
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data


class Data(Set): 
    def data_sg(self, project_id): 
        # 프로젝트의 versions 데이터 가져오기
        Set.connect_sg(self)
        ver_datas = []
        if project_id:
            filters = [["project", "is", {"type": "Project", "id": project_id}]]
            # filters = (["user", "is", {"type" : "HumanUser", "name" : username}])
            fields = ["code", "entity", "sg_version_type", "sg_status_list", "user"]
            versions = self.sg.find("Version", filters=filters, fields=fields)

            for version in versions:
                sgdata_version_name = version.get("code", "N/A")                            #이름
                # sgdata_sg_status = version.get("sg_status_list", "N/A")                   #status   
                #status : pub이면 손 못대게? 아닌가?
                sgdata_path = version.get("sg_path", "N/A")                                 #nuke path
                sgdata_extend = version.get("sg_version_file_type", "N/A")                  #extension
                sgdata_colorspace = version.get("sg_colorspace_1", "N/A")                   #color space
                sgdata_nk_version = version.get("sg_nk_version", "N/A")
                # codecname ; 확인
                # resolution ; project랑 확인? / 1차로 공란 확인 할 것
                # frame ; 확인

                ver_datas.append({
                    "version_name": sgdata_version_name,
                    "file_path" : sgdata_path, 
                    "extend" : sgdata_extend,
                    "colorspace" : sgdata_colorspace,
                    "nuke_version": sgdata_nk_version
                    })
        print (ver_datas)
        return ver_datas
    
    def data_nk(self):
        nk_datas = {}
        root = nuke.root()
        path = root["name"].value()                     # file path
        extend = path.split(".")[-1]                    # extendation
        colorspace = root["colorManagement"].value()    # colorspace
        nuke_version = nuke.NUKE_VERSION_STRING         # nk version
        
        nk_datas = {
            "file_path" : path,
            "extend" : extend,
            "colorspace" : colorspace,
            "nuke_version" : nuke_version
            }

        return nk_datas

    # def data_exr_mov(self, file_path):
    #     exr_datas = {}
    #     mov_datas = {}
    #     probe = ffmpeg.probe(file_path)

    #     # extract video_stream
    #     video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
    #     codec_name = video_stream['codec_name']
    #     colorspace = video_stream.get('color_space', "N/A")
    #     width = int(video_stream['width'])
    #     height = int(video_stream['height'])
    #     # a = video_stream.keys()
    #     # print(a)

    #     resolution = f"{width}x{height}"

    #     if file_path.split(".")[-1] == "mov":
    #         frame = int(video_stream['nb_frames'])

    #         mov_datas = {
    #         "file_path": file_path,
    #         "codec_name": codec_name,
    #         "colorspace": colorspace,
    #         "resolution": resolution,
    #         "frame": frame
    #         }

    #         return mov_datas
        
    #     elif file_path.split(".")[-1] == "exr":
    #         frame = 1
    #         exr_datas = {
    #         "file_path": file_path,
    #         "codec_name": codec_name,
    #         "colorspace": colorspace,
    #         "resolution": resolution,
    #         "frame": frame
    #         }
    #         return exr_datas
        

class Validate():
    def val_nk(self, ver, nk): 
        for k in nk.keys() : 
            if ver.get(k) == nk.get(k): 
                pass
                # return True
            else : 
                print(k, "is non valid, check again the values")
                return False

    def val_exr(self, exr):
        for k in exr.keys():
            if exr.get(k):
                pass
            else : 
                print ("value ", k, " in exr is now empty, check again.")
                return False

    def val_mov(self, mov):
        for k in mov.keys():
            if mov.get(k):
                pass
            else : 
                print ("value ", k, " in mov is now empty, check again.")
                return False
# nk exr mov all right -> Pub 
# one wrong -> print wrong

class Act(): 
    def ask(self, bool):
        bool = input("change or force?")    # Qmessage ; 수정할래 force 할래? 
        return bool 
        # if 수정 : change == 1
        #     return True                   #프로그램 창 닫히도록
        # else :    force == 0              #force
        #     return False                  #Pub으로 뜁니다

class Pub(): 
    def server_upload(self):
        pass
        """
        버전 업
        폴더 이동
        """

    def make_data_upload(self, path):
        
        #썸네일도 업로드 가능하게
        pass

    def sg_version_upload(self, sg, data): 
        upload = sg.create('Version', data)
        if not upload == 1 :
            print("version 업로드 되었습니다.")

    def sg_publish_upload(self): 
        upload = sg.create('Publish', data)
        if not upload == 1 :
            print("publish 업로드 되었습니다.")
    
if __name__ == "__main__" : 
    setting = Set()
    sg = setting.connect_sg()
    # shotgrid_data = shotgrid.get_versions_data(222)
    # shotgrid.save_to_json(shotgrid_data)

    data = Data()
    # 222 : project 불러오기 연결      
    dict_ver = data.data_sg(222)
    dict_nk = data.data_nk(222)
    dict_exr = data.data_exr(222)
    dict_mov = data.data_mov(222)
    # exr, mov 파일 따로 나올 수 있도록

    val = Validate()
    val_nk = val.val_nk(dict_ver, dict_nk)
    val_exr = val.val_exr(dict_exr)
    val_mov = val.val_mov(dict_mov)

    pub = Pub()
    if val_nk & val_exr & val_mov :                     #모두 True 일 때 
        server_upload = pub.server_upload
        ver_upload = pub.sg_version_upload
        if button_pub == 1:                             #pub버튼이 눌렸을 때
            pub_upload = pub.sg_publish_upload

    else :                                              #False가 하나라도 뜨면
        act = Act()
        ask = act.ask
        if ask == 0:                                    #Pub으로 뜁니다. 
            if 처음 button_ver == 1 :                    #처음에 version을 눌렀을 경우
                server_upload = pub.server_upload       #서버랑 버전 업데이트
                ver_upload = pub.sg_version_upload
                tmb_upload = pub.sg_thumbnail_upload
            elif 처음 button_pub == 1:                   #처음에 pub버튼으로 시작했을 경우
                server_upload = pub.server_upload       #서버, 버전, 퍼블리시 업데이트
                ver_upload = pub.sg_version_upload
                pub_upload = pub.sg_publish_upload
                tmb_upload = pub.sg_thumbnail_upload




#issue :
# login json에서 project_id, username ; 두번 필터링 하기
# 가져온 status ; fin ; 더이상 수정 못하게?

# exr, mov 데이터 파일 쪼갤 수 있는지? (쪼개도 되는지?) ; 일단 진행
# resolution ; 1차 : 공란 확인      2차 : project setting과 맞는지 확인하기

# ver / pub 버튼 눌린 것 중첩되는 실행함수 정리하기 (nested function, closure)

