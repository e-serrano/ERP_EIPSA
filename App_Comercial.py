# Form implementation generated from reading ui file 'App_Comercial.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMenu
import psycopg2
from config import config
from datetime import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from NewOffer_Window import Ui_New_Offer_Window
from EditOffer_Menu import Ui_EditOffer_Menu
from QueryOffer_Window import Ui_QueryOffer_Window
from NewOrder_Window import Ui_New_Order_Window
from EditOrder_Window import Ui_Edit_Order_Window
from QueryOrder_Window import Ui_QueryOrder_Window
from CreateTAG_Menu import Ui_CreateTag_Menu
from EditTags_Commercial_Window import Ui_EditTags_Window
from QueryTags_Window import Ui_QueryTags_Window
from ExportOffer_Window import Ui_ExportOffer_Window
from QueryDoc_Window import Ui_QueryDoc_Window
from EditUser_Menu import Ui_EditUser_Menu
from EditPassword_Window import Ui_EditPasswordWindow


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter


class Ui_App_Comercial(object):
    # def __init__(self, user, username):
    #     self.user=user
    #     self.username=username
    def __init__(self):
        self.user='Enrique Serrano'
        self.username='e.serranog'


    def setupUi(self, App_Comercial):
        App_Comercial.setObjectName("App_Comercial")
        App_Comercial.resize(945, 860)
        App_Comercial.setMinimumSize(QtCore.QSize(945, 860))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        App_Comercial.setWindowIcon(icon)
        App_Comercial.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=App_Comercial)
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
        self.LogoIcon.setPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Logo.ico"))
        self.LogoIcon.setScaledContents(True)
        self.LogoIcon.setObjectName("LogoIcon")
        self.Header.addWidget(self.LogoIcon)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem)
        self.Button_ExpOffer = QtWidgets.QPushButton(parent=self.frame)
        self.Button_ExpOffer.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_ExpOffer.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_ExpOffer.setToolTip('Exportar Oferta')
        self.Button_ExpOffer.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_ExpOffer.setStyleSheet("QPushButton{\n"
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
        self.Button_ExpOffer.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/Offer_Export.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_ExpOffer.setIcon(icon12)
        self.Button_ExpOffer.setIconSize(QtCore.QSize(40, 40))
        self.Button_ExpOffer.setObjectName("Button_ExpOffer")
        self.Header.addWidget(self.Button_ExpOffer)
        spacerItem11 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem11)
        self.Button_Doc = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Doc.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_Doc.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_Doc.setToolTip('Documentación')
        self.Button_Doc.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Doc.setStyleSheet("QPushButton{\n"
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
        self.Button_Doc.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/Documents.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_Doc.setIcon(icon1)
        self.Button_Doc.setIconSize(QtCore.QSize(40, 40))
        self.Button_Doc.setObjectName("Button_Doc")
        self.Header.addWidget(self.Button_Doc)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem1)

        if self.user in ['Ana Calvo','Enrique Serrano']:
            self.Button_Users = QtWidgets.QPushButton(parent=self.frame)
            self.Button_Users.setMinimumSize(QtCore.QSize(50, 50))
            self.Button_Users.setMaximumSize(QtCore.QSize(50, 50))
            self.Button_Users.setToolTip('Gestión Usuarios')
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
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/User_Edit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.Button_Users.setIcon(icon2)
            self.Button_Users.setIconSize(QtCore.QSize(40, 40))
            self.Button_Users.setObjectName("Button_Users")
            self.Header.addWidget(self.Button_Users)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem2)
        self.HeaderName = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.HeaderName.setFont(font)
        self.HeaderName.setStyleSheet("color:rgb(3, 174, 236)")
        self.HeaderName.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.HeaderName.setObjectName("HeaderName")
        self.Header.addWidget(self.HeaderName)
        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem3)
        self.Button_Profile = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Profile.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_Profile.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_Profile.setToolTip('Configuración')
        self.Button_Profile.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
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
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/User.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_Profile.setIcon(icon13)
        self.Button_Profile.setIconSize(QtCore.QSize(40, 40))
        self.Button_Profile.setObjectName("Button_Profile")
        self.Header.addWidget(self.Button_Profile)
        self.FrameApp.addLayout(self.Header)
        spacerItem4 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.FrameApp.addItem(spacerItem4)
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
        self.Button_NewOffer = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_NewOffer.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_NewOffer.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_NewOffer.setFont(font)
        self.Button_NewOffer.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/Offer_New.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_NewOffer.setIcon(icon3)
        self.Button_NewOffer.setIconSize(QtCore.QSize(40, 40))
        self.Button_NewOffer.setCheckable(False)
        self.Button_NewOffer.setAutoRepeat(False)
        self.Button_NewOffer.setAutoExclusive(False)
        self.Button_NewOffer.setObjectName("Button_NewOffer")
        self.verticalLayout_3.addWidget(self.Button_NewOffer)
        self.Button_EditOffer = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_EditOffer.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_EditOffer.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_EditOffer.setFont(font)
        self.Button_EditOffer.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/Offer_Edit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_EditOffer.setIcon(icon4)
        self.Button_EditOffer.setIconSize(QtCore.QSize(40, 40))
        self.Button_EditOffer.setObjectName("Button_EditOffer")
        self.verticalLayout_3.addWidget(self.Button_EditOffer)
        self.Button_QueryOffer = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryOffer.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_QueryOffer.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_QueryOffer.setFont(font)
        self.Button_QueryOffer.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/Offer_Search.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryOffer.setIcon(icon5)
        self.Button_QueryOffer.setIconSize(QtCore.QSize(40, 40))
        self.Button_QueryOffer.setObjectName("Button_QueryOffer")
        self.verticalLayout_3.addWidget(self.Button_QueryOffer)
        self.Button_NewOrder = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_NewOrder.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_NewOrder.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_NewOrder.setFont(font)
        self.Button_NewOrder.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/Order_New.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_NewOrder.setIcon(icon6)
        self.Button_NewOrder.setIconSize(QtCore.QSize(40, 40))
        self.Button_NewOrder.setObjectName("Button_NewOrder")
        self.verticalLayout_3.addWidget(self.Button_NewOrder)
        self.Button_EditOrder = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_EditOrder.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_EditOrder.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_EditOrder.setFont(font)
        self.Button_EditOrder.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/Order_Edit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_EditOrder.setIcon(icon7)
        self.Button_EditOrder.setIconSize(QtCore.QSize(40, 40))
        self.Button_EditOrder.setObjectName("Button_EditOrder")
        self.verticalLayout_3.addWidget(self.Button_EditOrder)
        self.Button_QueryOrder = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryOrder.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_QueryOrder.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_QueryOrder.setFont(font)
        self.Button_QueryOrder.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/Order_Search.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryOrder.setIcon(icon8)
        self.Button_QueryOrder.setIconSize(QtCore.QSize(40, 40))
        self.Button_QueryOrder.setObjectName("Button_QueryOrder")
        self.verticalLayout_3.addWidget(self.Button_QueryOrder)
        self.Button_NewTag = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_NewTag.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_NewTag.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_NewTag.setFont(font)
        self.Button_NewTag.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/TAG_New.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_NewTag.setIcon(icon9)
        self.Button_NewTag.setIconSize(QtCore.QSize(40, 40))
        self.Button_NewTag.setObjectName("Button_NewTag")
        self.verticalLayout_3.addWidget(self.Button_NewTag)
        self.Button_EditTag = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_EditTag.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_EditTag.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_EditTag.setFont(font)
        self.Button_EditTag.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/TAG_Edit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_EditTag.setIcon(icon10)
        self.Button_EditTag.setIconSize(QtCore.QSize(40, 40))
        self.Button_EditTag.setObjectName("Button_EditTag")
        self.verticalLayout_3.addWidget(self.Button_EditTag)
        self.Button_QueryTag = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryTag.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_QueryTag.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_QueryTag.setFont(font)
        self.Button_QueryTag.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/TAG_Search.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryTag.setIcon(icon11)
        self.Button_QueryTag.setIconSize(QtCore.QSize(40, 40))
        self.Button_QueryTag.setObjectName("Button_QueryTag")
        self.verticalLayout_3.addWidget(self.Button_QueryTag)
        self.PrincipalScreen.addWidget(self.ButtonFrame)
        spacerItem5 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.PrincipalScreen.addItem(spacerItem5)
        self.MainLayout = QtWidgets.QVBoxLayout()
        self.MainLayout.setObjectName("MainLayout")
        self.tableOffer = QtWidgets.QTableWidget(parent=self.frame)
        self.tableOffer.setMinimumSize(QtCore.QSize(650, 280))
        self.tableOffer.setObjectName("tableOffer")
        self.tableOffer.setColumnCount(6)
        self.tableOffer.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableOffer.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableOffer.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableOffer.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableOffer.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableOffer.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableOffer.setHorizontalHeaderItem(5, item)
        self.tableOffer.verticalHeader().setVisible(False)
        self.MainLayout.addWidget(self.tableOffer)
        spacerItem6 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.MainLayout.addItem(spacerItem6)
        self.BottomLayout = QtWidgets.QHBoxLayout()
        self.BottomLayout.setContentsMargins(-1, 0, -1, -1)
        self.BottomLayout.setObjectName("BottomLayout")

        try:
            commands = ("""
                        SELECT "offer_month", CAST(SUM("offer_amount") AS numeric)
                        FROM offer
                        WHERE ("responsible"=%s
                        AND
                        "offer_year"=%s
                        AND
                        "state"='Adjudicada')
                        GROUP BY "offer_month"
                        ORDER BY "offer_month"
                        """)
            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands
                data=(self.user[0] + self.user[self.user.find(' ')+1], date.today().year,)
                cur.execute(commands, data)
                results=cur.fetchall()
            # close communication with the PostgreSQL database server
                cur.close()
            # commit the changes
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            
            months=[int(x[0]) for x in results]
            amounts=[float(x[1]) for x in results]
            self.canvas=FigureCanvas(Figure())
            ax=self.canvas.figure.subplots()
            ax.plot(months,amounts)
            ax.set_xticks(range(1,13))
            ax.set_title('Ventas totales año actual')
            ax.set_xlabel('Mes')
            ax.set_ylabel('Importe (€)')

            self.canvas.setMinimumSize(QtCore.QSize(200, 400))
            self.canvas.setMaximumSize(QtCore.QSize(583, 400))

            self.canvas.setObjectName("Graph1")
            self.BottomLayout.addWidget(self.canvas)

            spacerItem7 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
            self.BottomLayout.addItem(spacerItem7)

            commands = ("""
                        SELECT COUNT(offer."num_offer"), product_type."variable"
                        FROM offer
                        INNER JOIN product_type ON (offer."material"=product_type."material")
                        WHERE ("responsible"=%s
                        AND
                        "offer_year"=%s
                        AND
                        "state"='Adjudicada')
                        GROUP BY product_type."variable"
                        """)
            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands
                data=(self.user[0] + self.user[self.user.find(' ')+1], date.today().year,)
                cur.execute(commands, data)
                results2=cur.fetchall()
            # close communication with the PostgreSQL database server
                cur.close()
            # commit the changes
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()


            count=[x[0] for x in results2]
            labels=[x[1] for x in results2]
            self.canvas2=FigureCanvas(Figure())
            bx=self.canvas2.figure.subplots()
            bx.pie(count,labels=labels,autopct='%1.1f%%')
            bx.set_title('Proporción equipos vendidos')

            self.canvas2.setMinimumSize(QtCore.QSize(200, 400))
            self.canvas2.setMaximumSize(QtCore.QSize(583, 400))
            self.canvas2.setObjectName("canvas2")
            self.BottomLayout.addWidget(self.canvas2)

        except:
            pass

        spacerItem8 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.BottomLayout.addItem(spacerItem8)
        self.Calendar = QtWidgets.QCalendarWidget(parent=self.frame)
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
"    icon-size:30px,30px;\n"
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
"    qproperty-icon: url(//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/back_arrow.png);\n"
"}\n"
"#qt_calendar_nextmonth {\n"
"    qproperty-icon: url(//nas01/DATOS/Comunes/EIPSA-ERP/button_icons/forward_arrow.png);\n"
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
        App_Comercial.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=App_Comercial)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 945, 22))
        self.menubar.setObjectName("menubar")
        App_Comercial.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=App_Comercial)
        self.statusbar.setObjectName("statusbar")
        App_Comercial.setStatusBar(self.statusbar)
        self.tableOffer.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.retranslateUi(App_Comercial)
        QtCore.QMetaObject.connectSlotsByName(App_Comercial)

        self.Button_NewOffer.clicked.connect(self.new_offer)
        self.Button_EditOffer.clicked.connect(self.edit_offer)
        self.Button_QueryOffer.clicked.connect(self.query_offer)
        self.Button_NewOrder.clicked.connect(self.new_order)
        self.Button_EditOrder.clicked.connect(self.edit_order)
        self.Button_QueryOrder.clicked.connect(self.query_order)
        self.Button_NewTag.clicked.connect(self.new_tag)
        self.Button_EditTag.clicked.connect(self.edit_tag)
        self.Button_QueryTag.clicked.connect(self.query_tag)
        self.Button_ExpOffer.clicked.connect(self.export_offer)
        self.Button_Doc.clicked.connect(self.documents)
        self.Button_Profile.clicked.connect(self.showMenu)

        if self.user in ['Ana Calvo','Enrique Serrano']:
            self.Button_Users.clicked.connect(self.user_edition)

        commands = ("""
                    SELECT "num_offer","state","client","presentation_date","material","offer_amount"
                    FROM offer
                    WHERE ("responsible" = %s
                    AND
                    ("state" = 'Presentada'
                    OR
                    "state" = 'Registrada'
                    ))
                    ORDER BY "num_offer"
                    """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            cur.execute(commands,(self.user[0] + self.user[self.user.find(' ')+1],))
            results=cur.fetchall()
            self.tableOffer.setRowCount(len(results))
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(6):
                    it=QtWidgets.QTableWidgetItem(str(row[column]))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableOffer.setItem(tablerow, column, it)

                tablerow+=1

            self.tableOffer.verticalHeader().hide()
            self.tableOffer.setItemDelegate(AlignDelegate(self.tableOffer))

        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


    def retranslateUi(self, App_Comercial):
        _translate = QtCore.QCoreApplication.translate
        App_Comercial.setWindowTitle(_translate("App_Comercial", "ERP EIPSA - Comercial"))
        self.HeaderName.setText(_translate("App_Comercial", self.user))
        self.Button_NewOffer.setText(_translate("App_Comercial", "    Nueva Oferta"))
        self.Button_EditOffer.setText(_translate("App_Comercial", "    Editar Oferta"))
        self.Button_QueryOffer.setText(_translate("App_Comercial", "    Consultar Ofertas"))
        self.Button_NewOrder.setText(_translate("App_Comercial", "    Nuevo Pedido"))
        self.Button_EditOrder.setText(_translate("App_Comercial", "    Editar Pedido"))
        self.Button_QueryOrder.setText(_translate("App_Comercial", "   Consultar Pedidos"))
        self.Button_NewTag.setText(_translate("App_Comercial", "    Nuevo(s) TAG(s)"))
        self.Button_EditTag.setText(_translate("App_Comercial", "    Editar TAG(s)"))
        self.Button_QueryTag.setText(_translate("App_Comercial", "    Consultar TAG(s)"))
        self.tableOffer.setSortingEnabled(True)
        item = self.tableOffer.horizontalHeaderItem(0)
        item.setText(_translate("App_Comercial", "Nº Oferta"))
        item = self.tableOffer.horizontalHeaderItem(1)
        item.setText(_translate("App_Comercial", "Estado"))
        item = self.tableOffer.horizontalHeaderItem(2)
        item.setText(_translate("App_Comercial", "Cliente"))
        item = self.tableOffer.horizontalHeaderItem(3)
        item.setText(_translate("App_Comercial", "Fecha Pres."))
        item = self.tableOffer.horizontalHeaderItem(4)
        item.setText(_translate("App_Comercial", "Material"))
        item = self.tableOffer.horizontalHeaderItem(5)
        item.setText(_translate("App_Comercial", "Importe"))
        __sortingEnabled = self.tableOffer.isSortingEnabled()
        self.tableOffer.setSortingEnabled(False)
        self.tableOffer.setSortingEnabled(__sortingEnabled)


    def new_offer(self):
        self.new_offer_window=QtWidgets.QMainWindow()
        self.ui=Ui_New_Offer_Window(self.user)
        self.ui.setupUi(self.new_offer_window)
        self.new_offer_window.show()
        self.ui.Button_Cancel.clicked.connect(self.update_table)


    def edit_offer(self):
        self.edit_offer_window=QtWidgets.QMainWindow()
        self.ui=Ui_EditOffer_Menu()
        self.ui.setupUi(self.edit_offer_window)
        self.edit_offer_window.show()
        self.ui.Button_Cancel.clicked.connect(self.update_table)


    def query_offer(self):
        self.query_offer_window=QtWidgets.QMainWindow()
        self.ui=Ui_QueryOffer_Window()
        self.ui.setupUi(self.query_offer_window)
        self.query_offer_window.show()


    def new_order(self):
        self.new_order_window=QtWidgets.QMainWindow()
        self.ui=Ui_New_Order_Window()
        self.ui.setupUi(self.new_order_window)
        self.new_order_window.show()


    def edit_order(self):
        self.edit_order_window=QtWidgets.QMainWindow()
        self.ui=Ui_Edit_Order_Window()
        self.ui.setupUi(self.edit_order_window)
        self.edit_order_window.show()


    def query_order(self):
        self.query_order_window=QtWidgets.QMainWindow()
        self.ui=Ui_QueryOrder_Window()
        self.ui.setupUi(self.query_order_window)
        self.query_order_window.show()


    def new_tag(self):
        self.new_tag_window=QtWidgets.QMainWindow()
        self.ui=Ui_CreateTag_Menu()
        self.ui.setupUi(self.new_tag_window)
        self.new_tag_window.show()


    def edit_tag(self):
        self.edittag_window=QtWidgets.QMainWindow()
        self.ui=Ui_EditTags_Window()
        self.ui.setupUi(self.edittag_window)
        self.edittag_window.show()


    def query_tag(self):
        self.querytag_window=QtWidgets.QMainWindow()
        self.ui=Ui_QueryTags_Window()
        self.ui.setupUi(self.querytag_window)
        self.querytag_window.show()


    def export_offer(self):
        self.exportoffer_window=QtWidgets.QMainWindow()
        self.ui=Ui_ExportOffer_Window()
        self.ui.setupUi(self.exportoffer_window)
        self.exportoffer_window.show()


    def documents(self):
        print('documents')
        self.querydoc_menu=QtWidgets.QMainWindow()
        self.ui=Ui_QueryDoc_Window()
        self.ui.setupUi(self.querydoc_menu)
        self.querydoc_menu.show()


    def showMenu(self):
        menu = QMenu(self.centralwidget)
        menu.setStyleSheet("QMenu::item:selected { background-color: rgb(3, 174, 236); color: white; }")
        option1 = menu.addAction("Editar contraseña")
        option1.triggered.connect(lambda: self.editpassword())
        menu.addAction(option1)
        button = self.Button_Profile
        menu.exec(button.mapToGlobal(button.pos()))

    def editpassword(self):
        self.edit_password_window=QtWidgets.QMainWindow()
        self.ui=Ui_EditPasswordWindow(self.username)
        self.ui.setupUi(self.edit_password_window)
        self.edit_password_window.show()


    def user_edition(self):
        self.edit_user_menu=QtWidgets.QMainWindow()
        self.ui=Ui_EditUser_Menu()
        self.ui.setupUi(self.edit_user_menu)
        self.edit_user_menu.show()


    def update_table(self):
        commands = ("""
                    SELECT "num_offer","state","client","presentation_date","material","offer_amount"
                    FROM offer
                    WHERE ("responsible" = %s
                    AND
                    ("state" = 'Presentada'
                    OR
                    "state" = 'Registrada'
                    ))
                    ORDER BY "num_offer"
                    """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            cur.execute(commands,(self.user[0] + self.user[self.user.find(' ')+1],))
            results=cur.fetchall()
            self.tableOffer.setRowCount(len(results))
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(6):
                    it=QtWidgets.QTableWidgetItem(str(row[column]))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableOffer.setItem(tablerow, column, it)

                tablerow+=1

            self.tableOffer.verticalHeader().hide()
            self.tableOffer.setItemDelegate(AlignDelegate(self.tableOffer))

        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    App_Comercial = QtWidgets.QMainWindow()
    ui = Ui_App_Comercial()
    ui.setupUi(App_Comercial)
    App_Comercial.showMaximized()
    sys.exit(app.exec())
