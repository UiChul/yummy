from PySide6.QtWidgets import QApplication, QTableWidget, QLabel, QVBoxLayout, QWidget, QHeaderView, QGridLayout, QPushButton
from PySide6.QtCore import Qt, QMimeData, QSize, QProcess
from PySide6.QtGui import QDrag, QPixmap, QCursor
import os
import sys
import json
sys.path.append("/home/rapa/yummy/pipeline/scripts/loader")


try:
    import nuke
except ImportError:
    nuke = None

class DraggableWidget(QWidget):
    def __init__(self, file_path, image_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 이미지와 라벨이 들어갈 레이아웃
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # 이미지 라벨
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)
        
        # 이미지 크기 조절
        desired_size = QSize(260, 135)  # 원하는 크기 (너비, 높이)
        scaled_pixmap = pixmap.scaled(desired_size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                                      Qt.TransformationMode.SmoothTransformation)
        
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(desired_size)  # QLabel 크기를 고정
        self.image_label.setScaledContents(True)  # 이미지가 QLabel에 맞게 조정되도록 설정
        layout.addWidget(self.image_label)

        # 드래그 가능한 라벨(이미지 라벨과 함께 동작함)
        self.draggable_label = QLabel(os.path.basename(file_path))
        self.draggable_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.draggable_label.setFixedSize(260, 20)
        self.draggable_label.setStyleSheet("font: 10pt;")
        layout.addWidget(self.draggable_label)

        self.file_path = file_path

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            
            # Q드래그 오브젝트 만들고 Mimedata 세팅
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.file_path)
            drag.setMimeData(mime_data)
            
            # Set the pixmap for the drag operation
            # pixmap = self.image_label.pixmap()
            # drag.setPixmap(pixmap)
            # drag.setHotSpot(event.position().toPoint() - self.rect().topLeft())
            
            # Start the drag operation
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
            text = event.mimeData().text()
            if nuke:
                self.apply_to_nuke(text)
            event.acceptProposedAction()
        else:
            event.ignore()

    def apply_to_nuke(self, text):
        if nuke:
            # 누크에서 리드 노드를 찾아서 추가, 리드 노드가 없다면 만들기
            read_nodes = []
            
            for node in nuke.allNodes():
                if node.Class() == "Read":
                    read_nodes.append(node)    

            if read_nodes:
                read_node = nuke.createNode('Read')

            # 리드 노드의 'file'에 mime 데이터로 넘어오는 파일 패스 전달
            read_node['file'].setValue(text)
            if not read_nodes:
                nuke.message("A new Read node has been created")

class Libraryclip:
    def __init__(self,Ui_Form):
        # super().__init__()
        self.ui = Ui_Form
        # self.ui.setupUi(self)

        # self.set_up()  # pyside UI 불러오기
        self.make_json_dic()

        # clip 테이블 위젯을 드래그&드랍 테이블 위젯으로 지정
        self.table_widget = DroppableTableWidget(3, 3)  # Initial size, will adjust dynamically
        self.table_widget.setMinimumSize(500, 400)

        # clip 테이블 위젯을 ui에서 만들어진 layout에 삽입
        if hasattr(self.ui, 'gridLayout_clip'):
            self.ui.gridLayout_clip.addWidget(self.table_widget, 0, 0)  # Add at position (0, 0)

        # mov와 썸네일 이미지 로드
        self.load_mov_and_image_files(
        f"/home/rapa/sub_server/project/{self.project}/template/shot/clip_lib", 
        f"/home/rapa/sub_server/project/{self.project}/template/shot/clip_lib/clip_thumbnail"
        )

    def make_json_dic(self):
        with open("/home/rapa/yummy/pipeline/json/project_data.json","rt",encoding="utf-8") as r:
            info = json.load(r)
        
        self.project = info["project"]
        self.user    = info["name"]
        self.rank    = info["rank"]
        self.resolution = info["resolution"]


    def load_mov_and_image_files(self, mov_path, image_path):
        """
        mov파일과 썸네일 이미지 파일 읽어서 테이블 위젯에 삽입
        """
        # mov 파일 리스트를 리스트로 저장
        mov_files = []        # [('explosion_1', 'explosion_1.mov'), ('explosion_2', 'explosion_2.mov')]
        for f in os.listdir(mov_path):
            if f.endswith('.mov'):
                base_name = os.path.splitext(f)[0]
                mov_files.append((base_name, f)) 
        
        # 리스트를 파일 이름 순으로 정렬
        mov_files.sort(key=lambda x: x[0])

        # 썸네일 이미지 파일 리스트를 딕셔너리로 저장
        images = {}
        for f in os.listdir(image_path):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
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
            self.table_widget.setCellWidget(row, col, draggable_widget)

    def set_up(self):
        from loader_ui.main_window_v002_ui import Ui_Form
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Libraryclip()
    window.show()
    sys.exit(app.exec())
