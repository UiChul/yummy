try:
    from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem, QListWidgetItem, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile
    from PySide6.QtGui import  Qt, QPixmap

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem, QListWidgetItem, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile
    from PySide2.QtGui import  Qt, QPixmap

import os
import re
# import nuke
import ffmpeg
import shutil
# import functools

class Publish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "C:/Users/LEE JIYEON/yummy/pipeline/scripts/publish/publish_ver4.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint) # UI 최상단 고정
        ui_file.close()

        
        file_tuple = QFileDialog.getOpenFileName(self, "import file", "C:/Users/LEE JIYEON/Desktop/YUMMY/project/Marvelous/seq/OPN/OPN_0010/cmp/dev/work", "nk File(*.nknc)")
        # file_tuple = QFileDialog.getOpenFileName(self, "import json file","/home/rapa/show/insideout2/seq/OPN/OPN_0100/comp/plate") 
        self.seq_path = file_tuple[0]
        QFileDialog.getExistingDirectory


    
if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()