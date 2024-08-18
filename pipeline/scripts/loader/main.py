from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QApplication,QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class Mainloader(QWidget):
    def __init__(self,info):
        super().__init__()
        self.set_up()
        self.info = info
        self.set_main_laoder()
        
    def set_main_laoder(self):
        self.ui.label_projectname.setText(f"{self.info["project"]}")
        self.ui.label_username.setText(f"{self.info["name"]}")
        
    def set_up(self):
        from main_window_ui import Ui_Form
        # ui_file_path = "/home/rapa/yummy/pipeline/scripts/loader/main_window.ui"
        # ui_file = QFile(ui_file_path)
        # ui_file.open(QFile.ReadOnly)
        # loader = QUiLoader()
        # self.ui = loader.load(ui_file,self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication()
    my  = Mainloader(info=3)
    my.show()
    app.exec()