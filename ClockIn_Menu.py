# Form implementation generated from reading ui file 'EditOffer_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import os
import pandas as pd
import psycopg2
from tkinter.filedialog import askopenfilename
from config import config

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class Ui_ClockIn_Menu(QtWidgets.QMainWindow):
    """
    UI class for the Clock In Menu window.
    """
    def __init__(self, username):
        """
        Initializes the main window, setting up the user interface and storing user-specific details.

        Args:
            username (str): The username of the user.
        """
        super().__init__()
        self.username = username
        self.setupUi(self)

    def setupUi(self, ClockIn_Menu):
        """
        Sets up the user interface for the ClockIn_Menu.

        Args:
            ClockIn_Menu (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        ClockIn_Menu.setObjectName("ClockIn_Menu")
        ClockIn_Menu.resize(300, 336)
        ClockIn_Menu.setMinimumSize(QtCore.QSize(300, 400))
        ClockIn_Menu.setMaximumSize(QtCore.QSize(300, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ClockIn_Menu.setWindowIcon(icon)
        ClockIn_Menu.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=ClockIn_Menu)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.Button_Import = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Import.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Import.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Import.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Import.setObjectName("Button_Import")
        self.gridLayout_2.addWidget(self.Button_Import, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.Button_Query = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Query.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Query.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Query.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Query.setObjectName("Button_Query")
        self.gridLayout_2.addWidget(self.Button_Query, 3, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem3, 6, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 8, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(140, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Cancel.setEnabled(True)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.horizontalLayout.addWidget(self.Button_Cancel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 9, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem3, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        ClockIn_Menu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=ClockIn_Menu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 22))
        self.menubar.setObjectName("menubar")
        ClockIn_Menu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=ClockIn_Menu)
        self.statusbar.setObjectName("statusbar")
        ClockIn_Menu.setStatusBar(self.statusbar)
        ClockIn_Menu.setWindowFlags(QtCore.Qt.WindowType.WindowMinimizeButtonHint)


        self.retranslateUi(ClockIn_Menu)
        self.Button_Cancel.clicked.connect(ClockIn_Menu.close) # type: ignore
        self.Button_Import.clicked.connect(lambda: self.importclockin(ClockIn_Menu))
        self.Button_Query.clicked.connect(lambda: self.clockin(ClockIn_Menu))
        QtCore.QMetaObject.connectSlotsByName(ClockIn_Menu)


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, ClockIn_Menu):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        ClockIn_Menu.setWindowTitle(_translate("ClockIn_Menu", "Fichajes"))
        self.Button_Import.setText(_translate("ClockIn_Menu", "Importar"))
        self.Button_Query.setText(_translate("ClockIn_Menu", "Consultar"))
        self.Button_Cancel.setText(_translate("ClockIn_Menu", "Cancelar"))

# Function to import clock-in hours
    def importclockin(self):
        """
        Imports clock-in hours from a selected text file into the database.

        Prompts the user to select a text file, processes the data, 
        and inserts it into the 'clock_in_times' table in the PostgreSQL database.

        Raises:
            Exception: If there is an error during the database operation.
        """
        fname = askopenfilename(filetypes=[("Archivos de Excel", "*.txt")],
                        title="Seleccionar archivo Excel")

        if fname:
            try:
                # Expected columns
                column_names = ['worker_id', 'name', 'workday', 'type_day', 'notes', 'time_1', 'time_2', 'time_3', 'time_4','extra']
                
                df = pd.read_csv(fname, sep="|", header=None, names=column_names, encoding="latin-1")
                df = df.astype(str)
                df_final = df.iloc[1:,[0, 2, 4, 5, 6, 7, 8]].copy()
                columns_update = ['time_1', 'time_2', 'time_3', 'time_4']

                # Apply replace on selected columns
                df_final[columns_update] = df_final[columns_update].apply(lambda x: x.str.replace(r'\(\d+\)', '', regex=True))
                df_final[columns_update] = df_final[columns_update].apply(lambda x: x.str.replace('nan', '0:00', regex=True))

                params = config()
                conn = psycopg2.connect(**params)
                cursor = conn.cursor()

                for index, row in df_final.iterrows():
                # Create a list of pairs (column_name, column_value) for each column with value
                    columns_values = [(column, row[column]) for column in df_final.columns if not pd.isnull(row[column])]

                # Creating string for columns names
                    columns = ', '.join([column for column, _ in columns_values])

                # Creating string for columns values. For money/amount values, dots are replaced for commas to avoid insertion problems
                    values = ', '.join([f"'{values.replace(',', '.')}'" if column in ['time_ot'] else f"'{values}'" for column, values in columns_values])

                    sql_insertion = f"INSERT INTO clock_in_times ({columns}) VALUES ({values})"

                    cursor.execute(sql_insertion)

                conn.commit()
                cursor.close()

                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("ERP EIPSA")
                dlg.setText("Datos importados con éxito")
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

# Function to show calendar with clock-in hours
    def clockin(self):
        """
        Opens the calendar window for viewing clock-in hours.
        """
        from ClockIn_Window import MyCalendarApp
        self.clockin_window = MyCalendarApp(self.username)
        self.clockin_window.showMaximized()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ClockIn_Menu = QtWidgets.QMainWindow()
    ui = Ui_ClockIn_Menu()
    ui.setupUi(ClockIn_Menu)
    ClockIn_Menu.show()
    sys.exit(app.exec())
