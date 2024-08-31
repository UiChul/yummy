# import subprocess

# subprocess.Popen(["/bin/bash", "-i", "-c", "nuke"])


import sys
sys.path.append("/home/rapa/yummy/pipeline/scripts/loader")
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QSizePolicy
from loader_ui.test_ui import Ui_Form

class Sizetest(QWidget):
    def __init__(self):
        super().__init__()
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.set_up()
        
        self.table.setRowCount(3)
        self.table.setColumnCount(3)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def set_up(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.table = self.ui.tableWidget

if __name__ == "__main__":
    app = QApplication()
    my = Sizetest()
    my.show()
    app.exec()