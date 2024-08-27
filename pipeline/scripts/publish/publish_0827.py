### nk info 중 path 이상하게나옴 ;; 수정해야함

### 0826 : version/publish upload
### 0827 : render

try:
    from PySide6.QtWidgets import QApplication, QWidget, QTableWidgetItem, QListWidgetItem, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QGroupBox
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtCore import QFile
    from PySide6.QtGui import  Qt, QPixmap

except:
    from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem, QListWidgetItem, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox, QGroupBox
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtCore import QFile
    from PySide2.QtGui import  Qt, QPixmap

import os
import re
import nuke
import ffmpeg
import shutil
# import functools

class CustomListWidget(QListWidget):
    def __init__(self, parent=None, start_path="", mode = "file"):
        super().__init__(parent)
        self.start_path = start_path
        self.mode = mode 

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._handle_double_click()
        super().mouseDoubleClickEvent(event)

    def _handle_double_click(self):
        if self.mode == 'folder':
            self.open_folder_dialog()
        else:
            self.open_file_dialog()

    def open_file_dialog(self):
        if not self.start_path:
            QMessageBox.warning(self, "Error", "The start path is not set.")
            return

        # Open file dialog to select files
        file_dialog = QFileDialog(self, "Select Files", self.start_path, "All Files (*)")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setViewMode(QFileDialog.List)
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                for file_path in selected_files:
                    file_name = os.path.basename(file_path)
                    self.addItem(file_name)
                # QMessageBox.information(self, "Files Selected", f"You selected:\n{file_path}")
   
    def open_folder_dialog(self):
        if not self.start_path:
            QMessageBox.warning(self, "Error", "The start path is not set.")
            return

        QMessageBox.information(self, "Folder Selected", "Please select folders for exr files")
        folder = QFileDialog.getExistingDirectory(self, "Select a Folder", self.start_path)
        
        if folder:
            file_name = os.path.basename(folder)
            self.addItem(file_name)
        else:
            QMessageBox.warning(self, "No Selection", "No folder was selected.")


class Publish(QWidget):

    def __init__(self):
        super().__init__()         

        ui_file_path = "C:/Users/LEE JIYEON/yummy/pipeline/scripts/publish/publish_ver5.ui"
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()                                      
        self.ui = loader.load(ui_file, self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint) # UI 최상단 고정
        ui_file.close()

        self.setup_file_in_groubBox_from_Dialog()
        self.setup_top_bar()
        self.setup_tablewidget_basket()

        self._collect_path()

        # Signal
        self.ui.pushButton_add_to_basket.clicked.connect(self.add_nk_item_tablewidget_basket)
        self.ui.pushButton_add_to_basket.clicked.connect(self.add_exr_item_tablewidget_basket)
        self.ui.pushButton_add_to_basket.clicked.connect(self.add_mov_item_tablewidget_basket)
        self.ui.pushButton_version.clicked.connect(self.increase_version_and_save_file)
    
    def setup_file_in_groubBox_from_Dialog(self):

        # nk_page
        nk_page = QWidget()
        layout1 = QVBoxLayout(nk_page)
        nk_file_path = os.path.dirname(nuke.scriptName())
        self.nk_file_listwidget = CustomListWidget(start_path = nk_file_path, mode="file")  # Use custom list widget
        self.nk_file_listwidget.setSelectionMode(QListWidget.MultiSelection)    # multi select listwidget_item
        self.nk_file_listwidget.setObjectName("nk_file_listwidget")
        layout1.addWidget(self.nk_file_listwidget)
        self.ui.groupBox_nk.setLayout(layout1)

        # exr_page
        exr_page = QWidget()
        layout2 = QVBoxLayout(exr_page)
        exr_folder_path = nk_file_path.split("work")[0]+"exr/"
        self.exr_file_listwidget = CustomListWidget(start_path = exr_folder_path, mode = "folder")  # Use custom list widget
        self.exr_file_listwidget.setSelectionMode(QListWidget.MultiSelection)   # multi select listwidget_item
        self.exr_file_listwidget.setObjectName("exr_file_listwidget")
        layout2.addWidget(self.exr_file_listwidget)
        self.ui.groupBox_exr.setLayout(layout2)

        # mov_page
        mov_page = QWidget()
        layout3 = QVBoxLayout(mov_page)
        mov_file_path = nk_file_path.split("work")[0]+"mov/"
        self.mov_file_listwidget = CustomListWidget(start_path = mov_file_path, mode = "file")  # Use custom list widget
        self.mov_file_listwidget.setSelectionMode(QListWidget.MultiSelection)   # multi select listwidget_item
        self.mov_file_listwidget.setObjectName("mov_file_listwidget")
        layout3.addWidget(self.mov_file_listwidget)
        self.ui.groupBox_mov.setLayout(layout3)

    def setup_top_bar(self):

        nk_file_path = nuke.scriptName()
        split = nk_file_path.split("/")
        project_name = split[5]
        shot_code = split[8]
        team_name = split[9]
        self.ui.label_project_name.setText(project_name)
        self.ui.label_shot_code.setText(shot_code)
        self.ui.label_team_name.setText(team_name)

    def _collect_path(self):
        
        self.current_nk_file_path = nuke.scriptName()
        self.work_path = f"{os.path.dirname(self.current_nk_file_path)}/"
        self.dev_path = self.work_path.split("work")[0]
        self.exr_folder_path = f"{self.dev_path}exr/"
        self.mov_file_path = f"{self.dev_path}mov/"

        print(self.work_path)
        print(self.dev_path)
        print(self.exr_folder_path)
        print(self.mov_file_path)

#===================================================================

    def setup_tablewidget_basket(self):

        self.ui.tableWidget_basket.setHorizontalHeaderLabels(["Publish File", "File Info"])
        self.ui.tableWidget_basket.setVerticalHeaderLabels(["nk", "exr", "mov"])

        row_count = self.ui.tableWidget_basket.rowCount()
        height = 85
        for row in range(row_count):
            self.ui.tableWidget_basket.setRowHeight(row, height)

        self.add_nk_item_tablewidget_basket()
        self.add_exr_item_tablewidget_basket()
        self.add_mov_item_tablewidget_basket()

    def add_nk_item_tablewidget_basket(self):
        
        ### nk item ###
        nk_selected_files = self.nk_file_listwidget.selectedItems()
        for file in nk_selected_files:
            nk_item = QTableWidgetItem()
            nk_selected_file = file.text()
            nk_item.setText(nk_selected_file)
            self.ui.tableWidget_basket.setItem(0, 0, nk_item)

            nk_info_dict = self._get_nk_validation_info()
            nk_info_text = "\n".join(f"{key} : {value}" for key, value in nk_info_dict.items())
            nk_validation_info = QTableWidgetItem(nk_info_text)
            nk_validation_info.setTextAlignment(Qt.AlignLeft | Qt.AlignTop) # 왼쪽 정렬, 위쪽 정렬
            self.ui.tableWidget_basket.setItem(0, 1, nk_validation_info)

    def add_exr_item_tablewidget_basket(self):

        ### exr item ###
        exr_selected_folders = self.exr_file_listwidget.selectedItems()
        for folder in exr_selected_folders:
            exr_item = QTableWidgetItem()
            exr_selected_folder = folder.text()
            exr_item.setText(exr_selected_folder)
            self.ui.tableWidget_basket.setItem(1, 0, exr_item)

            exr_file_path = f"{self.exr_folder_path}{exr_selected_folder}"
            exr_files = os.listdir(exr_file_path)
            for file in exr_files:
                self.exr_full_path = f"{exr_file_path}/{file}"

                exr_validation_info_dict = self._get_exr_and_mov_validation_info(self.exr_full_path)
                exr_info_text = "\n".join(f"{key} : {value}" for key, value in exr_validation_info_dict.items())
                exr_validation_info = QTableWidgetItem(exr_info_text)
                exr_validation_info.setTextAlignment(Qt.AlignLeft | Qt.AlignTop) # 왼쪽 정렬, 위쪽 정렬
                self.ui.tableWidget_basket.setItem(1, 1, exr_validation_info)

    def add_mov_item_tablewidget_basket(self):

        ### mov item ###
        mov_selected_files = self.mov_file_listwidget.selectedItems()
        for file in mov_selected_files:
            mov_item = QTableWidgetItem()
            mov_selected_file = file.text()
            mov_item.setText(mov_selected_file)
            self.ui.tableWidget_basket.setItem(2, 0, mov_item)

            mov_new_path = f"{self.mov_file_path}{mov_selected_file}"
        
            mov_validation_info_dict = self._get_exr_and_mov_validation_info(mov_new_path)
            mov_info_item = "\n".join(f"{key} : {value}" for key, value in mov_validation_info_dict.items())
            mov_validation_info = QTableWidgetItem(mov_info_item)
            mov_validation_info.setTextAlignment(Qt.AlignLeft | Qt.AlignTop) # 왼쪽 정렬, 위쪽 정렬
            self.ui.tableWidget_basket.setItem(2, 1, mov_validation_info)

    def _get_nk_validation_info(self):

        nk_file_validation_dict = {}
        root = nuke.root()
        path = root["name"].value()                     # file path
        extend = path.split(".")[-1]                    # extendation
        colorspace = root["colorManagement"].value()    # colorspace
        nuke_version = nuke.NUKE_VERSION_STRING         # nk version
        
        nk_file_validation_dict["file_path"] = path
        nk_file_validation_dict["extend"] = extend
        nk_file_validation_dict["colorspace"] = colorspace
        nk_file_validation_dict["nuke_version"] = nuke_version

        return nk_file_validation_dict

    def _get_exr_and_mov_validation_info(self, file_path):

            file_validation_info_dict = {}
            probe = ffmpeg.probe(file_path)

            # extract video_stream
            video_stream = next((stream for stream in probe['streams']if stream['codec_type'] == 'video'),None)
            codec_name = video_stream['codec_name']
            colorspace = video_stream.get('color_space', "N/A")
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            # a = video_stream.keys()
            # print(a)

            resolution = f"{width}x{height}"

            if file_path.split(".")[-1] == "mov":
                frame = int(video_stream['nb_frames'])

            elif file_path.split(".")[-1] == "exr":
                frame = 1

            # file_validation dictionary
            file_validation_info_dict = {
                "file_path": file_path,
                "codec_name": codec_name,
                "colorspace": colorspace,
                "resolution": resolution,
                "frame": frame
            }
            # print(file_validation_info_dict)
            return file_validation_info_dict

#==================================================================

    # def display_thumbnail(self):

    #     self.ui.label_thumbnail.clear()

    #     self.current_file_path = nuke.scriptName()
    #     nk_file_name = os.path.basename(self.current_file_path)
    #     png_file_name = nk_file_name.split(".")[0]

    #     image_path = f"C:/Users/LEE JIYEON/yummy/pipeline/scripts/publish/{png_file_name}.png"
    #     thumbnail = QPixmap(image_path)
    #     scaled_thumbnail = thumbnail.scaled(230, 190, Qt.AspectRatioMode.KeepAspectRatio)

    #     if os.path.exists(image_path):
    #         self.ui.label_thumbnail.setPixmap(scaled_thumbnail)
    #         return

    #     self.save_frame_as_thumbnail(image_path, 1001)

    # def save_frame_as_thumbnail(self, file_path, frame_number):
        
    #     reformat_node = nuke.createNode("Reformat")
    #     write_node = nuke.createNode("Write")
    #     write_node.setInput(0, reformat_node)

    #     new_format_name = 'HD_1080'
    #     formats = nuke.formats()
    #     new_format = next((fmt for fmt in formats if fmt.name() == new_format_name), None)

    #     if new_format:
    #         reformat_node['format'].setValue(new_format)

    #     write_node["file"].setValue(file_path)
    #     write_node["file_type"].setValue("png")
        
    #     write_node["first"].setValue(frame_number)
    #     write_node["last"].setValue(frame_number)
        
    #     # render
    #     nuke.execute(write_node, frame_number, frame_number)
        
    #     # clean up
    #     nuke.delete(write_node)
    #     nuke.delete(reformat_node)

#==================================================================
    def _make_new_version_path(self):
        """
        1.로컬패스를 /로 split 한다.
        2.project인자를 찾는다
        3.그 다음오는 인자는 project_name
        4.서버패스에서 같은 project_name을 찾는다
         
        """
        
        start_path = ""


    def _make_new_version_path(self):
        table_items = self.ui.tableWidget_basket.selectedItems()

        path = []
        for item in table_items:
            if item:
                nk_item_text = self.ui.tableWidget_basket.item(0, 0).text()
                nk_path = f"{self.work_path}{nk_item_text}"
                print(nk_path)
                
                exr_item_text = self.ui.tableWidget_basket.item(1, 0).text()
                exr_path = f"{self.exr_folder_path}{exr_item_text}"
                print(exr_path)
                
                mov_item_text = self.ui.tableWidget_basket.item(2, 0).text()
                mov_path = f"{self.mov_file_path}{mov_item_text}"
                print(mov_path)
                
            else:
                print("아이템이 없습니다.")
            
        path.extend([nk_path, exr_path, mov_path])

        return path
    
    def increase_version_and_save_file(self):
        """
        파일 경로 받아서 버전업시키고 save하는 함수
        """
        paths = self._make_new_version_path()

        for path in paths:
            base, ext = os.path.splitext(path)
            version_pattern = re.compile("v\d{3}")
            match = version_pattern.search(base)
            current_version = match.group(0)
            new_number = int(current_version[1:]) + 1
            new_version = f"v{new_number:03}"   # 현재 버전 번호가 존재하면 버전 번호를 증가
            new_base = base.replace(current_version, new_version)

            if ext == ".nknc":
                new_file_path = f"{new_base}{ext}"
                # print(new_file_path)
                nuke.scriptSaveAs(new_file_path)
                print("nk file이 version-up 되었습니다.")

            elif ext == ".mov":
                new_file_path = f"{new_base}{ext}"
                # print(new_file_path)
                shutil.copy2(base+ext, new_file_path)
                print("mov file이 version-up 되었습니다.")

            else:
                new_folder_path = new_base
                os.makedirs(new_folder_path)
                # print(base)
                exr_files = os.listdir(base)
                # print(exr_files)
                for exr_file in exr_files:
                    current_path = f"{base}/{exr_file}"
                    # print(current_path)
                    file_path = f"{new_folder_path}/{exr_file}"
                    # print(file_path)
                    match = version_pattern.search(exr_file)
                    exr_current_version = match.group(0)
                    exr_new_number = int(exr_current_version[1:]) + 1
                    exr_new_version = f"v{exr_new_number:03}"   # 현재 버전 번호가 존재하면 버전 번호를 증가
                    exr_new_path = file_path.replace(exr_current_version, exr_new_version)
                    # print(exr_new_path)
                    shutil.copy2(current_path, exr_new_path)

    # def copy_file_to_pub(self):
    #     nk_file
    #     exr_file
    #     mov_file
    #     shutil.copy2()

    #=========================================================
    # def copy_selected_files_to_pub(self):
    #     # Get selected items
    #     selected_items = self.tableWidget.selectedItems()
    #     if not selected_items:
    #         print("No files selected.")
    #         return

    #     # Ask user for destination folder
    #     destination_folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
    #     if not destination_folder:
    #         print("No destination folder selected.")
    #         return

    #     for item in selected_items:
    #         file_name = item.text()
    #         source_path = os.path.join(os.getcwd(), file_name)  # Example source path, replace with actual path
    #         destination_path = os.path.join(destination_folder, file_name)

    #         # Copy file to destination
    #         if os.path.exists(source_path):
    #             shutil.copy(source_path, destination_path)
    #             print(f"Copied {file_name} to {destination_folder}")
    #         else:
    #             print(f"Source file {source_path} does not exist.")
    

if __name__ == "__main__":
    app = QApplication()
    win = Publish()
    win.show()
    app.exec()
