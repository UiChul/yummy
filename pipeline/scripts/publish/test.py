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

import re
import os
import ffmpeg

class Publish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "/home/rapa/yummy/pipeline/scripts/publish/publish_ver4.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint) # UI 최상단 고정
        ui_file.close()

        self.ui.pushButton_add_to_basket.clicked.connect(self.add_item_tablewidget_basket)
        
        self.make_toolbox()
        self.setup_mov_file_list()
        # self.add_item_tablewidget_basket()

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

    def setup_mov_file_list(self):

        nk_file_path = "/home/rapa/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/work/"
        dev_file_path = nk_file_path.split("work")[0]   # dev_dir path
        self.mov_file_path = f"{dev_file_path}source/mov/"
        # print(self.mov_file_path)
        if not os.path.isdir(self.mov_file_path):
            os.makedirs(self.mov_file_path)

        self.mov_file_listwidget = self.ui.toolBox.findChild(QListWidget, "mov_file_listwidget")
        if self.mov_file_listwidget:
            mov_file_names = os.listdir(self.mov_file_path)
            # print(mov_file_names)
            for mov_file_name in mov_file_names:
                mov_item = QListWidgetItem(mov_file_name)
                mov_item.setFlags(mov_item.flags() | Qt.ItemIsUserCheckable)
                mov_item.setCheckState(Qt.Unchecked)
                self.mov_file_listwidget.addItem(mov_item)

    def add_item_tablewidget_basket(self):

        mov_selected_files = self.mov_file_listwidget.selectedItems()
        for mov_selected_file in mov_selected_files:
            item = QTableWidgetItem()
            item_name = mov_selected_file.text()
            item.setText(item_name)
            self.ui.tableWidget_basket.setItem(2, 0, item)

            mov_full_path = f"{self.mov_file_path}{item_name}"
            print(mov_full_path)
            mov_file_validation_info = self._get_exr_and_mov_validation_info(mov_full_path)
            print(mov_file_validation_info)


    def _get_exr_and_mov_validation_info(self, file_path):

            file_validation_info = {}
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
            file_validation_info = {
                "file_path": file_path,
                "codec_name": codec_name,
                "colorspace": colorspace,
                "resolution": resolution,
                "frame": frame
            }
            # print(file_validation_info)
            return file_validation_info

if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()
