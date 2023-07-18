# Form implementation generated from reading ui file 'DeleteUser_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config
from User_Delete_DB import delete_user_database


class Ui_DeleteUser_Window(object):
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
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
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
        self.label_email_deleteuser = QtWidgets.QLabel(parent=self.frame)
        self.label_email_deleteuser.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_email_deleteuser.sizePolicy().hasHeightForWidth())
        self.label_email_deleteuser.setSizePolicy(sizePolicy)
        self.label_email_deleteuser.setMinimumSize(QtCore.QSize(200, 25))
        self.label_email_deleteuser.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_email_deleteuser.setFont(font)
        self.label_email_deleteuser.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_email_deleteuser.setObjectName("label_email_deleteuser")
        self.verticalLayout.addWidget(self.label_email_deleteuser, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.email_deleteuser = QtWidgets.QLineEdit(parent=self.frame)
        self.email_deleteuser.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email_deleteuser.sizePolicy().hasHeightForWidth())
        self.email_deleteuser.setSizePolicy(sizePolicy)
        self.email_deleteuser.setMinimumSize(QtCore.QSize(200, 25))
        self.email_deleteuser.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.email_deleteuser.setFont(font)
        self.email_deleteuser.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.email_deleteuser.setObjectName("email_deleteuser")
        self.verticalLayout.addWidget(self.email_deleteuser, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.delete_deleteuser = QtWidgets.QPushButton(parent=self.frame)
        self.delete_deleteuser.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_deleteuser.sizePolicy().hasHeightForWidth())
        self.delete_deleteuser.setSizePolicy(sizePolicy)
        self.delete_deleteuser.setMinimumSize(QtCore.QSize(200, 35))
        self.delete_deleteuser.setMaximumSize(QtCore.QSize(200, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.delete_deleteuser.setFont(font)
        self.delete_deleteuser.setStyleSheet("QPushButton {\n"
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
"}\n"
"\n"
"QPushButton:focus{\n"
"    background-color: #019ad2;\n"
"    border-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:focus:pressed {\n"
"    background-color: rgb(1, 140, 190);\n"
"    border-color: rgb(255, 255, 255);\n"
"}")
        self.delete_deleteuser.setAutoDefault(True)
        self.delete_deleteuser.setObjectName("delete_deleteuser")
        self.verticalLayout.addWidget(self.delete_deleteuser, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        ForgetPass_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=ForgetPass_Window)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 275, 22))
        self.menubar.setObjectName("menubar")
        ForgetPass_Window.setMenuBar(self.menubar)

        self.retranslateUi(ForgetPass_Window)
        self.delete_deleteuser.clicked.connect(self.delete_user)
        QtCore.QMetaObject.connectSlotsByName(ForgetPass_Window)


    def retranslateUi(self, ForgetPass_Window):
        _translate = QtCore.QCoreApplication.translate
        ForgetPass_Window.setWindowTitle(_translate("ForgetPass_Window", "Eliminar Usuario"))
        self.label_email_deleteuser.setText(_translate("ForgetPass_Window", "Correo electrónico:"))
        self.delete_deleteuser.setText(_translate("ForgetPass_Window", "Eliminar"))


    def delete_user(self):
        email=self.email_deleteuser.text()
        commands_checkemail = ("""
                    SELECT *
                    FROM registration
                    WHERE "email" = %s
                    """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            cur.execute(commands_checkemail,(email,))
            results=cur.fetchall()
            match=list(filter(lambda x:email in x, results))
        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        if len(match)==0:
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Eliminar usuario")
            dlg.setText("El correo introducido no está registrado")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            del dlg, new_icon

        else:
            commands_deleteuser = ("""
                        DELETE FROM registration
                        WHERE "email" = %s
                        """)
            conn = None
            try:
                delete_user_database(email)
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands
                cur.execute(commands_deleteuser,(email,))
            # close communication with the PostgreSQL database server
                cur.close()
            # commit the changes
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Eliminar usuario")
                dlg.setText("Usuario eliminado con éxito")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                dlg.exec()
                del dlg, new_icon

                self.email_deleteuser.setText('')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ForgetPass_Window = QtWidgets.QMainWindow()
    ui = Ui_DeleteUser_Window()
    ui.setupUi(ForgetPass_Window)
    ForgetPass_Window.show()
    sys.exit(app.exec())
