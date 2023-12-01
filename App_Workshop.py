# Form implementation generated from reading ui file 'App_Workshop.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PasswordEdit_Window import Ui_EditPasswordWindow
from PyQt6.QtWidgets import QMenu
import os
import configparser
from config import config
import psycopg2
from Database_Connection import createConnection
from Assembly_Window import Ui_Assembly_Window
from Workshop_Window import Ui_Workshop_Window
from NotificationsHistory_Window import Ui_HistoryNotifications_Window
from TAGEdit_Workshop_Window import Ui_EditTags_Workshop_Window

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter


class Ui_App_Workshop(object):
    def __init__(self, name, username):
        self.name=name
        self.username=username


    def setupUi(self, App_Workshop):
        App_Workshop.setObjectName("App_Workshop")
        App_Workshop.resize(945, 860)
        App_Workshop.setMinimumSize(QtCore.QSize(945, 860))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        App_Workshop.setWindowIcon(icon)
        App_Workshop.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=App_Workshop)
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
        self.LogoIcon.setMinimumSize(QtCore.QSize(int(220), int(52)))
        self.LogoIcon.setMaximumSize(QtCore.QSize(int(220), int(52)))
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
        font.setPointSize(int(12))
        font.setBold(True)
        self.HeaderName.setFont(font)
        self.HeaderName.setStyleSheet("color:rgb(3, 174, 236)")
        self.HeaderName.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.HeaderName.setObjectName("HeaderName")
        self.Header.addWidget(self.HeaderName)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem2)
        self.Button_Notification = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Notification.setMinimumSize(QtCore.QSize(50, 50))
        self.Button_Notification.setMaximumSize(QtCore.QSize(50, 50))
        self.Button_Notification.setToolTip('Notificaciones')
        self.Button_Notification.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Notification.setStyleSheet("QPushButton{\n"
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
        self.Button_Notification.setText("")
        self.Button_Notification.setIconSize(QtCore.QSize(40, 40))
        self.Button_Notification.setObjectName("Button_Notification")
        self.Header.addWidget(self.Button_Notification)
        spacerItem15 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.Header.addItem(spacerItem15)
        self.Button_Profile = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Profile.setMinimumSize(QtCore.QSize(int(50), int(50)))
        self.Button_Profile.setMaximumSize(QtCore.QSize(int(50), int(50)))
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
        self.Button_Profile.setIconSize(QtCore.QSize(int(40), int(40)))
        self.Button_Profile.setObjectName("Button_Profile")
        self.Header.addWidget(self.Button_Profile)
        self.FrameApp.addLayout(self.Header)
        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.FrameApp.addItem(spacerItem3)
        self.PrincipalScreen = QtWidgets.QHBoxLayout()
        self.PrincipalScreen.setObjectName("PrincipalScreen")
        self.ButtonFrame = QtWidgets.QFrame(parent=self.frame)
        self.ButtonFrame.setMinimumSize(QtCore.QSize(int(220), 0))
        self.ButtonFrame.setMaximumSize(QtCore.QSize(int(220), 16777215))
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
        self.Button_QueryTag = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_QueryTag.setMinimumSize(QtCore.QSize(int(200), int(50)))
        self.Button_QueryTag.setMaximumSize(QtCore.QSize(int(200), int(50)))
        font = QtGui.QFont()
        font.setPointSize(int(12))
        font.setBold(True)
        self.Button_QueryTag.setFont(font)
        self.Button_QueryTag.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/TAG_Search.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_QueryTag.setIcon(icon1)
        self.Button_QueryTag.setIconSize(QtCore.QSize(int(40), int(40)))
        self.Button_QueryTag.setObjectName("v")
        self.verticalLayout_3.addWidget(self.Button_QueryTag)
        self.Button_Manufacturing = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_Manufacturing.setMinimumSize(QtCore.QSize(int(200), int(50)))
        self.Button_Manufacturing.setMaximumSize(QtCore.QSize(int(200), int(50)))
        font = QtGui.QFont()
        font.setPointSize(int(12))
        font.setBold(True)
        self.Button_Manufacturing.setFont(font)
        self.Button_Manufacturing.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Factory.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_Manufacturing.setIcon(icon1)
        self.Button_Manufacturing.setIconSize(QtCore.QSize(int(40), int(40)))
        self.Button_Manufacturing.setObjectName("Button_Manufacturing")
        self.verticalLayout_3.addWidget(self.Button_Manufacturing)
        self.Button_Assembly = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_Assembly.setMinimumSize(QtCore.QSize(int(200), int(50)))
        self.Button_Assembly.setMaximumSize(QtCore.QSize(int(200), int(50)))
        font = QtGui.QFont()
        font.setPointSize(int(12))
        font.setBold(True)
        self.Button_Assembly.setFont(font)
        self.Button_Assembly.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Assembly.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_Assembly.setIcon(icon3)
        self.Button_Assembly.setIconSize(QtCore.QSize(int(40), int(40)))
        self.Button_Assembly.setObjectName("Button_Assembly")
        self.verticalLayout_3.addWidget(self.Button_Assembly)
        self.Button_Dispatch = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_Dispatch.setMinimumSize(QtCore.QSize(int(200), int(50)))
        self.Button_Dispatch.setMaximumSize(QtCore.QSize(int(200), int(50)))
        font = QtGui.QFont()
        font.setPointSize(int(12))
        font.setBold(True)
        self.Button_Dispatch.setFont(font)
        self.Button_Dispatch.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Transport.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_Dispatch.setIcon(icon4)
        self.Button_Dispatch.setIconSize(QtCore.QSize(int(40), int(40)))
        self.Button_Dispatch.setObjectName("Button_Dispatch")
        self.verticalLayout_3.addWidget(self.Button_Dispatch)
        self.Button_Times = QtWidgets.QPushButton(parent=self.ButtonFrame)
        self.Button_Times.setMinimumSize(QtCore.QSize(int(200), int(50)))
        self.Button_Times.setMaximumSize(QtCore.QSize(int(200), int(50)))
        font = QtGui.QFont()
        font.setPointSize(int(12))
        font.setBold(True)
        self.Button_Times.setFont(font)
        self.Button_Times.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Clock.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_Times.setIcon(icon5)
        self.Button_Times.setIconSize(QtCore.QSize(int(40), int(40)))
        self.Button_Times.setObjectName("Button_Times")
        self.verticalLayout_3.addWidget(self.Button_Times)
        self.PrincipalScreen.addWidget(self.ButtonFrame)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.PrincipalScreen.addItem(spacerItem4)
        self.MainLayout = QtWidgets.QVBoxLayout()
        self.MainLayout.setObjectName("MainLayout")
        self.table = QtWidgets.QTableWidget(parent=self.frame)
        self.table.setMinimumSize(QtCore.QSize(int(650), int(280)))
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
#         self.Calendar = QtWidgets.QCalendarWidget(parent=self.frame)
#         self.Calendar.setEnabled(True)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.Calendar.sizePolicy().hasHeightForWidth())
#         self.Calendar.setSizePolicy(sizePolicy)
#         self.Calendar.setMinimumSize(QtCore.QSize(int(200), int(400)))
#         self.Calendar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
#         font = QtGui.QFont()
#         font.setPointSize(int(10))
#         self.Calendar.setFont(font)
#         self.Calendar.setStyleSheet("QCalendarWidget QWidget{\n"
# "background-color: rgb(3, 174, 236);\n"
# "}\n"
# "\n"
# "QCalendarWidget QTableView{\n"
# "    background-color: white;\n"
# "}\n"
# "\n"
# "QCalendarWidget QToolButton {\n"
# "    color: white;\n"
# "    font-size:15px;\n"
# "    icon-size:20px 20px;\n"
# "    background-color:rgb(3, 174, 236);\n"
# "}\n"
# "\n"
# "QCalendarWidget QToolButton::hover {\n"
# "    background-color : #019ad2;\n"
# "}\n"
# "\n"
# "QCalendarWidget QToolButton::pressed {\n"
# "    background-color: rgb(1, 140, 190);\n"
# "    border: 3px solid;\n"
# "    border-color: rgb(255, 255, 255);\n"
# "}\n"
# "\n"
# "QCalendarWidget QSpinBox{\n"
# "    background-color: rgb(255, 255, 255);\n"
# "    border: 2px solid;\n"
# "    border-color: rgb(3,174, 236);\n"
# "}\n"
# "\n"
# "QCalendarWidget QAbstractItemView:enabled{\n"
# "    selection-background-color: rgb(3, 174, 236);\n"
# "    selection-color: white;\n"
# "}\n"
# "\n"
# "#qt_calendar_prevmonth {\n"
# "    qproperty-icon: url(//nas01/DATOS/Comunes/EIPSA-ERP/Resources/Iconos/back_arrow.png);\n"
# "}\n"
# "#qt_calendar_nextmonth {\n"
# "    qproperty-icon: url(//nas01/DATOS/Comunes/EIPSA-ERP/Resources/Iconos/forward_arrow.png);\n"
# "}")
#         self.Calendar.setSelectedDate(QtCore.QDate.currentDate())
#         self.Calendar.setGridVisible(True)
#         self.Calendar.setNavigationBarVisible(True)
#         self.Calendar.setDateEditEnabled(True)
#         self.Calendar.setObjectName("Calendar")
#         self.BottomLayout.addWidget(self.Calendar)
        self.MainLayout.addLayout(self.BottomLayout)
        self.PrincipalScreen.addLayout(self.MainLayout)
        self.FrameApp.addLayout(self.PrincipalScreen)
        self.gridLayout.addLayout(self.FrameApp, 3, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        App_Workshop.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=App_Workshop)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 945, 22))
        self.menubar.setObjectName("menubar")
        App_Workshop.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=App_Workshop)
        self.statusbar.setObjectName("statusbar")
        App_Workshop.setStatusBar(self.statusbar)

        self.retranslateUi(App_Workshop)
        QtCore.QMetaObject.connectSlotsByName(App_Workshop)
        self.Button_QueryTag.clicked.connect(self.query_tag)
        self.Button_Manufacturing.clicked.connect(self.manufacture)
        self.Button_Assembly.clicked.connect(self.assembly)
        self.Button_Dispatch.clicked.connect(self.dispatch)
        self.Button_Times.clicked.connect(self.times)
        self.Button_Notification.clicked.connect(self.notifications)
        self.Button_Profile.clicked.connect(self.showMenu)

        self.load_notifications()


    def retranslateUi(self, App_Workshop):
        _translate = QtCore.QCoreApplication.translate
        App_Workshop.setWindowTitle(_translate("App_Workshop", "ERP EIPSA - Taller"))
        self.HeaderName.setText(_translate("App_Workshop", self.name))
        self.Button_QueryTag.setText(_translate("App_Workshop", "    Consultar TAG(s)"))
        self.Button_Manufacturing.setText(_translate("App_Workshop", "    Fabricación"))
        self.Button_Assembly.setText(_translate("App_Workshop", "    Montaje"))
        self.Button_Dispatch.setText(_translate("App_Workshop", "   Despachos"))
        self.Button_Times.setText(_translate("App_Workshop", "    Tiempos"))
        self.table.setSortingEnabled(True)


    def notifications(self):
        self.notification_window=Ui_HistoryNotifications_Window(self.username)
        self.notification_window.show()
        self.notification_window.Button_Cancel.clicked.connect(self.load_notifications)

    def query_tag(self):
        config_obj = configparser.ConfigParser()
        config_obj.read(r"C:\Program Files\ERP EIPSA\database.ini")
        dbparam = config_obj["postgresql"]
        # set your parameters for the database connection URI using the keys from the configfile.ini
        user_database = dbparam["user"]
        password_database = dbparam["password"]

        db_tags_tech = createConnection(user_database, password_database)
        if not db_tags_tech:
            sys.exit()

        self.edit_tags_app = Ui_EditTags_Workshop_Window(self.name, db_tags_tech)
        self.edit_tags_app.show()


    def manufacture(self):
        config_obj = configparser.ConfigParser()
        config_obj.read(r"C:\Program Files\ERP EIPSA\database.ini")
        dbparam = config_obj["postgresql"]
        # set your parameters for the database connection URI using the keys from the configfile.ini
        user_database = dbparam["user"]
        password_database = dbparam["password"]

        db_manufacture = createConnection(user_database, password_database)
        if not db_manufacture:
            sys.exit()

        self.workshop_window = Ui_Workshop_Window(db_manufacture)
        self.workshop_window.show()

    def assembly(self):
        config_obj = configparser.ConfigParser()
        config_obj.read(r"C:\Program Files\ERP EIPSA\database.ini")
        dbparam = config_obj["postgresql"]
        # set your parameters for the database connection URI using the keys from the configfile.ini
        user_database = dbparam["user"]
        password_database = dbparam["password"]

        db_assembly = createConnection(user_database, password_database)
        if not db_assembly:
            sys.exit()

        self.assembly_window = Ui_Assembly_Window(db_assembly)
        self.assembly_window.show()



    def dispatch(self):
        print('ordenes de compra')


    def times(self):
        print('ordenes de compra')


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

# Function to load number of notifications
    def load_notifications(self):
        query_tables_notifications = """SELECT table_name
                                FROM information_schema.tables
                                WHERE table_schema = 'notifications' AND table_type = 'BASE TABLE';"""
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            cur.execute(query_tables_notifications)
            results=cur.fetchall()
            tables_names=[x[0] for x in results]

            notifications = []

            for table in tables_names:
                commands_notifications = f" SELECT * FROM notifications.{table} WHERE username = '{self.username}' and state = 'Pendiente'"
                cur.execute(commands_notifications)
                results=cur.fetchall()

                for x in results:
                    notifications.append(x)

        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        if len(notifications) != 0:
            icon13 = QtGui.QIcon()
            icon13.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Notif_on.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        else:
            icon13 = QtGui.QIcon()
            icon13.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Notif_off.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.Button_Notification.setIcon(icon13)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    App_Workshop = QtWidgets.QMainWindow()
    ui = Ui_App_Workshop()
    ui.setupUi(App_Workshop)
    App_Workshop.show()
    sys.exit(app.exec())