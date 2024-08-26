from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
from PySide6.QtCore import QMimeData, Qt
from PySide6.QtGui import QCursor,QDrag
from darg_rnd_ui import Ui_Form

class Drag(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up()
        self.set_table_widget()
        
    def set_table_widget(self):
        self.table.setRowCount(1)
        self.table.setRowHeight(0,100)
        
        
        self.table.setColumnCount(3)
        self.table.setColumnWidth(0,100)
        self.table.setColumnWidth(1,100)
        self.table.setColumnWidth(2,100)
        
        item  = QTableWidgetItem()
        item.setText("1")
        self.table.setItem(0,0,item)
        
        self.table.setDragEnabled(True)  # 드래그 활성화
        self.table.setAcceptDrops(True)  # 드롭 허용
        self.table.setDragDropMode(QAbstractItemView.InternalMove)
        
        
    def startDrag(self, supportedActions):
        item = self.currentItem()  # 현재 선택된 아이템
        if not item:
            return

        drag = QDrag(self)
        mimeData = QMimeData()

        # MIME 데이터에 텍스트와 추가 정보를 포함
        mimeData.setText(item.text())
        mimeData.setData('application/x-item-info', f"Row:{item.row()}, Column:{item.column()}".encode('utf-8'))

        drag.setMimeData(mimeData)
        drag.setHotSpot(QCursor.pos() - self.rect().topLeft())  # 드래그 시 마우스 포인터 위치

        drag.exec(Qt.IgnoreAction)

    def dropEvent(self, event):
        mimeData = event.mimeData()

        if mimeData.hasFormat('application/x-item-info'):
            item_info = mimeData.data('application/x-item-info').data().decode('utf-8')
            print(f"드롭된 아이템 정보: {item_info}")

        super().dropEvent(event)  # 기본 드롭 이벤트 처리
        
    
        
        
        
        
        

        
    def set_up(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.table = self.ui.tableWidget
        
app = QApplication()
my = Drag()
my.show()
app.exec()