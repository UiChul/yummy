from PySide6.QtWidgets import QApplication, QTableWidget, QLabel
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QWidget, QHeaderView, QGridLayout
from PySide6.QtWidgets import QPushButton, QMenu, QCommandLinkButton
from PySide6.QtCore import Qt, QMimeData, QSize
from PySide6.QtCore import QProcess, Signal, QObject, QUrl
from PySide6.QtGui import QContextMenuEvent, QDrag, QPixmap
from PySide6.QtGui import QCursor, QAction,QIcon
from PySide6.QtGui import QMovie, QDesktopServices
from PySide6.QtGui import QPalette, QColor
import os
import sys
sys.path.append("/home/rapa/yummy/pipeline/scripts/loader")

from main_window_v002_uichul_ui import Ui_Form
# from loader_module.ffmpeg_module import find_resolution_frame
from loader_module.find_time_size import File_data

try:
    import nuke
except ImportError:
    nuke = None 

class DraggableWidget(QWidget):
    widgetClicked  = Signal(str, str)
    buttonClicked  = Signal(str)

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
        
        self.movie = QMovie(image_path)
        self.image_label.setMovie(self.movie)
        self.movie.setScaledSize(QSize(260,135))
        self.movie.start()
        self.movie.jumpToFrame(30)
        self.movie.setPaused(True)

        layout.addWidget(self.image_label)

        label_layout = QHBoxLayout()
        label_layout.setContentsMargins(0,0,0,0)

        # 드래그 가능한 라벨(이미지 라벨과 함께 동작함)
        self.draggable_label = QLabel(os.path.basename(file_path))
        self.draggable_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.draggable_label.setFixedSize(260, 20)
        self.draggable_label.setStyleSheet("font: 6pt;")
        self.draggable_label.setStyleSheet('color:rgb(211, 215, 207)')
        label_layout.addWidget(self.draggable_label)


        self.button = QPushButton(self)
        self.button.setFixedSize(25,25) 
        self.button.setCheckable(True)
        
        self.set_button_icon()
        self.button.clicked.connect(self.set_button_icon)
        self.button.clicked.connect(self.save_favorite_clips)
        label_layout.addWidget(self.button)

        label_widget = QWidget()
        label_widget.setLayout(label_layout)

        layout.addWidget(label_widget)

        self.file_path = file_path
        self.mov_file = os.path.basename(file_path)
        self.mov_name, self.ext_type = os.path.splitext(self.mov_file)
        self.selected_format = None


    def set_button_icon(self):

        # 이미지 경로 설정
        if self.button.isChecked():
            image_path = "/home/rapa/xgen/selected.png"
        else:
            image_path = "/home/rapa/xgen/unselected.png"

        # QPixmap을 사용하여 이미지를 로드하고 QIcon으로 변환
        pixmap = QPixmap(image_path)
        
        # 버튼 크기에 맞게 이미지 크기 조정 (비율 유지)
        button_size = self.button.size()
        scaled_pixmap = pixmap.scaled(button_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        # QIcon으로 변환 후 버튼 아이콘으로 설정
        icon = QIcon(scaled_pixmap)
        self.button.setIcon(icon)
        icon_size = QSize(button_size.width() -12, button_size.height() - 12)
        self.button.setIconSize(icon_size)  # 아이콘 크기 설정

        # 스타일시트 설정
        self.button.setStyleSheet(
            """
            QPushButton {
                padding: 0px; /* 버튼 내부 여백 제거 */
                margin: 0px; /* 버튼 외부 여백 제거 */
                border: none; /* 버튼 테두리 제거 */
                background: none; /* 버튼 배경 제거 */
                text-align: center; /* 텍스트 중앙 정렬 */
            }
            """
        )


    def save_favorite_clips(self):

        self.buttonClicked.emit(self.mov_name)


    def enterEvent(self, event):
        self.movie.setPaused(False)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.movie.setPaused(True)
        super().enterEvent(event)

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
        menubar = QMenu(self)

        header = QAction("Format")
        header.setEnabled(False)
        menubar.addAction(header)
        
        action1 = menubar.addAction("1280x720")
        action2 = menubar.addAction("1920x1080")
        action3 = menubar.addAction("3840x2160")

        action1.triggered.connect(self.handle_action1)
        action2.triggered.connect(self.handle_action2)
        action3.triggered.connect(self.handle_action3)

        menubar.exec(event.globalPos())

    # def contextMenuEvent(self, event: QContextMenuEvent) -> None:
    #     print (event.globalPos())
    #     self.show_menubar(event)
    #     return super().contextMenuEvent(event)
    
    def handle_action1(self):
        self.selected_format = "HD_720"

    def handle_action2(self):
        self.selected_format = "HD_1080"

    def handle_action3(self):
        self.selected_format = "UHD_4K"

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

class DraggableWidgetFav(QWidget):
    widgetClicked  = Signal(str, str)

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
        
        self.movie = QMovie(image_path)
        self.image_label.setMovie(self.movie)
        self.movie.setScaledSize(QSize(260,135))
        self.movie.start()
        self.movie.jumpToFrame(30)
        self.movie.setPaused(True)

        layout.addWidget(self.image_label)

        label_layout = QHBoxLayout()
        label_layout.setContentsMargins(0,0,0,0)

        # 드래그 가능한 라벨(이미지 라벨과 함께 동작함)
        self.draggable_label = QLabel(os.path.basename(file_path))
        self.draggable_label.setAlignment(Qt.AlignCenter)
        self.draggable_label.setFixedSize(260, 20)
        self.draggable_label.setStyleSheet("font: 6pt;")
        self.draggable_label.setStyleSheet('color:rgb(211, 215, 207)')
        label_layout.addWidget(self.draggable_label)

        label_widget = QWidget()
        label_widget.setLayout(label_layout)

        layout.addWidget(label_widget)

        self.file_path = file_path
        self.mov_file = os.path.basename(file_path)
        self.mov_name, self.ext_type = os.path.splitext(self.mov_file)
        self.selected_format = None

    def enterEvent(self, event):
        self.movie.setPaused(False)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.movie.setPaused(True)
        super().enterEvent(event)

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
        menubar = QMenu(self)

        header = QAction("Format")
        header.setEnabled(False)
        menubar.addAction(header)
        
        action1 = menubar.addAction("1280x720")
        action2 = menubar.addAction("1920x1080")
        action3 = menubar.addAction("3840x2160")

        action1.triggered.connect(self.handle_action1)
        action2.triggered.connect(self.handle_action2)
        action3.triggered.connect(self.handle_action3)

        menubar.exec(event.globalPos())

    # def contextMenuEvent(self, event: QContextMenuEvent) -> None:
    #     print (event.globalPos())
    #     self.show_menubar(event)
    #     return super().contextMenuEvent(event)
    
    def handle_action1(self):
        self.selected_format = "HD_720"

    def handle_action2(self):
        self.selected_format = "HD_1080"

    def handle_action3(self):
        self.selected_format = "UHD_4K"

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
            file_path = event.mimeData().text()
            if nuke:
                self.apply_to_nuke(file_path)
            event.acceptProposedAction()
        else:
            event.ignore()

    def apply_to_nuke(self, file_path):
        if nuke:
            # 누크에서 리드 노드를 찾아서 추가, 리드 노드가 없다면 만들기
            read_nodes = []
            
            for node in nuke.allNodes():
                if node.Class() == "Read":
                    read_nodes.append(node)    

            if read_nodes:
                read_node = nuke.createNode('Read')

            # 리드 노드의 'file'에 mime 데이터로 넘어오는 파일 패스 전달
            read_node['file'].setValue(file_path)
            if not read_nodes:
                nuke.message("A new Read node has been created")

class DroppableTableWidgetFav(QTableWidget):
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
            file_path = event.mimeData().text()
            if nuke:
                self.apply_to_nuke(file_path)
            event.acceptProposedAction()
        else:
            event.ignore()

    def apply_to_nuke(self, file_path):
        if nuke:
            # 누크에서 리드 노드를 찾아서 추가, 리드 노드가 없다면 만들기
            read_nodes = []
            
            for node in nuke.allNodes():
                if node.Class() == "Read":
                    read_nodes.append(node)    

            if read_nodes:
                read_node = nuke.createNode('Read')

            # 리드 노드의 'file'에 mime 데이터로 넘어오는 파일 패스 전달
            read_node['file'].setValue(file_path)
            if not read_nodes:
                nuke.message("A new Read node has been created")

class LibraryLoader(QWidget):
    def __init__(self):
        super().__init__()

        self.set_up()  # pyside UI 불러오기
        self.clip_fav_list = []

        self.setPalette(self.get_darkModePalette())

        # Main layout setup
        # layout = QVBoxLayout()
        # layout.setAlignment(Qt.AlignCenter)
        # self.setLayout(layout)

        # clip 테이블 위젯을 드래그&드랍 테이블 위젯으로 지정
        self.table_widget = DroppableTableWidget(3, 3)  # Initial size, will adjust dynamically
        self.table_widget.setMinimumSize(500, 400)

        self.table_widget_fav = DroppableTableWidgetFav(4,4)
        self.table_widget_fav.setMinimumSize(600,400)

        # clip 테이블 위젯을 ui에서 만들어진 layout에 삽입
        if hasattr(self.ui, 'gridLayout_clip'):
            self.ui.gridLayout_clip.addWidget(self.table_widget, 0, 0)  # Add at position (0, 0)
        if hasattr(self.ui, 'gridLayout_clip_fav'):
            self.ui.gridLayout_clip_fav.addWidget(self.table_widget_fav, 0, 0)  # Add at position (0, 0)

        # mov와 썸네일 이미지 로드
        self.load_mov_and_image_files(
        "/home/rapa/YUMMY/project/YUMMIE/template/shot/clip_lib", 
        "/home/rapa/YUMMY/project/YUMMIE/template/shot/clip_lib/clip_thumbnail"
        )


        # shotgird load button
        self.ui.commandLinkButton_shotgrid.clicked.connect(self.link_to_shotgrid)

        self.ui.pushButton_reset.clicked.connect(self.reset_ui)


        # 이미지 경로 설정
        image_path = "/home/rapa/xgen/reset.png"

        # QPixmap을 사용하여 이미지를 로드하고 QIcon으로 변환
        pixmap = QPixmap(image_path)
        
        # 버튼 크기에 맞게 이미지 크기 조정 (비율 유지)
        button_size = self.ui.pushButton_reset.size()

        scaled_pixmap = pixmap.scaled(button_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        # QIcon으로 변환 후 버튼 아이콘으로 설정
        icon = QIcon(scaled_pixmap)
        self.ui.pushButton_reset.setIcon(icon)
        icon_size = QSize(button_size.width() -10, button_size.height() - 10)
        self.ui.pushButton_reset.setIconSize(icon_size)  # 아이콘 크기 설정


        
    def reset_ui(self):
        print("0000000000")
        self.ui.comboBox_seq.clear()


    def link_to_shotgrid(self):
        url = QUrl("https://4thacademy.shotgrid.autodesk.com/projects/#Project_222")
        QDesktopServices.openUrl(url)

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
            draggable_widget.buttonClicked.connect(self.load_emited_button_list)
            self.table_widget.setCellWidget(row, col, draggable_widget)
    
    ################################################333
    # fav
    def load_emited_button_list(self,item):

        if item in self.clip_fav_list:
            self.clip_fav_list.remove(item)
        else:
            self.clip_fav_list.append(item)

        print(self.clip_fav_list)

        self.set_fav_items_in_tableWidget(        
        "/home/rapa/YUMMY/project/YUMMIE/template/shot/clip_lib", 
        "/home/rapa/YUMMY/project/YUMMIE/template/shot/clip_lib/clip_thumbnail")

    def set_fav_items_in_tableWidget(self, mov_path, image_path):
        
        self.table_widget_fav.clear()
        # 리스트를 파일 이름 순으로 정렬
        self.clip_fav_list.sort(key=lambda x: x[0])
        print ("457",self.clip_fav_list)

        # 썸네일 이미지 파일 리스트를 딕셔너리로 저장
        images = {}
        for f in os.listdir(image_path):
            if f.lower().endswith(('.gif')):
                base_name = os.path.splitext(f)[0]
                images[base_name] = f

        # 공통된 파일 이름을 담을 리스트 초기화
        fav_clip_existed_image_list = []
        
        # self.clip_fav_list에서 base_name을 하나씩 확인하여 images에 존재하는지 확인
        for base_name in self.clip_fav_list:
            if base_name in images:
                fav_clip_existed_image_list.append(base_name)
        print ("fav_clip_existed_image_list=" , fav_clip_existed_image_list)

        # 불러오는 파일 갯수에 맞게 테이블 셋업
        self.table_widget_fav.setRowCount(4)
        self.table_widget_fav.setColumnCount(4)

        # 드래그 가능한 위젯 안에 내용 채우기
        for index, base_name in enumerate(fav_clip_existed_image_list):
            row = index // 4
            col = index % 4
            
            # mov_file 찾기
            # clip_fav_file = None
            # for name, file in self.clip_fav_list:
            #     if name == base_name:
   
            #         break
            
            # image_file 찾기
            image_file = images[base_name]

            file_path = os.path.join(mov_path, base_name)
            image_file_path = os.path.join(image_path, image_file)

            draggable_widget_fav = DraggableWidgetFav(file_path, image_file_path)
            self.table_widget_fav.setCellWidget(row,col,draggable_widget_fav)




        
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
        # w,h,frame = find_resolution_frame(mov_path)
        # size,time = File_data.file_info(mov_path)
        
        self.ui.label_clip_filename.setText(mov_file)
        # self.ui.label_clip_filetype.setText(ext_type)
        # self.ui.label_clip_framerange.setText(str(frame))
        # self.ui.label_clip_resolution.setText(f"{w} X {h}")
        # self.ui.label_clip_savedtime.setText(time)
        # self.ui.label_clip_filesize.setText(size)
           
    def get_darkModePalette(self) :
    
        darkPalette = app.palette()
        darkPalette.setColor( QPalette.Window, QColor( 53, 53, 53 ) )
        darkPalette.setColor( QPalette.WindowText, QColor(211, 215, 207))
        darkPalette.setColor( QPalette.Disabled, QPalette.WindowText, QColor( 127, 127, 127 ) )
        darkPalette.setColor( QPalette.Base, QColor( 42, 42, 42 ) )
        darkPalette.setColor( QPalette.AlternateBase, QColor( 66, 66, 66 ) )
        darkPalette.setColor( QPalette.ToolTipBase, QColor( 53, 53, 53 ) )
        darkPalette.setColor( QPalette.ToolTipText, QColor(211, 215, 207) )
        darkPalette.setColor( QPalette.Text, QColor(211, 215, 207) )
        darkPalette.setColor( QPalette.Disabled, QPalette.Text, QColor( 127, 127, 127 ) )
        darkPalette.setColor( QPalette.Dark, QColor( 35, 35, 35 ) )
        darkPalette.setColor( QPalette.Shadow, QColor( 20, 20, 20 ) )
        darkPalette.setColor( QPalette.Button, QColor( 53, 53, 53 ) )
        darkPalette.setColor( QPalette.ButtonText, QColor(211, 215, 207) )
        darkPalette.setColor( QPalette.Disabled, QPalette.ButtonText, QColor( 127, 127, 127 ) )
        darkPalette.setColor( QPalette.BrightText, Qt.red )
        darkPalette.setColor( QPalette.Link, QColor( 42, 130, 218 ) )
        darkPalette.setColor( QPalette.Highlight, QColor( 42, 130, 218 ) )
        darkPalette.setColor( QPalette.Disabled, QPalette.Highlight, QColor( 80, 80, 80 ) )
        darkPalette.setColor( QPalette.HighlightedText, QColor(211, 215, 207) )
        darkPalette.setColor( QPalette.Disabled, QPalette.HighlightedText, QColor( 127, 127, 127 ), )
        
        return darkPalette
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryLoader()
    window.show()
    sys.exit(app.exec())
