# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'singin_window.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QSizePolicy, QStackedWidget,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(363, 227)
        Form.setStyleSheet(u"")
        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(10, 10, 341, 201))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.frame = QFrame(self.page)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 20, 321, 171))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayoutWidget = QWidget(self.frame)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(30, 70, 261, 80))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_email = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_email.setObjectName(u"lineEdit_email")
        self.lineEdit_email.setStyleSheet(u"")

        self.gridLayout.addWidget(self.lineEdit_email, 0, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.comboBox_project_name = QComboBox(self.gridLayoutWidget)
        self.comboBox_project_name.setObjectName(u"comboBox_project_name")
        self.comboBox_project_name.setStyleSheet(u"")

        self.gridLayout.addWidget(self.comboBox_project_name, 1, 1, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(110, 20, 91, 41))
        self.label_3.setStyleSheet(u"")
        self.label_3.setTextFormat(Qt.AutoText)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.label_qmovie = QLabel(self.page_2)
        self.label_qmovie.setObjectName(u"label_qmovie")
        self.label_qmovie.setGeometry(QRect(30, 50, 281, 111))
        self.stackedWidget.addWidget(self.page_2)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"E-mail      ", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Project", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:700;\">Sign in</span></p></body></html>", None))
        self.label_qmovie.setText("")
    # retranslateUi

