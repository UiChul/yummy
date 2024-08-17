try:
    from PySide6.QtWidgets import QApplication, QWidget
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile
    from PySide6.QtGui import  Qt

except:
    from PySide2.QtWidgets import QApplication, QWidget
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile
    from PySide2.QtGui import  Qt

import os
import nuke

class Publish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "/home/rapa/yummy/pipeline/scripts/publish/publish.ver2.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.set_nk_file_list()
        
    def set_nk_file_list(self):

        current_file_path = nuke.root().name()    #현재 nuke파일이 있는 절대경로
        nk_file_name = os.path.basename(current_file_path)    #파일이름 추출
        self.ui.listWidget_nk.addItem(nk_file_name)
        

    # def set_exr_file_list(self):

        # current_file_path = nuke.root().name()    #현재 nuke파일이 있는 경로+파일이름
        # print(current_file_path)

        # file_name = os.path.basename(current_file_path)

    # def set_mov_file_list(self):

        # current_file_path = nuke.root().name()    #현재 nuke파일이 있는 경로+파일이름
        # print(current_file_path)

        # file_name = os.path.basename(current_file_path)



if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()