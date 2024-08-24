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

import functools
import os
import nuke

class Publish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "/home/rapa/yummy/pipeline/scripts/publish/publish_ver3.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
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
        self.bring_info_for_validation()

    def make_toolbox(self):
        
        # Remove previous page
        while self.ui.toolBox.count() > 0:
            self.ui.toolBox.removeItem(0)

        # nk_page
        nk_page = QWidget()
        layout1 = QVBoxLayout(nk_page)
        nk_file_list = QListWidget()
        nk_file_list.setSelectionMode(QListWidget.MultiSelection)
        nk_file_list.setObjectName("nk_file_list")
        layout1.addWidget(nk_file_list)
        self.ui.toolBox.addItem(nk_page, "nk")

        # exr_page
        exr_page = QWidget()
        layout2 = QVBoxLayout(exr_page)
        exr_file_list = QListWidget()
        exr_file_list.setSelectionMode(QListWidget.MultiSelection)
        exr_file_list.setObjectName("exr_file_list")
        layout2.addWidget(exr_file_list)
        self.ui.toolBox.addItem(exr_page, "exr")

        # mov_page
        mov_page = QWidget()
        layout3 = QVBoxLayout(mov_page)
        mov_file_list = QListWidget()
        mov_file_list.setSelectionMode(QListWidget.MultiSelection)
        mov_file_list.setObjectName("mov_file_list")
        layout3.addWidget(mov_file_list)
        self.ui.toolBox.addItem(mov_page, "mov")

        # Signal
        nk_file_list.itemClicked.connect(self.display_thumbnail)
        nk_file_list.itemChanged.connect(self.setup_nk_file_list)

    def setup_top_bar(self):

        nk_file_path = nuke.scriptName()
        split = nk_file_path.split("/")
        print(split)
        project_name = split[5]
        shot_code = split[8]
        team_name = split[9]
        self.ui.label_project_name.setText(project_name)
        self.ui.label_shot_code.setText(shot_code)
        self.ui.label_team_name.setText(team_name)

    def setup_nk_file_list(self):

        current_file_path = nuke.scriptName()                 # 현재 nuke파일이 있는 절대경로
        nk_file_name = os.path.basename(current_file_path)    # 파일이름 추출
        self.nk_file_list = self.ui.toolBox.findChild(QListWidget, "nk_file_list")
        
        if self.nk_file_list:
            nk_item = QListWidgetItem(nk_file_name)
            nk_item.setFlags(nk_item.flags() | Qt.ItemIsUserCheckable)
            nk_item.setCheckState(Qt.Unchecked)
            self.nk_file_list.addItem(nk_item)
            if nk_item.checkState() == Qt.Checked:
                nk_item.setSelected(True)
            else:
                nk_item.setSelected(False)

    def setup_exr_file_list(self):
        
        nk_file_path = nuke.scriptName()                # 현재 nuke파일이 있는 절대경로
        dev_file_path = nk_file_path.split("work")[0]   # dev폴더경로
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

    def setup_mov_file_list(self):
        
        nk_file_path = nuke.scriptName()                # 현재 nuke파일이 있는 절대경로
        dev_file_path = nk_file_path.split("work")[0]   # dev폴더경로
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

    def bring_info_for_validation(self):

        #nk_file_validation
        root = nuke.root()
        path = root["name"].value()
        extend = path.split(".")[-1]
        colorspace = root["colorManagement"].value()
        nuke_version = nuke.NUKE_VERSION_STRING

        # exr_file_validation
        # from ffmpeg

        # for mov_file_validation
        # from ffmpeg

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

        write_node["file"].setValue(file_path)   # Set the file path for saving
        write_node["file_type"].setValue("png")  # Set the file type to png
        
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
