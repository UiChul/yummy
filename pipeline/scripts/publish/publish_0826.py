### nk info 중 path 이상하게나옴 ;; 수정해야함

### 0826 : version/publish upload
### 0827 : render

try:
    from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem, QListWidgetItem, QListWidget, QHBoxLayout, QVBoxLayout
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile
    from PySide6.QtGui import  Qt, QPixmap

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem, QListWidgetItem, QListWidget, QHBoxLayout, QVBoxLayout
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile
    from PySide2.QtGui import  Qt, QPixmap

import os
import re
import nuke
import ffmpeg
import functools

class Publish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "C:/Users/LEE JIYEON/yummy/pipeline/scripts/publish/publish_ver4.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint) # UI 최상단 고정
        ui_file.close()


        self.make_toolbox()
        self.setup_top_bar()
        self.setup_nk_file_list()
        self.setup_exr_file_list()
        self.setup_mov_file_list()

        self.setup_tablewidget_basket()

        # Signal
        self.ui.pushButton_add_to_basket.clicked.connect(self.add_item_tablewidget_basket)
        self.ui.pushButton_version.clicked.connect(self.increase_version_and_save_file)
        # self.ui.pushButton_version.clicked.connect(functools.partial(self.increase_version_and_save_file, nk_path))

        # self.increase_version("C:/Users/LEE JIYEON/Desktop/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/work/test0825_v001.nknc")

    def make_toolbox(self):
        
        # Remove previous page
        while self.ui.toolBox.count() > 0:
            self.ui.toolBox.removeItem(0)

        # nk_page
        nk_page = QWidget()
        layout1 = QVBoxLayout(nk_page)
        nk_file_listwidget = QListWidget()
        nk_file_listwidget.setSelectionMode(QListWidget.MultiSelection)    # multi select listwidget_item
        nk_file_listwidget.setObjectName("nk_file_listwidget")
        layout1.addWidget(nk_file_listwidget)
        self.ui.toolBox.addItem(nk_page, "nk")

        # exr_page
        exr_page = QWidget()
        layout2 = QVBoxLayout(exr_page)
        exr_file_listwidget = QListWidget()
        exr_file_listwidget.setSelectionMode(QListWidget.MultiSelection)   # multi select listwidget_item
        exr_file_listwidget.setObjectName("exr_file_listwidget")
        layout2.addWidget(exr_file_listwidget)
        self.ui.toolBox.addItem(exr_page, "exr")

        # mov_page
        mov_page = QWidget()
        layout3 = QVBoxLayout(mov_page)
        mov_file_listwidget = QListWidget()
        mov_file_listwidget.setSelectionMode(QListWidget.MultiSelection)   # multi select listwidget_item
        mov_file_listwidget.setObjectName("mov_file_listwidget")
        layout3.addWidget(mov_file_listwidget)
        self.ui.toolBox.addItem(mov_page, "mov")

        # Signal
        # nk_file_listwidget.itemClicked.connect(self.display_thumbnail)

    def setup_top_bar(self):

        nk_file_path = nuke.scriptName()
        split = nk_file_path.split("/")
        project_name = split[5]
        shot_code = split[8]
        team_name = split[9]
        self.ui.label_project_name.setText(project_name)
        self.ui.label_shot_code.setText(shot_code)
        self.ui.label_team_name.setText(team_name)

    def setup_nk_file_list(self):

        self.current_file_path = nuke.scriptName()
        nk_work_folder_path = os.path.dirname(self.current_file_path)
        self.nk_file_listwidget = self.ui.toolBox.findChild(QListWidget, "nk_file_listwidget")
        if self.nk_file_listwidget:
            nk_files = os.listdir(nk_work_folder_path)
            for nk_file in nk_files:
                nk_item = QListWidgetItem()
                nk_item.setText(nk_file)
                nk_item.setFlags(nk_item.flags() | Qt.ItemIsUserCheckable)
                nk_item.setCheckState(Qt.Unchecked)
                self.nk_file_listwidget.addItem(nk_item)

        # Signal
        self.nk_file_listwidget.itemClicked.connect(self._handle_checkbox_state)
    
    def setup_exr_file_list(self):
        
        # self.current_file_path = nuke.scriptName()
        dev_file_path = self.current_file_path.split("work")[0]   # dev_dir path
        self.exr_folder_path = f"{dev_file_path}source/exr/"
        # if os.path.isdir(self.exr_folder_path):
        #     pass
        # else:
        #     os.makedirs(self.exr_folder_path)

        self.exr_file_listwidget = self.ui.toolBox.findChild(QListWidget, "exr_file_listwidget")
        if self.exr_file_listwidget:
            exr_folders = os.listdir(self.exr_folder_path)         # exr은 폴더기준으로
            for exr_folder in exr_folders:
                exr_item = QListWidgetItem()
                exr_item.setText(exr_folder)
                exr_item.setFlags(exr_item.flags() | Qt.ItemIsUserCheckable)
                exr_item.setCheckState(Qt.Unchecked)
                self.exr_file_listwidget.addItem(exr_item)

        # Signal
        self.exr_file_listwidget.itemClicked.connect(self._handle_checkbox_state)

    def setup_mov_file_list(self):

        # self.current_file_path = nuke.scriptName()
        dev_file_path = self.current_file_path.split("work")[0]   # dev_dir path
        self.mov_folder_path = f"{dev_file_path}source/mov/"
        if not os.path.isdir(self.mov_folder_path):
            os.makedirs(self.mov_folder_path)

        self.mov_file_listwidget = self.ui.toolBox.findChild(QListWidget, "mov_file_listwidget")
        if self.mov_file_listwidget:
            mov_file_names = os.listdir(self.mov_folder_path)
            for mov_file_name in mov_file_names:
                mov_item = QListWidgetItem(mov_file_name)
                mov_item.setFlags(mov_item.flags() | Qt.ItemIsUserCheckable)
                mov_item.setCheckState(Qt.Unchecked)
                self.mov_file_listwidget.addItem(mov_item)

        # Signal
        self.mov_file_listwidget.itemClicked.connect(self._handle_checkbox_state)

    def _handle_checkbox_state(self, item):

        if item.checkState() == Qt.Unchecked:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)

#===================================================================

    def setup_tablewidget_basket(self):

        self.ui.tableWidget_basket.setHorizontalHeaderLabels(["Publish File", "File Info"])
        self.ui.tableWidget_basket.setVerticalHeaderLabels(["nk", "exr", "mov"])

        row_count = self.ui.tableWidget_basket.rowCount()
        height = 85
        for row in range(row_count):
            self.ui.tableWidget_basket.setRowHeight(row, height)

    def add_item_tablewidget_basket(self):
        
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


        ### exr item ###
        exr_selected_folders = self.exr_file_listwidget.selectedItems()
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

        ### mov item ###
        mov_selected_files = self.mov_file_listwidget.selectedItems()
        for file in mov_selected_files:
            mov_item = QTableWidgetItem()
            mov_selected_file = file.text()
            mov_item.setText(mov_selected_file)
            self.ui.tableWidget_basket.setItem(2, 0, mov_item)

            mov_new_path = f"{self.mov_folder_path}{mov_selected_file}"
        
            mov_validation_info_dict = self._get_exr_and_mov_validation_info(mov_new_path)
            mov_info_item = "\n".join(f"{key} : {value}" for key, value in mov_validation_info_dict.items())
            mov_validation_info = QTableWidgetItem(mov_info_item)
            mov_validation_info.setTextAlignment(Qt.AlignLeft | Qt.AlignTop) # 왼쪽 정렬, 위쪽 정렬
            self.ui.tableWidget_basket.setItem(2, 1, mov_validation_info)

        # print(nk_new_path)
        # return nk_new_path

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

    # def display_thumbnail(self):

    #     self.ui.label_thumbnail.clear()

    #     self.current_file_path = nuke.scriptName()
    #     nk_file_name = os.path.basename(self.current_file_path)
    #     png_file_name = nk_file_name.split(".")[0]

    #     image_path = f"C:/Users/LEE JIYEON/yummy/pipeline/scripts/publish/{png_file_name}.png"
    #     thumbnail = QPixmap(image_path)
    #     scaled_thumbnail = thumbnail.scaled(230, 190, Qt.AspectRatioMode.KeepAspectRatio)

    #     if os.path.exists(image_path):
    #         self.ui.label_thumbnail.setPixmap(scaled_thumbnail)
    #         return

    #     self.save_frame_as_thumbnail(image_path, 1001)

    # def save_frame_as_thumbnail(self, file_path, frame_number):
        
    #     reformat_node = nuke.createNode("Reformat")
    #     write_node = nuke.createNode("Write")
    #     write_node.setInput(0, reformat_node)

    #     new_format_name = 'HD_1080'
    #     formats = nuke.formats()
    #     new_format = next((fmt for fmt in formats if fmt.name() == new_format_name), None)

    #     if new_format:
    #         reformat_node['format'].setValue(new_format)

    #     write_node["file"].setValue(file_path)
    #     write_node["file_type"].setValue("png")
        
    #     write_node["first"].setValue(frame_number)
    #     write_node["last"].setValue(frame_number)
        
    #     # render
    #     nuke.execute(write_node, frame_number, frame_number)
        
    #     # clean up
    #     nuke.delete(write_node)
    #     nuke.delete(reformat_node)

#==================================================================
    def _make_version_new_path(self):
        table_items = self.ui.tableWidget_basket.selectedItems()

        new_path = []
        for item in table_items:
            if item:
                nk_item_text = self.ui.tableWidget_basket.item(0, 0).text()
                nk_new_path = f"{os.path.dirname(self.current_file_path)}/{nk_item_text}"
                
                exr_item_text = self.ui.tableWidget_basket.item(1, 0).text()
                exr_new_path = f"{self.exr_folder_path}{exr_item_text}"
                
                mov_item_text = self.ui.tableWidget_basket.item(2, 0).text()
                mov_new_path = f"{self.mov_folder_path}{mov_item_text}"
                
                new_path.extend([nk_new_path, exr_new_path, mov_new_path])
            else:
                print("아이템이 없습니다.")

        return new_path
    
    # def _get_exr_version_up_folder(self):
    #     os.listdir(self.exr_folder_path)

    def increase_version_and_save_file(self):
        """
        파일 경로 받아서 버전업시키고 save하는 함수
        """
        new_paths = self._make_version_new_path()

        for new_path in new_paths:
            base, ext = os.path.splitext(new_path)
            if ext in [".nknc", ".mov"]:
                # 현재 버전 번호 추출
                version_pattern = re.compile("v\d{3}$")
                match = version_pattern.search(base)
                if match:
                    current_version = match.group(0)
                    if current_version:
                        # 현재 버전 번호가 존재하면 버전 번호를 증가
                        version_number = int(current_version[1:]) + 1   # 버전 1씩 증가
                        new_version = f'v{version_number:03}'   # 버전 세 자리로 포맷팅
                    else:
                        # 버전 번호가 없으면 v001로 시작
                        version_number = "v001"
                    # new_base = version_pattern.sub(new_version, base)
                    new_base = f"{base}{new_version}"
                    new_file_path = f"{new_base}{ext}"

                    nuke.scriptSaveAs(new_file_path)
                    print(f"version_up_file이 저장되었습니다")

            else:
                pass


if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()
