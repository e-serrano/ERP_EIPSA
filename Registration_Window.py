# Form implementation generated from reading ui file 'Registration_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import re
import psycopg2
from config import config


class Ui_RegistrationWindow(object):
    def setupUi(self, RegistrationWindow):
        RegistrationWindow.setObjectName("RegistrationWindow")
        RegistrationWindow.resize(270, 615)
        RegistrationWindow.setMinimumSize(QtCore.QSize(270, 615))
        RegistrationWindow.setMaximumSize(QtCore.QSize(270, 615))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
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
        self.frame.setMinimumSize(QtCore.QSize(230, 550))
        self.frame.setMaximumSize(QtCore.QSize(230, 550))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(4, -1, 0, -1)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_name_reg = QtWidgets.QLabel(parent=self.frame)
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
        self.name_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.name_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name_reg.setFont(font)
        self.name_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.name_reg.setObjectName("name_reg")
        self.verticalLayout.addWidget(self.name_reg)
        self.label_secondname_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_secondname_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_secondname_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_secondname_reg.setFont(font)
        self.label_secondname_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_secondname_reg.setObjectName("label_secondname_reg")
        self.verticalLayout.addWidget(self.label_secondname_reg)
        self.secondname_reg = QtWidgets.QLineEdit(parent=self.frame)
        self.secondname_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.secondname_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.secondname_reg.setFont(font)
        self.secondname_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.secondname_reg.setObjectName("secondname_reg")
        self.verticalLayout.addWidget(self.secondname_reg)
        self.label_username_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_username_reg.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_username_reg.sizePolicy().hasHeightForWidth())
        self.label_username_reg.setSizePolicy(sizePolicy)
        self.label_username_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_username_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_username_reg.setFont(font)
        self.label_username_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_username_reg.setObjectName("label_username_reg")
        self.verticalLayout.addWidget(self.label_username_reg)
        self.username_reg = QtWidgets.QLineEdit(parent=self.frame)
        self.username_reg.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username_reg.sizePolicy().hasHeightForWidth())
        self.username_reg.setSizePolicy(sizePolicy)
        self.username_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.username_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.username_reg.setFont(font)
        self.username_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.username_reg.setObjectName("username_reg")
        self.verticalLayout.addWidget(self.username_reg)
        self.label_email_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_email_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_email_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_email_reg.setFont(font)
        self.label_email_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_email_reg.setObjectName("label_email_reg")
        self.verticalLayout.addWidget(self.label_email_reg)
        self.email_reg = QtWidgets.QLineEdit(parent=self.frame)
        self.email_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.email_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.email_reg.setFont(font)
        self.email_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.email_reg.setObjectName("email_reg")
        self.verticalLayout.addWidget(self.email_reg)
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
        self.password_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password_reg.setObjectName("password_reg")
        self.verticalLayout.addWidget(self.password_reg)
        self.label_rol_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_rol_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_rol_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_rol_reg.setFont(font)
        self.label_rol_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_rol_reg.setObjectName("label_rol_reg")
        self.verticalLayout.addWidget(self.label_rol_reg)
        self.rol_reg = QtWidgets.QComboBox(parent=self.frame)
        self.rol_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.rol_reg.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rol_reg.setFont(font)
        self.rol_reg.setObjectName("rol_reg")
        list_rol=['Comercial','Compras','Dirección','Fábrica','Facturación','Técnico',]
        self.rol_reg.addItems(list_rol)
        self.verticalLayout.addWidget(self.rol_reg)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.accept_reg = QtWidgets.QPushButton(parent=self.frame)
        self.accept_reg.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.accept_reg.sizePolicy().hasHeightForWidth())
        self.accept_reg.setSizePolicy(sizePolicy)
        self.accept_reg.setMinimumSize(QtCore.QSize(200, 30))
        self.accept_reg.setMaximumSize(QtCore.QSize(200, 30))
        self.accept_reg.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        font = QtGui.QFont()
        font.setFamily("-apple-system")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.accept_reg.setFont(font)
        self.accept_reg.setAutoDefault(True)
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
        self.exit_reg.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        font = QtGui.QFont()
        font.setFamily("-apple-system")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.exit_reg.setFont(font)
        self.exit_reg.setAutoDefault(True)
        self.exit_reg.setObjectName("exit_reg")
        self.verticalLayout.addWidget(self.exit_reg)
        self.label_error_reg = QtWidgets.QLabel(parent=self.frame)
        self.label_error_reg.setMinimumSize(QtCore.QSize(200, 25))
        self.label_error_reg.setMaximumSize(QtCore.QSize(200, 25))
        self.label_error_reg.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_error_reg.setText("")
        self.label_error_reg.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_error_reg.setWordWrap(True)
        self.label_error_reg.setObjectName("label_error_reg")
        self.verticalLayout.addWidget(self.label_error_reg)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 2)
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
        self.label_name_reg.setText(_translate("RegistrationWindow", "Nombre:"))
        self.label_secondname_reg.setText(_translate("RegistrationWindow", "Apellido:"))
        self.label_username_reg.setText(_translate("RegistrationWindow", "Nombre de Usuario:"))
        self.label_email_reg.setText(_translate("RegistrationWindow", "Correo electrónico:"))
        self.label_password_reg.setText(_translate("RegistrationWindow", "Contraseña:"))
        self.label_rol_reg.setText(_translate("RegistrationWindow", "Perfil:"))
        self.accept_reg.setText(_translate("RegistrationWindow", "Registrar"))
        self.exit_reg.setText(_translate("RegistrationWindow", "Salir"))


    def registration(self):
        reg_name=self.name_reg.text()
        reg_secondname=self.secondname_reg.text()
        reg_username=self.username_reg.text()
        reg_email=self.email_reg.text()
        reg_password=self.password_reg.text()
        reg_rol=self.rol_reg.currentText()

        if reg_name=="" or (reg_secondname=="" or (reg_username=="" or (reg_email=="" or reg_password==""))):
            self.label_error_reg.setText('Rellene todos los campos')

        else:
            if len(reg_username)<6:
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Username no válido")
                dlg.setText("El Username debe tener al menos 6 caracteres")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()

                del dlg, new_icon


            elif not re.fullmatch(r'[A-Za-z0-9]{8,}', reg_password):
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Contraseña no válida")
                dlg.setText("·La contraseña debe tener al menos 8 caracteres\n"
                            "·Debe contener al menos una mayúscula\n"
                            "·Debe contener al menos una minúscula\n"
                            "·Debe contener al menos un número")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()

                del dlg, new_icon


            elif not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', reg_email):
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Email no válido")
                dlg.setText("Por favor, introduzca un email válido")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()

                del dlg, new_icon


            else:
            #SQL Query for loading existing data in database
                commands = ("""
                            SELECT *
                            FROM datos_registro
                            """)
                conn = None
                try:
                # read the connection parameters
                    params = config()
                # connect to the PostgreSQL server
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                # execution of commands one by one
                    cur.execute(commands)
                    results=cur.fetchall()
                    match_username=list(filter(lambda x:reg_username in x, results))
                    match_email=list(filter(lambda x:reg_email in x, results))
                # close communication with the PostgreSQL database server
                    cur.close()
                # commit the changes
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if conn is not None:
                        conn.close()

            # checking if username registered in database
                if len(match_username)>0:
                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Registrar Usuario")
                    dlg.setText("El Nombre de Usuario introducido ya está registrado")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    dlg.exec()

            # checking if email registered in database
                elif len(match_email)>0:
                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Registrar Usuario")
                    dlg.setText("El correo electrónico introducido ya está registrado")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    dlg.exec()
                    del file, dlg, new_icon

                else:
                    commands = ("""
                                INSERT INTO datos_registro(
                                "id_registro","nombre","apellido","username","email","password","perfil")
                                VALUES (DEFAULT,%s,%s,%s,%s,%s,%s)
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
                        cur.execute(commands,data)
                    # close communication with the PostgreSQL database server
                        cur.close()
                    # commit the changes
                        conn.commit()

                    # showing success window
                        dlg = QtWidgets.QMessageBox()
                        new_icon = QtGui.QIcon()
                        new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                        dlg.setWindowIcon(new_icon)
                        dlg.setWindowTitle("Registrar Usuario")
                        dlg.setText("Usuario registrado con éxito")
                        dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        dlg.exec()

                    # putting all fields in blank
                        self.name_reg.setText('')
                        self.secondname_reg.setText('')
                        self.username_reg.setText('')
                        self.email_reg.setText('')
                        self.password_reg.setText('')

                        del dlg, new_icon

                    except (Exception, psycopg2.DatabaseError) as error:
                        print(error)
                    finally:
                        if conn is not None:
                            conn.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    RegistrationWindow = QtWidgets.QMainWindow()
    ui = Ui_RegistrationWindow()
    ui.setupUi(RegistrationWindow)
    RegistrationWindow.show()
    sys.exit(app.exec())