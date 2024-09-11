
try:
    from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem
    from PySide6.QtWidgets import QListWidgetItem, QListWidget, QVBoxLayout
    from PySide6.QtWidgets import QFileDialog, QMessageBox
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

import nuke
import ffmpeg
import os
import re
import shutil
from publish_pathfinder import PathFinder

class MainPublish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "/home/rapa/yummy/pipeline/scripts/publish/publish_ver6.ui"

        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint) # UI 최상단 고정
        ui_file.close()

        self._collect_path_material()
        self.setup_top_bar()
        self.create_listwidget_in_groubBox()
        self.setup_tablewidget_basket()
        self.set_delete_icon()

        # Signal
        self.ui.pushButton_add_to_basket.clicked.connect(self.on_add_button_clicked)
        self.ui.pushButton_version.clicked.connect(self.copy_to_Main_from_Sub)
        self.ui.pushButton_publish.clicked.connect(self.copy_to_pub_in_MainServer)
        self.ui.pushButton_delete.clicked.connect(self.delete_tablewidget_item)

    def on_add_button_clicked(self):
        self.add_nk_item_tablewidget_basket()
        self.add_exr_item_tablewidget_basket()
        self.add_mov_item_tablewidget_basket()
        self.count_tablewidget_item()
        self.get_description_text()

    def _collect_path_material(self):
        """path meterial"""
        self.nk_full_path = nuke.scriptName()
        self.dev_folder_path = self.nk_full_path.split("work")[0]
        self.work_folder_path = self.dev_folder_path + "work/"
        self.exr_folder_path = self.dev_folder_path + "exr/"
        self.mov_folder_path = self.dev_folder_path + "mov/"
        
        name_without_ext = os.path.basename(self.nk_full_path)
        split = name_without_ext.split("_")
        
        self.seq = split[0]
        self.code = split[1]
        self.shot_code = f"{self.seq}_{self.code}"
        self.team = split[2]
        self.ver = split[3]

    def setup_top_bar(self):
        """Top-bar about information like project, team_name, shot_code """
        split = self.nk_full_path.split("/")
        project_name = split[-8]

        self.ui.label_project_name.setText(project_name)
        self.ui.label_shot_code.setText(self.shot_code)
        self.ui.label_team_name.setText(self.team)
        
    # ======================================================================

    def create_listwidget_in_groubBox(self):
        """create listwidget according to file extension and put into Group box"""

        # nk_page
        nk_page = QWidget()
        layout1 = QVBoxLayout(nk_page)

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

        self.exr_folder_listwidget = QListWidget()
        self.exr_folder_listwidget.setObjectName("exr_file_listwidget")

        layout2.addWidget(self.exr_folder_listwidget)
        self.exr_folder_listwidget.addItem("Double-click here to add folder")
        self.ui.groupBox_exr.setLayout(layout2)

        self.exr_folder_listwidget.itemDoubleClicked.connect(self.open_exr_folder_dialog)
        self.exr_folder_listwidget.itemDoubleClicked.connect(self.generate_exr_thumbnail_from_file)

        # mov_page
        mov_page = QWidget()
        layout3 = QVBoxLayout(mov_page)

        self.mov_file_listwidget = QListWidget()
        self.mov_file_listwidget.setObjectName("mov_file_listwidget")

        layout3.addWidget(self.mov_file_listwidget)
        self.mov_file_listwidget.addItem("Double-click here to add file")
        self.ui.groupBox_mov.setLayout(layout3)

        self.mov_file_listwidget.itemDoubleClicked.connect(self.open_mov_file_dialog)
        self.mov_file_listwidget.itemDoubleClicked.connect(self.generate_mov_thumbnail_from_file)


    def open_nk_file_dialog(self):
        """nk item Dialog"""

        file_dialog = QFileDialog.getOpenFileNames(self, "Select Files from Local", self.work_folder_path, "All Files (*)")
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
        """mov item Dialog"""

        file_dialog = QFileDialog.getOpenFileNames(self, "Select Files from Local", self.mov_folder_path, "All Files (*)")
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
        """exr item Dialog (by folder)"""

        QMessageBox.information(self, "Folder Selected", "Please select 'Folder' for exr")

        folder = QFileDialog.getExistingDirectory(self, "Select Folder from Local", self.exr_folder_path)
        if folder:
            self.folder_name = os.path.basename(folder)
            self.exr_folder_listwidget.clear()

            item = QListWidgetItem(self.folder_name)
            self.exr_folder_listwidget.addItem(item)
            self.exr_folder_listwidget.setCurrentItem(item)
      

    # ===================================================================

    def setup_tablewidget_basket(self):
        """when clicked the add button, items are added in tablewidget"""

        self.ui.tableWidget_basket.setHorizontalHeaderLabels(["Publish File", "File Info"])
        self.ui.tableWidget_basket.setVerticalHeaderLabels(["nk", "exr", "mov"])

        row_count = self.ui.tableWidget_basket.rowCount()
        height = 80
        for row in range(row_count):
            self.ui.tableWidget_basket.setRowHeight(row, height)

    def add_nk_item_tablewidget_basket(self):
        
        ### nk item ###
        nk_selected_files = self.nk_file_listwidget.selectedItems()
        if nk_selected_files:
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
        else:
            pass
            
    def add_mov_item_tablewidget_basket(self):

        ### mov item ###
        mov_selected_files = self.mov_file_listwidget.selectedItems()
        if mov_selected_files:
            for file in mov_selected_files:
                mov_item = QTableWidgetItem()
                mov_selected_file = file.text()
                mov_item.setText(mov_selected_file)
                self.ui.tableWidget_basket.setItem(2, 0, mov_item)

                mov_file_path = f"{self.mov_folder_path}{mov_selected_file}"
            
                mov_validation_info_dict = self._get_mov_validation_info(mov_file_path)
                mov_info_item = "\n".join(f"{key} : {value}" for key, value in mov_validation_info_dict.items())
                mov_validation_info = QTableWidgetItem(mov_info_item)
                mov_validation_info.setTextAlignment(Qt.AlignLeft | Qt.AlignTop) # 왼쪽 정렬, 위쪽 정렬
                self.ui.tableWidget_basket.setItem(2, 1, mov_validation_info)
        else:
            pass

    def add_exr_item_tablewidget_basket(self):

        ### exr item ###
        exr_selected_folders = self.exr_folder_listwidget.selectedItems()
        if exr_selected_folders:
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
        else:
            pass
        
    def _get_nk_validation_info(self):
        """takeout info for validation before going through publishing"""

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

    def _get_exr_validation_info(self, file_path):

            file_validation_info_dict = {}
            probe = ffmpeg.probe(file_path)

            # extract video_stream
            video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
            codec_name = video_stream['codec_name']
            colorspace = video_stream.get('color_space', "N/A")
            width = int(video_stream['width'])
            height = int(video_stream['height'])

            resolution = f"{width}x{height}"

            # file_validation dictionary
            file_validation_info_dict = {
                "file_path": file_path,
                "codec_name": codec_name,
                "colorspace": colorspace,
                "resolution": resolution,
            }
            return file_validation_info_dict
    
    def _get_mov_validation_info(self, file_path):

            file_validation_info_dict = {}
            probe = ffmpeg.probe(file_path)

            # extract video_stream
            video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
            codec_name = video_stream['codec_name']
            colorspace = video_stream.get('color_space', "N/A")
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            frame = int(video_stream['nb_frames'])

            resolution = f"{width}x{height}"

            # file_validation dictionary
            file_validation_info_dict = {
                "file_path": file_path,
                "codec_name": codec_name,
                "colorspace": colorspace,
                "resolution": resolution,
                "frame": frame
            }
            return file_validation_info_dict
    
    def count_tablewidget_item(self):
        """count items in tablewidget"""
        row_count = self.ui.tableWidget_basket.rowCount()

        item_count = 0

        for row in range(row_count):
            item = self.ui.tableWidget_basket.item(row, 0)
            if item:
                item_count += 1
                self.ui.label_item_count.setText(str(item_count))
                
        return item_count

    def delete_tablewidget_item(self):
        """delete items if you want"""
        item_count = self.count_tablewidget_item()
        selected_items = self.ui.tableWidget_basket.selectedItems()

        rows_to_clear = set()
        for item in selected_items:
            row = item.row()
            rows_to_clear.add(row)

        for row in rows_to_clear:
             for column in range(self.ui.tableWidget_basket.columnCount()):
                self.ui.tableWidget_basket.setItem(row, column, None)
            
    # #==================================================================
    # move items from seb_server to main_server 

    def _find_sub_server_path(self):

        table_items = self.ui.tableWidget_basket.selectedItems()

        origin_local_paths = []
        for item in table_items:
            if item:
                nk_item = self.ui.tableWidget_basket.item(0, 0)
                exr_item = self.ui.tableWidget_basket.item(1, 0)
                mov_item = self.ui.tableWidget_basket.item(2, 0)

                self.nk_item_text = nk_item.text() if nk_item else ""
                nk_local_path = f"{self.work_folder_path}{self.nk_item_text}"

                self.exr_item_text = exr_item.text() if exr_item else ""
                exr_local_path = f"{self.exr_folder_path}{self.exr_item_text}"

                self.mov_item_text = mov_item.text() if mov_item else ""
                mov_local_path = f"{self.mov_folder_path}{self.mov_item_text}"
                
            else:
                print("아이템이 없습니다.")
            
        origin_local_paths.extend([nk_local_path, exr_local_path, mov_local_path])

        return origin_local_paths
    
    def _get_highest_version_number(self, path, version_pattern):
        
        highest_version = 0
        for filename in os.listdir(path):
            match = version_pattern.search(filename)
            if match:
                version_number = int(match.group(0)[1:])
                if version_number > highest_version:
                    highest_version = version_number
     
        return highest_version
    
    def version_up_in_sub_server(self):
        """Take the file_path, version it up and Save it"""

        sub_server_paths = self._find_sub_server_path() # nk, mov는 파일까지 포함된 풀패스, exr은 버전폴더까지만

        version_pattern = re.compile("v\d{3}")
        
        new_ver_sub_server_paths = []
        for sub_server_path in sub_server_paths:
            base, ext = os.path.splitext(sub_server_path)
            base_dir = os.path.dirname(sub_server_path)

            highest_version = self._get_highest_version_number(base_dir, version_pattern) # nk, mov는 아이템에서 버전패턴 검색, exr은 폴더에서 버전패턴 검색
            origin_version = version_pattern.search(base).group(0)

            new_version = f"v{highest_version + 1:03}"

            new_base = base.replace(origin_version, new_version)

            if ext == ".nknc":
                nk_ver_up_path = f"{new_base}{ext}"
                self.nk_new_ver_item = nk_ver_up_path.split("/")[-1]
                new_ver_sub_server_paths.append(nk_ver_up_path)
                # print("======nk======")
                nuke.scriptSaveAs(nk_ver_up_path)
                print("nk file이 version-up 되었습니다.")

            elif ext == ".mov":
                mov_ver_up_path = f"{new_base}{ext}"
                self.mov_new_ver_item = mov_ver_up_path.split("/")[-1]
                print(f"{self.mov_new_ver_item}:모브뉴아이템")
                new_ver_sub_server_paths.append(mov_ver_up_path)
                shutil.copy2(sub_server_path, mov_ver_up_path)
                print("mov file이 version-up 되었습니다.")

            elif os.path.isdir(sub_server_path):    
                new_ver_folder = new_base        
                os.makedirs(new_ver_folder, exist_ok=True)

                for exr_file in os.listdir(sub_server_path):
                    current_path = os.path.join(sub_server_path, exr_file)
                    match = version_pattern.search(exr_file)
                    if match:
                        current_ver_in_file = match.group(0)
                        new_exr_file = exr_file.replace(current_ver_in_file, new_version)
                        new_exr_path = os.path.join(new_ver_folder, new_exr_file)
                        self.exr_new_ver_item = new_exr_path.split("/")[-1]
                        
                        shutil.copy2(current_path, new_exr_path)
                        new_ver_sub_server_paths.append(new_exr_path)
                print("exr file이 version-up 되었습니다")
                nuke.message("sub_server에서 version-up이 완료되었습니다.")
                
            else:
                pass

            
        return new_ver_sub_server_paths

    def _find_MainServer_seq_path(self):
        """Find matching folder from Json and make Server path until 'seq' """

        json_file_path = '/home/rapa/yummy/pipeline/json/project_data.json'
        path_finder = PathFinder(json_file_path)

        start_path = '/home/rapa/YUMMY/project'

        # Get the new path
        server_project_path = path_finder.append_project_to_path(start_path)
        server_seq_path = f"{server_project_path}seq/"

        return server_seq_path
    
    def _find_MainServer_path(self):
        """Get material item in tablewidget and append into seq_path""" 

        seq_path = self._find_MainServer_seq_path()

        verup_main_server_paths = []

        new_ver_folder = self.exr_new_ver_item.split(".")[0]
        nk_main_server_path = f"{seq_path}{self.seq}/{self.shot_code}/{self.team}/dev/work/{self.nk_new_ver_item}"
        exr_main_server_path = f"{seq_path}{self.seq}/{self.shot_code}/{self.team}/dev/exr/{new_ver_folder}"
        mov_main_server_path = f"{seq_path}{self.seq}/{self.shot_code}/{self.team}/dev/mov/{self.mov_new_ver_item}"

        verup_main_server_paths.extend([nk_main_server_path, exr_main_server_path, mov_main_server_path])

        return verup_main_server_paths
    
    def copy_to_Main_from_Sub(self):

        verup_sub_server_paths = self.version_up_in_sub_server()     #exr로 파일까지 풀패스로
        verup_main_server_paths = self._find_MainServer_path()

        for verup_sub_server_path in verup_sub_server_paths:
            verup_sub_server_path = verup_sub_server_path.strip()
            _, ext = os.path.splitext(verup_sub_server_path)

            if ext == ".nknc":
                shutil.copy2(verup_sub_server_path, verup_main_server_paths[0])
                print("nk version up file이 server로 이동되었습니다.")
            
            elif ext == ".exr":
                exr_verup_sub_server_path = os.path.dirname(verup_sub_server_path)   #exr은 폴더째로 이동하기위해
                shutil.copytree(exr_verup_sub_server_path, verup_main_server_paths[1], dirs_exist_ok=True)
                print("exr version up folder가 server로 이동되었습니다.")

            elif ext == ".mov":
                shutil.copy2(verup_sub_server_path, verup_main_server_paths[2])
                print("mov version up file이 server로 이동되었습니다.")

        nuke.message("main_server로 파일 이동이 완료되었습니다.")

    def _find_MainServer_pub_path(self):
        """Use Dev_folder_path to make Pub_folder_path"""

        verup_main_server_paths = self._find_MainServer_path()
        ver_up_server_pub_paths = []

        for path in verup_main_server_paths:
            pub_path = path.replace("dev", "pub")
            ver_up_server_pub_paths.append(pub_path)

        return ver_up_server_pub_paths

    def copy_to_pub_in_MainServer(self):

        verup_sub_server_paths = self.version_up_in_sub_server()
        verup_main_server_paths = self._find_MainServer_path()
        ver_up_server_pub_paths = self._find_MainServer_pub_path()

        for verup_sub_server_path in verup_sub_server_paths:
            verup_sub_server_path = verup_sub_server_path.strip()
            base, ext = os.path.splitext(verup_sub_server_path)

            if ext == ".nknc":
                shutil.copy2(verup_sub_server_path, verup_main_server_paths[0])
                shutil.copy2(verup_main_server_paths[0], ver_up_server_pub_paths[0])
                print("nk version up file이 server로 이동되었습니다.")
            
            elif ext == ".exr":
                exr_verup_sub_server_path = os.path.dirname(verup_sub_server_path)
                shutil.copytree(exr_verup_sub_server_path, verup_main_server_paths[1], dirs_exist_ok=True)
                shutil.copytree(verup_main_server_paths[1], ver_up_server_pub_paths[1], dirs_exist_ok=True)
                print("exr version up folder가 server로 이동되었습니다.")

            elif ext == ".mov":
                shutil.copy2(verup_sub_server_path, verup_main_server_paths[2])
                shutil.copy2(verup_main_server_paths[2], ver_up_server_pub_paths[2])
                print("mov version up file이 server로 이동되었습니다.")

        nuke.message("main_server의 pub폴더에 파일이 저장되었습니다.")

    # #=================================================================

    def _make_thumbnail_path(self):
        """Make a thumbnail_path and If thumbnail_folder is not existed, it needs to create """

        split = self.dev_folder_path.split("dev")[0]
        thumbnail_path = f"{split}.thumbnail"

        if not os.path.isdir(thumbnail_path):
            os.makedirs(thumbnail_path)

        return thumbnail_path
    
    def display_thumbnail_in_ui(self, image_path):

        base, _ = os.path.splitext(image_path)
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
    
    # #=================================================================    

    def _create_nk_thumbnail(self, file_path, frame_number):
        # read_node 찾기 
        base_name = 'Read'
        max_num = 10

        for number in range(1, max_num + 1):
            node_name = f"{base_name}{number}"
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

        nk_path = f"{self.work_folder_path}{self.nk_file_names[0]}"
        base, _ = os.path.splitext(nk_path)
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

    # #=================================================================

    def _create_exr_thumbnail(self, input, output):
        (
            ffmpeg
            .input(input)
            .output(output)
            .run()
        )

    def generate_exr_thumbnail_from_file(self):

        exr_name = f"{self.folder_name}.1001.exr"
        image_name = f"{self.folder_name}.1001_exr.png"
        
        thumbnail_path = self._make_thumbnail_path()

        if not os.path.isdir(thumbnail_path):
            os.makedirs(thumbnail_path)

        exr_path = f"{self.exr_folder_path}{self.folder_name}/{exr_name}"
        exr_png_path = f"{thumbnail_path}/{image_name}"

        if not os.path.isfile(exr_png_path):
            self._create_exr_thumbnail(exr_path, exr_png_path)
            self.display_thumbnail_in_ui(exr_png_path)
            print("exr이 png가 되었습니다.")
        else:
            self.display_thumbnail_in_ui(exr_png_path)

        return exr_png_path
            
    # #=================================================================
    
    def _create_mov_thumbnail(self, input_path, output_path, frame_number=1):
        (
        ffmpeg
        .input(input_path, ss=0)
        .output(output_path, vframes=1)
        .run()
        )
        
    def generate_mov_thumbnail_from_file(self):
        
        mov_path = f"{self.mov_folder_path}{self.mov_file_names[0]}"

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
    

    # #=================================================================
    def gather_thumbnail_info(self):
        thumbnail_list = []
        nk_thumbnail_path = self.generate_nk_thumbnail_from_file()
        exr_thumbnail_path = self.generate_exr_thumbnail_from_file()
        mov_thumbnail_path = self.generate_mov_thumbnail_from_file()
        thumbnail_list.append(nk_thumbnail_path, exr_thumbnail_path, mov_thumbnail_path)

        return thumbnail_list

    def get_description_text(self):
        description_list = []
        nk_description = self.ui.lineEdit_description_nk.text() or ""
        exr_description = self.ui.lineEdit_description_exr.text() or ""
        mov_description = self.ui.lineEdit_description_mov.text() or ""
  
        description_list.extend([nk_description, exr_description, mov_description])

        return description_list
    
    def set_delete_icon(self):
        """set the trashbin_icon"""

        if self.ui.pushButton_delete.isChecked():
            image_path = "/home/rapa/yummy/pipeline/scripts/publish/delete_icon2.png"
        else:
            image_path = "/home/rapa/yummy/pipeline/scripts/publish/delete_icon2.png"

        # use QPixmap for image load and convert to QIcon
        pixmap = QPixmap(image_path)

        button_size = self.ui.pushButton_delete.size()
        scaled_pixmap = pixmap.scaled(button_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        # After converting, set the icon as button
        icon = QIcon(scaled_pixmap)
        self.ui.pushButton_delete.setIcon(icon)
        icon_size = QSize(button_size.width() -12, button_size.height() - 12)
        self.ui.pushButton_delete.setIconSize(icon_size)

def open_ui_in_nuke():
    from importlib import reload
    import sys
    global win
    sys.path.append("/home/rapa/sub_server/pipeline/scripts")
    import publish_main
    reload(publish_main)
    win = publish_main.MainPublish()
    win.show()


if __name__ == "__main__":
    app = QApplication()
    win = MainPublish()
    win.show()
    app.exec()

