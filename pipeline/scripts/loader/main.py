from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QWidget,QApplication,QHeaderView
from PySide6.QtWidgets import QTreeWidgetItem, QTableWidgetItem, QLabel
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QAbstractItemView, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
import os

# from functools import partial

class Mainloader(QWidget):
    def __init__(self,info):
        super().__init__()
        self.set_up()
        
        self.project = info["project"]
        self.user = info["name"]
        
        self.set_main_laoder()
        self.set_comboBox_seq()
        
        self.shot_treeWidget = self.ui.treeWidget
        self.work_table = self.ui.tableWidget_shot_work
        self.exr_table = self.ui.tableWidget_shot_exr
        self.mov_table = self.ui.tableWidget_shot_mov
        self.all_list = self.ui.listWidget_shot_allfile

        self.set_treeWidget_shot("OPN")
        self.tab_name = "work"
        #Signal
        self.ui.comboBox_seq.currentTextChanged.connect(self.set_treeWidget_shot)
        self.shot_treeWidget.itemClicked.connect(self.get_clicked_treeWidget_shot_item)
        self.ui.pushButton_shot_nuke.clicked.connect(self.load_nuke)
        self.ui.tabWidget_shot_task.tabBarClicked.connect(self.get_tab_name)

        self.work_table.itemClicked.connect(self.get_work_mov_file_information)
        self.work_table.itemClicked.connect(self.get_clicked_nuke_file_path)
        self.exr_table.itemClicked.connect(self.get_exr_file_information)
        self.mov_table.itemClicked.connect(self.get_work_mov_file_information)
        self.mov_table.itemClicked.connect(self.set_mov_files)

        # tab - PUB 숨기기
        # self.ui.tabWidget_all.tabBar().setTabVisible(3, False)
        
    """
    seq
    """    
    def set_comboBox_seq(self):
        file_path = f"/home/rapa/YUMMY/project/{self.project}/seq"
        seq_list = os.listdir(file_path)
        self.ui.comboBox_seq.addItems(seq_list)
    
    """
    shot
    """
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

        self.task_path = self.file_path + "/" + parent_text + "/" + selected_task
        # print (self.task_path)
        split = self.task_path.split("/", 3)
        # print (split)
        splited_work_path = split[3]
        # print ("splited_work_path =",splited_work_path)
        label_work_path = "▶" + " " + splited_work_path 

        self.ui.label_shot_filepath.setText(label_work_path)

        self.set_shot_tableWidgets()
        self.set_shot_work_files_tableWidget()
        # self.set_shot_exr_files_tableWidget()

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

    def get_tab_name (self,tabIndex):
        if tabIndex == 0 :
            self.tab_name = "work"
            self.set_shot_work_files_tableWidget()

            
        elif tabIndex == 1 :
            self.tab_name = "exr"
            self.set_shot_exr_files_tableWidget()


        elif tabIndex == 2 :
            self.tab_name = "mov"
            self.set_mov_text_files()



        else :
            self.tab_name = "all"
            self.set_all_files_listWidget()
        # print (self.tab_name)

    
    """
    work
    """
    def set_shot_work_files_tableWidget(self):
        """
        work file setting
        """
        work_files_path = self.task_path + "/" + "dev" + "/" f"{self.tab_name}"
        works = os.listdir(work_files_path)
        # print (works)

        # table 에 image + text 삽입
        image_path = [
            "/home/rapa/xgen/images1.png",
            "/home/rapa/xgen/images2.png",
            "/home/rapa/xgen/images3.png"
        ]

        row = 0
        col = 0

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

    def get_clicked_nuke_file_path (self,item):
        """
        shot_tableWidget에서 클릭한 파일 path 획득
        """
        selected_file = item.text()
        front_path = self.ui.label_shot_filepath.text()
        split_front_path = front_path.split(" ")[1]
        
        self.nuke_file_path = " /home/rapa/" + split_front_path + "/dev/" + f"{self.tab_name}" + "/" + selected_file
        # print (self.nuke_file_path)

        
    """
    exr
    """
    def set_shot_exr_files_tableWidget(self):
        """
        exr file setting
        """
        # 폴더안에 들어가서 v001.png 넣어야함.
        # table 에 image + text 삽입

        exr_files_path = self.task_path + "/" + "dev" + "/" f"{self.tab_name}"
        exrs = os.listdir(exr_files_path)
        # print (exrs)

        row = 0
        col = 0

        for exr in exrs :
            exr_file_path = exr_files_path + "/" + exr
            image_path = os.path.join(exr_file_path, exr + ".1001.png")
            
            label_img = QLabel()
            pixmap = QPixmap(image_path)
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

    def get_exr_file_information(self, item):
        """
        tableWidget에서 클릭한 exr 폴더의 파일의 정보 출력.
        """
        selected_file = item.text()
        file_name, _ = os.path.splitext(selected_file)

        self.ui.label_shot_filename.setText(file_name)
        self.ui.label_shot_filetype.setText(".exr")
    

    """
    mov 영상파일 수정해야함 ::::::::::::;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    """
    def set_mov_text_files(self):
        """
        mov file setting
        """
        mov_files_path = self.task_path + "/" + "dev" + "/" f"{self.tab_name}"
        movs = os.listdir(mov_files_path)
        # print (movs)
        # print (mov_files_path)

        image_path = [
            "/home/rapa/xgen/MOV_File.png.png"
        ]

        row = 0
        col = 0

        # table 에 image + text 삽입

        for i, mov in enumerate(movs):

            version = image_path[i % len(image_path)]
            # print (version)

            item = QTableWidgetItem()
            item.setText(mov)
            self.mov_table.setItem(row+1,col,item)
            item.setTextAlignment(Qt.AlignCenter)

            if col + 1 < self.mov_table.columnCount():
            
                label_img = QLabel()
                pixmap = QPixmap(version)
                label_img.setPixmap(pixmap) 
                label_img.setAlignment(Qt.AlignCenter)
                label_img.setScaledContents(True)
                self.mov_table.setCellWidget(row,col+1,label_img)

            col +=1
            
            # 갯수 맞춰서 다다음줄로
            if col >= self.mov_table.columnCount():            
                col = 0
                row += 2

        # 홀수 row 행 높이 조절
        for i in range(1, self.mov_table.rowCount(), 2):
            self.mov_table.setRowHeight(i,50)        

    def set_mov_files(self):
        """
        mov file setting
        """
        mov_files_path = self.task_path + "/" + "dev" + "/" f"{self.tab_name}"
        movs = os.listdir(mov_files_path)

        row = 0
        col = 0
        for i, mov in enumerate(movs):
            mov_path = os.path.join(mov_files_path, mov)
            mov_play_path = 'vlc --repeat ' + f"{mov_path}"
            os.system(mov_play_path)

            video_widget = QVideoWidget()
            media_player = QMediaPlayer(video_widget)
            media_player.setSource(QUrl.fromLocalFile(mov_play_path))
            media_player.setVideoOutput(video_widget)

            video_layout = QVBoxLayout()
            video_layout.addWidget(video_widget)

            video_container = QWidget()
            video_container.setLayout(video_layout)

            self.mov_table.setCellWidget(row,col,video_container)
            media_player.play()

    
    """
    all
    """
    def set_all_files_listWidget(self):
        """
        dev 파일 다 긁어와서 list에 한번에 다 넣어주기
        """
        # print(self.task_path)
        dev_work_path = self.task_path + "/dev/work"
        dev_exr_path = self.task_path + "/dev/exr"
        dev_mov_path = self.task_path + "/dev/mov"

        work_files = os.listdir(dev_work_path)
        exr_folders = os.listdir(dev_exr_path)
        mov_files = os.listdir(dev_mov_path)
        
        for exr_folder in exr_folders:


            exr_folder_path = dev_exr_path + "/" + exr_folder
            print (exr_folder_path)



        print (work_files, mov_files)


        item = QTableWidgetItem()
        item.setText()
        # self.exr_table.setItem(row+1,col,item)
        # item.setTextAlignment(Qt.AlignCenter)



        




    def get_work_mov_file_information(self, item):
        """
        tableWidget에서 클릭한 파일의 정보 출력.
        """
        selected_file = item.text()
        # print (selected_file)

        file_name, _ = os.path.splitext(selected_file)
        _ , file_type = os.path.splitext(selected_file)
        # print(file_type)

        self.ui.label_shot_filename.setText(file_name)
        self.ui.label_shot_filetype.setText(file_type)
     
    def load_nuke (self):
        nuke_path = 'source /home/rapa/env/nuke.env && /mnt/project/Nuke15.1v1/Nuke15.1 --nc' + f"{self.nuke_file_path}"
        os.system(nuke_path)


        
    
    def set_main_laoder(self):
    
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
    my  = Mainloader(info)
    my.show()
    app.exec()