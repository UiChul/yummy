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

        self.ui.pushButton_add_to_basket.clicked.connect(self.add_to_publisher)

        self.set_nk_file_list()
        self.make_tablewidget_basket()
        # self.temp_signal_for_widget()

    def make_tablewidget_basket(self):
        self.ui.tableWidget_basket.setHorizontalHeaderLabels(["Publish File", "File Info"])
        self.ui.tableWidget_basket.setVerticalHeaderLabels(["nk", "mov", "exr"])
    
    # def temp_signal_for_widget(self):

    def add_to_publisher(self):
        items = self.ui.listWidget_nk.selectedItems()
        for item in items:
            table_item = QTableWidgetItem()
            print(item)
            table_item.setText(str(item))
            self.ui.tableWidget_basket.setItem(0, 0, table_item)
        
    def set_nk_file_list(self):

        current_file_path = nuke.root().name()    #현재 nuke파일이 있는 절대경로
        nk_file_name = os.path.basename(current_file_path)    #파일이름 추출
        self.ui.listWidget_nk.addItem(nk_file_name)


if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()