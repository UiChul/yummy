

from PySide6.QtWidgets import QApplication, QTableWidget, QLabel, QVBoxLayout, QWidget, QHeaderView, QGridLayout
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QPixmap
import os
import sys
sys.path.append("/home/rapa/yummy/pipeline/scripts/loader")

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
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(300, 140)  # Adjust size as needed
        layout.addWidget(self.image_label)

        # Create and add the draggable label
        self.draggable_label = QLabel(os.path.basename(file_path))
        self.draggable_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.draggable_label.setFixedSize(300, 25)
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
            drag.exec_(Qt.CopyAction | Qt.MoveAction)
        else:
            super().mousePressEvent(event)

class DroppableTableWidget(QTableWidget):
    def __init__(self, rows, columns, *args, **kwargs):
        super().__init__(rows, columns, *args, **kwargs)
        self.setAcceptDrops(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)


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







class LibraryLoader(QWidget):
    def __init__(self):
        super().__init__()

        self.set_up()

        # Main layout setup
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Create QTableWidget
        self.table_widget = DroppableTableWidget(2,2)  # Initial size, will adjust dynamically

        # Add QTableWidget to gridLayout_test
        if hasattr(self.ui, 'gridLayout_mod'):
            self.ui.gridLayout_mod.addWidget(self.table_widget, 0, 0)  # Add at position (0, 0)


        self.set_asset_listWidget("Character")
        self.set_asset_type_comboBox()

        self.ui.comboBox_asset_type.currentTextChanged.connect(self.set_asset_listWidget)




        # Load asset json files into the table

        jsons = self.open_json_file()


        for json in jsons:
            asset_path = json["asset_info"]["asset_path"]

        print (asset_path)

        self.load_asset_files_in_tableWidget(asset_path, "/home/rapa/YUMMY/project/YUMMIE/asset/weapon/asset_thumbnail")

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

        self.ui.listWidget_mod.clear()
        self.ui.listWidget_rig.clear()


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

            if asset_type == json["asset_info"]["asset_type"]:
                if "mod" in task_step:
                    # print ("asset=",asset_name)
                    self.ui.listWidget_mod.addItem(asset_name)
                    # self.asset_paths["mod"] = f"{asset_path}/{asset_type}/mod/pub/"

                if "rig" in task_step:
                    # print(f"Adding to Rig List: {asset_name}")
                    self.ui.listWidget_rig.addItem(asset_name)
                    # self.asset_paths["rig"] = f"{asset_path}/{asset_type}/rig/pub/"





    def load_asset_files_in_tableWidget(self, json_path, image_path):
        """
        Load all .mov files from the given folder path into the table widget,
        and set images from the image_path folder.
        """
        count_mod = self.ui.listWidget_mod.count()

        asset_lists = []
        thumbnails_path = []
        for i in range(count_mod):
            item_text = self.ui.listWidget_mod.item(i).text()
            asset_lists.append(item_text)

            thumbnails_path = f"/home/rapa/asset_thumbnail/asset_{item_text}_thumbnail.png"

#여기서부터 하면됨. library 176번째 줄부터 참고 

        # Get a list of all .mov files in the directory
        # result = []
        # jsons = self.open_json_file()
        # for json in jsons :

        #     asset_name = json["asset_info"]["asset_name"]
        #     asset_type = json["asset_info"]["asset_type"]
        #     # result.append(asset_type)
        #     task_details_dict = json["asset_info"]["task_details"]

        #     task_step = []

        #     if task_details_dict:
        #         for task_details in task_details_dict:
        #             task_step.append(task_details["task_step"])
        #         # print ("step =" ,asset_name,task_step)

        #     print (asset_name)
        #     print ("asset_type=", asset_type)
        #     # print ("result=", result)
        #     print (task_step)

        # asset_type_list = list(set(result))
        # asset_type_list.sort()


        # # Get a list of all image files in the directory
        # images = []
        # for f in os.listdir(image_path):
        #     if f.lower().endswith(('.png', '.jpg', '.jpeg')):
        #         images.append(f)
        
        # # Adjust table size to fit the number of files
        # rows = (len(mov_files) // 3) + (1 if len(mov_files) % 3 else 0)
        # self.table_widget.setRowCount(rows)
        # self.table_widget.setColumnCount(3)

        # # Populate table with DraggableWidgets
        # for index, file_name in enumerate(mov_files):
        #     row = index // 3
        #     col = index % 3
        #     file_path = os.path.join(folder_path, file_name)

        #     # Create and set the image path
        #     image_name = images[index % len(images)]
        #     image_file_path = os.path.join(image_path, image_name)

        #     # Create a DraggableWidget and set it to the table cell
        #     draggable_widget = DraggableWidget(file_path, image_file_path)
        #     self.table_widget.setCellWidget(row, col, draggable_widget)

    def set_up(self):
        from main_window_v002_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
if __name__ == '__main__':
    app = QApplication.instance()  # Check if QApplication is already running
    if not app:
        app = QApplication(sys.argv)

    window = LibraryLoader()
    window.show()

    sys.exit(app.exec())