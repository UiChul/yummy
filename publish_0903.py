# MODI
### render/publish setting in nuke
### complete ALL process (open nuke > use ui > shotgrid upload/publish)



try:
    from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem
    from PySide6.QtWidgets import QListWidgetItem, QListWidget, QVBoxLayout
    from PySide6.QtWidgets import QFileDialog, QMessageBox, QPushButton
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, QSize
    from PySide6.QtGui import  Qt, QPixmap, QIcon

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem
    from PySide2.QtWidgets import QListWidgetItem, QListWidget, QVBoxLayout
    from PySide2.QtWidgets import QFileDialog, QMessageBox
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, QSize
    from PySide2.QtGui import  Qt, QPixmap, QIcon

import os
import sys
import re
import nuke
import json
import ffmpeg
import shutil

os.system("ffmpeg")
# sys.path.append("/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages")
from shotgun_api3 import shotgun

link = "https://4thacademy.shotgrid.autodesk.com/"
script_name = "test_park"
script_key = "snljjtxjfyfdxQfpnh7lgyf!f"

# def connect_sg():
# # 샷그리드 연결
#     sg = shotgun(link, script_name, script_key) #Shotgun 다시 불러와야?
#     return sg

class PathFinder():
    """
    Read Json File and find matching material (key:project_name)
    and then find Local path
    """

    def __init__(self):
        self.json_file_path = '/home/rapa/YUMMY/pipeline/json/project_data.json'
        # self.json_file_path = json_file_path
        self.key = 'project'
        self.json_data = self._read_paths_from_json()

    # def connect_sg(self):
    # # 샷그리드 연결
    #     self.sg = shotgun(link, script_name, script_key) #Shotgun 다시 불러와야?
    #     return self.sg

    def _read_paths_from_json(self):
        """Read Json file and data return"""
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    
    def append_project_to_path(self, start_path):
        """Find data that matches key(project_name) in Json data"""
        project_value = self.json_data[self.key]
        start_path = start_path.rstrip(os.sep)
        new_path = f"{start_path}/{project_value}/"
        return new_path
    
    def data_needed(self):
        data_json = self._read_paths_from_json() 
        self.project_name= data_json[self.key]
        self.project_id = data_json['project_id']
        self.user_name = data_json['name']
        self.project_res_width = data_json['resolution_width']
        self.project_res_height = data_json['resolution_height']
        # print(self.user_id, self.ㅋ, project_id, project_name, project_res_width, project_res_height)

class MainPublish(QWidget):
    def __init__(self):
        super().__init__()         
        loader = QUiLoader()
        # ui_file_path = "/Users/lucia/Downloads/publish7.ui"
        ui_file_path = "/home/rapa/yummy/pipeline/scripts/publish/publish_ver6.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint) # UI 최상단 고정
        ui_file.close()
        self.connect_sg()
        self.setup_file_in_groubBox_from_Local()
        self.setup_top_bar()
        self.setup_tablewidget_basket()
        self.set_delete_icon()
        self._collect_path()
        print("HeLLOOOOOO")

        # Signal
        self.ui.pushButton_add_to_basket.clicked.connect(self.on_add_button_clicked)
        self.ui.pushButton_version.clicked.connect(self.val_all_together_ver)            #validate 실행 되게
        # self.ui.pushButton_version.clicked.connect(self.make_message_for_upload)            #validate 실행 되게
        # self.ui.pushButton_version.clicked.connect(self.copy_to_Server_from_Local)
        self.ui.pushButton_publish.clicked.connect(self.val_all_together_pub)
        # self.ui.pushButton_publish.clicked.connect(self.make_message_for_upload)
        # self.ui.pushButton_publish.clicked.connect(self.copy_to_pub_from_dev_in_Server)
        # self.ui.pushButton_delete.clicked.connect(self.delete_tablewidget_item)
        # self.ui.pushButton_publish.clicked.connect(self.make_message_for_upload_success)
    
    def connect_sg(self):
        # 샷그리드 연결
        self.sg = shotgun.Shotgun(link, script_name, script_key) #Shotgun 다시 불러와야?
        return self.sg
    
    def on_add_button_clicked(self):
        self.add_nk_item_tablewidget_basket()
        self.add_exr_item_tablewidget_basket()
        self.add_mov_item_tablewidget_basket()
        self.count_tablewidget_item()
        self.get_description_text()

    def setup_file_in_groubBox_from_Local(self):

        # nk_page
        nk_page = QWidget()
        layout1 = QVBoxLayout(nk_page)
        self.nk_file_path = os.path.dirname(nuke.scriptName())
        self.nk_file_listwidget = QListWidget()
        self.nk_file_listwidget.setObjectName("nk_file_listwidget")
        layout1.addWidget(self.nk_file_listwidget)
        self.nk_file_listwidget.addItem("Double-click here to add file")
        self.ui.groupBox_nk.setLayout(layout1)
        self.nk_file_listwidget.itemDoubleClicked.connect(self.open_nk_file_dialog)
        self.nk_file_listwidget.itemDoubleClicked.connect(self.generate_nk_thumbnail_from_file)

        # exr_page
        exr_page = QWidget()
        layout2 = QVBoxLayout(exr_page)
        self.exr_folder_path = self.nk_file_path.split("work")[0]+"exr/"
        self.exr_folder_listwidget = QListWidget()
        self.exr_folder_listwidget.addItem("Double-click here to add folder")
        self.exr_folder_listwidget.setObjectName("exr_file_listwidget")
        layout2.addWidget(self.exr_folder_listwidget)
        self.ui.groupBox_exr.setLayout(layout2)
        self.exr_folder_listwidget.itemDoubleClicked.connect(self.open_exr_folder_dialog)
        self.exr_folder_listwidget.itemDoubleClicked.connect(self.generate_exr_thumbnail_from_file)

        # mov_page
        mov_page = QWidget()
        layout3 = QVBoxLayout(mov_page)
        self.mov_file_path = self.nk_file_path.split("work")[0]+"mov/"
        self.mov_file_listwidget = QListWidget()
        self.mov_file_listwidget.setObjectName("mov_file_listwidget")
        layout3.addWidget(self.mov_file_listwidget)
        self.mov_file_listwidget.addItem("Double-click here to add file")
        self.ui.groupBox_mov.setLayout(layout3)
        self.mov_file_listwidget.itemDoubleClicked.connect(self.open_mov_file_dialog)
        self.mov_file_listwidget.itemDoubleClicked.connect(self.generate_mov_thumbnail_from_file)

    def open_nk_file_dialog(self):
        file_dialog = QFileDialog.getOpenFileNames(self, "Select Files from Local", self.nk_file_path, "All Files (*)")
        selected_files = file_dialog[0]
        if selected_files:
            self.nk_file_names = [os.path.basename(path) for path in selected_files]
            self.nk_file_listwidget.clear()

            items = []
            for file_name in self.nk_file_names:
                item = QListWidgetItem(file_name)
                self.nk_file_listwidget.addItem(item)
                items.append(item)

            if items:
                self.nk_file_listwidget.setCurrentItem(items[0])

    def open_mov_file_dialog(self):
        file_dialog = QFileDialog.getOpenFileNames(self, "Select Files from Local", self.mov_file_path, "All Files (*)")
        selected_files = file_dialog[0]
        if selected_files:
            self.mov_file_names = [os.path.basename(path) for path in selected_files]
            self.mov_file_listwidget.clear()

            items = []
            for file_name in self.mov_file_names:
                item = QListWidgetItem(file_name)
                self.mov_file_listwidget.addItem(item)
                items.append(item)
            
            if items:
                self.mov_file_listwidget.setCurrentItem(items[0])

    def open_exr_folder_dialog(self):
        QMessageBox.information(self, "Folder Selected", "Please select 'Folder' for exr")

        folder = QFileDialog.getExistingDirectory(self, "Select Folder from Local", self.exr_folder_path)
        if folder:
            self.folder_name = os.path.basename(folder)
            self.exr_folder_listwidget.clear()

            item = QListWidgetItem(self.folder_name)
            self.exr_folder_listwidget.addItem(item)
            self.exr_folder_listwidget.setCurrentItem(item)
        
    def setup_top_bar(self):

        # self.nk_file_path = nuke.scriptName()
        split = self.nk_file_path.split("/")
        # print(split)
        project_name = split[-7]
        shot_code = split[-4]
        team_name = split[-3]
        self.ui.label_project_name.setText(project_name)
        self.ui.label_shot_code.setText(shot_code)
        self.ui.label_team_name.setText(team_name)

    def _collect_path(self):
        
        self.current_nk_file_path = nuke.scriptName()
        self.work_path = f"{os.path.dirname(self.current_nk_file_path)}/"
        self.dev_path = self.work_path.split("work")[0]
        self.exr_folder_path = f"{self.dev_path}exr/"
        self.mov_file_path = f"{self.dev_path}mov/"

    #===================================================================

    def setup_tablewidget_basket(self):

        self.ui.tableWidget_basket.setHorizontalHeaderLabels(["Publish File", "File Info"])
        self.ui.tableWidget_basket.setVerticalHeaderLabels(["nk", "exr", "mov"])

        row_count = self.ui.tableWidget_basket.rowCount()
        height = 80
        for row in range(row_count):
            self.ui.tableWidget_basket.setRowHeight(row, height)

        self.add_nk_item_tablewidget_basket()
        self.add_exr_item_tablewidget_basket()
        self.add_mov_item_tablewidget_basket()

    def add_nk_item_tablewidget_basket(self):
        
        ### nk item ###
        nk_selected_files = self.nk_file_listwidget.selectedItems()
        for file in nk_selected_files:
            nk_item = QTableWidgetItem()
            nk_selected_file = file.text()
            nk_item.setText(nk_selected_file)
            self.ui.tableWidget_basket.setItem(0, 0, nk_item)

            nk_info_dict = self._get_nk_validation_info()
            nk_info_text = "\n".join(f"{key} : {value}" for key, value in nk_info_dict.items())
            nk_validation_info = QTableWidgetItem(nk_info_text)
            nk_validation_info.setTextAlignment(Qt.AlignLeft | Qt.AlignTop) # 왼쪽 정렬, 위쪽 정렬
            self.ui.tableWidget_basket.setItem(0, 1, nk_validation_info)

    def add_exr_item_tablewidget_basket(self):

        ### exr item ###
        exr_selected_folders = self.exr_folder_listwidget.selectedItems()
        for folder in exr_selected_folders:
            exr_item = QTableWidgetItem()
            exr_selected_folder = folder.text()
            exr_item.setText(exr_selected_folder)
            self.ui.tableWidget_basket.setItem(1, 0, exr_item)

            exr_file_path = f"{self.exr_folder_path}{exr_selected_folder}"
            exr_files = os.listdir(exr_file_path)
            for file in exr_files:
                self.exr_full_path = f"{exr_file_path}/{file}"

                exr_validation_info_dict = self._get_exr_validation_info(self.exr_full_path)
                exr_info_text = "\n".join(f"{key} : {value}" for key, value in exr_validation_info_dict.items())
                exr_validation_info = QTableWidgetItem(exr_info_text)
                exr_validation_info.setTextAlignment(Qt.AlignLeft | Qt.AlignTop) # 왼쪽 정렬, 위쪽 정렬
                self.ui.tableWidget_basket.setItem(1, 1, exr_validation_info)

    def add_mov_item_tablewidget_basket(self):

        ### mov item ###
        mov_selected_files = self.mov_file_listwidget.selectedItems()
        for file in mov_selected_files:
            mov_item = QTableWidgetItem()
            mov_selected_file = file.text()
            mov_item.setText(mov_selected_file)
            self.ui.tableWidget_basket.setItem(2, 0, mov_item)

            self.mov_new_path = f"{self.mov_file_path}{mov_selected_file}"
        
            mov_validation_info_dict = self._get_mov_validation_info(self.mov_new_path)
            mov_info_item = "\n".join(f"{key} : {value}" for key, value in mov_validation_info_dict.items())
            mov_validation_info = QTableWidgetItem(mov_info_item)
            mov_validation_info.setTextAlignment(Qt.AlignLeft | Qt.AlignTop) # 왼쪽 정렬, 위쪽 정렬
            self.ui.tableWidget_basket.setItem(2, 1, mov_validation_info)

    #===================================================================

    def _get_versions_data(self):
        """
        프로젝트의 versions 데이터 가져오기
        """
        # json_file_path = '/home/rapa/YUMMY/pipeline/json/project_data.json'
        PF = PathFinder()
        sg_ver_data = PF._read_paths_from_json()
        # sg = self.connect_sg()

        # project_name = sg_ver_data.get('project', 'N/A')
        project_id = sg_ver_data.get('project_id', 'N/A')

        # data_making = PF.data_needed()
        # project_id = PF.data_needed[1]
        # print(project_id)
        ver_datas = {}

        if project_id:
            filters = [["project", "is", {"type": "Project", "id": project_id}]]
            fields = ["code", "entity", "sg_version_type", "description", "sg_status_list", "user"]
            versions = self.sg.find("Version", filters=filters, fields=fields)

            for version in versions:
                code = version.get("code", "N/A")                           #이름
                # sg_status_list = version.get("sg_status_list", "N/A")       #status   
                extension = version.get("sg_version_type", "N/A")        #type
                color = version.get("sg_colorspace", "N/A")                 #color space
                nuke_ver = version.get("sg_nk_version", "N/A")


                ver_datas["version_name"] = code, 
                ver_datas["extension"] = extension,
                ver_datas["colorspace"] =  color,
                ver_datas["nuke_ver"] = nuke_ver

        return ver_datas

    def _get_nk_validation_info(self):

        ######### 사실 마지막 아이템을 publish하지 중간껄 publish할 일이 있을까??
        ######### 중간꺼 한다치면 thumbnail은 어카지 ....
        nk_file_validation_dict = {}
        root = nuke.root()
        path = root["name"].value()                     # file path
        extension = path.split(".")[-1]                    # extension
        colorspace = root["colorManagement"].value()    # colorspace
        nuke_version = nuke.NUKE_VERSION_STRING         # nk version
        
        nk_file_validation_dict = {
        "file_path" : path,
        "extend" : extension,
        "colorspace" : colorspace,
        "nuke_version" : nuke_version
        }

        return nk_file_validation_dict

    def _get_exr_validation_info(self, file_path):
            exr_file_validation_dict = {}
            probe = ffmpeg.probe(file_path)

            # extract video_stream
            video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
            codec_name = video_stream['codec_name']
            colorspace = video_stream.get('color_space', "N/A")
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            frame = 1
            # a = video_stream.keys()
            # print(a)

            resolution = f"{width}x{height}"

            # file_validation dictionary
            exr_file_validation_dict = {
                "file_path": file_path,
                "codec_name": codec_name,
                "colorspace": colorspace,
                "resolution": resolution,
                "frame": frame
            }
            # print(file_validation_info_dict)
            return exr_file_validation_dict
    
    def _get_mov_validation_info(self, file_path):

            mov_file_validation_dict = {}
            probe = ffmpeg.probe(file_path)

            # extract video_stream
            video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
            codec_name = video_stream['codec_name']
            colorspace = video_stream.get('color_space', "N/A")
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            frame = int(video_stream['nb_frames'])
            # a = video_stream.keys()
            # print(a)

            resolution = f"{width}x{height}"

            # file_validation dictionary
            mov_file_validation_dict = {
                "file_path": file_path,
                "codec_name": codec_name,
                "colorspace": colorspace,
                "resolution": resolution,
                "frame": frame
            }
            # print(file_validation_info_dict)
            return mov_file_validation_dict

    def val_nk(self): 
        ver = self._get_versions_data()                  #dict
        nk = self._get_nk_validation_info()              #dict
        for k in nk.keys() : 
            if ver.get(k) == nk.get(k):                #file path도 같을 수 있나?
                return True
            else : 
                return (k, "is non valid, check again the values")

    def val_exr(self):
        exr = self._get_exr_validation_info(self.exr_full_path)
        for k in exr.keys():
            if exr.get(k):
                return True
            else : 
                return("value ", k, " in exr is now empty, check again.")

    def val_mov(self):
        mov = self._get_mov_validation_info(self.mov_new_path)
        for k in mov.keys():
            if mov.get(k):
                return True
            else : 
                return("value ", k, " in mov is now empty, check again.")

    def val_all_together_ver(self) : 
        TF_nk = self.val_nk()
        TF_exr = self.val_exr()
        TF_mov = self.val_mov()
        print(type(TF_nk))
        if TF_nk and TF_exr and TF_mov == True :              #validate 통과
            self.copy_to_Server_from_Local() 
            self.sg_upload_data_ver()
            self.sg_create_ver()
            # self.sg_thumbnail_upload()
            self.make_message_for_upload_success()
        else :                                            #validate 실패
            self.make_message_for_upload_ver()

    def val_all_together_pub(self) : 
        TF_nk = self.val_nk()
        TF_exr = self.val_exr()
        TF_mov = self.val_mov()
        if TF_nk & TF_exr & TF_mov == True :              #validate 통과
            self.copy_to_Server_from_Local 
            self.sg_upload_data_pub
            self.sg_create_ver
            self.sg_create_pub
            self.sg_thumbnail_upload
        else :                                            #validate 실패
            self.make_message_for_upload_pub

    #==================================================================

    def count_tablewidget_item(self):

        row_count = self.ui.tableWidget_basket.rowCount()

        item_count = 0

        for row in range(row_count):
            item = self.ui.tableWidget_basket.item(row, 0)
            if item:
                item_count += 1
        self.ui.label_item_count.setText(str(item_count))

    def delete_tablewidget_item(self):
        self.ui.tableWidget_basket.clear()
        selected_items = self.ui.tableWidget_basket.selectedItems()

        rows_to_clear = set()
        for item in selected_items:
            row = item.row()
            rows_to_clear.add(row)

        for row in rows_to_clear:
            self.ui.tableWidget_basket.setItem(row, 0, None)
            self.ui.tableWidget_basket.setItem(row, 1, None)

    #==================================================================

    def _find_Local_path(self):

        table_items = self.ui.tableWidget_basket.selectedItems()

        origin_local_path = []
        for item in table_items:
            if item:
                nk_item_text = self.ui.tableWidget_basket.item(0, 0).text()
                nk_local_path = f"{self.work_path}{nk_item_text}"
                
                exr_item_text = self.ui.tableWidget_basket.item(1, 0).text()
                exr_local_path = f"{self.exr_folder_path}{exr_item_text}"
                
                mov_item_text = self.ui.tableWidget_basket.item(2, 0).text()
                mov_local_path = f"{self.mov_file_path}{mov_item_text}"
                
            else:
                print("아이템이 없습니다.")
            
        origin_local_path.extend([nk_local_path, exr_local_path, mov_local_path])

        return origin_local_path

    def _get_highest_version_number(self, path, version_pattern):
        
        highest_version = 0
        for filename in os.listdir(path):
            match = version_pattern.search(filename)
            if match:
                version_number = int(match.group(0)[1:])
                if version_number > highest_version:
                    highest_version = version_number
     
        return highest_version

    def version_up_in_Local(self):
        """Take the file_path, version it up and Save it"""

        local_paths = self._find_Local_path() # nk, mov는 파일까지 포함된 풀패스, exr은 버전폴더까지만

        version_pattern = re.compile("v\d{3}")
        
        new_local_paths = []
        for local_path in local_paths:
            base, ext = os.path.splitext(local_path)
            base_dir = os.path.dirname(local_path)
            # nk : dev/work/opn_0010_mm_v010.nknc
            # mov : dev/mov/opn_0010_mm_v010.mov
            # exr : dev/exr/v010

            highest_version = self._get_highest_version_number(base_dir, version_pattern) # nk, mov는 아이템에서 버전패턴 검색, exr은 폴더에서 버전패턴 검색
            new_version = f"v{highest_version + 1:03}"

            new_base = base.replace(version_pattern.search(base).group(0), new_version)

            if ext == ".nknc":
                nk_version_up_path = f"{new_base}{ext}"
                new_local_paths.append(nk_version_up_path)
                # print("======nk======")
                nuke.scriptSaveAs(nk_version_up_path)
                print("nk file이 version-up 되었습니다.")

            elif ext == ".mov":
                mov_version_up_path = f"{new_base}{ext}"
                new_local_paths.append(mov_version_up_path)
                # print("======mov======")
                shutil.copy2(local_path, mov_version_up_path)
                print("mov file이 version-up 되었습니다.")

            elif os.path.isdir(local_path):      #local_path = 폴더까지 있는 오리진 폴더 경로
                new_ver_folder = new_base        #버전업된 폴더경로
                os.makedirs(new_ver_folder, exist_ok=True)

                for exr_file in os.listdir(local_path):
                    current_path = os.path.join(local_path, exr_file)
                    match = version_pattern.search(exr_file)
                    if match:
                        current_version_in_file = match.group(0)
                        print(f"{current_version_in_file}:파일 버전")
                        new_exr_file = exr_file.replace(current_version_in_file, new_version)
                        new_exr_path = os.path.join(new_ver_folder, new_exr_file)
                        
                        shutil.copy2(current_path, new_exr_path)
                        new_local_paths.append(new_exr_path)
                        print(f"exr file이 version-up 되었습니다: {new_exr_path}")

        return new_local_paths

    def _find_Server_seq_path(self):
        """Find matching folder from Json and make Server path until 'seq' """


        PF = PathFinder()
        sg_ver_data = PF._read_paths_from_json()
        # sg = self.connect_sg()

        # project_name = sg_ver_data.get('project', 'N/A')
        # project_id = sg_ver_data.get('project_id', 'N/A')

        # data_making = PF.data_needed()
        # project_id = PF.data_needed[1]
        # print(project_id)
        # ver_datas = {}



        # json_file_path = '/home/rapa/YUMMY/pipeline/json/project_data.json'
        # path_finder = PathFinder(json_file_path)

        start_path = '/home/rapa/YUMMY/project'

        # Get the new path
        server_project_path = PF.append_project_to_path(start_path)
        server_seq_path = f"{server_project_path}seq/"

        return server_seq_path

    def _find_Server_dev_path(self):
        """Get material item in tablewidget and append into seq_path""" 

        # Find server_path material based on the original version in tablewidget
        nk_file_name = self.ui.tableWidget_basket.item(0, 0).text()
        exr_v_folder_name = self.ui.tableWidget_basket.item(1, 0).text()
        mov_file_name = self.ui.tableWidget_basket.item(2, 0).text()

        # Finally can make server_path! (before version-up)
        seq_path = self._find_Server_seq_path()
        seq_name = nk_file_name.split("_")[0]
        code = nk_file_name.split("_")[1]
        shot_code = f"{seq_name}_{code}"
        team_name = nk_file_name.split("_")[2]

        nk_server_path = f"{seq_path}{seq_name}/{shot_code}/{team_name}/dev/work/{nk_file_name}"
        exr_server_path = f"{seq_path}{seq_name}/{shot_code}/{team_name}/dev/exr/{exr_v_folder_name}"
        mov_server_path = f"{seq_path}{seq_name}/{shot_code}/{team_name}/dev/mov/{mov_file_name}"

        # version pattern setting
        version_pattern = re.compile("v\d{3}")

        nk_match = version_pattern.search(nk_server_path)
        exr_match = version_pattern.search(exr_server_path)
        mov_match = version_pattern.search(mov_server_path)
        
        # server_path (after version-up)
        ver_up_server_dev_paths = []

        if nk_match:
            current_version = nk_match.group(0)
            new_number = int(current_version[1:]) + 1
            new_version = f"v{new_number:03}"
            nk_ver_up_server_path = nk_server_path.replace(current_version, new_version)

        if exr_match:
            current_version = exr_match.group(0)
            new_number = int(current_version[1:]) + 1
            new_version = f"v{new_number:03}"
            exr_ver_up_server_path = exr_server_path.replace(current_version, new_version)

        if mov_match:
            current_version = mov_match.group(0)
            new_number = int(current_version[1:]) + 1
            new_version = f"v{new_number:03}"
            mov_ver_up_server_path = mov_server_path.replace(current_version, new_version)

        ver_up_server_dev_paths.extend([nk_ver_up_server_path, exr_ver_up_server_path, mov_ver_up_server_path])

        return ver_up_server_dev_paths

    def copy_to_Server_from_Local(self):
        QMessageBox.information(self, "Folder Selected", "Please select 'Folder' for exr")

        ver_up_local_paths = self.version_up_in_Local()
        ver_up_server_dev_paths = self._find_Server_dev_path()

        for ver_up_local_path in ver_up_local_paths:
            ver_up_local_path = ver_up_local_path.strip()
            base, ext = os.path.splitext(ver_up_local_path)
            # print(ext)

            if ext == ".nknc":
                if not os.path.exists(ver_up_local_path):
                    print("source nk file does not exist")
                    continue
                dest_dir = os.path.dirname(ver_up_server_dev_paths[0])

                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                    shutil.copy2(ver_up_local_path, ver_up_server_dev_paths[0])
                    print("nk version up file이 server로 이동되었습니다.")

                # if not os.path.dirname(ver_up_server_dev_paths[0]):
                # print(f"{ver_up_local_path}:누크로컬패스")
                # print(f"{ver_up_server_dev_paths[0]}:누크서버패스")
                #     shutil.copy2(ver_up_local_path, ver_up_server_dev_paths[0])
                # print("nk version up file이 server로 이동되었습니다.")
            
            elif ext == ".exr":
                if not os.path.exists(ver_up_local_path):
                    print("source exr file does not exist")
                    continue
                dest_dir = os.path.dirname(ver_up_server_dev_paths[0])
                exr_ver_up_local_path = os.path.dirname(ver_up_local_path)
                exr_dest_dir = ver_up_server_dev_paths[1]

                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                    shutil.copy2(ver_up_local_path, ver_up_server_dev_paths[0])
                    print("exr version up file이 server로 이동되었습니다.")

                if os.path.exists(exr_ver_up_local_path):
                    shutil.copytree(exr_ver_up_local_path, exr_dest_dir, dirs_exist_ok=True)
                # exr_ver_up_local_path = os.path.dirname(ver_up_local_path)
                # print(f"{exr_ver_up_local_path}:이엑스알로컬패스")
                # print(f"{ver_up_server_dev_paths[1]}:이엑스알서버패스")
                # shutil.copytree(exr_ver_up_local_path, ver_up_server_dev_paths[1], dirs_exist_ok=True)
                    print("exr version up folder가 server로 이동되었습니다.")

            elif ext == ".mov":
                if not os.path.exists(ver_up_local_path):
                    print("source mov file does not exist")
                    continue
                dest_dir = os.path.dirname(ver_up_server_dev_paths[2])

                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                    shutil.copy2(ver_up_local_path, ver_up_server_dev_paths[2])
                    print("mov version up file이 server로 이동되었습니다.")

                # # print(f"{ver_up_local_path}:모브로컬패스")
                # # print(f"{ver_up_server_dev_paths[2]}:모브서버패스")
                # shutil.copy2(ver_up_local_path, ver_up_server_dev_paths[2])
                # print("mov version up file이 server로 이동되었습니다.")

    def _find_Server_pub_path(self):
        """Use Dev_folder_path to make Pub_folder_path"""

        ver_up_server_dev_paths = self._find_Server_dev_path()
        ver_up_server_pub_paths = []

        for path in ver_up_server_dev_paths:
            pub_path = path.replace("dev", "pub")
            ver_up_server_pub_paths.append(pub_path)

        return ver_up_server_pub_paths

    def copy_to_pub_from_dev_in_Server(self):

        ver_up_local_paths = self.version_up_in_Local()
        ver_up_server_dev_paths = self._find_Server_dev_path()
        ver_up_server_pub_paths = self._find_Server_pub_path()

        for ver_up_local_path in ver_up_local_paths:
            ver_up_local_path = ver_up_local_path.strip()
            base, ext = os.path.splitext(ver_up_local_path)
            # print(ext)

            if ext == ".nknc":
                # print(f"{ver_up_local_path}:누크로컬패스")
                # print(f"{ver_up_server_dev_paths[0]}:누크서버패스")
                shutil.copy2(ver_up_local_path, ver_up_server_dev_paths[0])
                shutil.copy2(ver_up_server_dev_paths[0], ver_up_server_pub_paths[0])
                print("nk version up file이 server로 이동되었습니다.")
            
            elif ext == ".exr":
                exr_ver_up_local_path = os.path.dirname(ver_up_local_path)
                # print(f"{exr_ver_up_local_path}:이엑스알로컬패스")
                # print(f"{ver_up_server_dev_paths[1]}:이엑스알서버패스")
                shutil.copytree(exr_ver_up_local_path, ver_up_server_dev_paths[1], dirs_exist_ok=True)
                shutil.copytree(ver_up_server_dev_paths[1], ver_up_server_pub_paths[1], dirs_exist_ok=True)
                print("exr version up folder가 server로 이동되었습니다.")

            elif ext == ".mov":
                # print(f"{ver_up_local_path}:모브로컬패스")
                # print(f"{ver_up_server_dev_paths[2]}:모브서버패스")
                shutil.copy2(ver_up_local_path, ver_up_server_dev_paths[2])
                shutil.copy2(ver_up_server_dev_paths[2], ver_up_server_pub_paths[2])
                print("mov version up file이 server로 이동되었습니다.")

    #=================================================================

    def _make_thumbnail_path(self):
        """Make a thumbnail_path and If thumbnail_folder is not existed, it needs to create """

        split = self.exr_folder_path.split("dev")[0]
        thumbnail_path = f"{split}.thumbnail"

        if not os.path.isdir(thumbnail_path):
            os.makedirs(thumbnail_path)

        return thumbnail_path
    
    def display_thumbnail_in_ui(self, image_path):

        base, png = os.path.splitext(image_path)
        origin_ext = base.split("_")[-1]

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(160, 160, Qt.AspectRatioMode.KeepAspectRatio)
            if origin_ext == "exr":
                self.ui.label_thumbnail_exr.setPixmap(scaled_pixmap)

            if origin_ext == "nk":
                self.ui.label_thumbnail_nk.setPixmap(scaled_pixmap)

            if origin_ext == "mov":
                self.ui.label_thumbnail_mov.setPixmap(scaled_pixmap)

    #=================================================================    

    def _create_nk_thumbnail(self, file_path, frame_number):
        # read_node 찾기 
        base_name = 'Read'
        max_num = 10

        for number in range(1, max_num + 1):
            node_name = f"{base_name}{number}"
            # print(node_name)
            read_node = nuke.toNode(node_name)
            if read_node is not None:
                break

        # reformat_node 생성 및 read_node와 연결
        reformat_node = nuke.createNode("Reformat")
        reformat_node.setInput(0, read_node)

        new_format_name = 'HD_1080'
        formats = nuke.formats()
        new_format = next((fmt for fmt in formats if fmt.name() == new_format_name), None)

        if new_format:
            reformat_node['format'].setValue(new_format)

        # write_node 생성 및 reformat_node와 연결
        write_node = nuke.createNode("Write")
        write_node.setInput(0, reformat_node)

        write_node["file"].setValue(file_path)
        write_node["first"].setValue(frame_number)
        write_node["last"].setValue(frame_number)

        # render
        nuke.execute(write_node, frame_number, frame_number)
        
        # clean up
        nuke.delete(write_node)
        nuke.delete(reformat_node)

    def generate_nk_thumbnail_from_file(self):

        nk_path = f"{self.nk_file_path}/{self.nk_file_names[0]}"
        base, ext = os.path.splitext(nk_path)
        image_name = base.split("/")[-1]
        thumbnail_path = self._make_thumbnail_path()
        if not os.path.isdir(thumbnail_path):
            os.makedirs(thumbnail_path)

        nk_png_path = f"{thumbnail_path}/{image_name}_nk.png"

        # display nk_thumbnail 
        if not os.path.isfile(nk_png_path):
            self._create_nk_thumbnail(nk_png_path, 1001)
            self.display_thumbnail_in_ui(nk_png_path)
            print("nk가 png가 되었습니다.")
        else:
            self.display_thumbnail_in_ui(nk_png_path)

        return nk_png_path

    #=================================================================

    def _create_exr_thumbnail(self, input, output):
        (
            ffmpeg
            .input(input)
            .output(output)
            .run()
        )

    def generate_exr_thumbnail_from_file(self):

        split = self.exr_folder_path.split("/")   # exr_folder_path : local path의 exr 폴더임
        shot_code = split[-5]
        team_name = split[-4]
        ver = self.folder_name
        exr_name = f"{shot_code}_{team_name}_{ver}.1001.exr"
        image_name = f"{shot_code}_{team_name}_{ver}.1001_exr.png"
        
        # thumbnail_folder_path = f"{self.exr_folder_path.split("dev")[0]}/.thumbnail"
        thumbnail_path = self._make_thumbnail_path()
        # print(thumbnail_path)

        if not os.path.isdir(thumbnail_path):
            os.makedirs(thumbnail_path)

        exr_path = f"{self.exr_folder_path}{ver}/{exr_name}"
        # print(f"{exr_path}:이엑스알")
        exr_png_path = f"{thumbnail_path}/{image_name}"
        # print(f"{exr_png_path}:이엑스알피엔지")

        if not os.path.isfile(exr_png_path):
            self._create_exr_thumbnail(exr_path, exr_png_path)
            self.display_thumbnail_in_ui(exr_png_path)
            print("exr이 png가 되었습니다.")
        else:
            self.display_thumbnail_in_ui(exr_png_path)

        return exr_png_path

    #=================================================================
    
    def _create_mov_thumbnail(self, input_path, output_path, frame_number=1):
        (
        ffmpeg
        .input(input_path, ss=0)
        .output(output_path, vframes=1)
        .run()
        )

    def generate_mov_thumbnail_from_file(self):

        mov_path = f"{self.mov_file_path}{self.mov_file_names[0]}"

        thumbnail_path = self._make_thumbnail_path()    
        image_name = self.mov_file_names[0].split(".")[0]
        mov_png_path = f"{thumbnail_path}/{image_name}_mov.png"

        if not os.path.isfile(mov_png_path):
            self._create_mov_thumbnail(mov_path, mov_png_path)
            self.display_thumbnail_in_ui(mov_png_path)
            print("mov가 png가 되었습니다.")
        else:
            self.display_thumbnail_in_ui(mov_png_path)

        return mov_png_path
    
    #=================================================================
    def gather_thumbnail_info(self):
        thumbnail_list = []
        nk_thumbnail_path = self.generate_nk_thumbnail_from_file()
        exr_thumbnail_path = self.generate_exr_thumbnail_from_file()
        mov_thumbnail_path = self.generate_mov_thumbnail_from_file()
        thumbnail_list.append(nk_thumbnail_path, exr_thumbnail_path, mov_thumbnail_path)

        return thumbnail_list

    def get_description_text(self):
        description_list = []
        nk_description = self.ui.lineEdit_description_nk.text()
        exr_description = self.ui.lineEdit_description_exr.text()
        mov_description = self.ui.lineEdit_description_mov.text()
        description_list.append(nk_description, exr_description, mov_description)

        return description_list

    def set_delete_icon(self):
        """set the trashbin_icon"""

        if self.ui.pushButton_delete.isChecked():
            image_path = "/home/rapa/yummy/pipeline/scripts/publish/delete_icon2.png"
        else:
            image_path = "/home/rapa/yummy/pipeline/scripts/publish/delete_icon2.png"

        # QPixmap을 사용하여 이미지를 로드하고 QIcon으로 변환
        pixmap = QPixmap(image_path)

        button_size = self.ui.pushButton_delete.size()
        scaled_pixmap = pixmap.scaled(button_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        # QIcon으로 변환 후 버튼 아이콘으로 설정
        icon = QIcon(scaled_pixmap)
        self.ui.pushButton_delete.setIcon(icon)
        icon_size = QSize(button_size.width() -12, button_size.height() - 12)
        self.ui.pushButton_delete.setIconSize(icon_size)  # 아이콘 크기 설정

#===============================================================     
    def make_message_for_upload_success(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Good")
        msg_box.setText("you've passed all the validation process."
                        "\n Now start to upload.")
        
        # button_thanks = QPushButton("Thanks!")
        # button_also_thanks = QPushButton("Also Thanks!")

        # msg_box.addButton(button_thanks, QMessageBox.AcceptRole)
        # msg_box.addButton(button_also_thanks, QMessageBox.RejectRole)
        result = msg_box.exec()     

        # msg_box.setStandardButtons(QMessageBox.OK | QMessageBox.AlsoThanks)

    def make_message_for_upload_ver(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setText("notValid in validateForm. \n",
                        self.val_nk(), 
                        self.val_exr(), 
                        self.val_mov(), 
                        "\n Do you still want to proceed?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setIcon(QMessageBox.Warning)
        result = msg_box.exec()                               
        if result == QMessageBox.Yes:       #force
            self.copy_to_Server_from_Local()
            self.sg_upload_data_ver()
            self.sg_create_ver()
            self.sg_thumbnail_upload()
        else:                              #validate again
            msg_box.setText("Please validate again.")

    def make_message_for_upload_pub(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setText("notValid in validateForm. \n",
                        self.val_nk(), 
                        self.val_exr(), 
                        self.val_mov(), 
                        "\n Do you still want to proceed?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setIcon(QMessageBox.Warning)
        result = msg_box.exec()                               
        if result == QMessageBox.Yes:       #force
            self.copy_to_Server_from_Local()
            self.sg_upload_data_pub()
            self.sg_create_ver()
            self.sg_create_pub()
            self.sg_thumbnail_upload()
        else:                              #validate again
            msg_box.setText("Please validate again.")

#===============================================================  
    def sg_upload_data_ver(self): 
        # sg = self.connect_sg()
        # json_file_path = '/home/rapa/YUMMY/pipeline/json/project_data.json'
        PF = PathFinder()
        sg_ver_data = PF._read_paths_from_json()
        # print(sg_ver_data)
        # sg = self.connect_sg()

        # project_name = sg_ver_data.get('project', 'N/A')
        project_id = sg_ver_data.get('project_id', 'N/A')
        user_name = sg_ver_data.get('name', 'N/A')
        # data_making = PF.data_needed()
        # project_id = PF.data_needed[1]
        # print(project_id)
        # ver_datas = {}


        # self.user_name = data_making[2]
        # user_name = self.user_name
        # ver_data  =[]
        if project_id:
            filters = [["project", "is", {"type": "Project", "id": project_id}]]
            # fields = ["code", "entity", "sg_version_type", "sg_status_list", "user"]
            to_use= self.sg.find("Version", filters = filters)
        if to_use : 
            #code, shot, shot_id빼서 정리
            shot = "PKG_030"
            code = shot + "_mm_v007"
            file_type = ".mov"
            file_path = '/home/rapa/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/mov/OPN_0010_cmp_v001.mov'
            version_nk = "15v2"
            colorspace = "sRGB"
            user_name = "UICHUL SHIN"

            ver_data = {
                "project" : {"type": "Project", "id" : project_id},
                "code" : code,
                # "image" : , =preview ; 썸네일, mov 올라갈 수 있도록
                "sg_status_list" : "wip",           #pub, sc
                "user": {"type" : "HumanUser", "name" : user_name, "id" : 93},
                "description" : "testing",
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

    def sg_create_ver(self):
        ver_data = self.sg_upload_data_ver()
        self.sg.create('Version', ver_data)
        print ("version 생성이 완료되었습니다.")

    def sg_upload_data_pub(self): 
        # sg = self.connect_sg()
        
        # json_file_path = '/home/rapa/YUMMY/pipeline/json/project_data.json'
        PF = PathFinder()

        # data_making = PF.data_needed()
        sg_ver_data = PF._read_paths_from_json()
        project_id = sg_ver_data.get('project_id', 'N/A')
        user_name = sg_ver_data.get('name', 'N/A')
        # project_id = data_making[1]
        # user_name = data_making[2]

        pub_data  =[]
        if project_id:
            filters = [["project", "is", {"type": "Project", "id": project_id}]]
            fields = ["code", "entity", "sg_version_type", "sg_status_list", "user"]
            find = self.sg.find("Version", filters=filters, fields=fields)

            #code, shot, shot_id빼서 정리
            shot = "PKG_030"
            code = shot + "_mm_v007"
            file_type = ".mov"
            file_path = '/home/rapa/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/mov/OPN_0010_cmp_v001.mov'
            version_nk = "15v2"
            colorspace = "sRGB"
        if find : 
            pub_data = {
                "project" : {"type": "Project", "id" : project_id},
                "code" : code,
                # "image" : , =preview ; 썸네일, mov 올라갈 수 있도록
                "sg_status_list" : "wip",           #pub, sc
                "user": {"type" : "HumanUser", "name" : user_name, "id" : user_id},
                "description" : "testing",
                "published_file_type" : file_type,         #exr, mov, nk
                "version" : self.ver_data[self.code],
                "sg_nk_version" : version_nk,
                "sg_colorspace_1" : colorspace
            }
            # sg.upload('Version', entity_id = "")
            # mov_file = '/Users/lucia/Desktop/4Codes/1Project/test_v001.mov'
            # sg.upload('Version', entity_id = "Content", path = mov_file, field_name = "sg_ddd", display_name = None)
            # print(pub_data)
            return pub_data

    def sg_create_pub(self, ver_data) : 
        self.sg.create('Publish', ver_data)
        print ("Publish 생성이 완료되었습니다.")

    def sg_thumbnail_upload():
        pass

def open_ui_in_nuke():
    from importlib import reload
    # import sys
    global win
    # sys.path.append("/home/rapa/yummy/pipeline/scripts/publish")
    import publish_0903
    reload(publish_0903)
    win = publish_0903.MainPublish()
    win.show()



if __name__ == "__main__":
    app = QApplication()
    win = MainPublish()
    win.show()
    # sys.exit(app.exec())








# issue : 
# 1. 0 -> 1 ? validate 할 것이 없는데?
# 2. version data 가져올 때 pub (final) 된 것이면 가져올 수 없게?
# 3. ver_data 가변적으로 앞 변수 가져올 수 있도록