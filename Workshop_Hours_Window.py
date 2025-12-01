from PySide6 import QtCore, QtGui, QtWidgets
from PySide6 import QtSql
from PySide6.QtCore import Qt
from utils.Database_Manager import Create_DBconnection
from datetime import *
import re
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QMimeData, QDate
from PySide6.QtGui import QKeySequence
import sys
from config import config, get_path
import locale
import pandas as pd



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

class CustomProxyModel_P(QtCore.QSortFilterProxyModel):
    """
    A custom proxy model that filters table rows based on expressions set for specific columns.

    Attributes:
        _filters (dict): A dictionary to store filter expressions for columns.
        header_names (dict): A dictionary to store header names for the table.

    Properties:
        filters: Getter for the current filter dictionary.

    """
    def __init__(self, parent=None):
        """
        Get the current filter expressions applied to columns.

        Returns:
            dict: Dictionary of column filters.
        """
        super().__init__(parent)
        self._filters = dict()
        self.header_names = {}

    @property
    def filters(self):
        """
        Get the current filter expressions applied to columns.

        Returns:
            dict: Dictionary of column filters.
        """
        return self._filters

    def setFilter(self, list_expresions, column, action_name=None):
        """
        Updates filters for a specified column based on provided expressions and action name.

        Args:
            list_expresions (list): List of filter expressions to be applied.
            column (int): Column index to which the filters are applied.
            action_name (str, optional): Action to determine how filters are updated. Defaults to None.
        """
        for expresion in list_expresions:
            if expresion or expresion == '':
                if column in self.filters:
                    if action_name or action_name == '':
                        self.filters[column].remove(expresion)
                    else:
                        self.filters[column].append(expresion)
                else:
                    self.filters[column] = [expresion]
            elif column in self.filters:
                if action_name or action_name == '':
                    self.filters[column].remove(expresion)
                    if not self.filters[column]:
                        del self.filters[column]
                else:
                    del self.filters[column]
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        """
        Check if a row passes the filter criteria based on the column filters.

        Args:
            source_row (int): The row number in the source model.
            source_parent (QModelIndex): The parent index of the row.

        Returns:
            bool: True if the row meets the filter criteria, False otherwise.
        """
        for column, expresions in self.filters.items():
            text = self.sourceModel().index(source_row, column, source_parent).data()

            if isinstance(text, QtCore.QDate): #Check if filters are QDate. If True, convert to text
                text = text.toString("yyyy-MM-dd")

            for expresion in expresions:
                if expresion == '':  # If expression is empty, match empty cells
                    if text == '':
                        break

                elif re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', str(expresion)):
                    expresion = QtCore.QDate.fromString(expresion, "dd/MM/yyyy")
                    expresion = expresion.toString("yyyy-MM-dd")
                    regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                    if regex.match(str(text)).hasMatch():
                        break

                else:
                    regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                    if regex.match(str(text)).hasMatch():
                        break
            else:
                return False
        return True

class EditableTableModel_P(QtSql.QSqlTableModel):
    """
    A custom SQL table model that supports editable columns, headers, and special flagging behavior based on user permissions.

    Signals:
        updateFailed (str): Signal emitted when an update to the model fails.
    """
    updateFailed = QtCore.Signal(str)

    def __init__(self, parent=None, column_range=None, database=None):
        """
        Initialize the model with user permissions and optional database and column range.

        Args:
            username (str): The username for permission-based actions.
            parent (QObject, optional): Parent object for the model. Defaults to None.
            column_range (list, optional): A list specifying the range of columns. Defaults to None.
        """
        super().__init__(parent, database)
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
        if index.column() in [0,4,25]:
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

class CustomProxyModel_O(QtCore.QSortFilterProxyModel):
    """
    A custom proxy model that filters table rows based on expressions set for specific columns.

    Attributes:
        _filters (dict): A dictionary to store filter expressions for columns.
        header_names (dict): A dictionary to store header names for the table.

    Properties:
        filters: Getter for the current filter dictionary.

    """
    def __init__(self, parent=None):
        """
        Get the current filter expressions applied to columns.

        Returns:
            dict: Dictionary of column filters.
        """
        super().__init__(parent)
        self._filters = dict()
        self.header_names = {}

    @property
    def filters(self):
        """
        Get the current filter expressions applied to columns.

        Returns:
            dict: Dictionary of column filters.
        """
        return self._filters

    def setFilter(self, list_expresions, column, action_name=None):
        """
        Updates filters for a specified column based on provided expressions and action name.

        Args:
            list_expresions (list): List of filter expressions to be applied.
            column (int): Column index to which the filters are applied.
            action_name (str, optional): Action to determine how filters are updated. Defaults to None.
        """
        for expresion in list_expresions:
            if expresion or expresion == '':
                if column in self.filters:
                    if action_name or action_name == '':
                        self.filters[column].remove(expresion)
                    else:
                        self.filters[column].append(expresion)
                else:
                    self.filters[column] = [expresion]
            elif column in self.filters:
                if action_name or action_name == '':
                    self.filters[column].remove(expresion)
                    if not self.filters[column]:
                        del self.filters[column]
                else:
                    del self.filters[column]
        self.invalidateFilter()


    def filterAcceptsRow(self, source_row, source_parent):
        """
        Check if a row passes the filter criteria based on the column filters.

        Args:
            source_row (int): The row number in the source model.
            source_parent (QModelIndex): The parent index of the row.

        Returns:
            bool: True if the row meets the filter criteria, False otherwise.
        """
        for column, expresions in self.filters.items():
            text = self.sourceModel().index(source_row, column, source_parent).data()

            if isinstance(text, QtCore.QDate): #Check if filters are QDate. If True, convert to text
                text = text.toString("yyyy-MM-dd")

            for expresion in expresions:
                if expresion == '':  # If expression is empty, match empty cells
                    if text == '':
                        break

                elif re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', str(expresion)):
                    expresion = QtCore.QDate.fromString(expresion, "dd/MM/yyyy")
                    expresion = expresion.toString("yyyy-MM-dd")
                    regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                    if regex.match(str(text)).hasMatch():
                        break

                else:
                    regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                    if regex.match(str(text)).hasMatch():
                        break
            else:
                return False
        return True

class EditableTableModel_O(QtSql.QSqlTableModel):
    """
    A custom SQL table model that supports editable columns, headers, and special flagging behavior based on user permissions.

    Signals:
        updateFailed (str): Signal emitted when an update to the model fails.
    """
    updateFailed = QtCore.Signal(str)

    def __init__(self, parent=None, column_range=None, database=None):
        """
        Initialize the model with user permissions and optional database and column range.

        Args:
            username (str): The username for permission-based actions.
            parent (QObject, optional): Parent object for the model. Defaults to None.
            column_range (list, optional): A list specifying the range of columns. Defaults to None.
        """
        super().__init__(parent, database)
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
        if index.column() in [0,4,25]:
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

class Ui_Workshop_Hours_Window(QtWidgets.QMainWindow):
    """
    A main window for managing workshop-related data, including models and proxies for tables.

    Inherits from:
        QtWidgets.QMainWindow: A top-level window that provides a main application window.
    
    Attributes:
        model_P (EditableTableModel_P): The model for table P.
        proxy_P (CustomProxyModel_P): The proxy model for table P.
        model_PA (EditableTableModel_PA): The model for table PA.
        proxy_PA (CustomProxyModel_PA): The proxy model for table PA.
        checkbox_states_P (dict): A dictionary tracking checkbox states for table P.
        dict_valuesuniques_P (dict): A dictionary of unique values for table P.
        dict_ordersort_P (dict): A dictionary for sorting orders in table P.
        action_checkbox_map_P (dict): A mapping of actions to checkboxes for table P.
        checkbox_filters_P (dict): A dictionary of filters applied to checkboxes for table P.
        checkbox_states_PA (dict): A dictionary tracking checkbox states for table PA.
        dict_valuesuniques_PA (dict): A dictionary of unique values for table PA.
        dict_ordersort_PA (dict): A dictionary for sorting orders in table PA.
        action_checkbox_map_PA (dict): A mapping of actions to checkboxes for table PA.
        checkbox_filters_PA (dict): A dictionary of filters applied to checkboxes for table PA.
        db (object): The database connection object.
        username (str): The username of the currently logged-in user.
    """
    def __init__(self, db, username):
        """
        Initializes the Ui_Workshop_Hours_Window, setting up models, proxies, and internal state.

        Args:
            db (object): The database connection object.
            username (str): The username of the currently logged-in user.
        """
        super().__init__()
        self.model_P = EditableTableModel_P(database=db)
        self.proxy_P = CustomProxyModel_P()
        self.model_O = EditableTableModel_O(database=db)
        self.proxy_O = CustomProxyModel_O()
        self.checkbox_states_P = {}
        self.dict_valuesuniques_P = {}
        self.dict_ordersort_P = {}
        self.action_checkbox_map_P = {}
        self.checkbox_filters_P = {}
        self.checkbox_states_O = {}
        self.dict_valuesuniques_O = {}
        self.dict_ordersort_O = {}
        self.action_checkbox_map_O = {}
        self.checkbox_filters_O = {}
        self.db = db
        self.username = username
        self.open_windows = {}
        self.model_P.dataChanged.connect(self.saveChanges)
        self.model_O.dataChanged.connect(self.saveChanges)
        self.setupUi(self)

    def closeEvent(self, event):
        """
        Handles the close event to clean up resources.

        Args:
            event (QtGui.QCloseEvent): The close event.
        """
        try:
            if self.model_P:
                self.model_P.clear()
            if self.model_O:
                self.model_O.clear()
            self.closeConnection()
        except Exception as e:
            print("Error during close event:", e)

    def closeConnection(self):
        """
        Closes the database connection and cleans up resources.
        """
        try:
            self.tableWorkshop_P.setModel(None)
            del self.model_P
            self.tableWorkshop_O.setModel(None)
            del self.model_O
            if self.db:
                self.db.close()
                del self.db
                if QtSql.QSqlDatabase.contains("workshop_connection"):
                    QtSql.QSqlDatabase.removeDatabase("workshop_connection")
        except Exception as e:
            print("Error closing connection:", e)


    def setupUi(self, Workshop_Hours_Window):
        """
        Sets up the user interface components for the main application window.

        Args:
            Workshop_Hours_Window (QtWidgets.QMainWindow): The main window object to set up.
        """
        self.id_list = []
        data_list = []
        Workshop_Hours_Window.setObjectName("Workshop_Hours_Window")
        Workshop_Hours_Window.resize(400, 561)
        Workshop_Hours_Window.setMinimumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Workshop_Hours_Window.setWindowIcon(icon)
        Workshop_Hours_Window.setStyleSheet(".QFrame {\n"
"    border: 2px solid;\n"
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
"}\n"
"QMenu {\n"
"background-color: white;\n"
"color: black;\n"
"}\n"
"QMenu::item {\n"
"background-color: white;\n"
"color: black;\n"
"}\n"
"QMenu::item:selected {background-color: rgb(3, 174, 236);}")
        self.centralwidget = QtWidgets.QWidget(parent=Workshop_Hours_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.hcab=QtWidgets.QHBoxLayout()
        self.hcab.setObjectName("hcab")
        self.toolExpExcel = QtWidgets.QToolButton(self.frame)
        self.toolExpExcel.setObjectName("ExpExcel_Button")
        self.toolExpExcel.setToolTip("Exportar a Excel")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "Excel.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolExpExcel.setIcon(icon)
        self.toolExpExcel.setIconSize(QtCore.QSize(25, 25))
        self.hcab.addWidget(self.toolExpExcel)
        self.hcabspacer=QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hcab.addItem(self.hcabspacer)
        self.gridLayout_2.addLayout(self.hcab, 0, 0, 1, 1)
        self.tabwidget = QtWidgets.QTabWidget(self.frame)
        self.tabwidget.setObjectName("tabwidget")
        self.tab_P = QtWidgets.QWidget()
        self.tab_P.setObjectName("tab_P")
        self.tabwidget.addTab(self.tab_P, "P-")
        self.tab_O = QtWidgets.QWidget()
        self.tab_O.setObjectName("tab_O")
        self.tabwidget.addTab(self.tab_O, "O-")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_P)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_O)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.hLayout_P = QtWidgets.QHBoxLayout()
        self.hLayout_P.setObjectName("hLayout_P")
        self.Button_All_P = QtWidgets.QPushButton(parent=self.frame)
        self.Button_All_P.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_All_P.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_All_P.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_All_P.setObjectName("Button_All_P")
        self.hLayout_P.addWidget(self.Button_All_P)
        self.gridLayout_3.addLayout(self.hLayout_P, 1, 0, 1, 1)
        self.tableWorkshop_P=QtWidgets.QTableView(parent=self.frame)
        self.model_P = EditableTableModel_P(database=self.db)
        self.tableWorkshop_P.setObjectName("tableWorkshop_P")
        self.gridLayout_3.addWidget(self.tableWorkshop_P, 2, 0, 1, 1)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.label_SumItems_P = QtWidgets.QLabel(parent=self.frame)
        self.label_SumItems_P.setMinimumSize(QtCore.QSize(40, 10))
        self.label_SumItems_P.setMaximumSize(QtCore.QSize(40, 10))
        self.label_SumItems_P.setText("")
        self.label_SumItems_P.setObjectName("label_SumItems_P")
        self.horizontalLayout.addWidget(self.label_SumItems_P)
        self.label_SumValue_P = QtWidgets.QLabel(parent=self.frame)
        self.label_SumValue_P.setMinimumSize(QtCore.QSize(80, 20))
        self.label_SumValue_P.setMaximumSize(QtCore.QSize(80, 20))
        self.label_SumValue_P.setText("")
        self.label_SumValue_P.setObjectName("label_SumValue_P")
        self.horizontalLayout.addWidget(self.label_SumValue_P)
        self.label_CountItems_P = QtWidgets.QLabel(parent=self.frame)
        self.label_CountItems_P.setMinimumSize(QtCore.QSize(60, 10))
        self.label_CountItems_P.setMaximumSize(QtCore.QSize(60, 10))
        self.label_CountItems_P.setText("")
        self.label_CountItems_P.setObjectName("label_CountItems_P")
        self.horizontalLayout.addWidget(self.label_CountItems_P)
        self.label_CountValue_P = QtWidgets.QLabel(parent=self.frame)
        self.label_CountValue_P.setMinimumSize(QtCore.QSize(80, 10))
        self.label_CountValue_P.setMaximumSize(QtCore.QSize(80, 10))
        self.label_CountValue_P.setText("")
        self.label_CountValue_P.setObjectName("label_CountValue_P")
        self.horizontalLayout.addWidget(self.label_CountValue_P)
        self.gridLayout_3.addLayout(self.horizontalLayout, 4, 0, 1, 1)

        self.hLayout_O = QtWidgets.QHBoxLayout()
        self.hLayout_O.setObjectName("hLayout_O")
        self.Button_All_O = QtWidgets.QPushButton(parent=self.frame)
        self.Button_All_O.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_All_O.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_All_O.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_All_O.setObjectName("Button_All_O")
        self.hLayout_O.addWidget(self.Button_All_O)
        self.gridLayout_4.addLayout(self.hLayout_O, 1, 0, 1, 1)
        self.tableWorkshop_O=QtWidgets.QTableView(parent=self.frame)
        self.model_O = EditableTableModel_O(database=self.db)
        self.tableWorkshop_O.setObjectName("tableWorkshop_O")
        self.gridLayout_4.addWidget(self.tableWorkshop_O, 2, 0, 1, 1)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.label_SumItems_O = QtWidgets.QLabel(parent=self.frame)
        self.label_SumItems_O.setMinimumSize(QtCore.QSize(40, 10))
        self.label_SumItems_O.setMaximumSize(QtCore.QSize(40, 10))
        self.label_SumItems_O.setText("")
        self.label_SumItems_O.setObjectName("label_SumItems_O")
        self.horizontalLayout.addWidget(self.label_SumItems_O)
        self.label_SumValue_O = QtWidgets.QLabel(parent=self.frame)
        self.label_SumValue_O.setMinimumSize(QtCore.QSize(80, 20))
        self.label_SumValue_O.setMaximumSize(QtCore.QSize(80, 20))
        self.label_SumValue_O.setText("")
        self.label_SumValue_O.setObjectName("label_SumValue_O")
        self.horizontalLayout.addWidget(self.label_SumValue_O)
        self.label_CountItems_O = QtWidgets.QLabel(parent=self.frame)
        self.label_CountItems_O.setMinimumSize(QtCore.QSize(60, 10))
        self.label_CountItems_O.setMaximumSize(QtCore.QSize(60, 10))
        self.label_CountItems_O.setText("")
        self.label_CountItems_O.setObjectName("label_CountItems_O")
        self.horizontalLayout.addWidget(self.label_CountItems_O)
        self.label_CountValue_O = QtWidgets.QLabel(parent=self.frame)
        self.label_CountValue_O.setMinimumSize(QtCore.QSize(80, 10))
        self.label_CountValue_O.setMaximumSize(QtCore.QSize(80, 10))
        self.label_CountValue_O.setText("")
        self.label_CountValue_O.setObjectName("label_CountValue_O")
        self.horizontalLayout.addWidget(self.label_CountValue_O)
        self.gridLayout_4.addLayout(self.horizontalLayout, 4, 0, 1, 1)

        self.gridLayout_2.addWidget(self.tabwidget, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        Workshop_Hours_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Workshop_Hours_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        Workshop_Hours_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Workshop_Hours_Window)
        self.statusbar.setObjectName("statusbar")
        Workshop_Hours_Window.setStatusBar(self.statusbar)
        self.tableWorkshop_P.setSortingEnabled(True)
        self.tableWorkshop_P.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid;}")
        self.tableWorkshop_O.setSortingEnabled(True)
        self.tableWorkshop_O.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid;}")
        # Workshop_Hours_Window.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.retranslateUi(Workshop_Hours_Window)
        QtCore.QMetaObject.connectSlotsByName(Workshop_Hours_Window)

        self.query_data()
        self.toolExpExcel.clicked.connect(self.exporttoexcel)
        self.tableWorkshop_P.selectionModel().selectionChanged.connect(self.countSelectedCells_P)
        self.tableWorkshop_O.selectionModel().selectionChanged.connect(self.countSelectedCells_O)


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, Workshop_Hours_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        Workshop_Hours_Window.setWindowTitle(_translate("EditTags_Window", "Fabricación"))
        self.Button_All_P.setText(_translate("EditTags_Window", "Ver Todos"))
        self.Button_All_O.setText(_translate("EditTags_Window", "Ver Todos"))

# Function to load orders on tables
    def query_data(self):
        """
        Queries the database for orders not delivered, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model_P.setTable("public.orders")
        self.model_P.setFilter("num_order NOT LIKE '%R%' AND (porc_deliveries <> 100 OR porc_deliveries IS NULL)")
        self.model_P.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model_P.select()
        self.proxy_P.setSourceModel(self.model_P)
        self.tableWorkshop_P.setModel(self.proxy_P)

        self.model_O.setTable("public.offers")
        self.model_O.setFilter("state NOT IN ('Declinada', 'Perdida', 'Adjudicada', 'No Ofertada', 'Budgetary')")
        self.model_O.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model_O.select()
        self.proxy_O.setSourceModel(self.model_O)
        self.tableWorkshop_O.setModel(self.proxy_O)

    # Getting the unique values for each column of the model
        for column in range(self.model_P.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_P:
                self.checkbox_states_P[column] = {}
                self.checkbox_states_P[column]['Seleccionar todo'] = True
                for row in range(self.model_P.rowCount()):
                    value = self.model_P.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_P[column][str(value)] = True
                self.dict_valuesuniques_P[column] = list_valuesUnique

    # Getting the unique values for each column of the model
        for column in range(self.model_O.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_O:
                self.checkbox_states_O[column] = {}
                self.checkbox_states_O[column]['Seleccionar todo'] = True
                for row in range(self.model_O.rowCount()):
                    value = self.model_O.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_O[column][str(value)] = True
                self.dict_valuesuniques_O[column] = list_valuesUnique

        for i in range(4, 45):
            self.tableWorkshop_P.hideColumn(i)

        for i in range(5,9):
            self.tableWorkshop_O.hideColumn(i)
        for i in range(10,38):
            self.tableWorkshop_O.hideColumn(i)

        headers_P =['Nº Pedido', 'Nº Oferta', 'Nº Ref', 'Fecha Pedido','Fecha Cont.','Notas Comercial','','','','','','','','Fecha Env Fab','F. Prev. Taller','',
                '% Montaje','Cambios %','F. Rec.','F. Prev. Montaje','Observaciones', 'Fecha Aviso',
                '', 'Fecha Envío', '', '','OK', '', '', '', '', '','','Extras', 'Aval', 'Estado Aval', 'Fecha Vto. Aval',
                '', 'Ordenes de Cambio', '', '', '', '% Env Fab', 'Notas Técnicas', '',
                'Almacén', 'Calidad', 'Empaquetado', 'Fresado', 'Montaje', 'Pirometría', 'Preparación', 'Soldadura', 'Taladro', 'Torno']

        headers_O =['Nº Oferta', 'Estado','Responsable','Cliente','Cliente Final',
                    '','','','','Material',
                    '','','','','',
                    '','','','','',
                    '','','','','',
                    '','','','','',
                    '','','','','',
                    '','', '',
                    'Almacén', 'Calidad', 'Empaquetado', 'Fresado', 'Montaje', 'Pirometría', 'Preparación', 'Soldadura', 'Taladro', 'Torno']
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(13, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(14, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(15, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(19, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_P.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_3.addWidget(self.tableWorkshop_P, 3, 0, 1, 1)

        self.model_P.setAllColumnHeaders(headers_P)

        self.Button_All_P.clicked.connect(self.query_all_P_workshop)
        self.tableWorkshop_P.setSortingEnabled(False)
        self.tableWorkshop_P.horizontalHeader().sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked_P)
        self.model_P.dataChanged.connect(self.saveChanges)

        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(13, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(14, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(15, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(19, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_O.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_4.addWidget(self.tableWorkshop_O, 3, 0, 1, 1)

        self.model_O.setAllColumnHeaders(headers_O)

        self.Button_All_O.clicked.connect(self.query_all_O_workshop)
        self.tableWorkshop_O.setSortingEnabled(False)
        self.tableWorkshop_O.horizontalHeader().sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked_O)
        self.model_O.dataChanged.connect(self.saveChanges)

        self.tableWorkshop_P.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableWorkshop_P, self.model_P, self.proxy_P)
        self.tableWorkshop_O.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableWorkshop_O, self.model_O, self.proxy_O)

# Function to save changes into database
    def saveChanges(self):
        """
        Saves changes made to the data models and updates unique values for each column.
        """
        self.model_P.submitAll()
        self.proxy_P.invalidateFilter()

        for column in range(self.model_P.columnCount()):
            list_valuesUnique = []
            for row in range(self.model_P.rowCount()):
                value = self.model_P.record(row).value(column)
                if value not in list_valuesUnique:
                    if isinstance(value, QtCore.QDate):
                        value=value.toString("dd/MM/yyyy")
                    list_valuesUnique.append(str(value))
                    if value not in self.checkbox_states_P[column]:
                        self.checkbox_states_P[column][value] = True
            self.dict_valuesuniques_P[column] = list_valuesUnique

        self.model_O.submitAll()

        for column in range(self.model_O.columnCount()):
            list_valuesUnique = []
            for row in range(self.model_O.rowCount()):
                value = self.model_O.record(row).value(column)
                if value not in list_valuesUnique:
                    if isinstance(value, QtCore.QDate):
                        value=value.toString("dd/MM/yyyy")
                    list_valuesUnique.append(str(value))
                    if value not in self.checkbox_states_O[column]:
                        self.checkbox_states_O[column][value] = True
            self.dict_valuesuniques_O[column] = list_valuesUnique

# Function when cancel button of menu is clicked
    def menu_cancelbutton_triggered(self):
        """
        Hides the menu when the cancel button is clicked.
        """
        self.menuValues.hide()

# Function for key events
    def custom_keyPressEvent(self, event, table, model, proxy):
        """
        Handles custom key events for cell operations in the table, including delete, copy, paste, and custom shortcuts.

        Args:
            event (QtGui.QKeyEvent): The key event to handle.
            table (QtWidgets.QTableView or QtWidgets.QTableWidget): The table that is handling the event.
            model (QtCore.QAbstractItemModel): The model associated with the table.
            proxy (QtCore.QSortFilterProxyModel): The proxy model used for filtering or sorting, if applicable.
        """
        if event.key() == QtCore.Qt.Key.Key_Delete:
            selected_indexes = table.selectionModel().selectedIndexes()
            if not selected_indexes:
                return
            
            model = table.model()
            model_indexes = [model.mapToSource(index) for index in selected_indexes]

            if isinstance(model, QtCore.QSortFilterProxyModel):
                model_indexes = [model.mapToSource(index) for index in selected_indexes]
                for index in model_indexes:
                    model.sourceModel().setData(index, None)
            else:
                model_indexes = selected_indexes
                for index in model_indexes:
                    model.setData(index, None)

        elif event.modifiers() and QtCore.Qt.KeyboardModifier.ControlModifier:
            if event.key() == QtCore.Qt.Key.Key_Comma:
                selected_indexes = table.selectionModel().selectedIndexes()
                if not selected_indexes:
                    return

                model = table.model()

                if isinstance(model, QtCore.QSortFilterProxyModel):
                    model_indexes = [model.mapToSource(index) for index in selected_indexes]
                    for index in model_indexes:
                        model.sourceModel().setData(index, date.today().strftime("%d/%m/%Y"))
                else:
                    model_indexes = selected_indexes
                    for index in model_indexes:
                        model.setData(index, date.today().strftime("%d/%m/%Y"))

        elif event.matches(QKeySequence.StandardKey.Copy):
            selected_indexes = table.selectionModel().selectedIndexes()
            if not selected_indexes:
                return
            
            model = table.model()
            model_indexes = [model.mapToSource(index) for index in selected_indexes]

            mime_data = QMimeData()
            data = bytearray()

            for index in model_indexes:
                data += str(model.data(index)).encode('utf-8') + b'\t'

            mime_data.setData("text/plain", data)

            clipboard = QApplication.clipboard()
            clipboard.setMimeData(mime_data)

        elif event.matches(QKeySequence.StandardKey.Paste):
            if table.selectionModel() != None:

                clipboard = QApplication.clipboard()
                mime_data = clipboard.mimeData()

                if not mime_data.hasFormat("text/plain"):
                    return

                data = mime_data.data("text/plain").data()
                values = data.split(b'\t')

                selected_indexes = table.selectionModel().selectedIndexes()
                if not selected_indexes:
                    return
                
                model = table.model()
                model_indexes = [model.mapToSource(index) for index in selected_indexes]

                for index, value in zip(model_indexes, values):
                    model.setData(index, value.decode('utf-8'))

                model.submitAll()

        elif event.matches(QKeySequence.StandardKey.InsertParagraphSeparator):
            current_index = table.currentIndex()
            if current_index.isValid() and not table.indexWidget(current_index):
                table.edit(current_index)

        elif event.matches(QKeySequence.StandardKey.MoveToNextLine):
            if table.selectionModel() != None:
                selected_indexes = table.selectionModel().selectedIndexes()
                if len(selected_indexes) == 1:
                    for index in selected_indexes:
                        current_row = index.row()
                        current_column = index.column()

                    new_row = current_row + 1 if current_row < model.rowCount() - 1 else current_row

                    table.selectionModel().clearSelection()
                    new_selection = QtCore.QItemSelection(QtCore.QModelIndex(model.index(new_row, current_column)), QtCore.QModelIndex(model.index(new_row, current_column)))
                    table.selectionModel().select(new_selection, QtCore.QItemSelectionModel.SelectionFlag.Select)

        elif event.matches(QKeySequence.StandardKey.MoveToPreviousLine):
            if table.selectionModel() != None:
                selected_indexes = table.selectionModel().selectedIndexes()
                if len(selected_indexes) == 1:
                    for index in selected_indexes:
                        current_row = index.row()
                        current_column = index.column()

                    new_row = current_row - 1 if current_row > 0 else 0

                    table.selectionModel().clearSelection()
                    new_selection = QtCore.QItemSelection(QtCore.QModelIndex(model.index(new_row, current_column)), QtCore.QModelIndex(model.index(new_row, current_column)))
                    table.selectionModel().select(new_selection, QtCore.QItemSelectionModel.SelectionFlag.Select)

        elif event.matches(QKeySequence.StandardKey.MoveToNextChar):
            if table.selectionModel() != None:
                selected_indexes = table.selectionModel().selectedIndexes()
                if len(selected_indexes) == 1:
                    for index in selected_indexes:
                        current_row = index.row()
                        current_column = index.column()

                    new_column = current_column + 1 if current_column < model.columnCount() - 1 else current_column

                    table.selectionModel().clearSelection()
                    new_selection = QtCore.QItemSelection(QtCore.QModelIndex(model.index(current_row, new_column)), QtCore.QModelIndex(model.index(current_row, new_column)))
                    table.selectionModel().select(new_selection, QtCore.QItemSelectionModel.SelectionFlag.Select)

        elif event.matches(QKeySequence.StandardKey.MoveToPreviousChar):
            if table.selectionModel() != None:
                selected_indexes = table.selectionModel().selectedIndexes()
                if len(selected_indexes) == 1:
                    for index in selected_indexes:
                        current_row = index.row()
                        current_column = index.column()

                    new_column = current_column - 1 if current_column > 1 else 1

                    table.selectionModel().clearSelection()
                    new_selection = QtCore.QItemSelection(QtCore.QModelIndex(model.index(current_row, new_column)), QtCore.QModelIndex(model.index(current_row, new_column)))
                    table.selectionModel().select(new_selection, QtCore.QItemSelectionModel.SelectionFlag.Select)


        super().keyPressEvent(event)

# Function to load data
    def query_all_P_workshop(self):
        """
        Queries the database for all orders P-, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model_P.dataChanged.disconnect(self.saveChanges)
        self.delete_allFilters_P()
        self.model_P.setTable("public.orders")
        self.model_P.setFilter("num_order LIKE 'P-%' AND num_order NOT LIKE '%R%'")
        self.model_P.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model_P.select()
        self.proxy_P.setSourceModel(self.model_P)
        self.tableWorkshop_P.setModel(self.proxy_P)

        # Getting the unique values for each column of the model
        for column in range(self.model_P.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_P:
                self.checkbox_states_P[column] = {}
                self.checkbox_states_P[column]['Seleccionar todo'] = True
                for row in range(self.model_P.rowCount()):
                    value = self.model_P.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_P[column][str(value)] = True
                self.dict_valuesuniques_P[column] = list_valuesUnique

        for i in range(4,44):
            self.tableWorkshop_P.hideColumn(i)

        headers_P =['Nº Pedido', 'Nº Oferta', 'Nº Ref', 'Fecha Pedido','Fecha Cont.','Notas Comercial','','','','','','','','Fecha Env Fab','F. Prev. Taller','',
                '% Montaje','Cambios %','F. Rec.','F. Prev. Montaje','Observaciones', 'Fecha Aviso',
                '', 'Fecha Envío', '', '','OK', '', '', '', '', '','','Extras', 'Aval', 'Estado Aval', 'Fecha Vto. Aval',
                '', 'Ordenes de Cambio', '', '', '', '% Env Fab', 'Notas Técnicas', '',
                'Almacén', 'Calidad', 'Empaquetado', 'Fresado', 'Montaje', 'Pirometría', 'Preparación', 'Soldadura', 'Taladro', 'Torno']

        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(13, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(14, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWorkshop_P.horizontalHeader().setSectionResizeMode(15, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_P.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid;}")
        self.gridLayout_3.addWidget(self.tableWorkshop_P, 2, 0, 1, 1)

        self.model_P.setAllColumnHeaders(headers_P)
        self.model_P.dataChanged.connect(self.saveChanges)

        self.tableWorkshop_P.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableWorkshop_P, self.model_P, self.proxy_P)

# Function to delete all filters
    def delete_allFilters_P(self):
        """
        Resets all filters and updates the table model with unique values for each column.
        """
        columns_number=self.model_P.columnCount()
        for index in range(columns_number):
            if index in self.proxy_P.filters:
                del self.proxy_P.filters[index]
            self.model_P.setIconColumnHeader(index, '')

        self.checkbox_states_P = {}
        self.dict_valuesuniques_P = {}
        self.dict_ordersort_P = {}
        self.checkbox_filters_P = {}

        self.proxy_P.invalidateFilter()
        self.tableWorkshop_P.setModel(None)
        self.tableWorkshop_P.setModel(self.proxy_P)

        # Getting the unique values for each column of the model
        for column in range(self.model_P.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_P:
                self.checkbox_states_P[column] = {}
                self.checkbox_states_P[column]['Seleccionar todo'] = True
                for row in range(self.model_P.rowCount()):
                    value = self.model_P.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_P[column][value] = True
                self.dict_valuesuniques_P[column] = list_valuesUnique

# Function when header is clicked
    def on_view_horizontalHeader_sectionClicked_P(self, logicalIndex):
        """
        Displays a menu when a column header is clicked. The menu includes options for sorting, filtering, and managing column visibility.
        
        Args:
            logicalIndex (int): Index of the clicked column.
        """
        self.logicalIndex = logicalIndex
        self.menuValues = QtWidgets.QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(self.tableWorkshop_P)

        valuesUnique_view = []
        for row in range(self.tableWorkshop_P.model().rowCount()):
            index = self.tableWorkshop_P.model().index(row, self.logicalIndex)
            value = index.data(Qt.ItemDataRole.DisplayRole)
            if value not in valuesUnique_view:
                if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
                valuesUnique_view.append(value)

        actionSortAscending = QtGui.QAction("Ordenar Ascendente", self.tableWorkshop_P)
        actionSortAscending.triggered.connect(self.on_actionSortAscending_triggered_P)
        self.menuValues.addAction(actionSortAscending)
        actionSortDescending = QtGui.QAction("Ordenar Descendente", self.tableWorkshop_P)
        actionSortDescending.triggered.connect(self.on_actionSortDescending_triggered_P)
        self.menuValues.addAction(actionSortDescending)
        self.menuValues.addSeparator()

        actionDeleteFilterColumn = QtGui.QAction("Quitar Filtro", self.tableWorkshop_P)
        actionDeleteFilterColumn.triggered.connect(self.on_actionDeleteFilterColumn_triggered_P)
        self.menuValues.addAction(actionDeleteFilterColumn)
        self.menuValues.addSeparator()

        actionTextFilter = QtGui.QAction("Buscar...", self.tableWorkshop_P)
        actionTextFilter.triggered.connect(self.on_actionTextFilter_triggered_P)
        self.menuValues.addAction(actionTextFilter)
        self.menuValues.addSeparator()

        scroll_menu = QtWidgets.QScrollArea()
        scroll_menu.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget(scroll_menu)
        scroll_menu.setWidget(scroll_widget)
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

        checkbox_all_widget = QtWidgets.QCheckBox('Seleccionar todo')

        if not self.checkbox_states_P[self.logicalIndex]['Seleccionar todo'] == True:
            checkbox_all_widget.setChecked(False)
        else:
            checkbox_all_widget.setChecked(True)
        
        checkbox_all_widget.toggled.connect(lambda checked, name='Seleccionar todo': self.on_select_all_toggled_P(checked, name))

        scroll_layout.addWidget(checkbox_all_widget)
        self.action_checkbox_map_P['Seleccionar todo'] = checkbox_all_widget

        if len(self.dict_ordersort_P) != 0 and self.logicalIndex in self.dict_ordersort_P:
            list_uniquevalues = sorted(list(set(self.dict_valuesuniques_P[self.logicalIndex])))
        else:
            list_uniquevalues = sorted(list(set(valuesUnique_view)))

        for actionName in list_uniquevalues:
            checkbox_widget = QtWidgets.QCheckBox(str(actionName))

            if self.logicalIndex not in self.checkbox_filters_P:
                checkbox_widget.setChecked(True)
            elif actionName not in self.checkbox_filters_P[self.logicalIndex]:
                checkbox_widget.setChecked(False)
            else:
                checkbox_widget.setChecked(True)

            checkbox_widget.toggled.connect(lambda checked, name=actionName: self.on_checkbox_toggled_P(checked, name))

            scroll_layout.addWidget(checkbox_widget)
            self.action_checkbox_map_P[actionName] = checkbox_widget

        action_scroll_menu = QtWidgets.QWidgetAction(self.menuValues)
        action_scroll_menu.setDefaultWidget(scroll_menu)
        self.menuValues.addAction(action_scroll_menu)

        self.menuValues.addSeparator()

        accept_button = QtGui.QAction("ACEPTAR", self.tableWorkshop_P)
        accept_button.triggered.connect(self.menu_acceptbutton_triggered_P)

        cancel_button = QtGui.QAction("CANCELAR", self.tableWorkshop_P)
        cancel_button.triggered.connect(self.menu_cancelbutton_triggered)

        self.menuValues.addAction(accept_button)
        self.menuValues.addAction(cancel_button)

        self.menuValues.setStyleSheet("QMenu::item:selected { background-color: #33bdef; }"
                                        "QMenu::item:pressed { background-color: rgb(1, 140, 190); }")

        headerPos = self.tableWorkshop_P.mapToGlobal(self.tableWorkshop_P.horizontalHeader().pos())        

        posY = headerPos.y() + self.tableWorkshop_P.horizontalHeader().height()
        scrollX = self.tableWorkshop_P.horizontalScrollBar().value()
        xInView = self.tableWorkshop_P.horizontalHeader().sectionViewportPosition(logicalIndex)
        posX = headerPos.x() + xInView - scrollX

        self.menuValues.exec(QtCore.QPoint(posX, posY))

# Function when accept button of menu is clicked
    def menu_acceptbutton_triggered_P(self):
        """
        Applies the selected filters and updates the table model with the new filters.
        """
        for column, filters in self.checkbox_filters_P.items():
            if filters:
                self.proxy_P.setFilter(filters, column)
            else:
                self.proxy_P.setFilter(None, column)

# Function when select all checkbox is clicked
    def on_select_all_toggled_P(self, checked, action_name):
        """
        Toggles the state of all checkboxes in the filter menu when the 'Select All' checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the 'Select All' checkbox.
            action_name (str): The name of the action (usually 'Select All').
        """
        filterColumn = self.logicalIndex
        imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
        icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))

        if checked:
            for checkbox_name, checkbox_widget in self.action_checkbox_map_P.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states_P[self.logicalIndex][checkbox_name] = checked

            if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map_P.values()):
                self.model_P.setIconColumnHeader(filterColumn, icono)
            else:
                self.model_P.setIconColumnHeader(filterColumn, '')
        
        else:
            for checkbox_name, checkbox_widget in self.action_checkbox_map_P.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states_P[self.logicalIndex][checkbox_widget.text()] = checked

# Function when checkbox of header menu is clicked
    def on_checkbox_toggled_P(self, checked, action_name):
        """
        Updates the filter state when an individual checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the checkbox.
            action_name (str): The name of the checkbox.
        """
        filterColumn = self.logicalIndex
        imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
        icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))

        if checked:
            if filterColumn not in self.checkbox_filters_P:
                self.checkbox_filters_P[filterColumn] = [action_name]
            else:
                if action_name not in self.checkbox_filters_P[filterColumn]:
                    self.checkbox_filters_P[filterColumn].append(action_name)
        else:
            if filterColumn in self.checkbox_filters_P and action_name in self.checkbox_filters_P[filterColumn]:
                self.checkbox_filters_P[filterColumn].remove(action_name)

        if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map_P.values()):
            self.model_P.setIconColumnHeader(filterColumn, '')
        else:
            self.model_P.setIconColumnHeader(filterColumn, icono)

# Function to delete individual column filter
    def on_actionDeleteFilterColumn_triggered_P(self):
        """
        Removes the filter from the selected column and updates the table model.
        """
        filterColumn = self.logicalIndex
        if filterColumn in self.proxy_P.filters:
            del self.proxy_P.filters[filterColumn]
        self.model_P.setIconColumnHeader(filterColumn, '')
        self.proxy_P.invalidateFilter()

        # self.tableWorkshop_P.setModel(None)
        self.tableWorkshop_P.setModel(self.proxy_P)

        if filterColumn in self.checkbox_filters_P:
            del self.checkbox_filters_P[filterColumn]

        self.checkbox_states_P[self.logicalIndex].clear()
        self.checkbox_states_P[self.logicalIndex]['Seleccionar todo'] = True
        for row in range(self.tableWorkshop_P.model().rowCount()):
            value = self.model_P.record(row).value(filterColumn)
            if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
            self.checkbox_states_P[self.logicalIndex][str(value)] = True

# Function to order column ascending
    def on_actionSortAscending_triggered_P(self):
        """
        Sorts the selected column in ascending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.AscendingOrder
        self.tableWorkshop_P.sortByColumn(sortColumn, sortOrder)

# Function to order column descending
    def on_actionSortDescending_triggered_P(self):
        """
        Sorts the selected column in descending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.DescendingOrder
        self.tableWorkshop_P.sortByColumn(sortColumn, sortOrder)

# Function when text is searched
    def on_actionTextFilter_triggered_P(self):
        """
        Opens a dialog to enter a text filter and applies it to the selected column.
        """
        filterColumn = self.logicalIndex
        dlg = QtWidgets.QInputDialog()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle('Buscar')
        clickedButton=dlg.exec()

        if clickedButton == 1:
            stringAction = dlg.textValue()
            if re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', stringAction):
                stringAction=QtCore.QDate.fromString(stringAction,"dd/MM/yyyy")
                stringAction=stringAction.toString("yyyy-MM-dd")

            filterString = QtCore.QRegularExpression(stringAction, QtCore.QRegularExpression.PatternOption(0))
            # del self.proxy.filters[filterColumn]
            self.proxy_P.setFilter([stringAction], filterColumn)

            imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
            icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))
            self.model_P.setIconColumnHeader(filterColumn, icono)


# Function to load data
    def query_all_O_workshop(self):
        """
        Queries the database for all orders O-, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model_O.dataChanged.disconnect(self.saveChanges)
        self.delete_allFilters_O()
        self.model_O.setTable("public.offers")
        self.model_O.setFilter("state NOT IN ('Declinada', 'Perdida', 'Adjudicada', 'No Ofertada', 'Budgetary')")
        self.model_O.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model_O.select()
        self.proxy_O.setSourceModel(self.model_O)
        self.tableWorkshop_O.setModel(self.proxy_O)

        # Getting the unique values for each column of the model
        for column in range(self.model_O.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_O:
                self.checkbox_states_O[column] = {}
                self.checkbox_states_O[column]['Seleccionar todo'] = True
                for row in range(self.model_O.rowCount()):
                    value = self.model_O.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_O[column][str(value)] = True
                self.dict_valuesuniques_O[column] = list_valuesUnique

        for i in range(5,9):
            self.tableWorkshop_O.hideColumn(i)
        for i in range(10,38):
            self.tableWorkshop_O.hideColumn(i)

        headers_O =['Nº Oferta', 'Estado','Responsable','Cliente','Cliente Final',
                    '','','','','Material',
                    '','','','','',
                    '','','','','',
                    '','','','','',
                    '','','','','',
                    '','','','','',
                    '','','',
                    'Almacén', 'Calidad', 'Empaquetado', 'Fresado', 'Montaje', 'Pirometría', 'Preparación', 'Soldadura', 'Taladro', 'Torno']

        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(13, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(14, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWorkshop_O.horizontalHeader().setSectionResizeMode(15, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableWorkshop_O.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid;}")
        self.gridLayout_4.addWidget(self.tableWorkshop_O, 2, 0, 1, 1)

        self.model_O.setAllColumnHeaders(headers_O)
        self.model_O.dataChanged.connect(self.saveChanges)

        self.tableWorkshop_O.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableWorkshop_O, self.model_O, self.proxy_O)

# Function to delete all filters
    def delete_allFilters_O(self):
        """
        Resets all filters and updates the table model with unique values for each column.
        """
        columns_number=self.model_O.columnCount()
        for index in range(columns_number):
            if index in self.proxy_O.filters:
                del self.proxy_O.filters[index]
            self.model_O.setIconColumnHeader(index, '')

        self.checkbox_states_O = {}
        self.dict_valuesuniques_O = {}
        self.dict_ordersort_O = {}
        self.checkbox_filters_O = {}

        self.proxy_O.invalidateFilter()
        self.tableWorkshop_O.setModel(None)
        self.tableWorkshop_O.setModel(self.proxy_O)

        # Getting the unique values for each column of the model
        for column in range(self.model_O.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_O:
                self.checkbox_states_O[column] = {}
                self.checkbox_states_O[column]['Seleccionar todo'] = True
                for row in range(self.model_O.rowCount()):
                    value = self.model_O.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_O[column][value] = True
                self.dict_valuesuniques_O[column] = list_valuesUnique

# Function when header is clicked
    def on_view_horizontalHeader_sectionClicked_O(self, logicalIndex):
        """
        Displays a menu when a column header is clicked. The menu includes options for sorting, filtering, and managing column visibility.
        
        Args:
            logicalIndex (int): Index of the clicked column.
        """
        self.logicalIndex = logicalIndex
        self.menuValues = QtWidgets.QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(self.tableWorkshop_O)

        valuesUnique_view = []
        for row in range(self.tableWorkshop_O.model().rowCount()):
            index = self.tableWorkshop_O.model().index(row, self.logicalIndex)
            value = index.data(Qt.ItemDataRole.DisplayRole)
            if value not in valuesUnique_view:
                if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
                valuesUnique_view.append(value)

        actionSortAscending = QtGui.QAction("Ordenar Ascendente", self.tableWorkshop_O)
        actionSortAscending.triggered.connect(self.on_actionSortAscending_triggered_O)
        self.menuValues.addAction(actionSortAscending)
        actionSortDescending = QtGui.QAction("Ordenar Descendente", self.tableWorkshop_O)
        actionSortDescending.triggered.connect(self.on_actionSortDescending_triggered_O)
        self.menuValues.addAction(actionSortDescending)
        self.menuValues.addSeparator()

        actionDeleteFilterColumn = QtGui.QAction("Quitar Filtro", self.tableWorkshop_O)
        actionDeleteFilterColumn.triggered.connect(self.on_actionDeleteFilterColumn_triggered_O)
        self.menuValues.addAction(actionDeleteFilterColumn)
        self.menuValues.addSeparator()

        actionTextFilter = QtGui.QAction("Buscar...", self.tableWorkshop_O)
        actionTextFilter.triggered.connect(self.on_actionTextFilter_triggered_O)
        self.menuValues.addAction(actionTextFilter)
        self.menuValues.addSeparator()

        scroll_menu = QtWidgets.QScrollArea()
        scroll_menu.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget(scroll_menu)
        scroll_menu.setWidget(scroll_widget)
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

        checkbox_all_widget = QtWidgets.QCheckBox('Seleccionar todo')

        if not self.checkbox_states_O[self.logicalIndex]['Seleccionar todo'] == True:
            checkbox_all_widget.setChecked(False)
        else:
            checkbox_all_widget.setChecked(True)
        
        checkbox_all_widget.toggled.connect(lambda checked, name='Seleccionar todo': self.on_select_all_toggled_O(checked, name))

        scroll_layout.addWidget(checkbox_all_widget)
        self.action_checkbox_map_O['Seleccionar todo'] = checkbox_all_widget

        if len(self.dict_ordersort_O) != 0 and self.logicalIndex in self.dict_ordersort_O:
            list_uniquevalues = sorted(list(set(self.dict_valuesuniques_O[self.logicalIndex])))
        else:
            list_uniquevalues = sorted(list(set(valuesUnique_view)))

        for actionName in list_uniquevalues:
            checkbox_widget = QtWidgets.QCheckBox(str(actionName))

            if self.logicalIndex not in self.checkbox_filters_O:
                checkbox_widget.setChecked(True)
            elif actionName not in self.checkbox_filters_O[self.logicalIndex]:
                checkbox_widget.setChecked(False)
            else:
                checkbox_widget.setChecked(True)

            checkbox_widget.toggled.connect(lambda checked, name=actionName: self.on_checkbox_toggled_O(checked, name))

            scroll_layout.addWidget(checkbox_widget)
            self.action_checkbox_map_O[actionName] = checkbox_widget

        action_scroll_menu = QtWidgets.QWidgetAction(self.menuValues)
        action_scroll_menu.setDefaultWidget(scroll_menu)
        self.menuValues.addAction(action_scroll_menu)

        self.menuValues.addSeparator()

        accept_button = QtGui.QAction("ACEPTAR", self.tableWorkshop_O)
        accept_button.triggered.connect(self.menu_acceptbutton_triggered_O)

        cancel_button = QtGui.QAction("CANCELAR", self.tableWorkshop_O)
        cancel_button.triggered.connect(self.menu_cancelbutton_triggered)

        self.menuValues.addAction(accept_button)
        self.menuValues.addAction(cancel_button)

        self.menuValues.setStyleSheet("QMenu::item:selected { background-color: #33bdef; }"
                                        "QMenu::item:pressed { background-color: rgb(1, 140, 190); }")

        headerPos = self.tableWorkshop_O.mapToGlobal(self.tableWorkshop_O.horizontalHeader().pos())        

        posY = headerPos.y() + self.tableWorkshop_O.horizontalHeader().height()
        scrollX = self.tableWorkshop_O.horizontalScrollBar().value()
        xInView = self.tableWorkshop_O.horizontalHeader().sectionViewportPosition(logicalIndex)
        posX = headerPos.x() + xInView - scrollX

        self.menuValues.exec(QtCore.QPoint(posX, posY))

# Function when accept button of menu is clicked
    def menu_acceptbutton_triggered_O(self):
        """
        Applies the selected filters and updates the table model with the new filters.
        """
        for column, filters in self.checkbox_filters_O.items():
            if filters:
                self.proxy_O.setFilter(filters, column)
            else:
                self.proxy_O.setFilter(None, column)

# Function when select all checkbox is clicked
    def on_select_all_toggled_O(self, checked, action_name):
        """
        Toggles the state of all checkboxes in the filter menu when the 'Select All' checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the 'Select All' checkbox.
            action_name (str): The name of the action (usually 'Select All').
        """
        filterColumn = self.logicalIndex
        imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
        icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))

        if checked:
            for checkbox_name, checkbox_widget in self.action_checkbox_map_PA.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states_PA[self.logicalIndex][checkbox_name] = checked

            if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map_PA.values()):
                self.model_PA.setIconColumnHeader(filterColumn, icono)
            else:
                self.model_PA.setIconColumnHeader(filterColumn, '')
        
        else:
            for checkbox_name, checkbox_widget in self.action_checkbox_map_PA.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states_PA[self.logicalIndex][checkbox_widget.text()] = checked

# Function when checkbox of header menu is clicked
    def on_checkbox_toggled_O(self, checked, action_name):
        """
        Updates the filter state when an individual checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the checkbox.
            action_name (str): The name of the checkbox.
        """
        filterColumn = self.logicalIndex
        imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
        icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))

        if checked:
            if filterColumn not in self.checkbox_filters_O:
                self.checkbox_filters_O[filterColumn] = [action_name]
            else:
                if action_name not in self.checkbox_filters_O[filterColumn]:
                    self.checkbox_filters_O[filterColumn].append(action_name)
        else:
            if filterColumn in self.checkbox_filters_O and action_name in self.checkbox_filters_O[filterColumn]:
                self.checkbox_filters_O[filterColumn].remove(action_name)

        if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map_O.values()):
            self.model_O.setIconColumnHeader(filterColumn, '')
        else:
            self.model_O.setIconColumnHeader(filterColumn, icono)

# Function to delete individual column filter
    def on_actionDeleteFilterColumn_triggered_O(self):
        """
        Removes the filter from the selected column and updates the table model.
        """
        filterColumn = self.logicalIndex
        if filterColumn in self.proxy_O.filters:
            del self.proxy_O.filters[filterColumn]
        self.model_O.setIconColumnHeader(filterColumn, '')
        self.proxy_O.invalidateFilter()

        # self.tableWorkshop.setModel(None)
        self.tableWorkshop_O.setModel(self.proxy_O)

        if filterColumn in self.checkbox_filters_O:
            del self.checkbox_filters_O[filterColumn]

        self.checkbox_states_O[self.logicalIndex].clear()
        self.checkbox_states_O[self.logicalIndex]['Seleccionar todo'] = True
        for row in range(self.tableWorkshop_O.model().rowCount()):
            value = self.model_O.record(row).value(filterColumn)
            if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
            self.checkbox_states_O[self.logicalIndex][str(value)] = True

# Function to order column ascending
    def on_actionSortAscending_triggered_O(self):
        """
        Sorts the selected column in ascending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.AscendingOrder
        self.tableWorkshop_O.sortByColumn(sortColumn, sortOrder)

# Function to order column descending
    def on_actionSortDescending_triggered_O(self):
        """
        Sorts the selected column in descending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.DescendingOrder
        self.tableWorkshop_O.sortByColumn(sortColumn, sortOrder)

# Function when text is searched
    def on_actionTextFilter_triggered_O(self):
        """
        Opens a dialog to enter a text filter and applies it to the selected column.
        """
        filterColumn = self.logicalIndex
        dlg = QtWidgets.QInputDialog()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle('Buscar')
        clickedButton=dlg.exec()

        if clickedButton == 1:
            stringAction = dlg.textValue()
            if re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', stringAction):
                stringAction=QtCore.QDate.fromString(stringAction,"dd/MM/yyyy")
                stringAction=stringAction.toString("yyyy-MM-dd")

            filterString = QtCore.QRegularExpression(stringAction, QtCore.QRegularExpression.PatternOption(0))
            # del self.proxy.filters[filterColumn]
            self.proxy_PA.setFilter([stringAction], filterColumn)

            imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
            icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))
            self.model_PA.setIconColumnHeader(filterColumn, icono)

# Function to export data to excel
    def exporttoexcel(self):
        """
        Exports the visible data from the table to an Excel file. If no data is loaded, displays a warning message.

        Shows a message box if there is no data to export and allows the user to save the data to an Excel file.
        """

        final_data1 = []
        final_data2 = []
        final_data3 = []

        visible_columns = [col for col in range(self.model_P.columnCount()) if not self.tableWorkshop_P.isColumnHidden(col)]
        visible_headers = self.model_P.getColumnHeaders(visible_columns)
        for row in range(self.proxy_P.rowCount()):
            tag_data = []
            for column in visible_columns:
                value = self.proxy_P.data(self.proxy_P.index(row, column))
                if isinstance(value, QDate):
                    value = value.toString("dd/MM/yyyy")
                elif column in [11,21]:
                    value = int(value) if value != '' else 0
                tag_data.append(value)
            final_data1.append(tag_data)

        final_data1.insert(0, visible_headers)
        df_P = pd.DataFrame(final_data1)
        df_P.columns = df_P.iloc[0]
        df_P = df_P[1:]

        visible_columns = [col for col in range(self.model_O.columnCount()) if not self.tableWorkshop_O.isColumnHidden(col)]
        visible_headers = self.model_O.getColumnHeaders(visible_columns)
        for row in range(self.proxy_O.rowCount()):
            tag_data = []
            for column in visible_columns:
                value = self.proxy_O.data(self.proxy_O.index(row, column))
                if isinstance(value, QDate):
                    value = value.toString("dd/MM/yyyy")
                elif column in [16,21]:
                    value = int(value) if value != '' else 0
                tag_data.append(value)
            final_data2.append(tag_data)

        final_data2.insert(0, visible_headers)
        df_O = pd.DataFrame(final_data2)
        df_O.columns = df_O.iloc[0]
        df_O = df_O[1:]

        output_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Guardar Excel", "", "Archivos de Excel (*.xlsx)")
        if output_path:
            if not output_path.lower().endswith(".xlsx"):
                output_path += ".xlsx"
            df_P.to_excel(output_path, index=False, header=True)
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                df_P.to_excel(writer, sheet_name='P-', index=False)
                df_O.to_excel(writer, sheet_name='PA-', index=False)

# Function to count selected cell and sum its values if possible
    def countSelectedCells_P(self):
        """
        Counts the number of selected cells and sums their values. Updates the UI labels with the count and sum.
        """
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        indexes = self.tableWorkshop_P.selectedIndexes()

        # Reset labels
        self.label_SumItems_P.setText("")
        self.label_SumValue_P.setText("")
        self.label_CountItems_P.setText("")
        self.label_CountValue_P.setText("")


        if len(indexes) < 1:
            return

        count_non_empty = 0
        sum_values = 0

        for ix in indexes:
            value = ix.data()

            if value not in [None, '', 0]:
                count_non_empty += 1

                try:
                    sum_values += int(value)
                except (ValueError, TypeError):
                    pass

        if sum_values:
            self.label_SumItems_P.setText("Suma:")
            self.label_SumValue_P.setText(sum_values)

        if count_non_empty > 0:
            self.label_CountItems_P.setText("Recuento:")
            self.label_CountValue_P.setText(str(count_non_empty))

# Function to count selected cell and sum its values if possible
    def countSelectedCells_O(self):
        """
        Counts the number of selected cells and sums their values. Updates the UI labels with the count and sum.
        """
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        indexes = self.tableWorkshop_O.selectedIndexes()

        # Reset labels
        self.label_SumItems_O.setText("")
        self.label_SumValue_O.setText("")
        self.label_CountItems_O.setText("")
        self.label_CountValue_O.setText("")


        if len(indexes) < 1:
            return

        count_non_empty = 0
        sum_values = 0

        for ix in indexes:
            value = ix.data()

            if value not in [None, '', 0]:
                count_non_empty += 1

                try:
                    sum_values += int(value)
                except (ValueError, TypeError):
                    pass

        if sum_values:
            self.label_SumItems_O.setText("Suma:")
            self.label_SumValue_O.setText(sum_values)

        if count_non_empty > 0:
            self.label_CountItems_O.setText("Recuento:")
            self.label_CountValue_O.setText(str(count_non_empty))






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dbparam = config()
    user_database = dbparam["user"]
    password_database = dbparam["password"]

    # Genera un nombre único para la conexión basado en el nombre de usuario y el contador
    db_manufacture = Create_DBconnection(user_database, password_database, 'workshop_connection_test')

    if not db_manufacture:
        sys.exit()

    Workshop_Hours_Window = Ui_Workshop_Hours_Window(db_manufacture, 'j.zofio')
    Workshop_Hours_Window.show()
    sys.exit(app.exec())