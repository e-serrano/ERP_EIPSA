# Form implementation generated from reading ui file 'Countries_Commercial_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtSql
from PyQt6.QtCore import Qt, QDate
from Database_Connection import createConnection
from config import config
import psycopg2
import configparser
from datetime import *
import os

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"



class AlignDelegate(QtWidgets.QStyledItemDelegate):
    """
    A custom item delegate for aligning cell content in a QTableView or QTableWidget to the center.

    Inherits from:
        QtWidgets.QStyledItemDelegate: Provides custom rendering and editing for table items.

    """
    def initStyleOption(self, option, index):
        """
        Initializes the style option for the item, setting its display alignment to center.

        Args:
            option (QtWidgets.QStyleOptionViewItem): The style option to initialize.
            index (QtCore.QModelIndex): The model index of the item.
        """
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter

class EditableTableModel(QtSql.QSqlTableModel):
    """
    A custom SQL table model that supports editable columns, headers, and special flagging behavior based on user permissions.

    Signals:
        updateFailed (str): Signal emitted when an update to the model fails.
    """
    updateFailed = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, column_range=None):
        """
        Initialize the model with user permissions and optional database and column range.

        Args:
            username (str): The username for permission-based actions.
            parent (QObject, optional): Parent object for the model. Defaults to None.
            column_range (list, optional): A list specifying the range of columns. Defaults to None.
        """
        super().__init__(parent)
        self.column_range = column_range

    def setAllColumnHeaders(self, headers):
        """
        Set headers for all columns in the model.

        Args:
            headers (list): A list of header names.
        """
        for column, header in enumerate(headers):
            self.setHeaderData(column, Qt.Orientation.Horizontal, header, Qt.ItemDataRole.DisplayRole)

    def setIndividualColumnHeader(self, column, header):
        """
        Set the header for a specific column.

        Args:
            column (int): The column index.
            header (str): The header name.
        """
        self.setHeaderData(column, Qt.Orientation.Horizontal, header, Qt.ItemDataRole.DisplayRole)

    def setIconColumnHeader(self, column, icon):
        """
        Set an icon in the header for a specific column.

        Args:
            column (int): The column index.
            icon (QIcon): The icon to display in the header.
        """
        self.setHeaderData(column, QtCore.Qt.Orientation.Horizontal, icon, Qt.ItemDataRole.DecorationRole)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        """
        Retrieve the header data for a specific section of the model.

        Args:
            section (int): The section index (column or row).
            orientation (Qt.Orientation): The orientation (horizontal or vertical).
            role (Qt.ItemDataRole, optional): The role for the header data. Defaults to DisplayRole.

        Returns:
            QVariant: The header data for the specified section.
        """
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return super().headerData(section, orientation, role)
        return super().headerData(section, orientation, role)

    def flags(self, index):
        """
        Get the item flags for a given index, controlling editability and selection based on user permissions.

        Args:
            index (QModelIndex): The index of the item.

        Returns:
            Qt.ItemFlags: The flags for the specified item.
        """
        flags = super().flags(index)
        if index.column() == 0:
            flags &= ~Qt.ItemFlag.ItemIsEditable
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        else:
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def getColumnHeaders(self, visible_columns):
        """
        Retrieve the headers for the specified visible columns.

        Args:
            visible_columns (list): List of column indices that are visible.

        Returns:
            list: A list of column headers for the visible columns.
        """
        column_headers = [self.headerData(col, Qt.Orientation.Horizontal) for col in visible_columns]
        return column_headers

class Ui_Countries_Window(QtWidgets.QMainWindow):
    """
    Main window for managing countries records.

    Attributes:
        model (EditableTableModel): The model for the editable table.
        db: The database connection.
    """
    def __init__(self, db):
        """
        Initializes the bank management window and sets up the UI.

        Args:
            db: The database connection.
        """
        super().__init__()
        self.model = EditableTableModel()
        self.db = db
        self.setupUi(self)
        self.model.dataChanged.connect(self.saveChanges)

    def closeEvent(self, event):
        """
        Handles the event triggered when the window is closed. Ensures models are cleared and database connections are closed.

        Args:
            event (QCloseEvent): The close event triggered when the window is about to close.
        """
        if self.model:
            self.model.clear()
        self.closeConnection()

    def closeConnection(self):
        """
        Closes the database connection and clears any references to the models.
        Also removes the 'drawing_index' database connection from Qt's connection list if it exists.
        """
        self.tableCountries.setModel(None)
        del self.model
        if self.db:
            self.db.close()
            del self.db
            if QtSql.QSqlDatabase.contains("qt_sql_default_connection"):
                QtSql.QSqlDatabase.removeDatabase("qt_sql_default_connection")

    def setupUi(self, Countries_Window):
        """
        Sets up the user interface for the Countries_Window.

        Args:
            Countries_Window (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        Countries_Window.setObjectName("Countries_Window")
        Countries_Window.resize(790, 595)
        Countries_Window.setMinimumSize(QtCore.QSize(790, 595))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Countries_Window.setWindowIcon(icon)
        Countries_Window.setStyleSheet(
".QFrame {\n"
"    border: 2px solid black;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(parent=Countries_Window)
        self.centralwidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setVerticalSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.hLayout1 = QtWidgets.QHBoxLayout()
        self.hLayout1.setObjectName("hLayout1")
        self.label_Name = QtWidgets.QLabel(parent=self.frame)
        self.label_Name.setMinimumSize(QtCore.QSize(80, 25))
        self.label_Name.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Name.setFont(font)
        self.label_Name.setObjectName("label_Name")
        self.hLayout1.addWidget(self.label_Name)
        self.Name_Countries = QtWidgets.QLineEdit(parent=self.frame)
        self.Name_Countries.setMinimumSize(QtCore.QSize(150, 25))
        self.Name_Countries.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Name_Countries.setFont(font)
        self.Name_Countries.setObjectName("Name_Countries")
        self.hLayout1.addWidget(self.Name_Countries)
        self.label_SubDate = QtWidgets.QLabel(parent=self.frame)
        self.label_SubDate.setMinimumSize(QtCore.QSize(80, 25))
        self.label_SubDate.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_SubDate.setFont(font)
        self.label_SubDate.setObjectName("label_SubDate")
        self.hLayout1.addWidget(self.label_SubDate)
        self.SubDate_Countries = QtWidgets.QLineEdit(parent=self.frame)
        self.SubDate_Countries.setMinimumSize(QtCore.QSize(150, 25))
        self.SubDate_Countries.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.SubDate_Countries.setFont(font)
        self.SubDate_Countries.setObjectName("SubDate_Countries")
        self.hLayout1.addWidget(self.SubDate_Countries)
        self.Button_Add = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Add.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_Add.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_Add.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_Add.setStyleSheet("QPushButton {\n"
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
"QPushButton:focus {\n"
"    background-color: #019ad2;\n"
"    border-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(1, 140, 190);\n"
"    border-color: rgb(255, 255, 255)\n"
"}\n"
"\n"
"QPushButton:focus:pressed {\n"
"    background-color: rgb(1, 140, 190);\n"
"    border-color: rgb(255, 255, 255);\n"
"}")
        self.Button_Add.setObjectName("Button_Add")
        self.hLayout1.addWidget(self.Button_Add)
        self.gridLayout_2.addLayout(self.hLayout1, 1, 0, 1, 1)
        self.hLayout2 = QtWidgets.QHBoxLayout()
        self.hLayout2.setObjectName("hLayout2")
        self.label_Agent = QtWidgets.QLabel(parent=self.frame)
        self.label_Agent.setMinimumSize(QtCore.QSize(80, 25))
        self.label_Agent.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Agent.setFont(font)
        self.label_Agent.setObjectName("label_Agent")
        self.hLayout2.addWidget(self.label_Agent)
        self.Agent_Countries = QtWidgets.QLineEdit(parent=self.frame)
        self.Agent_Countries.setMinimumSize(QtCore.QSize(150, 25))
        self.Agent_Countries.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Agent_Countries.setFont(font)
        self.Agent_Countries.setObjectName("Agent_Countries")
        self.hLayout2.addWidget(self.Agent_Countries)
        self.label_UnsubDate = QtWidgets.QLabel(parent=self.frame)
        self.label_UnsubDate.setMinimumSize(QtCore.QSize(80, 25))
        self.label_UnsubDate.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_UnsubDate.setFont(font)
        self.label_UnsubDate.setObjectName("label_UnsubDate")
        self.hLayout2.addWidget(self.label_UnsubDate)
        self.UnsubDate_Countries = QtWidgets.QLineEdit(parent=self.frame)
        self.UnsubDate_Countries.setMinimumSize(QtCore.QSize(150, 25))
        self.UnsubDate_Countries.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.UnsubDate_Countries.setFont(font)
        self.UnsubDate_Countries.setObjectName("UnsubDate_Countries")
        self.hLayout2.addWidget(self.UnsubDate_Countries)
        self.label_empty = QtWidgets.QLabel(parent=self.frame)
        self.label_empty.setMinimumSize(QtCore.QSize(150, 35))
        self.label_empty.setMaximumSize(QtCore.QSize(150, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_empty.setFont(font)
        self.label_empty.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_empty.setObjectName("label_empty")
        self.hLayout2.addWidget(self.label_empty)
        self.gridLayout_2.addLayout(self.hLayout2, 2, 0, 1, 1)
        self.hLayout3 = QtWidgets.QHBoxLayout()
        self.hLayout3.setObjectName("hLayout3")
        self.label_Porc = QtWidgets.QLabel(parent=self.frame)
        self.label_Porc.setMinimumSize(QtCore.QSize(80, 25))
        self.label_Porc.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Porc.setFont(font)
        self.label_Porc.setObjectName("label_Porc")
        self.hLayout3.addWidget(self.label_Porc)
        self.Porc_Countries = QtWidgets.QLineEdit(parent=self.frame)
        self.Porc_Countries.setMinimumSize(QtCore.QSize(150, 25))
        self.Porc_Countries.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Porc_Countries.setFont(font)
        self.Porc_Countries.setObjectName("Porc_Countries")
        self.hLayout3.addWidget(self.Porc_Countries)
        self.label_empty2 = QtWidgets.QLabel(parent=self.frame)
        self.label_empty2.setMinimumSize(QtCore.QSize(255, 35))
        self.label_empty2.setMaximumSize(QtCore.QSize(255, 35))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_empty2.setFont(font)
        self.label_empty2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_empty2.setObjectName("label_empty2")
        self.hLayout3.addWidget(self.label_empty2)
        self.Button_Delete = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Delete.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_Delete.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_Delete.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_Delete.setStyleSheet("QPushButton {\n"
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
"QPushButton:focus {\n"
"    background-color: #019ad2;\n"
"    border-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(1, 140, 190);\n"
"    border-color: rgb(255, 255, 255)\n"
"}\n"
"\n"
"QPushButton:focus:pressed {\n"
"    background-color: rgb(1, 140, 190);\n"
"    border-color: rgb(255, 255, 255);\n"
"}")
        self.Button_Delete.setObjectName("Button_Delete")
        self.hLayout3.addWidget(self.Button_Delete)
        self.gridLayout_2.addLayout(self.hLayout3, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 1)
        self.tableCountries=QtWidgets.QTableView(parent=self.frame)
        self.model = EditableTableModel()
        self.tableCountries.setObjectName("tableCountries")
        self.gridLayout_2.addWidget(self.tableCountries, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        Countries_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Countries_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 22))
        self.menubar.setObjectName("menubar")
        Countries_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Countries_Window)
        self.statusbar.setObjectName("statusbar")
        Countries_Window.setStatusBar(self.statusbar)

        self.retranslateUi(Countries_Window)
        QtCore.QMetaObject.connectSlotsByName(Countries_Window)
        self.Button_Delete.clicked.connect(self.deletecountry)
        self.Button_Add.clicked.connect(self.addcountry)
        self.query_Countries()
        self.model.dataChanged.connect(self.saveChanges)
        self.selection_model = self.tableCountries.selectionModel()
        self.selection_model.selectionChanged.connect(self.getdata)

# Function to translate and updates the text of various UI elements
    def retranslateUi(self, Countries_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        Countries_Window.setWindowTitle(_translate("Countries_Window", "País Destino"))
        self.tableCountries.setSortingEnabled(True)
        self.Button_Add.setText(_translate("Countries_Window", "Agregar"))
        self.Button_Delete.setText(_translate("Countries_Window", "Eliminar"))
        self.label_Name.setText(_translate("Countries_Window", "Nombre:"))
        self.label_Agent.setText(_translate("Countries_Window", "Agente:"))
        self.label_Porc.setText(_translate("Countries_Window", "Porcentaje:"))
        self.label_SubDate.setText(_translate("Countries_Window", "Fecha Alta:"))
        self.label_UnsubDate.setText(_translate("Countries_Window", "Fecha Baja:"))

# Function to add country record
    def addcountry(self):
        """
        Inserts a new bank record into the database after validating input fields.
        """
        name = self.Name_Countries.text()
        agent = self.Agent_Countries.text()
        porc = self.Porc_Countries.text()
        subdate = self.SubDate_Countries.text() if self.SubDate_Countries.text() != '' else None
        unsubdate = self.UnsubDate_Countries.text() if self.UnsubDate_Countries.text() != '' else None

        if name in ['', ' ']:
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("País Destino")
            dlg.setText('Debes rellenar el campo de "Nombre" como mínimo')
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            del dlg,new_icon

        else:
            commands_newcountry = ("""
                                INSERT INTO purch_fact.destination_country ("name","agent","porc","subscribe_date","unsubscribe_date")
                                VALUES (%s,%s,%s,%s,%s)
                                """)
            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands
                data=(name, agent, porc, subdate, unsubdate)
                cur.execute(commands_newcountry, data)
            # close communication with the PostgreSQL database server
                cur.close()
            # commit the changes
                conn.commit()

                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("País Destino")
                dlg.setText("Datos insertados con éxito")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                dlg.exec()
                del dlg,new_icon

                self.label_empty.setText('')
                self.Name_Countries.setText('')
                self.Agent_Countries.setText('')
                self.Porc_Countries.setText('')
                self.SubDate_Countries.setText('')
                self.UnsubDate_Countries.setText('')

                self.query_Countries()

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

# Function to delete country record
    def deletecountry(self):
        """
        Deletes the selected bank record from the database.
        """
        id_country = self.label_empty.text()

        if id_country == '':
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("País Destino")
            dlg.setText("Debes seleccionar un registro")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            del dlg,new_icon

        else:
            command_deletecountry = ("""
                                DELETE FROM purch_fact.destination_country
                                WHERE "id" =  %s
                                """)
            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands
                data=(id_country)
                cur.execute(command_deletecountry, data)
            # close communication with the PostgreSQL database server
                cur.close()
            # commit the changes
                conn.commit()

                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("País Destino")
                dlg.setText("Datos eliminados con éxito")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                dlg.exec()
                del dlg,new_icon

                self.label_empty.setText('')
                self.Name_Countries.setText('')
                self.Agent_Countries.setText('')
                self.Porc_Countries.setText('')
                self.SubDate_Countries.setText('')
                self.UnsubDate_Countries.setText('')

                self.query_Countries()

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

# Function to get data from record
    def getdata(self):
        """
        Fills input fields with data from the selected bank record in the table.
        """
        if len(self.tableCountries.selectedIndexes()) == 1:
            row = self.tableCountries.selectedIndexes()[0].row()
            self.label_empty.setText(str(self.model.data(self.model.index(row, 0))))
            self.Name_Countries.setText(self.model.data(self.model.index(row, 1)))
            self.Agent_Countries.setText(self.model.data(self.model.index(row, 2)))
            self.Porc_Countries.setText(str(self.model.data(self.model.index(row, 3))))
            subdate = self.model.data(self.model.index(row, 4))
            subdate = subdate.toString("dd/MM/yyyy")
            self.SubDate_Countries.setText(subdate)
            unsubdate = self.model.data(self.model.index(row, 5))
            unsubdate = unsubdate.toString("dd/MM/yyyy")
            self.UnsubDate_Countries.setText(unsubdate)

# Function to upload changes in database when field change
    def saveChanges(self):
        """
        Saves changes made to the data models and updates unique values for each column.
        """
        self.model.submitAll()

# Function to load table and setting in the window
    def query_Countries(self):
        """
        Queries the bank records from the database and updates the table view.
        """
        self.model.setTable("purch_fact.destination_country")
        self.model.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model.select()
        self.tableCountries.setModel(self.model)

        headers=['ID', 'Nombre', 'Agente', 'Porcentaje', 'Fecha Alta', 'Fecha Baja']

        self.tableCountries.setItemDelegate(AlignDelegate(self.tableCountries))
        self.tableCountries.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableCountries.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.tableCountries.setSortingEnabled(False)
        self.gridLayout_2.addWidget(self.tableCountries, 5, 0, 1, 1)

        self.model.setAllColumnHeaders(headers)



# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     config_obj = configparser.ConfigParser()
#     config_obj.read(r"C:\Program Files\ERP EIPSA\database.ini")
#     dbparam = config_obj["postgresql"]
#     # set your parameters for the database connection URI using the keys from the configfile.ini
#     user_database = dbparam["user"]
#     password_database = dbparam["password"]

#     if not createConnection(user_database, password_database):
#         sys.exit()

#     Countries_Window = Ui_Countries_Window()
#     Countries_Window.show()
#     sys.exit(app.exec())