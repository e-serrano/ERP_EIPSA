# Form implementation generated from reading ui file 'EditOrder_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6 import QtCore, QtGui, QtWidgets
import os

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class Ui_Verif_Dim_Drawing_Menu(object):
    def __init__(self, numorder, username):
        self.username=username
        self.numorder=numorder

    def setupUi(self, Verif_Dim_Drawing_Menu):
        Verif_Dim_Drawing_Menu.setObjectName("Verif_Dim_Drawing_Menu")
        Verif_Dim_Drawing_Menu.resize(300, 336)
        Verif_Dim_Drawing_Menu.setMinimumSize(QtCore.QSize(300, 300))
        Verif_Dim_Drawing_Menu.setMaximumSize(QtCore.QSize(300, 340))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Verif_Dim_Drawing_Menu.setWindowIcon(icon)
        if self.username == 'm.gil':
            Verif_Dim_Drawing_Menu.setStyleSheet("QWidget {\n"
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
            Verif_Dim_Drawing_Menu.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=Verif_Dim_Drawing_Menu)
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
        self.Button_Tags = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Tags.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Tags.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Tags.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Tags.setObjectName("Button_Tags")
        self.gridLayout_2.addWidget(self.Button_Tags, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.Button_Components = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Components.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Components.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Components.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Components.setObjectName("Button_Components")
        self.gridLayout_2.addWidget(self.Button_Components, 3, 0, 1, 1)
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
        Verif_Dim_Drawing_Menu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Verif_Dim_Drawing_Menu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 22))
        self.menubar.setObjectName("menubar")
        Verif_Dim_Drawing_Menu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Verif_Dim_Drawing_Menu)
        self.statusbar.setObjectName("statusbar")
        Verif_Dim_Drawing_Menu.setStatusBar(self.statusbar)
        Verif_Dim_Drawing_Menu.setWindowFlags(QtCore.Qt.WindowType.WindowMinimizeButtonHint)


        self.retranslateUi(Verif_Dim_Drawing_Menu)
        self.Button_Cancel.clicked.connect(Verif_Dim_Drawing_Menu.close) # type: ignore
        self.Button_Components.clicked.connect(lambda: self.of_components(Verif_Dim_Drawing_Menu))
        self.Button_Tags.clicked.connect(lambda: self.of_tags(Verif_Dim_Drawing_Menu))
        QtCore.QMetaObject.connectSlotsByName(Verif_Dim_Drawing_Menu)


    def retranslateUi(self, Verif_Dim_Drawing_Menu):
        _translate = QtCore.QCoreApplication.translate
        Verif_Dim_Drawing_Menu.setWindowTitle(_translate("Verif_Dim_Drawing_Menu", "Verificación"))
        self.Button_Components.setText(_translate("Verif_Dim_Drawing_Menu", "Dim Componentes/Almacén"))
        self.Button_Tags.setText(_translate("Verif_Dim_Drawing_Menu", "Dim Tags"))
        self.Button_Cancel.setText(_translate("Verif_Dim_Drawing_Menu", "Cancelar"))


    def of_tags(self,Verif_Dim_Drawing_Menu):
        from Verif_Dim_DrawingInsertTag_Window import Ui_Verif_Dim_DrawingInsertTag_Window
        self.of_drawing_insert_tag_window_menu=QtWidgets.QMainWindow()
        self.ui=Ui_Verif_Dim_DrawingInsertTag_Window(self.numorder, self.username)
        self.ui.setupUi(self.of_drawing_insert_tag_window_menu)
        self.of_drawing_insert_tag_window_menu.show()
        Verif_Dim_Drawing_Menu.close()


    def of_components(self,Verif_Dim_Drawing_Menu):
        from Verif_Dim_DrawingInsertComp_Window import Ui_Verif_Dim_DrawingInsertComp_Window
        self.of_drawing_insert_components_window_menu=QtWidgets.QMainWindow()
        self.ui=Ui_Verif_Dim_DrawingInsertComp_Window(self.numorder, self.username)
        self.ui.setupUi(self.of_drawing_insert_components_window_menu)
        self.of_drawing_insert_components_window_menu.show()
        Verif_Dim_Drawing_Menu.close()


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     Verif_Dim_Drawing_Menu = QtWidgets.QMainWindow()
#     ui = Ui_Verif_Dim_Drawing_Menu()
#     ui.setupUi(Verif_Dim_Drawing_Menu)
#     Verif_Dim_Drawing_Menu.show()
#     sys.exit(app.exec())
