from PySide6 import QtCore, QtGui, QtWidgets
from PySide6 import QtSql
from PySide6.QtCore import Qt
from utils.Database_Manager import Create_DBconnection
import configparser
from datetime import *
import os

basedir = r"\\ERP-EIPSA-DATOS\DATOS\Comunes\EIPSA-ERP"

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
    updateFailed = QtCore.Signal(str)

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

class Ui_TechOffice_Window(QtWidgets.QMainWindow):
    """
    Main window class for the technical office interface.

    This class initializes the main window for the technical office application and sets up the user interface.

    Attributes:
        model (EditableTableModel): The model used to manage editable data in a table.
        db (Database): The database connection object for interacting with the database.
    """
    def __init__(self,db):
        """
        Initializes the Ui_TechOffice_Window class.

        Args:
            db (Database): A database connection object.
        """
        super().__init__()
        self.model = EditableTableModel()
        self.db = db
        self.setupUi(self)

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
        self.tableTechOf.setModel(None)
        del self.model
        if self.db:
            self.db.close()
            del self.db
            if QtSql.QSqlDatabase.contains("qt_sql_default_connection"):
                QtSql.QSqlDatabase.removeDatabase("qt_sql_default_connection")

    def setupUi(self, TechOffice_Window):
        """
        Sets up the user interface for the TechOffice_Window.

        Args:
            TechOffice_Window (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        self.id_list = []
        data_list = []
        TechOffice_Window.setObjectName("TechOffice_Window")
        TechOffice_Window.resize(400, 561)
        TechOffice_Window.setMinimumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        TechOffice_Window.setWindowIcon(icon)
        TechOffice_Window.setStyleSheet("QWidget {\n"
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
"}")
        self.centralwidget = QtWidgets.QWidget(parent=TechOffice_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem2, 0, 0, 1, 1)
        self.tableTechOf=QtWidgets.QTableView(parent=self.frame)
        self.model = EditableTableModel()
        self.tableTechOf.setObjectName("tableTechOf")
        self.gridLayout_2.addWidget(self.tableTechOf, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        TechOffice_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=TechOffice_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        TechOffice_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=TechOffice_Window)
        self.statusbar.setObjectName("statusbar")
        TechOffice_Window.setStatusBar(self.statusbar)
        self.tableTechOf.setSortingEnabled(True)
        self.tableTechOf.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        # TechOffice_Window.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.retranslateUi(TechOffice_Window)
        QtCore.QMetaObject.connectSlotsByName(TechOffice_Window)

        self.model.setTable("public.orders")
        self.model.setFilter("num_order LIKE 'P-%' AND num_order NOT LIKE '%R%' AND (porc_deliveries <> 100 OR porc_deliveries IS NULL)")
        self.model.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model.select()
        self.tableTechOf.setModel(self.model)

        for i in range(1,9):
            self.tableTechOf.hideColumn(i)
        for i in range(11,25):
            self.tableTechOf.hideColumn(i)
        for i in range(26,32):
            self.tableTechOf.hideColumn(i)

        headers=['Nº Pedido', '','','','','','','','',
                'Fecha Recepción','Observaciones',
                '','','','','','','','','','','','','','',
                'OK']

        self.tableTechOf.setItemDelegate(AlignDelegate(self.tableTechOf))
        self.tableTechOf.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableTechOf.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_2.addWidget(self.tableTechOf, 3, 0, 1, 1)

        self.model.setAllColumnHeaders(headers)

# Function to translate and updates the text of various UI elements
    def retranslateUi(self, TechOffice_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        TechOffice_Window.setWindowTitle(_translate("EditTags_Window", "Oficina Técnica"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     dbparam = config()
#     user_database = dbparam["user"]
#     password_database = dbparam["password"]

#     if not Create_DBconnection(user_database, password_database):
#         sys.exit()

#     TechOffice_Window = Ui_TechOffice_Window()
#     TechOffice_Window.show()
#     sys.exit(app.exec())