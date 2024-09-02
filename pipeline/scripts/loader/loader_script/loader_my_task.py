from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication,QTableWidgetItem,QTableWidget
from PySide6.QtWidgets import QTableWidgetItem,QMessageBox,QLabel
from PySide6.QtWidgets import QWidget,QAbstractItemView
from PySide6.QtCore import QFile,QSize
from PySide6.QtGui import QPixmap,QMovie
import os
import json
import sys
import re
import threading
import subprocess
from datetime import datetime
sys.path.append("/home/rapa/yummy/")
from PySide6.QtGui import QPixmap
from pipeline.scripts.loader.loader_module.ffmpeg_module import change_to_png
from pipeline.scripts.loader.loader_module.find_time_size import File_data

class My_task:
    def __init__(self,Ui_Form):
        self.ui = Ui_Form
        self.table = self.ui.tableWidget_recent_files
        self.status_table = self.ui.tableWidget_mytask_status
        
        self.make_json_dic()
        self.set_click_thumbnail_mov()
        self.set_description_list()
        self.set_status_table()     
        self.set_mytask_table()
        
        self.table.itemClicked.connect(self.check_file_info)
        self.ui.pushButton_mytask_selectedopen.clicked.connect(self.set_open_btn)
        self.ui.pushButton_mytask_newfileopen.clicked.connect(self.set_new_btn)
        
    def make_json_dic(self):
        with open("/home/rapa/yummy/pipeline/json/project_data.json","rt",encoding="utf-8") as r:
            info = json.load(r)
        
        self.project = info["project"]
        self.user    = info["name"]
        self.rank    = info["rank"]
        self.resolution = info["resolution"]
        
    def check_file_info(self,item):
        
        if type(item) == list:
            file_info = item
        else:
            index = item.row()
            file_info  = []
            for col in range(2):
                info = self.table.item(index,col)
                file_info.append(info.text())
        
        self.status_table.clearContents()
        my_task_list = self.set_mytask_status(file_info)
        self.input_status_table(my_task_list)
        self.set_img(file_info)
        self.make_path(file_info)
          
    def set_img(self,file_info):
        file_name = file_info[0]
        temp,ext  = os.path.splitext(file_name)
        img_path  = temp.split("_")
        
        self.mov_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/mov/{temp}.mov"
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
        file_info = [temp,ext,self.resolution,save_time,file_size]
        self.set_file_information(file_info)
    
    def set_file_information(self,file_info):
        descirption = self.find_description_list(file_info[0])
        if not descirption:
            descirption = "No Comment"
        self.ui.label_mytask_filename.setText(f"{file_info[0]}")
        self.ui.label_mytask_filetype.setText(f"{file_info[1]}")
        self.ui.label_mytask_resolution.setText(f"{file_info[2]}")
        self.ui.label_mytask_savedtime.setText(f"{file_info[3]}")
        self.ui.label_mytask_filesize.setText(f"{file_info[4]}")
        self.ui.plainTextEdit_mytask_comment.setPlainText(descirption)
        
    def make_path(self,file_info):
        file_name = file_info[0]
        temp , ext=os.path.splitext(file_name)
        img_path = temp.split("_")    
        self.nuke_path = 'source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc' + f" /home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/work/{file_name}"
      
    def set_open_btn(self):
        if self.nuke_path:
            subprocess.Popen(self.nuke_path, shell=True,executable="/bin/bash")

            # os.system(self.nuke_path)
        else:
            self.set_messagebox("파일을 먼저 선택해주세요") 
        # pass
    
    def set_new_btn(self):
        subprocess.Popen('source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc', shell=True,executable="/bin/bash")

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
        
        user_dic = self.open_loader_json()
        
        my_task_list = []
        
        versions = user_dic["project_versions"]
        for version in versions:
            version_dic = {}
            if version["artist"] == self.user: 
                version_dic[version["updated_at"]] = version["version_code"]+".nknc"
                my_task_list.append(version_dic)
        
        my_task_list.sort(key=self.extract_time_mytask,reverse=True)
                
        return my_task_list
        
    def extract_time_mytask(self,item):
        save_time_str = list(item.keys())[0]
        return datetime.strptime(save_time_str, '%Y-%m-%d %H:%M:%S')
            
    def input_mytask_table(self):
        
        # 여기도 손을 보긴해야겠네
        # 우선 project 선택을 하면 자기 shot을 가지고 오고 거기서 어떤 버전을 사용했는지
        # 가져오고 이걸 시간순으로 정렬을 해서 my task에 띄운다.
        # nuke_path = f"/home/rapa/YUMMY/project/Marvelous/seq/OPN/OPN_0010/dev/work/"
         
         
        my_task_table = self.set_recent_file()  
        
        start_list = []
        
        i = 0
        for file_info in my_task_table:
            for time,file_name in file_info.items():
                if i == 0:
                    start_list.append(file_name)
                    start_list.append(time)
                item = QTableWidgetItem()
                item.setText(time)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i,1,item)
                
                
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                
                item = QTableWidgetItem()
                item.setText(file_name)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                
                self.table.setItem(i,0,item)
                
            i +=1
            
        self.check_file_info(start_list)
            
    def set_messagebox(self, text, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec()
        
    def set_click_thumbnail_mov(self):
        if self.ui.label_mytask_thumbnail.mouseDoubleClickEvent:
                self.ui.label_mytask_thumbnail.mouseDoubleClickEvent = self.play_video
                
    def play_video(self,event):
        cmd = f"vlc --repeat {self.mov_path}"
        os.system(cmd)
        
    def set_description_list(self):
        
        user_dic = self.open_loader_json()
        
        self.description_list = []
        
        versions = user_dic["project_versions"]
        
        for version in versions:
            version_dic = {}
            version_dic[version["version_code"]] = version["description"]
            self.description_list.append(version_dic)  
             
    
    def find_description_list(self,file_name):
        for comment in self.description_list:
            for shot_code , desription in comment.items():
                if shot_code == file_name:
                    return desription
      
    def open_loader_json(self):
        with open("/home/rapa/yummy/pipeline/json/open_loader_datas.json","rt",encoding="utf-8") as r:
               user_dic = json.load(r)
        return user_dic  
        
    def set_mytask_status(self,file_info):
        
        user_dic = self.open_loader_json()
        file_name = file_info[0]
        shot_code_data,_ = os.path.splitext(file_name)

        shot_code_data_split = shot_code_data.split("_")
        
        shot_code = "_".join([shot_code_data_split[0],shot_code_data_split[1]])
        
        project_versions = user_dic["project_versions"]
        
        my_task_list = []
        
        for version in project_versions:
            match_shot_code = re.match(fr"{shot_code}",version["version_code"])
            if match_shot_code:
                
                shot_dic = {}
                shot_info = version["version_code"].split("_")
                task  = shot_info[2]
                
                shot_dic["Artist"] = version["artist"] 
                shot_dic["Shot Code"]  = "_".join([shot_info[0],shot_info[1]])
                shot_dic["Task"]  = task
                shot_dic["Version"] = shot_info[-1] 
                shot_dic["Status"]  = version["sg_status_list"]
                shot_dic["UpdateDate"] = version["updated_at"]
                shot_dic["Description"] = version["description"]
                
                my_task_list.append(shot_dic)
        return my_task_list

        
    def input_status_table(self,my_task_list):
        # my_task_list.sort(key=self.extract_time,reverse = True)
        
        my_task_list.reverse()
        row = 0
        for status_info in my_task_list:
            col = 0
            for info in status_info.values():
                item = QTableWidgetItem()
                if col == 4:
                    if info == "wip":
                        label = QLabel()
                        gif_movie = QMovie("//home/rapa/YUMMY/pipeline/source/wip001.gif")
                        gif_movie.setScaledSize(QSize(80,60))# GIF 파일 경로 설정
                        label.setMovie(gif_movie)
                        gif_movie.start() 
                        label.setAlignment(Qt.AlignCenter)
                        self.status_table.setCellWidget(row, col, label)
                        
                    elif info == "pub":
                        label = QLabel()
                        gif_movie = QMovie("/home/rapa/YUMMY/pipeline/source/pub003.gif")
                        gif_movie.setScaledSize(QSize(100,50))# GIF 파일 경로 설정
                        label.setMovie(gif_movie)
                        gif_movie.start() 
                        label.setAlignment(Qt.AlignCenter)
                        self.status_table.setCellWidget(row, col, label)
                        
                    elif info == "fin" or info == "sc":
                        label = QLabel()
                        gif_movie = QMovie("/home/rapa/YUMMY/pipeline/source/pub002.gif")
                        gif_movie.setScaledSize(QSize(120,90))# GIF 파일 경로 설정
                        label.setMovie(gif_movie)
                        gif_movie.start() 
                        label.setAlignment(Qt.AlignCenter)
                        self.status_table.setCellWidget(row, col, label)
                                 
                else:
                    if not info:
                        info = "No description"
                    item.setText(info)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.status_table.setItem(row,col,item)
                col += 1
            row += 1
    
    # def extract_time(self,item):
    #     return datetime.strptime(item['UpdateDate'], '%Y-%m-%d %H:%M:%S')
    def set_status_table(self):
        
        self.status_table.setColumnCount(7)
        self.status_table.setRowCount(8)
        
        self.status_table.setHorizontalHeaderLabels(["Artist","ShotCode","Task","Version","Status","Upadate Data" ,"Description"])
        
        self.status_table.setColumnWidth(0, 1020 * 0.13)
        self.status_table.setColumnWidth(1, 1020 * 0.12)
        self.status_table.setColumnWidth(2, 1020 * 0.1)
        self.status_table.setColumnWidth(3, 1020 * 0.1)
        self.status_table.setColumnWidth(4, 1020 * 0.05)
        self.status_table.setColumnWidth(5, 1020*  0.20)
        self.status_table.setColumnWidth(6, 1030 * 0.30)
        self.status_table.setSelectionBehavior(QTableWidget.SelectRows)    
        self.status_table.setEditTriggers(QAbstractItemView.NoEditTriggers) 
           
    def set_up(self):
        from pipeline.scripts.loader.loader_ui.main_window_v002_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.table = self.ui.tableWidget_recent_files
        self.status_table = self.ui.tableWidget_mytask_status

info = {"project" : "YUMMIE" , "name" : "UICHUL SHIN","rank":"Artist","resolution" : "1920 X 1080"}
if __name__ == "__main__":
    app = QApplication()
    my = My_task()
    my.show()
    app.exec_()