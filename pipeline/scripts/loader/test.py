from PySide6.QtWidgets import QWidget, QHeaderView, QFileDialog, QLabel, QVBoxLayout, QTableWidgetItem
from PySide6.QtWidgets import QAbstractItemView, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QDrag
import os
import sys
import json
import subprocess

try:
    import nuke
except ImportError:
    nuke = None

from test_dragdrop import DroppableTableWidget, DraggableWidget

class LibraryLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up()

        self.project = info["project"]
        self.user = info["name"]

        # Use DroppableTableWidget instead of the ui table widget
        self.table_widget_mod = DroppableTableWidget(3, 3)
        self.table_widget_rig = DroppableTableWidget(3, 3)
        self.table_widget_temp = DroppableTableWidget(3, 3)  # If needed

        self.asset_paths = {"mod": None, "rig": None}

        self.set_user_information()
        # self.set_clip_files_text_table()

        # Disable the comboBox initially
        self.ui.comboBox_seq.setEnabled(False)

        # self.set_asset_listWidget("Character")
        # self.set_asset_type_comboBox()
        self.set_tableWidget()  # Set up the table widgets
        # self.input_asset_tableWidget_mod()
        # self.input_asset_tableWidget_rig()

        # # Signal connections
        # self.ui.comboBox_asset_type.currentTextChanged.connect(self.set_asset_listWidget)
        # self.table_widget_mod.cellClicked.connect(self.output_asset_path_tableWidget)
        # self.table_widget_rig.cellClicked.connect(self.output_asset_path_tableWidget)

    def set_tableWidget(self):
        tables = [self.table_widget_mod, self.table_widget_rig, self.table_widget_temp]
        for i in tables:
            h_header = i.horizontalHeader()
            h_header.setSectionResizeMode(QHeaderView.Stretch)
            i.setEditTriggers(QAbstractItemView.NoEditTriggers)
            i.setColumnCount(3)
            i.setRowCount(6)
            i.setAcceptDrops(True)
            i.setDragEnabled(True)
            i.setDragDropMode(QAbstractItemView.DragDrop)
            i.setDefaultDropAction(Qt.CopyAction)
            i.installEventFilter(self)

    # def input_asset_tableWidget_mod(self):
    #     self.table_widget_mod.clear()
    #     row = 0
    #     col = 0

    #     count_mod = self.ui.listWidget_mod.count()

    #     # listWidget에 띄어진 items_text
    #     asset_lists = []
    #     thumbnails_path = []
    #     for i in range(count_mod):
    #         item_text = self.ui.listWidget_mod.item(i).text()
    #         asset_lists.append(item_text)

    #         thumbnail_path = f"/home/rapa/xgen/asset_thumbnail/asset_{item_text}_thumbnail.png"
    #         thumbnails_path.append(thumbnail_path)

    #     row = 0
    #     col = 0
    #     for image, asset_list in zip(thumbnails_path, asset_lists):
    #         cell_widget = QWidget()
    #         layout = QVBoxLayout()

    #         path = os.path.join(thumbnail_path, image)
    #         label_image = QLabel()
    #         pixmap = QPixmap(path)
    #         label_image.setPixmap(pixmap)
    #         label_image.setAlignment(Qt.AlignCenter)
    #         label_image.setScaledContents(True)

    #         label_text = QLabel()
    #         label_text.setText(asset_list)
    #         label_text.setStyleSheet('font-size: 12px;')
    #         label_text.setAlignment(Qt.AlignCenter)
    #         label_text.setWordWrap(True)

    #         layout.addWidget(label_image)
    #         layout.addWidget(label_text)
    #         layout.setContentsMargins(20, 10, 20, 10)
    #         layout.setAlignment(Qt.AlignCenter)

    #         cell_widget.setLayout(layout)

    #         item = QTableWidgetItem(asset_list)
    #         item.setData(Qt.UserRole, os.path.join(self.asset_paths["mod"], asset_list))
    #         self.table_widget_mod.setItem(row, col, item)
    #         self.table_widget_mod.setCellWidget(row, col, cell_widget)

    #         self.reduce_item_visibility_in_tableWidget(row, col)

    #         col += 1

    #         if col >= 3:
    #             col = 0
    #             row += 1

    # def input_asset_tableWidget_rig(self):
    #     self.table_widget_rig.clear()
    #     row = 0
    #     col = 0

    #     count_rig = self.ui.listWidget_rig.count()

    #     # listWidget에 띄어진 items_text
    #     asset_lists = []
    #     thumbnails_path = []
    #     for i in range(count_rig):
    #         item_text = self.ui.listWidget_rig.item(i).text()
    #         asset_lists.append(item_text)

    #         thumbnail_path = f"/home/rapa/xgen/asset_thumbnail/asset_{item_text}_thumbnail.png"
    #         thumbnails_path.append(thumbnail_path)

    #     row = 0
    #     col = 0
    #     for image, asset_list in zip(thumbnails_path, asset_lists):
    #         cell_widget = QWidget()
    #         layout = QVBoxLayout()

    #         path = os.path.join(thumbnail_path, image)
    #         label_image = QLabel()
    #         pixmap = QPixmap(path)
    #         label_image.setPixmap(pixmap)
    #         label_image.setAlignment(Qt.AlignCenter)
    #         label_image.setScaledContents(True)

    #         label_text = QLabel()
    #         label_text.setText(asset_list)
    #         label_text.setStyleSheet('font-size: 12px;')
    #         label_text.setAlignment(Qt.AlignCenter)
    #         label_text.setWordWrap(True)

    #         layout.addWidget(label_image)
    #         layout.addWidget(label_text)
    #         layout.setContentsMargins(20, 10, 20, 10)
    #         layout.setAlignment(Qt.AlignCenter)

    #         cell_widget.setLayout(layout)

    #         self.table_widget_rig.setCellWidget(row, col, cell_widget)

    #         item = QTableWidgetItem(asset_list)
    #         item.setData(Qt.UserRole, os.path.join(self.asset_paths["rig"], asset_list))
    #         self.table_widget_rig.setItem(row, col, item)
    #         self.table_widget_rig.setCellWidget(row, col, cell_widget)

    #         self.reduce_item_visibility_in_tableWidget(row, col)

    #         col += 1

    #         if col >= 3:
    #             col = 0
    #             row += 1

    # other methods unchanged

    def set_user_information(self):
        self.ui.label_projectname.setText(f"{self.project}")
        self.ui.label_username.setText(f"{self.user}")

    def set_up(self):
        from main_window_v002_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)

info = {"project": "Marvelous", "name": "su"}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LibraryLoader()
    win.show()
    sys.exit(app.exec())
