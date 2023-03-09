# Form implementation generated from reading ui file 'ForgetPass_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


import os, sys
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ForgetPass_Window(object):
    def setupUi(self, ForgetPass_Window):
        ForgetPass_Window.setObjectName("ForgetPass_Window")
        ForgetPass_Window.resize(275, 340)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ForgetPass_Window.sizePolicy().hasHeightForWidth())
        ForgetPass_Window.setSizePolicy(sizePolicy)
        ForgetPass_Window.setMaximumSize(QtCore.QSize(275, 340))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ForgetPass_Window.setWindowIcon(icon)
        ForgetPass_Window.setAutoFillBackground(False)
        ForgetPass_Window.setStyleSheet("QWidget {\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
".QFrame {\n"
"    border: 2px solid black;\n"
"}")
        ForgetPass_Window.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(parent=ForgetPass_Window)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(230, 300))
        self.frame.setMaximumSize(QtCore.QSize(230, 300))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_email_forgetpass = QtWidgets.QLabel(parent=self.frame)
        self.label_email_forgetpass.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_email_forgetpass.sizePolicy().hasHeightForWidth())
        self.label_email_forgetpass.setSizePolicy(sizePolicy)
        self.label_email_forgetpass.setMinimumSize(QtCore.QSize(200, 25))
        self.label_email_forgetpass.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_email_forgetpass.setFont(font)
        self.label_email_forgetpass.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_email_forgetpass.setObjectName("label_email_forgetpass")
        self.verticalLayout.addWidget(self.label_email_forgetpass, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.email_forgetpass = QtWidgets.QLineEdit(parent=self.frame)
        self.email_forgetpass.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_forgetpass.sizePolicy().hasHeightForWidth())
        self.email_forgetpass.setSizePolicy(sizePolicy)
        self.email_forgetpass.setMinimumSize(QtCore.QSize(200, 25))
        self.email_forgetpass.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.email_forgetpass.setFont(font)
        self.email_forgetpass.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.email_forgetpass.setObjectName("email_forgetpass")
        self.verticalLayout.addWidget(self.email_forgetpass, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.send_forgetpass = QtWidgets.QPushButton(parent=self.frame)
        self.send_forgetpass.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.send_forgetpass.sizePolicy().hasHeightForWidth())
        self.send_forgetpass.setSizePolicy(sizePolicy)
        self.send_forgetpass.setMinimumSize(QtCore.QSize(200, 35))
        self.send_forgetpass.setMaximumSize(QtCore.QSize(200, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.send_forgetpass.setFont(font)
        self.send_forgetpass.setStyleSheet("QPushButton {\n"
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
"}")
        self.send_forgetpass.setObjectName("send_forgetpass")
        self.verticalLayout.addWidget(self.send_forgetpass, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        ForgetPass_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=ForgetPass_Window)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 275, 22))
        self.menubar.setObjectName("menubar")
        ForgetPass_Window.setMenuBar(self.menubar)

        self.retranslateUi(ForgetPass_Window)
        self.send_forgetpass.clicked.connect(self.send_email)
        QtCore.QMetaObject.connectSlotsByName(ForgetPass_Window)


    def retranslateUi(self, ForgetPass_Window):
        _translate = QtCore.QCoreApplication.translate
        ForgetPass_Window.setWindowTitle(_translate("ForgetPass_Window", "ERP EIPSA"))
        self.label_email_forgetpass.setText(_translate("ForgetPass_Window", "Correo electrónico:"))
        self.send_forgetpass.setText(_translate("ForgetPass_Window", "Enviar"))


    def send_email(self):
        email=self.email_forgetpass.text()
        print(email)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ForgetPass_Window = QtWidgets.QMainWindow()
    ui = Ui_ForgetPass_Window()
    ui.setupUi(ForgetPass_Window)
    ForgetPass_Window.show()
    sys.exit(app.exec())
