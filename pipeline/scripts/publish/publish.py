try:
    from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem
    from PySide6.QtWidgets import QLabel, QLineEdit, QRadioButton, QSpacerItem, QSizePolicy
    from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile
    from PySide6.QtGui import  Qt

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem
    from PySide2.QtWidgets import QLabel, QLineEdit, QRadioButton, QSpacerItem, QSizePolicy
    from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile
    from PySide2.QtGui import  Qt

import os
import functools
import nuke

class Publish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "/home/rapa/YUMMY_project/PUBLISH.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        
        self.ui.pushButton_render.clicked.connect(self.submit_render)

        self.table.setStyleSheet("selection-background-color: rgb(120,90,57)")

        self.get_info()

if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()