from PySide6.QtWidgets import QApplication, QTableWidget, QLabel, QVBoxLayout, QWidget, QHeaderView, QGridLayout
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QPixmap
import os
import sys

try:
    import nuke
except ImportError:
    nuke = None  # Nuke가 import되지 않은 경우를 대비

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
        self.image_label.setFixedSize(200, 200)  # Adjust size as needed
        layout.addWidget(self.image_label)

        # Create and add the draggable label
        self.draggable_label = QLabel(os.path.basename(file_path))
        self.draggable_label.setAlignment(Qt.AlignCenter)
        self.draggable_label.setFixedSize(300, 50)
        self.draggable_label.setStyleSheet("border: 1px solid black; background-color: lightgray;")
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

class LibraryLoader(QWidget):  # QWidget으로 변경
    def __init__(self):
        super().__init__()

        self.set_up()

        # Main layout setup
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create QTableWidget
        self.table_widget = DroppableTableWidget(3, 3)  # Initial size, will adjust dynamically

        # Add QTableWidget to gridLayout_test
        if hasattr(self.ui, 'gridLayout_clip'):
            self.ui.gridLayout_clip.addWidget(self.table_widget, 0, 0)  # Add at position (0, 0)

        # Load MOV files into the table
        self.load_mov_files("/home/rapa/YUMMY/project/Marvelous/template/shot/clip_lib", "/home/rapa/xgen/clip_thumbnail")

    def load_mov_files(self, folder_path, image_path):
        """
        Load all .mov files from the given folder path into the table widget,
        and set images from the image_path folder.
        """
        # Get a list of all .mov files in the directory
        mov_files = [f for f in os.listdir(folder_path) if f.endswith('.mov')]
        
        if not mov_files:
            print(f"No .mov files found in {folder_path}")
            return

        # Get a list of all image files in the directory
        images = [f for f in os.listdir(image_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Adjust table size to fit the number of files
        rows = (len(mov_files) // 3) + (1 if len(mov_files) % 3 else 0)
        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(3)

        # Populate table with DraggableWidgets
        for index, file_name in enumerate(mov_files):
            row = index // 3
            col = index % 3
            file_path = os.path.join(folder_path, file_name)

            # Create and set the image path
            image_name = images[index % len(images)]
            image_file_path = os.path.join(image_path, image_name)

            # Create a DraggableWidget and set it to the table cell
            draggable_widget = DraggableWidget(file_path, image_file_path)
            self.table_widget.setCellWidget(row, col, draggable_widget)

    def set_up(self):
        from main_window_v002_ui import Ui_Form
        # ui_file_path = "/home/rapa/yummy/pipeline/scripts/loader/main_window.ui"
        # ui_file = QFile(ui_file_path)
        # ui_file.open(QFile.ReadOnly)
        # loader = QUiLoader()
        # self.ui = loader.load(ui_file,self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
if __name__ == '__main__':
    app = QApplication.instance()  # Check if QApplication is already running
    if not app:
        app = QApplication(sys.argv)

    window = LibraryLoader()
    window.show()

    sys.exit(app.exec())
