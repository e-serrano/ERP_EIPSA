from PySide6 import QtCore, QtGui, QtWidgets
from PySide6 import QtSql
from PySide6.QtCore import Qt
from utils.Database_Manager import Create_DBconnection
from config import config
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

                # elif re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', expresion):
                #     expresion = QtCore.QDate.fromString(expresion, "dd/MM/yyyy")
                #     expresion = expresion.toString("yyyy-MM-dd")
                #     regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                #     if regex.match(str(text)).hasMatch():
                #         break

                else:
                    regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                    if regex.match(str(text)).hasMatch():
                        break
            else:
                return False
        return True

class Ui_Deliveries_Window(QtWidgets.QMainWindow):
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
        Initializes the Ui_Deliveries_Window with the specified name and database connection.

        Args:
            name (str): Name associated with the window.
            db (object): Database connection.
        """
        super().__init__()
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
        self.tableDeliveries.setModel(None)
        del self.model
        if self.db:
            self.db.close()
            del self.db
            if QtSql.QSqlDatabase.contains("qt_sql_default_connection"):
                QtSql.QSqlDatabase.removeDatabase("qt_sql_default_connection")

    def setupUi(self, Deliveries_Window):
        """
        Sets up the user interface for the Deliveries_Window.

        Args:
            Deliveries_Window (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        self.id_list = []
        data_list = []
        Deliveries_Window.setObjectName("Deliveries_Window")
        Deliveries_Window.resize(400, 561)
        Deliveries_Window.setMinimumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Deliveries_Window.setWindowIcon(icon)
        Deliveries_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=Deliveries_Window)
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
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setObjectName("hLayout")
        self.Button_All = QtWidgets.QPushButton(parent=self.frame)
        self.Button_All.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_All.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_All.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_All.setObjectName("Button_All")
        self.hLayout.addWidget(self.Button_All)
        self.gridLayout_2.addLayout(self.hLayout, 1, 0, 1, 1)
        self.tableDeliveries=QtWidgets.QTableView(parent=self.frame)
        self.model = EditableTableModel()
        self.tableDeliveries.setObjectName("tableDeliveries")
        self.gridLayout_2.addWidget(self.tableDeliveries, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        Deliveries_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Deliveries_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        Deliveries_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Deliveries_Window)
        self.statusbar.setObjectName("statusbar")
        Deliveries_Window.setStatusBar(self.statusbar)
        self.tableDeliveries.setSortingEnabled(True)
        self.tableDeliveries.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        # Deliveries_Window.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.retranslateUi(Deliveries_Window)
        QtCore.QMetaObject.connectSlotsByName(Deliveries_Window)

        self.model.setTable("public.orders")
        self.model.setFilter("num_order NOT LIKE '%R%' AND (porc_deliveries <> 100 OR porc_deliveries IS NULL)")
        self.model.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model.select()
        self.proxy.setSourceModel(self.model)
        self.tableDeliveries.setModel(self.proxy)

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

        for i in range(1,22):
            self.tableDeliveries.hideColumn(i)
        for i in range(26,self.model.columnCount()):
            self.tableDeliveries.hideColumn(i)

        headers=['Nº Pedido', '','','','','','','','','','','','','','','','','','','','','',
                '% Real Envío', 'Fecha Último Envío', 'Fecha Entregas Parciales', 'Observaciones','OK', '', '', '', '','','']

        self.tableDeliveries.setItemDelegate(AlignDelegate(self.tableDeliveries))
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(21,QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(22,QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(23,QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(24,QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(25,QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableDeliveries.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_2.addWidget(self.tableDeliveries, 2, 0, 1, 1)

        self.model.setAllColumnHeaders(headers)

        self.Button_All.clicked.connect(self.query_all_deliveries)
        self.tableDeliveries.setSortingEnabled(False)
        self.tableDeliveries.horizontalHeader().sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked)
        self.model.dataChanged.connect(self.saveChanges)


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, Deliveries_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        Deliveries_Window.setWindowTitle(_translate("Deliveries_Window", "Envíos"))
        self.Button_All.setText(_translate("Deliveries_Window", "Ver Todos"))

# Function to load all P and PA
    def query_all_deliveries(self):
        """
        Queries the database for all orders, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model.dataChanged.disconnect(self.saveChanges)
        self.delete_allFilters()
        self.model.setTable("public.orders")
        self.model.setFilter("num_order NOT LIKE '%R%'")
        self.model.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model.select()
        self.proxy.setSourceModel(self.model)
        self.tableDeliveries.setModel(self.proxy)

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

        for i in range(1,22):
            self.tableDeliveries.hideColumn(i)
        for i in range(26,self.model.columnCount()):
            self.tableDeliveries.hideColumn(i)


        headers=['Nº Pedido', '','','','','','','','','','','','','','','','','','','','','',
                '% Real Envío', 'Fecha Último Envío', 'Fecha Entregas Parciales', 'Observaciones','OK', '', '', '', '','','']

        self.tableDeliveries.setItemDelegate(AlignDelegate(self.tableDeliveries))
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(21,QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(22,QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(23,QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(24,QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(25,QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableDeliveries.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_2.addWidget(self.tableDeliveries, 2, 0, 1, 1)

        self.model.setAllColumnHeaders(headers)
        self.model.dataChanged.connect(self.saveChanges)

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
        self.tableDeliveries.setModel(None)
        self.tableDeliveries.setModel(self.proxy)

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

# Function when header is clicked
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):
        """
        Displays a menu when a column header is clicked. The menu includes options for sorting, filtering, and managing column visibility.
        
        Args:
            logicalIndex (int): Index of the clicked column.
        """
        self.logicalIndex = logicalIndex
        self.menuValues = QtWidgets.QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(self.tableDeliveries)

        valuesUnique_view = []
        for row in range(self.tableDeliveries.model().rowCount()):
            index = self.tableDeliveries.model().index(row, self.logicalIndex)
            value = index.data(Qt.ItemDataRole.DisplayRole)
            if value not in valuesUnique_view:
                if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
                valuesUnique_view.append(value)

        actionSortAscending = QtGui.QAction("Ordenar Ascendente", self.tableDeliveries)
        actionSortAscending.triggered.connect(self.on_actionSortAscending_triggered)
        self.menuValues.addAction(actionSortAscending)
        actionSortDescending = QtGui.QAction("Ordenar Descendente", self.tableDeliveries)
        actionSortDescending.triggered.connect(self.on_actionSortDescending_triggered)
        self.menuValues.addAction(actionSortDescending)
        self.menuValues.addSeparator()

        actionDeleteFilterColumn = QtGui.QAction("Quitar Filtro", self.tableDeliveries)
        actionDeleteFilterColumn.triggered.connect(self.on_actionDeleteFilterColumn_triggered)
        self.menuValues.addAction(actionDeleteFilterColumn)
        self.menuValues.addSeparator()

        actionTextFilter = QtGui.QAction("Buscar...", self.tableDeliveries)
        actionTextFilter.triggered.connect(self.on_actionTextFilter_triggered)
        self.menuValues.addAction(actionTextFilter)
        self.menuValues.addSeparator()

        scroll_menu = QtWidgets.QScrollArea()
        scroll_menu.setStyleSheet("background-color: rgb(255, 255, 255)")
        scroll_menu.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget(scroll_menu)
        scroll_menu.setWidget(scroll_widget)
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

        checkbox_all_widget = QtWidgets.QCheckBox('Seleccionar todo')

        if not self.checkbox_states[self.logicalIndex]['Seleccionar todo'] == True:
            checkbox_all_widget.setChecked(False)
        else:
            checkbox_all_widget.setChecked(True)
        
        checkbox_all_widget.toggled.connect(lambda checked, name='Seleccionar todo': self.on_select_all_toggled(checked, name))

        scroll_layout.addWidget(checkbox_all_widget)
        self.action_checkbox_map['Seleccionar todo'] = checkbox_all_widget

        if len(self.dict_ordersort) != 0 and self.logicalIndex in self.dict_ordersort:
            list_uniquevalues = sorted(list(set(self.dict_valuesuniques[self.logicalIndex])))
        else:
            list_uniquevalues = sorted(list(set(valuesUnique_view)))

        for actionName in list_uniquevalues:
            checkbox_widget = QtWidgets.QCheckBox(str(actionName))

            if self.logicalIndex not in self.checkbox_filters:
                checkbox_widget.setChecked(True)
            elif actionName not in self.checkbox_filters[self.logicalIndex]:
                checkbox_widget.setChecked(False)
            else:
                checkbox_widget.setChecked(True)

            checkbox_widget.toggled.connect(lambda checked, name=actionName: self.on_checkbox_toggled(checked, name))

            scroll_layout.addWidget(checkbox_widget)
            self.action_checkbox_map[actionName] = checkbox_widget

        action_scroll_menu = QtWidgets.QWidgetAction(self.menuValues)
        action_scroll_menu.setDefaultWidget(scroll_menu)
        self.menuValues.addAction(action_scroll_menu)

        self.menuValues.addSeparator()

        accept_button = QtGui.QAction("ACEPTAR", self.tableDeliveries)
        accept_button.triggered.connect(self.menu_acceptbutton_triggered)

        cancel_button = QtGui.QAction("CANCELAR", self.tableDeliveries)
        cancel_button.triggered.connect(self.menu_cancelbutton_triggered)

        self.menuValues.addAction(accept_button)
        self.menuValues.addAction(cancel_button)

        self.menuValues.setStyleSheet("QMenu { color: black; }"
                                        "QMenu { background-color: rgb(255, 255, 255); }"
                                        "QMenu::item:selected { background-color: #33bdef; }"
                                        "QMenu::item:pressed { background-color: rgb(1, 140, 190); }")

        headerPos = self.tableDeliveries.mapToGlobal(self.tableDeliveries.horizontalHeader().pos())        

        posY = headerPos.y() + self.tableDeliveries.horizontalHeader().height()
        scrollX = self.tableDeliveries.horizontalScrollBar().value()
        xInView = self.tableDeliveries.horizontalHeader().sectionViewportPosition(logicalIndex)
        posX = headerPos.x() + xInView - scrollX

        self.menuValues.exec(QtCore.QPoint(posX, posY))

# Function when cancel button of menu is clicked
    def menu_cancelbutton_triggered(self):
        """
        Hides the menu when the cancel button is clicked.
        """
        self.menuValues.hide()

# Function when accept button of menu is clicked
    def menu_acceptbutton_triggered(self):
        """
        Applies the selected filters and updates the table model with the new filters.
        """
        for column, filters in self.checkbox_filters.items():
            if filters:
                self.proxy.setFilter(filters, column)
            else:
                self.proxy.setFilter(None, column)

# Function when select all checkbox is clicked
    def on_select_all_toggled(self, checked, action_name):
        """
        Toggles the state of all checkboxes in the filter menu when the 'Select All' checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the 'Select All' checkbox.
            action_name (str): The name of the action (usually 'Select All').
        """
        filterColumn = self.logicalIndex
        imagen_path = os.path.abspath(os.path.join(basedir, "Resources/Iconos/Filter_Active.png"))
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

# Function when checkbox of header menu is clicked
    def on_checkbox_toggled(self, checked, action_name):
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
            self.model.setIconColumnHeader(filterColumn, '')
        else:
            self.model.setIconColumnHeader(filterColumn, icono)

# Function to delete individual column filter
    def on_actionDeleteFilterColumn_triggered(self):
        """
        Removes the filter from the selected column and updates the table model.
        """
        filterColumn = self.logicalIndex
        if filterColumn in self.proxy.filters:
            del self.proxy.filters[filterColumn]
        self.model.setIconColumnHeader(filterColumn, '')
        self.proxy.invalidateFilter()

        # self.tableDeliveries.setModel(None)
        self.tableDeliveries.setModel(self.proxy)

        if filterColumn in self.checkbox_filters:
            del self.checkbox_filters[filterColumn]

        self.checkbox_states[self.logicalIndex].clear()
        self.checkbox_states[self.logicalIndex]['Seleccionar todo'] = True
        for row in range(self.tableDeliveries.model().rowCount()):
            value = self.model.record(row).value(filterColumn)
            if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
            self.checkbox_states[self.logicalIndex][str(value)] = True

# Function to order column ascending
    def on_actionSortAscending_triggered(self):
        """
        Sorts the selected column in ascending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.AscendingOrder
        self.tableDeliveries.sortByColumn(sortColumn, sortOrder)

# Function to order column descending
    def on_actionSortDescending_triggered(self):
        """
        Sorts the selected column in descending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.DescendingOrder
        self.tableDeliveries.sortByColumn(sortColumn, sortOrder)

# Function when text is searched
    def on_actionTextFilter_triggered(self):
        """
        Opens a dialog to enter a text filter and applies it to the selected column.
        """
        filterColumn = self.logicalIndex
        dlg = QtWidgets.QInputDialog()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
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
            self.proxy.setFilter([stringAction], filterColumn, None)

            imagen_path = os.path.abspath(os.path.join(basedir, "Resources/Iconos/Filter_Active.png"))
            icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))
            self.model.setIconColumnHeader(filterColumn, icono)






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dbparam = config()
    user_database = dbparam["user"]
    password_database = dbparam["password"]

    db = Create_DBconnection(user_database, password_database)
    if not db:
        sys.exit()

    Deliveries_Window = Ui_Deliveries_Window(db)
    Deliveries_Window.show()
    sys.exit(app.exec())