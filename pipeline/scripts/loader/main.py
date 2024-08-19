from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QApplication,QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os

class Mainloader(QWidget):
    def __init__(self,info):
        super().__init__()
        self.set_up()
        
        self.project = info["project"]
        self.user = info["name"]
        
        self.set_main_laoder()
        self.set_comboBox_seq()
        
        
        #Signal
        self.ui.comboBox_seq.currentTextChanged.connect(self.set_comboBox_shot)
        
        
    def set_comboBox_seq(self):
        file_path = f"/home/rapa/YUMMY/project/{self.project}/seq"
        seq_list = os.listdir(file_path)
        self.ui.comboBox_seq.addItems(seq_list)
    
    def set_comboBox_shot(self,seq):
        self.ui.comboBox_shot_shotname.clear()
        file_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{seq}"
        shot_list = os.listdir(file_path)
        self.ui.comboBox_shot_shotname.addItems(shot_list)

        
    
    def set_main_laoder(self):
    
        self.ui.label_projectname.setText(f"{self.project}")
        self.ui.label_username.setText(f"{self.user}")
        
    def set_up(self):
        from main_window_ui import Ui_Form
        # ui_file_path = "/home/rapa/yummy/pipeline/scripts/loader/main_window.ui"
        # ui_file = QFile(ui_file_path)
        # ui_file.open(QFile.ReadOnly)
        # loader = QUiLoader()
        # self.ui = loader.load(ui_file,self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

info = {"project" : "YUMMY" , "name" : "su"}

if __name__ == "__main__":
    app = QApplication()
    my  = Mainloader(info)
    my.show()
    app.exec()