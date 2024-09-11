from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication,QPalette,QColor, QResizeEvent
from PySide6.QtWidgets import QMainWindow,QApplication, QSizePolicy
from PySide6.QtCore import Qt, QSize,Signal,QObject,QThread

import sys
sys.path.append("/home/rapa/yummy/pipeline/scripts/loader")
from loader_ui.main_window_v005_ui import Ui_MainWindow
from loader_script.loader_shot import Mainloader
from loader_script.loader_my_task_v002 import My_task
from loader_script.loader_clip_v002 import Libraryclip
from loader_script.loader_asset import Libraryasset
from loader_module.project_data import project_data
from loader_script.loader_pub import Loader_pub
from loader_script.status_monitor import ChangeHandler
from loader_script.webhook_app import WebhookServer

import json
import subprocess
from monitor_daemon import MonitorDaemon
# from monitor_daemon import MonitorDaemon
# class Merge(QWidget,Mainloader,project_data,Loader_pub):

class Thread_monitor(QObject):
    
    finished = Signal()
    finished_first = Signal(dict)
    
    def __init__(self):
        super().__init__()
    
    def open_monitor(self):
        event_handler = ChangeHandler()
        self.finished.emit()
        
    def open_webhook(self):
        server = WebhookServer()
        self.finished.emit()
        
    def open_demon(self):
        monitor_daemon_script = "/home/rapa/yummy/pipeline/scripts/portpolio/loader/monitor_daemon.py"
        log_file = "/home/rapa/yummy/pipeline/scripts/loader/monitor_log.txt"
        self.demon_monitor = MonitorDaemon(monitor_daemon_script, log_file)
        self.demon_monitor.start_monitoring()
        self.finished.emit()
        
class Merge(QMainWindow,Libraryclip,project_data,My_task,Loader_pub,Mainloader,Libraryasset):
    def __init__(self,info):
        super().__init__()
        self.set_up()
        self.setPalette(self.get_darkModePalette())
        self.tab_enable(info)
        self.set_main_loader(info)

        
        info = project_data.__init__(self,info)
        self.write_project_json(info)
        
        self.connect_script() 
        
        # monitor_daemon_script = "/home/rapa/yummy/pipeline/scripts/portpolio/loader/monitor_daemon.py"
        # log_file = "/home/rapa/yummy/pipeline/scripts/loader/monitor_log.txt"
        # self.demon_monitor = MonitorDaemon(monitor_daemon_script, log_file)
        # self.demon_monitor.start_monitoring()
        
        self.ui.pushButton_reset.clicked.connect(self.reset_ui)
        # server = WebhookServer()
        # self.open_status_monitor_thread()
        # if server:
        #     event_handler = ChangeHandler()
        self.open_webhook_monitor_thread()
        self.open_status_monitor_thread()
        self.open_demon_monitor_thread()

    def open_status_monitor_thread(self):

        self.status_monitor = Thread_monitor()
        self.thread_monitor = QThread()
        self.status_monitor.moveToThread(self.thread_monitor)
        self.thread_monitor.started.connect(self.status_monitor.open_monitor)
        self.status_monitor.finished.connect(self.finish_status_monitor_thread)
        self.status_monitor.finished.connect(self.thread_monitor.quit)
        self.status_monitor.finished.connect(self.status_monitor.deleteLater)
        self.thread_monitor.finished.connect(self.thread_monitor.deleteLater)
        self.thread_monitor.start()
        
    def finish_status_monitor_thread(self):
        print("스테이터스 모니터 연결 ^^")
        
    def open_webhook_monitor_thread(self):

        self.webhook_monitor = Thread_monitor()
        self.webhook_thread_monitor = QThread()
        self.webhook_monitor.moveToThread(self.webhook_thread_monitor)
        self.webhook_thread_monitor.started.connect(self.webhook_monitor.open_webhook)
        self.webhook_monitor.finished.connect(self.finish_webhook_monitor_thread)
        self.webhook_monitor.finished.connect(self.webhook_thread_monitor.quit)
        self.webhook_monitor.finished.connect(self.webhook_monitor.deleteLater)
        self.webhook_thread_monitor.finished.connect(self.webhook_thread_monitor.deleteLater)
        self.webhook_thread_monitor.start()
        
    def finish_webhook_monitor_thread(self):
        print("웹훅 모니터 연결 ^^")
        
        
    def open_demon_monitor_thread(self):

        self.demon_monitor = Thread_monitor()
        self.demon_thread_monitor = QThread()
        self.demon_monitor.moveToThread(self.demon_thread_monitor)
        self.demon_thread_monitor.started.connect(self.demon_monitor.open_demon)
        self.demon_monitor.finished.connect(self.finish_demon_monitor_thread)
        self.demon_monitor.finished.connect(self.demon_thread_monitor.quit)
        self.demon_monitor.finished.connect(self.demon_monitor.deleteLater)
        self.demon_thread_monitor.finished.connect(self.demon_thread_monitor.deleteLater)
        self.demon_thread_monitor.start()
        
    def finish_demon_monitor_thread(self):
        print("웹훅 모니터 연결 ^^")
    
    def set_main_loader(self,info):
        
        project   = info["project"]
        user      = info["name"]
        rank      = info["rank"]
        
        self.ui.label_projectname.setText(f"{project}")
        self.ui.label_username.setText(f"{user}")
        self.ui.label_rank.setText(f"{rank}")
    
    def write_project_json(self,info):
        with open("/home/rapa/yummy/pipeline/json/project_data.json", "w") as w:
            json.dump(info,w,indent = "\n")
            
    
    def tab_enable(self,info):
        if not info["rank"] == "Admin":
            self.ui.tabWidget_all.removeTab(3)

    def reset_ui(self):
        print("0000000000")
        login_path = "python3.9 /home/rapa/yummy/pipeline/scripts/loader/loader_script/singin.py"
        subprocess.Popen(login_path, shell=True,executable="/bin/bash")

        sys.exit()


    def center_window(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry() 
        screen_center = screen_geometry.center() 
        window_geometry = self.frameGeometry()  
        window_geometry.moveCenter(screen_center)  
        adjusted_position = window_geometry.topLeft()
        self.move(adjusted_position)

        user = info["name"]
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowTitle(f"{user} Loader")

    def resizeEvent(self, event):
        new_size = event.size()
        old_size = event.oldSize()
        
        self.shot.resize_shot_status(new_size)
        # self.shot.resize_tab(new_size)
        # self.shot.set_status_table_1(new_size)
        
        self.my_task.resize_my_task_status(new_size)
        self.my_task.resize_mytask_table(new_size)
        self.my_task.resize_mytask_object(new_size)

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
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.center_window()

    def connect_script(self):
        self.my_task = My_task(self.ui)
        self.shot = Mainloader(self.ui)
        self.lib_clip = Libraryclip(self.ui)
        self.lib_asset = Libraryasset(self.ui)
        self.pub = Loader_pub(self.ui)

info = {
"project": "YUMMIE",
"project_id": 222,
"name": "Wooin JUNG",
"user_id": 155,
"rank": "Admin",
"resolution_width": "1920",
"resolution_height": "1080",
"resolution": "1920 X 1080"
}

if __name__ == "__main__":
    app  = QApplication()
    my = Merge(info)
    my.show()
    app.exec()
    
    
    
    
    