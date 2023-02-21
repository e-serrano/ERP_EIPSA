# Form implementation generated from reading ui file 'TypeTAG_Menu.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from CreateTAG_Menu import *
from CreateTAGFlow_Window import *
from CreateTAGTemp_Window import *

class Ui_TypeTag_Menu(object):
    def setupUi(self, TypeTag_Menu):
        TypeTag_Menu.setObjectName("Type_Tag_Menu")
        TypeTag_Menu.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        TypeTag_Menu.resize(300, 400)
        TypeTag_Menu.setMinimumSize(QtCore.QSize(300, 400))
        TypeTag_Menu.setMaximumSize(QtCore.QSize(300, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        TypeTag_Menu.setWindowIcon(icon)
        TypeTag_Menu.setStyleSheet("QWidget {\n"
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
"  box-shadow: rgba(255, 255, 255, .4) 0 1px 0 0 inset;\n"
"  box-sizing: border-box;\n"
"  color: #fff;\n"
"  cursor: pointer;\n"
"  display: inline-block;\n"
"  font-family: -apple-system,system-ui,\"Segoe UI\",\"Liberation Sans\",sans-serif;\n"
"  font-size: 15px;\n"
"  font-weight: 800;\n"
"  line-height: 1.15385;\n"
"  margin: 0;\n"
"  outline: none;\n"
"  padding: 8px .8em;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  text-shadow: 0px 1px 0px #263666;\n"
"  user-select: none;\n"
"  -webkit-user-select: none;\n"
"  touch-action: manipulation;\n"
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
"}")
        self.centralwidget = QtWidgets.QWidget(parent=TypeTag_Menu)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(275, 325))
        self.frame.setMaximumSize(QtCore.QSize(275, 325))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem2, 6, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem3, 8, 0, 1, 1)
        self.Button_Temp = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Temp.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Temp.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Temp.setObjectName("Button_Temp")
        self.gridLayout_2.addWidget(self.Button_Temp, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(140, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Cancel.setEnabled(True)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.horizontalLayout.addWidget(self.Button_Cancel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 9, 0, 1, 1)
        self.Button_Flow = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Flow.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Flow.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Flow.setObjectName("Button_Flow")
        self.gridLayout_2.addWidget(self.Button_Flow, 1, 0, 1, 1)
        self.Button_Level = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Level.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Level.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Level.setObjectName("Button_Level")
        self.gridLayout_2.addWidget(self.Button_Level, 5, 0, 1, 1)
        self.Button_Others = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Others.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Others.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Others.setObjectName("Button_Others")
        self.gridLayout_2.addWidget(self.Button_Others, 7, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem5, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        TypeTag_Menu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=TypeTag_Menu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 22))
        self.menubar.setObjectName("menubar")
        TypeTag_Menu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=TypeTag_Menu)
        self.statusbar.setObjectName("statusbar")
        TypeTag_Menu.setStatusBar(self.statusbar)

        self.retranslateUi(TypeTag_Menu)
        self.Button_Cancel.clicked.connect(TypeTag_Menu.close) # type: ignore
        self.Button_Flow.clicked.connect(lambda: self.Typetag(TypeTag_Menu, 'Caudal'))
        self.Button_Temp.clicked.connect(lambda: self.Typetag(TypeTag_Menu, 'Temperatura'))
        self.Button_Level.clicked.connect(lambda: self.Typetag(TypeTag_Menu, 'Nivel'))
        self.Button_Others.clicked.connect(lambda: self.Typetag(TypeTag_Menu, 'Otros'))
        QtCore.QMetaObject.connectSlotsByName(TypeTag_Menu)


    def retranslateUi(self, TypeTag_Menu):
        _translate = QtCore.QCoreApplication.translate
        TypeTag_Menu.setWindowTitle(_translate("TypeTag_Menu", "Crear TAG"))
        self.Button_Temp.setText(_translate("TypeTag_Menu", "Temperatura"))
        self.Button_Cancel.setText(_translate("TypeTag_Menu", "Cancelar"))
        self.Button_Flow.setText(_translate("TypeTag_Menu", "Caudal"))
        self.Button_Level.setText(_translate("TypeTag_Menu", "Nivel"))
        self.Button_Others.setText(_translate("TypeTag_Menu", "Otros"))

    def Typetag(self, TypeTag_Menu, variable):
        final_variable=variable
        
        if final_variable=='Caudal':
            self.createtagQ_window=QtWidgets.QMainWindow()
            self.ui=Ui_CreateTAGFlow_Window()
            self.ui.setupUi(self.createtagQ_window)
            self.createtagQ_window.show()
            TypeTag_Menu.hide()
            self.ui.Button_Cancel.clicked.connect(TypeTag_Menu.show)

        if final_variable=='Temperatura':
            self.createtagT_window=QtWidgets.QMainWindow()
            self.ui=Ui_CreateTAGTemp_Window()
            self.ui.setupUi(self.createtagT_window)
            self.createtagT_window.show()
            TypeTag_Menu.hide()
            self.ui.Button_Cancel.clicked.connect(TypeTag_Menu.show)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TypeTag_Menu = QtWidgets.QMainWindow()
    ui = Ui_TypeTag_Menu()
    ui.setupUi(TypeTag_Menu)
    TypeTag_Menu.show()
    sys.exit(app.exec())
