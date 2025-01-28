# Form implementation generated from reading ui file 'Login_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
import os
from PyQt6 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config
import hashlib

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class Ui_Login_Window(object):
    """
    Main window class for the Login Window. Manages the UI and interactions with the database.
    """
    def setupUi(self, Login_Window):
        """
        Sets up the user interface components for the main application window.

        Args:
            Login_Window (QtWidgets.QMainWindow): The main window object to set up.
        """
        self.Login_Window = Login_Window
        Login_Window.setObjectName("Login_Window")
        Login_Window.resize(670, 400)
        Login_Window.setMinimumSize(QtCore.QSize(670, 400))
        Login_Window.setMaximumSize(QtCore.QSize(670, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico")))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Login_Window.setWindowIcon(icon)
        Login_Window.setAutoFillBackground(False)
        Login_Window.setStyleSheet("QWidget {\n"
        "background-color: rgb(255, 255, 255);\n"
        "}\n"
        "\n"
        ".QFrame {\n"
        "    border: 2px solid black;\n"
        "}")
        Login_Window.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(parent=Login_Window)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 0, 1, 1)
        self.logo = QtWidgets.QLabel(parent=self.frame)
        self.logo.setMaximumSize(QtCore.QSize(275, 200))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Logo.ico"))))
        self.logo.setScaledContents(False)
        self.logo.setObjectName("logo")
        self.gridLayout_3.addWidget(self.logo, 1, 1, 7, 1)
        self.label_username_login = QtWidgets.QLabel(parent=self.frame)
        self.label_username_login.setEnabled(True)
        self.label_username_login.setMinimumSize(QtCore.QSize(200, 25))
        self.label_username_login.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_username_login.setFont(font)
        self.label_username_login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_username_login.setObjectName("label_username_login")
        self.gridLayout_3.addWidget(self.label_username_login, 1, 2, 1, 2)
        self.username_login = QtWidgets.QLineEdit(parent=self.frame)
        self.username_login.setEnabled(True)
        self.username_login.setMinimumSize(QtCore.QSize(200, 25))
        self.username_login.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.username_login.setFont(font)
        self.username_login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.username_login.setObjectName("username_login")
        self.gridLayout_3.addWidget(self.username_login, 2, 2, 1, 2)
        self.label_password_login = QtWidgets.QLabel(parent=self.frame)
        self.label_password_login.setEnabled(True)
        self.label_password_login.setMinimumSize(QtCore.QSize(200, 25))
        self.label_password_login.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_password_login.setFont(font)
        self.label_password_login.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_password_login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_password_login.setObjectName("label_password_login")
        self.gridLayout_3.addWidget(self.label_password_login, 3, 2, 1, 2)
        self.password_login = QtWidgets.QLineEdit(parent=self.frame)
        self.password_login.setEnabled(True)
        self.password_login.setMinimumSize(QtCore.QSize(200, 25))
        self.password_login.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.password_login.setFont(font)
        self.password_login.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password_login.setObjectName("password_login")
        self.gridLayout_3.addWidget(self.password_login, 4, 2, 1, 1)
        self.show_password = QtWidgets.QPushButton(parent=self.frame)
        self.show_password.setMinimumSize(QtCore.QSize(25, 25))
        self.show_password.setMaximumSize(QtCore.QSize(25, 25))
        self.show_password.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.show_password.setStyleSheet("\n"
        "QPushButton {\n"
        "background-color: #33bdef;\n"
        "  border: 1px solid transparent;\n"
        "  border-radius: 3px;\n"
        "  color: #fff;\n"
        "  font-family: -apple-system,system-ui,\"Segoe UI\",\"Liberation Sans\",sans-serif;\n"
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
        self.show_password.setObjectName("show_password")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Eye_White.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.show_password.setIcon(icon6)
        self.show_password.setIconSize(QtCore.QSize(20, 20))
        self.gridLayout_3.addWidget(self.show_password, 4, 3, 1, 1)
        
        self.accept_login = QtWidgets.QPushButton(parent=self.frame)
        self.accept_login.setEnabled(True)
        self.accept_login.setMinimumSize(QtCore.QSize(200, 35))
        self.accept_login.setMaximumSize(QtCore.QSize(16777215, 35))
        self.accept_login.setAutoDefault(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.accept_login.setFont(font)
        self.accept_login.setStyleSheet("\n"
        "QPushButton {\n"
        "background-color: #33bdef;\n"
        "  border: 1px solid transparent;\n"
        "  border-radius: 3px;\n"
        "  color: #fff;\n"
        "  font-family: -apple-system,system-ui,\"Segoe UI\",\"Liberation Sans\",sans-serif;\n"
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
        self.accept_login.setObjectName("accept_login")
        self.gridLayout_3.addWidget(self.accept_login, 6, 2, 1, 2)
        self.forgetpass_login = QtWidgets.QPushButton(parent=self.frame)
        self.forgetpass_login.setEnabled(True)
        self.forgetpass_login.setMinimumSize(QtCore.QSize(200, 35))
        self.forgetpass_login.setMaximumSize(QtCore.QSize(16777215, 35))
        self.forgetpass_login.setAutoDefault(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.forgetpass_login.setFont(font)
        self.forgetpass_login.setStyleSheet("QPushButton {\n"
        "background-color: #fff;\n"
        "  border: 1px solid transparent;\n"
        "  border-radius: 3px;\n"
        "  border-color: #33bdef;\n"
        "  color: #33bdef;\n"
        "  font-family: -apple-system,system-ui,\"Segoe UI\",\"Liberation Sans\",sans-serif;\n"
        "  font-weight: 800;\n"
        "  line-height: 1.15385;\n"
        "  margin: 0;\n"
        "  outline: none;\n"
        "  padding: 8px .8em;\n"
        "  text-align: center;\n"
        "  text-decoration: none;\n"
        "  vertical-align: center;\n"
        "  white-space: nowrap;\n"
        "}\n"
        "\n"
        "QPushButton:hover {\n"
        "    background-color: rgb(236, 236, 236);\n"
        "    border-color: rgb(0, 0, 0);\n"
        "}\n"
        "\n"
        "QPushButton:pressed {\n"
        "    background-color: rgb(220, 220, 220);\n"
        "    border-color: rgb(255, 255, 255);\n"
        "}\n"
        "\n"
        "QPushButton:focus{\n"
        "    background-color: rgb(236, 236, 236);\n"
        "    border-color: rgb(0, 0, 0);\n"
        "}\n"
        "\n"
        "QPushButton:focus:pressed {\n"
        "    background-color: rgb(220, 220, 220);\n"
        "    border-color: rgb(255, 255, 255);\n"
        "}")
        self.forgetpass_login.setObjectName("forgetpass_login")
        self.gridLayout_3.addWidget(self.forgetpass_login, 7, 2, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 0, 2, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 5, 2, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 8, 2, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        Login_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Login_Window)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 22))
        self.menubar.setObjectName("menubar")
        Login_Window.setMenuBar(self.menubar)

        self.retranslateUi(Login_Window)
        self.accept_login.clicked.connect(self.verification_login) # action when button 1 is pressed
        self.forgetpass_login.clicked.connect(self.forgetpassword) # action when button 2 is pressed
        self.password_login.returnPressed.connect(self.verification_login)
        QtCore.QMetaObject.connectSlotsByName(Login_Window)

        self.show_password.pressed.connect(self.start_show_timer)
        self.show_password.released.connect(self.stop_show_timer)

# Function to translate and updates the text of various UI elements
    def retranslateUi(self, Login_Window):
        """
        Translates and updates the text of various UI elements in the given Login_Window.
        """
        _translate = QtCore.QCoreApplication.translate
        Login_Window.setWindowTitle(_translate("Login_Window", "ERP EIPSA"))
        self.label_username_login.setText(_translate("Login_Window", "Nombre de Usuario:"))
        self.label_password_login.setText(_translate("Login_Window", "Contraseña:"))
        self.accept_login.setText(_translate("Login_Window", "Acceder"))
        self.forgetpass_login.setText(_translate("Login_Window", "¿Olvidaste la contraseña?"))

# Function to verify the login
    def verification_login(self):
        """
        Validates the user's login credentials. If the username or password fields are empty, 
        displays a warning message. If credentials are provided, queries the database to verify 
        the username and password. Depending on the user's role, opens the corresponding application 
        window. Displays error messages for invalid username, incorrect password, or unrecognized roles.
        """
        login_username = self.username_login.text().lower() if self.username_login.text().lower() != 'm' else 'm.sahuquillo'
        login_password = self.password_login.text()

        if login_username == '' or login_password == '':
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("EIPSA ERP")
            dlg.setText('Por favor, rellena los campos')
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()

        else:
            # SQL Query for loading existing data in database
            commands_userlogin = ("""
                        SELECT *
                        FROM users_data.registration
                        """)
            conn = None
            try:
                # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands one by one
                cur.execute(commands_userlogin)
                results = cur.fetchall()
                match = list(filter(lambda x: login_username in x, results))
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

        # checking if username is correct
            password_bytes = login_password.encode('utf-8')
            hash_object = hashlib.sha256(password_bytes)
            hashed_password = hash_object.hexdigest()

            if len(match) == 0:
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("EIPSA ERP")
                dlg.setText('Usuario incorrecto. Inténtalo de nuevo')
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()

        # checking if password is correct
            elif hashed_password != match[0][5]:
            # elif login_password != match[0][5]:
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("EIPSA ERP")
                dlg.setText('Contraseña incorrecta. Inténtalo de nuevo')
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()

            else:
                rol_app = match[0][6]

                if rol_app == 'Comercial':
                    from App_Comercial import Ui_App_Comercial
                    self.ui_comercial = Ui_App_Comercial(match[0][1]+' '+match[0][2], login_username)
                    self.ui_comercial.showMaximized()
                    self.Login_Window.close()

                elif rol_app == "Compras":
                    from App_Purchasing import Ui_App_Purchasing
                    self.app_window = QtWidgets.QMainWindow()
                    self.ui_purchase = Ui_App_Purchasing(match[0][1]+' '+match[0][2], login_username)
                    self.ui_purchase.setupUi(self.app_window)
                    self.app_window.showMaximized()
                    self.Login_Window.close()

                elif rol_app == "Técnico":
                    from App_Technical import Ui_App_Technical
                    self.app_window = Ui_App_Technical(match[0][1]+' '+match[0][2], login_username)
                    self.app_window.showMaximized()
                    self.Login_Window.close()

                elif rol_app == "Master":
                    from App_Master import Ui_App_Master
                    self.app_window = QtWidgets.QMainWindow()
                    self.ui_master = Ui_App_Master(match[0][1]+' '+match[0][2], login_username)
                    self.ui_master.setupUi(self.app_window)
                    self.app_window.showMaximized()
                    self.Login_Window.close()

                elif rol_app == "Almacén":
                    from App_Warehouse import Ui_App_Warehouse
                    self.app_window = QtWidgets.QMainWindow()
                    self.ui_warehouse = Ui_App_Warehouse(match[0][1]+' '+match[0][2], login_username)
                    self.ui_warehouse.setupUi(self.app_window)
                    self.app_window.showMaximized()
                    self.Login_Window.close()

                elif rol_app == "Taller":
                    from App_Workshop import Ui_App_Workshop
                    self.app_window = QtWidgets.QMainWindow()
                    self.ui_workshop = Ui_App_Workshop(match[0][1]+' '+match[0][2], login_username)
                    self.ui_workshop.setupUi(self.app_window)
                    self.app_window.showMaximized()
                    self.Login_Window.close()

                elif rol_app == "Dirección":
                    from App_Manager import Ui_App_Manager
                    self.app_window = QtWidgets.QMainWindow()
                    self.ui_manager = Ui_App_Manager(match[0][1]+' '+match[0][2], login_username)
                    self.ui_manager.setupUi(self.app_window)
                    self.app_window.showMaximized()
                    self.Login_Window.close()

                elif rol_app == "SubDirección":
                    from App_SubManager import Ui_App_SubManager
                    self.app_window = QtWidgets.QMainWindow()
                    self.ui_managerf = Ui_App_SubManager(match[0][1]+' '+match[0][2], login_username)
                    self.ui_managerf.setupUi(self.app_window)
                    self.app_window.showMaximized()
                    self.Login_Window.close()

                elif rol_app == "Facturación":
                    from App_Invoicing import Ui_App_Invoicing
                    self.app_window = QtWidgets.QMainWindow()
                    self.ui_invoice = Ui_App_Invoicing(match[0][1]+' '+match[0][2], login_username)
                    self.ui_invoice.setupUi(self.app_window)
                    self.app_window.showMaximized()
                    self.Login_Window.close()

                elif rol_app == 'Verificación':
                    from App_Verification import Ui_App_Verification
                    self.app_window = QtWidgets.QMainWindow()
                    self.ui_verification = Ui_App_Verification(match[0][1]+' '+match[0][2], login_username)
                    self.ui_verification.setupUi(self.app_window)
                    self.app_window.showMaximized()
                    self.Login_Window.close()

                else:
                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("ERP EIPSA")
                    dlg.setText("La aplicación no está disponible para este usuario. Disculpe las molestias")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    dlg.exec()
                    del dlg, new_icon

# Function when password has been forgotten
    def forgetpassword(self):
        """
        Opens a window for password recovery.
        """
        from PasswordForget_Window import Ui_ForgetPass_Window
        self.forgetpass_window=QtWidgets.QMainWindow()
        self.ui=Ui_ForgetPass_Window()
        self.ui.setupUi(self.forgetpass_window)
        self.forgetpass_window.show()

# Function to start timer when password view button is clicked
    def start_show_timer(self):
        """
        Sets the password field to normal mode, showing the password in plain text.
        """
        self.password_login.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)

# Function to stop timer when password view button is clicked
    def stop_show_timer(self):
        """
        Sets the password field to password mode, hiding the password.
        """
        self.password_login.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Login_Window = QtWidgets.QMainWindow()
    ui = Ui_Login_Window()
    ui.setupUi(Login_Window)
    Login_Window.show()
    sys.exit(app.exec())