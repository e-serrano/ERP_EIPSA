# Form implementation generated from reading ui file 'Registration_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.
import os, sys
import tkinter as tk
from tkinter import *
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RegistrationWindow(object):
    def setupUi(self, RegistrationWindow):
        RegistrationWindow.setObjectName("RegistrationWindow")
        RegistrationWindow.resize(270, 413)
        RegistrationWindow.setMaximumSize(QtCore.QSize(270, 413))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        RegistrationWindow.setWindowIcon(icon)
        RegistrationWindow.setStyleSheet("QWidget {\n"
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
"  padding: 0px .8em;\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=RegistrationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(250, 352))
        self.frame.setMaximumSize(QtCore.QSize(250, 352))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_name_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_name_reg.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name_reg.sizePolicy().hasHeightForWidth())
        self.label_name_reg.setSizePolicy(sizePolicy)
        self.label_name_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_name_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_name_reg.setFont(font)
        self.label_name_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_name_reg.setObjectName("label_name_reg")
        self.verticalLayout.addWidget(self.label_name_reg)
        self.name_reg = QtWidgets.QLineEdit(parent=self.frame)
        self.name_reg.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_reg.sizePolicy().hasHeightForWidth())
        self.name_reg.setSizePolicy(sizePolicy)
        self.name_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.name_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name_reg.setFont(font)
        self.name_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.name_reg.setObjectName("name_reg")
        self.verticalLayout.addWidget(self.name_reg)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.label_password_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_password_reg.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_password_reg.sizePolicy().hasHeightForWidth())
        self.label_password_reg.setSizePolicy(sizePolicy)
        self.label_password_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_password_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_password_reg.setFont(font)
        self.label_password_reg.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_password_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_password_reg.setObjectName("label_password_reg")
        self.verticalLayout.addWidget(self.label_password_reg)
        self.password_reg = QtWidgets.QLineEdit(parent=self.frame)
        self.password_reg.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_reg.sizePolicy().hasHeightForWidth())
        self.password_reg.setSizePolicy(sizePolicy)
        self.password_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.password_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.password_reg.setFont(font)
        self.password_reg.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.password_reg.setObjectName("password_reg")
        self.verticalLayout.addWidget(self.password_reg)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.accept_reg = QtWidgets.QPushButton(parent=self.frame)
        self.accept_reg.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.accept_reg.sizePolicy().hasHeightForWidth())
        self.accept_reg.setSizePolicy(sizePolicy)
        self.accept_reg.setMinimumSize(QtCore.QSize(200, 30))
        self.accept_reg.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.accept_reg.setFont(font)
        self.accept_reg.setObjectName("accept_reg")
        self.verticalLayout.addWidget(self.accept_reg)
        self.exit_reg = QtWidgets.QPushButton(parent=self.frame)
        self.exit_reg.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_reg.sizePolicy().hasHeightForWidth())
        self.exit_reg.setSizePolicy(sizePolicy)
        self.exit_reg.setMinimumSize(QtCore.QSize(200, 30))
        self.exit_reg.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.exit_reg.setFont(font)
        self.exit_reg.setObjectName("exit_reg")
        self.verticalLayout.addWidget(self.exit_reg)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        RegistrationWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=RegistrationWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 270, 22))
        self.menubar.setObjectName("menubar")
        RegistrationWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=RegistrationWindow)
        self.statusbar.setObjectName("statusbar")
        RegistrationWindow.setStatusBar(self.statusbar)

        self.retranslateUi(RegistrationWindow)
        self.accept_reg.clicked.connect(self.registration) # type: ignore
        self.exit_reg.clicked.connect(RegistrationWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(RegistrationWindow)

    def retranslateUi(self, RegistrationWindow):
        _translate = QtCore.QCoreApplication.translate
        RegistrationWindow.setWindowTitle(_translate("RegistrationWindow", "Registrar Usuario"))
        self.label_name_reg.setText(_translate("RegistrationWindow", "Nombre de Usuario:"))
        self.label_password_reg.setText(_translate("RegistrationWindow", "Contraseña:"))
        self.accept_reg.setText(_translate("RegistrationWindow", "Registrar"))
        self.exit_reg.setText(_translate("RegistrationWindow", "Salir"))

    def registration(self):
        reg_name=self.name_reg.text()
        reg_password=self.password_reg.text()
        path=os.path.join(os.getcwd(), 'Passwords', reg_name)
        file=open(path, 'w')
        file.write(reg_name + '\n' + reg_password)
        file.close()
        self.reg_root=tk.Tk()
        self.reg_root.iconbitmap('icon.ico')
        Label(self.reg_root, text = 'Usuario registrado con éxito').pack()
        Button(self.reg_root, text ='Ok', command = self.reg_root.destroy).pack()
        self.reg_root.mainloop()

        del path, file, self.reg_root


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RegistrationWindow = QtWidgets.QMainWindow()
    ui = Ui_RegistrationWindow()
    ui.setupUi(RegistrationWindow)
    RegistrationWindow.show()
    sys.exit(app.exec())
