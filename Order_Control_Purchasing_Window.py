from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtSql
from PyQt6.QtCore import Qt
from datetime import *
from config import get_path, config
import re
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QMimeData, QDate
from PyQt6.QtGui import QKeySequence
import sys
import pandas as pd
from tkinter.filedialog import asksaveasfilename
from PDF_Styles import CustomPDF_A3
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from io import BytesIO
import numpy as np
from Excel_Export_Templates import order_reports
from utils.Database_Manager import Database_Connection, Create_DBconnection
from utils.Show_Message import MessageHelper


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

class ColorDelegate(QtWidgets.QItemDelegate):
    """
    A custom item delegate for applying background colors to cells in a QTableView or QTableWidget.

    Inherits from:
        QtWidgets.QItemDelegate: Provides custom rendering for table items.
    """
    def __init__(self, parent=None):
        """
        Initializes the ColorDelegate, setting up the color mapping from the database.

        Args:
            parent (QtWidgets.QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)

    def paint(self, painter, option, index: QtCore.QModelIndex):
        """
        Paints the background color of the item based on its column and value.

        Args:
            painter (QtGui.QPainter): The painter used for painting.
            option (QtWidgets.QStyleOptionViewItem): The style option for the item.
            index (QtCore.QModelIndex): The model index of the item.
        """
        value = index.model().data(index, role=Qt.ItemDataRole.DisplayRole)
        background_color = QtGui.QColor(255, 255, 255)

        if index.column() == 35:
            if isinstance(value, (date, datetime)):
                if value <= QtCore.QDate.currentDate():
                    background_color = QtGui.QColor(255, 0, 0) #Red

        painter.fillRect(option.rect, background_color)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter

        super().paint(painter, option, index)

class CustomProxyModel(QtCore.QSortFilterProxyModel):
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

class EditableTableModel(QtSql.QSqlTableModel):
    """
    A custom SQL table model that supports editable columns, headers, and special flagging behavior based on user permissions.

    Signals:
        updateFailed (str): Signal emitted when an update to the model fails.
    """
    updateFailed = QtCore.pyqtSignal(str)

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
        if index.column() in [0,4,14,25]:
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

class Ui_Purchasing_Order_Control_Window(QtWidgets.QMainWindow):
    """
    A main window for managing Assembly-related data, including models and proxies for tables.

    Inherits from:
        QtWidgets.QMainWindow: A top-level window that provides a main application window.
    
    Attributes:
        model (EditableTableModel): The model for table.
        proxy (CustomProxyModel): The proxy model for table.
        checkbox_states (dict): A dictionary tracking checkbox states for table.
        dict_valuesuniques (dict): A dictionary of unique values for table.
        dict_ordersort (dict): A dictionary for sorting orders in table.
        action_checkbox_map (dict): A mapping of actions to checkboxes for table.
        checkbox_filters (dict): A dictionary of filters applied to checkboxes for table.
        db (object): The database connection object.
        username (str): The username of the currently logged-in user.
    """
    def __init__(self, db, username):
        """
        Initializes the Ui_Purchasing_Order_Control_Window, setting up models, proxies, and internal state.

        Args:
            db (object): The database connection object.
            username (str): The username of the currently logged-in user.
        """
        super().__init__()
        self.model = EditableTableModel(database=db)
        self.proxy = CustomProxyModel()
        self.checkbox_states = {}
        self.dict_valuesuniques = {}
        self.dict_ordersort = {}
        self.action_checkbox_map = {}
        self.checkbox_filters = {}
        self.db = db
        self.username = username
        self.open_windows = {}
        self.model.dataChanged.connect(self.saveChanges)
        self.setupUi(self)

    def closeEvent(self, event):
        """
        Handles the close event to clean up resources.

        Args:
            event (QtGui.QCloseEvent): The close event.
        """
        try:
            if self.model:
                self.model.clear()
            self.closeConnection()
        except Exception as e:
            print("Error during close event:", e)

    def closeConnection(self):
        """
        Closes the database connection and cleans up resources.
        """
        try:
            self.tableOrders.setModel(None)
            del self.model
            if self.db:
                self.db.close()
                del self.db
                if QtSql.QSqlDatabase.contains("order_control_purchasing_connection"):
                    QtSql.QSqlDatabase.removeDatabase("order_control_purchasing_connection")
        except Exception as e:
            print("Error closing connection:", e)


    def setupUi(self, Purchasing_Order_Control_Window):
        """
        Sets up the user interface components for the main application window.

        Args:
            Purchasing_Order_Control_Window (QtWidgets.QMainWindow): The main window object to set up.
        """
        self.id_list = []
        data_list = []
        Purchasing_Order_Control_Window.setObjectName("Purchasing_Order_Control_Window")
        Purchasing_Order_Control_Window.resize(400, 561)
        Purchasing_Order_Control_Window.setMinimumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Purchasing_Order_Control_Window.setWindowIcon(icon)
        Purchasing_Order_Control_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=Purchasing_Order_Control_Window)
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
        self.hcabspacer=QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hcab.addItem(self.hcabspacer)
        self.toolExpReport = QtWidgets.QToolButton(self.frame)
        self.toolExpReport.setObjectName("ExpReport_Button")
        self.toolExpReport.setToolTip("Generar Informe")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "Reports.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolExpReport.setIcon(icon)
        self.toolExpReport.setIconSize(QtCore.QSize(25, 25))
        self.hcab.addWidget(self.toolExpReport)
        self.hcabspacer=QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hcab.addItem(self.hcabspacer)
        self.gridLayout_2.addLayout(self.hcab, 0, 0, 1, 1)
        self.tabwidget = QtWidgets.QTabWidget(self.frame)
        self.tabwidget.setObjectName("tabwidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabwidget.addTab(self.tab, "P-")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setObjectName("hLayout")
        self.Button_All = QtWidgets.QPushButton(parent=self.frame)
        self.Button_All.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_All.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_All.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_All.setObjectName("Button_All")
        self.hLayout.addWidget(self.Button_All)
        self.gridLayout_3.addLayout(self.hLayout, 1, 0, 1, 1)
        self.tableOrders=QtWidgets.QTableView(parent=self.frame)
        self.model = EditableTableModel(database=self.db)
        self.tableOrders.setObjectName("tableOrders")
        self.gridLayout_3.addWidget(self.tableOrders, 2, 0, 1, 1)

        self.gridLayout_2.addWidget(self.tabwidget, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        Purchasing_Order_Control_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Purchasing_Order_Control_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        Purchasing_Order_Control_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Purchasing_Order_Control_Window)
        self.statusbar.setObjectName("statusbar")
        Purchasing_Order_Control_Window.setStatusBar(self.statusbar)
        self.tableOrders.setSortingEnabled(True)
        self.tableOrders.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")

        self.retranslateUi(Purchasing_Order_Control_Window)
        QtCore.QMetaObject.connectSlotsByName(Purchasing_Order_Control_Window)

        self.query_data()
        self.toolExpExcel.clicked.connect(self.exporttoexcel)
        self.toolExpReport.clicked.connect(self.generate_report)


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, Purchasing_Order_Control_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        Purchasing_Order_Control_Window.setWindowTitle(_translate("Purchasing_Order_Control_Window", "Control Pedidos"))
        self.Button_All.setText(_translate("Purchasing_Order_Control_Window", "Ver Todos"))

# Function to load orders on tables
    def query_data(self):
        """
        Queries the database for orders not delivered, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model.setTable("public.orders")
        self.model.setFilter("num_order NOT LIKE '%R%' AND (porc_deliveries <> 100 OR porc_deliveries IS NULL)")
        self.model.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model.select()
        self.proxy.setSourceModel(self.model)
        self.tableOrders.setModel(self.proxy)

    # Getting the unique values for each column of the model
        for column in range(self.model.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states:
                self.checkbox_states[column] = {}
                self.checkbox_states[column]['Seleccionar todo'] = True
                for row in range(self.model.rowCount()):
                    value = self.model.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states[column][str(value)] = True
                self.dict_valuesuniques[column] = list_valuesUnique

        self.tableOrders.hideColumn(1)
        for i in range(3,6):
            self.tableOrders.hideColumn(i)
        for i in range(7,37):
            self.tableOrders.hideColumn(i)
        for i in range(38,self.model.columnCount()):
            self.tableOrders.hideColumn(i)

        headers=['Nº Pedido', '','Nº Ref','','','','Importe','','','','','','','','F. Prev. Taller','',
                '% Montaje','Cambios %','F. Rec.','F. Prev. Montaje','Observaciones', 'Fecha Aviso',
                '', 'Fecha Envío', '', '','OK', '', '', '', '', '','','Extras', 'Aval', 'Estado Aval', 'Fecha Vto. Aval', 'Material Disponible']

        self.tableOrders.setItemDelegate(AlignDelegate(self.tableOrders))
        self.color_delegate = ColorDelegate(self)
        self.tableOrders.setItemDelegateForColumn(4, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(14, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(16, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(19, self.color_delegate)
        # self.tableOrders.setItemDelegateForColumn(35, self.color_delegate)
        self.tableOrders.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setSectionResizeMode(37, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setDefaultSectionSize(80)
        self.tableOrders.horizontalHeader().resizeSection(16, 60)
        self.tableOrders.horizontalHeader().resizeSection(20, 700)
        self.tableOrders.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_3.addWidget(self.tableOrders, 3, 0, 1, 1)

        self.model.setAllColumnHeaders(headers)

        self.Button_All.clicked.connect(self.query_all)
        self.tableOrders.setSortingEnabled(False)
        self.tableOrders.horizontalHeader().sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked)
        self.model.dataChanged.connect(self.saveChanges)

        self.tableOrders.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableOrders, self.model, self.proxy)

# Function to load all orders
    def query_all(self):
        """
        Queries the database for all orders P-, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model.dataChanged.disconnect(self.saveChanges)
        self.delete_allFilters()
        self.model.setTable("public.orders")
        self.model.setFilter("num_order NOT LIKE '%R%'")
        self.model.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model.select()
        self.proxy.setSourceModel(self.model)
        self.tableOrders.setModel(self.proxy)

        # Getting the unique values for each column of the model
        for column in range(self.model.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states:
                self.checkbox_states[column] = {}
                self.checkbox_states[column]['Seleccionar todo'] = True
                for row in range(self.model.rowCount()):
                    value = self.model.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states[column][str(value)] = True
                self.dict_valuesuniques[column] = list_valuesUnique

        self.tableOrders.hideColumn(1)
        for i in range(3,6):
            self.tableOrders.hideColumn(i)
        for i in range(7,37):
            self.tableOrders.hideColumn(i)
        for i in range(38,self.model.columnCount()):
            self.tableOrders.hideColumn(i)

        headers=['Nº Pedido', '','Nº Ref','','','','Importe','','','','','','','','F. Prev. Taller','',
                '% Montaje','Cambios %','F. Rec.','F. Prev. Montaje','Observaciones', 'Fecha Aviso',
                '', 'Fecha Envío', '', '','OK', '', '', '', '', '','','Extras', 'Aval', 'Estado Aval', 'Fecha Vto. Aval', 'Material Disponible']

        self.tableOrders.setItemDelegate(AlignDelegate(self.tableOrders))
        self.color_delegate = ColorDelegate(self)
        self.tableOrders.setItemDelegateForColumn(4, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(14, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(16, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(19, self.color_delegate)
        # self.tableOrders.setItemDelegateForColumn(35, self.color_delegate)
        self.tableOrders.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setSectionResizeMode(37, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.tableOrders.setItemDelegate(AlignDelegate(self.tableOrders))
        self.color_delegate = ColorDelegate(self)
        self.tableOrders.setItemDelegateForColumn(4, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(14, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(16, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(19, self.color_delegate)
        # self.tableOrders.setItemDelegateForColumn(35, self.color_delegate)
        self.tableOrders.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setSectionResizeMode(36, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setDefaultSectionSize(80)
        self.tableOrders.horizontalHeader().resizeSection(16, 60)
        self.tableOrders.horizontalHeader().resizeSection(20, 700)
        self.tableOrders.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_3.addWidget(self.tableOrders, 2, 0, 1, 1)

        self.model.setAllColumnHeaders(headers)
        self.model.dataChanged.connect(self.saveChanges)

        self.tableOrders.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableOrders, self.model, self.proxy)

# Functions to delete all filters when tool button is clicked
    def delete_allFilters(self):
        columns_number=self.model.columnCount()
        for index in range(columns_number):
            if index in self.proxy.filters:
                del self.proxy.filters[index]
            self.model.setIconColumnHeader(index, '')

        self.checkbox_states = {}
        self.dict_valuesuniques = {}
        self.dict_ordersort = {}
        self.checkbox_filters = {}

        self.proxy.invalidateFilter()
        self.tableOrders.setModel(None)
        self.tableOrders.setModel(self.proxy)

        # Getting the unique values for each column of the model
        for column in range(self.model.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states:
                self.checkbox_states[column] = {}
                self.checkbox_states[column]['Seleccionar todo'] = True
                for row in range(self.model.rowCount()):
                    value = self.model.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states[column][value] = True
                self.dict_valuesuniques[column] = list_valuesUnique

# Function to save changes into database
    def saveChanges(self):
        """
        Saves changes made to the data models and updates unique values for each column.
        """
        self.model.submitAll()

        for column in range(self.model.columnCount()):
            list_valuesUnique = []
            for row in range(self.model.rowCount()):
                value = self.model.record(row).value(column)
                if value not in list_valuesUnique:
                    if isinstance(value, QtCore.QDate):
                        value=value.toString("dd/MM/yyyy")
                    list_valuesUnique.append(str(value))
                    if value not in self.checkbox_states[column]:
                        self.checkbox_states[column][value] = True
            self.dict_valuesuniques[column] = list_valuesUnique

# Function when header of each table is clicked
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):
        """
        Displays a menu when a column header is clicked. The menu includes options for sorting, filtering, and managing column visibility.
        
        Args:
            logicalIndex (int): Index of the clicked column.
        """
        self.logicalIndex = logicalIndex
        self.menuValues = QtWidgets.QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(self.tableOrders)

        valuesUnique_view = []
        for row in range(self.tableOrders.model().rowCount()):
            index = self.tableOrders.model().index(row, self.logicalIndex)
            value = index.data(Qt.ItemDataRole.DisplayRole)
            if value not in valuesUnique_view:
                if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
                valuesUnique_view.append(value)

        actionSortAscending = QtGui.QAction("Ordenar Ascendente", self.tableOrders)
        actionSortAscending.triggered.connect(self.on_actionSortAscending_triggered)
        self.menuValues.addAction(actionSortAscending)
        actionSortDescending = QtGui.QAction("Ordenar Descendente", self.tableOrders)
        actionSortDescending.triggered.connect(self.on_actionSortDescending_triggered)
        self.menuValues.addAction(actionSortDescending)
        self.menuValues.addSeparator()

        actionDeleteFilterColumn = QtGui.QAction("Quitar Filtro", self.tableOrders)
        actionDeleteFilterColumn.triggered.connect(self.on_actionDeleteFilterColumn_triggered)
        self.menuValues.addAction(actionDeleteFilterColumn)
        self.menuValues.addSeparator()

        actionTextFilter = QtGui.QAction("Buscar...", self.tableOrders)
        actionTextFilter.triggered.connect(self.on_actionTextFilter_triggered)
        self.menuValues.addAction(actionTextFilter)
        self.menuValues.addSeparator()

        self.menuValues.setStyleSheet("QMenu { color: black; }"
                                        "QMenu { background-color: rgb(255, 255, 255); }"
                                        "QMenu::item:selected { background-color: #33bdef; }"
                                        "QMenu::item:pressed { background-color: rgb(1, 140, 190); }")

        headerPos = self.tableOrders.mapToGlobal(self.tableOrders.horizontalHeader().pos())        

        posY = headerPos.y() + self.tableOrders.horizontalHeader().height()
        scrollX = self.tableOrders.horizontalScrollBar().value()
        xInView = self.tableOrders.horizontalHeader().sectionViewportPosition(logicalIndex)
        posX = headerPos.x() + xInView - scrollX

        self.menuValues.exec(QtCore.QPoint(posX, posY))

# Function when cancel button of menu is clicked
    def menu_cancelbutton_triggered(self):
        """
        Hides the menu when the cancel button is clicked.
        """
        self.menuValues.hide()

# Function when accept button of menu is clicked for each table
    def menu_acceptbutton_triggered_P(self):
        """
        Applies the selected filters and updates the table model with the new filters.
        """
        for column, filters in self.checkbox_filters.items():
            if filters:
                self.proxy.setFilter(filters, column)
            else:
                self.proxy.setFilter(None, column)

# Function when select all checkbox is clicked for each table
    def on_select_all_toggled(self, checked, action_name):
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
            for checkbox_name, checkbox_widget in self.action_checkbox_map.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states[self.logicalIndex][checkbox_name] = checked

            if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map.values()):
                self.model.setIconColumnHeader(filterColumn, icono)
            else:
                self.model.setIconColumnHeader(filterColumn, '')
        
        else:
            for checkbox_name, checkbox_widget in self.action_checkbox_map.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states[self.logicalIndex][checkbox_widget.text()] = checked

# Function when checkbox of header menu is clicked for each table
    def on_checkbox_toggled(self, checked, action_name):
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
            if filterColumn not in self.checkbox_filters:
                self.checkbox_filters[filterColumn] = [action_name]
            else:
                if action_name not in self.checkbox_filters[filterColumn]:
                    self.checkbox_filters[filterColumn].append(action_name)
        else:
            if filterColumn in self.checkbox_filters and action_name in self.checkbox_filters[filterColumn]:
                self.checkbox_filters[filterColumn].remove(action_name)

        if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map.values()):
            self.model.setIconColumnHeader(filterColumn, '')
        else:
            self.model.setIconColumnHeader(filterColumn, icono)

# Function to delete individual column filter for each table
    def on_actionDeleteFilterColumn_triggered(self):
        """
        Removes the filter from the selected column and updates the table model.
        """
        filterColumn = self.logicalIndex
        if filterColumn in self.proxy.filters:
            del self.proxy.filters[filterColumn]
        self.model.setIconColumnHeader(filterColumn, '')
        self.proxy.invalidateFilter()

        # self.tableOrders.setModel(None)
        self.tableOrders.setModel(self.proxy)

        if filterColumn in self.checkbox_filters:
            del self.checkbox_filters[filterColumn]

        self.checkbox_states[self.logicalIndex].clear()
        self.checkbox_states[self.logicalIndex]['Seleccionar todo'] = True
        for row in range(self.tableOrders.model().rowCount()):
            value = self.model.record(row).value(filterColumn)
            if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
            self.checkbox_states[self.logicalIndex][str(value)] = True

# Function to order column ascending for each table
    def on_actionSortAscending_triggered(self):
        """
        Sorts the selected column in ascending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.AscendingOrder
        self.tableOrders.sortByColumn(sortColumn, sortOrder)

# Function to order column descending for each table
    def on_actionSortDescending_triggered(self):
        """
        Sorts the selected column in descending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.DescendingOrder
        self.tableOrders.sortByColumn(sortColumn, sortOrder)

# Function when text is searched for each table
    def on_actionTextFilter_triggered(self):
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
        if event.key() == QtCore.Qt.Key.Key_Delete: # Event when delete key is pressed
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

        elif event.modifiers() and QtCore.Qt.KeyboardModifier.ControlModifier: # Event when ctrl + comma is pressed
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

        elif event.matches(QKeySequence.StandardKey.Copy): # Event for copy (ctrl + c)
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

        elif event.matches(QKeySequence.StandardKey.Paste): # Event for paste (ctrl + v)
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

        elif event.matches(QKeySequence.StandardKey.MoveToNextLine): # Event for down cursor pressed
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
                    table.selectionModel().setCurrentIndex(model.index(new_row, current_column), QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect)

        elif event.matches(QKeySequence.StandardKey.MoveToPreviousLine): # Event for up cursor pressed
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
                    table.selectionModel().setCurrentIndex(model.index(new_row, current_column), QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect)

        elif event.matches(QKeySequence.StandardKey.MoveToNextChar): # Event for right cursor pressed
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
                    table.selectionModel().setCurrentIndex(model.index(current_row, new_column), QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect)

        elif event.matches(QKeySequence.StandardKey.MoveToPreviousChar): # Event for left cursor pressed
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
                    table.selectionModel().setCurrentIndex(model.index(current_row, new_column), QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect)

        elif event.matches(QKeySequence.StandardKey.InsertParagraphSeparator): # Event for enter pressed
            current_index = table.selectionModel().selectedIndexes()[0]

            if current_index.isValid():
                table.edit(current_index)

        super().keyPressEvent(event)

# Function to export data to excel
    def exporttoexcel(self):
        """
        Exports the visible data from the table to an Excel file. If no data is loaded, displays a warning message.

        Shows a message box if there is no data to export and allows the user to save the data to an Excel file.
        """

        final_data1 = []

        visible_columns = [col for col in range(self.model.columnCount()) if not self.tableOrders.isColumnHidden(col)]
        visible_headers = self.model.getColumnHeaders(visible_columns)
        for row in range(self.proxy.rowCount()):
            tag_data = []
            for column in visible_columns:
                value = self.proxy.data(self.proxy.index(row, column))
                if isinstance(value, QDate):
                    value = value.toString("dd/MM/yyyy")
                elif column in [11,21]:
                    value = int(value) if value != '' else 0
                tag_data.append(value)
            final_data1.append(tag_data)

        final_data1.insert(0, visible_headers)
        df = pd.DataFrame(final_data1)
        df.columns = df.iloc[0]
        df = df[1:]

        output_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")], title="Guardar archivo de Excel")
        if output_path:
            df.to_excel(output_path, index=False, header=True)
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='P-', index=False)

# Function to generate reports
    def generate_report(self):
        """
        Generates a report based on chosen selection
        """
        while True:
            report, ok = QtWidgets.QInputDialog.getItem(None, "Informes", "Selecciona un informe:", ['Ofertas', 'Pedidos'], 0, False)
            if ok and report:
                while True:
                    if report == 'Ofertas':
                        self.report_offers()
                        break
                    elif report == 'Pedidos':
                        self.report_orders()
                        break
                break
            else:
                break


    def report_offers(self):
        start_date, end_date = self.get_date_range()

        if start_date and end_date:
            query_graph_commercial_1 = ("""
                            SELECT offers.num_offer, offers.state, offers.responsible,
                            COALESCE(offers.offer_amount, 0::money) AS offer_amount, COALESCE(orders.order_amount, 0::money) AS order_amount, orders.num_order
                            FROM offers
                            LEFT JOIN orders ON offers.num_offer = orders.num_offer
                            WHERE EXTRACT(YEAR FROM offers.register_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                            """)

            query_graph_commercial_2 = ("""
                                SELECT num_offer, state, responsible, 'offers' AS source_table
                                FROM offers
                                WHERE EXTRACT(YEAR FROM offers.register_date) = EXTRACT(YEAR FROM CURRENT_DATE)

                                UNION ALL

                                SELECT id_offer, state, responsible, 'received_offers' AS source_table
                                FROM received_offers
                                WHERE EXTRACT(YEAR FROM received_offers.register_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                                """)

            query_graph_calculation_1 = ("""
                            SELECT offers.num_offer, offers.state, offers.responsible_calculations,
                            COALESCE(offers.offer_amount, 0::money) AS offer_amount, COALESCE(orders.order_amount, 0::money) AS order_amount
                            FROM offers
                            LEFT JOIN orders ON offers.num_offer = orders.num_offer
                            WHERE EXTRACT(YEAR FROM offers.register_date) = EXTRACT(YEAR FROM CURRENT_DATE) AND (offers.responsible_calculations NOT IN ('N/A', '') AND offers.responsible_calculations IS NOT NULL)
                            """)

            query_graph_calculation_2 = ("""
                                SELECT num_offer, state, responsible_calculations, 'offers' AS source_table
                                FROM offers
                                WHERE EXTRACT(YEAR FROM offers.register_date) = EXTRACT(YEAR FROM CURRENT_DATE) AND (offers.responsible_calculations NOT IN ('N/A', '') AND offers.responsible_calculations IS NOT NULL)
                                """)

            query_last_weekly_summary = ("""
                                SELECT num_offer, state, responsible, responsible_calculations, client, final_client,
                                recep_date, presentation_date, limit_date,
                                probability, priority, material, items_number, offer_amount, actions, source_table
                                FROM (
                                SELECT num_offer, state, responsible, responsible_calculations, client, final_client,
                                TO_CHAR(recep_date, 'DD/MM/YYYY') as recep_date, TO_CHAR(presentation_date, 'DD/MM/YYYY') as presentation_date, TO_CHAR(limit_date, 'DD/MM/YYYY') as limit_date,
                                probability, '' as priority, material, items_number, offer_amount, actions, 'offers' AS source_table
                                FROM offers
                                WHERE register_date >= %s AND register_date <= %s

                                UNION ALL

                                SELECT id_offer as num_offer, state, responsible, '' as responsible_calculations, client, final_client,
                                TO_CHAR(recep_date, 'DD/MM/YYYY') as recep_date, '' as presentation_date, TO_CHAR(limit_date, 'DD/MM/YYYY') as limit_date,
                                '' as probability, '' as priority, material, items_number, '' as offer_amount, '' as actions, 'received_offers' AS source_table
                                FROM received_offers
                                WHERE register_date >= %s AND register_date <= %s) as final_table

                                ORDER BY array_position(
                                ARRAY['No Ofertada', 'Declinada', 'Perdida', 'Recibida', 'Registrada', 'En Estudio', 'Presentada', 'Adjudicada'], state), num_offer
                                """)

            query_active_summary = ("""
                                SELECT * FROM (
                                SELECT num_offer, state, responsible, responsible_calculations, client, final_client,
                                TO_CHAR(recep_date, 'DD/MM/YYYY'), TO_CHAR(presentation_date, 'DD/MM/YYYY'), TO_CHAR(limit_date, 'DD/MM/YYYY'),
                                probability, '' as priority, material, items_number, offer_amount, actions
                                FROM offers
                                WHERE state IN ('Registrada', 'En Estudio', 'Presentada')

                                UNION ALL

                                SELECT id_offer as num_offer, state, responsible, '' as responsible_calculations, client, final_client,
                                TO_CHAR(recep_date, 'DD/MM/YYYY'), '' as presentation_date, TO_CHAR(limit_date, 'DD/MM/YYYY'),
                                '' as probability, '' as priority, material, items_number, '' as offer_amount, '' as actions
                                FROM received_offers
                                WHERE state IN ('Registrada')) as final_table

                                ORDER BY state
                                """)

            with Database_Connection(config()) as conn:
                with conn.cursor() as cur:

                    cur.execute(query_graph_commercial_1)
                    results_graph_commercial_1 = cur.fetchall()
                    df_graph_commercial_1 = pd.DataFrame(results_graph_commercial_1, columns=['Nº Oferta', 'Estado', 'Responsable', 'Importe Oferta', 'Importe Pedido', 'Nº Pedido'])

                    df_graph_commercial_1['Importe Oferta'] = df_graph_commercial_1['Importe Oferta']\
                                                .str.replace('€', '', regex=False) \
                                                .str.replace('.', '', regex=False) \
                                                .str.replace(',', '.', regex=False) \
                                                .astype(float)

                    df_graph_commercial_1['Importe Pedido'] = df_graph_commercial_1['Importe Pedido']\
                                                .str.replace('€', '', regex=False) \
                                                .str.replace('.', '', regex=False) \
                                                .str.replace(',', '.', regex=False) \
                                                .astype(float)

                    df_graph_commercial_1['Importe Final'] = df_graph_commercial_1.apply(lambda row: row['Importe Pedido'] if row['Estado'] == 'Adjudicada' else row['Importe Oferta'], axis=1)

                    cur.execute(query_graph_commercial_2)
                    results_graph_commercial_2 = cur.fetchall()
                    df_graph_commercial_2 = pd.DataFrame(results_graph_commercial_2, columns=['Nº Oferta', 'Estado', 'Responsable', 'Tabla'])

                    cur.execute(query_graph_calculation_1)
                    results_graph_calculation_1 = cur.fetchall()
                    df_graph_calculation_1 = pd.DataFrame(results_graph_calculation_1, columns=['Nº Oferta', 'Estado', 'Responsable', 'Importe Oferta', 'Importe Pedido'])

                    df_graph_calculation_1['Importe Oferta'] = df_graph_calculation_1['Importe Oferta']\
                                                .str.replace('€', '', regex=False) \
                                                .str.replace('.', '', regex=False) \
                                                .str.replace(',', '.', regex=False) \
                                                .astype(float)

                    df_graph_calculation_1['Importe Pedido'] = df_graph_calculation_1['Importe Pedido']\
                                                .str.replace('€', '', regex=False) \
                                                .str.replace('.', '', regex=False) \
                                                .str.replace(',', '.', regex=False) \
                                                .astype(float)

                    df_graph_calculation_1['Importe Final'] = df_graph_calculation_1.apply(lambda row: row['Importe Pedido'] if row['Estado'] == 'Adjudicada' else row['Importe Oferta'], axis=1)

                    cur.execute(query_graph_calculation_2)
                    results_graph_calculation_2 = cur.fetchall()
                    df_graph_calculation_2 = pd.DataFrame(results_graph_calculation_2, columns=['Nº Oferta', 'Estado', 'Responsable', 'Tabla'])

                    df_graph_orders_1 = df_graph_commercial_1.dropna(subset=['Nº Pedido'])

                    cur.execute(query_last_weekly_summary, (start_date, end_date, start_date, end_date))
                    results_weekly = cur.fetchall()
                    df_weekly = pd.DataFrame(results_weekly,
                    columns=['Nº Oferta', 'Estado', 'Responsable', 'Cálculos', 'Cliente', 'Cl. Final',
                    'Fecha Rec.', 'Fecha Pres.', 'Fecha Vto.',
                    'Prob.', 'Prior.', 'Material', 'Nº Eqs.', 'Importe', 'Acciones', 'Tabla']
                    )

                    df_weekly['Importe Euros'] = df_weekly['Importe']\
                                                .str.replace('€', '', regex=False) \
                                                .str.replace('.', '', regex=False) \
                                                .str.replace(',', '.', regex=False) \
                                                .astype(float)

                    cur.execute(query_active_summary)
                    results_active = cur.fetchall()
                    df_active = pd.DataFrame(results_active, columns=['Nº Oferta', 'Estado', 'Responsable', 'Cálculos', 'Cliente', 'Cl. Final',
                    'Fecha Rec.', 'Fecha Pres.', 'Fecha Vto.',
                    'Prob.', 'Prior.', 'Material', 'Nº Eqs.', 'Importe', 'Acciones']
                    )

                    df_active['Importe Euros'] = df_active['Importe']\
                                                .str.replace('€', '', regex=False) \
                                                .str.replace('.', '', regex=False) \
                                                .str.replace(',', '.', regex=False) \
                                                .astype(float)

            pdf = self.generate_report_offers(start_date, end_date, df_graph_commercial_1, df_graph_commercial_2, df_graph_calculation_1, df_graph_calculation_2, df_graph_orders_1, df_weekly, df_active)

            output_path = asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")], title="Guardar PDF")
            if output_path:
                pdf.output(output_path)

    def generate_report_offers(self, start_date, end_date, df_graph_commercial_1, df_graph_commercial_2, df_graph_calculation_1, df_graph_calculation_2, df_graph_orders_1, df_weekly, df_active):
        pdf = CustomPDF_A3('P')

        pdf.add_font('DejaVuSansCondensed', '', str(get_path("Resources", "Iconos", "DejaVuSansCondensed.ttf")))
        pdf.add_font('DejaVuSansCondensed-Bold', '', str(get_path("Resources", "Iconos", "DejaVuSansCondensed-Bold.ttf")))

        pdf.set_auto_page_break(auto=True)
        pdf.set_margins(0.5, 0.5)

        pdf.set_fill_color(3, 174, 236)

        pdf.add_page()

        pdf.image(str(get_path("Resources", "Iconos", "Eipsa Logo Blanco.png")), 1, 0.8, 7, 2)
        pdf.ln(3)

        pdf.set_font('Helvetica', 'B', size=6)
        y_position = 0.5
        pdf.set_xy(12.55, y_position)
        pdf.fixed_height_multicell(3.5, 0.6, 'TOTAL IMPORTE REGISTRADO ' + str(datetime.today().year), fill=True)
        pdf.set_xy(16.05, y_position)
        pdf.cell(0.4, 0.6,'')
        pdf.fixed_height_multicell(4, 0.6, 'TOTAL IMPORTE OFERTADO ' + str(datetime.today().year), fill=True)
        pdf.set_xy(20.45, y_position)
        pdf.cell(0.4, 0.6,'')
        pdf.fixed_height_multicell(4, 0.6, 'TOTAL IMPORTE BUDGETARY ' + str(datetime.today().year), fill=True)
        pdf.set_xy(24.85, y_position)
        pdf.cell(0.4, 0.6, '')
        pdf.fixed_height_multicell(4, 0.6, 'TOTAL IMPORTE ADJUDICADO ' + str(datetime.today().year), fill=True)

        received_amount = df_graph_commercial_1['Importe Oferta'].sum()
        offered_amount = df_graph_commercial_1[df_graph_commercial_1['Estado'] != 'Budgetary']['Importe Oferta'].sum()
        budgetary_amount = df_graph_commercial_1[df_graph_commercial_1['Estado'] == 'Budgetary']['Importe Oferta'].sum()
        order_amount = df_graph_commercial_1[df_graph_commercial_1['Estado'] == 'Adjudicada']['Importe Oferta'].sum()

        pdf.set_font('DejaVuSansCondensed-Bold','', size=6)
        y_position = 1.1
        pdf.set_xy(12.55, y_position)
        pdf.fixed_height_multicell(3.5, 0.3, self.euro_format(received_amount), fill=False)
        pdf.set_xy(16.05, y_position)
        pdf.cell(0.4, 0.6,'')
        pdf.fixed_height_multicell(4, 0.3, self.euro_format(offered_amount) + " / " + f"{(offered_amount/received_amount):.1%}", fill=False)
        pdf.set_xy(20.45, y_position)
        pdf.cell(0.4, 0.3, '')
        pdf.fixed_height_multicell(4, 0.3, self.euro_format(budgetary_amount) + " / " + f"{(budgetary_amount/received_amount):.1%}", fill=False)
        pdf.set_xy(24.85, y_position)
        pdf.cell(0.4, 0.3, '')
        pdf.fixed_height_multicell(4, 0.3, self.euro_format(order_amount) + " / " + f"{(order_amount/offered_amount):.1%}", fill=False)

        pdf.set_font('Helvetica', 'B', size=6)
        y_position = 1.6
        pdf.set_xy(12.55, y_position)
        pdf.fixed_height_multicell(3.5, 0.6, 'TOTAL OFERTAS REGISTRADAS ' + str(datetime.today().year), fill=True)
        pdf.set_xy(16.05, y_position)
        pdf.cell(0.4, 0.6, '')
        pdf.fixed_height_multicell(4, 0.6, 'TOTAL OFERTAS REALIZADAS ' + str(datetime.today().year), fill=True)
        pdf.set_xy(20.45, y_position)
        pdf.cell(0.4, 0.6, '')
        pdf.fixed_height_multicell(4, 0.6, 'TOTAL BUDGETARIES\n' + str(datetime.today().year), fill=True)
        pdf.set_xy(24.85, y_position)
        pdf.cell(0.4, 0.6, '')
        pdf.fixed_height_multicell(4, 0.6, 'TOTAL OFERTAS ADJUDICADAS ' + str(datetime.today().year), fill=True)
        pdf.set_xy(26.4, y_position)

        received_count = df_graph_commercial_2.shape[0]
        offered_count = df_graph_commercial_2[df_graph_commercial_2['Estado'] != 'Budgetary'].shape[0]
        budgetary_count = df_graph_commercial_2[df_graph_commercial_2['Estado'] == 'Budgetary'].shape[0]
        order_count = df_graph_commercial_2[df_graph_commercial_2['Estado'] == 'Adjudicada'].shape[0]
        
        pdf.set_font('DejaVuSansCondensed-Bold','', size=6)
        y_position = 2.2
        pdf.set_xy(12.55, y_position)
        pdf.fixed_height_multicell(3.5, 0.3, str(received_count), fill=False)
        pdf.set_xy(16.05, y_position)
        pdf.cell(0.4, 0.3, '')
        pdf.fixed_height_multicell(4, 0.3, str(offered_count) + " / " + f"{(offered_count/received_count):.1%}", fill=False)
        pdf.set_xy(20.45, y_position)
        pdf.cell(0.4, 0.3, '')
        pdf.fixed_height_multicell(4, 0.3, str(budgetary_count) + " / " + f"{(budgetary_count/received_count):.1%}", fill=False)
        pdf.set_xy(24.85, y_position)
        pdf.cell(0.4, 0.3, '')
        pdf.fixed_height_multicell(4, 0.3, str(order_count) + " / " + f"{(order_count/offered_count):.1%}", fill=False)

        df_graph_commercial_1 = df_graph_commercial_1[df_graph_commercial_1['Estado'] != 'Budgetary']
        img_graph_1, img_graph_2 = self.graphs_commercial_report(df_graph_commercial_1, df_graph_commercial_2)
        img_graph_3, img_graph_4 = self.graphs_calculation_report(df_graph_calculation_1, df_graph_calculation_2)
        img_graph_5, img_graph_6 = self.graphs_orders_report(df_graph_orders_1)

        y_position = 3
        pdf.image(img_graph_1, x=0.5, y=y_position, w=8.5, h=4.5)
        pdf.image(img_graph_3, x=10.6, y=y_position, w=8.5, h=4.5)
        pdf.image(img_graph_5, x=20.7, y=y_position, w=8.5, h=4.5)
        pdf.ln(5)

        y_position = pdf.get_y()
        pdf.image(img_graph_2, x=0.5, y=y_position, w=8.5, h=4.5)
        pdf.image(img_graph_4, x=10.6, y=y_position, w=8.5, h=4.5)
        pdf.image(img_graph_6, x=20.7, y=y_position, w=8.5, h=4.5)
        pdf.ln(5)

        pdf.set_fill_color(255, 255, 64)
        pdf.set_font('Helvetica', 'B', size=7)
        pdf.cell(19.75, 0.5, 'RESUMEN SEMANAL', fill=True)
        pdf.cell(3, 0.5, (start_date.strftime('%d/%m/%Y')), fill=True, align='C')
        pdf.cell(3, 0.5, '-', fill=True, align='C')
        pdf.cell(3, 0.5, (end_date.strftime('%d/%m/%Y')), fill=True, align='C')
        pdf.ln(0.5)

        pdf.set_fill_color(3, 174, 236)
        pdf.cell(3, 0.5, 'REGISTRADAS:')
        pdf.cell(3, 0.5, str(df_weekly.shape[0]), align='L')
        pdf.cell(1.5, 0.5, '')
        pdf.cell(3, 0.5, 'EN ESTUDIO:')
        pdf.cell(3, 0.5, str(df_weekly[df_weekly['Estado'] == 'En Estudio'].shape[0]), align='L')
        pdf.cell(1.5, 0.5, '')
        pdf.cell(3, 0.5, 'REALIZADAS:')
        pdf.cell(3, 0.5, str(df_weekly[~df_weekly['Estado'].isin(['Registrada', 'En Estudio'])].shape[0]), align='L')
        pdf.cell(1.5, 0.5, '')
        pdf.cell(3, 0.5, 'ADJUDICADAS:')
        pdf.cell(3, 0.5, str(df_weekly[df_weekly['Estado'] == 'Adjudicada'].shape[0]), align='L')
        pdf.ln(0.5)

        pdf.cell(1.5, 0.3, 'OFERTA', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'ESTADO', fill=True, border=1, align='C')
        pdf.cell(2, 0.3, 'RESP.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'CALC.', fill=True, border=1, align='C')
        pdf.cell(3, 0.3, 'CLIENTE', fill=True, border=1, align='C')
        pdf.cell(3.5, 0.3, 'CLIENTE FINAL', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. REC.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. PRES.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. VTO.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PROB.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PRIOR.', fill=True, border=1, align='C')
        pdf.cell(2.75, 0.3, 'MATERIAL', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'Nº EQ.', fill=True, border=1, align='C')
        pdf.cell(2.2, 0.3, 'IMPORTE', fill=True, border=1, align='C')
        pdf.cell(3.25, 0.3, 'ACCIONES', fill=True, border=1, align='C')
        pdf.ln()

        pdf.set_font('DejaVuSansCondensed', size=6)
        for _, row in df_weekly.iterrows():
            # getting the required height of the row
            line_h = pdf.font_size * 1.5
            h_client = pdf.get_multicell_height(2.75, line_h, '' if row['Cliente'] is None else str(row['Cliente']))
            h_clfinal = pdf.get_multicell_height(3.25, line_h, '' if row['Cl. Final'] is None else str(row['Cl. Final']))
            h_material = pdf.get_multicell_height(2.5, line_h, '' if row['Material'] is None else str(row['Material']))
            h_actions = pdf.get_multicell_height(3, line_h, '' if row['Acciones'] is None else str(row['Acciones']))

            row_height = max(h_client, h_clfinal, h_material, h_actions, line_h)

            # Setting values for table
            pdf.cell(1.5, row_height, '' if row['Nº Oferta'] is None else str(row['Nº Oferta']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Estado'] is None else str(row['Estado']), border=1, align='C')
            pdf.cell(2, row_height, '' if row['Responsable'] is None else str(row['Responsable']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Cálculos'] is None else str(row['Cálculos']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3, row_height, '' if row['Cliente'] is None else str(row['Cliente']), border=1)
            pdf.set_xy(x + 3, y)

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.5, row_height, '' if row['Cl. Final'] is None else str(row['Cl. Final']), border=1)
            pdf.set_xy(x + 3.5, y)

            pdf.cell(1.5, row_height, '' if row['Fecha Rec.'] is None else str(row['Fecha Rec.']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Fecha Pres.'] is None else str(row['Fecha Pres.']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Fecha Vto.'] is None else str(row['Fecha Vto.']), border=1, align='C')
            pdf.cell(1, row_height, '' if row['Prob.'] is None else str(row['Prob.']), border=1, align='C')
            pdf.cell(1, row_height, '' if row['Prior.'] is None else str(row['Prior.']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(2.75, row_height, '' if row['Material'] is None else str(row['Material']), border=1)
            pdf.set_xy(x + 2.75, y)

            pdf.cell(1, row_height, '' if row['Nº Eqs.'] is None else str(row['Nº Eqs.']), border=1, align='C')
            pdf.cell(2.2, row_height, '' if row['Importe'] is None else str(row['Importe']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.25, row_height, '' if row['Acciones'] is None else str(row['Acciones']), border=1)
            pdf.set_xy(x + 2.5, y)

            pdf.ln(row_height)

        pdf.set_font('DejaVuSansCondensed-Bold', size=7)
        pdf.cell(22, 0.3, '')
        pdf.cell(4.25, 0.3, 'TOTAL:', align='R')
        pdf.cell(2.5, 0.3, self.euro_format(df_weekly['Importe Euros'].sum()), align='C')
        pdf.ln(0.5)

        pdf.set_fill_color(255, 255, 64)
        pdf.cell(28.75, 0.5, 'OFERTAS EN ACTIVO', fill=True)
        pdf.ln(0.5)

        pdf.set_fill_color(3, 174, 236)

        df_registered = df_active[df_active['Estado'] == 'Registrada'].sort_values(by=['Responsable', 'Nº Oferta'])

        if df_registered.shape[0] > 0:
            pdf.cell(3, 0.5, 'REGISTRADAS:')
            pdf.cell(3, 0.5, str(df_registered.shape[0]), align='L')
            pdf.ln(0.5)

            pdf.cell(1.5, 0.3, 'OFERTA', fill=True, border=1, align='C')
            pdf.cell(1.5, 0.3, 'ESTADO', fill=True, border=1, align='C')
            pdf.cell(2, 0.3, 'RESP.', fill=True, border=1, align='C')
            pdf.cell(1.5, 0.3, 'CALC.', fill=True, border=1, align='C')
            pdf.cell(3, 0.3, 'CLIENTE', fill=True, border=1, align='C')
            pdf.cell(3.5, 0.3, 'CLIENTE FINAL', fill=True, border=1, align='C')
            pdf.cell(1.5, 0.3, 'F. REC.', fill=True, border=1, align='C')
            pdf.cell(1.5, 0.3, 'F. PRES.', fill=True, border=1, align='C')
            pdf.cell(1.5, 0.3, 'F. VTO.', fill=True, border=1, align='C')
            pdf.cell(1, 0.3, 'PROB.', fill=True, border=1, align='C')
            pdf.cell(1, 0.3, 'PRIOR.', fill=True, border=1, align='C')
            pdf.cell(2.75, 0.3, 'MATERIAL', fill=True, border=1, align='C')
            pdf.cell(1, 0.3, 'Nº EQ.', fill=True, border=1, align='C')
            pdf.cell(2.2, 0.3, 'IMPORTE', fill=True, border=1, align='C')
            pdf.cell(3.25, 0.3, 'ACCIONES', fill=True, border=1, align='C')
            pdf.ln()

            pdf.set_font('DejaVuSansCondensed', size=6)
            for _, row in df_registered.iterrows():
                # getting the required height of the row
                line_h = pdf.font_size * 1.5
                h_client = pdf.get_multicell_height(2.75, line_h, '' if row['Cliente'] is None else str(row['Cliente']))
                h_clfinal = pdf.get_multicell_height(3.25, line_h, '' if row['Cl. Final'] is None else str(row['Cl. Final']))
                h_material = pdf.get_multicell_height(2.5, line_h, '' if row['Material'] is None else str(row['Material']))
                h_actions = pdf.get_multicell_height(3, line_h, '' if row['Acciones'] is None else str(row['Acciones']))

                row_height = max(h_client, h_clfinal, h_material, h_actions, line_h)

                # Setting values for table
                pdf.cell(1.5, row_height, '' if row['Nº Oferta'] is None else str(row['Nº Oferta']), border=1, align='C')
                pdf.cell(1.5, row_height, '' if row['Estado'] is None else str(row['Estado']), border=1, align='C')
                pdf.cell(2, row_height, '' if row['Responsable'] is None else str(row['Responsable']), border=1, align='C')
                pdf.cell(1.5, row_height, '' if row['Cálculos'] is None else str(row['Cálculos']), border=1, align='C')

                x = pdf.get_x()
                y = pdf.get_y()
                pdf.fixed_height_multicell(3, row_height, '' if row['Cliente'] is None else str(row['Cliente']), border=1)
                pdf.set_xy(x + 3, y)

                x = pdf.get_x()
                y = pdf.get_y()
                pdf.fixed_height_multicell(3.5, row_height, '' if row['Cl. Final'] is None else str(row['Cl. Final']), border=1)
                pdf.set_xy(x + 3.5, y)

                pdf.cell(1.5, row_height, '' if row['Fecha Rec.'] is None else str(row['Fecha Rec.']), border=1, align='C')
                pdf.cell(1.5, row_height, '' if row['Fecha Pres.'] is None else str(row['Fecha Pres.']), border=1, align='C')
                pdf.cell(1.5, row_height, '' if row['Fecha Vto.'] is None else str(row['Fecha Vto.']), border=1, align='C')
                pdf.cell(1, row_height, '' if row['Prob.'] is None else str(row['Prob.']), border=1, align='C')
                pdf.cell(1, row_height, '' if row['Prior.'] is None else str(row['Prior.']), border=1, align='C')

                x = pdf.get_x()
                y = pdf.get_y()
                pdf.fixed_height_multicell(2.75, row_height, '' if row['Material'] is None else str(row['Material']), border=1)
                pdf.set_xy(x + 2.75, y)

                pdf.cell(1, row_height, '' if row['Nº Eqs.'] is None else str(row['Nº Eqs.']), border=1, align='C')
                pdf.cell(2.2, row_height, '' if row['Importe'] is None else str(row['Importe']), border=1, align='C')

                x = pdf.get_x()
                y = pdf.get_y()
                pdf.fixed_height_multicell(3.25, row_height, '' if row['Acciones'] is None else str(row['Acciones']), border=1)
                pdf.set_xy(x + 2.5, y)

                pdf.ln(row_height)

            pdf.set_font('DejaVuSansCondensed-Bold', size=7)
            pdf.cell(20.75, 0.3, '')
            pdf.cell(5, 0.3, 'TOTAL:', align='R')
            pdf.cell(3, 0.3, self.euro_format(df_registered['Importe Euros'].sum()), align='C')
            pdf.ln()

        df_study = df_active[df_active['Estado'] == 'En Estudio'].sort_values(by=['Responsable', 'Nº Oferta'])

        df_study['Fecha Vto.'] = pd.to_datetime(df_study['Fecha Vto.'], format='%d/%m/%Y', errors='coerce')
        df_study['days_diff'] = (pd.Timestamp.today() - df_study['Fecha Vto.']).dt.days
        df_study['Fecha Vto.'] = df_study['Fecha Vto.'].dt.strftime('%d/%m/%Y')

        pdf.set_font('Helvetica', 'B', size=7)
        pdf.cell(3, 0.5, 'EN ESTUDIO:')
        pdf.cell(3, 0.5, str(df_study.shape[0]), align='L')
        pdf.ln(0.5)

        pdf.cell(1.5, 0.3, 'OFERTA', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'ESTADO', fill=True, border=1, align='C')
        pdf.cell(2, 0.3, 'RESP.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'CALC.', fill=True, border=1, align='C')
        pdf.cell(3, 0.3, 'CLIENTE', fill=True, border=1, align='C')
        pdf.cell(3.5, 0.3, 'CLIENTE FINAL', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. REC.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. PRES.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. VTO.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PROB.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PRIOR.', fill=True, border=1, align='C')
        pdf.cell(2.75, 0.3, 'MATERIAL', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'Nº EQ.', fill=True, border=1, align='C')
        pdf.cell(2.2, 0.3, 'IMPORTE', fill=True, border=1, align='C')
        pdf.cell(3.25, 0.3, 'ACCIONES', fill=True, border=1, align='C')
        pdf.ln()

        pdf.set_fill_color(255, 105, 105)
        pdf.set_font('DejaVuSansCondensed', size=6)
        for _, row in df_study.iterrows():
            # getting the required height of the row
            line_h = pdf.font_size * 1.5
            h_client = pdf.get_multicell_height(2.75, line_h, '' if row['Cliente'] is None else str(row['Cliente']))
            h_clfinal = pdf.get_multicell_height(3.25, line_h, '' if row['Cl. Final'] is None else str(row['Cl. Final']))
            h_material = pdf.get_multicell_height(2.5, line_h, '' if row['Material'] is None else str(row['Material']))
            h_actions = pdf.get_multicell_height(3, line_h, '' if row['Acciones'] is None else str(row['Acciones']))

            row_height = max(h_client, h_clfinal, h_material, h_actions, line_h)

            # Setting values for table
            pdf.cell(1.5, row_height, '' if row['Nº Oferta'] is None else str(row['Nº Oferta']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Estado'] is None else str(row['Estado']), border=1, align='C')
            pdf.cell(2, row_height, '' if row['Responsable'] is None else str(row['Responsable']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Cálculos'] is None else str(row['Cálculos']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3, row_height, '' if row['Cliente'] is None else str(row['Cliente']), border=1)
            pdf.set_xy(x + 3, y)

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.5, row_height, '' if row['Cl. Final'] is None else str(row['Cl. Final']), border=1)
            pdf.set_xy(x + 3.5, y)

            pdf.cell(1.5, row_height, '' if row['Fecha Rec.'] is None else str(row['Fecha Rec.']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Fecha Pres.'] is None else str(row['Fecha Pres.']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Fecha Vto.'] is None else str(row['Fecha Vto.']), border=1, align='C', fill=True if row['days_diff'] > 0 else False)
            pdf.cell(1, row_height, '' if row['Prob.'] is None else str(row['Prob.']), border=1, align='C')
            pdf.cell(1, row_height, '' if row['Prior.'] is None else str(row['Prior.']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(2.75, row_height, '' if row['Material'] is None else str(row['Material']), border=1)
            pdf.set_xy(x + 2.75, y)

            pdf.cell(1, row_height, '' if row['Nº Eqs.'] is None else str(row['Nº Eqs.']), border=1, align='C')
            pdf.cell(2.2, row_height, '' if row['Importe'] is None else str(row['Importe']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.25, row_height, '' if row['Acciones'] is None else str(row['Acciones']), border=1)
            pdf.set_xy(x + 2.5, y)

            pdf.ln(row_height)

        pdf.set_font('DejaVuSansCondensed-Bold', size=7)
        pdf.cell(20.75, 0.3, '')
        pdf.cell(5, 0.3, 'TOTAL:', align='R')
        pdf.cell(3, 0.3, self.euro_format(df_study['Importe Euros'].sum()), align='C')
        pdf.ln()

        # pdf.add_page()

        df_active['Fecha Pres.'] = pd.to_datetime(df_active['Fecha Pres.'], format='%d/%m/%Y', errors='coerce')
        df_active['days_diff'] = (pd.Timestamp.today() - df_active['Fecha Pres.']).dt.days

        df_presented = df_active[df_active['Estado'] == 'Presentada'].sort_values(by=['Fecha Pres.'])

        df_less_30 = df_presented[df_presented['days_diff'] <= 30].copy()
        df_more_30 = df_presented[df_presented['days_diff'] > 30].copy()

        df_less_30['Fecha Pres.'] = df_less_30['Fecha Pres.'].dt.strftime('%d/%m/%Y')
        df_more_30['Fecha Pres.'] = df_more_30['Fecha Pres.'].dt.strftime('%d/%m/%Y')

        pdf.set_fill_color(3, 174, 236)
        pdf.set_font('Helvetica', 'B', size=7)
        pdf.cell(3, 0.5, 'PRESENTADAS:')
        pdf.cell(3, 0.5, str(df_presented.shape[0]), align='L')
        pdf.ln(0.5)

        df_active['Fecha Pres.'] = pd.to_datetime(df_active['Fecha Pres.'], errors='coerce', dayfirst=True)

        pdf.cell(1.5, 0.3, 'OFERTA', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'ESTADO', fill=True, border=1, align='C')
        pdf.cell(2, 0.3, 'RESP.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'CALC.', fill=True, border=1, align='C')
        pdf.cell(3, 0.3, 'CLIENTE', fill=True, border=1, align='C')
        pdf.cell(3.5, 0.3, 'CLIENTE FINAL', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. REC.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. PRES.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. VTO.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PROB.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PRIOR.', fill=True, border=1, align='C')
        pdf.cell(2.75, 0.3, 'MATERIAL', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'Nº EQ.', fill=True, border=1, align='C')
        pdf.cell(2.2, 0.3, 'IMPORTE', fill=True, border=1, align='C')
        pdf.cell(3.25, 0.3, 'ACCIONES', fill=True, border=1, align='C')
        pdf.ln()

        pdf.set_font('DejaVuSansCondensed', size=6)
        for _, row in df_less_30.iterrows():
            # getting the required height of the row
            line_h = pdf.font_size * 1.5
            h_client = pdf.get_multicell_height(2.75, line_h, '' if row['Cliente'] is None else str(row['Cliente']))
            h_clfinal = pdf.get_multicell_height(3.25, line_h, '' if row['Cl. Final'] is None else str(row['Cl. Final']))
            h_material = pdf.get_multicell_height(2.5, line_h, '' if row['Material'] is None else str(row['Material']))
            h_actions = pdf.get_multicell_height(3, line_h, '' if row['Acciones'] is None else str(row['Acciones']))

            row_height = max(h_client, h_clfinal, h_material, h_actions, line_h)

            # Setting values for table
            pdf.cell(1.5, row_height, '' if row['Nº Oferta'] is None else str(row['Nº Oferta']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Estado'] is None else str(row['Estado']), border=1, align='C')
            pdf.cell(2, row_height, '' if row['Responsable'] is None else str(row['Responsable']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Cálculos'] is None else str(row['Cálculos']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3, row_height, '' if row['Cliente'] is None else str(row['Cliente']), border=1)
            pdf.set_xy(x + 3, y)

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.5, row_height, '' if row['Cl. Final'] is None else str(row['Cl. Final']), border=1)
            pdf.set_xy(x + 3.5, y)

            pdf.cell(1.5, row_height, '' if row['Fecha Rec.'] is None else str(row['Fecha Rec.']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Fecha Pres.'] is None else str(row['Fecha Pres.']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Fecha Vto.'] is None else str(row['Fecha Vto.']), border=1, align='C')
            pdf.cell(1, row_height, '' if row['Prob.'] is None else str(row['Prob.']), border=1, align='C')
            pdf.cell(1, row_height, '' if row['Prior.'] is None else str(row['Prior.']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(2.75, row_height, '' if row['Material'] is None else str(row['Material']), border=1)
            pdf.set_xy(x + 2.75, y)

            pdf.cell(1, row_height, '' if row['Nº Eqs.'] is None else str(row['Nº Eqs.']), border=1, align='C')
            pdf.cell(2.2, row_height, '' if row['Importe'] is None else str(row['Importe']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.25, row_height, '' if row['Acciones'] is None else str(row['Acciones']), border=1)
            pdf.set_xy(x + 2.5, y)

            pdf.ln(row_height)

        pdf.set_fill_color(3, 174, 236)
        pdf.set_font('DejaVuSansCondensed-Bold', size=7)
        pdf.cell(20.75, 0.3, '')
        pdf.cell(5, 0.3, 'TOTAL:', align='R')
        pdf.cell(3, 0.3, self.euro_format(df_less_30['Importe Euros'].sum()), align='C')
        pdf.ln()

        pdf.cell(1.5, 0.3, 'OFERTA', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'ESTADO', fill=True, border=1, align='C')
        pdf.cell(2, 0.3, 'RESP.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'CALC.', fill=True, border=1, align='C')
        pdf.cell(3, 0.3, 'CLIENTE', fill=True, border=1, align='C')
        pdf.cell(3.5, 0.3, 'CLIENTE FINAL', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. REC.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. PRES.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. VTO.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PROB.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PRIOR.', fill=True, border=1, align='C')
        pdf.cell(2.75, 0.3, 'MATERIAL', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'Nº EQ.', fill=True, border=1, align='C')
        pdf.cell(2.2, 0.3, 'IMPORTE', fill=True, border=1, align='C')
        pdf.cell(3.25, 0.3, 'ACCIONES', fill=True, border=1, align='C')
        pdf.ln()

        pdf.set_fill_color(255, 105, 105)
        pdf.set_font('DejaVuSansCondensed', size=6)
        for _, row in df_more_30.iterrows():
            # getting the required height of the row
            line_h = pdf.font_size * 1.5
            h_client = pdf.get_multicell_height(2.75, line_h, '' if row['Cliente'] is None else str(row['Cliente']))
            h_clfinal = pdf.get_multicell_height(3.25, line_h, '' if row['Cl. Final'] is None else str(row['Cl. Final']))
            h_material = pdf.get_multicell_height(2.5, line_h, '' if row['Material'] is None else str(row['Material']))
            h_actions = pdf.get_multicell_height(3, line_h, '' if row['Acciones'] is None else str(row['Acciones']))

            row_height = max(h_client, h_clfinal, h_material, h_actions, line_h)

            # Setting values for table
            pdf.cell(1.5, row_height, '' if row['Nº Oferta'] is None else str(row['Nº Oferta']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Estado'] is None else str(row['Estado']), border=1, align='C')
            pdf.cell(2, row_height, '' if row['Responsable'] is None else str(row['Responsable']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Cálculos'] is None else str(row['Cálculos']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3, row_height, '' if row['Cliente'] is None else str(row['Cliente']), border=1)
            pdf.set_xy(x + 3, y)

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.5, row_height, '' if row['Cl. Final'] is None else str(row['Cl. Final']), border=1)
            pdf.set_xy(x + 3.5, y)

            pdf.cell(1.5, row_height, '' if row['Fecha Rec.'] is None else str(row['Fecha Rec.']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Fecha Pres.'] is None else str(row['Fecha Pres.']), border=1, align='C', fill=True)
            pdf.cell(1.5, row_height, '' if row['Fecha Vto.'] is None else str(row['Fecha Vto.']), border=1, align='C')
            pdf.cell(1, row_height, '' if row['Prob.'] is None else str(row['Prob.']), border=1, align='C')
            pdf.cell(1, row_height, '' if row['Prior.'] is None else str(row['Prior.']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(2.75, row_height, '' if row['Material'] is None else str(row['Material']), border=1)
            pdf.set_xy(x + 2.75, y)

            pdf.cell(1, row_height, '' if row['Nº Eqs.'] is None else str(row['Nº Eqs.']), border=1, align='C')
            pdf.cell(2.2, row_height, '' if row['Importe'] is None else str(row['Importe']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.25, row_height, '' if row['Acciones'] is None else str(row['Acciones']), border=1)
            pdf.set_xy(x + 2.5, y)

            pdf.ln(row_height)

        pdf.set_font('DejaVuSansCondensed-Bold', size=7)
        pdf.cell(20.75, 0.3, '')
        pdf.cell(5, 0.3, 'TOTAL:', align='R')
        pdf.cell(3, 0.3, self.euro_format(df_more_30['Importe Euros'].sum()), align='C')
        pdf.ln()

        return pdf

    def euro_format(self, valor):
        return f"{valor:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')

    def euro_format_axis(self, x, pos):
        if x >= 1_000_000:
            return f'{x/1_000_000:.1f}M€'.replace('.', ',')
        elif x >= 1_000:
            return f'{x/1_000:.0f}k€'.replace('.', ',')
        else:
            return f'{x:.0f}€'

    def get_date_range(self):
        """
        Shows input dialogs to enter dates and convert to correct format
        """
        start_date_str, ok1 = QtWidgets.QInputDialog.getText(None, "Fecha inicial", "Introduce la fecha inicial (DD/MM/YYYY):")
        if not ok1 or not start_date_str:
            return None, None

        end_date_str, ok2 = QtWidgets.QInputDialog.getText(None, "Fecha final", "Introduce la fecha final (DD/MM/YYYY):")
        if not ok2 or not end_date_str:
            return None, None

        # Validate and convert date to format yyyy-mm-dd
        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y").date()
        except ValueError:
            MessageHelper.show_message("Formato de fecha inválido. Usa DD/MM/YYYY.", "warning")
            return None, None

        return start_date, end_date

    def graphs_commercial_report(self, df_graph_commercial_1, df_graph_commercial_2):
        final_state_mapping = {
            "Registrada": ["Adjudicada", "Declinada", "No Ofertada", "Perdida", "Presentada", "Registrada", "En Estudio"],
            "No Ofertada": ["No Ofertada", "Declinada", "En Estudio"],
            "Ofertada": ["Adjudicada", "Perdida", "Presentada"],
            "No PO": ["Perdida", "Presentada"],
            "PO": ["Adjudicada"]
        }

        state_colors = {
            "Registrada": "#9467bd",
            "No Ofertada": "#ff7f0e",
            "Ofertada": "#ffe70eda",
            "No PO": "#d62728",
            "PO": "#2ca02c",
        }

        pivot_table_commercial_1 = df_graph_commercial_1.pivot_table(index='Responsable', columns='Estado', values='Importe Final', aggfunc='sum', fill_value=0)

        categories = pivot_table_commercial_1.index.tolist()
        final_states = list(final_state_mapping.keys())
        final_values = np.zeros((len(categories), len(final_states)))

        for state in state_colors.keys():
            if state not in pivot_table_commercial_1.columns:
                pivot_table_commercial_1[state] = 0

        for j, final_state in enumerate(final_states):
            original_list = final_state_mapping[final_state]
            # Sumatorio de las columnas originales que forman el estado final
            final_values[:, j] = pivot_table_commercial_1[original_list].sum(axis=1)

        x = np.arange(len(categories))           # Categories position
        width = 0.8 / len(final_states)               # Bar width

        fig, ax = plt.subplots(figsize=(8,5))

        for i, state in enumerate(final_states):
            color = state_colors.get(state, "#119efc")
            ax.bar(x + i*width, final_values[:, i], width=width, label=state, color=color)

        ax.set_xticks(x + width*(len(final_states)-1)/2)  # Center ticks
        ax.set_xticklabels(categories)

        ax.yaxis.set_major_formatter(FuncFormatter(self.euro_format_axis))
        ax.set_ylabel("Importe")
        ax.set_title("Importes por responsable y estado")
        ax.legend()

        img_graph_1 = BytesIO()
        plt.savefig(img_graph_1, format='PNG', bbox_inches='tight')
        plt.close()
        img_graph_1.seek(0)

        pivot_table_commercial_2 = df_graph_commercial_2.pivot_table(index='Responsable', columns='Estado', values='Nº Oferta', aggfunc='count', fill_value=0)

        categories = pivot_table_commercial_2.index.tolist()
        final_states = list(final_state_mapping.keys())
        final_values = np.zeros((len(categories), len(final_states)))

        for state in state_colors.keys():
            if state not in pivot_table_commercial_2.columns:
                pivot_table_commercial_2[state] = 0

        for j, final_state in enumerate(final_states):
            original_list = final_state_mapping[final_state]
            # Sumatorio de las columnas originales que forman el estado final
            final_values[:, j] = pivot_table_commercial_2[original_list].sum(axis=1)

        x = np.arange(len(categories))           # Categories position
        width = 0.8 / len(final_states)               # Bar width

        fig, ax = plt.subplots(figsize=(8,5))

        for i, state in enumerate(final_states):
            color = state_colors.get(state, "#119efc")
            ax.bar(x + i*width, final_values[:, i], width=width, label=state, color=color)

        ax.set_xticks(x + width*(len(final_states)-1)/2)  # Center ticks
        ax.set_xticklabels(categories)

        ax.set_ylabel("Recuento")
        ax.set_title("Recuento de ofertas por estado")
        ax.legend()

        img_graph_2 = BytesIO()
        plt.savefig(img_graph_2, format='PNG', bbox_inches='tight')
        plt.close()
        img_graph_2.seek(0)

        return [img_graph_1, img_graph_2]

    def graphs_calculation_report(self, df_graph_calculation_1, df_graph_calculation_2):
        final_state_mapping = {
            "Ofertada": ["Adjudicada", "Perdida", "Presentada", "No Ofertada", "Declinada"],
            "No PO": ["Perdida", "Presentada", "No Ofertada", "Declinada"],
            "PO": ["Adjudicada"]
        }

        state_colors = {
            "Ofertada": "#ffe70eda",
            "No PO": "#d62728",
            "PO": "#2ca02c",
        }

        pivot_table_calculation_1 = df_graph_calculation_1.pivot_table(index='Responsable', columns='Estado', values='Importe Final', aggfunc='sum', fill_value=0)

        categories = pivot_table_calculation_1.index.tolist()
        final_states = list(final_state_mapping.keys())
        final_values = np.zeros((len(categories), len(final_states)))

        for state in state_colors.keys():
            if state not in pivot_table_calculation_1.columns:
                pivot_table_calculation_1[state] = 0

        for j, final_state in enumerate(final_states):
            original_list = final_state_mapping[final_state]
            # Filter columns in pivot only
            existing_columns = [col for col in original_list if col in pivot_table_calculation_1.columns]
            if existing_columns:
                final_values[:, j] = pivot_table_calculation_1[existing_columns].sum(axis=1)
            else:
                final_values[:, j] = 0

        x = np.arange(len(categories))           # Categories position
        width = 0.8 / len(final_states)               # Bar width

        fig, ax = plt.subplots(figsize=(8,5))

        for i, state in enumerate(final_states):
            color = state_colors.get(state, "#119efc")
            ax.bar(x + i*width, final_values[:, i], width=width, label=state, color=color)

        ax.set_xticks(x + width*(len(final_states)-1)/2)  # Center ticks
        ax.set_xticklabels(categories)

        ax.yaxis.set_major_formatter(FuncFormatter(self.euro_format_axis))
        ax.set_ylabel("Importe")
        ax.set_title("Importes por responsable y estado")
        ax.legend()

        img_graph_3 = BytesIO()
        plt.savefig(img_graph_3, format='PNG', bbox_inches='tight')
        plt.close()
        img_graph_3.seek(0)

        pivot_table_calculation_2 = df_graph_calculation_2.pivot_table(index='Responsable', columns='Estado', values='Nº Oferta', aggfunc='count', fill_value=0)

        categories = pivot_table_calculation_2.index.tolist()
        final_states = list(final_state_mapping.keys())
        final_values = np.zeros((len(categories), len(final_states)))

        for state in state_colors.keys():
            if state not in pivot_table_calculation_2.columns:
                pivot_table_calculation_2[state] = 0

        for j, final_state in enumerate(final_states):
            original_list = final_state_mapping[final_state]
            # Filter columns in pivot only
            existing_columns = [col for col in original_list if col in pivot_table_calculation_2.columns]
            if existing_columns:
                final_values[:, j] = pivot_table_calculation_2[existing_columns].sum(axis=1)
            else:
                final_values[:, j] = 0

        fig, ax = plt.subplots(figsize=(8,5))

        for i, state in enumerate(final_states):
            color = state_colors.get(state, "#119efc")
            ax.bar(x + i*width, final_values[:, i], width=width, label=state, color=color)

        ax.set_xticks(x + width*(len(final_states)-1)/2)  # Center ticks
        ax.set_xticklabels(categories)

        ax.set_ylabel("Recuento")
        ax.set_title("Recuento de ofertas por estado")
        ax.legend()

        img_graph_4 = BytesIO()
        plt.savefig(img_graph_4, format='PNG', bbox_inches='tight')
        plt.close()
        img_graph_4.seek(0)

        return [img_graph_3, img_graph_4]

    def graphs_orders_report(self, df_graph_orders_1):
        df_p = df_graph_orders_1[df_graph_orders_1['Nº Pedido'].str.startswith('P-')]
        df_pa = df_graph_orders_1[df_graph_orders_1['Nº Pedido'].str.startswith('PA-')]

        sum_amount = pd.Series({
            'P': df_p['Importe Pedido'].sum(),
            'PA': df_pa['Importe Pedido'].sum()
        })

        count = pd.Series({
            'P': df_p.shape[0],
            'PA': df_pa.shape[0]
        })

        fig, ax = plt.subplots(figsize=(8,5))
        sum_amount.plot(kind='bar', color=['green', 'yellow'])
        ax.yaxis.set_major_formatter(FuncFormatter(self.euro_format_axis))
        ax.set_xticklabels(sum_amount.index, rotation=0)
        ax.set_title('Suma de Importe por Tipo de Pedido')
        ax.set_ylabel('Suma Importe')
        ax.set_xlabel('Tipo Pedido')

        img_graph_5 = BytesIO()
        plt.savefig(img_graph_5, format='PNG', bbox_inches='tight')
        plt.close()
        img_graph_5.seek(0)

        fig, ax = plt.subplots(figsize=(8,5))
        count.plot(kind='bar', color=['green', 'yellow'])
        ax.set_xticklabels(count.index, rotation=0)
        ax.set_title('Recuento por Tipo de Pedido')
        ax.set_ylabel('Recuento')
        ax.set_xlabel('Tipo Pedido')

        img_graph_6 = BytesIO()
        plt.savefig(img_graph_6, format='PNG', bbox_inches='tight')
        plt.close()
        img_graph_6.seek(0)

        return [img_graph_5, img_graph_6]

    def report_orders(self):
        query_orders = (r"""
                    SELECT p.num_order, o.responsible, o.client, o.final_client, o.material, p.items_number, p.order_date, p.expected_date,
                    p.material_available, p.recep_date_workshop, p.porc_workshop, p.expected_date_workshop, p.expected_date_assembly, p.percent_sent_workshop,
                    COALESCE(
                        CAST(
                            NULLIF(
                                REGEXP_REPLACE(o.delivery_time, '.*?(\d+)[^\d]+(\d+).*', '\2'), -- take second number
                                ''
                            ) AS INTEGER
                        ),
                        0
                    ) AS deliv_time_num,
                    p.porc_deliveries, p.last_date_deliveries, p.regularisation, p.notes, p.notes_technical, p.order_amount, p.closed,
                    pt.variable, p.total_charged
                    FROM orders as p
                    LEFT JOIN offers as o ON p.num_offer = o.num_offer
                    LEFT JOIN product_type as pt ON o.material = pt.material
                    WHERE p.num_order NOT LIKE 'PA%' AND p.total_charged IS NULL""")

        query_order_amount = ("""
                SELECT num_order, SUM(amount) AS total_amount_tags FROM (
                SELECT num_order, amount FROM tags_data.tags_flow

                UNION ALL

                SELECT num_order, amount FROM tags_data.tags_temp

                UNION ALL

                SELECT num_order, amount FROM tags_data.tags_level

                UNION ALL

                SELECT num_order, amount FROM tags_data.tags_others
                ) AS combined
                GROUP BY num_order
                """)

        query_docs = ("""
                    SELECT 
                    num_order,
                    COUNT(num_doc_eipsa) AS total_docs,
                    SUM(CASE WHEN state IS NULL OR state = '' THEN 1 ELSE 0 END) AS count_no_sent,
                    SUM(CASE WHEN state = 'Enviado' THEN 1 ELSE 0 END) AS count_sent,
                    SUM(CASE WHEN state LIKE 'Com%' THEN 1 ELSE 0 END) AS count_comment,
                    SUM(CASE WHEN state LIKE 'Eli%' THEN 1 ELSE 0 END) AS count_deleted,
                    SUM(CASE WHEN state LIKE 'Ap%' THEN 1 ELSE 0 END) AS count_approved,
                    COALESCE(
                        TO_CHAR(MIN(CASE WHEN doc_type_id IN (1, 16) THEN TO_DATE(date_first_rev, 'DD/MM/YYYY') END), 'DD/MM/YYYY'),
                        ''
                    ) AS min_date_sent_drawings,
                    COALESCE(
                        TO_CHAR(MAX(CASE WHEN state = 'Aprobado' AND doc_type_id IN (1, 16) THEN TO_DATE(state_date, 'DD/MM/YYYY') END), 'DD/MM/YYYY'),
                        ''
                    ) AS max_date_approved_drawings,
                    COALESCE(
                        TO_CHAR(MIN(CASE WHEN doc_type_id = 6 THEN TO_DATE(date_first_rev, 'DD/MM/YYYY') END), 'DD/MM/YYYY'),
                        ''
                    ) AS min_date_sent_dossier,
                    COALESCE(
                        TO_CHAR(MAX(CASE WHEN state = 'Aprobado' AND doc_type_id = 6 THEN TO_DATE(state_date, 'DD/MM/YYYY') END), 'DD/MM/YYYY'),
                        ''
                    ) AS max_date_approved_dossier
                FROM documentation
                GROUP BY num_order
                """)

        query_tags_fab = ("""
                SELECT num_order, MAX(date_final_fab) AS max_date_fab FROM (
                SELECT num_order, final_verif_dim_date AS date_final_fab FROM tags_data.tags_flow
                UNION ALL
                SELECT num_order, final_verif_of_eq_date AS date_final_fab FROM tags_data.tags_flow

                UNION ALL

                SELECT num_order, final_verif_dim_date AS date_final_fab FROM tags_data.tags_temp
                UNION ALL
                SELECT num_order, final_verif_of_eq_date AS date_final_fab FROM tags_data.tags_temp
                UNION ALL
                SELECT num_order, final_verif_of_sensor_date AS date_final_fab FROM tags_data.tags_temp

                UNION ALL

                SELECT num_order, final_verif_dim_date AS date_final_fab FROM tags_data.tags_level
                UNION ALL
                SELECT num_order, final_verif_of_eq_date AS date_final_fab FROM tags_data.tags_level

                UNION ALL

                SELECT num_order, final_verif_dim_date AS date_final_fab FROM tags_data.tags_others
                UNION ALL
                SELECT num_order, final_verif_of_eq_date AS date_final_fab FROM tags_data.tags_others
                ) AS combined
                GROUP BY num_order
                """)

        query_tags_insp = ("""
                SELECT num_order, SUM(items_inspected) AS items_inspected_count FROM (
                SELECT num_order, SUM(CASE WHEN inspection IS NOT NULL THEN 1 ELSE 0 END) AS items_inspected FROM tags_data.tags_flow
                GROUP BY num_order

                UNION ALL

                SELECT num_order, SUM(CASE WHEN inspection IS NOT NULL THEN 1 ELSE 0 END) AS items_inspected FROM tags_data.tags_temp
                GROUP BY num_order

                UNION ALL

                SELECT num_order, SUM(CASE WHEN inspection IS NOT NULL THEN 1 ELSE 0 END) AS items_inspected FROM tags_data.tags_level
                GROUP BY num_order

                UNION ALL

                SELECT num_order, SUM(CASE WHEN inspection IS NOT NULL THEN 1 ELSE 0 END) AS items_inspected FROM tags_data.tags_others
                GROUP BY num_order
                ) AS combined
                GROUP BY num_order
                """)

        query_tags_fact = ("""
                SELECT num_order, SUM(percent_amount_fact) AS percent_fact, SUM(amount_fact) AS total_fact FROM (
                SELECT num_order, (amount_fact::numeric * COALESCE(percent_invoiced, 0) / 100.0) AS percent_amount_fact, amount_fact FROM tags_data.tags_flow

                UNION ALL

                SELECT num_order, (amount_fact::numeric * COALESCE(percent_invoiced, 0) / 100.0) AS percent_amount_fact, amount_fact FROM tags_data.tags_temp

                UNION ALL

                SELECT num_order, (amount_fact::numeric * COALESCE(percent_invoiced, 0) / 100.0) AS percent_amount_fact, amount_fact FROM tags_data.tags_level

                UNION ALL

                SELECT num_order, (amount_fact::numeric * COALESCE(percent_invoiced, 0) / 100.0) AS percent_amount_fact, amount_fact FROM tags_data.tags_others
                ) AS combined
                GROUP BY num_order
                """)

        query_tags_charged = ("""
                SELECT combined.num_order, SUM(combined.percent_amount_fact) AS percent_charged, SUM(combined.amount_fact) AS total_charged
                FROM (
                    SELECT t.num_order, (t.amount_fact::numeric * COALESCE(t.percent_invoiced, 0) / 100.0) AS percent_amount_fact, amount_fact
                    FROM tags_data.tags_flow AS t
                    JOIN purch_fact.invoice_header AS i
                    ON t.invoice_number = i.num_invoice
                    WHERE t.invoice_number IS NOT NULL and i.pay_date IS NOT NULL

                    UNION ALL

                    SELECT t.num_order, (t.amount_fact::numeric * COALESCE(t.percent_invoiced, 0) / 100.0) AS percent_amount_fact, amount_fact
                    FROM tags_data.tags_temp AS t
                    JOIN purch_fact.invoice_header AS i
                    ON t.invoice_number = i.num_invoice
                    WHERE t.invoice_number IS NOT NULL and i.pay_date IS NOT NULL

                    UNION ALL

                    SELECT t.num_order, (t.amount_fact::numeric * COALESCE(t.percent_invoiced, 0) / 100.0) AS percent_amount_fact, amount_fact
                    FROM tags_data.tags_level AS t
                    JOIN purch_fact.invoice_header AS i
                    ON t.invoice_number = i.num_invoice
                    WHERE t.invoice_number IS NOT NULL and i.pay_date IS NOT NULL

                    UNION ALL

                    SELECT t.num_order, (t.amount_fact::numeric * COALESCE(t.percent_invoiced, 0) / 100.0) AS percent_amount_fact, amount_fact
                    FROM tags_data.tags_others AS t
                    JOIN purch_fact.invoice_header AS i
                    ON t.invoice_number = i.num_invoice
                    WHERE t.invoice_number IS NOT NULL and i.pay_date IS NOT NULL
                ) AS combined
                GROUP BY combined.num_order
                """)

        final_query_1 = (f"""
                        SELECT query1."num_order", query1."responsible", query1."client", query1."final_client", query1."material", query1."items_number",
                        TO_CHAR(query1."order_date", 'DD/MM/YYYY') AS order_date, TO_CHAR(query1."expected_date", 'DD/MM/YYYY') AS expected_date,
                        query3."total_docs", query3."count_no_sent", query3."count_sent", query3."count_comment", query3."count_deleted", query3."count_approved",
                        query3."min_date_sent_drawings",
                        query3."max_date_approved_drawings",
                        query1."recep_date_workshop", query1."percent_sent_workshop",
                        
                        CASE 
                            WHEN query3."max_date_approved_drawings" IS NULL OR query3."max_date_approved_drawings" = '' THEN
                                TO_CHAR(query1."expected_date", 'DD/MM/YYYY')
                            ELSE 
                                TO_CHAR((
                                WITH fechas_validas AS (
                                    SELECT d::date
                                    FROM generate_series(
                                        TO_DATE(query3."max_date_approved_drawings", 'DD/MM/YYYY'),
                                        TO_DATE(query3."max_date_approved_drawings", 'DD/MM/YYYY') + INTERVAL '1 year',
                                        INTERVAL '1 day'
                                    ) AS d
                                    WHERE EXTRACT(MONTH FROM d) <> 8  -- excluir agosto
                                    ORDER BY d
                                )
                                SELECT d
                                FROM fechas_validas
                                OFFSET GREATEST(COALESCE(query1."deliv_time_num", 0) * 7 - 1, 0)
                                LIMIT 1
                            ), 'DD/MM/YYYY')
                        END AS new_contractual_date,
                        
                        query1."material_available", 
                        query1."porc_workshop", query1."expected_date_workshop", query1."expected_date_assembly",
                        TO_CHAR(query4."max_date_fab", 'DD/MM/YYYY') AS max_date_fab,
                        query5."items_inspected_count",
                        query3."min_date_sent_dossier",
                        query3."max_date_approved_dossier",
                        query1. "porc_deliveries", query1."last_date_deliveries",
                        (query6.percent_fact::numeric / NULLIF(query6.total_fact::numeric, 0) * 100)::numeric(10,2) AS fact_percent,
                        (query7.percent_charged::numeric / NULLIF(query7.total_charged::numeric, 0) * 100)::numeric(10,2) AS charged_percent,
                        query1."regularisation", query1."notes", query1."notes_technical",
                        query6."total_fact", query2."total_amount_tags", query1."order_amount", query1."variable"
                        FROM ({query_orders}) AS query1
                        
                        LEFT JOIN ({query_order_amount}) AS query2 ON query1."num_order" = query2."num_order"
                        LEFT JOIN ({query_docs}) AS query3 ON query1."num_order" = query3."num_order"
                        LEFT JOIN ({query_tags_fab}) AS query4 ON query1."num_order" = query4."num_order"
                        LEFT JOIN ({query_tags_insp}) AS query5 ON query1."num_order" = query5."num_order"
                        LEFT JOIN ({query_tags_fact}) AS query6 ON query1."num_order" = query6."num_order"
                        LEFT JOIN ({query_tags_charged}) AS query7 ON query1."num_order" = query7."num_order"
                        WHERE query1.closed IS NULL AND query1.num_order NOT LIKE '%R%'
                        ORDER BY query1."num_order" ASC
                        """)

        final_query_2 = (f"""
                        SELECT query1."variable", COUNT(query1."num_order"),
                        SUM(query2."total_amount_tags"::numeric) AS total_order_amount,
                        ROUND((SUM(query3."total_fact"::numeric) / SUM(query2."total_amount_tags"::numeric) * 100), 2) AS fact_percent,
                        ROUND((SUM(query4."total_charged"::numeric) / SUM(query2."total_amount_tags"::numeric) * 100), 2) AS charged_percent,
                        (SUM(query2."total_amount_tags"::numeric) - SUM(query3."total_fact"::numeric)) AS pending
                        FROM ({query_orders}) AS query1
                        LEFT JOIN ({query_order_amount}) AS query2 ON query1."num_order" = query2."num_order"
                        LEFT JOIN ({query_tags_fact}) AS query3 ON query1."num_order" = query3."num_order"
                        LEFT JOIN ({query_tags_charged}) AS query4 ON query1."num_order" = query4."num_order"
                        GROUP BY query1."variable"
                        ORDER BY query1."variable" ASC
                        """)

        columns_1 = ['PEDIDO', 'RESPONSABLE', 'CLIENTE', 'CLIENTE FINAL', 'MATERIAL', 'Nº EQUIPOS',
                    'FECHA PO', 'FECHA CONT.',
                    'DOCS TOTALES', 'DOCS NO ENV.', 'DOCS ENV.', 'DOCS COM.', 'DOCS ELIM.', 'DOCS AP.', 
                    'FECHA ENV PLANOS', 'FECHA AP PLANOS',
                    'FECHA ENV FAB.', '% ENV FAB',
                    'NUEVA FECHA CONT.',
                    'MAT. DISP.', '% FAB', 'PREV. FAB', 'PREV. MONT.',
                    'FECHA FINAL FAB.',
                    'EQS INSPEC.',
                    'FECHA ENV DOSSIER', 'FECHA AP DOSSIER',
                    '% ENV.', 'FECHA ENVÍO',
                    '% FACT.',
                    '% COBRADO',
                    'ORDENES CAMBIO', 'NOTAS', 'NOTAS TÉCNICAS', 'IMPORTE', 'IMPORTE PO TAGS', 'IMPORTE PO', 'VARIABLE']

        columns_2 = ['VARIABLE', 'Nº PEDIDOS', 'IMPORTE TOTAL', '% FACT.', '% COBRADO', 'PTE FACTURAR']

        with Database_Connection(config()) as conn:
            with conn.cursor() as cur:
                cur.execute(final_query_1)
                results_1 = cur.fetchall()

                cur.execute(final_query_2)
                results_2 = cur.fetchall()

            df_1 = pd.DataFrame(results_1, columns=columns_1)
            df_1 = df_1.fillna('')
            df_1.replace('None', '')

            df_1['IMPORTE'] = (
                df_1['IMPORTE']
                .str.replace('€', '', regex=False)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )

            df_1['IMPORTE PO TAGS'] = (
                df_1['IMPORTE PO TAGS']
                .str.replace('€', '', regex=False)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )

            df_1['IMPORTE PO'] = (
                df_1['IMPORTE PO']
                .str.replace('€', '', regex=False)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )

            df_1['IMPORTE'] = df_1.apply(
                lambda row: float(row['IMPORTE'].strip()) if row['IMPORTE'].strip() != '' else
                (float(row['IMPORTE PO TAGS']) if row['IMPORTE PO TAGS'].strip() != '' else
                (float(row['IMPORTE PO']) if row['IMPORTE PO'].strip() != '' else '')),
                axis=1)

            df_2 = df_1.copy()

            df_2['% FACT.'] = pd.to_numeric(df_2['% FACT.'], errors='coerce').fillna(0)
            df_2['% COBRADO'] = pd.to_numeric(df_2['% COBRADO'], errors='coerce').fillna(0)

            df_2['IMPORTE FACTURADO'] = df_2['IMPORTE'] * (df_2['% FACT.'] / 100)
            df_2['IMPORTE COBRADO'] = df_2['IMPORTE'] * (df_2['% COBRADO'] / 100)

            summary = df_2.groupby('VARIABLE').agg(
                **{
                    'Nº PEDIDOS': ('PEDIDO', 'count'),
                    'IMPORTE TOTAL': ('IMPORTE', 'sum'),
                    'IMPORTE FACTURADO': ('IMPORTE FACTURADO', 'sum'),
                    'IMPORTE COBRADO': ('IMPORTE COBRADO', 'sum'),
                }
            ).reset_index()

            summary['% FACT.'] = (summary['IMPORTE FACTURADO'] / summary['IMPORTE TOTAL'] * 100).round(2)
            summary['% COBRADO'] = (summary['IMPORTE COBRADO'] / summary['IMPORTE TOTAL'] * 100).round(2)
            summary['PTE FACTURAR'] = (summary['IMPORTE TOTAL'] - summary['IMPORTE FACTURADO']).round(2)

            summary = summary[columns_2]

            df_3 = pd.read_excel(r'\\nas01\DATOS\Comunes\Ana\CP\informe_estructurado.xlsx')

            order_reports(df_1, summary, df_3)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dbparam = config()
    user_database = dbparam["user"]
    password_database = dbparam["password"]

    # Genera un nombre único para la conexión basado en el nombre de usuario y el contador
    db_manufacture = Create_DBconnection(user_database, password_database, 'Assembly_connection')

    if not db_manufacture:
        sys.exit()

    Purchasing_Order_Control_Window = Ui_Purchasing_Order_Control_Window(db_manufacture,'j.sanz')
    Purchasing_Order_Control_Window.show()
    sys.exit(app.exec())