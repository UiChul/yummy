# from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHeaderView, QFileDialog, QTableWidget, QLabel
from PySide6.QtWidgets import QVBoxLayout, QLabel, QApplication, QTableWidgetItem
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QMimeData, QUrl, Qt
from PySide6.QtGui import QPixmap, Qt, QDrag, QClipboard

try:
    import nuke
except ImportError:
    nuke = None

import os, sys
import ffmpeg
import subprocess

info = {"project": "Marvelous", "name": "su"}

class DraggableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_path = ""

    def set_file_path(self, file_path):
        self._file_path = file_path
        self.setText(file_path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.text():
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self._file_path)
            drag.setMimeData(mime_data)
            drag.exec_(Qt.CopyAction | Qt.MoveAction)
        else:
            super().mousePressEvent(event)

class DroppableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            self.setText(text)
            if nuke in globals():
                self.apply_to_nuke(text)
            event.acceptProposedAction()
        else:
            event.ignore()

    def apply_to_nuke(self, text):
        if nuke:
            #Read node를 찾거나 만들기
            read_nodes = [node for node in nuke.allNodes() if node.Class() == "Read"]
            if read_nodes:
                read_node = read_nodes[0]  # Use the first Read node found
            else:
                read_node = nuke.createNode('Read')
    
            read_node["file"].setValue(text)

        if read_node:
            nuke.connectViewer(0, read_node)

class LibraryLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up()

        self.project = info["project"]
        self.user = info["name"]

        self.clip_table = self.ui.tableWidget_clip_files

        self.set_user_information()
        self.set_clip_files_text_table()

        # ComboBox 비활성화
        self.ui.comboBox_seq.setEnabled(False)

        # Signal 연결
        self.clip_table.cellPressed.connect(self.handle_cell_click)
        # self.ui.pushButton_clip_file_nuke.clicked.connect(self.open_file_window)

    def set_clip_files_text_table(self):
        """
        이미지와 텍스트를 포함하는 셀 위젯을 테이블에 설정합니다.
        """
        file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib/"
        clip_lists = os.listdir(file_path)

        image_path = "/home/rapa/xgen/clip_thumbnail"
        images = os.listdir(image_path)

        count = len(clip_lists) // 3

        h_header = self.clip_table.horizontalHeader()
        h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        h_header.setSectionResizeMode(QHeaderView.Stretch)
        self.clip_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.clip_table.setColumnCount(3)
        self.clip_table.setRowCount(count + 1)

        row = 0
        col = 0
        for image, clip_list in zip(images, clip_lists):
            cell_widget = QWidget()
            layout = QVBoxLayout()

            path = os.path.join(image_path, image)
            label_image = QLabel()
            pixmap = QPixmap(path)
            label_image.setPixmap(pixmap)
            label_image.setAlignment(Qt.AlignCenter)
            label_image.setScaledContents(True)

            label_text = DraggableLabel(self)
            label_text.setText(clip_list)
            label_text.setStyleSheet('font-size: 9px;')
            label_text.setAlignment(Qt.AlignCenter)
            label_text.setWordWrap(True)
            label_text.setObjectName("clipTextLabel")  # 명시적 이름 설정

            layout.addWidget(label_image)
            layout.addWidget(label_text)
            layout.setContentsMargins(20, 5, 20, 10)
            layout.setAlignment(Qt.AlignCenter)

            cell_widget.setLayout(layout)

            # QTableWidgetItem 생성 및 데이터 설정
            item = QTableWidgetItem(clip_list)
            item.setData(Qt.UserRole, os.path.join(file_path, clip_list))
            self.clip_table.setItem(row, col, item)
            self.clip_table.setCellWidget(row, col, cell_widget)

            col += 1

            if col >= 3:
                col = 0
                row += 1

        return clip_lists

    def handle_cell_click(self, row, column):
        """
        클릭된 셀의 위젯에서 QLabel의 텍스트와 전체 파일 경로를 프린트합니다.
        """
        item = self.clip_table.item(row, column)
        print ("item=",item)
        if item:
            # QTableWidgetItem에서 파일 경로를 가져옵니다
            file_path = item.data(Qt.UserRole)
            print(f"Clicked on: {file_path}")
            self.selected_item = file_path  # 클릭된 파일의 전체 경로 저장

        else:
            print("No item found at the clicked cell.")
            return file_path

    # def startDrag(self, supportedActions):
    #     """
    #     드래그 시작 시 호출됩니다.
    #     """
    #     row = self.clip_table.currentRow()
    #     column = self.clip_table.currentColumn()
    #     item = self.clip_table.item(row, column)
        
    #     if item:
    #         drag = QDrag(self)
    #         mimeData = QMimeData()
            
    #         # QTableWidgetItem에서 파일 경로를 가져옵니다
    #         file_path = item.data(Qt.UserRole)
            
    #         if file_path:
    #             mimeData.setText(file_path)
    #             drag.setMimeData(mimeData)
    #             drag.exec_(supportedActions)

    # def import_clip_file_to_nuke(self):
    #     """
    #     선택된 클립 파일을 Nuke에 가져옵니다.
    #     """
    #     if hasattr(self, 'selected_item'):
    #         file_path = self.selected_item
    #         read_node = nuke.createNode('Read')
    #         nuke.connectViewer(0, read_node)
    #         read_node['file'].setValue(file_path)

    #         # 프레임 정보 업데이트
    #         frame = self.get_frame_info(file_path)
    #         read_node['last'].setValue(frame)

    #         read_node['selected'].setValue(True)

    # def open_file_window(self):
    #     """
    #     Nuke 파일을 선택하는 파일 대화 상자를 엽니다.
    #     """
    #     file_tuple = QFileDialog.getOpenFileName(self, "Nuke 파일 가져오기", f"/home/rapa/YUMMY/project/{self.project}/seq/OPN/OPN_0010")
    #     self.selected_nuke_file_path = file_tuple[0]
    #     print(self.selected_nuke_file_path)

    #     if self.selected_nuke_file_path:
    #         nuke_path = "/mnt/project/Nuke15.1v1/Nuke15.1"
    #         command = f'source /home/rapa/env/nuke.env && {nuke_path} --nc "{self.selected_nuke_file_path}"'
    #         subprocess.run(command, shell=True)

    def get_frame_info(self, input_file):
        """
        비디오 파일의 프레임 수를 가져옵니다.
        """
        probe = ffmpeg.probe(input_file)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

        if input_file.split(".")[-1] in ["mov", "mp4"]:
            frame = int(video_stream['nb_frames'])
        else:
            frame = 0

        return frame

    def set_user_information(self):
        """
        사용자 및 프로젝트 정보를 설정합니다.
        """
        self.ui.label_projectname.setText(f"{self.project}")
        self.ui.label_username.setText(f"{self.user}")

    def set_up(self):
        """
        UI를 설정합니다.
        """
        from main_window_v002_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
        
    win = LibraryLoader()
    win.show()
    app.exec()