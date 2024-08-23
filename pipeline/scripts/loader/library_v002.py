import os
import sys
import subprocess
from PySide6.QtWidgets import QWidget, QFileDialog, QVBoxLayout, QLabel, QApplication, QTableWidgetItem, QAbstractItemView, QHeaderView
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtUiTools import QUiLoader

import ffmpeg

try:
    import nuke
    NUKESCRIPT_RUNNING = True
except ImportError:
    NUKESCRIPT_RUNNING = False

class LibraryLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up()

        self.project = info["project"]
        self.user = info["name"]

        self.clip_table = self.ui.tableWidget_clip_files

        self.set_user_information()
        self.set_clip_files_text_table()

        # Signal
        self.clip_table.itemClicked.connect(self.set_clip_files_text_table)
        self.ui.pushButton_clip_file_nuke.clicked.connect(self.handle_nuke_file)

    def set_clip_files_text_table(self):
        self.clip_table.clear()
        file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib/"
        clip_lists = os.listdir(file_path)

        image_path = "/home/rapa/xgen/clip_thumbnail"
        images = os.listdir(image_path)

        count = (len(clip_lists) // 3)
        
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

            label_text = QLabel()
            label_text.setText(clip_list)
            label_text.setStyleSheet(''' font-size: 9px; ''')
            label_text.setAlignment(Qt.AlignCenter)
            label_text.setWordWrap(True)

            layout.addWidget(label_image)
            layout.addWidget(label_text)
            layout.setContentsMargins(20, 5, 20, 10)
            layout.setAlignment(Qt.AlignCenter)

            cell_widget.setLayout(layout)

            self.clip_table.setCellWidget(row, col, cell_widget)  

            col += 1  

            if col >= 3:
                col = 0
                row += 1

        return clip_lists

    def handle_nuke_file(self):
        try:
            if 'nuke' in sys.modules:
                # Nuke 모듈이 로드되어 있으면 Nuke가 실행 중임
                self.import_clip_file_to_nuke(self.clip_table.currentItem())
            else:
                # Nuke 모듈이 로드되지 않았으면, Nuke를 새로 엽니다.
                self.open_file_window()
        except Exception as e:
            print(f"파일을 Nuke에 추가하는 동안 오류가 발생했습니다: {e}")


    def import_clip_file_to_nuke(self, item):
        # Nuke의 현재 인스턴스에 접근하여 노드 추가
        try:
            # 선택된 항목의 텍스트를 가져옵니다.
            selected_item = item.text()
            file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib/{selected_item}"

            # Nuke에서 Read 노드 생성
            read_node = nuke.createNode('Read')
            read_node['file'].setValue(file_path)
            nuke.connectViewer(0, read_node)
            read_node['selected'].setValue(True)

            # 프레임 정보 업데이트
            frame = self.get_frame_info(file_path)
            read_node['last'].setValue(frame)

            print(f"파일 {file_path}이(가) Nuke에 성공적으로 추가되었습니다.")
        except Exception as e:
            print(f"Nuke에서 파일을 추가하는 동안 오류가 발생했습니다: {e}")

    def handle_nuke_file(self):
        try:
            nuke_script = """
import nuke
selected_item = '{selected_item}'
file_path = f"/home/rapa/YUMMY/project/{self.project}/template/shot/clip_lib/{selected_item}"
read_node = nuke.createNode('Read')
read_node['file'].setValue(file_path)
nuke.connectViewer(0, read_node)
read_node['selected'].setValue(True)
frame = 0
read_node['last'].setValue(frame)
"""
            item = self.clip_table.currentItem()
            if item:
                selected_item = item.text()
                nuke_script = nuke_script.format(selected_item=selected_item)
                nuke.executeScript(nuke_script)
                print(f"파일 {selected_item}이(가) Nuke에 성공적으로 추가되었습니다.")
            else:
                self.open_file_window()
        except Exception as e:
            print(f"Nuke에서 파일을 추가하는 동안 오류가 발생했습니다: {e}")

    def open_file_window(self):
        file_tuple = QFileDialog.getOpenFileName(self, "Import Nuke File", f"/home/rapa/YUMMY/project/{self.project}")
        self.selected_nuke_file_path = file_tuple[0]

        if self.selected_nuke_file_path:
            nuke_path = "/mnt/project/Nuke15.1v1/Nuke15.1"
            command = f'source /home/rapa/env/nuke.env && {nuke_path} --nc "{self.selected_nuke_file_path}"'
            os.system(command)

    def get_frame_info(self, input):
        probe = ffmpeg.probe(input)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

        if input.split(".")[-1] in ["mov", "mp4"]:
            frame = int(video_stream['nb_frames'])
        else:
            frame = 0

        return frame

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
    app.exec()