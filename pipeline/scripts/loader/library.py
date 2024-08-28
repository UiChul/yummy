
from PySide6.QtWidgets import QWidget, QHeaderView, QFileDialog, QTableWidget, QLabel
from PySide6.QtWidgets import QVBoxLayout, QLabel, QApplication, QTableWidgetItem
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QMimeData, QUrl, Qt
from PySide6.QtCore import Qt, QByteArray, QDataStream, QIODevice, QEvent
from PySide6.QtGui import QPixmap, Qt, QDrag, QClipboard

try:
    import nuke
except ImportError:
    nuke = None

    # from nukescripts import addDropDataCallback

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
        
        
        # self.clip_table = self.ui.tableWidget_clip_files

        self.asset_paths = {"mod" : None, "rig": None}
        
        self.set_user_information()
        # self.set_clip_files_text_table()

 
        # comboBox 일단 비활성화 해놓음
        self.ui.comboBox_seq.setEnabled(False)

        self.set_asset_listWidget("Character")
        self.set_asset_type_comboBox()
        self.set_tableWidget()
        self.input_asset_tableWidget_mod()
        self.input_asset_tableWidget_rig()

        
        #Signal
        self.ui.comboBox_asset_type.currentTextChanged.connect(self.set_asset_listWidget)
        self.ui.tableWidget_mod.cellClicked.connect(self.output_asset_path_tableWidget)
        self.ui.tableWidget_rig.cellClicked.connect(self.output_asset_path_tableWidget)

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

    # def open_json_file (self):
    #     json_file_path = '/home/rapa/YUMMY/pipeline/json/open_loader_datas.json'
    #     with open(json_file_path,encoding='UTF-8') as file:
    #         datas = json.load(file)

    #         json_assets = datas['assets_with_versions']

    #     return json_assets
    
    # def set_asset_type_comboBox(self):
    #     self.ui.comboBox_asset_type.clear()
        
    #     jsons = self.open_json_file()
    #     # print(jsons)
    #     result = []
    #     for json in jsons:
    #         asset_type = json["asset_info"]["asset_type"]
    #         result.append(asset_type)

    #     asset_type_list = list(set(result))
    #     asset_type_list.sort()

    #     self.ui.comboBox_asset_type.addItems(asset_type_list)

    #     # print(asset_type_list)
    #     return asset_type_list
    

    # def set_asset_listWidget(self, asset_type = ""):
    #     if not asset_type:
    #         asset_type = self.ui.comboBox_asset_type.currentText()

    #     self.ui.listWidget_mod.clear()
    #     self.ui.listWidget_rig.clear()


    #     jsons = self.open_json_file()

    #     for json in jsons:
    #         asset_name = json["asset_info"]["asset_name"]
    #         asset_path = json["asset_info"]["asset_path"]
    #         self.task_step = None
            
    #         task_details_dict = json["asset_info"]["task_details"]

    #         task_step = []

    #         if task_details_dict:
    #             for task_details in task_details_dict:
    #                 task_step.append(task_details["task_step"])
    #             # print ("step =" ,asset_name,task_step)

    #         if asset_type == json["asset_info"]["asset_type"]:
    #             if "mod" in task_step:
    #                 # print ("asset=",asset_name)
    #                 self.ui.listWidget_mod.addItem(asset_name)
    #                 self.asset_paths["mod"] = f"{asset_path}/{asset_type}/mod/pub/"

    #             if "rig" in task_step:
    #                 # print(f"Adding to Rig List: {asset_name}")
    #                 self.ui.listWidget_rig.addItem(asset_name)
    #                 self.asset_paths["rig"] = f"{asset_path}/{asset_type}/rig/pub/"

    #     self.input_asset_tableWidget_mod()
    #     self.input_asset_tableWidget_rig()
        


    # def set_tableWidget(self):

    #     tables = [self.ui.tableWidget_mod, self.ui.tableWidget_rig]
    #     for i in tables:
    #         h_header = i.horizontalHeader()
    #         h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
    #         h_header.setSectionResizeMode(QHeaderView.Stretch)
    #         i.setEditTriggers(QAbstractItemView.NoEditTriggers) 
    #         i.setColumnCount(2)
    #         i.setRowCount(6)
    #         i.setAcceptDrops(True)
    #         i.setDragEnabled(True)
    #         i.setDragDropMode(QAbstractItemView.DragDrop)
    #         i.setDefaultDropAction(Qt.CopyAction)
    #         i.installEventFilter(self)

    # def input_asset_tableWidget_mod(self):
    #     """
    #     click 한 asset 의 파일 path , json 에서 땡겨와서, tableWidget에 세팅
    #     """
    #     self.ui.tableWidget_mod.clear()
    #     row = 0
    #     col = 0

    #     count_mod = self.ui.listWidget_mod.count()
    #     count_rig = self.ui.listWidget_rig.count()
        
    #     # listWidget에 띄어진 items_text
    #     asset_lists = []
    #     thumbnails_path = []
    #     for i in range(count_mod):
    #         item_text = self.ui.listWidget_mod.item(i).text()
    #         asset_lists.append(item_text)

    #         thumbnail_path = f"/home/rapa/xgen/asset_thumbnail/asset_{item_text}_thumbnail.png"
    #         thumbnails_path.append(thumbnail_path)

    #     # print (asset_lists)
    #     # print (thumbnails_path)

    #     row = 0
    #     col = 0
    #     for image, asset_list in zip(thumbnails_path, asset_lists):
    #         cell_widget = QWidget()
    #         layout = QVBoxLayout()

    #         path = os.path.join(thumbnail_path,image)
    #         label_image = QLabel()
    #         pixmap = QPixmap(path)
    #         label_image.setPixmap(pixmap)
    #         label_image.setAlignment(Qt.AlignCenter)
    #         label_image.setScaledContents(True)

    #         label_text = QLabel()
    #         label_text.setText(asset_list)
    #         label_text.setStyleSheet(''' font-size: 12px; ''')
    #         label_text.setAlignment(Qt.AlignCenter)
    #         label_text.setWordWrap(True)

    #         layout.addWidget(label_image)
    #         layout.addWidget(label_text)
    #         layout.setContentsMargins(20,10,20,10)
    #         layout.setAlignment(Qt.AlignCenter)

    #         cell_widget.setLayout(layout)

    #         item = QTableWidgetItem(asset_list)
    #         item.setData(Qt.UserRole, os.path.join(self.asset_paths["mod"], asset_list))
    #         self.ui.tableWidget_mod.setItem(row, col, item)
    #         self.ui.tableWidget_mod.setCellWidget(row, col, cell_widget)

    #         self.reduce_item_visibility_in_tableWidget(row, col)
            
    #         col += 1  

    #         if col >= 3:
    #             col = 0
    #             row += 1

    # def input_asset_tableWidget_rig(self):
    #         """
    #         click 한 asset 의 파일 path , json 에서 땡겨와서, tableWidget에 세팅
    #         """
    #         self.ui.tableWidget_rig.clear()
            
    #         row = 0
    #         col = 0

    #         count_rig = self.ui.listWidget_rig.count()
            
    #         # listWidget에 띄어진 items_text
    #         asset_lists = []
    #         thumbnails_path = []
    #         for i in range(count_rig):
    #             item_text = self.ui.listWidget_rig.item(i).text()
    #             asset_lists.append(item_text)

    #             thumbnail_path = f"/home/rapa/xgen/asset_thumbnail/asset_{item_text}_thumbnail.png"
    #             thumbnails_path.append(thumbnail_path)

    #         # print (asset_lists)
    #         # print (thumbnails_path)

    #         row = 0
    #         col = 0
    #         for image, asset_list in zip(thumbnails_path, asset_lists):
    #             cell_widget = QWidget()
    #             layout = QVBoxLayout()

    #             path = os.path.join(thumbnail_path,image)
    #             label_image = QLabel()
    #             pixmap = QPixmap(path)
    #             label_image.setPixmap(pixmap)
    #             label_image.setAlignment(Qt.AlignCenter)
    #             label_image.setScaledContents(True)

    #             label_text = QLabel()
    #             label_text.setText(asset_list)
    #             label_text.setStyleSheet(''' font-size: 12px; ''')
    #             label_text.setAlignment(Qt.AlignCenter)
    #             label_text.setWordWrap(True)

    #             layout.addWidget(label_image)
    #             layout.addWidget(label_text)
    #             layout.setContentsMargins(20,10,20,10)
    #             layout.setAlignment(Qt.AlignCenter)

    #             cell_widget.setLayout(layout)

    #             self.ui.tableWidget_rig.setCellWidget(row,col,cell_widget)

    #             item = QTableWidgetItem(asset_list)
    #             item.setData(Qt.UserRole, os.path.join(self.asset_paths["rig"], asset_list))
    #             self.ui.tableWidget_rig.setItem(row, col, item)
    #             self.ui.tableWidget_rig.setCellWidget(row, col, cell_widget)

    #             self.reduce_item_visibility_in_tableWidget(row, col)

    #             col += 1  

    #             if col >= 3:
    #                 col = 0
    #                 row += 1

    # def reduce_item_visibility_in_tableWidget(self, row, col): 
    #     tables = self.ui.tableWidget_rig, self.ui.tableWidget_mod
    #     for table in tables:
    #         item = table.item(row, col)
    #         if item:
    #             item.setText('')
    #             font = item.font()
    #             font.setPointSize(1) 
    #             item.setFont(font)
        
    # def output_asset_path_tableWidget(self, row, col):

    #     item = self.ui.tableWidget_mod.item(row, col) 
    #     print (item)

    #     file_path = item.data(Qt.UserRole)
    #     print (file_path)

    #     return file_path



    
    """
    clip
    """

    # def set_clip_files_text_table (self):
    #     """
    #     이미지와 텍스트를 함께 포함하는 커스텀 QWidget생성.
    #     """


    #     # self.ui.tableWidget_mod.clear()
    #     file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib/"
    #     clip_lists = os.listdir(file_path)

    #     image_path = "/home/rapa/xgen/clip_thumbnail"
    #     images = os.listdir(image_path)

    #     count = (len(clip_lists) / 3)

        # h_header = self.clip_table.horizontalHeader()
        # h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        # h_header.setSectionResizeMode(QHeaderView.Stretch)
        # self.clip_table.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        # self.clip_table.setColumnCount(3)
        # self.clip_table.setRowCount(count+1)

        # row = 0
        # col = 0
        # for image, clip_list in zip(images, clip_lists):
        #     cell_widget = QWidget()
        #     layout = QVBoxLayout()

        #     path = os.path.join(image_path,image)
        #     label_image = QLabel()
        #     pixmap = QPixmap(path)
        #     label_image.setPixmap(pixmap)
        #     label_image.setAlignment(Qt.AlignCenter)
        #     label_image.setScaledContents(True)

        #     label_text = QLabel()
        #     label_text.setText(clip_list)
        #     label_text.setStyleSheet(''' font-size: 9px; ''')
        #     label_text.setAlignment(Qt.AlignCenter)
        #     label_text.setWordWrap(True)

        #     layout.addWidget(label_image)
        #     layout.addWidget(label_text)
        #     layout.setContentsMargins(20,5,20,10)
        #     layout.setAlignment(Qt.AlignCenter)

        #     cell_widget.setLayout(layout)

        #     self.clip_table.setCellWidget(row,col,cell_widget)  

        #     col += 1  

        #     if col >= 3:
        #         col = 0
        #         row += 1

        # return clip_lists


    # def import_clip_file_to_nuke (self,item):

    #     # make read node in nuke
    #     self.selected_item = item.text()
    #     file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib/{self.selected_item}"
    #     read_node = nuke.createNode('Read')
    #     nuke.connectViewer(0,read_node)
    #     read_node['file'].setValue(file_path)

    #     # frame resetting
    #     frame = self.get_frame_info(file_path)
    #     read_node['last'].setValue(frame)

    #     read_node['selected'].setValue(True)
 

    # def open_file_window(self):

    #     file_tuple = QFileDialog.getOpenFileName(self, "import nuke file", f"/home/rapa/YUMMY/project/{self.project}/seq/OPN/OPN_0010") 
    #     self.selected_nuke_file_path = file_tuple[0]
    #     print (self.selected_nuke_file_path)

    #     if self.selected_nuke_file_path:
    #         nuke_path = "/mnt/project/Nuke15.1v1/Nuke15.1"
    #         command = f'source /home/rapa/env/nuke.env && {nuke_path} --nc "{self.selected_nuke_file_path}"'
    #         os.system(command)


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
class DraggableWidget(QWidget):
    def __init__(self, image_path, asset_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_path = image_path
        self.asset_name = asset_name
        self.file_path = "/home/rapa/YUMMY/project/YUMMIE/template/asset/Character/mod/pub/man"

        layout = QVBoxLayout()

        label_image = QLabel()
        pixmap = QPixmap(self.image_path)
        label_image.setPixmap(pixmap)
        label_image.setAlignment(Qt.AlignCenter)
        label_image.setScaledContents(True)

        label_text = QLabel()
        label_text.setText(self.asset_name)
        label_text.setStyleSheet('''font-size: 12px;''')
        label_text.setAlignment(Qt.AlignCenter)
        label_text.setWordWrap(True)

        layout.addWidget(label_image)
        layout.addWidget(label_text)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.file_path)
            drag.setMimeData(mime_data)
            drag.exec_(Qt.CopyAction | Qt.MoveAction)
        else:
            super().mousePressEvent(event)

            # Encode widget information into mime data
            # data = QByteArray()
            # stream = QDataStream(data, QIODevice.WriteOnly)
            # stream.writeQString(self.asset_name)
            # stream.writeQString(self.image_path)


class DroppableTableWidget(QTableWidget):
    def __init__(self, rows, columns, *args, **kwargs):
        super().__init__(rows, columns, *args, **kwargs)
        self.setAcceptDrops(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            if nuke:
                self.apply_to_nuke(text)
            event.acceptProposedAction()
        else:
            event.ignore()

    def apply_to_nuke(self, text):
        if nuke:
            # Find or create a Read node
            read_nodes = [node for node in nuke.allNodes() if node.Class() == "Read"]
            if read_nodes:
                read_node = read_nodes[0]  # Use the first Read node found
            else:
                read_node = nuke.createNode('Read')

            # Set the 'file' path
            read_node['file'].setValue(text)

            # Optionally connect the Read node to the viewer
            nuke.connectViewer(0, read_node)

            # Provide feedback if no Read nodes were found initially
            if not read_nodes:
                nuke.message("A new Read node has been created and configured.")


info = {"project" : "Marvelous" , "name" : "su"}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win  = LibraryLoader()
    win.show()

    draggable_widget = DraggableWidget("path/to/image.png", "AssetName", LibraryLoader())
    app.exec()