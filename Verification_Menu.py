# Form implementation generated from reading ui file 'EditOrder_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from VerificationInsert_Window import Ui_VerificationInsert_Window
from VerificationQuery_Window import Ui_VerificationQuery_Window
import os

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class Ui_Verification_Menu(object):
    def __init__(self, username):
        self.username=username

    def setupUi(self, Verification_Menu):
        Verification_Menu.setObjectName("Verification_Menu")
        Verification_Menu.resize(300, 336)
        Verification_Menu.setMinimumSize(QtCore.QSize(300, 300))
        Verification_Menu.setMaximumSize(QtCore.QSize(300, 340))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Verification_Menu.setWindowIcon(icon)
        if self.username == 'm.gil':
            Verification_Menu.setStyleSheet("QWidget {\n"
    "background-color: #121212;\n"
    "}\n"
    "\n"
    ".QFrame {\n"
    "    border: 2px solid white;\n"
    "}\n"
    "\n"
    "QPushButton {\n"
    "background-color: #33bdef;\n"
    "  border: 1px solid transparent;\n"
    "  border-radius: 3px;\n"
    "  color: #fff;\n"
    "  font-family: -apple-system,system-ui,\"Segoe UI\",\"Liberation Sans\",sans-serif;\n"
    "  font-size: 15px;\n"
    "  font-weight: 800;\n"
    "  line-height: 1.15385;\n"
    "  margin: 0;\n"
    "  outline: none;\n"
    "  padding: 8px .8em;\n"
    "  text-align: center;\n"
    "  text-decoration: none;\n"
    "  vertical-align: baseline;\n"
    "  white-space: nowrap;\n"
    "}\n"
    "\n"
    "QPushButton:hover {\n"
    "    background-color: #019ad2;\n"
    "    border-color: rgb(0, 0, 0);\n"
    "}\n"
    "\n"
    "QPushButton:pressed {\n"
    "    background-color: rgb(1, 140, 190);\n"
    "    border-color: rgb(255, 255, 255);\n"
    "}"
    )
        else:
            Verification_Menu.setStyleSheet("QWidget {\n"
    "background-color: rgb(255, 255, 255);\n"
    "}\n"
    "\n"
    ".QFrame {\n"
    "    border: 2px solid black;\n"
    "}\n"
    "\n"
    "QPushButton {\n"
    "background-color: #33bdef;\n"
    "  border: 1px solid transparent;\n"
    "  border-radius: 3px;\n"
    "  color: #fff;\n"
    "  font-family: -apple-system,system-ui,\"Segoe UI\",\"Liberation Sans\",sans-serif;\n"
    "  font-size: 15px;\n"
    "  font-weight: 800;\n"
    "  line-height: 1.15385;\n"
    "  margin: 0;\n"
    "  outline: none;\n"
    "  padding: 8px .8em;\n"
    "  text-align: center;\n"
    "  text-decoration: none;\n"
    "  vertical-align: baseline;\n"
    "  white-space: nowrap;\n"
    "}\n"
    "\n"
    "QPushButton:hover {\n"
    "    background-color: #019ad2;\n"
    "    border-color: rgb(0, 0, 0);\n"
    "}\n"
    "\n"
    "QPushButton:pressed {\n"
    "    background-color: rgb(1, 140, 190);\n"
    "    border-color: rgb(255, 255, 255);\n"
    "}"
    )
        self.centralwidget = QtWidgets.QWidget(parent=Verification_Menu)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(275, 275))
        self.frame.setMaximumSize(QtCore.QSize(275, 275))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 1)
        self.Button_Insert = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Insert.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Insert.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Insert.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Insert.setObjectName("Button_Insert")
        self.gridLayout_2.addWidget(self.Button_Insert, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.Button_Query = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Query.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Query.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Query.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Query.setObjectName("Button_Query")
        self.gridLayout_2.addWidget(self.Button_Query, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(140, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Cancel.setEnabled(True)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.horizontalLayout.addWidget(self.Button_Cancel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 5, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        Verification_Menu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Verification_Menu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 22))
        self.menubar.setObjectName("menubar")
        Verification_Menu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Verification_Menu)
        self.statusbar.setObjectName("statusbar")
        Verification_Menu.setStatusBar(self.statusbar)
        Verification_Menu.setWindowFlags(QtCore.Qt.WindowType.WindowMinimizeButtonHint)


        self.retranslateUi(Verification_Menu)
        self.Button_Cancel.clicked.connect(Verification_Menu.close) # type: ignore
        self.Button_Query.clicked.connect(lambda: self.query_Verification(Verification_Menu))
        self.Button_Insert.clicked.connect(lambda: self.insert_Verification(Verification_Menu))
        QtCore.QMetaObject.connectSlotsByName(Verification_Menu)


    def retranslateUi(self, Verification_Menu):
        _translate = QtCore.QCoreApplication.translate
        Verification_Menu.setWindowTitle(_translate("Verification_Menu", "Verificación"))
        self.Button_Query.setText(_translate("Verification_Menu", "Consultar"))
        self.Button_Insert.setText(_translate("Verification_Menu", "Insertar"))
        self.Button_Cancel.setText(_translate("Verification_Menu", "Cancelar"))


    def insert_Verification(self,Verification_Menu):
        self.Verificationinsert_window=QtWidgets.QMainWindow()
        self.ui=Ui_VerificationInsert_Window(self.username)
        self.ui.showMaximized()
        Verification_Menu.close()


    def query_Verification(self,Verification_Menu):
        self.Verificationquery_window=QtWidgets.QMainWindow()
        self.ui=Ui_VerificationQuery_Window(self.username)
        self.ui.setupUi(self.Verificationquery_window)
        self.Verificationquery_window.showMaximized()
        Verification_Menu.close()


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     Verification_Menu = QtWidgets.QMainWindow()
#     ui = Ui_Verification_Menu()
#     ui.setupUi(Verification_Menu)
#     Verification_Menu.show()
#     sys.exit(app.exec())
