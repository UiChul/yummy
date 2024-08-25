from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QWidget,QApplication,QHeaderView
from PySide6.QtWidgets import QTreeWidgetItem, QTableWidgetItem, QLabel
from PySide6.QtWidgets import QAbstractItemView, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
import os
import sys
import json
sys.path.append("/home/rapa/yummy")

from pipeline.scripts.loader.loader_module.ffmpeg_module import change_to_png
from pipeline.scripts.loader.loader_module.set_thumbnail import find_file_path
from pipeline.scripts.loader.loader_module.find_time_size import File_data
from pipeline.scripts.loader.loader_module import ffmpeg_module

# from functools import partial

class Mainloader(QWidget):
    def __init__(self,info):
        super().__init__()
        self.set_up()
        print(info)
        
        self.project = info["project"]
        self.user    = info["name"]
        self.rank    = info["rank"]
        self.resolution = info["resolution"]
        
        self.set_user_information()
        self.input_project()
        self.set_comboBox_seq()
        self.set_shot_tableWidgets()
        
        
        self.shot_treeWidget = self.ui.treeWidget
        self.work_table = self.ui.tableWidget_shot_work
        self.exr_table = self.ui.tableWidget_shot_exr
        self.mov_table = self.ui.tableWidget_shot_mov
        self.all_list = self.ui.listWidget_shot_allfile

        self.set_treeWidget_shot(self.seq_list[0])
        self.tab_name = "work"
        
        self.task_path = ""
        
        #Signal
        self.ui.comboBox_seq.currentTextChanged.connect(self.set_treeWidget_shot)
        self.shot_treeWidget.itemClicked.connect(self.get_clicked_treeWidget_shot_item)
        self.ui.pushButton_shot_nuke.clicked.connect(self.load_nuke)
        self.ui.tabWidget_shot_task.tabBarClicked.connect(self.get_tab_name)
        self.ui.pushButton_search.clicked.connect(self.search_file_in_alllist)
        self.ui.lineEdit_alllist_search.returnPressed.connect(self.search_file_in_alllist)

        self.work_table.itemClicked.connect(self.get_work_file_information)

        self.exr_table.itemClicked.connect(self.get_exr_file_information)

        self.mov_table.itemClicked.connect(self.get_mov_file_information)
        self.mov_table.itemDoubleClicked.connect(self.set_mov_files)

        self.all_list.itemClicked.connect(self.get_all_file_information)

        # self.set_mov_thumbnail()
        # tab - PUB 숨기기
        # self.ui.tabWidget_all.tabBar().setTabVisible(3, False)
        
    
    #==========================================================================================
    # tree 위젯 셋팅 추가
    #==========================================================================================
    
    
    def input_project(self):
        with open("/home/rapa/yummy/pipeline/json/login_user_data.json","rt",encoding="utf-8") as r:
            user_dic = json.load(r)
            
        for projects in user_dic["projects"]:
            if projects["name"] == self.project:
                self.transform_json_data(projects["shot_code"])
            
        
    def transform_json_data(self,data):
        self.transformed_data = {}

        for key, value in data.items():
            prefix = key.split('_')[0]  # 접두사 추출 (예: 'INS', 'BRK', 'FLB')

            if prefix not in self.transformed_data:
                self.transformed_data[prefix] = []

            self.transformed_data[prefix].append([key, value['steps']])
        
        print(self.transformed_data)
        
        
        
    #==========================================================================================
    # 트리 위젯 세팅 
    #==========================================================================================
        
    """
    seq
    """    
    def set_comboBox_seq(self):
        self.project_path = f"/home/rapa/YUMMY/project/{self.project}/seq"
        self.seq_list = []
        
        for key in self.transformed_data.keys():
            self.seq_list.append(key)
        self.ui.comboBox_seq.addItems(self.seq_list)  
    """
    shot
    """
    def set_treeWidget_shot(self,seq = ""):
        if not seq:
            seq = self.ui.comboBox_seq.currentText()
        self.shot_treeWidget.clear()
        self.file_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{seq}"
        shot_codes = os.listdir(self.file_path)

        # Headerlabel setting
        self.shot_treeWidget.setHeaderLabels(["Shot Code"])

        shot_info = self.transformed_data[seq]
        
        task_shot_code = []
            
        for shot_detail in shot_info:
            task_shot_code.append(shot_detail[0])
            
        # shot code setting
        for shot_code in shot_codes:
            parent_item = QTreeWidgetItem(self.shot_treeWidget)
            if shot_code in task_shot_code:
                parent_item.setText(0, shot_code)
                parent_item.setForeground(0,QColor("Green"))
                
                task_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{seq}/{shot_code}"
                tasks = os.listdir(task_path)

                my_task = []
                for shot_detail in shot_info:
                    if shot_detail[0] == shot_code:
                        for i in shot_detail[1]:
                            my_task.append(i)
                                  
                for task in tasks :
                    task_item = QTreeWidgetItem(parent_item)
                    if task in my_task:
                        task_item.setText(0,task)
                        task_item.setForeground(0,QColor("Green"))
                    else:
                        pub_list = os.listdir(f"{task_path}/{task}/pub/")
                        if pub_list:
                            task_item.setText(0,task)
                            task_item.setForeground(0,QColor("YellowGreen"))
                        else:
                            task_item.setText(0,task)
                            task_item.setForeground(0,QColor("lightgray"))                                      
            else:
                parent_item.setText(0, shot_code)
                parent_item.setForeground(0,QColor("lightgray"))
                
                task_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{seq}/{shot_code}"
                tasks = os.listdir(task_path)
    
                for task in tasks :
                    task_item = QTreeWidgetItem(parent_item)
                    pub_list = os.listdir(f"{task_path}/{task}/pub/")
                    if pub_list:
                        task_item.setText(0,task)
                        task_item.setForeground(0,QColor("YellowGreen"))
                        parent_item.setForeground(0,QColor("YellowGreen"))
                    else:
                        task_item.setText(0,task)
                        task_item.setForeground(0,QColor("lightgray"))
                

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

        self.task_path = self.file_path + "/" + parent_text + "/" + selected_task
        split = self.task_path.split("/", 3)
        splited_work_path = split[3]
        label_work_path = "▶  " + splited_work_path 

        self.ui.label_shot_filepath.setText(label_work_path)

        # self.set_shot_work_files_tableWidget()
        # self.set_shot_all_files_listWidget()
        
    def find_project_task(self,project):
        for project_info in self.user_dic["projects"]:
            if project_info["name"] == project:
                print(project)
                return project_info["shot_code"]
        
    #=======================================================================================
    # 테이블 위젯 세팅 work,mov,exr별로
    #==========================================================================================

    def set_shot_tableWidgets(self):
        """
        tableWidgets (in shot) setting
        """
        #set Table(tab 한번에 세팅)
        tablename = ["work","mov","exr"]
        table_widget = [getattr(self.ui, f"tableWidget_shot_{i}") for i in tablename]

        for i in table_widget:
            h_header = i.horizontalHeader()
            h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
            h_header.setSectionResizeMode(QHeaderView.Stretch)
            i.setEditTriggers(QAbstractItemView.NoEditTriggers) 
            i.setColumnCount(3)
            i.setRowCount(8)
            
    def set_shot_table(self):
        """
        tableWidgets (in shot) setting
        """
        #set Table(tab 한번에 세팅)
        tablename = ["work","mov","exr"]
        table_widget = [getattr(self.ui, f"tableWidget_shot_{i}") for i in tablename]

        for i in table_widget:
            h_header = i.horizontalHeader()
            h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
            h_header.setSectionResizeMode(QHeaderView.Stretch)
            i.setEditTriggers(QAbstractItemView.NoEditTriggers) 
            i.setColumnCount(3)
            i.setRowCount(8)
            
    def get_tab_name (self,tabIndex):
        if tabIndex == 0 :
            self.tab_name = "work"
            self.set_shot_work_files_tableWidget()

        elif tabIndex == 1 :
            self.tab_name = "exr"
            self.set_shot_exr_files_tableWidget()


        elif tabIndex == 2 :
            self.tab_name = "mov"
            self.set_mov_text_files_tableWidget()

        else :
            self.tab_name = "all"   
            self.set_shot_all_files_listWidget()  

    """
    work
    """
    def set_shot_work_files_tableWidget(self):
        """
        work file setting
        """
        self.work_table.clearContents()
        
        h_header = self.work_table.horizontalHeader()
        h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(QHeaderView.Stretch)
        self.work_table.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        self.work_table.setColumnCount(3)
        self.work_table.setRowCount(8)
        
        if self.task_path:
            work_files_path = self.task_path + "/dev/" + self.tab_name
            works = os.listdir(work_files_path)
            if not works:
                print(works)
                self.work_table.setColumnWidth(0, 339)  # -2는 약간의 여유 공간
                self.work_table.setRowHeight(0, 494)
                
                self.work_table.setColumnCount(1)
                self.work_table.setRowCount(1)
                return
              
        else:
            return
        # print (works)

        # table 에 image + text 삽입
        image_path = [
            "/home/rapa/xgen/images1.png",
            "/home/rapa/xgen/images2.png",  
            "/home/rapa/xgen/images3.png"
        ]

        row = 0
        col = 0

        for work in works:
            if not work.split(".")[-1] == "nknc":
                works.remove(work)
       
        for i, work in enumerate(works):
            version = image_path[i % len(image_path)]
            # print (version)

            label_img = QLabel()
            pixmap = QPixmap(version)
            label_img.setPixmap(pixmap) 
            label_img.setAlignment(Qt.AlignCenter)
            label_img.setScaledContents(True)
            self.work_table.setCellWidget(row,col,label_img)

            item = QTableWidgetItem()
            item.setText(work)
            self.work_table.setItem(row+1,col,item)
            item.setTextAlignment(Qt.AlignCenter)

            col +=1
            
            # 갯수 맞춰서 다다음줄로
            if col >= self.work_table.columnCount():            
                col = 0
                row += 2

        # 홀수 row 행 높이 조절
        for i in range(1, self.work_table.rowCount(), 2):
            self.work_table.setRowHeight(i,50)

        
    """
    exr
    """
    def set_shot_exr_files_tableWidget(self):
        """
        exr file setting
        """
        # 폴더안에 들어가서 v001.png 넣어야함.
        # table 에 image + text 삽입
        
        self.exr_table.clearContents()
        if self.task_path:

            exr_files_path = self.task_path + "/dev/" + self.tab_name
            exrs = os.listdir(exr_files_path)
            
        else:
            return
        # print (exrs)

        row = 0
        col = 0

        for exr in exrs :
            exr_file_path = exr_files_path + "/" + exr
            image_path = os.path.join(exr_file_path, exr + ".1001.png")
            
            if not os.path.isdir(f"{self.task_path}/.thumbnail/"):
                os.makedirs(f"{self.task_path}/.thumbnail/")

            png_path = f"{self.task_path}/.thumbnail/{exr}.1001.png"
            
            if not os.path.isfile(png_path):
                change_to_png(image_path,png_path)
            
            label_img = QLabel()
            pixmap = QPixmap(png_path)
            label_img.setPixmap(pixmap) 
            label_img.setAlignment(Qt.AlignCenter)
            label_img.setScaledContents(True)
            self.exr_table.setCellWidget(row,col,label_img)

            item = QTableWidgetItem()
            item.setText(exr)
            self.exr_table.setItem(row+1,col,item)
            item.setTextAlignment(Qt.AlignCenter)

            col +=1
            
            # 갯수 맞춰서 다다음줄로
            if col >= self.exr_table.columnCount():            
                col = 0
                row += 2

        # 홀수 row 행 높이 조절
        for i in range(1, self.exr_table.rowCount(), 2):
            self.exr_table.setRowHeight(i,50) 
 
 
    def set_mov_text_files_tableWidget(self):
           """
           mov file setting
           """
           self.mov_table.clearContents()
           if self.task_path:
                mov_files_path = self.task_path + "/dev/" + self.tab_name
                movs = os.listdir(mov_files_path)
           else:
               return
           # print (movs)
           # print (mov_files_path)

           image_path = [
               "/home/rapa/xgen/MOV_File.png"
           ]

           row = 0
           col = 0

           # table 에 image + text 삽입

           for i, mov in enumerate(movs):

               version = image_path[i % len(image_path)]
               # print (version)

               label_img = QLabel()
               pixmap = QPixmap(version)
               label_img.setPixmap(pixmap) 
               label_img.setAlignment(Qt.AlignCenter)
               label_img.setScaledContents(True)
               self.exr_table.setCellWidget(row,col,label_img)

               item = QTableWidgetItem()
               item.setText(mov)
               self.mov_table.setItem(row+1,col,item)
               item.setTextAlignment(Qt.AlignCenter)


               col +=1

               # 갯수 맞춰서 다다음줄로
               if col >= self.mov_table.columnCount():            
                   col = 00
                   row += 2

           # 홀수 row 행 높이 조절
           for i in range(1, self.mov_table.rowCount(), 2):
               self.mov_table.setRowHeight(i,50)                     
#   ==========================================================================================
#    File Information Setting
#==========================================================================================

    def get_exr_file_information(self, item):
        
        """
        tableWidget에서 클릭한 exr 폴더의 파일의 정보 출력.
        """
        
        selected_file = item.text()
        file_name, _ = os.path.splitext(selected_file)
        
        selected_file = self.get_clicked_nuke_file_path(selected_file)

        file_path = selected_file
        
        size,time= File_data.dir_info(selected_file)
        start,last,frame = ffmpeg_module.get_frame_count_from_directory(selected_file)
        
        frame_range = f"{start}-{last} {frame}"
    
        self.ui.label_shot_filename.setText(file_name)
        self.ui.label_shot_filetype.setText(".exr")
        self.ui.label_shot_framerange.setText(frame_range)
        self.ui.label_shot_resolution.setText(self.resolution)
        self.ui.label_shot_savedtime.setText(time)
        self.ui.label_shot_filesize.setText(size)
        

    def get_work_file_information(self, item):
        """
        tableWidget에서 클릭한 파일의 정보 출력.
        """
        selected_file = item.text()

        file_name,file_type = os.path.splitext(selected_file)
        
        selected_file = self.get_clicked_nuke_file_path(selected_file)
        size,time= File_data.file_info(selected_file)
        
        self.ui.label_shot_filename.setText(file_name)
        self.ui.label_shot_filetype.setText(".nknc")
        self.ui.label_shot_framerange.setText("-")
        self.ui.label_shot_resolution.setText(self.resolution)
        self.ui.label_shot_savedtime.setText(time)
        self.ui.label_shot_filesize.setText(size)
        
        
    def get_mov_file_information(self, item):
        """
        tableWidget에서 클릭한 파일의 정보 출력.
        """
        selected_file = item.text()
        # print (selected_file)

        file_name,  file_type = os.path.splitext(selected_file)
        selected_file = item.text()

        file_name,file_type = os.path.splitext(selected_file)
        
        selected_file = self.get_clicked_nuke_file_path(selected_file)
        size,time= File_data.file_info(selected_file)
        w,h,frame_range = ffmpeg_module.find_resolution_frame(selected_file)

        self.ui.label_shot_filename.setText(file_name)
        self.ui.label_shot_filetype.setText(file_type)
        self.ui.label_shot_framerange.setText(str(frame_range))
        self.ui.label_shot_resolution.setText(self.resolution)
        self.ui.label_shot_savedtime.setText(time)
        self.ui.label_shot_filesize.setText(size)
        

    def get_all_file_information (self,item):
        """
        listWidget에서 클릭한 파일 정보 출력.
        """
        selected_file = item.text()

        file_name, file_type = os.path.splitext(selected_file)
        
        if not file_type :
            self.ui.label_shot_filetype.setText(".exr")
        else:
            self.ui.label_shot_filetype.setText(file_type)

        if file_name == ".nknc":
            self.ui.label_shot_filetype.setText(".nknc")

        self.ui.label_shot_filename.setText(file_name)
        
        
    """
    mov
    """

    def set_mov_files(self,item):
        """
        mov file setting
        """
        mov_files_path = self.task_path + "/" + "dev" + "/" f"{self.tab_name}"
        movs = item.text()

        mov_path = os.path.join(mov_files_path, movs)
        mov_play_path = 'vlc --repeat ' + f"{mov_path}"
        os.system(mov_play_path)

    def set_mov_thumbnail(self):
        mov_files_path = "/home/rapa/YUMMY/project/Marvelous/seq/OPN/OPN_0010/ani/dev/mov" 
        movs = os.listdir(mov_files_path)
        col = 0
        for mov in movs:
            mov_play_path = mov_files_path + mov
            video_widget = QVideoWidget()
            media_player = QMediaPlayer(video_widget)
            media_player.setSource(QUrl.fromLocalFile(mov_play_path))
            media_player.setVideoOutput(video_widget)
            video_layout = QVBoxLayout()
            video_layout.addWidget(video_widget)
            video_container = QWidget()
            video_container.setLayout(video_layout)
            self.mov_table.setCellWidget(0,col,video_container)
            col += 1
            # media_player.play()
    """ 
    all
    """
    def set_shot_all_files_listWidget(self):
        """
        dev 파일 다 긁어와서 list에 한번에 다 넣어주기 (중복 항목 제외)
        """
        # print(self.task_path)
        dev_work_path = self.task_path + "/dev/work"
        dev_exr_path = self.task_path + "/dev/exr"
        dev_mov_path = self.task_path + "/dev/mov"

        work_files = os.listdir(dev_work_path)
        exr_folders = os.listdir(dev_exr_path)
        mov_files = os.listdir(dev_mov_path)

        all_files = work_files + mov_files + exr_folders
        a = ",".join(all_files)
        
        existing_all_items = self.all_list.findItems(a, Qt.MatchExactly)

        if work_files not in existing_all_items:
            self.all_list.addItems(work_files)
        if exr_folders not in existing_all_items:
            self.all_list.addItems(exr_folders)
        if mov_files not in existing_all_items:
            self.all_list.addItems(mov_files)                    
            
        return work_files,mov_files
        
    def search_file_in_alllist(self): 
        
        searching_item = self.ui.lineEdit_alllist_search.text()

        for i in range(self.all_list.count()):
            item = self.all_list.item(i)
            item.setBackground(QColor('#ffffff'))

        # 검색어가 비어있을때는 함수 종료 
        if not searching_item.strip():
            return

        find_items = self.all_list.findItems(searching_item, Qt.MatchContains)
        
        for item in find_items:
            item.setBackground(QColor('#f7e345'))
        
    """
    NUKE
    """
    def get_clicked_nuke_file_path (self,selected_file):
        """
        shot_tableWidget에서 클릭한 파일 path 획득
        """
        front_path = self.ui.label_shot_filepath.text()
        split_front_path = front_path.split(" ")[1]
            
        self.nuke_file_path = "/home/rapa/" + split_front_path + "/dev/" + f"{self.tab_name}" + "/" + selected_file
        return self.nuke_file_path

    def load_nuke (self):
        nuke_path = 'source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc ' + f"{self.nuke_file_path}"
        os.system(nuke_path)


    def set_user_information(self):
    
        self.ui.label_projectname.setText(f"{self.project}")
        self.ui.label_username.setText(f"{self.user}")
        self.ui.label_rank.setText(f"{self.rank}")
        
    def set_up(self):
        # ui_file_path = "/home/rapa/yummy/pipeline/scripts/loader/main_window.ui"
        # ui_file = QFile(ui_file_path)
        # ui_file.open(QFile.ReadOnly)
        # loader = QUiLoader()
        # self.ui = loader.load(ui_file,self)
        from pipeline.scripts.loader.loader_ui.main_window_v002_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)

info = {"project" : "YUMMIE", "name" : "지연 이", "rank" : "Artist", "resolution" : "1920 X 1080"}

if __name__ == "__main__":
    app = QApplication()
    my  = Mainloader(info)
    my.show()
    app.exec()