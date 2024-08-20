from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QApplication

from main_window_v002_ui import Ui_Form
from main import Mainloader
from my_task import My_task

class Merge(QWidget,My_task,Mainloader):
    def __init__(self,info):
        super().__init__()
        self.info = info
        self.set_up()
        
    def set_up(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # info = {"project" : "Marvelous" , "name" : "su","rank":"Artist"}
        # Mainloader(info,self.ui)
        Mainloader.__init__(self,self.info,self.ui)
        My_task.__init__(self,self.ui)
        
if __name__ == "__main__":
    app  = QApplication()
    my = Merge()
    my.show()
    app.exec()