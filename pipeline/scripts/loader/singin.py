from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QApplication,QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class Signin(QWidget):
    
    def __init__(self):
        super().__init__()
        self.set_up()
        self.input_project()
        self.user_example = {"Uichul" : ["suc708@naver.com" , "artist"]}
        self.ui.lineEdit.returnPressed.connect(self.check_login)
    
    # 
    def input_project(self):
        project_name = ["yummy", "baked", "Marvelous", "Moomins", "phoenix"]
        self.ui.comboBox.addItems(project_name)
        
    def check_login(self):
        
        user_name = ""
        
        user_example = {1 : {"name" : "Uichul" , "email" : "suc@" , "job" : "artist"}, 
                        2 : {"name" : "Jiyeon" , "email" : "ji@"  , "job" :  "artist"}, 
                        3 : {"name" : "Wooin"  , "email" : "woo@" , "job" :  "artist"},
                        4 : {"name" : "Hyogi"  , "email" : "hyo@" , "job" :  "artist"},
                        5 : {"name" : "Suyeon" , "email" : "su@"  , "job" :  "artist"}}
        
        user_email = self.ui.lineEdit.text()
        
        if not user_email:
            self.set_messagebox("email을 입력해주세요" , "로그인 실패")
            return
        
        for info in user_example.values():
            if info["email"] == user_email:
                user_name = info["name"]
                self.set_messagebox(f"{user_name}님 로그인 되었습니다.","로그인 성공")
        
        if not user_name:
            self.set_messagebox("email 정보가 정확하지 않습니다","로그인 실패")
            
    def set_messagebox(self, text, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec()
    
    def set_up(self):
        ui_file_path = "/home/rapa/yummy/pipeline/scripts/loader/singin_window.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file,self)
        
        
app = QApplication()
my = Signin()
my.show()
app.exec()