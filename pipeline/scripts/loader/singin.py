from PySide6.QtCore import Qt,Signal
from PySide6.QtWidgets import QWidget,QApplication,QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from shotgun_api3 import shotgun
import os
import json

# apen1112@gmail.com
# MOTIONDESIGN310@GMAIL.COM
# stellalee969@gmail.com

class Signin(QWidget):
    
    def __init__(self):
        super().__init__()
        self.set_up()
        self.ui.lineEdit_email.returnPressed.connect(self.check_login)
        self.ui.pushButton.clicked.connect(self.connect_loader)
        
    def input_project(self):
        with open("/home/rapa/yummy/pipeline/json/login_user_data.json","rt",encoding="utf-8") as r:
            user_dic = json.load(r)
        project_name = ["-"]
        for pro in user_dic["projects"]:
            project_name.append(pro["name"])
        self.user_name = user_dic["name"]
        self.ui.comboBox_project_name.addItems(project_name)
        
    def set_messagebox(self, text, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec()
        
    def check_login(self):
        
        user_email = self.ui.lineEdit_email.text()

        if not user_email:
            self.set_messagebox("email을 입력해주세요" , "로그인 실패")
            return
        
        sg = self.connect_sg()
        user= self.get_user_by_email(sg, user_email)

        if not user:
            self.set_messagebox("email 정보가 정확하지 않습니다","로그인 실패")
            return
        else:
            from get_datas_for_login import Signinfo
            Signinfo(user_email)    
            self.set_messagebox("프로젝트를 선택해주세요.","이메일 인증 성공")
            self.input_project()
            self.ui.comboBox_project_name.setVisible(True)
            self.ui.label_2.setVisible(True)
            self.ui.pushButton.setVisible(True)
            
    def connect_loader(self):
        project = self.ui.comboBox_project_name.currentText()
        info = {"project" : project , "name" : self.user_name }
        from main import Mainloader
        self.load = Mainloader(info)
        self.load.show()            
        
    #=====================================================================================
        
    def connect_sg(self):
        URL = "https://4thacademy.shotgrid.autodesk.com"
        SCRIPT_NAME = "test_hyo"
        API_KEY = "ljbgffxqg@cejveci5dQebhdx"
        """
        샷그리드 연결
        """
        sg = shotgun.Shotgun(URL, SCRIPT_NAME, API_KEY)

        return sg

    def get_user_by_email(self,sg, email):
        """
        입력된 이메일 정보로 유저 정보 가져오기
        """
        filters = [["email", "is", email]]
        fields = ["id", "name", "email", "permission_rule_set"]
        users = sg.find("HumanUser", filters=filters, fields=fields)
        if users:
            return users[0]
        else:
            return users
    
    def set_up(self):
        from singin_window_ui import Ui_Form
        # ui_file_path = "singin_window.ui"
        # ui_file = QFile(ui_file_path)
        # ui_file.open(QFile.ReadOnly)
        # loader = QUiLoader()
        # self.ui = loader.load(ui_file,self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.comboBox_project_name.setVisible(False)
        self.ui.label_2.setVisible(False)
        self.ui.pushButton.setVisible(False)
        
        
    
if __name__ == "__main__":
    app = QApplication()
    sign = Signin()
    sign.show()
    app.exec()