from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QWidget,QApplication,QHeaderView
from PySide6.QtWidgets import QTreeWidgetItem, QTableWidgetItem, QLabel,QTableWidget
from PySide6.QtWidgets import QAbstractItemView, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile,QSize
from PySide6.QtGui import QPixmap, QColor,QFont,QMovie
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
import threading
import subprocess
import os
import sys
import json
from functools import partial
from datetime import datetime

sys.path.append("/home/rapa/yummy/pipeline/scripts/loader")

from loader_module.ffmpeg_module import change_to_png
from loader_module.find_time_size import File_data
from loader_module import ffmpeg_module

# from functools import partial

class Mainloader:
    def __init__(self,Ui_Form):
        # super().__init__()
        self.ui = Ui_Form
        # self.set_up()
        
        self.set_project_info()
        self.set_shot_tableWidgets()
        self.set_status_table_list()
        self.input_project()
        self.set_comboBox_seq()
        self.set_description_list()
        
        self.get_task_tab_name(2)
        
        self.shot_treeWidget = self.ui.treeWidget
        self.work_table = self.ui.tableWidget_shot_work
        self.exr_table = self.ui.tableWidget_shot_exr
        self.mov_table = self.ui.tableWidget_shot_mov
        self.all_list = self.ui.listWidget_shot_allfile

        self.set_treeWidget_shot(self.seq_list[0])
        self.tab_name = ""
        self.task_path = ""
        
        #Signal
        self.ui.comboBox_seq.currentTextChanged.connect(self.set_treeWidget_shot)
        self.shot_treeWidget.itemClicked.connect(self.get_clicked_treeWidget_shot_item)
        self.ui.pushButton_shot_open.clicked.connect(self.load_nuke)
        self.ui.pushButton_shot_new.clicked.connect(self.load_new_nuke)
        
        self.ui.tabWidget_shot_task.tabBarClicked.connect(self.get_tab_name)
        self.ui.tabWidget_shot_status.tabBarClicked.connect(self.get_task_tab_name)
        self.ui.pushButton_search.clicked.connect(self.search_file_in_alllist)
        self.ui.lineEdit_alllist_search.returnPressed.connect(self.search_file_in_alllist)

        self.work_table.itemClicked.connect(self.set_work_file_information)
        self.exr_table.itemClicked.connect(self.set_exr_file_information)
        self.mov_table.itemClicked.connect(self.set_mov_file_information)
        
        self.mov_table.itemDoubleClicked.connect(self.set_mov_files)
        self.all_list.itemClicked.connect(self.set_all_file_information)

    
    # ==============================================================================================    
    # json 연결
    # ==============================================================================================    
    
    # project 기본 세팅 설정
    
    def set_project_info(self):
        with open("/home/rapa/yummy/pipeline/json/project_data.json","rt",encoding="utf-8") as r:
            info = json.load(r)
            
        self.project = info["project"]
        self.user    = info["name"]
        self.rank    = info["rank"]
        self.resolution = info["resolution"]
    
    # ==========================================================================================
    # tree 위젯 셋팅 추가
    # ==========================================================================================
    
    
    def input_project(self):
        with open("/home/rapa/yummy/pipeline/json/login_user_data.json","rt",encoding="utf-8") as r:
            user_dic = json.load(r)
            
        for projects in user_dic["projects"]:
            if projects["name"] == self.project:
                self.transform_json_data(projects["shot_code"])

    def transform_json_data(self,data):
        
        self.transformed_data = {}

        for key, value in data.items():
            prefix = key.split('_')[0]

            if prefix not in self.transformed_data:
                self.transformed_data[prefix] = []

            self.transformed_data[prefix].append([key, value['steps']])
                 
    #==========================================================================================
    # 트리 위젯 세팅 
    #==========================================================================================
        
    def set_comboBox_seq(self):
        self.project_path = f"/home/rapa/YUMMY/project/{self.project}/seq"
        self.seq_list = []
        
        for key in self.transformed_data.keys():
            self.seq_list.append(key)
        self.ui.comboBox_seq.addItems(self.seq_list)  

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
        
        self.my_dev_list = []
        # shot code setting
        for shot_code in shot_codes:
            parent_item = QTreeWidgetItem(self.shot_treeWidget)
            if shot_code in task_shot_code:
                parent_item.setText(0, shot_code)
                parent_item.setForeground(0,QColor(0,251,236))
                
                task_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{seq}/{shot_code}"
                tasks = os.listdir(task_path)
                tasks.sort()
                my_task = []
                for shot_detail in shot_info:
                    if shot_detail[0] == shot_code:
                        for i in shot_detail[1]:
                            my_task.append(i)
                              
                for task in tasks :
                    task_item = QTreeWidgetItem(parent_item)
                    if task in my_task:
                        task_item.setText(0,task)
                        task_item.setForeground(0,QColor(0,251,236))
                        my_task_dict = {}
                        my_task_dict[task] = shot_code
                        self.my_dev_list.append(my_task_dict)
                        
                    else:
                        pub_list = os.listdir(f"{task_path}/{task}/pub/work")
                        if pub_list:
                            task_item.setText(0,task)
                            task_item.setForeground(0,QColor("Skyblue"))
                           
                        else:
                            task_item.setText(0,task)
                            task_item.setForeground(0,QColor("lightgray"))                                      
            else:
                parent_item.setText(0, shot_code)
                parent_item.setForeground(0,QColor("lightgray"))
                
                task_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{seq}/{shot_code}"
                tasks = os.listdir(task_path)
                tasks.sort()
                for task in tasks : 
                    task_item = QTreeWidgetItem(parent_item)
                    pub_list = os.listdir(f"{task_path}/{task}/pub/work")
                    if pub_list:
                        task_item.setText(0,task)
                        task_item.setForeground(0,QColor(122, 181, 181))
                        parent_item.setForeground(0,QColor(122, 181, 181))
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
        
        self.clear_file_info()
        
        if self.tab_name == "work":
            self.set_shot_work_files_tableWidget()
        elif self.tab_name == "exr":
            self.set_shot_exr_files_tableWidget()
        elif self.tab_name == "mov":
            self.set_shot_mov_files_tableWidget()
        elif self.tab_name == "all":
            self.set_shot_all_files_listWidget()
        else:
            self.set_shot_work_files_tableWidget()
            
    #=======================================================================================
    # 테이블 위젯 세팅 work,mov,exr별로
    #==========================================================================================

    def set_shot_tableWidgets(self):
        #set Table(tab 한번에 세팅)
        tablename = ["work","mov","exr"]
        self.table_widget = [getattr(self.ui, f"tableWidget_shot_{i}") for i in tablename]
            
    def set_shot_table(self,tab):
        """
        tableWidgets (in shot) setting
        """
        #set Table(tab 한번에 세팅)      
        if tab == "work":
            table_widget = self.table_widget[0]
        elif tab == "mov":
            table_widget = self.table_widget[1]
        elif tab == "exr":
            table_widget = self.table_widget[2]

        h_header = table_widget.horizontalHeader()
        h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(QHeaderView.Stretch)
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        table_widget.setColumnCount(3)
        table_widget.setRowCount(8)
        table_widget.setShowGrid(False)
                 
    def get_tab_name (self,tabIndex):
        if tabIndex == 0 :
            self.tab_name = "work"
            self.set_shot_work_files_tableWidget()

        elif tabIndex == 1 :
            self.tab_name = "exr"
            self.set_shot_exr_files_tableWidget()


        elif tabIndex == 2 :
            self.tab_name = "mov"
            self.set_shot_mov_files_tableWidget()

        else :
            self.tab_name = "all"   
            self.set_shot_all_files_listWidget()  

    # work 파일
    def set_shot_work_files_tableWidget(self):
        """
        work file setting
        """
        self.tab_name = "work"
            
        self.clear_file_info()
        self.set_shot_table("work")
        
        for row in range(self.work_table.rowCount()):
            self.work_table.setRowHeight(row,195)
            
        self.work_table.setShowGrid(True)
        
        
        self.work_table.clearContents()
            
        if self.task_path:

            task = self.task_path.split("/")[-1]
            shot_code = self.task_path.split("/")[-2]
            
            pub_dev = "pub"
            
            for task_shot_code in self.my_dev_list:
                for dev_task,dev_shot_code in task_shot_code.items():
                    if dev_task == task and dev_shot_code == shot_code:
                        pub_dev = "dev"
            
            work_files_path = self.task_path + f"/{pub_dev}/" + self.tab_name
            works = os.listdir(work_files_path)
                      
            if not works:
                h_header = self.work_table.horizontalHeader()
                h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
                h_header.setSectionResizeMode(QHeaderView.Stretch)
                self.work_table.setColumnCount(1)
                self.work_table.setRowCount(1)
                self.work_table.setShowGrid(False)
                       
                item = QTableWidgetItem()
                item.setText("EMPTY")
                
                # 테이블 폰트 사이즈 조절
                font  = QFont()
                font.setPointSize(40)
                item.setFont(font)
                
                # 아이템 클릭할 수 없게 만들기
                item.setFlags(Qt.NoItemFlags)
                self.work_table.setItem(0,0,item)
                item.setTextAlignment(Qt.AlignCenter)   
                return   
        else:
            return
        
        # table 에 image + text 삽입
        row = 0
        col = 0

        for work in works:
            if not work.split(".")[-1] == "nknc":
                works.remove(work)
       
        for work in works:
            
            cell_widget = QWidget()
            layout = QVBoxLayout()

            label_img = QLabel()
            pixmap = QPixmap("/home/rapa/YUMMY/pipeline/source/images1.png")
            label_img.setPixmap(pixmap) 
            label_img.setAlignment(Qt.AlignCenter)
            label_img.setScaledContents(True)
            
            label_text = QLabel()
            label_text.setText(work)
            label_text.setAlignment(Qt.AlignCenter)
            label_text.setStyleSheet('font-size: 11px;color:rgb(211, 215, 207);')
            label_text.setWordWrap(True)
            
            layout.addWidget(label_img)
            layout.addWidget(label_text)
            layout.setContentsMargins(0,0,0,10)
            layout.setAlignment(Qt.AlignCenter)  
            cell_widget.setLayout(layout)
            
            item = QTableWidgetItem()
            item.setText(work)
            self.work_table.setItem(row, col, item)
            self.work_table.setCellWidget(row,col,cell_widget)
            
            col +=1
            
            # self.reduce_item_visibility_in_tableWidget(row, col)
            
            # 갯수 맞춰서 다다음줄로
            if col >= self.work_table.columnCount():            
                col = 0
                row += 1

        # # 홀수 row 행 높이 조절
        # for i in range(1, self.work_table.rowCount(), 2):
        #     self.work_table.setRowHeight(i,50)
        
    # exr 파일
    def set_shot_exr_files_tableWidget(self):
        """
        exr file setting
        """
        # 폴더안에 들어가서 v001.png 넣어야함.
        # table 에 image + text 삽입
        if not self.tab_name:
            self.tab_name = "exr" 
        
        self.clear_file_info()
        self.set_shot_table("exr")
        
        for row in range(self.work_table.rowCount()):
            self.exr_table.setRowHeight(row,120)
        
        self.exr_table.setShowGrid(True)
        
        self.exr_table.clearContents()
        
        if self.task_path:
            
            
            task = self.task_path.split("/")[-1]
            shot_code = self.task_path.split("/")[-2]
            
            pub_dev = "pub"
            
            for task_shot_code in self.my_dev_list:
                for dev_task,dev_shot_code in task_shot_code.items():
                    if dev_task == task and dev_shot_code == shot_code:
                        pub_dev = "dev"
                        
            exr_files_path = self.task_path + f"/{pub_dev}/" + self.tab_name
            exrs = os.listdir(exr_files_path)
            if not exrs:
                h_header = self.exr_table.horizontalHeader()
                h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
                h_header.setSectionResizeMode(QHeaderView.Stretch)
                self.exr_table.setColumnCount(1)
                self.exr_table.setRowCount(1)
                self.exr_table.setShowGrid(False)
                       
                item = QTableWidgetItem()
                item.setText("EMPTY")
                
                # 테이블 폰트 사이즈 조절
                font  = QFont()
                font.setPointSize(40)
                item.setFont(font)
                
                # 아이템 클릭할 수 없게 만들기
                item.setFlags(Qt.NoItemFlags)
                self.exr_table.setItem(0,0,item)
                item.setTextAlignment(Qt.AlignCenter)
            
        else:
            return
        
        row = 0
        col = 0

        for exr in exrs :
            exr_file_path = exr_files_path + "/" + exr
            image_path = os.path.join(exr_file_path, exr + ".1001.exr")
            
            if not os.path.isdir(f"{self.task_path}/.thumbnail/"):
                os.makedirs(f"{self.task_path}/.thumbnail/")

            png_path = f"{self.task_path}/.thumbnail/{exr}.1001.png"
            
            if not os.path.isfile(png_path):
                change_to_png(image_path,png_path)
            
            cell_widget = QWidget()
            layout = QVBoxLayout()

            
            label_img = QLabel()
            pixmap = QPixmap(png_path)
            label_img.setPixmap(pixmap) 
            label_img.setAlignment(Qt.AlignCenter)
            label_img.setScaledContents(True)
            
            label_text = QLabel()
            label_text.setText(exr)
            label_text.setAlignment(Qt.AlignCenter)
            label_text.setStyleSheet('font-size: 11px;color:rgb(211, 215, 207);')
            # label_text.setStyleSheet('color:rgb(211, 215, 207);')
            label_text.setWordWrap(True)
            
            layout.addWidget(label_img)
            layout.addWidget(label_text)
            layout.setContentsMargins(0,0,0,10)
            layout.setAlignment(Qt.AlignCenter)  
            cell_widget.setLayout(layout)

            item = QTableWidgetItem()
            item.setText(exr)
            self.exr_table.setItem(row, col, item)
            self.exr_table.setCellWidget(row,col,cell_widget)
            
            col +=1
            
            # 갯수 맞춰서 다다음줄로
            if col >= self.exr_table.columnCount():            
                col = 0
                row += 1
 
    # mov 파일
    def set_shot_mov_files_tableWidget(self):
        """
        exr file setting
        """
        # 폴더안에 들어가서 v001.png 넣어야함.
        # table 에 image + text 삽입
        
        if not self.tab_name:
            self.tab_name = "mov"
        
        self.clear_file_info()
        self.set_shot_table("mov")
        
        for row in range(self.work_table.rowCount()):
            self.mov_table.setRowHeight(row,120)
    
        self.mov_table.setShowGrid(True)
        self.mov_table.clearContents()
        
        if self.task_path:
            
            task = self.task_path.split("/")[-1]
            shot_code = self.task_path.split("/")[-2]
            
            pub_dev = "pub"
            
            for task_shot_code in self.my_dev_list:
                for dev_task,dev_shot_code in task_shot_code.items():
                    if dev_task == task and dev_shot_code == shot_code:
                        pub_dev = "dev"                     

            mov_files_path = self.task_path + f"/{pub_dev}/" + self.tab_name
            movs = os.listdir(mov_files_path)
            if not movs:
                h_header = self.mov_table.horizontalHeader()
                h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
                h_header.setSectionResizeMode(QHeaderView.Stretch)
                self.mov_table.setColumnCount(1)
                self.mov_table.setRowCount(1)
                self.mov_table.setShowGrid(False)
                       
                item = QTableWidgetItem()
                item.setText("EMPTY")
                
                # 테이블 폰트 사이즈 조절
                font  = QFont()
                font.setPointSize(40)
                item.setFont(font)
                
                # 아이템 클릭할 수 없게 만들기
                item.setFlags(Qt.NoItemFlags)
                self.mov_table.setItem(0,0,item)
                item.setTextAlignment(Qt.AlignCenter)
            
        else:
            return

        row = 0
        col = 0

        for mov in movs :
            
            mov_name = mov.split(".")[0]

            exr_file_path = self.task_path + "/dev/exr/" + mov_name
            image_path = os.path.join(exr_file_path, mov_name + ".1001.exr")
        
            if not os.path.isdir(f"{self.task_path}/.thumbnail/"):
                os.makedirs(f"{self.task_path}/.thumbnail/")   
                
            png_path = f"{self.task_path}/.thumbnail/{mov_name}.1001.png"  
             
            if not os.path.isfile(png_path):
                change_to_png(image_path,png_path)
            
            cell_widget = QWidget()
            layout = QVBoxLayout()
            
            label_img = QLabel()
            pixmap = QPixmap(png_path)
            label_img.setPixmap(pixmap) 
            label_img.setAlignment(Qt.AlignCenter)
            label_img.setScaledContents(True)
            
            label_text = QLabel()
            label_text.setText(mov)
            label_text.setAlignment(Qt.AlignCenter)
            label_text.setStyleSheet('font-size: 11px; color:rgb(211, 215, 207);')
            label_text.setWordWrap(True)
            
            layout.addWidget(label_img)
            layout.addWidget(label_text)
            layout.setContentsMargins(0,0,0,10)
            layout.setAlignment(Qt.AlignCenter)  
            cell_widget.setLayout(layout)
            
            item = QTableWidgetItem()
            item.setText(mov)
            self.mov_table.setItem(row, col, item)
            self.mov_table.setCellWidget(row,col,cell_widget)      
        
            col +=1
            
            # 갯수 맞춰서 다다음줄로
            if col >= self.mov_table.columnCount():            
                col = 0
                row += 2
    
    # all 파일
    def set_shot_all_files_listWidget(self):
        """
        dev 파일 다 긁어와서 list에 한번에 다 넣어주기 (중복 항목 제외)
        """
        self.all_list.clear()

        if not self.task_path:
            return
        
        dev_work_path = self.task_path + "/dev/work"
        dev_exr_path = self.task_path + "/dev/exr"
        dev_mov_path = self.task_path + "/dev/mov"

        
        work_files = os.listdir(dev_work_path)
        exr_folders = os.listdir(dev_exr_path)
        mov_files = os.listdir(dev_mov_path)
         
        for i,exr in enumerate(exr_folders):
            exr_folders[i] = exr+".exr"
            
        all_files = work_files + mov_files + exr_folders
        a = ",".join(all_files)

        existing_all_items = self.all_list.findItems(a, Qt.MatchExactly)
        
        if work_files not in existing_all_items:
            self.all_list.addItems(work_files)
        if exr_folders not in existing_all_items:
            self.all_list.addItems(exr_folders)
        if mov_files not in existing_all_items:
            self.all_list.addItems(mov_files)         
                       
    #=========================================================================================
    #    File Iformation Setting
    #==========================================================================================
    
    def input_work_information(self,selected_file):

        file_name,file_type = os.path.splitext(selected_file)
        
        desription = self.find_description_list(file_name)
        
        if self.tab_name == "all":
            selected_file = self.get_all_tab_file_path(selected_file,"work")
        else:
            selected_file = self.get_file_path(selected_file)
        
        
        size,time= File_data.file_info(selected_file)
        
        self.ui.label_shot_filename.setText(file_name)
        self.ui.label_shot_filetype.setText(file_type)
        self.ui.label_shot_framerange.setText("-")
        self.ui.label_shot_resolution.setText(self.resolution)
        self.ui.label_shot_savedtime.setText(time)
        self.ui.label_shot_filesize.setText(size)
        if not desription:
            desription = "No description"
        self.ui.plainTextEdit_shot_comment.setPlainText(desription)
        
    def set_work_file_information(self,item):
        
        selected_file = item.text()
        
        self.input_work_information(selected_file)

    def input_exr_information(self,selected_file):
        
        file_name, file_type = os.path.splitext(selected_file)
        
        desription = self.find_description_list(file_name)

        if self.tab_name == "all":
            selected_file = self.get_all_tab_file_path(file_name,"exr")
        else:
            selected_file = self.get_file_path(file_name)
            
        
        size,time= File_data.dir_info(selected_file)
        start,last,frame = ffmpeg_module.get_frame_count_from_directory(selected_file)
        
        frame_range = f"{start}-{last} {frame}"
    
        self.ui.label_shot_filename.setText(file_name)
        self.ui.label_shot_filetype.setText(".exr")
        self.ui.label_shot_framerange.setText(frame_range)
        self.ui.label_shot_resolution.setText(self.resolution)
        self.ui.label_shot_savedtime.setText(time)
        self.ui.label_shot_filesize.setText(size)
        if not desription:
            desription = "No description"
        self.ui.plainTextEdit_shot_comment.setPlainText(desription)
         
    def set_exr_file_information(self, item):
          
        selected_file = item.text()
        
        self.input_exr_information(selected_file)
   
    def input_mov_information(self,selected_file):
        file_name,file_type = os.path.splitext(selected_file)
        
        desription = self.find_description_list(file_name)
        
        if self.tab_name == "all":
            selected_file = self.get_all_tab_file_path(selected_file,"mov")
        else:
            selected_file = self.get_file_path(selected_file)
            
        
        size,time= File_data.file_info(selected_file)
        w,h,frame_range = ffmpeg_module.find_resolution_frame(selected_file)

        self.ui.label_shot_filename.setText(file_name)
        self.ui.label_shot_filetype.setText(file_type)
        self.ui.label_shot_framerange.setText(str(frame_range))
        self.ui.label_shot_resolution.setText(self.resolution)
        self.ui.label_shot_savedtime.setText(time)
        self.ui.label_shot_filesize.setText(size)
        if not desription:
            desription = "No description"
        self.ui.plainTextEdit_shot_comment.setPlainText(desription)
        
    def set_mov_file_information(self, item):
        """
        tableWidget에서 클릭한 파일의 정보 출력.
        """
        selected_file = item.text()
        
        self.input_mov_information(selected_file)

    def set_all_file_information (self,item):
        
        """
        listWidget에서 클릭한 파일 정보 출력.
        """
        selected_file = item.text()

        file_name, file_type = os.path.splitext(selected_file)
         
        if file_type == ".nknc":
            self.input_work_information(selected_file)
        elif file_type == ".mov":
            self.input_mov_information(selected_file)
        elif file_type == ".exr":
            self.input_exr_information(selected_file)

    def clear_file_info(self):
        self.ui.label_shot_filename.clear()
        self.ui.label_shot_filetype.clear()
        self.ui.label_shot_framerange.clear()
        self.ui.label_shot_resolution.clear()
        self.ui.label_shot_savedtime.clear()
        self.ui.label_shot_filesize.clear()
        self.ui.plainTextEdit_shot_comment.clear()

    def find_description_list(self,file_name):
            for comment in self.description_list:
                for shot_code , desription in comment.items():
                    if shot_code == file_name:
                        return desription

    def set_description_list(self):

            user_dic = self.open_loader_json()
            
            self.description_list = []
 
            versions = user_dic["project_versions"]
            for version in versions:
                version_dic = {}
                version_dic[version["version_code"]] = version["description"]
                self.description_list.append(version_dic)  
                
    def open_loader_json(self):
        with open("/home/rapa/yummy/pipeline/json/open_loader_datas.json","rt",encoding="utf-8") as r:
            user_dic = json.load(r)
        return user_dic
        
    #=========================================================================================
    # file_name으로 path 찾기
    #==========================================================================================
        
    def get_file_path (self,selected_file):
        """
        shot_tableWidget에서 클릭한 파일 path 획득
        """
        front_path = self.ui.label_shot_filepath.text()
        split_front_path = front_path.split("  ")[1]
         
        self.nuke_file_path = "/home/rapa/" + split_front_path + "/dev/" + self.tab_name + "/" + selected_file
        return self.nuke_file_path

    def get_all_tab_file_path(self,selected_file,file_type):
        
        front_path = self.ui.label_shot_filepath.text()
        split_front_path = front_path.split("  ")[1]
            
        self.nuke_file_path = "/home/rapa/" + split_front_path + "/dev/" + file_type + "/" + selected_file
        return self.nuke_file_path
     
    #=========================================================================================
    # vlc 연결
    #==========================================================================================
    def set_mov_files(self,item):
        """
        mov file setting
        """
        mov_files_path = self.task_path + "/" + "dev" + "/" f"{self.tab_name}"
        movs = item.text()

        mov_path = os.path.join(mov_files_path, movs)
        mov_play_path = 'vlc --repeat ' + f"{mov_path}"
        os.system(mov_play_path)
       
    #=========================================================================================
    # 검색 기능
    #==========================================================================================
     
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
     
    #=========================================================================================
    # 버튼 연결
    #==========================================================================================
    # def thread_load_nuke(self):
    #     thread_load = threading.Thread(target=self.load_nuke)
    #     thread_load.start()   
        
        
    def load_nuke (self):
        
        directory_path = os.path.dirname(self.nuke_file_path)
        task_type = directory_path.split("/")[-1]
        
        if task_type == "work":
            cmd_path = 'source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc ' + f"{self.nuke_file_path}"
            subprocess.Popen(cmd_path, shell=True,executable="/bin/bash")

        elif task_type == "mov":
            cmd_path = "xdg-open " + directory_path + "/"
            os.system(cmd_path)
            
        elif task_type == "exr":
            cmd_path = "xdg-open " + directory_path + "/"
            os.system(cmd_path)
            
    # def thread_load_new_nuke(self):
    #     thread_load_new = threading.Thread(target=self.load_new_nuke)
    #     thread_load_new.start()   
        
    def load_new_nuke(self):
        subprocess.Popen("source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc", shell=True,executable="/bin/bash")
        

     
    #=========================================================================================
    # 스테이터스 창
    #==========================================================================================    
     
    def set_status_table_list(self):
        tablename = ["ani","cmp","lgt","mm","ly"]
        self.task_table_widget = [getattr(self.ui, f"tableWidget_shot_{task}") for task in tablename]
        # self.sort_status_task()
        for task_table in self.task_table_widget:
            task_table.itemDoubleClicked.connect(partial(self.set_status_vlc,task_table))
    
    
    
    # 스터이스창 더블클릭시 mov 파일 실행되게
    def set_status_vlc(self,task_table,item):
        index = item.row()
        file_info = []
        for col in range(1,3):
            info = task_table.item(index,col)
            file_info.append(info.text())
        file_info.insert(1,self.st_tab_name)
        
        shot_code = file_info[0].split("_")[0]
        
        mov_name = "_".join(file_info)
        vlc_path = f"/home/rapa/YUMMY/project/{self.project}/seq/{shot_code}/{file_info[0]}/{file_info[1]}/dev/mov/{mov_name}.mov"
        
        subprocess.Popen(f"vlc --repeat {vlc_path}", shell=True,executable="/bin/bash")
    
    
    def sort_status_task(self):
        user_dic = self.open_loader_json()
        
        self.status_dic = {"ani":[],"cmp":[],"lgt":[],"mm":[],"ly":[]}
        
        task_list = user_dic["project_versions"]
        
        for status in task_list:
            if status["version_code"][0].isupper():
                shot_dic = {}
                shot_info = status["version_code"].split("_")
                task  = shot_info[2]
                
                shot_dic["Artist"] = status["artist"] 
                shot_dic["Shot Code"]  = "_".join([shot_info[0],shot_info[1]])
                shot_dic["Version"] = shot_info[-1] 
                shot_dic["Status"]  = status["sg_status_list"]
                shot_dic["Update Date"] = status["updated_at"]
                shot_dic["Description"] = status["description"]
                
                self.status_dic[task].append(shot_dic)
        
    def get_task_tab_name(self,tabindex):
        self.sort_status_task()
        
        if tabindex == 0 :
            self.st_tab_name = "ani"
            task_table = self.task_table_widget[0]
            status_list = self.status_dic["ani"]
                
        elif tabindex == 1 :
            self.st_tab_name = "cmp"
            task_table = self.task_table_widget[1]
            status_list = self.status_dic["cmp"]            

        elif tabindex == 2 :
            self.st_tab_name = "lgt"
            task_table = self.task_table_widget[2]
            status_list = self.status_dic["lgt"]
            
        elif tabindex == 4 :
            self.st_tab_name = "mm"
            task_table = self.task_table_widget[3]
            status_list = self.status_dic["mm"]
            
        elif tabindex == 3 :
            self.st_tab_name = "ly"
            task_table = self.task_table_widget[4]
            status_list = self.status_dic["ly"]
            
        self.set_status_table_1(task_table)
        self.input_status_table_1(status_list,task_table)
        
    def set_status_table_1(self,task_table):
        
        task_table.setColumnCount(6)
        task_table.setRowCount(8)
        
        task_table.setHorizontalHeaderLabels(["Artist","ShotCode", "Version","Status","Upadate Data" ,"Description"])
        
        task_table.setColumnWidth(0, 1020 * 0.14)
        task_table.setColumnWidth(1, 1020 * 0.13)
        task_table.setColumnWidth(2, 1020 * 0.1)
        task_table.setColumnWidth(3, 1020 * 0.05)
        task_table.setColumnWidth(4, 1020*  0.23)
        task_table.setColumnWidth(5, 1030 * 0.35)
        
        task_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        for row in range(task_table.rowCount()):
            task_table.setRowHeight(row,30)
            
        
        task_table.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        task_table.setShowGrid(True)
    
    def input_status_table_1(self,status_list,task_table):
        
        if not status_list:
            return
        status_list.sort(key=self.extract_time_shot,reverse = True)
        
        row = 0
        for status_info in status_list:
            col = 0
            for info in status_info.values():
                item = QTableWidgetItem()
                if col == 3:
                    if info == "wip":
                        label = QLabel()
                        # pixmap = QPixmap("/home/rapa/xgen/wip.png")
                        # scaled_pixmap = pixmap.scaled(20,20)
                        # label.setPixmap(scaled_pixmap)
                        gif_movie = QMovie("/home/rapa/YUMMY/pipeline/source/wip001.gif")
                        gif_movie.setScaledSize(QSize(80,60))# GIF 파일 경로 설정
                        label.setMovie(gif_movie)
                        gif_movie.start() 
                        label.setAlignment(Qt.AlignCenter)
                        task_table.setCellWidget(row, col, label)
                        
                    elif info == "pub":
                        label = QLabel()
                        # pixmap = QPixmap("/home/rapa/xgen/wip.png")
                        # scaled_pixmap = pixmap.scaled(20,20)
                        # label.setPixmap(scaled_pixmap)
                        gif_movie = QMovie("/home/rapa/YUMMY/pipeline/source/pub003.gif")
                        gif_movie.setScaledSize(QSize(100,50))# GIF 파일 경로 설정
                        label.setMovie(gif_movie)
                        gif_movie.start() 
                        label.setAlignment(Qt.AlignCenter)
                        task_table.setCellWidget(row, col, label)
                        
                    elif info == "fin" or info == "sc":
                        label = QLabel()
                        gif_movie = QMovie("/home/rapa/YUMMY/pipeline/source/pub002.gif")
                        gif_movie.setScaledSize(QSize(120,90))# GIF 파일 경로 설정
                        label.setMovie(gif_movie)
                        gif_movie.start() 
                        label.setAlignment(Qt.AlignCenter)
                        task_table.setCellWidget(row, col, label)
                                 
                else:
                    if not info:
                        info = "No description"
                    item.setText(info)
                    item.setTextAlignment(Qt.AlignCenter)
                    task_table.setItem(row,col,item)
                col += 1
            row += 1
    
    def extract_time_shot(self,item):
        return datetime.strptime(item['Update Date'], '%Y-%m-%d %H:%M:%S')
           
    def set_up(self):
        from loader_ui.main_window_v002_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication()
    my  = Mainloader()
    my.show()
    app.exec()