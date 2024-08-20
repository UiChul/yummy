from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QApplication

from main_window_v002_ui import Ui_Form
from main import Mainloader
from my_task import My_task

class Merge(QWidget,My_task,Mainloader):
    def __init__(self,info):
        super().__init__()
        self.set_up(info)
        self.tab_enable(info)
        
    
    def tab_enable(self,info):
        if not info["rank"] == "Yummy_manager":
            self.ui.tabWidget_all.removeTab(3)
    
    def set_up(self,info):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        Mainloader.__init__(self,info,self.ui)
        My_task.__init__(self,self.ui)
        
        
if __name__ == "__main__":
    app  = QApplication()
    my = Merge()
    my.show()
    app.exec()