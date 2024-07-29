#○ Form implementation generated from reading ui file 'Registration_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import random
import string
import re
import psycopg2
from config import config
import os
import hashlib 
from Email_Styles import emai_new_user

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class Ui_RegistrationWindow(object):
    def setupUi(self, RegistrationWindow):
        RegistrationWindow.setObjectName("RegistrationWindow")
        RegistrationWindow.resize(270, 615)
        RegistrationWindow.setMinimumSize(QtCore.QSize(270, 655))
        RegistrationWindow.setMaximumSize(QtCore.QSize(270, 655))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
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
"  color: #fff;\n"
"  font-family: -apple-system,system-ui,\"Segoe UI\",\"Liberation Sans\",sans-serif;\n"
"  font-size: 15px;\n"
"  font-weight: 800;\n"
"  line-height: 1.15385;\n"
"  margin: 0;\n"
"  outline: none;\n"
"  padding: 0px .8em;\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=RegistrationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(230, 590))
        self.frame.setMaximumSize(QtCore.QSize(230, 590))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(10)
        self.label_name_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_name_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_name_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_name_reg.setFont(font)
        self.label_name_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_name_reg.setObjectName("label_name_reg")
        self.gridLayout_3.addWidget(self.label_name_reg, 0, 0, 1, 1)
        self.name_reg = QtWidgets.QLineEdit(parent=self.frame)
        self.name_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.name_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name_reg.setFont(font)
        self.name_reg.setObjectName("name_reg")
        self.gridLayout_3.addWidget(self.name_reg, 1, 0, 1, 1)
        self.label_secondname_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_secondname_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_secondname_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_secondname_reg.setFont(font)
        self.label_secondname_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_secondname_reg.setObjectName("label_secondname_reg")
        self.gridLayout_3.addWidget(self.label_secondname_reg, 2, 0, 1, 1)
        self.secondname_reg = QtWidgets.QLineEdit(parent=self.frame)
        self.secondname_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.secondname_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.secondname_reg.setFont(font)
        self.secondname_reg.setObjectName("secondname_reg")
        self.gridLayout_3.addWidget(self.secondname_reg, 3, 0, 1, 1)
        self.label_username_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_username_reg.setEnabled(True)
        self.label_username_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_username_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_username_reg.setFont(font)
        self.label_username_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_username_reg.setObjectName("label_username_reg")
        self.gridLayout_3.addWidget(self.label_username_reg, 4, 0, 1, 1)
        self.username_reg = QtWidgets.QLineEdit(parent=self.frame)
        self.username_reg.setEnabled(True)
        self.username_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.username_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.username_reg.setFont(font)
        self.username_reg.setObjectName("username_reg")
        self.gridLayout_3.addWidget(self.username_reg, 5, 0, 1, 1)
        self.label_email_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_email_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_email_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_email_reg.setFont(font)
        self.label_email_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_email_reg.setObjectName("label_email_reg")
        self.gridLayout_3.addWidget(self.label_email_reg, 6, 0, 1, 1)
        self.email_reg = QtWidgets.QLineEdit(parent=self.frame)
        self.email_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.email_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.email_reg.setFont(font)
        self.email_reg.setObjectName("email_reg")
        self.gridLayout_3.addWidget(self.email_reg, 7, 0, 1, 1)
        self.label_rol_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_rol_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_rol_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_rol_reg.setFont(font)
        self.label_rol_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_rol_reg.setObjectName("label_rol_reg")
        self.gridLayout_3.addWidget(self.label_rol_reg, 8, 0, 1, 1)
        self.rol_reg = QtWidgets.QComboBox(parent=self.frame)
        self.rol_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.rol_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rol_reg.setFont(font)
        self.rol_reg.setObjectName("rol_reg")
        list_rol=['Almacén','Comercial','Compras','Dirección','Facturación','Taller','Técnico','Verificación']
        self.rol_reg.addItems(list_rol)
        self.gridLayout_3.addWidget(self.rol_reg, 9, 0, 1, 1)
        self.label_initials = QtWidgets.QLabel(parent=self.frame)
        self.label_initials.setMinimumSize(QtCore.QSize(200, 25))
        self.label_initials.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_initials.setFont(font)
        self.label_initials.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_initials.setObjectName("label_initials")
        self.gridLayout_3.addWidget(self.label_initials, 10, 0, 1, 1)
        self.initials_reg = QtWidgets.QLineEdit(parent=self.frame)
        self.initials_reg.setEnabled(True)
        self.initials_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.initials_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.initials_reg.setFont(font)
        self.initials_reg.setObjectName("initials_reg")
        self.gridLayout_3.addWidget(self.initials_reg, 11, 0, 1, 1)
        self.label_initials.setVisible(False)
        self.initials_reg.setVisible(False)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_3.addItem(spacerItem, 12, 0, 1, 1)
        self.accept_reg = QtWidgets.QPushButton(parent=self.frame)
        self.accept_reg.setEnabled(True)
        self.accept_reg.setMinimumSize(QtCore.QSize(200, 30))
        self.accept_reg.setMaximumSize(QtCore.QSize(200, 30))
        self.accept_reg.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        font = QtGui.QFont()
        font.setFamily("-apple-system")
        font.setPointSize(10)
        font.setBold(True)
        self.accept_reg.setFont(font)
        self.accept_reg.setAutoDefault(True)
        self.accept_reg.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.accept_reg.setObjectName("accept_reg")
        self.gridLayout_3.addWidget(self.accept_reg, 13, 0, 1, 1)
        self.exit_reg = QtWidgets.QPushButton(parent=self.frame)
        self.exit_reg.setEnabled(True)
        self.exit_reg.setMinimumSize(QtCore.QSize(200, 30))
        self.exit_reg.setMaximumSize(QtCore.QSize(200, 30))
        self.exit_reg.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        font = QtGui.QFont()
        font.setFamily("-apple-system")
        font.setPointSize(10)
        font.setBold(True)
        self.exit_reg.setFont(font)
        self.exit_reg.setAutoDefault(True)
        self.exit_reg.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.exit_reg.setObjectName("exit_reg")
        self.gridLayout_3.addWidget(self.exit_reg, 14, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)
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
        self.rol_reg.currentIndexChanged.connect(self.visible)


    def retranslateUi(self, RegistrationWindow):
        _translate = QtCore.QCoreApplication.translate
        RegistrationWindow.setWindowTitle(_translate("RegistrationWindow", "Registrar Usuario"))
        self.label_name_reg.setText(_translate("RegistrationWindow", "Nombre:"))
        self.label_secondname_reg.setText(_translate("RegistrationWindow", "Apellido:"))
        self.label_username_reg.setText(_translate("RegistrationWindow", "Nombre de Usuario:"))
        self.label_email_reg.setText(_translate("RegistrationWindow", "Correo electrónico:"))
        self.label_rol_reg.setText(_translate("RegistrationWindow", "Perfil:"))
        self.label_initials.setText(_translate("RegistrationWindow", "Siglas:"))
        self.accept_reg.setText(_translate("RegistrationWindow", "Registrar"))
        self.exit_reg.setText(_translate("RegistrationWindow", "Salir"))


    def registration(self):
        reg_name=self.name_reg.text()
        reg_secondname=self.secondname_reg.text()
        reg_username=self.username_reg.text()
        reg_email=self.email_reg.text()
        reg_rol=self.rol_reg.currentText()
        reg_initials=self.initials_reg.text()

    # Generating a random password
        caract = string.ascii_letters + string.digits + string.punctuation
        long = 12
        random_password = ""
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$')
        while True:
            for _ in range(long):
                random_password += random.choice(caract)

            if pattern.match(random_password):
                break
            else:
                random_password = ""

        if reg_name=="" or (reg_secondname=="" or (reg_username=="" or reg_email=="")):
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Registrar Usuario")
            dlg.setText("Rellene todos los campos")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            del dlg, new_icon

        elif reg_rol == 'Comercial' and reg_initials == '':
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Registrar Usuario")
            dlg.setText("Rellene el campo de siglas")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            del dlg, new_icon

        else:
            if len(reg_username)<6:
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Username no válido")
                dlg.setText("El Username debe tener al menos 6 caracteres")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()
                del dlg, new_icon

            elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', reg_email):
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Email no válido")
                dlg.setText("Por favor, introduzca un email válido")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()
                del dlg, new_icon


            else:
            #SQL Query for loading existing data in database
                commands_loadregdatabase = ("""
                            SELECT *
                            FROM users_data.registration
                            """)
                commands_loadinitials = ("""
                            SELECT *
                            FROM users_data.initials
                            """)
                conn = None
                try:
                # read the connection parameters
                    params = config()
                # connect to the PostgreSQL server
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                # execution of commands one by one
                    cur.execute(commands_loadregdatabase)
                    results=cur.fetchall()
                    match_username=list(filter(lambda x:reg_username in x, results))
                    match_email=list(filter(lambda x:reg_email in x, results))

                    cur.execute(commands_loadinitials)
                    results_initials=cur.fetchall()
                    match_initials=list(filter(lambda x:reg_initials in x, results_initials))
                # close communication with the PostgreSQL database server
                    cur.close()
                # commit the changes
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("ERP EIPSA")
                    dlg.setText("Ha ocurrido el siguiente error:\n"
                                + str(error))
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    dlg.exec()
                    del dlg, new_icon
                finally:
                    if conn is not None:
                        conn.close()

            # checking if username registered in database
                if len(match_username)>0:
                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Registrar Usuario")
                    dlg.setText("El nombre de usuario introducido ya está registrado")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    dlg.exec()
                    del dlg, new_icon

            # checking if email registered in database
                elif len(match_email)>0:
                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Registrar Usuario")
                    dlg.setText("El correo electrónico introducido ya está registrado")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    dlg.exec()
                    del dlg, new_icon

            # checking if initials registered in database
                elif len(match_initials)>0:
                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Registrar Usuario")
                    dlg.setText("Las siglas introducidas ya están registrado")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    dlg.exec()
                    del dlg, new_icon

                else:
                    password_bytes = random_password.encode('utf-8')
                    hash_object = hashlib.sha256(password_bytes)
                    reg_password = hash_object.hexdigest()

                    commands_reguser = ("""
                                INSERT INTO users_data.registration(
                                "id","name","surname","username","email","password","profile")
                                VALUES (DEFAULT,%s,%s,%s,%s,%s,%s)
                                """)
                    commands_initials = ("""
                                INSERT INTO users_data.initials(
                                "username","initials")
                                VALUES (%s,%s)
                                """)
                    conn = None
                    try:
                    # read the connection parameters
                        params = config()
                    # connect to the PostgreSQL server
                        conn = psycopg2.connect(**params)
                        cur = conn.cursor()
                    # execution of commands one by one
                        data=(reg_name,reg_secondname,reg_username,reg_email,reg_password,reg_rol,)
                        cur.execute(commands_reguser,data)
                        if reg_rol == 'Comercial':
                            data=(reg_username,reg_initials,)
                            cur.execute(commands_initials,data)
                    # close communication with the PostgreSQL database server
                        cur.close()
                    # commit the changes
                        conn.commit()

                        email = emai_new_user(reg_email, reg_username, reg_password)
                        email.send_email()

                    # showing success window
                        dlg = QtWidgets.QMessageBox()
                        new_icon = QtGui.QIcon()
                        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                        dlg.setWindowIcon(new_icon)
                        dlg.setWindowTitle("Registrar Usuario")
                        dlg.setText("Usuario registrado con éxito")
                        dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        dlg.exec()
                        del dlg, new_icon

                    # putting all fields in blank
                        self.name_reg.setText('')
                        self.secondname_reg.setText('')
                        self.username_reg.setText('')
                        self.email_reg.setText('')
                        self.initials_reg.setText('')

                    except (Exception, psycopg2.DatabaseError) as error:
                        dlg = QtWidgets.QMessageBox()
                        new_icon = QtGui.QIcon()
                        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                        dlg.setWindowIcon(new_icon)
                        dlg.setWindowTitle("ERP EIPSA")
                        dlg.setText("Ha ocurrido el siguiente error:\n"
                                    + str(error))
                        dlg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        dlg.exec()
                        del dlg, new_icon
                    finally:
                        if conn is not None:
                            conn.close()


    def visible(self):
        if self.rol_reg.currentText() != 'Comercial':
            self.label_initials.setVisible(False)
            self.initials_reg.setVisible(False)
        else:
            self.label_initials.setVisible(True)
            self.initials_reg.setVisible(True)

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     RegistrationWindow = QtWidgets.QMainWindow()
#     ui = Ui_RegistrationWindow()
#     ui.setupUi(RegistrationWindow)
#     RegistrationWindow.show()
#     sys.exit(app.exec())