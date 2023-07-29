# Form implementation generated from reading ui file 'App_Master.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMenu
import psycopg2
import sys
import configparser
from Database_Connection import createConnection
from config import config
from datetime import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from QueryOffer_Window import Ui_QueryOffer_Window
from QueryOrder_Window import Ui_QueryOrder_Window
from QueryDoc_Window import Ui_QueryDoc_Window
from QueryTags_Window import Ui_QueryTags_Window
from EditTags_Commercial_Window import Ui_EditTags_Window
from EditUser_Menu import Ui_EditUser_Menu
from EditDB_Menu import Ui_EditDB_Menu
from ImportDB_Menu import Ui_ImportDB_Menu
from QueryTableChanges_Window import Ui_QueryTableChanges_Window
from AddTask_Window import Ui_AddTask_Window
from EditPassword_Window import Ui_EditPasswordWindow



class ImageCalendarWidget(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_dates = []

    def set_task_dates(self, dates):
        self.task_dates = dates
        self.updateCells()

    def paintCell(self, painter, rect, date):
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)

        if date in self.task_dates:
            image_path = "//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/Flag.png" 
            image = QtGui.QImage(image_path)
            if not image.isNull():
                image_scaled = image.scaled(rect.width() // 4, rect.height() // 4, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                image_rect = image_scaled.rect()
                image_rect.moveTopRight(rect.topRight() - QtCore.QPoint(2, -5))
                painter.drawImage(image_rect, image_scaled)


class Ui_App_Master(object):
    def __init__(self, name, username):
        self.name=name
        self.username=username
    # def __init__(self):
    #     self.name='Enrique Serrano'
    #     self.username='e.serranog'


    def setupUi(self, App_Master):
        App_Master.setObjectName("App_Master")
        App_Master.resize(1254, 860)
        App_Master.setMinimumSize(QtCore.QSize(945, 860))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        App_Master.setWindowIcon(icon)
        App_Master.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=App_Master)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.FrameApp = QtWidgets.QVBoxLayout()
        self.FrameApp.setObjectName("FrameApp")
        self.Header = QtWidgets.QHBoxLayout()
        self.Header.setContentsMargins(-1, 0, -1, -1)
        self.Header.setObjectName("Header")
        self.LogoIcon = QtWidgets.QLabel(parent=self.frame)
        self.LogoIcon.setMinimumSize(QtCore.QSize(220, 52))
        self.LogoIcon.setMaximumSize(QtCore.QSize(220, 52))
        self.LogoIcon.setText("")
        self.LogoIcon.setPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/Logo.ico"))
        self.LogoIcon.setScaledContents(True)
        self.LogoIcon.setObjectName("LogoIcon")
        self.Header.addWidget(self.LogoIcon)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem)
        self.Button_Users = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Users.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_Users.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_Users.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Users.setStyleSheet("QPushButton{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(3, 174, 236);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(200, 200, 200);\n"
"    border-radius: 10px;\n"
"}")
        self.Button_Users.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/User_Edit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_Users.setIcon(icon1)
        self.Button_Users.setIconSize(QtCore.QSize(40, 40))
        self.Button_Users.setObjectName("Button_Users")
        self.Header.addWidget(self.Button_Users)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem1)
        self.Button_DBEdit = QtWidgets.QPushButton(parent=self.frame)
        self.Button_DBEdit.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_DBEdit.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_DBEdit.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_DBEdit.setStyleSheet("QPushButton{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(3, 174, 236);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(200, 200, 200);\n"
"    border-radius: 10px;\n"
"}")
        self.Button_DBEdit.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/Database_Admin.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_DBEdit.setIcon(icon2)
        self.Button_DBEdit.setIconSize(QtCore.QSize(40, 40))
        self.Button_DBEdit.setObjectName("Button_DBEdit")
        self.Header.addWidget(self.Button_DBEdit)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem2)
        self.Button_DBImport = QtWidgets.QPushButton(parent=self.frame)
        self.Button_DBImport.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_DBImport.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_DBImport.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_DBImport.setStyleSheet("QPushButton{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(3, 174, 236);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(200, 200, 200);\n"
"    border-radius: 10px;\n"
"}")
        self.Button_DBImport.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/Database_Import.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_DBImport.setIcon(icon3)
        self.Button_DBImport.setIconSize(QtCore.QSize(40, 40))
        self.Button_DBImport.setObjectName("Button_DBImport")
        self.Header.addWidget(self.Button_DBImport)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem3)
        self.Button_DBChanges = QtWidgets.QPushButton(parent=self.frame)
        self.Button_DBChanges.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_DBChanges.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_DBChanges.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_DBChanges.setStyleSheet("QPushButton{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(3, 174, 236);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(200, 200, 200);\n"
"    border-radius: 10px;\n"
"}")
        self.Button_DBChanges.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/Database_Changes.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_DBChanges.setIcon(icon4)
        self.Button_DBChanges.setIconSize(QtCore.QSize(40, 40))
        self.Button_DBChanges.setObjectName("Button_DBChanges")
        self.Header.addWidget(self.Button_DBChanges)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem4)
        self.Button_NewTask = QtWidgets.QPushButton(parent=self.frame)
        self.Button_NewTask.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_NewTask.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_NewTask.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_NewTask.setStyleSheet("QPushButton{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(3, 174, 236);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(200, 200, 200);\n"
"    border-radius: 10px;\n"
"}")
        self.Button_NewTask.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/Task_New.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_NewTask.setIcon(icon5)
        self.Button_NewTask.setIconSize(QtCore.QSize(40, 40))
        self.Button_NewTask.setObjectName("Button_NewTask")
        self.Header.addWidget(self.Button_NewTask)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem5)
        self.HeaderName = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.HeaderName.setFont(font)
        self.HeaderName.setStyleSheet("color:rgb(3, 174, 236)")
        self.HeaderName.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.HeaderName.setObjectName("HeaderName")
        self.Header.addWidget(self.HeaderName)
        spacerItem6 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem6)
        self.Button_Profile = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Profile.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_Profile.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_Profile.setStyleSheet("QPushButton{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(3, 174, 236);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(200, 200, 200);\n"
"    border-radius: 10px;\n"
"}")
        self.Button_Profile.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/User.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_Profile.setIcon(icon6)
        self.Button_Profile.setIconSize(QtCore.QSize(40, 40))
        self.Button_Profile.setObjectName("Button_Profile")
        self.Header.addWidget(self.Button_Profile)
        self.FrameApp.addLayout(self.Header)
        spacerItem7 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.FrameApp.addItem(spacerItem7)
        self.PrincipalScreen = QtWidgets.QHBoxLayout()
        self.PrincipalScreen.setObjectName("PrincipalScreen")
        self.ButtonFrame = QtWidgets.QFrame(parent=self.frame)
        self.ButtonFrame.setMinimumSize(QtCore.QSize(220, 0))
        self.ButtonFrame.setMaximumSize(QtCore.QSize(220, 16777215))
        self.ButtonFrame.setAutoFillBackground(False)
        self.ButtonFrame.setStyleSheet("QFrame{\n"
"    background-color: rgb(3, 174, 236);\n"
"}\n"
"\n"
"QPushButton{\n"
"    border: 1px solid transparent;\n"
"    color: rgb(3, 174, 236);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    border: 1px solid transparent;\n"
"    border-color: rgb(0, 0, 0);\n"
"    color: rgb(0,0,0);\n"
"    background-color: rgb(200, 200, 200);\n"
"    border-radius: 10px;\n"
"}")
        self.ButtonFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ButtonFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ButtonFrame.setObjectName("ButtonFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.ButtonFrame)
        self.verticalLayout_3.setContentsMargins(9, 0, -1, 0)
        self.verticalLayout_3.setSpacing(25)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Button_QueryOffer = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryOffer.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_QueryOffer.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_QueryOffer.setFont(font)
        self.Button_QueryOffer.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/Offer_Search.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryOffer.setIcon(icon7)
        self.Button_QueryOffer.setIconSize(QtCore.QSize(40, 40))
        self.Button_QueryOffer.setObjectName("Button_QueryOffer")
        self.verticalLayout_3.addWidget(self.Button_QueryOffer)
        self.Button_QueryOrder = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryOrder.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_QueryOrder.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_QueryOrder.setFont(font)
        self.Button_QueryOrder.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/Order_Search.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryOrder.setIcon(icon8)
        self.Button_QueryOrder.setIconSize(QtCore.QSize(40, 40))
        self.Button_QueryOrder.setObjectName("Button_QueryOrder")
        self.verticalLayout_3.addWidget(self.Button_QueryOrder)
        self.Button_QueryDoc = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryDoc.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_QueryDoc.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_QueryDoc.setFont(font)
        self.Button_QueryDoc.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/Documents_Search.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryDoc.setIcon(icon9)
        self.Button_QueryDoc.setIconSize(QtCore.QSize(40, 40))
        self.Button_QueryDoc.setObjectName("Button_QueryDoc")
        self.verticalLayout_3.addWidget(self.Button_QueryDoc)
        self.Button_QueryTag = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryTag.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_QueryTag.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_QueryTag.setFont(font)
        self.Button_QueryTag.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/TAG_Search.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryTag.setIcon(icon10)
        self.Button_QueryTag.setIconSize(QtCore.QSize(40, 40))
        self.Button_QueryTag.setObjectName("Button_QueryTag")
        self.verticalLayout_3.addWidget(self.Button_QueryTag)
        self.Button_EditTag = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_EditTag.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_EditTag.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_EditTag.setFont(font)
        self.Button_EditTag.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/TAG_Edit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_EditTag.setIcon(icon11)
        self.Button_EditTag.setIconSize(QtCore.QSize(40, 40))
        self.Button_EditTag.setObjectName("Button_EditTag")
        self.verticalLayout_3.addWidget(self.Button_EditTag)
        self.PrincipalScreen.addWidget(self.ButtonFrame)
        spacerItem8 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.PrincipalScreen.addItem(spacerItem8)
        self.MainLayout = QtWidgets.QVBoxLayout()
        self.MainLayout.setObjectName("MainLayout")
        self.tableMaster = QtWidgets.QTableWidget(parent=self.frame)
        self.tableMaster.setMinimumSize(QtCore.QSize(650, 280))
        self.tableMaster.setObjectName("tableMaster")
        self.tableMaster.setColumnCount(0)
        self.tableMaster.setRowCount(0)
        self.tableMaster.verticalHeader().setVisible(False)
        self.MainLayout.addWidget(self.tableMaster)
        spacerItem9 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.MainLayout.addItem(spacerItem9)
        self.BottomLayout = QtWidgets.QHBoxLayout()
        self.BottomLayout.setContentsMargins(-1, 0, -1, -1)
        self.BottomLayout.setObjectName("BottomLayout")
        self.Calendar = ImageCalendarWidget(parent=self.frame)
        self.Calendar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Calendar.sizePolicy().hasHeightForWidth())
        self.Calendar.setSizePolicy(sizePolicy)
        self.Calendar.setMinimumSize(QtCore.QSize(200, 400))
        self.Calendar.setMaximumSize(QtCore.QSize(583, 400))
        self.Calendar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.Calendar.setStyleSheet("QCalendarWidget QWidget{\n"
"background-color: rgb(3, 174, 236);\n"
"}\n"
"\n"
"QCalendarWidget QTableView{\n"
"    background-color: white;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton {\n"
"    color: white;\n"
"    font-size:20px;\n"
"    icon-size:30px 30px;\n"
"    background-color:rgb(3, 174, 236);\n"
"}\n"
"\n"
"QCalendarWidget QToolButton::hover {\n"
"    background-color : #019ad2;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton::pressed {\n"
"    background-color: rgb(1, 140, 190);\n"
"    border: 3px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QCalendarWidget QSpinBox{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: 2px solid;\n"
"    border-color: rgb(3,174, 236);\n"
"}\n"
"\n"
"QCalendarWidget QAbstractItemView:enabled{\n"
"    selection-background-color: rgb(3, 174, 236);\n"
"    selection-color: white;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth {\n"
"    qproperty-icon: url(//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/back_arrow.png);\n"
"}\n"
"#qt_calendar_nextmonth {\n"
"    qproperty-icon: url(//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/forward_arrow.png);\n"
"}")
        self.Calendar.setSelectedDate(QtCore.QDate.currentDate())
        self.Calendar.setGridVisible(True)
        self.Calendar.setNavigationBarVisible(True)
        self.Calendar.setDateEditEnabled(True)
        self.Calendar.setObjectName("Calendar")
        self.BottomLayout.addWidget(self.Calendar)
        self.MainLayout.addLayout(self.BottomLayout)
        self.PrincipalScreen.addLayout(self.MainLayout)
        self.FrameApp.addLayout(self.PrincipalScreen)
        self.gridLayout.addLayout(self.FrameApp, 3, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        App_Master.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=App_Master)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1254, 22))
        self.menubar.setObjectName("menubar")
        App_Master.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=App_Master)
        self.statusbar.setObjectName("statusbar")
        App_Master.setStatusBar(self.statusbar)

        self.retranslateUi(App_Master)
        QtCore.QMetaObject.connectSlotsByName(App_Master)

        self.Button_QueryOffer.clicked.connect(self.query_offer)
        self.Button_QueryOrder.clicked.connect(self.query_order)
        self.Button_QueryDoc.clicked.connect(self.query_doc)
        self.Button_QueryTag.clicked.connect(self.query_tag)
        self.Button_EditTag.clicked.connect(self.edit_tag)
        self.Button_Users.clicked.connect(self.user_edition)
        self.Button_DBEdit.clicked.connect(self.editdb)
        self.Button_DBImport.clicked.connect(self.importdb)
        self.Button_DBChanges.clicked.connect(self.dbchanges)
        self.Button_NewTask.clicked.connect(self.newtask)
        self.Button_Profile.clicked.connect(self.showMenu)
        self.Calendar.selectionChanged.connect(self.show_selected_date_tasks)
        self.setup_task_dates()


    def retranslateUi(self, App_Master):
        _translate = QtCore.QCoreApplication.translate
        App_Master.setWindowTitle(_translate("App_Master", "ERP EIPSA"))
        self.Button_Users.setToolTip(_translate("App_Master", "Editar Usuarios"))
        self.Button_DBEdit.setToolTip(_translate("App_Master", "Editar BBDD"))
        self.Button_DBImport.setToolTip(_translate("App_Master", "Importar a BBDD"))
        self.Button_DBChanges.setToolTip(_translate("App_Master", "Tablas De Cambios"))
        self.Button_NewTask.setToolTip(_translate("App_Master", "Crear Tarea"))
        self.HeaderName.setText(_translate("App_Master", self.name))
        self.Button_QueryOffer.setText(_translate("App_Master", "    Consultar Ofertas"))
        self.Button_QueryOrder.setText(_translate("App_Master", "   Consultar Pedidos"))
        self.Button_QueryDoc.setText(_translate("App_Master", "   Consultar Docum."))
        self.Button_QueryTag.setText(_translate("App_Master", "    Consultar TAG(s)"))
        self.Button_EditTag.setText(_translate("App_Master", "    Editar TAG(s)"))
        self.tableMaster.setSortingEnabled(True)


    def query_offer(self):
        self.query_offer_window=QtWidgets.QMainWindow()
        self.ui=Ui_QueryOffer_Window()
        self.ui.setupUi(self.query_offer_window)
        self.query_offer_window.show()


    def query_order(self):
        self.query_order_window=QtWidgets.QMainWindow()
        self.ui=Ui_QueryOrder_Window()
        self.ui.setupUi(self.query_order_window)
        self.query_order_window.show()


    def query_doc(self):
        self.querydoc_menu=QtWidgets.QMainWindow()
        self.ui=Ui_QueryDoc_Window()
        self.ui.setupUi(self.querydoc_menu)
        self.querydoc_menu.show()


    def query_tag(self):
        # self.querytag_window=QtWidgets.QMainWindow()
        # self.ui=Ui_QueryTags_Window()
        # self.ui.setupUi(self.querytag_window)
        # self.querytag_window.show()

        dlg = QtWidgets.QMessageBox()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle("ERP EIPSA")
        dlg.setText("Este módulo aún no está disponible.\nDisculpe las molestias")
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        dlg.exec()
        del dlg, new_icon


    def edit_tag(self):
        # config_obj = configparser.ConfigParser()
        # config_obj.read(r"C:\Program Files\ERP EIPSA\database.ini")
        # dbparam = config_obj["postgresql"]
        # # set your parameters for the database connection URI using the keys from the configfile.ini
        # user = dbparam["user"]
        # password = dbparam["password"]

        # if not createConnection(user, password):
        #     sys.exit()

        # self.edittag_window=QtWidgets.QMainWindow()
        # self.ui=Ui_EditTags_Window()
        # self.ui.setupUi(self.edittag_window)
        # self.edittag_window.show()

        dlg = QtWidgets.QMessageBox()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle("ERP EIPSA")
        dlg.setText("Este módulo aún no está disponible.\nDisculpe las molestias")
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        dlg.exec()
        del dlg, new_icon


    def user_edition(self):
        self.edit_user_menu=QtWidgets.QMainWindow()
        self.ui=Ui_EditUser_Menu()
        self.ui.setupUi(self.edit_user_menu)
        self.edit_user_menu.show()


    def editdb(self):
        self.dbedit_menu=QtWidgets.QMainWindow()
        self.ui=Ui_EditDB_Menu()
        self.ui.setupUi(self.dbedit_menu)
        self.dbedit_menu.show()


    def importdb(self):
        self.dbimport_menu=QtWidgets.QMainWindow()
        self.ui=Ui_ImportDB_Menu()
        self.ui.setupUi(self.dbimport_menu)
        self.dbimport_menu.show()


    def dbchanges(self):
        self.tableschanges_menu=QtWidgets.QMainWindow()
        self.ui=Ui_QueryTableChanges_Window()
        self.ui.setupUi(self.tableschanges_menu)
        self.tableschanges_menu.show()


    def newtask(self):
        self.newtaskwindow=QtWidgets.QMainWindow()
        self.ui=Ui_AddTask_Window(self.name)
        self.ui.setupUi(self.newtaskwindow)
        self.newtaskwindow.show()
        self.ui.Button_Cancel.clicked.connect(self.setup_task_dates)


    def showMenu(self):
        menu = QMenu(self.centralwidget)
        menu.setStyleSheet("QMenu { border: 1px solid black; width: 125px; right: -1px; }"
        "QMenu::item:selected { background-color: rgb(3, 174, 236); color: white; }")
        option1 = menu.addAction("Editar contraseña")
        option1.triggered.connect(lambda: self.editpassword())
        menu.addAction(option1)
        button = self.Button_Profile
        menu.exec(button.mapToGlobal(QtCore.QPoint(-75, 50)))

    def editpassword(self):
            self.edit_password_window=QtWidgets.QMainWindow()
            self.ui=Ui_EditPasswordWindow(self.username)
            self.ui.setupUi(self.edit_password_window)
            self.edit_password_window.show()


    def setup_task_dates(self):
        commands_loaddatestasks = ("""
                    SELECT "task_date","task"
                    FROM tasks
                    WHERE ("responsible" = %s)
                    ORDER BY "task_date"
                    """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            if self.name == 'Carlos Crespo':
                cur.execute(commands_loaddatestasks,(self.name[0] + self.name[self.name.find(' ')+1] + 'H',))
            else:
                cur.execute(commands_loaddatestasks,(self.name[0] + self.name[self.name.find(' ')+1],))
            results=cur.fetchall()
        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()

            dates_with_tasks_raw=[x[0] for x in results]
            dates_with_tasks=list(set(dates_with_tasks_raw))

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        # Stablish dates with task assigned to put icon on calendar
        # task_dates = [QtCore.QDate.currentDate().addDays(0), QtCore.QDate.currentDate().addDays(3)]
        task_dates = dates_with_tasks
        self.Calendar.set_task_dates(task_dates)


    def show_selected_date_tasks(self):
        selected_date = self.Calendar.selectedDate()
        tasks = self.get_tasks_for_date(selected_date)

        if tasks:
            task_text = "\n".join(tasks)
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("ERP EIPSA")
            dlg.setText("Tareas para la fecha:\n"
                        "\n"
                        + task_text)
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            dlg.exec()
            del dlg, new_icon


    def get_tasks_for_date(self, date):
        # Función de ejemplo para obtener las tareas asociadas a una fecha
        # Aquí puedes implementar tu propia lógica para recuperar las tareas de una fuente de datos
        commands_loaddatestasks = ("""
                    SELECT "task_date","task"
                    FROM tasks
                    WHERE ("responsible" = %s)
                    ORDER BY "task_date"
                    """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            if self.name == 'Carlos Crespo':
                cur.execute(commands_loaddatestasks,(self.name[0] + self.name[self.name.find(' ')+1] + 'H',))
            else:
                cur.execute(commands_loaddatestasks,(self.name[0] + self.name[self.name.find(' ')+1],))
            results=cur.fetchall()
        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()

            dict={}
            for i in range(len(results)):
                key=results[i][0]
                value=results[i][1]
                if key not in dict:
                    dict[key] = [value]
                    
                else:
                    partial_list = dict.get(key)
                    partial_list.append(value)
                    dict.update({key: partial_list})
            
            return dict.get(date)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    App_Master = QtWidgets.QMainWindow()
    ui = Ui_App_Master()
    ui.setupUi(App_Master)
    App_Master.show()
    sys.exit(app.exec())