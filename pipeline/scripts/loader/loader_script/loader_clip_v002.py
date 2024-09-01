from PySide6.QtWidgets import QApplication, QTableWidget, QLabel, QVBoxLayout
from PySide6.QtWidgets import QWidget, QHeaderView, QGridLayout, QPushButton, QMenu
from PySide6.QtCore import Qt, QMimeData, QSize, QProcess, Signal, QObject
from PySide6.QtGui import QContextMenuEvent, QDrag, QPixmap, QCursor, QAction, QMovie
import os
import sys
import subprocess
sys.path.append("/home/rapa/yummy/pipeline/scripts/loader")

from loader_ui.main_window_v002_ui import Ui_Form
from loader_module.ffmpeg_module import find_resolution_frame
from loader_module.find_time_size import File_data

try:
    import nuke
except ImportError:
    nuke = None 

class DraggableWidget(QWidget):
    widgetClicked = Signal(str, str)
    
    def __init__(self, file_path, image_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 이미지와 라벨이 들어갈 레이아웃
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # 이미지 라벨
        self.image_label = QLabel()
        self.image_label.setFixedSize(260, 135)
        
        #이미지 라벨에 QMovie로 gif 넣기
        self.movie = QMovie(image_path)
        self.image_label.setMovie(self.movie)

        self.movie.setScaledSize(QSize(260,135))

        self.movie.start() #창이 열릴 때 gif 실행하고 바로 pause
        self.movie.setPaused(True)

        layout.addWidget(self.image_label)

        # 드래그 가능한 라벨(이미지 라벨과 함께 동작함)
        self.draggable_label = QLabel(os.path.basename(file_path))
        self.draggable_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.draggable_label.setFixedSize(260, 20)
        self.draggable_label.setStyleSheet("font: 10pt;")
        layout.addWidget(self.draggable_label)

        self.file_path = file_path
        self.mov_file = os.path.basename(file_path)
        self.mov_name, self.ext_type = os.path.splitext(self.mov_file)
 
    def enterEvent(self, event): #위젯에 마우스를 올렸을 때, gif pause 해제
        self.movie.setPaused(False)
        super().enterEvent(event)

    def leaveEvent(self, event): #마우스가 떠나면, 다시 gif pause
        self.movie.setPaused(True)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            #위젯을 클릭했을 때, clip info 표시를 위한 emit
            self.widgetClicked.emit(self.mov_name, self.ext_type) 
            # Q드래그 오브젝트 만들고 Mimedata 세팅
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.file_path)
            drag.setMimeData(mime_data)
            drag.exec(Qt.MoveAction | Qt.CopyAction)

        if event.buttons() == Qt.RightButton:
            self.show_menubar(event)

    def show_menubar(self, event):
        main_menu = QMenu(self)
        sub_menu = QMenu(self)
        sub_menu.setTitle("resolution")

        main_header = QAction(self.mov_file)
        main_header.setEnabled(False)
        main_menu.addAction(main_header)
        
        main_menu.addMenu(sub_menu)

        action1 = main_menu.addAction("open folder")

        main_menu.addAction(action1)

        sub_action_1 = sub_menu.addAction("1280x720")
        sub_action_2 = sub_menu.addAction("1920x1080")
        sub_action_3 = sub_menu.addAction("3840x2160")

        sub_menu.addAction(sub_action_1)
        sub_menu.addAction(sub_action_2)
        sub_menu.addAction(sub_action_3)

        action1.triggered.connect(self.handle_action1)
        sub_action_1.triggered.connect(self.handle_subAction1)
        sub_action_2.triggered.connect(self.handle_subAction2)
        sub_action_3.triggered.connect(self.handle_subAction3)

        main_menu.exec(event.globalPos())

    def handle_action1(self):
        folder_path = os.path.dirname(self.file_path)

        if os.path.isdir(folder_path):
            subprocess.run(["xdg-open", folder_path])
    
    def handle_subAction1(self):
        self.selected_format = "HD_720"
        self.emit_mimedata()

    def handle_subAction2(self):
        self.selected_format = "HD_1080"
        self.emit_mimedata()

    def handle_subAction3(self):
        self.selected_format = "UHD_4K"
        self.emit_mimedata()

    def emit_mimedata(self):
        mime_data = QMimeData()
        data = f"file_path:{self.file_path},resolution:{self.selected_format or 'none'}"
        mime_data.setText(data)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec(Qt.MoveAction | Qt.CopyAction)

    def mouseDoubleClickEvent(self, event): #마우스 더블 클릭 이벤트로 rv실행
        if event.button() == Qt.LeftButton:
            self.open_mov_in_rv()

    def open_mov_in_rv(self):
        # QProcess 인스턴스 생성
        process = QProcess(self)

        # RV 실행 파일의 경로
        rv_path = "/home/rapa/RV/bin/rv" 
        mov_file_path = self.file_path  # 위젯의 파일 경로

        # RV를 실행하고 MOV 파일을 인수로 전달하여 파일 자동 재생
        arguments = [mov_file_path, '-play', '-gamma', '2.2'] 
        process.start(rv_path, arguments)

        # 프로세스 상태와 출력을 모니터링
        process.readyRead.connect(self.handle_ready_read)
        process.finished.connect(self.handle_finished)

    def handle_ready_read(self):
        process = self.sender()
        output = process.readAll().data().decode()
        print(f"RV Output: {output}")

    def handle_finished(self):
        print("RV process finished")

class DroppableTableWidget(QTableWidget):
    def __init__(self, rows, columns, *args, **kwargs):
        super().__init__(rows, columns, *args, **kwargs)
        self.setAcceptDrops(True)
        self.setSelectionMode(QTableWidget.MultiSelection) 
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
            data = event.mimeData().text()
            file_path, resolution = self.parse_mimedata(data)

            if nuke:
                # 파일 경로를 설정하고 Read 노드를 반환
                read_node = self.apply_file_path_to_nuke(file_path)
                
                # 반환된 Read 노드에 해상도를 설정
                if read_node:
                    self.apply_resolution_to_nuke(read_node, resolution)

            event.acceptProposedAction()
        else:
            event.ignore()

    # def parse_mimedata(self, data):
    #     """
    #     문자열 데이터에서 파일 경로와 해상도를 파싱합니다.
    #     """
    #     file_path = None
    #     resolution = None

    #     # 문자열 데이터를 ','로 나누고 각 부분을 검사
    #     parts = data.split(',')
    #     for part in parts:
    #         if part.startswith("file_path:"):
    #             file_path = part[len("file_path:"):]
    #         elif part.startswith("resolution:"):
    #             resolution = part[len("resolution:"):]

    #     return file_path, resolution

    def apply_file_path_to_nuke(self, file_path):
        if nuke:
            # 모든 Read 노드 검색
            read_nodes = [node for node in nuke.allNodes() if node.Class() == "Read"]

            # 기존 Read 노드가 있으면 첫 번째 노드를 사용하고, 없으면 새로 생성
            if read_nodes:
                read_node = read_nodes[0]
            else:
                read_node = nuke.createNode('Read')

            # 파일 경로 설정
            if file_path:
                read_node['file'].setValue(file_path)

            # 새로 생성된 Read 노드가 있으면 확인 메시지 표시
            if not read_nodes:
                nuke.message("A new Read node has been created")

class Libraryclip:
    def __init__(self,Ui_Form):
        # super().__init__()
        self.ui = Ui_Form
        # self.set_up()  # pyside UI 불러오기

        # Main layout setup
        # layout = QVBoxLayout()
        # layout.setAlignment(Qt.AlignCenter)
        # self.setLayout(layout)

        # clip 테이블 위젯을 드래그&드랍 테이블 위젯으로 지정
        self.table_widget = DroppableTableWidget(3, 3)  # Initial size, will adjust dynamically
        self.table_widget.setMinimumSize(500, 400)

        # clip 테이블 위젯을 ui에서 만들어진 layout에 삽입
        if hasattr(self.ui, 'gridLayout_clip'):
            self.ui.gridLayout_clip.addWidget(self.table_widget, 0, 0)  # Add at position (0, 0)

        # mov와 썸네일 이미지 로드
        self.load_mov_and_image_files(
        "/home/rapa/YUMMY/project/YUMMIE/template/shot/clip_lib", 
        "/home/rapa/YUMMY/project/YUMMIE/template/shot/clip_lib/clip_thumbnail"
        )

        # self.start_webhooks_monitor()

    def load_mov_and_image_files(self, mov_path, image_path):
        """
        mov파일과 썸네일 이미지 파일 읽어서 테이블 위젯에 삽입
        """
        # mov 파일 리스트를 리스트로 저장
        mov_files = [] # [('explosion_1', 'explosion_1.mov'), ('explosion_2', 'explosion_2.mov')]
        for f in os.listdir(mov_path):
            if f.endswith('.mov'):
                base_name = os.path.splitext(f)[0]
                mov_files.append((base_name, f))
        
        # 리스트를 파일 이름 순으로 정렬
        mov_files.sort(key=lambda x: x[0])

        # 썸네일 이미지 파일 리스트를 딕셔너리로 저장
        images = {}
        for f in os.listdir(image_path):
            if f.lower().endswith(('.gif')):
                base_name = os.path.splitext(f)[0]
                images[base_name] = f

        # 공통된 파일 이름을 담을 리스트 초기화
        common_name = []
        
        # mov_files에서 base_name을 하나씩 확인하여 images에 존재하는지 확인
        for base_name, _ in mov_files:
            if base_name in images:
                common_name.append(base_name)

        # 불러오는 파일 갯수에 맞게 테이블 셋업
        rows = (len(common_name) // 3) + (1 if len(common_name) % 3 else 0)
        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(3)

        # 드래그 가능한 위젯 안에 내용 채우기
        for index, base_name in enumerate(common_name):
            row = index // 3
            col = index % 3
            
            # mov_file 찾기
            mov_file = None
            for name, file in mov_files:
                if name == base_name:
                    mov_file = file
                    break
            
            # image_file 찾기
            image_file = images[base_name]

            file_path = os.path.join(mov_path, mov_file)
            image_file_path = os.path.join(image_path, image_file)

            # 셀 위젯 만들기
            draggable_widget = DraggableWidget(file_path, image_file_path)
            draggable_widget.widgetClicked.connect(self.file_info)
            self.table_widget.setCellWidget(row, col, draggable_widget)
        
    def set_up(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)


    def file_info(self, mov_file, ext_type):
        self.ui.label_clip_filename.clear()
        self.ui.label_clip_filetype.clear()
        self.ui.label_clip_framerange.clear()
        self.ui.label_clip_resolution.clear()
        self.ui.label_clip_savedtime.clear()
        self.ui.label_clip_filesize.clear()
        
        mov_path = f"/home/rapa/YUMMY/project/YUMMIE/template/shot/clip_lib/{mov_file}{ext_type}"
        w,h,frame = find_resolution_frame(mov_path)
        size,time = File_data.file_info(mov_path)
        
        self.ui.label_clip_filename.setText(mov_file)
        self.ui.label_clip_filetype.setText(ext_type)
        self.ui.label_clip_framerange.setText(str(frame))
        self.ui.label_clip_resolution.setText(f"{w} X {h}")
        self.ui.label_clip_savedtime.setText(time)
        self.ui.label_clip_filesize.setText(size)
           
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryLoader()
    window.show()
    sys.exit(app.exec())
