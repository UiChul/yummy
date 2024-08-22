from PySide6.QtWidgets import QWidget,QApplication,QTreeWidgetItem
from PySide6.QtGui import QFont,QPixmap
import sys
sys.path.append("/home/rapa/yummy")
from functools import partial
from pipeline.scripts.loader.loader_module.exr_to_jpg import change_to_png,find_resolution_frame
from pipeline.scripts.loader.loader_module.find_time_size import File_data
import os

class Loader_pub:
    def __init__(self,Ui_Form):
        self.ui = Ui_Form
        self.tree = self.ui.treeWidget_pub_list
        self.ui.groupBox_shot_file_info_3.setVisible(False)
        # self.set_up(Ui_Form)
        self.set_listwidget()
        self.set_vlc_mov()
        
        self.tree.itemClicked.connect(self.set_thumbnail)
        self.tree.itemDoubleClicked.connect(self.open_file)
        
    ## 그럼 리스트 위젯으로 하고 일단 하드코딩으로 해결해야할듯
    def set_listwidget(self):
    
        parent_item = QTreeWidgetItem(self.tree)
        parent_item.setText(0,"OPN_0010_ani_v003")
        
        pub = ["OPN_0010_ani_v003.nknc","OPN_0010_ani_v003.mov","OPN_0010_ani_v003.exr"]
        for i in pub:
            item1 = QTreeWidgetItem(parent_item)
            item1.setText(0,f"{i}")
    
    def set_thumbnail(self,item,column):
        pub_name =item.text(column)
        pub_len = pub_name.split(".")
        self.set_file_info(pub_name)
        
        if len(pub_len) == 2:
            pub_name = pub_len[0]
            
        img_path = pub_name.split("_")
        image_path = f"/home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/exr/{pub_name}/{pub_name}.1001.exr"
        png_path = f"/home/rapa/YUMMY/project/Marvelous/seq/{pub_name}.1001.png"
        self.mov_path = f"/home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/mov/{pub_name}.mov"
        
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
            
            open_path = f"/home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/"
            w,h,frame = find_resolution_frame(open_path+"mov"+f"/{nuke_name}.mov")
            print(ext)
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
            
            open_path = f" /home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/"
            
            print(ext)
            if ext == ".nknc":
                nuke_path = 'source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc' + open_path + f"/work/{pub_name}"
                os.system(nuke_path)
            
            elif ext == ".mov":
                mov_path = "xdg-open " + open_path + "/mov"
                os.system(mov_path)
            
            elif ext == ".exr":
                exr_path = "xdg-open " + open_path + "/exr"
                os.system(exr_path)
                
    # def find_file_size_date(self,path):
        
    def set_up(self,Ui_Form):
        self.ui = Ui_Form
        self.tree = self.ui.treeWidget_pub_list
        self.ui.groupBox_shot_file_info_3.setVisible(False)

if __name__ == "__main__":
    app = QApplication()
    my = Loader_pub()
    my.show()
    app.exec()