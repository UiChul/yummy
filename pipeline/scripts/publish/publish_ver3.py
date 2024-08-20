# class 객체화
# {shot}/nuke/renders/{shot}_comp{_nameindex}_{version}.####.{ext}


try:
    from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem, QToolBox, QCheckBox, QListWidgetItem, QVBoxLayout
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile
    from PySide6.QtGui import  Qt

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem, QToolBox, QCheckBox, QListWidgetItem, QVBoxLayout
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile
    from PySide2.QtGui import  Qt

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

        self.ui.pushButton_add_to_basket.clicked.connect(self.add_item_tablewidget_basket)

        # self.set_nk_file_list()
        self.set_exr_file_list()
        self.make_tablewidget_basket()
        self.bring_info_for_validation()
        # self.create_listwidget()

        # self.setItemWidget(self.create_listwidget("item"))

    # def create_listwidget(self, text):
    #     widget = QWidget()
    #     layout = QVBoxLayout()
    #     checkbox = QCheckBox(text)
    #     layout.addWidget(checkbox)
    #     widget.setLayout(layout)

    #     item = QListWidgetItem()
    #     self.addItem()
    #     self.setItemWidget(item, widget)

        # current_file_path = nuke.scriptName()    #현재 nuke파일이 있는 절대경로
        # nk_file_name = os.path.basename(current_file_path)    #파일이름 추출
        # self.ui.listWidget_nk.addItem(nk_file_name)

        # checkbox = QCheckBox()
        # self.ui.listWidget_nk.addWidget(checkbox)

    def set_nk_file_list(self):

        current_file_path = nuke.scriptName()    #현재 nuke파일이 있는 절대경로
        nk_file_name = os.path.basename(current_file_path)    #파일이름 추출
        self.ui.listWidget_nk.addItem(nk_file_name)

        checkbox = QCheckBox()
        self.ui.listWidget_nk.addWidget(checkbox)

    def set_exr_file_list(self):
        
        nk_file_path = nuke.scriptName()         #현재 nuke파일이 있는 절대경로
        dev_file_path = os.path.dirname(nk_file_path)
        exr_file_path = f"{dev_file_path}/source/exr/"
        if os.path.isdir(exr_file_path):
            pass
        else:
            os.makedirs(exr_file_path)

        exr_file_names = os.listdir(exr_file_path)
        for exr_file_name in exr_file_names:
            self.ui.listWidget_exr.addItem(exr_file_name)

    def set_mov_file_list(self):
        
        nk_file_path = nuke.scriptName()         #현재 nuke파일이 있는 절대경로
        dev_file_path = os.path.dirname(nk_file_path)
        mov_file_path = f"{dev_file_path}/source/mov/"
        if os.path.isdir(mov_file_path):
            pass
        else:
            os.makedirs(mov_file_path)

        mov_file_names = os.listdir(mov_file_path)
        for mov_file_name in mov_file_names:
            self.ui.listWidget_mov.addItem(mov_file_name)







    def make_tablewidget_basket(self):

        self.ui.tableWidget_basket.setHorizontalHeaderLabels(["Publish File", "File Info"])
        self.ui.tableWidget_basket.setVerticalHeaderLabels(["nk", "exr", "mov"])

    def bring_info_for_validation(self):

        # nk_file_validation
        root = nuke.root()
        path = root["name"].value()
        extend = path.split(".")[-1]
        colorspace = root["colorManagement"].value()
        nuke_version = nuke.NUKE_VERSION_STRING

        # exr_file_validation
        # from ffmpeg

        # for mov_file_validation
        # from ffmpeg

    def add_item_tablewidget_basket(self):

        nk_file_items = self.ui.listWidget_nk.selectedItems()
        for nk_file_item in nk_file_items:
            item_name = nk_file_item.text()
            nk_file_item=QTableWidgetItem()
            nk_file_item.setText(item_name)
            self.ui.tableWidget_basket.setItem(0, 0, nk_file_item)

        # exr_dict = {}
        exr_file_items = self.ui.listWidget_exr.selectedItems()
        for exr_file_item in exr_file_items:
            item_name = exr_file_item.text()
            exr_file_item = QTableWidgetItem()
            exr_file_item.setText(item_name)
            self.ui.tableWidget_basket.setItem(1, 0, exr_file_item)

        mov_file_items = self.ui.listWidget_mov.selectedItems()
        for mov_file_item in mov_file_items:
            item_name = mov_file_item.text()
            mov_file_item = QTableWidgetItem()
            mov_file_item.setText(item_name)
            self.ui.tableWidget_basket.setItem(2, 0, mov_file_item)

        if not self.ui.tableWidget_basket.item(0,0):
            print("아이템 없음")
        else:
            print("아이템 잇음")




if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()