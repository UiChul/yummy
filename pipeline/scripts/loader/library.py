from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QApplication,QHeaderView
from PySide6.QtWidgets import QTreeWidgetItem, QTableWidgetItem, QLabel
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap
import os

# from functools import partial

class Mainloader(QWidget):
    def __init__(self,info):
        super().__init__()
        self.set_up()
        
        self.project = info["project"]
        self.user = info["name"]
        
        self.set_main_laoder()
        self.set_comboBox_seq()

    def set_comboBox_seq(self):
        file_path = f"/home/rapa/YUMMY/project/{self.project}/seq"
        seq_list = os.listdir(file_path)
        self.ui.comboBox_seq.addItems(seq_list)
    













    def set_main_laoder(self):
    
        self.ui.label_projectname.setText(f"{self.project}")
        self.ui.label_username.setText(f"{self.user}")
        
    def set_up(self):
        from main_window_v002_ui import Ui_Form
        # ui_file_path = "/home/rapa/yummy/pipeline/scripts/loader/main_window.ui"
        # ui_file = QFile(ui_file_path)
        # ui_file.open(QFile.ReadOnly)
        # loader = QUiLoader()
        # self.ui = loader.load(ui_file,self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    

info = {"project" : "Marvelous" , "name" : "su"}

if __name__ == "__main__":
    app = QApplication()
    my  = Mainloader(info)
    my.show()
    app.exec()