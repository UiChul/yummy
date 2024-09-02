from PySide6.QtCore import Qt,Signal,QSize
from PySide6.QtCore import QObject,QThread,QTimer
from PySide6.QtWidgets import QWidget,QApplication,QMessageBox
from PySide6.QtGui import QMovie,QGuiApplication
from PySide6.QtGui import QPalette,QColor
from shotgun_api3 import shotgun
import json
import sys

sys.path.append("/home/rapa/yummy/pipeline/scripts/loader")

from loader_ui.singin_window_ui import Ui_Form
from loader_script.get_datas_for_login import Signinfo
from loader_script.get_datas_for_user import OpenLoaderData

class Sg_json(QObject):
    
    finished = Signal()
    finished_first = Signal(dict)
    
    def __init__(self, project = ""):
        super().__init__()
        self.project = project
    
    def open_loader(self):
        if self.project == "-":
            self.finished.emit()
            return  
        OpenLoaderData(self.project)
        self.finished.emit()
    
    def open_sg(self):
        flow = Shotgrid_connect(self.project)
        flow.connect_sg()
        user= flow.get_user_by_email()
        self.finished_first.emit(user)
    
    def open_project_login(self):
        Signinfo(self.project)
        self.finished.emit()

class Shotgrid_connect:
    
    def __init__(self,user_email):
        
        self.user_email = user_email
        # self.connect_sg()
        # self.get_user_by_email()
        
    def connect_sg(self):
        URL = "https://4thacademy.shotgrid.autodesk.com"
        SCRIPT_NAME = "test_hyo"
        API_KEY = "ljbgffxqg@cejveci5dQebhdx"
        """
        샷그리드 연결
        """
        self.sg = shotgun.Shotgun(URL, SCRIPT_NAME, API_KEY)

        # return sg

    def get_user_by_email(self):
        """
        입력된 이메일 정보로 유저 정보 가져오기
        """
        filters = [["email", "is", self.user_email]]
        fields = ["id", "name", "email", "permission_rule_set"]
        users = self.sg.find("HumanUser", filters=filters, fields=fields)
        if users:
            return users[0]
        else:
            return users

class Signin(QWidget):
    
    def __init__(self):
        super().__init__()
        self.set_up()
        self.put_loader_gif()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.email_vaildate = 0
        self.ui.lineEdit_email.returnPressed.connect(self.check_login)
        
    def put_loader_gif(self):
        self.gif_index = 0  # 현재 재생 중인 GIF 인덱스
        self.gif_paths = [  # 변경할 GIF 경로 목록
            "/home/rapa/xgen/run001.gif",
            "/home/rapa/xgen/run002.gif",
            "/home/rapa/xgen/run003.gif",
            "/home/rapa/xgen/run004.gif"
        ]
    
    def set_first_login_gif(self):
        gif_movie = QMovie("/home/rapa/xgen/run003.gif")
        gif_movie.setScaledSize(QSize(150,150))
        self.ui.label_qmovie.setMovie(gif_movie)
        gif_movie.start()
        self.ui.label_qmovie.setAlignment(Qt.AlignCenter)   
        
    def input_project(self):
        with open("/home/rapa/yummy/pipeline/json/login_user_data.json","rt",encoding="utf-8") as r:
            user_dic = json.load(r)
        project_name = ["-"]
        for pro in user_dic["projects"]:
            project_name.append(pro["name"])
        self.user_name = user_dic["name"]
        self.rank = user_dic["permission_group"]
        self.ui.comboBox_project_name.addItems(project_name)
        
    def set_messagebox(self, text, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec()
        
    def connect_shotgrid_thread(self):
        # self.set_login_buffering_img()
        self.set_first_login_gif()
        self.ui.stackedWidget.setCurrentIndex(1) 
        user_email = self.ui.lineEdit_email.text()
        
        self.worker = Sg_json(user_email)
        self.thread_json = QThread()
        self.worker.moveToThread(self.thread_json)
        self.thread_json.started.connect(self.worker.open_sg)
        
        self.worker.finished_first.connect(self.thread_json.quit)
        self.worker.finished_first.connect(self.worker.deleteLater)
        self.thread_json.finished.connect(self.thread_json.deleteLater)
        
        self.worker.finished_first.connect(self.connect_shotgird_finished)
        self.thread_json.start()
     
    def connect_shotgird_finished(self,user):
        if not user:
            gif_movie = QMovie("/home/rapa/xgen/slip001.gif")
            gif_movie.setScaledSize(QSize(150,150))
            self.ui.label_qmovie.setMovie(gif_movie)
            gif_movie.start()
            self.ui.label_qmovie.setAlignment(Qt.AlignCenter)    
            self.set_messagebox("email 정보가 정확하지 않습니다","로그인 실패")
            self.ui.stackedWidget.setCurrentIndex(0) 
        else:
            self.make_user_thread()
    
    def make_user_thread(self):
        self.set_first_login_gif()
        self.ui.stackedWidget.setCurrentIndex(1) 
        user_email = self.ui.lineEdit_email.text()
        self.worker = Sg_json(user_email)
        self.thread_json = QThread()
        self.worker.moveToThread(self.thread_json)
        self.thread_json.started.connect(self.worker.open_project_login)
        self.worker.finished.connect(self.make_user_finished)
        self.worker.finished.connect(self.thread_json.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread_json.finished.connect(self.thread_json.deleteLater)
        self.thread_json.start()
        
    def make_user_finished(self):
        self.set_messagebox("프로젝트를 선택해주세요.","이메일 인증 성공")
        self.input_project()
        
        self.ui.lineEdit_email.setEnabled(False)
        self.ui.label.setEnabled(False)
        
        
        self.ui.comboBox_project_name.setVisible(True)
        self.ui.label_2.setVisible(True)
        self.ui.stackedWidget.setCurrentIndex(0)  
                
        self.email_vaildate += 1
        
    def check_login(self):
        
        user_email = self.ui.lineEdit_email.text()
        
        if not user_email:
            self.set_messagebox("email을 입력해주세요" , "로그인 실패")
            return
        
        self.connect_shotgrid_thread()
        
    def keyPressEvent(self, event):
        if self.email_vaildate == 1:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:    
                # if not self.thread_json.isRunning():      
                self.open_loader()
                self.email_vaildate +=1                        
        else:
            print("no vaildate")
    
    def open_loader(self):
        self.set_login_buffering_img()
        self.ui.stackedWidget.setCurrentIndex(1)  
        project = self.ui.comboBox_project_name.currentText()
        if project == "-":
            self.email_vaildate -= 1
            
        
        self.worker = Sg_json(project)
        self.thread_json = QThread()
        self.worker.moveToThread(self.thread_json)
        self.thread_json.started.connect(self.worker.open_loader)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.finished.connect(self.thread_json.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread_json.finished.connect(self.thread_json.deleteLater)
        self.thread_json.start()
         
    def on_worker_finished(self):
        self.connect_loader()
        
    def set_login_buffering_img(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gif)
        self.timer.start(2200)  # 2초(2000밀리초)마다 실행
        # 첫 번째 GIF 설정
        self.update_gif()
        
    def update_gif(self):
        # self.ui.stackedWidget.setCurrentIndex(1)
        gif_path = self.gif_paths[self.gif_index]
        gif_movie = QMovie(gif_path)
        gif_movie.setScaledSize(QSize(150,150))
        self.ui.label_qmovie.setMovie(gif_movie)
        gif_movie.start()
        self.ui.label_qmovie.setAlignment(Qt.AlignCenter)
        
        self.gif_index = (self.gif_index + 1) % len(self.gif_paths)
           
    def find_project_info(self,project):
        with open("/home/rapa/yummy/pipeline/json/login_user_data.json","rt",encoding="utf-8") as r:
            user_dic = json.load(r)
            
            user_id = user_dic["user_id"]
            project_id = ""
            resolution_width  =  ""
            resolution_height =  ""

            
            for project_info in user_dic["projects"]:
                if project == project_info["name"]:
                    project_id = project_info["id"]
                    resolution_width = project_info["resolution_width"]
                    resolution_height = project_info["resolution_height"]
                    
        return project_id,user_id,resolution_width,resolution_height
    
    def connect_loader(self):
        project = self.ui.comboBox_project_name.currentText()
        
        if project == "-":
            return
        project_id,user_id,resolution_width,resolution_height = self.find_project_info(project)
        
        info = {"project" : project , "project_id" : project_id , "name" : self.user_name, "user_id" : user_id, "rank": self.rank, "resolution_width" : resolution_width, "resolution_height":resolution_height}
        from loader_script.loader_merge import Merge
        self.load = Merge(info)
        self.load.show()       
        self.close()     

    def center_window(self):
        # 화면의 중심 좌표를 얻음
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()  # 화면의 전체 지오메트리 얻기
        screen_center = screen_geometry.center()  # 화면의 중심점 얻기
        # 현재 창의 크기 및 중심 좌표 계산
        window_geometry = self.frameGeometry()  # 현재 창의 프레임 지오메트리 얻기
        window_geometry.moveCenter(screen_center)  # 창의 중심을 화면의 중심으로 이동
        # 최종적으로 계산된 좌표로 창 이동
        offset_y = 200  # 화면 중심보다 50 픽셀 위로 이동
        adjusted_position = window_geometry.topLeft()
        adjusted_position.setY(adjusted_position.y() - offset_y)  # Y 좌표를 조정하여 위로 이동

        # 최종적으로 계산된 좌표로 창 이동
        self.move(adjusted_position)

    def get_darkModePalette(self) :
        darkPalette = self.palette()
        darkPalette.setColor( QPalette.Window, QColor( 53, 53, 53 ) )
        darkPalette.setColor( QPalette.WindowText, QColor(211, 215, 207))
        darkPalette.setColor( QPalette.Disabled, QPalette.WindowText, QColor( 127, 127, 127 ) )
        darkPalette.setColor( QPalette.Base, QColor( 42, 42, 42 ) )
        darkPalette.setColor( QPalette.AlternateBase, QColor( 66, 66, 66 ) )
        darkPalette.setColor( QPalette.ToolTipBase, QColor( 53, 53, 53 ) )
        darkPalette.setColor( QPalette.ToolTipText, QColor(211, 215, 207) )
        darkPalette.setColor( QPalette.Text, QColor(211, 215, 207) )
        darkPalette.setColor( QPalette.Disabled, QPalette.Text, QColor( 127, 127, 127 ) )
        darkPalette.setColor( QPalette.Dark, QColor( 35, 35, 35 ) )
        darkPalette.setColor( QPalette.Shadow, QColor( 20, 20, 20 ) )
        darkPalette.setColor( QPalette.Button, QColor( 53, 53, 53 ) )
        darkPalette.setColor( QPalette.ButtonText, QColor(211, 215, 207) )
        darkPalette.setColor( QPalette.Disabled, QPalette.ButtonText, QColor( 127, 127, 127 ) )
        darkPalette.setColor( QPalette.BrightText, Qt.red )
        darkPalette.setColor( QPalette.Link, QColor( 42, 130, 218 ) )
        darkPalette.setColor( QPalette.Highlight, QColor( 42, 130, 218 ) )
        darkPalette.setColor( QPalette.Disabled, QPalette.Highlight, QColor( 80, 80, 80 ) )
        darkPalette.setColor( QPalette.HighlightedText, QColor(211, 215, 207) )
        darkPalette.setColor( QPalette.Disabled, QPalette.HighlightedText, QColor( 127, 127, 127 ), )
        return darkPalette

    def set_up(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.center_window()
        self.ui.comboBox_project_name.setVisible(False)
        self.ui.label_2.setVisible(False)
        self.setPalette(self.get_darkModePalette())

if __name__ == "__main__":
    app = QApplication()
    sign = Signin()
    sign.show()
    app.exec()