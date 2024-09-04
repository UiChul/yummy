from PySide6.QtWidgets import QFileDialog
import sys

class Nuke_test():
    def __init__(self):
        # 클립 import하면 이거 QFileDialog 나오게 하고
        file_tuple = QFileDialog.getOpenFileName(self, "select_nuke",f"/home/rapa/server/project/Marvelous/seq/OPN/OPN_0010/work/") 
        self.seq_path = file_tuple[0]
        
        # qfileDialog에서 클립을 선택하면 바로 nuke에 연동되게 만드는 걸 목표
        # nuke -t 로 py자체를 구동시켜서 넘기자.
        # 이건 sys.path로 인자를 넘겨줘서 py자체로 넘겨줘야 할 듯.
        # 그래서 넘겨줄 때 파일이름 frame수 2개를 넘겨줘서 작동되게 만들어보자
        print(self.seq_path)


        
        
        