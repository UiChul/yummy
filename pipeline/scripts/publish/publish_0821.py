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
import nuke
import ffmpeg

class Publish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "/home/rapa/yummy/pipeline/scripts/publish/publish_ver3.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint) # UI 최상단 고정
        ui_file.close()

        # Signal
        self.ui.pushButton_add_to_basket.clicked.connect(self.add_item_tablewidget_basket)

        self.make_toolbox()
        self.setup_top_bar()
        self.setup_nk_file_list()
        self.setup_exr_file_list()
        self.setup_mov_file_list()

        self.setup_tablewidget_basket()
        self.add_item_tablewidget_basket()
        self.bring_validation_info()
        self._get_exr_and_mov_validation_info("/home/rapa/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/source/exr/test_1001.exr")

    def make_toolbox(self):
        
        # Remove previous page
        while self.ui.toolBox.count() > 0:
            self.ui.toolBox.removeItem(0)

        # nk_page
        nk_page = QWidget()
        layout1 = QVBoxLayout(nk_page)
        nk_file_list = QListWidget()
        nk_file_list.setSelectionMode(QListWidget.MultiSelection)    # multi select listwidget_item
        nk_file_list.setObjectName("nk_file_list")
        layout1.addWidget(nk_file_list)
        self.ui.toolBox.addItem(nk_page, "nk")

        # exr_page
        exr_page = QWidget()
        layout2 = QVBoxLayout(exr_page)
        exr_file_list = QListWidget()
        exr_file_list.setSelectionMode(QListWidget.MultiSelection)   # multi select listwidget_item
        exr_file_list.setObjectName("exr_file_list")
        layout2.addWidget(exr_file_list)
        self.ui.toolBox.addItem(exr_page, "exr")

        # mov_page
        mov_page = QWidget()
        layout3 = QVBoxLayout(mov_page)
        mov_file_list = QListWidget()
        mov_file_list.setSelectionMode(QListWidget.MultiSelection)   # multi select listwidget_item
        mov_file_list.setObjectName("mov_file_list")
        layout3.addWidget(mov_file_list)
        self.ui.toolBox.addItem(mov_page, "mov")

        # Signal
        nk_file_list.itemClicked.connect(self.display_thumbnail)

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

        current_file_path = nuke.scriptName()                 # full_path
        nk_file_name = os.path.basename(current_file_path)    # export file_name from full_path
        self.nk_file_list = self.ui.toolBox.findChild(QListWidget, "nk_file_list")
        
        if self.nk_file_list:
            nk_item = QListWidgetItem(nk_file_name)
            nk_item.setFlags(nk_item.flags() | Qt.ItemIsUserCheckable)
            nk_item.setCheckState(Qt.Unchecked)
            self.nk_file_list.addItem(nk_item)

        # Signal
        self.nk_file_list.itemClicked.connect(self._handle_checkbox_state)

    def setup_exr_file_list(self):
        
        nk_file_path = nuke.scriptName()                # full_path
        dev_file_path = nk_file_path.split("work")[0]   # dev_dir path
        exr_file_path = f"{dev_file_path}source/exr/"
        if os.path.isdir(exr_file_path):
            pass
        else:
            os.makedirs(exr_file_path)

        self.exr_file_list = self.ui.toolBox.findChild(QListWidget, "exr_file_list")
        if self.exr_file_list:
            exr_file_names = os.listdir(exr_file_path)
            for exr_file_name in exr_file_names:
                exr_item = QListWidgetItem(exr_file_name)
                exr_item.setFlags(exr_item.flags() | Qt.ItemIsUserCheckable)
                exr_item.setCheckState(Qt.Unchecked)
                self.exr_file_list.addItem(exr_item)

        # Signal
        self.exr_file_list.itemClicked.connect(self._handle_checkbox_state)

        full_path = f"{exr_file_path}{exr_item}"
        print(full_path)
        # return full_path

    def setup_mov_file_list(self):
        
        nk_file_path = nuke.scriptName()                # full_path
        dev_file_path = nk_file_path.split("work")[0]   # dev_dir path
        mov_file_path = f"{dev_file_path}source/mov/"
        if os.path.isdir(mov_file_path):
            pass
        else:
            os.makedirs(mov_file_path)

        self.mov_file_list = self.ui.toolBox.findChild(QListWidget, "mov_file_list")
        if self.mov_file_list:
            mov_file_names = os.listdir(mov_file_path)
            for mov_file_name in mov_file_names:
                mov_item = QListWidgetItem(mov_file_name)
                mov_item.setFlags(mov_item.flags() | Qt.ItemIsUserCheckable)
                mov_item.setCheckState(Qt.Unchecked)
                self.mov_file_list.addItem(mov_item)

        # Signal
        self.mov_file_list.itemClicked.connect(self._handle_checkbox_state)

        full_path = f"{mov_file_path}{mov_item}"
        print(full_path)
        # return full_path

    def _handle_checkbox_state(self, item):

        if item.checkState() == Qt.Unchecked:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)

#===================================================================

    def setup_tablewidget_basket(self):

        self.ui.tableWidget_basket.setHorizontalHeaderLabels(["Publish File", "File Info"])
        self.ui.tableWidget_basket.setVerticalHeaderLabels(["nk", "mov", "exr"])

    def add_item_tablewidget_basket(self):
        nk_items = self.nk_file_list.selectedItems()
        for nk_item in nk_items:
            item = QTableWidgetItem()
            item_name = nk_item.text()
            item.setText(item_name)
            self.ui.tableWidget_basket.setItem(0, 0, item)

        exr_items = self.exr_file_list.selectedItems()
        for exr_item in exr_items:
            item = QTableWidgetItem()
            item_name = exr_item.text()
            item.setText(item_name)
            self.ui.tableWidget_basket.setItem(1, 0, item)

        mov_items = self.mov_file_list.selectedItems()
        for mov_item in mov_items:
            item = QTableWidgetItem()
            item_name = mov_item.text()
            item.setText(item_name)
            self.ui.tableWidget_basket.setItem(2, 0, item)

    def bring_validation_info(self):

        # nk_file_validation_info
        nk_file_validation = {}
        root = nuke.root()
        path = root["name"].value()                     # file path
        extend = path.split(".")[-1]                    # extendation
        colorspace = root["colorManagement"].value()    # colorspace
        nuke_version = nuke.NUKE_VERSION_STRING         # nk version
        
        nk_file_validation["file_path"] = path
        nk_file_validation["extend"] = extend
        nk_file_validation["colorspace"] = colorspace
        nk_file_validation["nuke_version"] = nuke_version

        # exr_file_validation_info
        # exr_file_path = self.setup_exr_file_list()
        # exr_file_validation = self._get_exr_and_mov_validation_info(exr_file_path)
        # print(exr_file_validation)

        # # mov_file_validation_info
        # mov_file_path = self.setup_mov_file_list()
        # print(mov_file_path)
        # mov_file_validation = self._get_exr_and_mov_validation_info(mov_file_path)
        # print(mov_file_validation)

    def _get_exr_and_mov_validation_info(self, file_path):

            file_validation_info = {}
            probe = ffmpeg.probe(file_path)

            # extract video_stream
            video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
            codec_name = video_stream['codec_name']
            colorspace = video_stream['color_space']
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            resolution = f"{width}x{height}"

            if file_path.split(".")[-1] == "mov":
                frame = int(video_stream['nb_frames'])
            else:
                frame = int(video_stream['frame'])
                print(frame)

            # file_validation dictionary
            file_validation_info["file_path"] = file_path
            file_validation_info["codec_name"] = codec_name
            file_validation_info["colorspace"] = colorspace
            file_validation_info["resolution"] = resolution
            file_validation_info["frame"] = frame
            print(file_validation_info)

            return file_validation_info

    def display_thumbnail(self):

        current_file_path = nuke.scriptName()
        nk_file_name = os.path.basename(current_file_path)
        png_file_name = nk_file_name.split(".")[0]

        image_path = f"/home/rapa/yummy/pipeline/scripts/publish/{png_file_name}.png"
        thumbnail = QPixmap(image_path)
        scaled_thumbnail = thumbnail.scaled(230, 190, Qt.AspectRatioMode.KeepAspectRatio)

        if os.path.exists(image_path):
            self.ui.label_thumbnail.setPixmap(scaled_thumbnail)
            return

        # self.ui.label_thumbnail.setPixmap(scaled_thumbnail)
        self.save_frame_as_thumbnail(image_path, 1001)

    def save_frame_as_thumbnail(self, file_path, frame_number):
        
        reformat_node = nuke.createNode("Reformat")
        write_node = nuke.createNode("Write")
        write_node.setInput(0, reformat_node)

        new_format_name = 'HD_1080'
        formats = nuke.formats()
        new_format = next((fmt for fmt in formats if fmt.name() == new_format_name), None)

        if new_format:
            reformat_node['format'].setValue(new_format)

        write_node["file"].setValue(file_path)
        write_node["file_type"].setValue("png")
        
        write_node["first"].setValue(frame_number)
        write_node["last"].setValue(frame_number)
        
        # render
        nuke.execute(write_node, frame_number, frame_number)
        
        # clean up
        nuke.delete(write_node)
        nuke.delete(reformat_node)

if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()
