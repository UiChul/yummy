

from PySide6.QtWidgets import QApplication, QTableWidget, QLabel
from PySide6.QtWidgets import  QVBoxLayout, QWidget, QHeaderView
from PySide6.QtWidgets import QTableWidgetItem, QAbstractItemView
from PySide6.QtCore import Qt, QMimeData, QSize
from PySide6.QtGui import QDrag, QPixmap, QCursor
import os
import sys
sys.path.append("/home/rapa/yummy/pipeline/scripts/loader/drag_drop")

try:
    import nuke
except ImportError:
    nuke = None  # Nuke가 import되지 않은 경우를 대비

import json

class DraggableWidget(QWidget):
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

            # Change cursor shape to indicate drag operation
            QApplication.setOverrideCursor(QCursor(Qt.DragCopyCursor))

        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Restore the cursor shape
            QApplication.restoreOverrideCursor()
        super().mouseReleaseEvent(event)

class DroppableTableWidget(QTableWidget):
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
class LibraryLoader_rig(QWidget):
    def __init__(self):
        super().__init__()

        self.set_up()

        # Main layout setup
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Create QTableWidget
        self.table_widget = DroppableTableWidget(3,3)  # Initial size, will adjust dynamically

        # Add QTableWidget to gridLayout_test
        if hasattr(self.ui, 'gridLayout_rig'):
            self.ui.gridLayout_rig.addWidget(self.table_widget, 0, 0)  # Add at position (0, 0)


        self.set_asset_listWidget("character")
        # Load asset json files into the table
        self.set_asset_type_comboBox()
        self.load_asset_files_in_tableWidget()

        self.ui.comboBox_asset_type.currentTextChanged.connect(self.set_asset_listWidget)
        self.ui.comboBox_asset_type.currentTextChanged.connect(self.load_asset_files_in_tableWidget)
        


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

    def set_asset_listWidget(self, asset_type = ""):
        if not asset_type:
            asset_type = self.ui.comboBox_asset_type.currentText()
        # print ("asset_type0",asset_type)

        self.ui.listWidget_mod.clear()
        self.ui.listWidget_rig.clear()

        jsons = self.open_json_file()

        for json in jsons:
            asset_name = json["asset_info"]["asset_name"]
            self.task_step = None
            
            task_details_dict = json["asset_info"]["task_details"]

            task_step = []

            if task_details_dict:
                for task_details in task_details_dict:
                    task_step.append(task_details["task_step"])
                # print ("step =" ,asset_name,task_step)

            if asset_type == json["asset_info"]["asset_type"]:
                if "mod" in task_step:
                    # print ("asset=",asset_name)
                    self.ui.listWidget_mod.addItem(asset_name)
                    # self.asset_paths["mod"] = f"{asset_path}/{asset_type}/mod/pub/"

                if "rig" in task_step:
                    # print(f"Adding to Rig List: {asset_name}")
                    self.ui.listWidget_rig.addItem(asset_name)
                    # self.asset_paths["rig"] = f"{asset_path}/{asset_type}/rig/pub/"


    def load_asset_files_in_tableWidget(self, current_asset_type=""):
        """
        Load all .abc files from the given folder path into the table widget,
        and set images from the image_path folder.
        """

        if not current_asset_type:
            current_asset_type = self.ui.comboBox_asset_type.currentText()

        self.table_widget.clear()

        count_rig = self.ui.listWidget_rig.count()

        # Lists to store assets and corresponding thumbnail paths
        assets_in_listWidget = []
        thumbnails_path = []

        for i in range(count_rig):
            item_text = self.ui.listWidget_rig.item(i).text()
            assets_in_listWidget.append(item_text)
            thumbnail_path = f"/home/rapa/YUMMY/project/asset_thumbnail/{current_asset_type}_rig_{item_text}_thumbnail.png"
            thumbnails_path.append(thumbnail_path)

        print("assets_in_listWidget = ", assets_in_listWidget)
        jsons = self.open_json_file()

        # Initialize matched_asset_paths as a dictionary
        matched_asset_paths = {}

        for json in jsons:
            asset_name = json["asset_info"]["asset_name"]
            asset_type = json["asset_info"]["asset_type"]
            asset_full_path = json["asset_info"]["asset_path"] + "/rig/pub/" + asset_name

            if asset_name in assets_in_listWidget and asset_type == current_asset_type:
                matched_asset_paths[asset_name] = asset_full_path  # Store path using asset name as key

        print("matching = ", matched_asset_paths)

        # Adjust table size to fit the number of assets
        rows = (len(assets_in_listWidget) // 3) + (1 if len(assets_in_listWidget) % 3 else 0)
        self.table_widget.setRowCount(rows * 3)
        self.table_widget.setColumnCount(2)

        row = 0
        col = 0

        alembics = []  # List to store the full paths of alembic files
        for asset_name in assets_in_listWidget:
            # Fetch the corresponding path for the asset from the dictionary
            asset_path = matched_asset_paths.get(asset_name)
            if not asset_path:
                print(f"No path found for asset {asset_name}")
                continue

            cache_folder_path = os.path.join(asset_path, "cache")
            print("cache_folder", cache_folder_path)

            if os.path.exists(cache_folder_path) and os.path.isdir(cache_folder_path):
                file_names = os.listdir(cache_folder_path)
                print("file_names =", file_names)

                # Collect all alembic file paths for the current asset
                for file_name in file_names:
                    alembic_full_file_path = os.path.join(cache_folder_path, file_name)
                    alembics.append(alembic_full_file_path)  # Add each file to the list
                    print("Alembic File Path: ", alembic_full_file_path)

        print("alembics", alembics)

        # Loop through alembics and thumbnails to create DraggableWidgets
        for index, (alembic, thumbnail) in enumerate(zip(alembics, thumbnails_path)):
            row = index // 3
            col = index % 3

            # Create DraggableWidget with correct paths
            draggable_widget = DraggableWidget(alembic, thumbnail)
            self.table_widget.setCellWidget(row, col, draggable_widget)
            print("Added DraggableWidget", alembic, thumbnail)
 



    def reduce_item_visibility_in_tableWidget(self, row, col): 

        item = self.table_widget.item(row, col)
        if item:
            item.setText('')
            font = item.font()
            font.setPointSize(1) 
            item.setFont(font)

    def set_up(self):
        from main_window_v002_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
if __name__ == '__main__':
    app = QApplication.instance()  # Check if QApplication is already running
    if not app:
        app = QApplication(sys.argv)

    window = LibraryLoader_rig()
    window.show()

    sys.exit(app.exec())