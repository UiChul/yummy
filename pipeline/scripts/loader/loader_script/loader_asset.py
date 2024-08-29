

from PySide6.QtWidgets import QApplication, QTableWidget, QLabel
from PySide6.QtWidgets import  QVBoxLayout, QWidget, QHeaderView
from PySide6.QtWidgets import QTableWidgetItem, QAbstractItemView, QSizePolicy
from PySide6.QtCore import Qt, QMimeData, QSize
from PySide6.QtGui import QDrag, QPixmap, QCursor
import os
import sys
sys.path.append("/home/rapa/yummy/pipeline/scripts/loader")

try:
    import nuke
except ImportError:
    nuke = None  # Nuke가 import되지 않은 경우를 대비

import json

# mod
class DraggableWidget_mod(QWidget):
    def __init__(self, file_path, image_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up the layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Create and add the image label
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)

        # 이미지 크기조절
        desired_size = QSize(400,320)  # 원하는 크기 (너비, 높이)
        scaled_pixmap = pixmap.scaled(desired_size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                                      Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(280, 188)  # Adjust size as needed
        self.image_label.setScaledContents(True)  # 이미지가 QLabel에 맞게 조정되도록 설정
        layout.addWidget(self.image_label)

        # Create and add the draggable label
        self.draggable_label = QLabel(os.path.basename(file_path))
        self.draggable_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.draggable_label.setFixedSize(280, 25)
        self.draggable_label.setStyleSheet(
                                           "font: 10pt;"
                                           )
        layout.addWidget(self.draggable_label)

        self.file_path = file_path

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Mouse Click Signal")
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.file_path) # Store file path in QMimeData
            drag.setMimeData(mime_data)
             # Set the drag cursor
            drag.setHotSpot(event.pos())
            drag.setPixmap(self.image_label.pixmap())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

            # Change cursor shape to indicate drag operation
            QApplication.setOverrideCursor(QCursor(Qt.DragCopyCursor))
        else:
            super().mousePressEvent(event)
            print("Mouse Click Signal")

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Restore the cursor shape
            QApplication.restoreOverrideCursor()
        super().mouseReleaseEvent(event)

class DroppableTableWidget_mod(QTableWidget):
    def __init__(self, rows, columns, *args, **kwargs):
        super().__init__(rows, columns, *args, **kwargs)
        self.setAcceptDrops(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        cell_width = 275 # Width of each cell in pixels
        cell_height = 215  # Height of each cell in pixels

        for column in range(columns):
            self.setColumnWidth(column, cell_width)
        for row in range(rows):
            self.setRowHeight(row, cell_height)

        self.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers) 

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

# rig
class DraggableWidget_rig(QWidget):
    def __init__(self, file_path, image_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up the layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Create and add the image label
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)

        # 이미지 크기조절
        desired_size = QSize(400,320)  # 원하는 크기 (너비, 높이)
        scaled_pixmap = pixmap.scaled(desired_size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                                      Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(280, 188)  # Adjust size as needed
        self.image_label.setScaledContents(True)  # 이미지가 QLabel에 맞게 조정되도록 설정
        layout.addWidget(self.image_label)

        # Create and add the draggable label
        self.draggable_label = QLabel(os.path.basename(file_path))
        self.draggable_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.draggable_label.setFixedSize(280, 25)
        self.draggable_label.setStyleSheet(
                                           "font: 10pt;"
                                           )
        layout.addWidget(self.draggable_label)

        self.file_path = file_path


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.file_path)  # Store file path in QMimeData
            drag.setMimeData(mime_data)

             # Set the drag cursor
            drag.setHotSpot(event.pos())
            drag.setPixmap(self.image_label.pixmap())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Restore the cursor shape
            QApplication.restoreOverrideCursor()
        super().mouseReleaseEvent(event)

class DroppableTableWidget_rig(QTableWidget):
    def __init__(self, rows, columns, *args, **kwargs):
        super().__init__(rows, columns, *args, **kwargs)
        self.setAcceptDrops(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        cell_width = 275 # Width of each cell in pixels
        cell_height = 215  # Height of each cell in pixels

        for column in range(columns):
            self.setColumnWidth(column, cell_width)
        for row in range(rows):
            self.setRowHeight(row, cell_height)
            

        self.setSizeAdjustPolicy(QTableWidget.AdjustToContentsOnFirstShow)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers) 

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


class Libraryasset():
    def __init__(self,Ui_Form):
        # super().__init__()
        self.ui = Ui_Form
        # self.set_up()

        # Main layout setup
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.make_json_dic()
        # Create QTableWidget
        self.table_widget_mod = DroppableTableWidget_mod(3,3)  # Initial size, will adjust dynamically
        self.table_widget_rig = DroppableTableWidget_rig(3,3)

        # Add QTableWidget to gridLayout_test
        if hasattr(self.ui, 'gridLayout_mod'):
            self.ui.gridLayout_mod.addWidget(self.table_widget_mod, 0, 0)  # Add at position (0, 0)
        if hasattr(self.ui, 'gridLayout_rig'):
            self.ui.gridLayout_rig.addWidget(self.table_widget_rig, 0, 0)  # Add at position (0, 0)

        self.set_asset_listWidget("character")
        # Load asset json files into the table
        self.set_asset_type_comboBox()
        
        self.load_asset_files_in_tableWidget_mod()
        self.load_asset_files_in_tableWidget_rig()

        
        self.ui.comboBox_asset_type.currentTextChanged.connect(self.set_asset_listWidget)
        self.ui.comboBox_asset_type.currentTextChanged.connect(self.load_asset_files_in_tableWidget_mod)
        self.ui.comboBox_asset_type.currentTextChanged.connect(self.load_asset_files_in_tableWidget_rig)
        
        self.table_widget_mod.itemClicked.connect(self.set_asset_information)
        

    def open_json_file (self):
        json_file_path = '/home/rapa/yummy/pipeline/json/open_loader_datas.json'
        with open(json_file_path,encoding='UTF-8') as file:
            datas = json.load(file)

        json_assets = datas['assets_with_versions']

        return json_assets

    def set_asset_type_comboBox(self):
            self.ui.comboBox_asset_type.clear()
            
            jsons = self.open_json_file()
            result = []
            for json in jsons:
                asset_type = json["asset_info"]["asset_type"]
                result.append(asset_type)

            asset_type_list = list(set(result))
            asset_type_list.sort()

            self.ui.comboBox_asset_type.addItems(asset_type_list)

            return asset_type_list
    
    def make_json_dic(self):
        with open("/home/rapa/yummy/pipeline/json/project_data.json","rt",encoding="utf-8") as r:
            info = json.load(r)
        
        self.project = info["project"]
        # self.user    = info["name"]
        # self.rank    = info["rank"]
        # self.resolution = info["resolution"]

    def set_asset_listWidget(self, asset_type = ""):
        if not asset_type:
            asset_type = self.ui.comboBox_asset_type.currentText()

        self.ui.listWidget_mod.clear()
        self.ui.listWidget_rig.clear()
        # self.asset_paths = ["mod"], ["rig"]

        jsons = self.open_json_file()

        for json in jsons:
            asset_name = json["asset_info"]["asset_name"]
            self.task_step = None
            
            task_details_dict = json["asset_info"]["task_details"]

            task_step = []

            if task_details_dict:
                for task_details in task_details_dict:
                    task_step.append(task_details["task_step"])

            if asset_type == json["asset_info"]["asset_type"]:
                if "mod" in task_step:
                    self.ui.listWidget_mod.addItem(asset_name)
                    # self.asset_paths["mod"] = f"{asset_path}/{asset_type}/mod/pub/"

                if "rig" in task_step:
                    self.ui.listWidget_rig.addItem(asset_name)
                    # self.asset_paths["rig"] = f"{asset_path}/{asset_type}/rig/pub/"

########################################################################################
# mod
    def load_asset_files_in_tableWidget_mod(self, current_asset_type=""):
        """
        Load all .abc files from the given folder path into the table widget,
        and set images from the image_path folder.
        """
        if not current_asset_type:
            current_asset_type = self.ui.comboBox_asset_type.currentText()

        self.table_widget_mod.clear()

        count_mod = self.ui.listWidget_mod.count()

        # Lists to store assets and corresponding thumbnail paths
        assets_in_listWidget = []
        thumbnails_path = []

        for i in range(count_mod):
            item_text = self.ui.listWidget_mod.item(i).text()
            assets_in_listWidget.append(item_text)
            thumbnail_path = f"/home/rapa/YUMMY/project/{self.project}/asset/.thumbnail/{current_asset_type}_rig_{item_text}_thumbnail.png"
            thumbnails_path.append(thumbnail_path)

        # print("assets_in_listWidget = ", assets_in_listWidget)
        jsons = self.open_json_file()

        # Initialize matched_asset_paths as a dictionary
        matched_asset_paths = {}

        for json in jsons:
            asset_name = json["asset_info"]["asset_name"]
            asset_type = json["asset_info"]["asset_type"]
            asset_full_path = json["asset_info"]["asset_path"] + "/mod/pub/" + asset_name
            # print ("asset_full_path = ",asset_full_path)

            if asset_name in assets_in_listWidget and asset_type == current_asset_type:
                matched_asset_paths[asset_name] = asset_full_path  # Store path using asset name as key

        # print("matching = ", matched_asset_paths)

        # Adjust table size to fit the number of assets
        # rows = (len(assets_in_listWidget) // 2) + (1 if len(assets_in_listWidget) % 2 else 0)
        self.table_widget_mod.setRowCount(3)
        self.table_widget_mod.setColumnCount(2)

        row = 0
        col = 0

        alembics = []  # List to store the full paths of alembic files
        for asset_name in assets_in_listWidget:
            # Fetch the corresponding path for the asset from the dictionary
            asset_path = matched_asset_paths.get(asset_name)
            if not asset_path:
                # print(f"No path found for asset {asset_name}")
                continue

            cache_folder_path = os.path.join(asset_path, "cache")
            # print("cache_folder", cache_folder_path)

            if os.path.exists(cache_folder_path) and os.path.isdir(cache_folder_path):
                file_names = os.listdir(cache_folder_path)
                # print("file_names =", file_names)

                # Collect all alembic file paths for the current asset
                for file_name in file_names:
                    alembic_full_file_path = os.path.join(cache_folder_path, file_name)
                    alembics.append(alembic_full_file_path)  # Add each file to the list

        # print("alembics", alembics)

        # Loop through alembics and thumbnails to create DraggableWidgets
        for index, (alembic, thumbnail) in enumerate(zip(alembics, thumbnails_path)):
            row = index // 2
            col = index % 2

            # Create DraggableWidget with correct paths
            draggable_widget_mod = DraggableWidget_mod(alembic, thumbnail)
            print(draggable_widget_mod)
            self.table_widget_mod.setCellWidget(row, col, draggable_widget_mod)
            # print("Added DraggableWidget", alembic, thumbnail)

    

# rig
#############################################################################################
    def load_asset_files_in_tableWidget_rig(self, current_asset_type=""):
        """
        Load all .abc files from the given folder path into the table widget,
        and set images from the image_path folder.
        """

        if not current_asset_type:
            current_asset_type = self.ui.comboBox_asset_type.currentText()

        self.table_widget_rig.clear()

        count_rig = self.ui.listWidget_rig.count()

        # Lists to store assets and corresponding thumbnail paths
        assets_in_listWidget = []
        thumbnails_path = []

        for i in range(count_rig):
            item_text = self.ui.listWidget_rig.item(i).text()
            assets_in_listWidget.append(item_text)
            thumbnail_path = f"/home/rapa/YUMMY/project/{self.project}/asset/.thumbnail/{current_asset_type}_rig_{item_text}_thumbnail.png"
            thumbnails_path.append(thumbnail_path)

        # print (len(assets_in_listWidget))
        # print (len(thumbnails_path))

        # print("assets_in_listWidget = ", assets_in_listWidget)
        jsons = self.open_json_file()

        # Initialize matched_asset_paths as a dictionary
        matched_asset_paths = {}

        for json in jsons:
            asset_name = json["asset_info"]["asset_name"]
            asset_type = json["asset_info"]["asset_type"]
            asset_full_path = json["asset_info"]["asset_path"] + "/rig/pub/" + asset_name

            if asset_name in assets_in_listWidget and asset_type == current_asset_type:
                matched_asset_paths[asset_name] = asset_full_path  # Store path using asset name as key

        # print("matching = ", matched_asset_paths)

        # Adjust table size to fit the number of assets
        # rows = (len(assets_in_listWidget) // 2) + (1 if len(assets_in_listWidget) % 2 else 0)
        self.table_widget_rig.setRowCount(3)
        self.table_widget_rig.setColumnCount(2)

        row = 0
        col = 0

        alembics = []  # List to store the full paths of alembic files
        for asset_name in assets_in_listWidget:
            # Fetch the corresponding path for the asset from the dictionary
            asset_path = matched_asset_paths.get(asset_name)
            if not asset_path:
                # print(f"No path found for asset {asset_name}")
                continue

            cache_folder_path = os.path.join(asset_path, "cache")
            # print("cache_folder", cache_folder_path)

            if os.path.exists(cache_folder_path) and os.path.isdir(cache_folder_path):
                file_names = os.listdir(cache_folder_path)
                # print("file_names =", file_names)

                # Collect all alembic file paths for the current asset
                for file_name in file_names:
                    # print ("000000000000000000000000000000",file_name)
                    alembic_full_file_path = os.path.join(cache_folder_path, file_name)
                    # print (alembic_full_file_path)
                    alembics.append(alembic_full_file_path)  # Add each file to the list
                    # print("Alembic File Path: ", alembic_full_file_path)

        # print("alembics", alembics)

        # Loop through alembics and thumbnails to create DraggableWidgets
        for index, (alembic, thumbnail) in enumerate(zip(alembics, thumbnails_path)):
            row = index // 2
            col = index % 2

            # Create DraggableWidget with correct paths
            draggable_widget_rig = DraggableWidget_rig(alembic, thumbnail)
            self.table_widget_rig.setCellWidget(row, col, draggable_widget_rig)
            # print("Added DraggableWidget", alembic, thumbnail)



##########################################################################################3
    def set_asset_information(self):
        # asset_name = item.text()
        print("Hello")
        # self.ui.label_asset_filename.setText(asset_name)
        # self.ui.label_asset_filetype.setText("abc")
        # 일단 informaiton 나머지 미완..~^^ ㅎ

    def set_up(self):
        from loader_ui.main_window_v002_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QApplication()  # Check if QApplication is already running
    window = Libraryasset()
    window.show()
    app.exec()