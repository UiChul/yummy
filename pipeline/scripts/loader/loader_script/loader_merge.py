from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget,QApplication,QSizePolicy
from PySide6.QtCore import Qt, QSize

import os,sys
sys.path.append("/home/rapa/yummy/pipeline/scripts/loader")
from loader_ui.main_window_v002_ui import Ui_Form
from loader_script.loader_shot import Mainloader
from loader_script.loader_my_task import My_task
from loader_script.loader_clip_v002 import Libraryclip
from loader_script.loader_asset import Libraryasset
from loader_module.project_data import project_data
from loader_script.loader_pub import Loader_pub
import json

# class Merge(QWidget,Mainloader,project_data,Loader_pub):
class Merge(QWidget,Libraryclip,project_data,My_task,Loader_pub,Mainloader,Libraryasset):
    def __init__(self,info):
        super().__init__()
        self.set_up(info)
        self.tab_enable(info)
        
    def set_main_loader(self,info):
        
        project = info["project"]
        user    = info["name"]
        rank    = info["rank"]
        
        self.ui.label_projectname.setText(f"{project}")
        self.ui.label_username.setText(f"{user}")
        self.ui.label_rank.setText(f"{rank}")
    
    def write_project_json(self,info):
        with open("/home/rapa/yummy/pipeline/json/project_data.json", "w") as w:
            json.dump(info,w,indent = "\n")
    
    def tab_enable(self,info):
        if not info["rank"] == "Admin":
            self.ui.tabWidget_all.removeTab(3)
            
    def center_window(self):
        # 화면의 중심 좌표를 얻음
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()  # 화면의 전체 지오메트리 얻기
        screen_center = screen_geometry.center()  # 화면의 중심점 얻기
        # 현재 창의 크기 및 중심 좌표 계산
        window_geometry = self.frameGeometry()  # 현재 창의 프레임 지오메트리 얻기
        window_geometry.moveCenter(screen_center)  # 창의 중심을 화면의 중심으로 이동
        # 최종적으로 계산된 좌표로 창 이동 
        adjusted_position = window_geometry.topLeft()
        # 최종적으로 계산된 좌표로 창 이동
        self.move(adjusted_position)
    
    def set_up(self,info):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.center_window()
        self.set_main_loader(info)
        info = project_data.__init__(self,info,self.ui)
        self.write_project_json(info)
        Libraryclip.__init__(self,self.ui)
        Libraryasset.__init__(self,self.ui)
        My_task.__init__(self,self.ui)
        Loader_pub.__init__(self,self.ui)
        Mainloader.__init__(self,self.ui)

info = {"project": "YUMMIE",

"name": "UICHUL SHIN",

"rank": "Admin"} 
if __name__ == "__main__":
    app  = QApplication()
    my = Merge(info)
    my.show()
    app.exec()