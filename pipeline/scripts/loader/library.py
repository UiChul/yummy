from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QApplication,QHeaderView
from PySide6.QtWidgets import QTreeWidgetItem, QTableWidgetItem, QLabel
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap
import os

# from functools import partial

class LibraryLoader(QWidget):
    def __init__(self,info):
        super().__init__()
        self.set_up()
        
        self.project = info["project"]
        self.user = info["name"]
        

        # self.asset_tree = self.ui.treeWidget_asset_file_path
        
        self.set_user_information()
        self.set_asset_treeWidget()

        # comboBox 일단 비활성화 해놓음
        self.ui.comboBox_seq.setEnabled(False)
        
        #Signal

    def set_asset_treeWidget(self):
        self.asset_tree.clear()
        file_path = f"/home/rapa/YUMMY/project/{self.project}/asset"
        asset_list = os.listdir(file_path)
    
        # Headerlabel setting
        self.asset_tree.setHeaderLabels([" Asset"])

        # shot code setting
        for asset_item in asset_list:
            parent_item = QTreeWidgetItem(self.asset_tree)
            parent_item.setText(0, asset_item)

        # task setting
            self.task_path = f"/home/rapa/YUMMY/project/{self.project}/asset/{asset_item}"
            tasks = os.listdir(self.task_path)

            for task in tasks :
                task_item = QTreeWidgetItem(parent_item)
                task_item.setText(0,task)

    # def set_asset_type
    













    def set_user_information(self):
    
        self.ui.label_projectname.setText(f"{self.project}")
        self.ui.label_username.setText(f"{self.user}")
        
    def set_up(self):
        from main_window_v002_ui import Ui_Form
        # ui_file_path = "/home/rapa/yummy/pipeline/scripts/loader/main_window.ui"
        # ui_file = QFile(ui_file_path)
        # ui_file.open(QFile.ReadOnly)
        # loader = QUiLoader()
        # self.ui = loader.load(ui_file,self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    

info = {"project" : "Marvelous" , "name" : "su"}

if __name__ == "__main__":
    app = QApplication()
    my  = LibraryLoader(info)
    my.show()
    app.exec()