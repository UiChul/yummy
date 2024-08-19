try:
    from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile
    from PySide6.QtGui import  Qt

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile
    from PySide2.QtGui import  Qt

import os
import nuke

class Publish(QWidget):

    def __init__(self):
            super().__init__()         

            ui_file_path = "/home/rapa/yummy/pipeline/scripts/publish/publish_ver2.ui"
            ui_file = QFile(ui_file_path)
            ui_file.open(QFile.ReadOnly)
            loader = QUiLoader()                                      
            self.ui = loader.load(ui_file, self)
            ui_file.close()

            self.test()

    def test(self):
        print("blahdh")

if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()