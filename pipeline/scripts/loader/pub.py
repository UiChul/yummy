from PySide6.QtWidgets import QWidget,QApplication
from main_window_v002_ui import Ui_Form

class Loader_Pub(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up()
        
    def set_up(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
    
app = QApplication()
my = Loader_Pub()
my.show()
app.exec()