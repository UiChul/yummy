try:
    from PySide6.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile
    from PySide6.QtGui import  Qt

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTreeWidgetItem
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile
    from PySide2.QtGui import  Qt

import os
import functools

class Publish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "/home/rapa/yummy/pipeline/scripts/publish/publish.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.tree = self.ui.treeWidget_shot_file_struc

        # self.ui.pushButton_publish.clicked.connect(self.)

        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["yummy"])

        self.set_the_structure()
        
    def set_the_structure(self):
        start_dic = "/home/rapa/yummy"

        for dir in os.listdir(start_dic):
            parent_path = os.path.join(start_dic, dir)
            if os.path.isdir(parent_path):
                parent_dir = QTreeWidgetItem(self.tree)
                parent_dir.setText(0, dir)
                self.m_childs(parent_dir, parent_path)

    def m_childs(self, parent_dir, parent_path):
        for dir in os.listdir(parent_path):
            child_path = os.path.join(parent_path, dir)
            if os.path.isdir(child_path):
                child_dir = QTreeWidgetItem(parent_dir)
                child_dir.setText(0, os.path.basename(child_path))
                self.m_childs(child_dir, child_path)






if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()