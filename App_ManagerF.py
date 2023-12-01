# Form implementation generated from reading ui file 'App_ManagerF.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMenu
from PyQt6.QtCore import Qt
import psycopg2
import sys
from config import config
from datetime import *
from OfferQuery_Window import Ui_QueryOffer_Window
from OrderQuery_Window import Ui_QueryOrder_Window
from TAGQuery_Window import Ui_QueryTags_Window
from DocQuery_Window import Ui_QueryDoc_Window
from OfferGraphs_Window import Ui_GraphsOffer_Window
from ClientsGeneralResume_Window import Ui_ClientsGeneralResume_Window
from PasswordEdit_Window import Ui_EditPasswordWindow
from ClientResume_Window import Ui_ClientResume_Window
from TaskQuery_Window import Ui_QueryTask_Window
from TaskAdd_Window import Ui_AddTask_Window
import os

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter


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
            image_path = os.path.abspath(os.path.join(basedir, "Resources/Iconos/Flag.png"))
            image = QtGui.QImage(image_path)
            if not image.isNull():
                image_scaled = image.scaled(rect.width() // 4, rect.height() // 4, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                image_rect = image_scaled.rect()
                image_rect.moveTopRight(rect.topRight() - QtCore.QPoint(2, -5))
                painter.drawImage(image_rect, image_scaled)


class Ui_App_ManagerF(object):
    def __init__(self, name, username):
        self.name=name
        self.username=username


    def setupUi(self, App_ManagerF):
        App_ManagerF.setObjectName("App_ManagerF")
        App_ManagerF.resize(945, 860)
        App_ManagerF.setMinimumSize(QtCore.QSize(945, 860))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        App_ManagerF.setWindowIcon(icon)
        App_ManagerF.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=App_ManagerF)
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
        self.LogoIcon.setPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Logo.ico"))))
        self.LogoIcon.setScaledContents(True)
        self.LogoIcon.setObjectName("LogoIcon")
        self.Header.addWidget(self.LogoIcon)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem)
        self.Button_Graphs = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Graphs.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_Graphs.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_Graphs.setToolTip('Gráficos')
        self.Button_Graphs.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Graphs.setStyleSheet("QPushButton{\n"
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
        self.Button_Graphs.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Chart.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_Graphs.setIcon(icon14)
        self.Button_Graphs.setIconSize(QtCore.QSize(40, 40))
        self.Button_Graphs.setObjectName("Button_Graphs")
        self.Header.addWidget(self.Button_Graphs)
        spacerItem10 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem10)
        self.Button_ClientsResume = QtWidgets.QPushButton(parent=self.frame)
        self.Button_ClientsResume.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_ClientsResume.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_ClientsResume.setToolTip('Resumen Clientes')
        self.Button_ClientsResume.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_ClientsResume.setStyleSheet("QPushButton{\n"
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
        self.Button_ClientsResume.setText("")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Customers.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_ClientsResume.setIcon(icon15)
        self.Button_ClientsResume.setIconSize(QtCore.QSize(40, 40))
        self.Button_ClientsResume.setObjectName("Button_ClientsResume")
        self.Header.addWidget(self.Button_ClientsResume)
        spacerItem13 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem13)
        self.Button_QueryTask = QtWidgets.QPushButton(parent=self.frame)
        self.Button_QueryTask.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_QueryTask.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_QueryTask.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_QueryTask.setStyleSheet("QPushButton{\n"
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
        self.Button_QueryTask.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Task.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryTask.setIcon(icon5)
        self.Button_QueryTask.setIconSize(QtCore.QSize(40, 40))
        self.Button_QueryTask.setObjectName("Button_QueryTask")
        self.Button_QueryTask.setToolTip("Tareas")
        self.Header.addWidget(self.Button_QueryTask)
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
        icon13.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/User.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
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
        self.Button_QueryOffer = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryOffer.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_QueryOffer.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_QueryOffer.setFont(font)
        self.Button_QueryOffer.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Offer_Search.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryOffer.setIcon(icon5)
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
        icon8.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Order_Search.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryOrder.setIcon(icon8)
        self.Button_QueryOrder.setIconSize(QtCore.QSize(40, 40))
        self.Button_QueryOrder.setObjectName("Button_QueryOrder")
        self.verticalLayout_3.addWidget(self.Button_QueryOrder)
        self.Button_QueryTag = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryTag.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_QueryTag.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_QueryTag.setFont(font)
        self.Button_QueryTag.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/TAG_Search.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryTag.setIcon(icon11)
        self.Button_QueryTag.setIconSize(QtCore.QSize(40, 40))
        self.Button_QueryTag.setObjectName("Button_QueryTag")
        self.verticalLayout_3.addWidget(self.Button_QueryTag)
        self.Button_QueryDoc = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryDoc.setMinimumSize(QtCore.QSize(200, 50))
        self.Button_QueryDoc.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.Button_QueryDoc.setFont(font)
        self.Button_QueryDoc.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Documents_Search.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryDoc.setIcon(icon4)
        self.Button_QueryDoc.setIconSize(QtCore.QSize(40, 40))
        self.Button_QueryDoc.setObjectName("Button_QueryDoc")
        self.verticalLayout_3.addWidget(self.Button_QueryDoc)
        self.PrincipalScreen.addWidget(self.ButtonFrame)
        spacerItem5 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.PrincipalScreen.addItem(spacerItem5)
        self.MainLayout = QtWidgets.QVBoxLayout()
        self.MainLayout.setObjectName("MainLayout")
        self.tableOffer = QtWidgets.QTableWidget(parent=self.frame)
        self.tableOffer.setMinimumSize(QtCore.QSize(650, 280))
        self.tableOffer.setObjectName("tableOffer")
        self.tableOffer.setColumnCount(11)
        self.tableOffer.setRowCount(0)
        for i in range(11):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            item.setFont(font)
            self.tableOffer.setHorizontalHeaderItem(i, item)
        self.tableOffer.verticalHeader().setVisible(False)
        self.tableOffer.setSortingEnabled(False)
        self.tableOffer.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        self.MainLayout.addWidget(self.tableOffer)
        spacerItem6 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.MainLayout.addItem(spacerItem6)
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
        self.Calendar.setMinimumSize(QtCore.QSize(300, 400))
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
"    qproperty-icon: url(//nas01/DATOS/Comunes/EIPSA-ERP/Resources/Iconos/back_arrow.png);\n"
"}\n"
"#qt_calendar_nextmonth {\n"
"    qproperty-icon: url(//nas01/DATOS/Comunes/EIPSA-ERP/Resources/Iconos/forward_arrow.png);\n"
"\n"
"}")
        self.Calendar.setSelectedDate(QtCore.QDate.currentDate())
        self.Calendar.setGridVisible(True)
        self.Calendar.setNavigationBarVisible(True)
        self.Calendar.setDateEditEnabled(True)
        self.Calendar.setObjectName("Calendar")
        self.Calendar.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.BottomLayout.addWidget(self.Calendar)
        self.MainLayout.addLayout(self.BottomLayout)
        self.PrincipalScreen.addLayout(self.MainLayout)
        self.FrameApp.addLayout(self.PrincipalScreen)
        self.gridLayout.addLayout(self.FrameApp, 3, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        App_ManagerF.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=App_ManagerF)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 945, 22))
        self.menubar.setObjectName("menubar")
        App_ManagerF.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=App_ManagerF)
        self.statusbar.setObjectName("statusbar")
        App_ManagerF.setStatusBar(self.statusbar)
        self.tableOffer.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.retranslateUi(App_ManagerF)
        QtCore.QMetaObject.connectSlotsByName(App_ManagerF)

        self.Button_QueryOffer.clicked.connect(self.query_offer)
        self.Button_QueryOrder.clicked.connect(self.query_order)
        self.Button_QueryTag.clicked.connect(self.query_tag)
        self.Button_QueryDoc.clicked.connect(self.query_documents)
        self.Button_Graphs.clicked.connect(self.graphs)
        self.Button_ClientsResume.clicked.connect(self.clients_generalresume)
        self.Button_Profile.clicked.connect(self.showMenu)
        self.tableOffer.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.Button_QueryTask.clicked.connect(self.querytask)
        self.Calendar.activated.connect(self.show_selected_date_tasks)
        self.Calendar.customContextMenuRequested.connect(self.show_context_menu)

        self.setup_task_dates()


        commands_appcomercial = ("""
                    SELECT "num_offer","state","responsible","client","final_client",TO_CHAR("presentation_date", 'DD-MM-YYYY'),"material","offer_amount","notes","important","tracking"
                    FROM offers
                    WHERE (("state" = 'Presentada'
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
            cur.execute(commands_appcomercial)
            results=cur.fetchall()
            self.tableOffer.setRowCount(len(results))
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(11):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
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


    def show_context_menu(self, point):
        selected_date = self.Calendar.selectedDate()
        menu = QMenu(self.centralwidget)

        menu.setStyleSheet("QMenu { border: 1px solid black; width: 150px; right: -1px; }"
        "QMenu::item:selected { background-color: rgb(3, 174, 236); color: white; }")

        action1 = menu.addAction("Agregar tareas")
        action1.triggered.connect(lambda: self.newtask(selected_date))
        action2 = menu.addAction("Editar tareas")
        action2.triggered.connect(lambda: self.querytask(selected_date))

        menu.exec(self.Calendar.mapToGlobal(point))

    def retranslateUi(self, App_ManagerF):
        _translate = QtCore.QCoreApplication.translate
        App_ManagerF.setWindowTitle(_translate("App_ManagerF", "ERP EIPSA - Dirección"))
        self.HeaderName.setText(_translate("App_ManagerF", self.name))
        self.Button_QueryOffer.setText(_translate("App_ManagerF", "    Consultar Ofertas"))
        self.Button_QueryOrder.setText(_translate("App_ManagerF", "   Consultar Pedidos"))
        self.Button_QueryTag.setText(_translate("App_ManagerF", "    Consultar TAG(s)"))
        self.Button_QueryDoc.setText(_translate("App_ManagerF", "    Consultar Docs."))
        self.tableOffer.setSortingEnabled(True)
        item = self.tableOffer.horizontalHeaderItem(0)
        item.setText(_translate("App_ManagerF", "Nº Oferta"))
        item = self.tableOffer.horizontalHeaderItem(1)
        item.setText(_translate("App_ManagerF", "Estado"))
        item = self.tableOffer.horizontalHeaderItem(2)
        item.setText(_translate("App_ManagerF", "Responsable"))
        item = self.tableOffer.horizontalHeaderItem(3)
        item.setText(_translate("App_ManagerF", "Cliente"))
        item = self.tableOffer.horizontalHeaderItem(4)
        item.setText(_translate("App_ManagerF", "Cliente Final"))
        item = self.tableOffer.horizontalHeaderItem(5)
        item.setText(_translate("App_ManagerF", "Fecha Pres."))
        item = self.tableOffer.horizontalHeaderItem(6)
        item.setText(_translate("App_ManagerF", "Material"))
        item = self.tableOffer.horizontalHeaderItem(7)
        item.setText(_translate("App_ManagerF", "Importe"))
        item = self.tableOffer.horizontalHeaderItem(8)
        item.setText(_translate("App_ManagerF", "Notas"))
        item = self.tableOffer.horizontalHeaderItem(9)
        item.setText(_translate("App_ManagerF", "Ptos. Importantes"))
        item = self.tableOffer.horizontalHeaderItem(10)
        item.setText(_translate("App_ManagerF", "Seguimiento"))
        __sortingEnabled = self.tableOffer.isSortingEnabled()
        self.tableOffer.setSortingEnabled(False)
        self.tableOffer.setSortingEnabled(__sortingEnabled)


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


    def query_tag(self):
        self.querytag_window=QtWidgets.QMainWindow()
        self.ui=Ui_QueryTags_Window('Comercial')
        self.ui.setupUi(self.querytag_window)
        self.querytag_window.show()


    def query_documents(self):
        self.querydoc_menu=QtWidgets.QMainWindow()
        self.ui=Ui_QueryDoc_Window()
        self.ui.setupUi(self.querydoc_menu)
        self.querydoc_menu.show()


    def graphs(self):
        self.graphswindow=QtWidgets.QMainWindow()
        self.ui=Ui_GraphsOffer_Window()
        self.ui.setupUi(self.graphswindow)
        self.graphswindow.show()


    def clients_generalresume(self):
        self.clients_general_resume_window=QtWidgets.QMainWindow()
        self.ui=Ui_ClientsGeneralResume_Window()
        self.ui.setupUi(self.clients_general_resume_window)
        self.clients_general_resume_window.show()


    def querytask(self, date=None):
        self.querytaskwindow=Ui_QueryTask_Window(self.name, date)
        self.querytaskwindow.show()
        self.querytaskwindow.Button_Cancel.clicked.connect(self.setup_task_dates)


    def newtask(self, date):
        self.newtaskwindow=QtWidgets.QMainWindow()
        self.ui=Ui_AddTask_Window(self.name, date)
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



#Function to update the table
    def update_table(self):
        commands_appcomercial = ("""
                    SELECT "num_offer","state","responsible","client","final_client",TO_CHAR("presentation_date", 'DD-MM-YYYY'),"material","offer_amount","notes","important","tracking"
                    FROM offers
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
            if self.name == 'Carlos Crespo':
                cur.execute(commands_appcomercial,(self.name[0] + self.name[self.name.find(' ')+1] + 'H',))
            else:
                cur.execute(commands_appcomercial,(self.name[0] + self.name[self.name.find(' ')+1],))
            results=cur.fetchall()
            self.tableOffer.setRowCount(len(results))
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(11):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
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


# Function to check if column index of double clicked cell is equal to first column index
    def on_item_double_clicked(self, item):
        if item.column() == 2:
            self.clientresume(item)

        elif item.column() in [8,9,10]:
            cell_content = item.text()
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Ofertas")
            dlg.setText(cell_content)
            dlg.exec()


# Function when double clicked cell is in first column
    def clientresume(self, item):
        clientname=item.text()
        self.client_resume_window=QtWidgets.QMainWindow()
        self.ui=Ui_ClientResume_Window(clientname)
        self.ui.setupUi(self.client_resume_window)
        self.client_resume_window.show()


# Function to stablish dates with task assigned to put icon on calendar
    def setup_task_dates(self):
        commands_loaddatestasks_LB = ("""
                    SELECT "task_date","task"
                    FROM tasks
                    WHERE ("creator" IN ('CCH', 'SS', 'LB')
                    AND
                    "state" = 'Pendiente')
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
            cur.execute(commands_loaddatestasks_LB)
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
        # task_dates = [QtCore.QDate.currentDate().addDays(0), QtCore.QDate.currentDate().addDays(3)]
        task_dates = dates_with_tasks
        self.Calendar.set_task_dates(task_dates)


    def show_selected_date_tasks(self):
        self.click_count = 0
        selected_date = self.Calendar.selectedDate()
        if self.name == 'Carlos Crespo':
            creator=self.name[0] + self.name[self.name.find(' ')+1] + 'H'
        else:
            creator=self.name[0] + self.name[self.name.find(' ')+1]
        returned = self.get_tasks_for_date(creator, selected_date)

        if returned:
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("ERP EIPSA")
            final_text=''

            for item in returned:
                responsible = item[0]
                tasks = item [1]
                task_text = "<br><br>-".join(tasks)
                final_text += "<br><br>" + f"<b>{responsible}:</b><br>-" + task_text

            dlg.setText(f"<html><body>Tareas para la fecha {selected_date.toString('dd-MM-yyyy')}:{final_text}</body></html>")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            dlg.exec()
            del dlg, new_icon


#Function to obtain tasks associated to a date
    def get_tasks_for_date(self, creator, date):
        commands_loaddatestasks_LB = ("""
                    SELECT "responsible","task_date","task","state","creator"
                    FROM tasks
                    WHERE ("creator" IN ('CCH', 'SS', 'LB')
                    AND
                    "task_date" IS NOT NULL
                    AND
                    "state" = 'Pendiente')
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
            cur.execute(commands_loaddatestasks_LB)
            results=cur.fetchall()
        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()

            dict_responsibles_tasks={}

            for i in range(len(results)):
                responsible=results[i][0]
                key=QtCore.QDate(results[i][1].year, results[i][1].month, results[i][1].day)
                value="(" + results[i][4]+") " + results[i][2] + " (" + results[i][3] + ")"

                if responsible not in dict_responsibles_tasks:
                    dict_responsibles_tasks[responsible] = [{key: [value]}]

                else:
                    for item in dict_responsibles_tasks[responsible]:
                        if key not in item:
                            item[key] = [value]

                        else:
                            item[key].append(value)

            value_to_return = []
            for item in dict_responsibles_tasks.keys():
                for element in dict_responsibles_tasks[item]:
                    if date in element:
                        value_to_return.append([item,dict_responsibles_tasks[item][dict_responsibles_tasks[item].index(element)][date]])

            return value_to_return

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()




# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     App_ManagerF = QtWidgets.QMainWindow()
#     ui = Ui_App_ManagerF()
#     ui.setupUi(App_ManagerF)
#     App_ManagerF.showMaximized()
#     sys.exit(app.exec())