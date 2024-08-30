# MODI
### making error&pass code when already ver number in it -- 목
### tumbnail, description output process --- 목
### render/publish setting in nuke -- 목
### nk info 중 path 이상하게나옴 ;; 수정해야함 --금
### find maximum version in Local_path -- 금
### complete ALL process (open nuke > use ui > shotgrid upload/publish) -- 금
### 금요일 퇴근전 의철님께 넘기기★
### 주말 코드 수정/레쥬메/등등

try:
    from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem
    from PySide6.QtWidgets import QListWidgetItem, QListWidget, QHBoxLayout
    from PySide6.QtWidgets import QVBoxLayout, QFileDialog, QMessageBox, QGroupBox
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, Signal, QObject
    from PySide6.QtGui import  Qt, QPixmap

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem
    from PySide2.QtWidgets import QListWidgetItem, QListWidget, QHBoxLayout
    from PySide2.QtWidgets import QVBoxLayout, QFileDialog, QMessageBox, QGroupBox
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, Signal, QObject
    from PySide2.QtGui import  Qt, QPixmap

import os
import re
import nuke
import json
import ffmpeg
import shutil
# import functools


class PathFinder:
    """
    Read Json File and find matching material (key:project_name)
    and then find Local path
    """

    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.key = 'project'
        self.json_data = self._read_paths_from_json()

    def _read_paths_from_json(self):
        """Read Json file and data return"""

        # try:
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
        # except FileNotFoundError:
        #     print(f"Error: The file {self.json_file_path} was not found.")
        #     return {}
        # except json.JSONDecodeError:
        #     print("Error: The JSON file could not be decoded.")
        #     return {}
        # except UnicodeDecodeError:
        #     print("Error: The file encoding is not correct. Please check the file encoding.")
        #     return {}

    def append_project_to_path(self, start_path):
        """Find data that matches key(project_name) in Json data"""

        # if self.key not in self.json_data:
        #     print(f"Error: Key '{self.key}' not found in the Json data.")
        #     return None

        project_value = self.json_data[self.key]
        
        start_path = start_path.rstrip(os.sep)
        
        new_path = f"{start_path}/{project_value}/"
        
        return new_path

class MainPublish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "C:/Users/LEE JIYEON/yummy/pipeline/scripts/publish/publish_ver6.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint) # UI 최상단 고정
        ui_file.close()

        self.setup_file_in_groubBox_from_Local()
        self.setup_top_bar()
        self.setup_tablewidget_basket()

        self._collect_path()

        # Signal
        self.ui.pushButton_add_to_basket.clicked.connect(self.add_nk_item_tablewidget_basket)
        self.ui.pushButton_add_to_basket.clicked.connect(self.add_exr_item_tablewidget_basket)
        self.ui.pushButton_add_to_basket.clicked.connect(self.add_mov_item_tablewidget_basket)
        self.ui.pushButton_version.clicked.connect(self.copy_to_Server_from_Local)
        self.ui.pushButton_publish.clicked.connect(self.copy_to_pub_from_dev_in_Server)

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
            self.nk_file_listwidget.addItems(self.nk_file_names)
            # print(self.nk_file_names)

    def open_mov_file_dialog(self):
        file_dialog = QFileDialog.getOpenFileNames(self, "Select Files from Local", self.mov_file_path, "All Files (*)")
        selected_files = file_dialog[0]
        if selected_files:
            self.mov_file_names = [os.path.basename(path) for path in selected_files]
            self.mov_file_listwidget.clear()
            self.mov_file_listwidget.addItems(self.mov_file_names)

    def open_exr_folder_dialog(self):
        QMessageBox.information(self, "Folder Selected", "Please select 'Folder' for exr")

        folder = QFileDialog.getExistingDirectory(self, "Select Folder from Local", self.exr_folder_path)
        if folder:
            self.folder_name = os.path.basename(folder)
            self.exr_folder_listwidget.clear()
            self.exr_folder_listwidget.addItem(self.folder_name)
            # self.generate_thumbnail_from_file()
      
    def setup_top_bar(self):

        # self.nk_file_path = nuke.scriptName()
        split = self.nk_file_path.split("/")
        project_name = split[5]
        shot_code = split[8]
        team_name = split[9]
        self.ui.label_project_name.setText(project_name)
        self.ui.label_shot_code.setText(shot_code)
        self.ui.label_team_name.setText(team_name)

    def _collect_path(self):
        
        self.current_nk_file_path = nuke.scriptName()
        self.work_path = f"{os.path.dirname(self.current_nk_file_path)}/"
        self.dev_path = self.work_path.split("work")[0]
        self.exr_folder_path = f"{self.dev_path}exr/"
        self.mov_file_path = f"{self.dev_path}mov/"

        # print(self.work_path)
        # print(self.dev_path)
        # print(self.exr_folder_path)
        # print(self.mov_file_path)

    #===================================================================

    def setup_tablewidget_basket(self):

        self.ui.tableWidget_basket.setHorizontalHeaderLabels(["Publish File", "File Info"])
        self.ui.tableWidget_basket.setVerticalHeaderLabels(["nk", "exr", "mov"])

        row_count = self.ui.tableWidget_basket.rowCount()
        height = 85
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

                exr_validation_info_dict = self._get_exr_and_mov_validation_info(self.exr_full_path)
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

            mov_new_path = f"{self.mov_file_path}{mov_selected_file}"
        
            mov_validation_info_dict = self._get_exr_and_mov_validation_info(mov_new_path)
            mov_info_item = "\n".join(f"{key} : {value}" for key, value in mov_validation_info_dict.items())
            mov_validation_info = QTableWidgetItem(mov_info_item)
            mov_validation_info.setTextAlignment(Qt.AlignLeft | Qt.AlignTop) # 왼쪽 정렬, 위쪽 정렬
            self.ui.tableWidget_basket.setItem(2, 1, mov_validation_info)

    def _get_nk_validation_info(self):

        nk_file_validation_dict = {}
        root = nuke.root()
        path = root["name"].value()                     # file path
        extend = path.split(".")[-1]                    # extendation
        colorspace = root["colorManagement"].value()    # colorspace
        nuke_version = nuke.NUKE_VERSION_STRING         # nk version
        
        nk_file_validation_dict["file_path"] = path
        nk_file_validation_dict["extend"] = extend
        nk_file_validation_dict["colorspace"] = colorspace
        nk_file_validation_dict["nuke_version"] = nuke_version

        return nk_file_validation_dict

    def _get_exr_and_mov_validation_info(self, file_path):

            file_validation_info_dict = {}
            probe = ffmpeg.probe(file_path)

            # extract video_stream
            video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
            codec_name = video_stream['codec_name']
            colorspace = video_stream.get('color_space', "N/A")
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            # a = video_stream.keys()
            # print(a)

            resolution = f"{width}x{height}"

            if file_path.split(".")[-1] == "mov":
                frame = int(video_stream['nb_frames'])

            elif file_path.split(".")[-1] == "exr":
                frame = 1

            # file_validation dictionary
            file_validation_info_dict = {
                "file_path": file_path,
                "codec_name": codec_name,
                "colorspace": colorspace,
                "resolution": resolution,
                "frame": frame
            }
            # print(file_validation_info_dict)
            return file_validation_info_dict

    #==================================================================

    def _find_Local_path(self):

        table_items = self.ui.tableWidget_basket.selectedItems()

        ver_up_local_path = []
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
            
        ver_up_local_path.extend([nk_local_path, exr_local_path, mov_local_path])

        return ver_up_local_path
    
    def increase_version_in_Local(self):
        """Take the file_path, version it up and Save it"""

        local_paths = self._find_Local_path()

        version_pattern = re.compile("v\d{3}")
        
        ver_up_local_paths = []
        for local_path in local_paths:
            base, ext = os.path.splitext(local_path)
            match = version_pattern.search(base)
            current_version = match.group(0)
            new_number = int(current_version[1:]) + 1
            new_version = f"v{new_number:03}"   # 현재 버전 번호가 존재하면 버전 번호를 증가
            new_base = base.replace(current_version, new_version)

            if ext == ".nknc":
                nk_version_up_path = f"{new_base}{ext}"
                ver_up_local_paths.append(nk_version_up_path)
                # print("======nk======")
                nuke.scriptSaveAs(nk_version_up_path)
                print("nk file이 version-up 되었습니다.")

            elif ext == ".mov":
                mov_version_up_path = f"{new_base}{ext}"
                ver_up_local_paths.append(mov_version_up_path)
                # print("======mov======")
                shutil.copy2(base+ext, mov_version_up_path)
                print("mov file이 version-up 되었습니다.")

            else:
                new_ver_folder = new_base
                os.makedirs(new_ver_folder)
                # print(base)
                exr_files = os.listdir(base)
                # print(exr_files)
                for exr_file in exr_files:
                    current_path = f"{base}/{exr_file}"
                    # print(current_path)
                    new_ver_folder_path = f"{new_ver_folder}/{exr_file}"
                    # print(new_ver_folder_path)
                    match = version_pattern.search(exr_file)
                    exr_current_version = match.group(0)
                    exr_new_number = int(exr_current_version[1:]) + 1
                    exr_new_version = f"v{exr_new_number:03}"   # 현재 버전 번호가 존재하면 버전 번호를 증가
                    exr_version_up_path = new_ver_folder_path.replace(exr_current_version, exr_new_version)
                    ver_up_local_paths.append(exr_version_up_path)
                    # print(exr_version_up_path)
                    shutil.copy2(current_path, exr_version_up_path)
        return ver_up_local_paths

    def _find_Server_seq_path(self):
        """Find matching folder from Json and make Server path until 'seq' """

        json_file_path = 'C:/home/rapa/YUMMY/pipeline/json/project_data.json'
        path_finder = PathFinder(json_file_path)

        start_path = 'C:/home/rapa/YUMMY/project'

        # Get the new path
        server_project_path = path_finder.append_project_to_path(start_path)
        server_seq_path = f"{server_project_path}seq/"
        # print(server_seq_path)

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

        ver_up_local_paths = self.increase_version_in_Local()
        ver_up_server_dev_paths = self._find_Server_dev_path()

        for ver_up_local_path in ver_up_local_paths:
            ver_up_local_path = ver_up_local_path.strip()
            base, ext = os.path.splitext(ver_up_local_path)
            print(ext)

            if ext == ".nknc":
                # print(f"{ver_up_local_path}:누크로컬패스")
                # print(f"{ver_up_server_dev_paths[0]}:누크서버패스")
                shutil.copy2(ver_up_local_path, ver_up_server_dev_paths[0])
                print("nk version up file이 server로 이동되었습니다.")
            
            elif ext == ".exr":
                exr_ver_up_local_path = os.path.dirname(ver_up_local_path)
                # print(f"{exr_ver_up_local_path}:이엑스알로컬패스")
                # print(f"{ver_up_server_dev_paths[1]}:이엑스알서버패스")
                shutil.copytree(exr_ver_up_local_path, ver_up_server_dev_paths[1], dirs_exist_ok=True)
                print("exr version up folder가 server로 이동되었습니다.")

            elif ext == ".mov":
                # print(f"{ver_up_local_path}:모브로컬패스")
                # print(f"{ver_up_server_dev_paths[2]}:모브서버패스")
                shutil.copy2(ver_up_local_path, ver_up_server_dev_paths[2])
                print("mov version up file이 server로 이동되었습니다.")

    def _find_Server_pub_path(self):
        """Use Dev_folder_path to make Pub_folder_path"""

        ver_up_server_dev_paths = self._find_Server_dev_path()
        ver_up_server_pub_paths = []

        for path in ver_up_server_dev_paths:
            pub_path = path.replace("dev", "pub")
            ver_up_server_pub_paths.append(pub_path)

        return ver_up_server_pub_paths

    def copy_to_pub_from_dev_in_Server(self):

        ver_up_local_paths = self.increase_version_in_Local()
        ver_up_server_dev_paths = self._find_Server_dev_path()
        ver_up_server_pub_paths = self._find_Server_pub_path()

        for ver_up_local_path in ver_up_local_paths:
            ver_up_local_path = ver_up_local_path.strip()
            base, ext = os.path.splitext(ver_up_local_path)
            print(ext)

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
        
        reformat_node = nuke.createNode("Reformat")
        write_node = nuke.createNode("Write")
        write_node.setInput(0, reformat_node)

        new_format_name = 'HD_1080'
        formats = nuke.formats()
        new_format = next((fmt for fmt in formats if fmt.name() == new_format_name), None)

        if new_format:
            reformat_node['format'].setValue(new_format)

        # nk_png_path = self.generate_nk_thumbnail_from_file()
        write_node["file"].setValue(file_path)
        write_node["first"].setValue(frame_number)
        write_node["last"].setValue(frame_number)
        print(file_path)

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
        print(thumbnail_path)

        if not os.path.isdir(thumbnail_path):
            os.makedirs(thumbnail_path)

        exr_path = f"{self.exr_folder_path}{ver}/{exr_name}"
        print(f"{exr_path}:이엑스알")
        exr_png_path = f"{thumbnail_path}/{image_name}"
        print(f"{exr_png_path}:이엑스알피엔지")

        if not os.path.isfile(exr_png_path):
            self._create_exr_thumbnail(exr_path, exr_png_path)
            self.display_thumbnail_in_ui(exr_png_path)
            print("exr이 png가 되었습니다.")
        else:
            self.display_thumbnail_in_ui(exr_png_path)
            
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
    #=================================================================


if __name__ == "__main__":
    app = QApplication()
    win = MainPublish()
    win.show()
    app.exec()

