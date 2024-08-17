from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QApplication,QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class Mainloader(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up()
        
    def set_up(self):
        ui_file_path = "/home/rapa/yummy/pipeline/scripts/loader/main_window.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file,self)

if __name__ == "__main__":
    app = QApplication()
    my  = Mainloader()
    my.show()
    app.exec()