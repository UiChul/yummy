from PySide6.QtWidgets import QWidget,QApplication,QTreeWidgetItem
from PySide6.QtGui import QFont,QPixmap

from pipeline.scripts.loader.loader_ui.main_window_v002_ui import Ui_Form
from functools import partial
from pipeline.scripts.loader.loader_module.file_info import File_data
import os

class Loader_Pub(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up()
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
        
        if len(pub_len) == 1:
            img_path = pub_name.split("_")
            image_path = f"/home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/exr/{pub_name}/{pub_name}.1010.png"
            self.mov_path = f"/home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/mov/{pub_name}.mov"
            
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(630,350)
            self.ui.label_pub_thumbnail.setPixmap(scaled_pixmap)
    
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
            
            print(ext)
            if ext == ".nknc":
                nuke_path = 'source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc' + f" /home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/work/{pub_name}"
                os.system(nuke_path)
            
            elif ext == ".mov":
                mov_path = f"xdg-open /home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/mov"
                os.system(mov_path)
            
            elif ext == ".exr":
                exr_path = f"xdg-open /home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/exr"
                os.system(exr_path)
                
    # def find_file_size_date(self,path):
        
    
    
    
        
    def set_up(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.tree = self.ui.treeWidget_pub_list
    
app = QApplication()

my = Loader_Pub()
my.show()
app.exec()