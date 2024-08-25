from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication,QTableWidgetItem,QTableWidget
from PySide6.QtWidgets import QTableWidgetItem, QAbstractItemView,QMessageBox
from PySide6.QtWidgets import QWidget
import sys
sys.path.append("/home/rapa/yummy/")
from PySide6.QtGui import QPixmap
from pipeline.scripts.loader.loader_module.ffmpeg_module import change_to_png
from pipeline.scripts.loader.loader_module.find_time_size import File_data
import os
import json
from datetime import datetime


class My_task(QWidget):
    def __init__(self,info):
        super().__init__()
        # self.ui = Ui_Form
        # self.table = self.ui.tableWidget_recent_files
        self.set_up()
        self.info = info
        
        self.project = info["project"]
        self.name = info["name"]
        
        self.set_recent_file()
        
        self.set_mytask_table()
        self.table.itemClicked.connect(self.check_file_info)
        self.ui.pushButton_mytask_selectedopen.clicked.connect(self.set_open_btn)
        self.ui.pushButton_mytask_newfileopen.clicked.connect(self.set_new_btn)
        
    def check_file_info(self,item):
        index = item.row()
        file_info  = []
        for col in range(2):
            info = self.table.item(index,col)
            file_info.append(info.text())

        print(file_info)
        self.set_img(file_info)
        self.make_path(file_info)
        
        
    def set_img(self,file_info):
        file_name = file_info[0]
        temp , ext=os.path.splitext(file_name)
        img_path = temp.split("_")

        image_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/exr/{temp}/{temp}.1001.exr"
        
        if not os.path.isdir(f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/.thumbnail/"):
            os.makedirs(f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/.thumbnail/")
        
        png_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/.thumbnail/{temp}.1001.png"
        
        nuke_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/work/{file_name}"
        
        if not os.path.isfile(png_path):
            change_to_png(image_path,png_path)
            
        pixmap = QPixmap(png_path)
        scaled_pixmap = pixmap.scaled(270,152)
        self.ui.label_mytask_thumbnail.setPixmap(scaled_pixmap)
        
        file_size,save_time  =  File_data.file_info(nuke_path)
        file_info = [temp,ext,self.info["resolution"],save_time,file_size]
        self.set_file_information(file_info)
    
    def set_file_information(self,file_info):
        self.ui.label_mytask_filename.setText(f"{file_info[0]}")
        self.ui.label_mytask_filetype.setText(f"{file_info[1]}")
        self.ui.label_mytask_resolution.setText(f"{file_info[2]}")
        self.ui.label_mytask_savedtime.setText(f"{file_info[3]}")
        self.ui.label_mytask_filesize.setText(f"{file_info[4]}")
        
    def make_path(self,file_info):
        file_name = file_info[0]
        temp , ext=os.path.splitext(file_name)
        img_path = temp.split("_")    
        self.nuke_path = 'source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc' + f" /home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/work/{file_name}"
    
    def set_open_btn(self):
        try:
            os.system(self.nuke_path)
        except:
            self.set_messagebox("파일을 먼저 선택해주세요") 
        pass
            
    def set_new_btn(self):
        os.system('source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc')
        pass
        
    def set_mytask_table(self):
        self.table.setColumnCount(2)
        self.table.setRowCount(10)
        
        self.table.setHorizontalHeaderLabels(["Name", "Update_time"])
        
        self.table.setColumnWidth(0, 495 * 0.6)
        self.table.setColumnWidth(1, 500 * 0.4)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        
        self.input_mytask_table()
        
    def set_recent_file(self):
        with open("/home/rapa/yummy/pipeline/json/open_loader_datas.json","rt",encoding="utf-8") as r:
            user_dic = json.load(r)
        
        my_task_list = []
        
        versions = user_dic["versions"]
        for version in versions:
            version_dic = {}
            if version["created_by"] == self.name: 
                version_dic[version["updated_at"]] = version["version_code"]+".nknc"
                my_task_list.append(version_dic)
        
        my_task_list.sort(key=self.extract_time,reverse=True)
                
        return my_task_list
        
    def extract_time(self,item):
        save_time_str = list(item.keys())[0]
        return datetime.strptime(save_time_str, '%Y-%m-%d %H:%M:%S')
    
            
            
    def input_mytask_table(self):
        
        # 여기도 손을 보긴해야겠네
        # 우선 project 선택을 하면 자기 shot을 가지고 오고 거기서 어떤 버전을 사용했는지
        # 가져오고 이걸 시간순으로 정렬을 해서 my task에 띄운다.
        # nuke_path = f"/home/rapa/YUMMY/project/Marvelous/seq/OPN/OPN_0010/dev/work/"
         
        my_task_table = self.set_recent_file()  
        
        i = 0
        for file_info in my_task_table:
            for time,file_name in file_info.items():
                item = QTableWidgetItem()
                item.setText(time)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i,1,item)
                item = QTableWidgetItem()
                item.setText(file_name)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i,0,item)
            i +=1
            
    def set_messagebox(self, text, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec()
        
    
    def set_up(self):
        from pipeline.scripts.loader.loader_ui.main_window_v002_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.table = self.ui.tableWidget_recent_files

info = {"project" : "YUMMIE" , "name" : "지연 이","rank":"Artist","resolution" : "1920 X 1080"}
if __name__ == "__main__":
    app = QApplication()
    my = My_task(info)
    my.show()
    app.exec()