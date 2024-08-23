
try:
    # from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QWidget,QApplication,QHeaderView
    from PySide6.QtWidgets import QTreeWidgetItem, QTableWidgetItem, QLabel
    from PySide6.QtWidgets import QAbstractItemView
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile
    from PySide6.QtGui import QPixmap, Qt

except:
    # from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QWidget,QApplication,QHeaderView
    from PySide2.QtWidgets import QTreeWidgetItem, QTableWidgetItem, QLabel
    from PySide2.QtWidgets import QAbstractItemView
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile
    from PySide2.QtGui import QPixmap, Qt
    # from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale, ...)


import os, sys
import ffmpeg
import nuke

class LibraryLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up()
        
        self.project = info["project"]
        self.user = info["name"]
        
        
        self.clip_table = self.ui.tableWidget_clip_files
        
        self.set_user_information()
        # self.set_asset_treeWidget()
        self.set_clip_files_text_table()
        self.render_for_thumbnails()

        # comboBox 일단 비활성화 해놓음
        self.ui.comboBox_seq.setEnabled(False)
        
        #Signal
        self.clip_table.itemClicked.connect(self.import_clip_file_to_nuke)


    
    """
    asset(cache)
    """
    def set_asset_treeWidget(self):
        pass
        # self.asset_tree.clear()
        # file_path = f"/home/rapa/YUMMY/project/{self.project}/asset"
        # asset_list = os.listdir(file_path)
    
        # # Headerlabel setting
        # self.asset_tree.setHeaderLabels([" Asset"])

        # # shot code setting
        # for asset_item in asset_list:
        #     parent_item = QTreeWidgetItem(self.asset_tree)
        #     parent_item.setText(0, asset_item)

        # # task setting
        #     self.task_path = f"/home/rapa/YUMMY/project/{self.project}/asset/{asset_item}"
        #     tasks = os.listdir(self.task_path)

        #     for task in tasks :
        #         task_item = QTreeWidgetItem(parent_item)
        #         task_item.setText(0,task)

    
    """
    clip
    """
    def set_clip_files_text_table (self):
        self.clip_table.clear()
        file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib"
        clip_lists = os.listdir(file_path)

        count = (len(clip_lists) / 3)
        # print (count)

        h_header = self.clip_table.horizontalHeader()
        h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(QHeaderView.Stretch)
        self.clip_table.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        self.clip_table.setColumnCount(3)

        if not count / 2 == 0 :
            self.clip_table.setRowCount((count+1) *2)
        else:
            self.clip_table.setRowCount(count+1)

        row = 1
        col = 0
        for clip_list in clip_lists:
            # print (clip_list)
            item = QTableWidgetItem()
            item.setText(clip_list)
            item.setTextAlignment(Qt.AlignCenter)
            self.clip_table.setItem(row,col,item)

            col += 1

            if col >= self.clip_table.columnCount():            
                col = 0
                row += 2

        # 홀수 row 행 높이 조절
        for i in range(1, self.clip_table.rowCount(), 2):
            self.clip_table.setRowHeight(i,50)        

        return clip_lists

    def import_clip_file_to_nuke (self,item):
        a = self.set_clip_files_text_table

        # make read node in nuke
        selected_item = item.text()
        file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib/{selected_item}"
        read_node = nuke.createNode('Read')
        nuke.connectViewer(0,read_node)
        read_node['file'].setValue(file_path)

        # frame resetting
        frame = self.get_frame_info(file_path)
        read_node['last'].setValue(frame)

        read_node['selected'].setValue(True)


    def render_for_thumbnails(self):
        # 테이블에 있는 모든 파일을 노드로 만들기
        file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib"
        clip_files = os.listdir(file_path)
        # print (clip_files)

        for clip_file in clip_files:
            clip_file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib/{clip_file}"
            read_node = nuke.createNode('Read')
            nuke.connectViewer(0,read_node)
            read_node['file'].setValue(clip_file_path)

            frame = self.get_frame_info(file_path)
            read_node['last'].setValue(frame)
            middle_frame = int(frame/2)

            read_node['selected'].setValue(True)

            read_node = nuke.toNode() 
            #render center_frame

            read_node.setInput(0,write_node)
            png_path = clip_file_path + f"/{clip_file}.png"
            write_node = nuke.createNode('Write')
            write_node['file'].setValue(png_path)
            write_node['first'].setValue(middle_frame)
            write_node['last'].setValue(middle_frame)

            write_node['selected'].setValue(True)
            nuke.execute(write_node,middle_frame,middle_frame)

            


        # read_node['selected'].setValue(True)
        # read_node['']



                





    def get_frame_info(self,input):
        probe = ffmpeg.probe(input)
        video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)

        if input.split(".")[-1] == "mov" or input.split(".")[-1] == "mp4":
            frame = int(video_stream['nb_frames'])
        else:
            frame = 0

        return frame



        




    













    def set_user_information(self):

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
    app = QApplication(sys)
    win  = LibraryLoader()
    win.show()
    app.exec()