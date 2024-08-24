from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QApplication
import os,sys
sys.path.append("/home/rapa/yummy")
from pipeline.scripts.loader.loader_ui.main_window_v002_ui import Ui_Form
from pipeline.scripts.loader.loader_script.main import Mainloader
from pipeline.scripts.loader.loader_script.my_task import My_task
from pipeline.scripts.loader.loader_module.project_data import project_data
from pipeline.scripts.loader.loader_script.pub import Loader_pub


class Merge(QWidget,My_task,Mainloader,project_data,Loader_pub):
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
        
    
    def tab_enable(self,info):
        if not info["rank"] == "Admin":
            self.ui.tabWidget_all.removeTab(3)
    
    def set_up(self,info):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.set_main_loader(info)
        info = project_data.__init__(self,info,self.ui)
        Mainloader.__init__(self,info,self.ui)
        My_task.__init__(self,info,self.ui)
        Loader_pub.__init__(self,info,self.ui)
         
if __name__ == "__main__":
    app  = QApplication()
    my = Merge()
    my.show()
    app.exec()