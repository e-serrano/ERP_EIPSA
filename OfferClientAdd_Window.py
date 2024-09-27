# Form implementation generated from reading ui file 'OfferClientAdd_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config
import os

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class Ui_OfferClientAdd_Window(object):
    """
    UI class for the Offer client add window.
    """
    def setupUi(self, OfferClientAdd_Window):
        """
        Sets up the user interface for the OfferClientAdd_Window.

        Args:
            OfferClientAdd_Window (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        OfferClientAdd_Window.setObjectName("OfferClientAdd_Window")
        OfferClientAdd_Window.resize(275, 340)
        OfferClientAdd_Window.setMinimumSize(QtCore.QSize(275, 340))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        OfferClientAdd_Window.setWindowIcon(icon)
        OfferClientAdd_Window.setAutoFillBackground(False)
        OfferClientAdd_Window.setStyleSheet("QWidget {\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
".QFrame {\n"
"    border: 2px solid black;\n"
"}")
        OfferClientAdd_Window.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(parent=OfferClientAdd_Window)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_name_OfferClientAdd = QtWidgets.QLabel(parent=self.frame)
        self.label_name_OfferClientAdd.setEnabled(True)
        self.label_name_OfferClientAdd.setMinimumSize(QtCore.QSize(200, 25))
        self.label_name_OfferClientAdd.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_name_OfferClientAdd.setFont(font)
        self.label_name_OfferClientAdd.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_name_OfferClientAdd.setObjectName("label_name_OfferClientAdd")
        self.verticalLayout.addWidget(self.label_name_OfferClientAdd, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.name_OfferClientAdd = QtWidgets.QLineEdit(parent=self.frame)
        self.name_OfferClientAdd.setEnabled(True)
        self.name_OfferClientAdd.setMinimumSize(QtCore.QSize(200, 25))
        self.name_OfferClientAdd.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name_OfferClientAdd.setFont(font)
        self.name_OfferClientAdd.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.name_OfferClientAdd.setObjectName("name_OfferClientAdd")
        self.verticalLayout.addWidget(self.name_OfferClientAdd, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_country_OfferClientAdd = QtWidgets.QLabel(parent=self.frame)
        self.label_country_OfferClientAdd.setEnabled(True)
        self.label_country_OfferClientAdd.setMinimumSize(QtCore.QSize(200, 25))
        self.label_country_OfferClientAdd.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_country_OfferClientAdd.setFont(font)
        self.label_country_OfferClientAdd.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_country_OfferClientAdd.setObjectName("label_country_OfferClientAdd")
        self.verticalLayout.addWidget(self.label_country_OfferClientAdd, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.country_OfferClientAdd = QtWidgets.QComboBox(parent=self.frame)
        self.country_OfferClientAdd.setEnabled(True)
        self.country_OfferClientAdd.setMinimumSize(QtCore.QSize(200, 25))
        self.country_OfferClientAdd.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.country_OfferClientAdd.setFont(font)
        self.country_OfferClientAdd.setObjectName("country_OfferClientAdd")
        self.verticalLayout.addWidget(self.country_OfferClientAdd, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.add_OfferClientAdd = QtWidgets.QPushButton(parent=self.frame)
        self.add_OfferClientAdd.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_OfferClientAdd.sizePolicy().hasHeightForWidth())
        self.add_OfferClientAdd.setSizePolicy(sizePolicy)
        self.add_OfferClientAdd.setMinimumSize(QtCore.QSize(200, 35))
        self.add_OfferClientAdd.setMaximumSize(QtCore.QSize(200, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.add_OfferClientAdd.setFont(font)
        self.add_OfferClientAdd.setAutoDefault(True)
        self.add_OfferClientAdd.setStyleSheet("QPushButton {\n"
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
        self.add_OfferClientAdd.setObjectName("add_OfferClientAdd")
        self.verticalLayout.addWidget(self.add_OfferClientAdd, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.exit_OfferClientAdd = QtWidgets.QPushButton(parent=self.frame)
        self.exit_OfferClientAdd.setEnabled(True)
        self.exit_OfferClientAdd.setMinimumSize(QtCore.QSize(200, 35))
        self.exit_OfferClientAdd.setMaximumSize(QtCore.QSize(200, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.exit_OfferClientAdd.setFont(font)
        self.exit_OfferClientAdd.setAutoDefault(True)
        self.exit_OfferClientAdd.setStyleSheet("QPushButton {\n"
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
        self.exit_OfferClientAdd.setObjectName("exit_OfferClientAdd")
        self.verticalLayout.addWidget(self.exit_OfferClientAdd, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        OfferClientAdd_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=OfferClientAdd_Window)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 275, 22))
        self.menubar.setObjectName("menubar")
        OfferClientAdd_Window.setMenuBar(self.menubar)
        OfferClientAdd_Window.setWindowFlags(QtCore.Qt.WindowType.WindowMinimizeButtonHint)

        self.retranslateUi(OfferClientAdd_Window)
        self.add_OfferClientAdd.clicked.connect(self.add_client)
        self.exit_OfferClientAdd.clicked.connect(OfferClientAdd_Window.close)
        QtCore.QMetaObject.connectSlotsByName(OfferClientAdd_Window)

        commands_countries = "SELECT * FROM countries_list ORDER BY country_name"
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands one by one
            cur.execute(commands_countries)
            results_countries=cur.fetchall()

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

        list_countries=[x[0] for x in results_countries]
        self.country_OfferClientAdd.addItems(list_countries)


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, OfferClientAdd_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        OfferClientAdd_Window.setWindowTitle(_translate("OfferClientAdd_Window", "Añadir Cliente"))
        self.label_name_OfferClientAdd.setText(_translate("OfferClientAdd_Window", "Nombre Cliente:"))
        self.label_country_OfferClientAdd.setText(_translate("OfferClientAdd_Window", "País Cliente:"))
        self.add_OfferClientAdd.setText(_translate("OfferClientAdd_Window", "Añadir"))
        self.exit_OfferClientAdd.setText(_translate("OfferClientAdd_Window", "Salir"))


    def add_client(self):
        """
        Adds a new client to the database.
        """
        client_name=self.name_OfferClientAdd.text()
        country=self.country_OfferClientAdd.currentText()

        if client_name == '':
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Añadir Cliente")
            dlg.setText("Introduce un nombre de cliente")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
        else:
        #SQL Query for loading existing data in database
            commands = ("""
                        SELECT *
                        FROM clients_list
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
                match=list(filter(lambda x:client_name in x, results))
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
            
            if len(match)>0:
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Añadir Cliente")
                dlg.setText("El cliente ya se encuentra en la base de datos")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()

            else:
                commands = ("""
                    INSERT INTO clients_list ("client_name", "country") VALUES (%s,%s)
                    """)
                conn = None
                try:
                # read the connection parameters
                    params = config()
                # connect to the PostgreSQL server
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                # execution of commands one by one
                    cur.execute(commands,(client_name,country,))
                # close communication with the PostgreSQL database server
                    cur.close()
                # commit the changes
                    conn.commit()

                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Añadir Cliente")
                    dlg.setText("Cliente añadido con éxito")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    dlg.exec()
                    del dlg, new_icon
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    OfferClientAdd_Window = QtWidgets.QMainWindow()
    ui = Ui_OfferClientAdd_Window()
    ui.setupUi(OfferClientAdd_Window)
    OfferClientAdd_Window.show()
    sys.exit(app.exec())
