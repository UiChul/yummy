print("깃허브 테스트")
print("리눅스 테스트")
print("우인님")
print("우인님2")
print("우인님3")
print("지연님")
print("효기님")
print("지연님2")

def set_shot_exr_files_tableWidget(self):
        """
        exr file setting
        """
        # 폴더안에 들어가서 v001.png 넣어야함.
        # table 에 image + text 삽입
        
        self.set_shot_table(self.tab_name)
        self.exr_table.clearContents()
        
        if self.task_path:

            exr_files_path = self.task_path + "/dev/" + self.tab_name
            exrs = os.listdir(mov_files_path)
            if not exrs:
                h_header = self.mov_table.horizontalHeader()
                h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
                h_header.setSectionResizeMode(QHeaderView.Stretch)
                self.mov_table.setColumnCount(1)
                self.mov_table.setRowCount(1)
                self.mov_table.setShowGrid(False)
                       
                item = QTableWidgetItem()
                item.setText("EMPTY")
                
                # 테이블 폰트 사이즈 조절
                font  = QFont()
                font.setPointSize(40)
                item.setFont(font)
                
                # 아이템 클릭할 수 없게 만들기
                item.setFlags(Qt.NoItemFlags)
                self.mov_table.setItem(0,0,item)
                item.setTextAlignment(Qt.AlignCenter)
            
        else:
            return
        # print (exrs)

        row = 0
        col = 0

        for exr in exrs :
            exr_file_path = exr_files_path + "/" + exr
            image_path = os.path.join(exr_file_path, exr + ".1001.exr")
            
            if not os.path.isdir(f"{self.task_path}/.thumbnail/"):
                os.makedirs(f"{self.task_path}/.thumbnail/")

            png_path = f"{self.task_path}/.thumbnail/{exr}.1001.png"
            
            if not os.path.isfile(png_path):
                change_to_png(image_path,png_path)
            
            label_img = QLabel()
            pixmap = QPixmap(png_path)
            label_img.setPixmap(pixmap) 
            label_img.setAlignment(Qt.AlignCenter)
            label_img.setScaledContents(True)
            self.exr_table.setCellWidget(row,col,label_img)

            item = QTableWidgetItem()
            item.setText(exr)
            self.exr_table.setItem(row+1,col,item)
            item.setTextAlignment(Qt.AlignCenter)

            col +=1
            
            # 갯수 맞춰서 다다음줄로
            if col >= self.exr_table.columnCount():            
                col = 0
                row += 2

        # 홀수 row 행 높이 조절
        for i in range(1, self.exr_table.rowCount(), 2):
            self.exr_table.setRowHeight(i,50) 
            
            
 def set_mov_text_files_tableWidget(self):
    #     """
    #     mov file setting
    #     """
    #     self.set_shot_table(self.tab_name)
    #     self.mov_table.clearContents()
        
    #     if self.task_path:
    #         mov_files_path = self.task_path + "/dev/" + self.tab_name
    #         movs = os.listdir(mov_files_path)
    #         if not movs:
    #             h_header = self.mov_table.horizontalHeader()
    #             h_header.setSectionResizeMode(QHeaderView.ResizeToContents)
    #             h_header.setSectionResizeMode(QHeaderView.Stretch)
    #             self.mov_table.setColumnCount(1)
    #             self.mov_table.setRowCount(1)
    #             self.mov_table.setShowGrid(False)  
                
    #             item = QTableWidgetItem()
    #             item.setText("EMPTY")
    #             # 테이블 폰트 사이즈 조절
    #             font  = QFont()
    #             font.setPointSize(40)
    #             item.setFont(font)
    #             # 아이템 클릭할 수 없게 만들기
    #             item.setFlags(Qt.NoItemFlags)
    #             self.mov_table.setItem(0,0,item)
    #             item.setTextAlignment(Qt.AlignCenter)     
    #     else:
    #         return
    #     # print (movs)
    #     # print (mov_files_path)

    #     row = 0
    #     col = 0

    #     # table 에 image + text 삽입
    #     for mov in movs:
            
    #         mov_name = mov.split(".")[0]

    #         exr_file_path = self.task_path + "/dev/exr/" + mov_name
    #         image_path = os.path.join(exr_file_path, mov_name + ".1001.exr")
        
    #         if not os.path.isdir(f"{self.task_path}/.thumbnail/"):
    #             os.makedirs(f"{self.task_path}/.thumbnail/")   
                
    #         png_path = f"{self.task_path}/.thumbnail/{mov_name}.1001.png"  
             
    #         if not os.path.isfile(png_path):
    #             change_to_png(image_path,png_path)
        
    #         label_img = QLabel()
    #         pixmap = QPixmap(png_path)
    #         label_img.setPixmap(pixmap) 
    #         label_img.setAlignment(Qt.AlignCenter)
    #         label_img.setScaledContents(True)
    #         self.mov_table.setCellWidget(row,col,label_img)
            
    #         item = QTableWidgetItem()
    #         item.setText(mov)
    #         self.mov_table.setItem(row+1,col,item)
    #         item.setTextAlignment(Qt.AlignCenter)

    #         col +=1

    #          # 갯수 맞춰서 다다음줄로
    #         if col >= self.mov_table.columnCount():            
    #             col = 0
    #             row += 2

    #     # 홀수 row 행 높이 조절
    #     for i in range(1, self.mov_table.rowCount(), 2):
    #         self.mov_table.setRowHeight(i,50)             