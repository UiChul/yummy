from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication,QTableWidgetItem,QTableWidget
from PySide6.QtWidgets import QTableWidgetItem, QAbstractItemView,QMessageBox
from PySide6.QtGui import QPixmap
from pipeline.scripts.loader.loader_module.find_time_size import File_data
import os


class My_task:
    def __init__(self,info,Ui_Form):
        self.ui = Ui_Form
        self.table = self.ui.tableWidget_recent_files
        # self.set_up(Ui_Form)
        self.info = info
        
        self.set_mytask_table()
        self.table.itemClicked.connect(self.check_file_info)
        self.ui.pushButton_mytask_selectedopen.clicked.connect(self.set_open_btn)
        self.ui.pushButton_mytask_newfileopen.clicked.connect(self.set_new_btn)
        
    def check_file_info(self,item):
        index = item.row()
        file_info  = []
        for col in range(3):
            info = self.table.item(index,col)
            file_info.append(info.text())

        self.set_img(file_info)
        self.make_path(file_info)
        
        
    def set_img(self,file_info):
        file_name = file_info[0]
        temp , ext=os.path.splitext(file_name)
        img_path = temp.split("_")

        image_path = f"/home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/exr/{temp}/{temp}.1001.png"
        
        nuke_path = f"/home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/work/{file_name}"
        pixmap = QPixmap(image_path)
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
        self.nuke_path = 'source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc' + f" /home/rapa/YUMMY/project/Marvelous/seq/{img_path[0]}/{img_path[0]}_{img_path[1]}/{img_path[2]}/dev/work/{file_name}"
    
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
        self.table.setColumnCount(3)
        self.table.setRowCount(10)
        
        self.table.setHorizontalHeaderLabels(["Name", "Save_time", "Size"])
        
        self.table.setColumnWidth(0, 495 * 0.5)
        self.table.setColumnWidth(1, 495 * 0.3)
        self.table.setColumnWidth(2, 495 * 0.2)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        
        self.input_mytask_table()
        
    def input_mytask_table(self):
        
        # 여기도 손을 보긴해야겠네
        # 우선 project 선택을 하면 자기 shot을 가지고 오고 거기서 어떤 버전을 사용했는지
        # 가져오고 이걸 시간순으로 정렬을 해서 my task에 띄운다.
        # nuke_path = f"/home/rapa/YUMMY/project/Marvelous/seq/OPN/OPN_0010/dev/work/"
         
        example = {1:{"name" :"OPN_0010_ani_v001.nknc","save":"08-20-15:00","size":"4KB"},
                   2:{"name" :"OPN_0010_ani_v002.nknc","save":"08-20-15:00","size":"4KB"},
                   3:{"name" :"OPN_0010_ani_v003.nknc","save":"08-20-15:00","size":"4KB"}}
        
        i = 0
        for ex in example.values():
            j = 0
            for info in ex.values():
                item = QTableWidgetItem()
                item.setText(info)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i,j,item)
                j +=1
            i +=1
            
    def set_messagebox(self, text, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec()
        
    
    def set_up(self,Ui_Form):
        self.ui = Ui_Form
        self.ui.setupUi(self)
        self.table = self.ui.tableWidget_recent_files


if __name__ == "__main__":
    app = QApplication()
    my = My_task()
    my.show()
    app.exec()