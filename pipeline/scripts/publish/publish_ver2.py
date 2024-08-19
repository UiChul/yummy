try:
    from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile
    from PySide6.QtGui import  Qt

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile
    from PySide2.QtGui import  Qt

import os
import nuke

class Publish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "/home/rapa/yummy/pipeline/scripts/publish/publish_ver2.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.ui.pushButton_add_to_basket.clicked.connect(self.add_item_tablewidget_basket)

        self.set_nk_file_list()
        self.set_exr_file_list()
        self.make_tablewidget_basket()

    def make_tablewidget_basket(self):

        self.ui.tableWidget_basket.setHorizontalHeaderLabels(["Publish File", "File Info"])
        self.ui.tableWidget_basket.setVerticalHeaderLabels(["nk", "mov", "exr"])

        root_setup = nuke.root()
        print(root_setup)

    def add_item_tablewidget_basket(self):

        nk_items = self.ui.listWidget_nk.selectedItems()
        for nk_item in nk_items:
            nk_item = QTableWidgetItem()
            item_name = nk_item.text()
            nk_item.setText(item_name)
            self.ui.tableWidget_basket.setItem(0, 0, nk_item)

        exr_items = self.ui.listWidget_nk.selectedItems()
        for exr_item in exr_items:
            exr_item = QTableWidgetItem()
            item_name = exr_item.text()
            exr_item.setText(item_name)
            self.ui.tableWidget_basket.setItem(1, 0, exr_item)

        mov_items = self.ui.listWidget_nk.selectedItems()
        for mov_item in mov_items:
            mov_item = QTableWidgetItem()
            item_name = mov_item.text()
            mov_item.setText(item_name)
            self.ui.tableWidget_basket.setItem(2, 0, mov_item)
        
    def set_nk_file_list(self):

        current_file_path = nuke.scriptName()    #현재 nuke파일이 있는 절대경로
        nk_file_name = os.path.basename(current_file_path)    #파일이름 추출
        self.ui.listWidget_nk.addItem(nk_file_name)

    def set_exr_file_list(self):
        
        nk_file_path = nuke.scriptName()         #현재 nuke파일이 있는 절대경로
        dev_file_path = nk_file_path.split("work")[0]
        exr_file_path = dev_file_path + "souce/exr/"
        if os.path.isdir(exr_file_path):
            pass
        else:
            os.makedirs(exr_file_path)

        exr_file_names = os.listdir(exr_file_path)
        for exr_file_name in exr_file_names:
            self.ui.listWidget_exr.addItem(exr_file_name)

    def set_mov_file_list(self):
        
        nk_file_path = nuke.scriptName()         #현재 nuke파일이 있는 절대경로
        dev_file_path = nk_file_path.split("work")[0]
        mov_file_path = dev_file_path + "souce/mov/"
        if os.path.isdir(mov_file_path):
            pass
        else:
            os.makedirs(mov_file_path)

        mov_file_names = os.listdir(mov_file_path)
        for mov_file_name in mov_file_names:
            self.ui.listWidget_mov.addItem(mov_file_name)

if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()