from PySide6 import QtCore, QtGui, QtWidgets
from PySide6 import QtSql
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QKeySequence, QTextDocument, QTextCursor
from utils.Database_Manager import Create_DBconnection
from config.config_functions import config_database
import configparser
from datetime import *
import os
import re

basedir = r"\\ERP-EIPSA-DATOS\Comunes\EIPSA-ERP"

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
    def paint(self, painter, option, index: QtCore.QModelIndex):
        """
        Paints the background color of the item based on its column and value.

        Args:
            painter (QtGui.QPainter): The painter used for painting.
            option (QtWidgets.QStyleOptionViewItem): The style option for the item.
            index (QtCore.QModelIndex): The model index of the item.
        """
        value = index.model().data(index, role=Qt.ItemDataRole.DisplayRole)
        # if index.column() == 16 and value <= 50 and value >= 1:
        #     background_color = QtGui.QColor(255, 255, 0) #Yellow
        # elif index.column() == 16 and value < 100  and value > 50:
        #     background_color = QtGui.QColor(0, 255, 0) #Green
        # elif index.column() == 16 and value == 100:
        #     background_color = QtGui.QColor(0, 102, 204) #Blue
        # else:
        #     background_color = QtGui.QColor(255, 255, 255) #White

        # painter.fillRect(option.rect, background_color)
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
        Apply a filter expression to a specific column, or remove it if necessary.

        Args:
            expresion (str): The filter expression.
            column (int): The index of the column to apply the filter to.
            action_name (str, optional): Name of the action, can be empty. Defaults to None.
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
                if expresion == '':  # Si la expresión es vacía, coincidir con celdas vacías
                    if text == '':
                        break

                elif re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', expresion):
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
        self._modified_rows = set()
        self.column_range = column_range

    def setData(self, index, value, role=QtCore.Qt.ItemDataRole.EditRole):
        if role == QtCore.Qt.ItemDataRole.EditRole:
            current_value = self.data(index, role)
            if current_value != value:
                success = super().setData(index, value, role)
                if success:
                    self._modified_rows.add(index.row())
                return success
        return super().setData(index, value, role)

    def getModifiedRows(self):
        return list(self._modified_rows)

    def clearModifiedRows(self):
        self._modified_rows.clear()

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
        if index.column() < 10:
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

class Ui_Dispatch_Window(QtWidgets.QMainWindow):
    """
    A window for editing technical tags in the application.

    Attributes:
        model (EditableTableModel): The data model for the table.
        proxy (CustomProxyModel): The proxy model for filtering and sorting.
        db (object): Database connection.
        checkbox_states (dict): States of checkboxes.
        dict_valuesuniques (dict): Unique values for columns.
        dict_ordersort (dict): Sorting order for columns.
        hiddencolumns (list): List of hidden column indices.
        action_checkbox_map (dict): Map of actions to checkboxes.
        checkbox_filters (dict): Filters based on checkbox states.
    """
    def __init__(self, db):
        """
        Initializes the Ui_EditTags_Technical_Window with the specified name and database connection.

        Args:
            db (object): Database connection.
        """
        super().__init__()
        self._saving1 = False
        self.model = EditableTableModel()
        self.proxy = CustomProxyModel()
        self.checkbox_states = {}
        self.dict_valuesuniques = {}
        self.dict_ordersort = {}
        self.action_checkbox_map = {}
        self.checkbox_filters = {}
        self.db = db
        self.model.dataChanged.connect(self.saveChanges)
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
        self.tableDispatch.setModel(None)
        del self.model
        if self.db:
            self.db.close()
            del self.db
            if QtSql.QSqlDatabase.contains("qt_sql_default_connection"):
                QtSql.QSqlDatabase.removeDatabase("qt_sql_default_connection")

    def setupUi(self, Dispatch_Window):
        """
        Sets up the user interface for the Dispatch_Window.

        Args:
            Dispatch_Window (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        self.id_list = []
        data_list = []
        Dispatch_Window.setObjectName("Dispatch_Window")
        Dispatch_Window.resize(400, 561)
        Dispatch_Window.setMinimumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Dispatch_Window.setWindowIcon(icon)
        Dispatch_Window.setStyleSheet(
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
        self.centralwidget = QtWidgets.QWidget(parent=Dispatch_Window)
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
        self.toolDeleteFilter = QtWidgets.QToolButton(self.frame)
        self.toolDeleteFilter.setObjectName("DeleteFilter_Button")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Filter_Delete.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolDeleteFilter.setIcon(icon)
        self.toolDeleteFilter.setIconSize(QtCore.QSize(25, 25))
        self.hcab.addWidget(self.toolDeleteFilter)
        self.hcabspacer2=QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hcab.addItem(self.hcabspacer2)
        self.toolDispatchQuery = QtWidgets.QToolButton(self.frame)
        self.toolDispatchQuery.setObjectName("DispatchQuery_Button")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Table.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolDispatchQuery.setIcon(icon2)
        self.toolDispatchQuery.setIconSize(QtCore.QSize(25, 25))
        self.hcab.addWidget(self.toolDispatchQuery)
        self.hcabspacer=QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hcab.addItem(self.hcabspacer)
        self.gridLayout_2.addLayout(self.hcab, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem2, 1, 0, 1, 1)
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setObjectName("hLayout")
        self.Button_All = QtWidgets.QPushButton(parent=self.frame)
        self.Button_All.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_All.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_All.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_All.setObjectName("Button_All")
        self.hLayout.addWidget(self.Button_All)
        self.gridLayout_2.addLayout(self.hLayout, 2, 0, 1, 1)
        self.tableDispatch=QtWidgets.QTableView(parent=self.frame)
        self.model = EditableTableModel()
        self.tableDispatch.setObjectName("tableDispatch")
        self.gridLayout_2.addWidget(self.tableDispatch, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        Dispatch_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Dispatch_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        Dispatch_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Dispatch_Window)
        self.statusbar.setObjectName("statusbar")
        Dispatch_Window.setStatusBar(self.statusbar)
        self.tableDispatch.setSortingEnabled(True)
        self.tableDispatch.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        # Dispatch_Window.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.retranslateUi(Dispatch_Window)
        QtCore.QMetaObject.connectSlotsByName(Dispatch_Window)

        self.model.setTable("purch_fact.invoice_header")
        self.model.setFilter("date_dispatch IS NULL")
        self.model.setSort(1, QtCore.Qt.SortOrder.DescendingOrder)
        self.model.select()

        self.proxy.setSourceModel(self.model)
        self.tableDispatch.setModel(self.proxy)

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

        self.tableDispatch.hideColumn(0)
        self.tableDispatch.hideColumn(1)
        for i in range(3,5):
            self.tableDispatch.hideColumn(i)
        for i in range(6,52):
            self.tableDispatch.hideColumn(i)
        self.tableDispatch.hideColumn(58)
        self.tableDispatch.hideColumn(59)
        self.tableDispatch.hideColumn(60)

        headers=['ID', 'Nº Factura', 'Nº Albarán', '', '', 'Nº Pedido', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '',
                '', '', 'Destino', 'Bultos', 'Peso', 'Descripción', 'Transporte', 'Fecha', '', '', '']

        self.tableDispatch.setItemDelegate(AlignDelegate(self.tableDispatch))
        # self.color_delegate = ColorDelegate(self)
        # self.tableDispatch.setItemDelegateForColumn(16, self.color_delegate)
        # self.tableDispatch.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableDispatch.horizontalHeader().setDefaultSectionSize(50)
        self.tableDispatch.horizontalHeader().resizeSection(5, 125)
        self.tableDispatch.horizontalHeader().resizeSection(52, 175)
        self.tableDispatch.horizontalHeader().resizeSection(53, 50)
        self.tableDispatch.horizontalHeader().resizeSection(54, 125)
        self.tableDispatch.horizontalHeader().resizeSection(55, 600)
        self.tableDispatch.horizontalHeader().resizeSection(56, 75)
        self.tableDispatch.horizontalHeader().resizeSection(57, 75)
        # self.tableDispatch.horizontalHeader().setSectionResizeMode(52, QtWidgets.QHeaderView.ResizeMode.Interactive)
        # self.tableDispatch.horizontalHeader().setSectionResizeMode(55, QtWidgets.QHeaderView.ResizeMode.Interactive)
        # self.tableDispatch.horizontalHeader().setSectionResizeMode(57, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.tableDispatch.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid;}")
        self.gridLayout_2.addWidget(self.tableDispatch, 3, 0, 1, 1)

        self.model.setAllColumnHeaders(headers)

        self.toolDeleteFilter.clicked.connect(self.delete_allFilters)
        self.toolDispatchQuery.clicked.connect(self.query_all_Dispatch)
        self.Button_All.clicked.connect(self.see_all_Dispatch_editable)
        self.tableDispatch.setSortingEnabled(False)
        self.tableDispatch.horizontalHeader().sectionClicked.connect(lambda logicalIndex: self.on_view_horizontalHeader_sectionClicked(logicalIndex, self.tableDispatch, self.model, self.proxy))
        self.model.dataChanged.connect(self.saveChanges)

        self.tableDispatch.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableDispatch, self.model, self.proxy)


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, Dispatch_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        Dispatch_Window.setWindowTitle(_translate("EditTags_Window", "Despachos"))
        self.Button_All.setText(_translate("EditTags_Window", "Ver Todos"))

# Function to load all dispatch in new window
    def query_all_Dispatch(self):
        """
        Opens the dispatch table window.
        """
        from windows.Dispatch_Query_Window import Ui_Dispatch_Query_Window
        self.dispatch_query_window = QtWidgets.QMainWindow()
        self.ui = Ui_Dispatch_Query_Window()
        self.ui.setupUi(self.dispatch_query_window)
        self.dispatch_query_window.show()

# Function to load all dispatch in editable table
    def see_all_Dispatch_editable(self):
        """
        Queries the database for all orders, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model.dataChanged.disconnect(self.saveChanges)
        self.delete_allFilters()
        self.model.clear()
        self.model.setTable("purch_fact.invoice_header")
        current_year = int(QtCore.QDate.currentDate().year())
        self.model.setFilter(f"(EXTRACT(YEAR FROM date_invoice) = {current_year} OR EXTRACT(YEAR FROM date_invoice) = {current_year - 1} )")
        self.model.setSort(1, QtCore.Qt.SortOrder.DescendingOrder)
        self.model.select()

        self.proxy.setSourceModel(self.model)
        self.tableDispatch.setModel(self.proxy)

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

        self.tableDispatch.hideColumn(0)
        self.tableDispatch.hideColumn(1)
        for i in range(3,5):
            self.tableDispatch.hideColumn(i)
        for i in range(6,52):
            self.tableDispatch.hideColumn(i)
        self.tableDispatch.hideColumn(58)
        self.tableDispatch.hideColumn(59)
        self.tableDispatch.hideColumn(60)

        headers=['ID', 'Nº Factura', 'Nº Albarán', '', '', 'Nº Pedido', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '',
                '', '', '', '', '', '', '', '', '', '',
                '', '', 'Destino', 'Bultos', 'Peso', 'Descripción', 'Transporte', 'Fecha', '', '', '']

        self.tableDispatch.setItemDelegate(AlignDelegate(self.tableDispatch))
        # self.color_delegate = ColorDelegate(self)
        # self.tableDispatch.setItemDelegateForColumn(16, self.color_delegate)
        # self.tableDispatch.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableDispatch.horizontalHeader().setDefaultSectionSize(50)
        self.tableDispatch.horizontalHeader().resizeSection(5, 125)
        self.tableDispatch.horizontalHeader().resizeSection(52, 175)
        self.tableDispatch.horizontalHeader().resizeSection(54, 125)
        self.tableDispatch.horizontalHeader().resizeSection(55, 300)
        self.tableDispatch.horizontalHeader().resizeSection(56, 100)
        self.tableDispatch.horizontalHeader().resizeSection(57, 100)
        # self.tableDispatch.horizontalHeader().setSectionResizeMode(52, QtWidgets.QHeaderView.ResizeMode.Interactive)
        # self.tableDispatch.horizontalHeader().setSectionResizeMode(55, QtWidgets.QHeaderView.ResizeMode.Interactive)
        # self.tableDispatch.horizontalHeader().setSectionResizeMode(57, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableDispatch.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid;}")
        self.gridLayout_2.addWidget(self.tableDispatch, 3, 0, 1, 1)

        self.model.setAllColumnHeaders(headers)
        self.model.dataChanged.connect(self.saveChanges)

        self.tableDispatch.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableDispatch, self.model, self.proxy)

# Function to delete all filters when tool button is clicked
    def delete_allFilters(self):
        """
        Resets all filters and updates the table model with unique values for each column.
        """
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
        self.tableDispatch.setModel(None)
        self.tableDispatch.setModel(self.proxy)

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
    def saveChanges(self): #, topLeft, bottomRight):
        """
        Saves changes made to the data models and updates unique values for each column.
        """
        self.model.submitAll()

        # if topLeft == bottomRight:
        #     index = topLeft  # Obtiene el índice de la celda modificada


        #     if index.isValid():
        #         current_value = self.tableDispatch.model().mapToSource(index).data()  # Valor actual desde el modelo fuente
        #         new_value = self.model.data(index, Qt.ItemDataRole.EditRole)

        #         print(current_value, new_value)

        #         if current_value != new_value:  # Compara el valor actual con el nuevo
        #             # Establece el nuevo valor en la celda
        #             if self.model.setData(index, new_value):
        #                 # Solo llama a submit() si el valor se estableció correctamente
        #                 if self.model.submit():  # Usa submit() solo para esta celda
        #                     print("Cambios guardados exitosamente.")
        #                 else:
        #                     print('a')
        #             else:
        #                 print('b')
        #         else:
        #             print('c')
        #     else:
        #         print('d')

        if self._saving1:
            return  # Avoid recursive entries
        self._saving1 = True

        db = self.model.database()
        db.transaction()

        success = True
        for row in self.model.getModifiedRows():
            if not self.model.submit():
                print(f"❌ Error guardando fila {row}: {self.model.lastError().text()}")
                success = False

        if success:
            db.commit()

            for row in self.model.getModifiedRows():
                top_left = self.model.index(row, 0)
                bottom_right = self.model.index(row, self.model.columnCount() - 1)
                self.model.dataChanged.emit(top_left, bottom_right)
        else:
            db.rollback()

        self.model.clearModifiedRows()
        
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

# Function when header is clicked
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex, table, model, proxy):
        """
        Displays a menu when a column header is clicked. The menu includes options for sorting, filtering, and managing column visibility.
        
        Args:
            logicalIndex (int): Index of the clicked column.
            table (QtWidgets.QTableView): The table view displaying the data.
            model (QtGui.QStandardItemModel): The model associated with the table.
            proxy (QtCore.QSortFilterProxyModel): The proxy model used for filtering and sorting.
        """

        self.logicalIndex = logicalIndex
        self.menuValues = QtWidgets.QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(table)

        valuesUnique_view = {table.model().index(row, self.logicalIndex).data(Qt.ItemDataRole.DisplayRole) for row in range(table.model().rowCount())}
        valuesUnique_view = [value.toString("dd/MM/yyyy") if isinstance(value, QtCore.QDate) else value for value in valuesUnique_view]

        actionSortAscending = QtGui.QAction("Ordenar Ascendente", table)
        actionSortAscending.triggered.connect(lambda: self.on_actionSortAscending_triggered(table))
        self.menuValues.addAction(actionSortAscending)
        actionSortDescending = QtGui.QAction("Ordenar Descendente", table)
        actionSortDescending.triggered.connect(lambda: self.on_actionSortDescending_triggered(table))
        self.menuValues.addAction(actionSortDescending)
        self.menuValues.addSeparator()

        actionDeleteFilterColumn = QtGui.QAction("Quitar Filtro", table)
        actionDeleteFilterColumn.triggered.connect(lambda: self.on_actionDeleteFilterColumn_triggered(table, model, proxy))
        self.menuValues.addAction(actionDeleteFilterColumn)
        self.menuValues.addSeparator()

        actionTextFilter = QtGui.QAction("Buscar...", table)
        actionTextFilter.triggered.connect(lambda: self.on_actionTextFilter_triggered(model, proxy))
        self.menuValues.addAction(actionTextFilter)
        # self.menuValues.addSeparator()

        # scroll_menu = QtWidgets.QScrollArea()
        # scroll_menu.setStyleSheet("background-color: rgb(255, 255, 255)")
        # scroll_menu.setWidgetResizable(True)
        # scroll_widget = QtWidgets.QWidget(scroll_menu)
        # scroll_menu.setWidget(scroll_widget)
        # scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

        # checkbox_all_widget = QtWidgets.QCheckBox('Seleccionar todo')

        # if not self.checkbox_states[self.logicalIndex]['Seleccionar todo'] == True:
        #     checkbox_all_widget.setChecked(False)
        # else:
        #     checkbox_all_widget.setChecked(True)
        
        # checkbox_all_widget.toggled.connect(lambda checked, name='Seleccionar todo': self.on_select_all_toggled(checked, name, model))

        # scroll_layout.addWidget(checkbox_all_widget)
        # self.action_checkbox_map['Seleccionar todo'] = checkbox_all_widget

        # if len(self.dict_ordersort) != 0 and self.logicalIndex in self.dict_ordersort:
        #     list_uniquevalues = sorted(list(set(self.dict_valuesuniques[self.logicalIndex])))
        # else:
        #     list_uniquevalues = sorted(list(set(valuesUnique_view)))

        # for actionName in list_uniquevalues:
        #     checkbox_widget = QtWidgets.QCheckBox(str(actionName))

        #     if self.logicalIndex not in self.checkbox_filters:
        #         checkbox_widget.setChecked(True)
        #     elif actionName not in self.checkbox_filters[self.logicalIndex]:
        #         checkbox_widget.setChecked(False)
        #     else:
        #         checkbox_widget.setChecked(True)

        #     checkbox_widget.toggled.connect(lambda checked, name=actionName: self.on_checkbox_toggled(checked, name, model))

        #     scroll_layout.addWidget(checkbox_widget)
        #     self.action_checkbox_map[actionName] = checkbox_widget

        # action_scroll_menu = QtWidgets.QWidgetAction(self.menuValues)
        # action_scroll_menu.setDefaultWidget(scroll_menu)
        # self.menuValues.addAction(action_scroll_menu)

        # self.menuValues.addSeparator()

        # accept_button = QtGui.QAction("ACEPTAR", table)
        # accept_button.triggered.connect(lambda: self.menu_acceptbutton_triggered(proxy))

        # cancel_button = QtGui.QAction("CANCELAR", table)
        # cancel_button.triggered.connect(self.menu_cancelbutton_triggered)

        # self.menuValues.addAction(accept_button)
        # self.menuValues.addAction(cancel_button)

        self.menuValues.setStyleSheet("QMenu::item:selected { background-color: #33bdef; }"
                                        "QMenu::item:pressed { background-color: rgb(1, 140, 190); }")

        headerPos = table.mapToGlobal(table.horizontalHeader().pos())        

        posY = headerPos.y() + table.horizontalHeader().height()
        scrollX = table.horizontalScrollBar().value()
        xInView = table.horizontalHeader().sectionViewportPosition(logicalIndex)
        posX = headerPos.x() + xInView - scrollX

        self.menuValues.exec(QtCore.QPoint(posX, posY))

# Function when cancel button of menu is clicked
    def menu_cancelbutton_triggered(self):
        """
        Hides the menu when the cancel button is clicked.
        """
        self.menuValues.hide()

# Function when accept button of menu is clicked
    def menu_acceptbutton_triggered(self, proxy):
        """
        Applies the selected filters and updates the table model with the new filters.
        """
        for column, filters in self.checkbox_filters.items():
            if filters:
                proxy.setFilter(filters, column, exact_match=True)
            else:
                proxy.setFilter(None, column)

# Function when select all checkbox is clicked
    def on_select_all_toggled(self, checked, action_name, model):
        """
        Toggles the state of all checkboxes in the filter menu when the 'Select All' checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the 'Select All' checkbox.
            action_name (str): The name of the action (usually 'Select All').
            model (QAbstractItemModel): The model associated with the table view.
        """
        filterColumn = self.logicalIndex

    # Load icon
        if not hasattr(self, 'icono_filter_active'):
            imagen_path = os.path.abspath(os.path.join(basedir, "Resources/Iconos/Filter_Active.png"))
            self.icono_filter_active = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))
        
    # Select map and state related to model
        checkbox_map = self.action_checkbox_map
        checkbox_states = self.checkbox_states

    # Change state of checkboxes if necessary
        for checkbox_name, checkbox_widget in checkbox_map.items():
            if checkbox_widget.isChecked() != checked:
                checkbox_widget.setChecked(checked)
                checkbox_states[self.logicalIndex][checkbox_widget.text()] = checked

    # Adjust icon of header
        all_checked = all(checkbox_widget.isChecked() for checkbox_widget in checkbox_map.values())
        model.setIconColumnHeader(filterColumn, self.icono_filter_active if all_checked else '')

# Function when checkbox of header menu is clicked
    def on_checkbox_toggled(self, checked, action_name, model):
        """
        Updates the filter state when an individual checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the checkbox.
            action_name (str): The name of the checkbox.
        """
        filterColumn = self.logicalIndex
        imagen_path = os.path.abspath(os.path.join(basedir, "Resources/Iconos/Filter_Active.png"))
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
            model.setIconColumnHeader(filterColumn, '')
        else:
            model.setIconColumnHeader(filterColumn, icono)

# Function to delete individual column filter
    def on_actionDeleteFilterColumn_triggered(self, table, model, proxy):
        """
        Removes the filter from the selected column and updates the table model.
        
        Args:
            table (QtWidgets.QTableView): The table view displaying the data.
            model (QtGui.QStandardItemModel): The model associated with the table.
            proxy (QtCore.QSortFilterProxyModel): The proxy model used for filtering and sorting.
        """
        filterColumn = self.logicalIndex
        if filterColumn in proxy.filters:
            del proxy.filters[filterColumn]
        model.setIconColumnHeader(filterColumn, "")
        proxy.invalidateFilter()

        if filterColumn in self.checkbox_filters:
            del self.checkbox_filters[filterColumn]

        self.checkbox_states[self.logicalIndex].clear()
        self.checkbox_states[self.logicalIndex]["Seleccionar todo"] = True
        for row in range(table.model().rowCount()):
            value = model.record(row).value(filterColumn)
            if isinstance(value, QtCore.QDate):
                value = value.toString("dd/MM/yyyy")
            self.checkbox_states[self.logicalIndex][str(value)] = True

# Function to order column ascending
    def on_actionSortAscending_triggered(self, table):
        """
        Sorts the selected column in ascending order.
        
        Args:
            table (QtWidgets.QTableView): The table view displaying the data.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.AscendingOrder
        table.sortByColumn(sortColumn, sortOrder)

# Function to order column descending
    def on_actionSortDescending_triggered(self, table):
        """
        Sorts the selected column in descending order.
        
        Args:
            table (QtWidgets.QTableView): The table view displaying the data.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.DescendingOrder
        table.sortByColumn(sortColumn, sortOrder)

# Function when text is searched
    def on_actionTextFilter_triggered(self, model, proxy):
        """
        Opens a dialog to enter a text filter and applies it to the selected column.
        
        Args:
            model (QtGui.QStandardItemModel): The model associated with the table.
            proxy (QtCore.QSortFilterProxyModel): The proxy model used for filtering and sorting.
        """
        filterColumn = self.logicalIndex
        dlg = QtWidgets.QInputDialog()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle("Buscar")
        clickedButton = dlg.exec()

        if clickedButton == 1:
            stringAction = dlg.textValue()
            if re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', stringAction):
                stringAction=QtCore.QDate.fromString(stringAction,"dd/MM/yyyy")
                stringAction=stringAction.toString("yyyy-MM-dd")

            filterString = QtCore.QRegularExpression(stringAction, QtCore.QRegularExpression.PatternOption(0))
            # del self.proxy.filters[filterColumn]
            proxy.setFilter([stringAction], filterColumn, None)

            imagen_path = os.path.abspath(os.path.join(basedir, "Resources/Iconos/Filter_Active.png"))
            icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))
            model.setIconColumnHeader(filterColumn, icono)

# Function to get the text of the selected cells
    def get_selected_text(self, indexes):
        """
        Retrieves the text from the selected cells and returns it as a plain text string.

        Args:
            indexes (list of QModelIndex): A list of QModelIndex objects representing the selected cells.
        
        Returns:
            str: A string containing the text from the selected cells.
        """
        """
        Retrieves the text from the selected cells and returns it as a plain text string.

        Args:
            indexes (list of QModelIndex): A list of QModelIndex objects representing the selected cells.
        
        Returns:
            str: A string containing the text from the selected cells.
        """
        if len(indexes) == 1: # For only one cell selected
            index = indexes[0]
            cell_data = index.data(Qt.ItemDataRole.DisplayRole)
            return cell_data
        else:
            rows = set()
            cols = set()
            for index in indexes:
                rows.add(index.row())
                cols.add(index.column())

            text_doc = QTextDocument()
            cursor = QTextCursor(text_doc)

            for row in sorted(rows):
                for col in sorted(cols):
                    index = self.model.index(row, col)  # Obtain corresponding index
                    cell_data = index.data(Qt.ItemDataRole.DisplayRole)
                    cursor.insertText(str(cell_data))
                    cursor.insertText('\t')  # Tab separating columns
                cursor.insertText('\n')  # Line break at end of row

            return text_doc.toPlainText()

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

        elif event.matches(QKeySequence.StandardKey.Copy):
            selected_indexes = table.selectionModel().selectedIndexes()
            if not selected_indexes:
                return

            mime_data = QtCore.QMimeData()
            data = bytearray()

            if isinstance(model, QtCore.QSortFilterProxyModel):
                for index in selected_indexes:
                    source_index = proxy.mapToSource(index)
                    data += str(model.sourceModel().data(source_index)).encode('utf-8') + b'\t'
            else:
                for index in selected_indexes:
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

                if isinstance(model, QtCore.QSortFilterProxyModel):
                    model_indexes = [proxy.mapToSource(index) for index in selected_indexes]
                    if len(values) == 2:
                        for index in model_indexes:
                            model.sourceModel().setData(index, values[0].decode('utf-8'))
                    else:
                        for index, value in zip(model_indexes, values):
                            model.sourceModel().setData(index, value.decode('utf-8'))
                else:
                    model_indexes = selected_indexes
                    if len(values) == 2:
                        for index in model_indexes:
                            model.setData(index, values[0].decode('utf-8'))
                    else:
                        for index, value in zip(model_indexes, values):
                            model.setData(index, value.decode('utf-8'))

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

        elif event.matches(QKeySequence.StandardKey.InsertParagraphSeparator):
            current_index = table.currentIndex()
            if current_index.isValid() and not table.indexWidget(current_index):
                table.edit(current_index)

        super().keyPressEvent(event)



if __name__ == "__main__":
    import sys
    import os

    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    app = QtWidgets.QApplication(sys.argv)
    dbparam = config_database()
    user_database = dbparam["user"]
    password_database = dbparam["password"]

    db = Create_DBconnection(user_database, password_database)
    if not db:
        sys.exit()

    Dispatch_Window = Ui_Dispatch_Window(db)
    Dispatch_Window.show()
    sys.exit(app.exec())