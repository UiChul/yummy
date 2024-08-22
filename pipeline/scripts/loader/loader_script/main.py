from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QApplication,QMessageBox
from PySide6.QtWidgets import QTreeWidgetItem, QTableWidgetItem, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap
from pipeline.scripts.loader.loader_module.project_data import project_data
import os
import sys
sys.path.append("/home/rapa/yummy")

# from functools import partial

class Mainloader():
    def __init__(self,info,Ui_Form):
        self.ui = Ui_Form
        # self.set_up(Ui_Form)
        print(info)
        
        self.project = info["project"]
        self.user    = info["name"]
        self.rank    = info["rank"]
        self.resolution = info["resolution"]
        
        self.set_comboBox_seq()
        
        self.shot_treeWidget = self.ui.treeWidget
        self.work_table = self.ui.tableWidget_shot_work

        self.set_treeWidget_shot("OPN")
        
        #Signal
        self.ui.comboBox_seq.currentTextChanged.connect(self.set_treeWidget_shot)
        self.shot_treeWidget.itemClicked.connect(self.get_clicked_treeWidget_shot_item)

        # tab - PUB 숨기기
        # self.ui.tabWidget_all.tabBar().setTabVisible(3, False)
        
        
    def set_comboBox_seq(self):
        file_path = f"/home/rapa/YUMMY/project/{self.project}/seq"
        seq_list = os.listdir(file_path)
        self.ui.comboBox_seq.addItems(seq_list)
    
    def set_treeWidget_shot(self,seq):
        self.shot_treeWidget.clear()
        self.file_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{seq}"
        shot_codes = os.listdir(self.file_path)

        # Headerlabel setting
        self.shot_treeWidget.setHeaderLabels(["Shot Code"])

        # shot code setting
        for shot_code in shot_codes:
            parent_item = QTreeWidgetItem(self.shot_treeWidget)
            parent_item.setText(0, shot_code)

        # task setting
            self.task_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{seq}/{shot_code}"
            tasks = os.listdir(self.task_path)

            for task in tasks :
                task_item = QTreeWidgetItem(parent_item)
                task_item.setText(0,task)

    def get_clicked_treeWidget_shot_item (self,item,column):
        """
        선택한 task item 가져오기
        """
        selected_task = item.text(column)

        # 선택한 task의 부모인 shot_code 가져오기 
        parent_item = item.parent()

        if not parent_item:
            return
        else : 
            parent_text = parent_item.text(0)
            # print (parent_text)

        self.work_path = self.file_path + "/" + parent_text + "/" + selected_task

        split = self.work_path.split("/", 3)
        # print (split)
        splited_work_path = split[3]
        # print ("splited_work_path =",splited_work_path)
        label_work_path = "▶" + " " + splited_work_path

        self.ui.label_shot_filepath.setText(label_work_path)

        self.set_work_files_in_tableWidget()

    def set_work_files_in_tableWidget(self):
        """
        work file setting
        """
        #set Table
        self.work_table.setColumnCount(3)
        self.work_table.setRowCount(5)

        
        work_files_path = self.work_path + "/" + "dev" + "/" "work"
        works = os.listdir(work_files_path)
        # print (works)

        # row = 0
        # col = 0
        # table 에 text 로 넣어보기 
        # for work in works:
        #     print (work)
        #     item = QTableWidgetItem()
        #     item.setText(work)
        #     self.work_table.setItem(row,col,item)
        #     col +=1
        
        # label_img = QLabel()
        # image_path_v001 = "/home/rapa/xgen/v001_nknc.png"
        # self.pixmap_v001 = QPixmap(image_path_v001)
        # v001_scaled_pixmap = self.pixmap_v001(199,186, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # label_img.setPixmap(v001_scaled_pixmap)

        label_img = QLabel()
        image_path = "/home/rapa/xgen/v001_nknc.png"
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(100,100)
        img = label_img.setPixmap(scaled_pixmap)
        
        row = 0
        col = 0
        for work in works:
            print (work)
            item = QTableWidgetItem()
            item.setIcon(img)
            self.work_table.setItem(row,col,item)
            col +=1
    
        
        
    def set_up(self,Ui_Form):
        # ui_file_path = "/home/rapa/yummy/pipeline/scripts/loader/main_window.ui"
        # ui_file = QFile(ui_file_path)
        # ui_file.open(QFile.ReadOnly)
        # loader = QUiLoader()
        # self.ui = loader.load(ui_file,self)
        self.ui = Ui_Form
        print(self.ui)
        self.ui.setupUi(self)

    

info = {"project" : "Marvelous" , "name" : "su","rank":"Artist"}

if __name__ == "__main__":
    app = QApplication()
    my  = Mainloader(info)
    my.show()
    app.exec()