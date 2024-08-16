# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHeaderView,
    QSizePolicy, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1315, 862)
        self.tabWidget_file_structure = QTabWidget(Form)
        self.tabWidget_file_structure.setObjectName(u"tabWidget_file_structure")
        self.tabWidget_file_structure.setGeometry(QRect(-10, 20, 1291, 781))
        font = QFont()
        font.setBold(True)
        self.tabWidget_file_structure.setFont(font)
        self.tabWidget_file_structure.setTabPosition(QTabWidget.North)
        self.tabWidget_file_structure.setTabShape(QTabWidget.Rounded)
        self.tabWidget_file_structure.setDocumentMode(False)
        self.tabWidget_file_structure.setTabsClosable(False)
        self.tabWidget_file_structure.setMovable(False)
        self.tab_shot = QWidget()
        self.tab_shot.setObjectName(u"tab_shot")
        self.treeWidget_shot_file_sturcture = QTreeWidget(self.tab_shot)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget_shot_file_sturcture.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_shot_file_sturcture.setObjectName(u"treeWidget_shot_file_sturcture")
        self.treeWidget_shot_file_sturcture.setGeometry(QRect(10, 80, 271, 421))
        self.gridLayoutWidget = QWidget(self.tab_shot)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(410, 60, 481, 461))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.comboBox = QComboBox(self.tab_shot)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(10, 10, 121, 27))
        self.tabWidget_file_structure.addTab(self.tab_shot, "")
        self.tab_my_task = QWidget()
        self.tab_my_task.setObjectName(u"tab_my_task")
        self.tabWidget_file_structure.addTab(self.tab_my_task, "")
        self.tab_clip = QWidget()
        self.tab_clip.setObjectName(u"tab_clip")
        self.tabWidget_file_structure.addTab(self.tab_clip, "")

        self.retranslateUi(Form)

        self.tabWidget_file_structure.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tabWidget_file_structure.setTabText(self.tabWidget_file_structure.indexOf(self.tab_shot), QCoreApplication.translate("Form", u"SHOT", None))
        self.tabWidget_file_structure.setTabText(self.tabWidget_file_structure.indexOf(self.tab_my_task), QCoreApplication.translate("Form", u"MY TASK", None))
        self.tabWidget_file_structure.setTabText(self.tabWidget_file_structure.indexOf(self.tab_clip), QCoreApplication.translate("Form", u"Clip_LIB", None))
    # retranslateUi

