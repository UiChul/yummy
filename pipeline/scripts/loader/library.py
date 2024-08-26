
try:
    # from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QWidget,QHeaderView,QFileDialog
    from PySide6.QtWidgets import QVBoxLayout, QTableWidgetItem, QLabel, QApplication
    from PySide6.QtWidgets import QAbstractItemView
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile, QMimeData, QUrl
    from PySide6.QtGui import QPixmap, Qt, QDrag

except:
    # from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QWidget,QHeaderView,QFileDialog
    from PySide2.QtWidgets import QVBoxLayout, QTableWidgetItem, QLabel, QApplication
    from PySide2.QtWidgets import QAbstractItemView
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile, QMimeData, QUrl
    from PySide2.QtGui import QPixmap, Qt, QDrag
    # from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale, ...)

    import nuke

    from nukescripts import addDropDataCallback

import os, sys
import json

import ffmpeg
import ffmpeg_change_codec

import subprocess

class LibraryLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up()
        
        self.project = info["project"]
        self.user = info["name"]
        
        
        self.clip_table = self.ui.tableWidget_clip_files

        
        self.set_user_information()
        self.set_clip_files_text_table()

 
        # comboBox 일단 비활성화 해놓음
        self.ui.comboBox_seq.setEnabled(False)

        self.set_asset_listWidget("Character")
        self.set_asset_type_comboBox()


        
        #Signal
        self.ui.comboBox_asset_type.currentTextChanged.connect(self.set_asset_listWidget)
        # self.clip_table.itemClicked.connect(self.set_clip_files_text_table)
        # self.clip_table.itemClicked.connect(self.import_clip_file_to_nuke)
        # self.ui.pushButton_clip_file_nuke.clicked.connect(self.open_file_window)
        self.ui.listWidget_mod.itemClicked.connect(self.set_asset_tableWidget)
        self.ui.listWidget_rig.itemClicked.connect(self.set_asset_tableWidget)
        # self.ui.listWidget_temp.itemClicked.connect(self.set_asset_tableWidget)

        # self.clip_table.itemClicked.connect(self.open_file_window)

        # self.clip_table.setAcceptDrops(True)
        # self.clip_table.setDragEnabled(True) 
        # self.clip_table.setDropIndicatorShown(True)  

        # file_path = "/home/rapa/YUMMY/project/Marvelous/asset/Prop/rig/pub/turntable/cache/turntable.abc"

        # read_geo_node =  nuke.createNode('ReadGeo')
        # read_geo_node['file'].setValue(file_path)

        
    
    """
    asset(cache)
    """
    # def set_asset_type_comboBox (self):
    #     self.ui.comboBox_asset_type.clear()
    #     asset_type_path = f"/home/rapa/YUMMY/project/{self.project}/asset"
    #     asset_type_list = os.listdir(asset_type_path)
    #     self.ui.comboBox_asset_type.addItems(asset_type_list)

    #     return asset_type_path

    def open_json_file (self):
        json_file_path = '/home/rapa/YUMMY/pipeline/json/open_loader_datas.json'
        with open(json_file_path,encoding='UTF-8') as file:
            datas = json.load(file)

            json_assets = datas['assets_with_versions']

        return json_assets
    
    def set_asset_type_comboBox(self):
        self.ui.comboBox_asset_type.clear()
        
        jsons = self.open_json_file()
        # print(jsons)
        result = []
        for json in jsons:
            asset_type = json["asset_info"]["asset_type"]
            result.append(asset_type)

        asset_type_list = list(set(result))
        asset_type_list.sort()

        self.ui.comboBox_asset_type.addItems(asset_type_list)

        # print(asset_type_list)
        return asset_type_list
    
            

    
    def set_asset_listWidget(self,clicked_asset_type = ""):

        asset_type = self.ui.comboBox_asset_type.currentText()
        self.ui.listWidget_mod.clear()
        self.ui.listWidget_rig.clear()



        # print (clicked_asset_type)

        jsons = self.open_json_file()
        for json in jsons:
            asset_name = json["asset_info"]["asset_name"]
            asset_path = json["asset_info"]["asset_path"]
            self.task_step = None
            
            task_details_dict = json["asset_info"]["task_details"]

            task_step = []

            if task_details_dict:
                for task_details in task_details_dict:
                    task_step.append(task_details["task_step"])
                # print ("step =" ,asset_name,task_step)

            if clicked_asset_type == json["asset_info"]["asset_type"]:
                if "mod" in task_step:
                    # print ("asset=",asset_name)
                    self.ui.listWidget_mod.addItem(asset_name)
                    mod_full_path = asset_path + "/" + asset_type + "/" + "mod" + "/pub/" 

                if "rig" in task_step:
                    # print(f"Adding to Rig List: {asset_name}")
                    self.ui.listWidget_rig.addItem(asset_name)
                    rig_full_path = asset_path + "/" + asset_type + "/" + "rig" + "/pub/" 

                return mod_full_path, rig_full_path




    def set_asset_tableWidget(self, item):
        """
        click 한 asset 의 파일 path , json 에서 땡겨와서, tableWidget에 세팅
        """

        clicked_asset = item.text()
        print (clicked_asset)


        # jsons = self.open_json_file()

        # for json in jsons:
        #     asset_name = json["asset_info"]["asset_name"]   
        #     asset_path = json["asset_info"]["asset_path"]
        #     task_details_dict = json["asset_info"]["task_details"]
            
        #     task_step = []

        #     if task_details_dict:
        #         for task_details in task_details_dict:
        #             task_step.append(task_details["task_step"])
                    
        #     if "mod" in task_step :
        #         asset_full_path = asset_path + "/" + asset_type + "/" + "mod" + "/pub/" + clicked_asset

        #     if "rig" in task_step :
        #         asset_full_path = asset_path + "/" + asset_type + "/" + "rig" + "/pub/" + clicked_asset

        # print (asset_full_path)

            

            # if clicked_asset == asset_name:
            #     print (asset_path)


        # jsons = self.open_json_file()
        # asset_type_list = self.set_asset_type_comboBox()
        # for asset_type in asset_type_list:
        #     print (asset_type)

        # # print (asset_path)

        # asset_type_path = asset_path + "/" + asset_type + "/" + self.task_step + "/pub/" + asset
        # print (asset_type_path) 
        

            
    # def set_asset_listWidget(self,asset_name):
    #     self.ui.listWidget_mod.clear()
    #     self.ui.listWidget_rig.clear()
    #     self.ui.listWidget_temp.clear()

    #     json_file_path = '/home/rapa/YUMMY/pipeline/json/open_loader_datas.json'

    #     with open(json_file_path,encoding='UTF-8') as file:
    #         datas = json.load(file)

    #         json_assets = datas['assets']

    #         for json_asset_name in json_assets:

    #             if json_asset_name['task_details'] :
    #                 task_details_dict = json_asset_name['task_details'][0]
    #                 # print (task_details_dict)
                
    #                 if 'task_step' in task_details_dict :
    #                     task_step_value = task_details_dict['task_step']
    #                     # print (task_step_value)
    #             # print (json_asset_name["asset_type"])

    #             asset_type_path = self.set_asset_type_comboBox()
    #             asset_name = json_asset_name['asset_name']
    #             asset_type = json_asset_name["asset_type"]
    #             task_step = task_step_value

    #             file_path = asset_type_path + "/" + asset_type + "/" + task_step + "/pub/" + asset_name 
    #             print (file_path)

            
    #             if task_step == "mod" :
    #                 self.ui.listWidget_mod.addItem(json_asset_name['asset_name'])

    #             elif task_step == "rig" :
    #                 self.ui.listWidget_rig.addItem(json_asset_name['asset_name'])

    #             elif task_step == "N/A" :
    #                 self.ui.listWidget_temp.addItem(json_asset_name['asset_name'])

                    


    # def set_asset_tableWidget(self,item):
    #     asset = item.text()
    #     asset_type_path = self.set_asset_type_comboBox()
    #     asset_name = self.ui.comboBox_asset_type.currentText()
    #     print (asset_name)

    #     index = item.currentIndex()
    #     print (index)

    #     asset_path = asset_type_path + '/' + asset_name
    #     print (asset_path)
        # asset_list = os.listdir(asset)
        # print (asset_list)

        # self.ui.tableWidget_mod.setItem()



        

        
        
        

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
    def drag_drop(self):
        pass


    def set_clip_files_text_table (self):
        """
        이미지와 텍스트를 함께 포함하는 커스텀 QWidget생성.
        """


        # self.clip_table.clear()
        file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib/"
        clip_lists = os.listdir(file_path)

        image_path = "/home/rapa/xgen/clip_thumbnail"
        images = os.listdir(image_path)

        count = (len(clip_lists) / 3)

        h_header = self.clip_table.horizontalHeader()
        h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(QHeaderView.Stretch)
        self.clip_table.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        self.clip_table.setColumnCount(3)
        self.clip_table.setRowCount(count+1)

        row = 0
        col = 0
        for image, clip_list in zip(images, clip_lists):
            cell_widget = QWidget()
            layout = QVBoxLayout()

            path = os.path.join(image_path,image)
            label_image = QLabel()
            pixmap = QPixmap(path)
            label_image.setPixmap(pixmap)
            label_image.setAlignment(Qt.AlignCenter)
            label_image.setScaledContents(True)

            label_text = QLabel()
            label_text.setText(clip_list)
            label_text.setStyleSheet(''' font-size: 9px; ''')
            label_text.setAlignment(Qt.AlignCenter)
            label_text.setWordWrap(True)

            layout.addWidget(label_image)
            layout.addWidget(label_text)
            layout.setContentsMargins(20,5,20,10)
            layout.setAlignment(Qt.AlignCenter)

            cell_widget.setLayout(layout)

            self.clip_table.setCellWidget(row,col,cell_widget)  

            col += 1  

            if col >= 3:
                col = 0
                row += 1

        return clip_lists


    def import_clip_file_to_nuke (self,item):

        # make read node in nuke
        self.selected_item = item.text()
        file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib/{self.selected_item}"
        read_node = nuke.createNode('Read')
        nuke.connectViewer(0,read_node)
        read_node['file'].setValue(file_path)

        # frame resetting
        frame = self.get_frame_info(file_path)
        read_node['last'].setValue(frame)

        read_node['selected'].setValue(True)
 
    def open_file_window(self):

        file_tuple = QFileDialog.getOpenFileName(self, "import nuke file", f"/home/rapa/YUMMY/project/{self.project}/seq/OPN/OPN_0010") 
        self.selected_nuke_file_path = file_tuple[0]
        print (self.selected_nuke_file_path)

        if self.selected_nuke_file_path:
            nuke_path = "/mnt/project/Nuke15.1v1/Nuke15.1"
            command = f'source /home/rapa/env/nuke.env && {nuke_path} --nc "{self.selected_nuke_file_path}"'
            os.system(command)


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



"""
drag & drop
"""
    # def startDrag(self, supportedActions):
    #     # 선택된 아이템 가져오기
    #     item = self.tableWidget.currentItem()
    #     if item:
    #         drag = QDrag(self)
    #         mimeData = QMimeData()

    #         # 드래그할 파일 생성
    #         file_path = "/home/rapa/YUMMY/project/Marvelous/template/shot/clip_lib/OpenfootageNET_00268_Fluid_lowres.mov"
    #         mimeData.setUrls([QUrl.fromLocalFile(file_path)])
    #         drag.setMimeData(mimeData)

    #         # 드래그 시작
    #         drag.exec_(supportedActions)

    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasUrls():
    #         event.acceptProposedAction()
    #     else:
    #         event.ignore()

    # def dropEvent(self, event):
    #     if event.mimeData().hasUrls():
    #         urls = event.mimeData().urls()
    #         for url in urls:
    #             print(f"Dropped file: {url.toLocalFile()}")
    #         event.acceptProposedAction()
    #     else:
    #         event.ignore()
        

info = {"project" : "Marvelous" , "name" : "su"}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win  = LibraryLoader()
    win.show()
    app.exec()