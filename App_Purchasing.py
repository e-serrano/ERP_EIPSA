# Form implementation generated from reading ui file 'App_Purchasing.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from Purchasing_Menu import Ui_Purchasing_Menu
from QueryOffer_Window import Ui_QueryOffer_Window
from QueryOrder_Window import Ui_QueryOrder_Window
from QueryTags_Window import Ui_QueryTags_Window
from EditPassword_Window import Ui_EditPasswordWindow
from PyQt6.QtWidgets import QMenu
import os

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter


class Ui_App_Purchasing(object):
    def __init__(self, name, username):
        self.name=name
        self.username=username


    def setupUi(self, App_Purchasing):
        App_Purchasing.setObjectName("App_Purchasing")
        App_Purchasing.resize(945, 860)
        App_Purchasing.setMinimumSize(QtCore.QSize(945, 860))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        App_Purchasing.setWindowIcon(icon)
        App_Purchasing.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=App_Purchasing)
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
        self.LogoIcon.setMinimumSize(QtCore.QSize(int(220//1.5), int(52//1.5)))
        self.LogoIcon.setMaximumSize(QtCore.QSize(int(220//1.5), int(52//1.5)))
        self.LogoIcon.setText("")
        self.LogoIcon.setPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Logo.ico"))))
        self.LogoIcon.setScaledContents(True)
        self.LogoIcon.setObjectName("LogoIcon")
        self.Header.addWidget(self.LogoIcon)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem1)
        self.HeaderName = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(int(12//1.5))
        font.setBold(True)
        self.HeaderName.setFont(font)
        self.HeaderName.setStyleSheet("color:rgb(3, 174, 236)")
        self.HeaderName.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.HeaderName.setObjectName("HeaderName")
        self.Header.addWidget(self.HeaderName)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem2)
        self.Button_Profile = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Profile.setMinimumSize(QtCore.QSize(int(50//1.5), int(50//1.5)))
        self.Button_Profile.setMaximumSize(QtCore.QSize(int(50//1.5), int(50//1.5)))
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
        self.Button_Profile.setIconSize(QtCore.QSize(int(40//1.5), int(40//1.5)))
        self.Button_Profile.setObjectName("Button_Profile")
        self.Header.addWidget(self.Button_Profile)
        self.FrameApp.addLayout(self.Header)
        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.FrameApp.addItem(spacerItem3)
        self.PrincipalScreen = QtWidgets.QHBoxLayout()
        self.PrincipalScreen.setObjectName("PrincipalScreen")
        self.ButtonFrame = QtWidgets.QFrame(parent=self.frame)
        self.ButtonFrame.setMinimumSize(QtCore.QSize(int(220//1.5), 0))
        self.ButtonFrame.setMaximumSize(QtCore.QSize(int(220//1.5), 16777215))
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
        self.Button_Purchasing = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_Purchasing.setMinimumSize(QtCore.QSize(int(200//1.5), int(50//1.5)))
        self.Button_Purchasing.setMaximumSize(QtCore.QSize(int(200//1.5), int(50//1.5)))
        font = QtGui.QFont()
        font.setPointSize(int(12//1.5))
        font.setBold(True)
        self.Button_Purchasing.setFont(font)
        self.Button_Purchasing.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Purchasing.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_Purchasing.setIcon(icon1)
        self.Button_Purchasing.setIconSize(QtCore.QSize(int(40//1.5), int(40//1.5)))
        self.Button_Purchasing.setObjectName("Button_Purchasing")
        self.verticalLayout_3.addWidget(self.Button_Purchasing)
        # self.Button_PurchaseOrder = QtWidgets.QPushButton(parent=self.ButtonFrame)
        # self.Button_PurchaseOrder.setMinimumSize(QtCore.QSize(200, 50))
        # self.Button_PurchaseOrder.setMaximumSize(QtCore.QSize(200, 50))
        # font = QtGui.QFont()
        # font.setPointSize(int(12//1.5))
        # font.setBold(True)
        # self.Button_PurchaseOrder.setFont(font)
        # self.Button_PurchaseOrder.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        # icon2 = QtGui.QIcon()
        # icon2.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Purchase_Order.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        # self.Button_PurchaseOrder.setIcon(icon2)
        # self.Button_PurchaseOrder.setIconSize(QtCore.QSize(40, 40))
        # self.Button_PurchaseOrder.setObjectName("Button_PurchaseOrder")
        # self.verticalLayout_3.addWidget(self.Button_PurchaseOrder)
        self.Button_QueryOffer = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryOffer.setMinimumSize(QtCore.QSize(int(200//1.5), int(50//1.5)))
        self.Button_QueryOffer.setMaximumSize(QtCore.QSize(int(200//1.5), int(50//1.5)))
        font = QtGui.QFont()
        font.setPointSize(int(12//1.5))
        font.setBold(True)
        self.Button_QueryOffer.setFont(font)
        self.Button_QueryOffer.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Offer_Search.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryOffer.setIcon(icon3)
        self.Button_QueryOffer.setIconSize(QtCore.QSize(int(40//1.5), int(40//1.5)))
        self.Button_QueryOffer.setObjectName("Button_QueryOffer")
        self.verticalLayout_3.addWidget(self.Button_QueryOffer)
        self.Button_QueryOrder = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryOrder.setMinimumSize(QtCore.QSize(int(200//1.5), int(50//1.5)))
        self.Button_QueryOrder.setMaximumSize(QtCore.QSize(int(200//1.5), int(50//1.5)))
        font = QtGui.QFont()
        font.setPointSize(int(12//1.5))
        font.setBold(True)
        self.Button_QueryOrder.setFont(font)
        self.Button_QueryOrder.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Order_Search.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryOrder.setIcon(icon4)
        self.Button_QueryOrder.setIconSize(QtCore.QSize(int(40//1.5), int(40//1.5)))
        self.Button_QueryOrder.setObjectName("Button_QueryOrder")
        self.verticalLayout_3.addWidget(self.Button_QueryOrder)
        self.Button_QueryTag = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryTag.setMinimumSize(QtCore.QSize(int(200//1.5), int(50//1.5)))
        self.Button_QueryTag.setMaximumSize(QtCore.QSize(int(200//1.5), int(50//1.5)))
        font = QtGui.QFont()
        font.setPointSize(int(12//1.5))
        font.setBold(True)
        self.Button_QueryTag.setFont(font)
        self.Button_QueryTag.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/TAG_Search.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryTag.setIcon(icon5)
        self.Button_QueryTag.setIconSize(QtCore.QSize(int(40//1.5), int(40//1.5)))
        self.Button_QueryTag.setObjectName("Button_QueryTag")
        self.verticalLayout_3.addWidget(self.Button_QueryTag)
        self.PrincipalScreen.addWidget(self.ButtonFrame)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.PrincipalScreen.addItem(spacerItem4)
        self.MainLayout = QtWidgets.QVBoxLayout()
        self.MainLayout.setObjectName("MainLayout")
        self.table = QtWidgets.QTableWidget(parent=self.frame)
        self.table.setMinimumSize(QtCore.QSize(int(650//1.5), int(280//1.5)))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.verticalHeader().setVisible(False)
        self.MainLayout.addWidget(self.table)
        spacerItem5 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.MainLayout.addItem(spacerItem5)
        self.BottomLayout = QtWidgets.QHBoxLayout()
        self.BottomLayout.setContentsMargins(-1, 0, -1, -1)
        self.BottomLayout.setObjectName("BottomLayout")
        self.Calendar = QtWidgets.QCalendarWidget(parent=self.frame)
        self.Calendar.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Calendar.sizePolicy().hasHeightForWidth())
        self.Calendar.setSizePolicy(sizePolicy)
        self.Calendar.setMinimumSize(QtCore.QSize(int(200//1.5), int(400//1.5)))
        self.Calendar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        font = QtGui.QFont()
        font.setPointSize(int(10//1.5))
        self.Calendar.setFont(font)
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
"    font-size:15px;\n"
"    icon-size:20px 20px;\n"
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
        App_Purchasing.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=App_Purchasing)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 945, 22))
        self.menubar.setObjectName("menubar")
        App_Purchasing.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=App_Purchasing)
        self.statusbar.setObjectName("statusbar")
        App_Purchasing.setStatusBar(self.statusbar)

        self.retranslateUi(App_Purchasing)
        QtCore.QMetaObject.connectSlotsByName(App_Purchasing)
        self.Button_Purchasing.clicked.connect(self.purchase)
        # self.Button_PurchaseOrder.clicked.connect(self.purchase_order)
        self.Button_QueryOffer.clicked.connect(self.query_offer)
        self.Button_QueryOrder.clicked.connect(self.query_order)
        self.Button_QueryTag.clicked.connect(self.query_tag)
        self.Button_Profile.clicked.connect(self.showMenu)


    def retranslateUi(self, App_Purchasing):
        _translate = QtCore.QCoreApplication.translate
        App_Purchasing.setWindowTitle(_translate("App_Purchasing", "ERP EIPSA - Compras"))
        self.HeaderName.setText(_translate("App_Purchasing", self.name))
        self.Button_Purchasing.setText(_translate("App_Purchasing", "    Compras"))
        # self.Button_PurchaseOrder.setText(_translate("App_Purchasing", " Orden de Compra"))
        self.Button_QueryOffer.setText(_translate("App_Purchasing", "    Consultar Ofertas"))
        self.Button_QueryOrder.setText(_translate("App_Purchasing", "   Consultar Pedidos"))
        self.Button_QueryTag.setText(_translate("App_Purchasing", "    Consultar TAG(s)"))
        self.table.setSortingEnabled(True)


    def purchase(self):
        self.purchasing_window=QtWidgets.QMainWindow()
        self.ui=Ui_Purchasing_Menu(self.name)
        self.ui.setupUi(self.purchasing_window)
        self.purchasing_window.show()


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


    def showMenu(self):
        menu = QMenu(self.centralwidget)
        menu.setStyleSheet("QMenu { border: 1px solid black; width: 125px; right: -1px; font: 10px}"
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
