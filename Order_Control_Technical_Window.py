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
from utils.Database_Manager import Create_DBconnection
from utils.Business_Report import report_offers, report_orders


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
        background_color = QtGui.QColor(255, 255, 255, 0)

        if index.column() == 35:
            if isinstance(value, (date, datetime)):
                if value <= QtCore.QDate.currentDate():
                    background_color = QtGui.QColor(255, 0, 0, 0) #Red

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

class Ui_Technical_Order_Control_Window(QtWidgets.QMainWindow):
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
        Initializes the Ui_Technical_Order_Control_Window, setting up models, proxies, and internal state.

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
                if QtSql.QSqlDatabase.contains("order_control_technical_connection"):
                    QtSql.QSqlDatabase.removeDatabase("order_control_technical_connection")
        except Exception as e:
            print("Error closing connection:", e)


    def setupUi(self, Technical_Order_Control_Window):
        """
        Sets up the user interface components for the main application window.

        Args:
            Technical_Order_Control_Window (QtWidgets.QMainWindow): The main window object to set up.
        """
        self.id_list = []
        data_list = []
        Technical_Order_Control_Window.setObjectName("Technical_Order_Control_Window")
        Technical_Order_Control_Window.resize(400, 561)
        Technical_Order_Control_Window.setMinimumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Technical_Order_Control_Window.setWindowIcon(icon)
        Technical_Order_Control_Window.setStyleSheet(
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
"QMenu::item:selected {background-color: rgb(3, 174, 236);}")
        self.centralwidget = QtWidgets.QWidget(parent=Technical_Order_Control_Window)
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
        Technical_Order_Control_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Technical_Order_Control_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        Technical_Order_Control_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Technical_Order_Control_Window)
        self.statusbar.setObjectName("statusbar")
        Technical_Order_Control_Window.setStatusBar(self.statusbar)
        self.tableOrders.setSortingEnabled(True)
        self.tableOrders.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        self.tableOrders.setStyleSheet("gridline-color: #CCCCCC")

        self.retranslateUi(Technical_Order_Control_Window)
        QtCore.QMetaObject.connectSlotsByName(Technical_Order_Control_Window)

        self.query_data()
        self.toolExpExcel.clicked.connect(self.exporttoexcel)
        self.toolExpReport.clicked.connect(self.generate_report)


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, Technical_Order_Control_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        Technical_Order_Control_Window.setWindowTitle(_translate("Technical_Order_Control_Window", "Control Pedidos"))
        self.Button_All.setText(_translate("Technical_Order_Control_Window", "Ver Todos"))

# Function to load orders on tables
    def query_data(self):
        """
        Queries the database for orders not delivered, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model.setTable("public.orders")
        self.model.setFilter("(num_order NOT LIKE '%R%') AND (porc_deliveries <> 100 OR porc_deliveries IS NULL)")
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
        for i in range(6,13):
            self.tableOrders.hideColumn(i)
        for i in range(14,42):
            self.tableOrders.hideColumn(i)
        for i in range(44,self.model.columnCount()):
            self.tableOrders.hideColumn(i)

        headers=['Nº Pedido', '','Nº Ref','Fecha Pedido','Fecha Cont.','Notas Comercial','','','','','','','','Fecha Env Fab','F. Prev. Taller','',
                '% Montaje','Cambios %','F. Rec.','F. Prev. Montaje','Observaciones', 'Fecha Aviso',
                '', 'Fecha Envío', '', '','OK', '', '', '', '', '','','Extras', 'Aval', 'Estado Aval', 'Fecha Vto. Aval',
                '', 'Ordenes de Cambio', '', '', '', '% Env Fab', 'Notas Técnicas']

        self.tableOrders.setItemDelegate(AlignDelegate(self.tableOrders))
        self.color_delegate = ColorDelegate(self)
        self.tableOrders.setItemDelegateForColumn(4, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(14, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(16, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(19, self.color_delegate)
        # self.tableOrders.setItemDelegateForColumn(35, self.color_delegate)
        self.tableOrders.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setSectionResizeMode(13, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setSectionResizeMode(43, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setDefaultSectionSize(80)
        self.tableOrders.horizontalHeader().resizeSection(16, 60)
        self.tableOrders.horizontalHeader().resizeSection(20, 700)
        self.tableOrders.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.tableOrders.setStyleSheet("gridline-color: #CCCCCC")
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
        for i in range(6,13):
            self.tableOrders.hideColumn(i)
        for i in range(14,42):
            self.tableOrders.hideColumn(i)
        for i in range(44,self.model.columnCount()):
            self.tableOrders.hideColumn(i)

        headers=['Nº Pedido', '','Nº Ref','Fecha Pedido','Fecha Cont.','Notas Comercial','','','','','','','','Fecha Env Fab','F. Prev. Taller','',
                '% Montaje','Cambios %','F. Rec.','F. Prev. Montaje','Observaciones', 'Fecha Aviso',
                '', 'Fecha Envío', '', '','OK', '', '', '', '', '','','Extras', 'Aval', 'Estado Aval', 'Fecha Vto. Aval',
                '', 'Ordenes de Cambio', '', '', '', '% Env Fab', 'Notas Técnicas']

        self.tableOrders.setItemDelegate(AlignDelegate(self.tableOrders))
        self.color_delegate = ColorDelegate(self)
        self.tableOrders.setItemDelegateForColumn(4, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(14, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(16, self.color_delegate)
        self.tableOrders.setItemDelegateForColumn(19, self.color_delegate)
        # self.tableOrders.setItemDelegateForColumn(35, self.color_delegate)
        self.tableOrders.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setSectionResizeMode(13, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableOrders.horizontalHeader().setSectionResizeMode(43, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
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

        self.menuValues.setStyleSheet("QMenu::item:selected { background-color: #33bdef; }"
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

        output_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Guardar Excel", "", "Archivos de Excel (*.xlsx)")
        if output_path:
            if not output_path.lower().endswith(".xlsx"):
                output_path += ".xlsx"
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
                        report_offers()
                        break
                    elif report == 'Pedidos':
                        report_orders()
                        break
                break
            else:
                break



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dbparam = config()
    user_database = dbparam["user"]
    password_database = dbparam["password"]

    # Genera un nombre único para la conexión basado en el nombre de usuario y el contador
    db_technical_control = Create_DBconnection(user_database, password_database, 'order_control_technical_connection')

    if not db_technical_control:
        sys.exit()

    Technical_Order_Control_Window = Ui_Technical_Order_Control_Window(db_technical_control,'j.martinez')
    Technical_Order_Control_Window.show()
    sys.exit(app.exec())