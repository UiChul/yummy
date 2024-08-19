from PySide6.QtCore import Qt,Signal
from PySide6.QtWidgets import QWidget,QApplication,QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os

class Signin(QWidget):
    
    def __init__(self):
        super().__init__()
        self.set_up()
        self.input_project()
        self.ui.lineEdit_email.returnPressed.connect(self.check_login)
    
    def input_project(self):
        project_name = ["YUMMY", "Marvelous"]
        self.ui.comboBox_project_name.addItems(project_name)
        
    def check_login(self):
        
        self.user_name = ""
        
        # 나중에 json으로 대체
        user_example = {1 : {"name" : "Uichul" , "email" : "suc@" , "job" :  "artist"}, 
                        2 : {"name" : "Jiyeon" , "email" : "ji@"  , "job" :  "artist"}, 
                        3 : {"name" : "Wooin"  , "email" : "woo@" , "job" :  "artist"},
                        4 : {"name" : "Hyogi"  , "email" : "hyo@" , "job" :  "artist"},
                        5 : {"name" : "Suyeon" , "email" : "su@"  , "job" :  "artist"}}
        
        
        user_email = self.ui.lineEdit_email.text()
        
        if not user_email:
            self.set_messagebox("email을 입력해주세요" , "로그인 실패")
            return
        
        for info in user_example.values():
            if info["email"] == user_email:
                self.user_name = info["name"]
                self.set_messagebox(f"{self.user_name}님 로그인 되었습니다.","로그인 성공")
                project = self.ui.comboBox_project_name.currentText()
                info["project"] = project
                self.close()
                from main import Mainloader
                self.main = Mainloader(info)
                self.main.show()
                
        if not self.user_name:
            self.set_messagebox("email 정보가 정확하지 않습니다","로그인 실패")
            return
          
    def set_messagebox(self, text, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec()
    
    def set_up(self):
        from singin_window_ui import Ui_Form
        # ui_file_path = "singin_window.ui"
        # ui_file = QFile(ui_file_path)
        # ui_file.open(QFile.ReadOnly)
        # loader = QUiLoader()
        # self.ui = loader.load(ui_file,self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
    
if __name__ == "__main__":
    app = QApplication()
    sign = Signin()
    sign.show()
    app.exec()