from PySide6.QtWidgets import QWidget,QApplication,QTreeWidgetItem
from PySide6.QtGui import QFont,QPixmap
import sys
sys.path.append("/home/rapa/yummy")
from functools import partial
from pipeline.scripts.loader.loader_module.ffmpeg_module import change_to_png,find_resolution_frame
from pipeline.scripts.loader.loader_module.find_time_size import File_data
import os
import json


class Loader_pub(QWidget):
    def __init__(self):
        super().__init__()
        # self.ui = Ui_Form
        self.set_up()
        # self.tree = self.ui.treeWidget_pub_list
        # self.ui.groupBox_shot_file_info_3.setVisible(False)
        
        self.make_json_dic()
        self.find_pub_list()
        self.set_listwidget()
        self.set_vlc_mov()
        
        self.tree.itemClicked.connect(self.set_thumbnail)
        self.tree.itemDoubleClicked.connect(self.open_file)
        
    def make_json_dic(self):
        with open("/home/rapa/yummy/pipeline/json/project_data.json","rt",encoding="utf-8") as r:
            info = json.load(r)
        
        self.project = info["project"]
        self.user    = info["name"]
        self.rank    = info["rank"]
        self.resolution = info["resolution"]
    
    
    def find_pub_list(self):
        with open("/home/rapa/yummy/pipeline/json/open_loader_datas.json","rt",encoding="utf-8") as r:
            user_dic = json.load(r)
            
            pub_list = []
            project_versions = user_dic["project_versions"]
            for version in project_versions:
                if version["sg_status_list"] == "pub":
                    if version["version_code"][0].isupper():
                        pub_list.append(version["version_code"])                
            return pub_list
            
    
    ## 그럼 리스트 위젯으로 하고 일단 하드코딩으로 해결해야할듯
    def set_listwidget(self):
        
        pub_list = self.find_pub_list()
        
        for pub in pub_list:
            parent_item = QTreeWidgetItem(self.tree)
            parent_item.setText(0,pub)
        
            pub_child = [f"{pub}.nknc",f"{pub}.mov",f"{pub}.exr"]
            for chlid in pub_child:
                item1 = QTreeWidgetItem(parent_item)
                item1.setText(0,chlid)
    
    def set_thumbnail(self,item,column):
        
        pub_name =item.text(column)
        pub_len = pub_name.split(".")
        self.set_file_info(pub_name)
        
        if len(pub_len) == 2:
            pub_name = pub_len[0]
            
        img_path = pub_name.split("_")
        image_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/exr/{pub_name}/{pub_name}.1001.exr"
        
        if not os.path.isdir(f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/.thumbnail/"):
            os.makedirs(f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/.thumbnail/")
        
        png_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/.thumbnail/{pub_name}.1001.png"

        self.mov_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/mov/{pub_name}.mov"
        
        if not os.path.isfile(png_path):
            change_to_png(image_path,png_path)
        
        pixmap = QPixmap(png_path)
        scaled_pixmap = pixmap.scaled(630,350)
        self.ui.label_pub_thumbnail.setPixmap(scaled_pixmap)
        
                  
    def set_file_info(self,pub_name):
        pub_len = pub_name.split(".")
        
        if len(pub_len) == 1:
            self.ui.groupBox_shot_file_info_3.setVisible(False)
            print("no")
            return
        
        if len(pub_len) == 2:
            print("Hello")
            self.ui.groupBox_shot_file_info_3.setVisible(True)
            nuke_name, ext = os.path.splitext(pub_name)
            img_path = nuke_name.split("_")
            
            open_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/"
            w,h,frame = find_resolution_frame(open_path+"mov"+f"/{nuke_name}.mov")
            if ext == ".nknc":
                nuke_path = open_path + f"work/{pub_name}"
                size,time=File_data.file_info(nuke_path)
                file_info_list = [nuke_name,ext,"-",f"{w} X {h}",time,size]
                
            elif ext == ".mov":
                nuke_path = open_path + f"mov/{pub_name}"
                size,time=File_data.file_info(nuke_path)
                file_info_list = [nuke_name,ext,str(frame),f"{w} X {h}",time,size]
            
            elif ext == ".exr":
                nuke_path = open_path + f"exr/{nuke_name}"
                size,time = File_data.dir_info(nuke_path)
                file_info_list = [nuke_name,ext,str(frame),f"{w} X {h}",time,size]

        self.write_file_info(file_info_list)
        
    def write_file_info(self,file_info_list):
        self.ui.label_pub_filename.setText(file_info_list[0])
        self.ui.label_pub_filetype.setText(file_info_list[1])
        self.ui.label_pub_framerange.setText(file_info_list[2])
        self.ui.label_pub_resolution.setText(file_info_list[3])
        self.ui.label_pub_savedtime.setText(file_info_list[4])
        self.ui.label_pub_filesize.setText(file_info_list[5])
            
    
    def set_vlc_mov(self):
        if self.ui.label_pub_thumbnail.mouseDoubleClickEvent:
                self.ui.label_pub_thumbnail.mouseDoubleClickEvent = self.play_video
        
    
    def play_video(self,event):
        cmd = f"vlc --repeat {self.mov_path}"
        os.system(cmd)
    
    
    def open_file(self,item,column):
        pub_name =item.text(column)
        pub_len = pub_name.split(".")
        
        if len(pub_len) == 2:
            nuke_name, ext = os.path.splitext(pub_name)
            img_path = nuke_name.split("_")
            
            open_path = f" /home/rapa/YUMMY/project/{self.project}/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/"
            
            if ext == ".nknc":
                nuke_path = 'source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc' + open_path + f"/work/{pub_name}"
                os.system(nuke_path)
            
            elif ext == ".mov":
                mov_path = "xdg-open " + open_path + "/mov"
                os.system(mov_path)
            
            elif ext == ".exr":
                exr_path = "xdg-open " + open_path + "/exr"
                print("exr")
                os.system(exr_path)
               
    # def find_file_size_date(self,path):
        
    def set_up(self):
        from pipeline.scripts.loader.loader_ui.main_window_v002_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.tree = self.ui.treeWidget_pub_list
        self.ui.groupBox_shot_file_info_3.setVisible(False)
        
info = {"project" : "YUMMIE" , "name" : "UICHUL SHIN","rank":"Artist","resolution" : "1920 X 1080"}

if __name__ == "__main__":
    app = QApplication()
    my = Loader_pub()
    my.show()
    app.exec()