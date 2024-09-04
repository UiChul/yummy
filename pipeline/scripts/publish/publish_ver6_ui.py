# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'publish_ver6.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(685, 974)
        Form.setStyleSheet(u"background-color: rgb(54, 54, 54);")
        self.horizontalLayoutWidget = QWidget(Form)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(22, 10, 461, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_project_name = QLabel(self.horizontalLayoutWidget)
        self.label_project_name.setObjectName(u"label_project_name")
        font = QFont()
        font.setFamilies([u"Cantarell"])
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(True)
        self.label_project_name.setFont(font)
        self.label_project_name.setStyleSheet(u"font: 700 oblique 11pt \"Cantarell\";")
        self.label_project_name.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_project_name)

        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label)

        self.label_team_name = QLabel(self.horizontalLayoutWidget)
        self.label_team_name.setObjectName(u"label_team_name")
        self.label_team_name.setFont(font)
        self.label_team_name.setStyleSheet(u"font: 700 oblique 11pt \"Cantarell\";")
        self.label_team_name.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_team_name)

        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_2)

        self.label_shot_code = QLabel(self.horizontalLayoutWidget)
        self.label_shot_code.setObjectName(u"label_shot_code")
        self.label_shot_code.setFont(font)
        self.label_shot_code.setStyleSheet(u"font: 700 oblique 11pt \"Cantarell\";")
        self.label_shot_code.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_shot_code)

        self.horizontalLayoutWidget_3 = QWidget(Form)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(30, 550, 641, 41))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_item_count = QLabel(self.horizontalLayoutWidget_3)
        self.label_item_count.setObjectName(u"label_item_count")
        self.label_item_count.setMaximumSize(QSize(20, 16777215))
        font1 = QFont()
        font1.setPointSize(12)
        self.label_item_count.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_item_count)

        self.label_count_basket_items = QLabel(self.horizontalLayoutWidget_3)
        self.label_count_basket_items.setObjectName(u"label_count_basket_items")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.label_count_basket_items.setFont(font2)

        self.horizontalLayout_3.addWidget(self.label_count_basket_items)

        self.pushButton_delete = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        self.pushButton_delete.setMaximumSize(QSize(40, 35))
        self.pushButton_delete.setStyleSheet(u"background-color: rgb(80, 80, 80);")

        self.horizontalLayout_3.addWidget(self.pushButton_delete)

        self.tableWidget_basket = QTableWidget(Form)
        if (self.tableWidget_basket.columnCount() < 2):
            self.tableWidget_basket.setColumnCount(2)
        if (self.tableWidget_basket.rowCount() < 3):
            self.tableWidget_basket.setRowCount(3)
        self.tableWidget_basket.setObjectName(u"tableWidget_basket")
        self.tableWidget_basket.setGeometry(QRect(20, 610, 651, 281))
        self.tableWidget_basket.setRowCount(3)
        self.tableWidget_basket.setColumnCount(2)
        self.tableWidget_basket.horizontalHeader().setVisible(True)
        self.tableWidget_basket.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_basket.horizontalHeader().setDefaultSectionSize(140)
        self.tableWidget_basket.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_basket.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_basket.verticalHeader().setDefaultSectionSize(75)
        self.tableWidget_basket.verticalHeader().setHighlightSections(True)
        self.tableWidget_basket.verticalHeader().setStretchLastSection(True)
        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(20, 520, 651, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.horizontalLayoutWidget_2 = QWidget(Form)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(20, 920, 651, 32))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_version = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_version.setObjectName(u"pushButton_version")
        font3 = QFont()
        font3.setFamilies([u"Artifakt Element Book"])
        font3.setBold(False)
        self.pushButton_version.setFont(font3)
        self.pushButton_version.setStyleSheet(u"background-color: rgb(190, 190, 190);\n"
"")

        self.horizontalLayout_2.addWidget(self.pushButton_version)

        self.line_2 = QFrame(self.horizontalLayoutWidget_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line_2)

        self.pushButton_publish = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_publish.setObjectName(u"pushButton_publish")
        font4 = QFont()
        font4.setFamilies([u"Artifakt Element Book"])
        font4.setBold(True)
        self.pushButton_publish.setFont(font4)
        self.pushButton_publish.setStyleSheet(u"background-color: rgb(190, 190, 190);\n"
"")

        self.horizontalLayout_2.addWidget(self.pushButton_publish)

        self.pushButton_add_to_basket = QPushButton(Form)
        self.pushButton_add_to_basket.setObjectName(u"pushButton_add_to_basket")
        self.pushButton_add_to_basket.setGeometry(QRect(20, 480, 651, 27))
        font5 = QFont()
        font5.setFamilies([u"Artifakt Element Book"])
        self.pushButton_add_to_basket.setFont(font5)
        self.pushButton_add_to_basket.setStyleSheet(u"background-color: rgb(80, 80, 80);")
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 70, 651, 381))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_description_exr = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_description_exr.setObjectName(u"lineEdit_description_exr")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_description_exr.sizePolicy().hasHeightForWidth())
        self.lineEdit_description_exr.setSizePolicy(sizePolicy1)
        self.lineEdit_description_exr.setMinimumSize(QSize(150, 0))
        self.lineEdit_description_exr.setMaximumSize(QSize(200, 120))
        self.lineEdit_description_exr.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.lineEdit_description_exr, 5, 2, 2, 1)

        self.groupBox_mov = QGroupBox(self.gridLayoutWidget)
        self.groupBox_mov.setObjectName(u"groupBox_mov")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_mov.sizePolicy().hasHeightForWidth())
        self.groupBox_mov.setSizePolicy(sizePolicy2)
        self.groupBox_mov.setMinimumSize(QSize(0, 0))
        self.groupBox_mov.setMaximumSize(QSize(300, 16777215))
        font6 = QFont()
        font6.setPointSize(14)
        font6.setBold(True)
        self.groupBox_mov.setFont(font6)

        self.gridLayout.addWidget(self.groupBox_mov, 8, 0, 2, 1)

        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setFont(font2)

        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setFont(font2)

        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font7 = QFont()
        font7.setPointSize(8)
        font7.setBold(True)
        self.label_4.setFont(font7)

        self.gridLayout.addWidget(self.label_4, 4, 2, 1, 1)

        self.label_thumbnail_nk = QLabel(self.gridLayoutWidget)
        self.label_thumbnail_nk.setObjectName(u"label_thumbnail_nk")
        sizePolicy1.setHeightForWidth(self.label_thumbnail_nk.sizePolicy().hasHeightForWidth())
        self.label_thumbnail_nk.setSizePolicy(sizePolicy1)
        self.label_thumbnail_nk.setMinimumSize(QSize(150, 0))
        self.label_thumbnail_nk.setMaximumSize(QSize(200, 100))

        self.gridLayout.addWidget(self.label_thumbnail_nk, 2, 1, 2, 1)

        self.groupBox_exr = QGroupBox(self.gridLayoutWidget)
        self.groupBox_exr.setObjectName(u"groupBox_exr")
        sizePolicy2.setHeightForWidth(self.groupBox_exr.sizePolicy().hasHeightForWidth())
        self.groupBox_exr.setSizePolicy(sizePolicy2)
        self.groupBox_exr.setMinimumSize(QSize(0, 0))
        self.groupBox_exr.setMaximumSize(QSize(300, 16777215))
        self.groupBox_exr.setFont(font6)

        self.gridLayout.addWidget(self.groupBox_exr, 5, 0, 2, 1)

        self.label_thumbnail_mov = QLabel(self.gridLayoutWidget)
        self.label_thumbnail_mov.setObjectName(u"label_thumbnail_mov")
        sizePolicy1.setHeightForWidth(self.label_thumbnail_mov.sizePolicy().hasHeightForWidth())
        self.label_thumbnail_mov.setSizePolicy(sizePolicy1)
        self.label_thumbnail_mov.setMinimumSize(QSize(0, 0))
        self.label_thumbnail_mov.setMaximumSize(QSize(200, 100))

        self.gridLayout.addWidget(self.label_thumbnail_mov, 8, 1, 2, 1)

        self.label_10 = QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setFont(font2)

        self.gridLayout.addWidget(self.label_10, 7, 0, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setFont(font7)

        self.gridLayout.addWidget(self.label_7, 7, 1, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setFont(font7)

        self.gridLayout.addWidget(self.label_11, 1, 1, 1, 1)

        self.lineEdit_description_mov = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_description_mov.setObjectName(u"lineEdit_description_mov")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.lineEdit_description_mov.sizePolicy().hasHeightForWidth())
        self.lineEdit_description_mov.setSizePolicy(sizePolicy3)
        self.lineEdit_description_mov.setMinimumSize(QSize(150, 0))
        self.lineEdit_description_mov.setMaximumSize(QSize(200, 120))
        self.lineEdit_description_mov.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.lineEdit_description_mov, 8, 2, 2, 1)

        self.label_thumbnail_exr = QLabel(self.gridLayoutWidget)
        self.label_thumbnail_exr.setObjectName(u"label_thumbnail_exr")
        sizePolicy1.setHeightForWidth(self.label_thumbnail_exr.sizePolicy().hasHeightForWidth())
        self.label_thumbnail_exr.setSizePolicy(sizePolicy1)
        self.label_thumbnail_exr.setMinimumSize(QSize(0, 0))
        self.label_thumbnail_exr.setMaximumSize(QSize(200, 100))

        self.gridLayout.addWidget(self.label_thumbnail_exr, 5, 1, 2, 1)

        self.label_12 = QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setFont(font7)

        self.gridLayout.addWidget(self.label_12, 1, 2, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setFont(font7)

        self.gridLayout.addWidget(self.label_6, 7, 2, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setFont(font7)

        self.gridLayout.addWidget(self.label_5, 4, 1, 1, 1)

        self.groupBox_nk = QGroupBox(self.gridLayoutWidget)
        self.groupBox_nk.setObjectName(u"groupBox_nk")
        sizePolicy2.setHeightForWidth(self.groupBox_nk.sizePolicy().hasHeightForWidth())
        self.groupBox_nk.setSizePolicy(sizePolicy2)
        self.groupBox_nk.setMinimumSize(QSize(0, 0))
        self.groupBox_nk.setMaximumSize(QSize(300, 16777215))
        self.groupBox_nk.setFont(font6)
        self.groupBox_nk.setFlat(False)

        self.gridLayout.addWidget(self.groupBox_nk, 2, 0, 2, 1)

        self.lineEdit_description_nk = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_description_nk.setObjectName(u"lineEdit_description_nk")
        sizePolicy1.setHeightForWidth(self.lineEdit_description_nk.sizePolicy().hasHeightForWidth())
        self.lineEdit_description_nk.setSizePolicy(sizePolicy1)
        self.lineEdit_description_nk.setMinimumSize(QSize(150, 0))
        self.lineEdit_description_nk.setMaximumSize(QSize(200, 120))
        self.lineEdit_description_nk.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.lineEdit_description_nk, 2, 2, 2, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_project_name.setText(QCoreApplication.translate("Form", u"PROJECT_NAME", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_team_name.setText(QCoreApplication.translate("Form", u"TEAM_NAME", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_shot_code.setText(QCoreApplication.translate("Form", u"SHOT_CODE", None))
        self.label_item_count.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_count_basket_items.setText(QCoreApplication.translate("Form", u"items upload by Publisher.", None))
        self.pushButton_delete.setText("")
        self.pushButton_version.setText(QCoreApplication.translate("Form", u"Version upload", None))
        self.pushButton_publish.setText(QCoreApplication.translate("Form", u"Publish upload", None))
        self.pushButton_add_to_basket.setText(QCoreApplication.translate("Form", u"ADD", None))
        self.groupBox_mov.setTitle("")
        self.label_9.setText(QCoreApplication.translate("Form", u"EXR", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"NK", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Description", None))
        self.label_thumbnail_nk.setText("")
        self.groupBox_exr.setTitle("")
        self.label_thumbnail_mov.setText("")
        self.label_10.setText(QCoreApplication.translate("Form", u"MOV", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Thumbnail", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Thumbnail", None))
        self.label_thumbnail_exr.setText("")
        self.label_12.setText(QCoreApplication.translate("Form", u"Description", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Description", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Thumbnail", None))
        self.groupBox_nk.setTitle("")
    # retranslateUi

