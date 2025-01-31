# Form implementation generated from reading ui file 'QueryInvoice_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import re
from PyQt6 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config
import os
from datetime import *
import configparser
from Database_Connection import createConnection
import locale

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


class CustomTableWidget(QtWidgets.QTableWidget):
    """
    Custom QTableWidget that supports filtering and sorting features.

    Attributes:
        list_filters (list): Stores filters applied to the table.
        column_filters (dict): Maps column indices to sets of applied filters.
        column_actions (dict): Maps column indices to actions related to columns.
        checkbox_states (dict): Stores the state of checkboxes for filtering.
        rows_hidden (dict): Maps column indices to sets of hidden row indices.
        general_rows_to_hide (set): Set of row indices that are hidden across the table.
    """
    def __init__(self, parent=None):
        """
        Initializes the CustomTableWidget.

        Sets up the initial state of the widget, including filters, checkbox states, 
        and hidden rows.

        Args:
            parent (QWidget, optional): The parent widget of this table. Defaults to None.
        """
        super().__init__(parent)
        self.list_filters=[]
        self.column_filters = {}
        self.column_actions = {}
        self.checkbox_states = {}
        self.rows_hidden = {}
        self.general_rows_to_hide = set()

# Function to show the menu
    def show_unique_values_menu(self, column_index, header_pos, header_height):
        """
        Displays a context menu for unique values in a specified column.

        The menu includes options to remove filters, sort the column, and filter by text. 
        It also allows the user to select/unselect unique values via checkboxes.

        Args:
            column_index (int): The index of the column for which the menu is displayed.
            header_pos (QPoint): The position of the header in the viewport.
            header_height (int): The height of the header.
        """
        menu = QtWidgets.QMenu(self)
        actionDeleteFilterColumn = QtGui.QAction("Quitar Filtro")
        actionDeleteFilterColumn.triggered.connect(lambda: self.delete_filter(column_index))
        menu.addAction(actionDeleteFilterColumn)
        menu.addSeparator()
        actionOrderAsc = menu.addAction("Ordenar Ascendente")
        actionOrderAsc.triggered.connect(lambda: self.sort_column(column_index, QtCore.Qt.SortOrder.AscendingOrder))
        actionOrderDesc = menu.addAction("Ordenar Descendente")
        actionOrderDesc.triggered.connect(lambda: self.sort_column(column_index, QtCore.Qt.SortOrder.DescendingOrder))
        menu.addSeparator()
        actionFilterByText = menu.addAction("Buscar Texto")
        actionFilterByText.triggered.connect(lambda: self.filter_by_text(column_index))
        menu.addSeparator()

        menu.setStyleSheet("QMenu { color: black; }"
                        "QMenu::item:selected { background-color: #33bdef; }"
                        "QMenu::item:pressed { background-color: rgb(1, 140, 190); }")

        if column_index not in self.column_filters:
            self.column_filters[column_index] = set()

        scroll_menu = QtWidgets.QScrollArea()
        scroll_menu.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget(scroll_menu)
        scroll_menu.setWidget(scroll_widget)
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

        checkboxes = []

        select_all_checkbox = QtWidgets.QCheckBox("Seleccionar todo")
        if column_index in self.checkbox_states:
            select_all_checkbox.setCheckState(QtCore.Qt.CheckState(self.checkbox_states[column_index].get("Seleccionar todo", QtCore.Qt.CheckState(2))))
        else:
            select_all_checkbox.setCheckState(QtCore.Qt.CheckState(2))
        scroll_layout.addWidget(select_all_checkbox)
        checkboxes.append(select_all_checkbox)

        unique_values = self.get_unique_values(column_index)
        filtered_values = self.get_filtered_values()

        for value in sorted(unique_values):
            checkbox = QtWidgets.QCheckBox(value)
            if select_all_checkbox.isChecked(): 
                checkbox.setCheckState(QtCore.Qt.CheckState(2))
            else:
                if column_index in self.checkbox_states and value in self.checkbox_states[column_index]:
                    checkbox.setCheckState(QtCore.Qt.CheckState(self.checkbox_states[column_index][value]))
                elif filtered_values is None or value in filtered_values[column_index]:
                    checkbox.setCheckState(QtCore.Qt.CheckState(2))
                else:
                    checkbox.setCheckState(QtCore.Qt.CheckState(0))
            scroll_layout.addWidget(checkbox)
            checkboxes.append(checkbox)

        select_all_checkbox.stateChanged.connect(lambda state: self.set_all_checkboxes_state(checkboxes, state, column_index))

        for value, checkbox in zip(sorted(unique_values), checkboxes[1:]):
            checkbox.stateChanged.connect(lambda checked, value=value, checkbox=checkbox: self.apply_filter(column_index, value, checked))

    # Action for drop down menu and adding scroll area as widget
        action_scroll_menu = QtWidgets.QWidgetAction(menu)
        action_scroll_menu.setDefaultWidget(scroll_menu)
        menu.addAction(action_scroll_menu)

        menu.exec(header_pos - QtCore.QPoint(0, header_height))

# Function to delete filter on selected column
    def delete_filter(self,column_index):
        """
        Removes the filter applied to the specified column.

        Unhides previously hidden rows and resets the checkbox state for the column.

        Args:
            column_index (int): The index of the column from which to delete the filter.
        """
        if column_index in self.column_filters:
            del self.column_filters[column_index]
        if column_index in self.checkbox_states:
            del self.checkbox_states[column_index]
        if column_index in self.rows_hidden:
            for item in self.rows_hidden[column_index]:
                self.setRowHidden(item, False)
                if item in self.general_rows_to_hide:
                    self.general_rows_to_hide.remove(item)
            del self.rows_hidden[column_index]
        header_item = self.horizontalHeaderItem(column_index)
        header_item.setIcon(QtGui.QIcon())

# Function to set all checkboxes state
    def set_all_checkboxes_state(self, checkboxes, state, column_index):
        """
        Sets the state of all checkboxes in the filter menu for a specific column.

        Args:
            checkboxes (list): List of checkboxes to update.
            state (Qt.CheckState): The desired state for the checkboxes.
            column_index (int): The index of the column for which the checkboxes are set.
        """
        if column_index not in self.checkbox_states:
            self.checkbox_states[column_index] = {}

        for checkbox in checkboxes:
            checkbox.setCheckState(QtCore.Qt.CheckState(state))

        self.checkbox_states[column_index]["Seleccionar todo"] = state

# Function to apply filters to table
    def apply_filter(self, column_index, value, checked, text_filter=None, filter_dialog=None):
        """
        Applies a filter to the specified column based on the checkbox state and optional text filter.

        Args:
            column_index (int): The index of the column to filter.
            value (str): The value to filter by.
            checked (bool): Indicates if the filter should be applied (True) or removed (False).
            text_filter (str, optional): Additional text filter for filtering items. Defaults to None.
            filter_dialog (QDialog, optional): The dialog used for the text filter. Defaults to None.
        """
        if column_index not in self.column_filters:
            self.column_filters[column_index] = set()

        if text_filter is None:
            if value is None:
                self.column_filters[column_index] = set()
            elif checked:
                self.column_filters[column_index].add(value)
            elif value in self.column_filters[column_index]:
                self.column_filters[column_index].remove(value)

        rows_to_hide = set()
        for row in range(self.rowCount()):
            show_row = True

            # Check filters for all columns
            for col, filters in self.column_filters.items():
                item = self.item(row, col)
                if item:
                    item_value = item.text()
                    if text_filter is None:
                        if filters and item_value not in filters:
                            show_row = False
                            break

        # Filtering by text
            if text_filter is not None:
                filter_dialog.accept()
                item = self.item(row, column_index)
                if item:
                    if text_filter.upper() in item.text().upper():
                        self.column_filters[column_index].add(item.text())
                    else:
                        show_row = False

            if not show_row:
                if row not in self.general_rows_to_hide:
                    self.general_rows_to_hide.add(row)
                    rows_to_hide.add(row)
            else:
                if row in self.general_rows_to_hide:
                    self.general_rows_to_hide.remove(row)

        # Update hidden rows for this column depending on checkboxes
        if checked and text_filter is None:
            if column_index not in self.rows_hidden:
                self.rows_hidden[column_index] = set(rows_to_hide)
            else:
                self.rows_hidden[column_index].update(rows_to_hide)

        # Update hidden rows for this column depending on filtered text
        if text_filter is not None and value is None:
            if column_index not in self.rows_hidden:
                self.rows_hidden[column_index] = set(rows_to_hide)
            else:
                self.rows_hidden[column_index].update(rows_to_hide)

        # Iterate over all rows to hide them as necessary
        for row in range(self.rowCount()):
            self.setRowHidden(row, row in self.general_rows_to_hide)

        header_item = self.horizontalHeaderItem(column_index)
        if len(self.general_rows_to_hide) > 0:
            header_item.setIcon(QtGui.QIcon(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Filter_Active.png"))))
        else:
            header_item.setIcon(QtGui.QIcon())

# Function to apply filters to table based on a desired text
    def filter_by_text(self, column_index):
        """
        Opens a dialog for filtering the specified column by text input.

        Args:
            column_index (int): The index of the column to filter.
        """
        filter_dialog = QtWidgets.QDialog(self)
        filter_dialog.setWindowTitle("Filtrar por texto")
        
        label = QtWidgets.QLabel("Texto a filtrar:")
        text_input = QtWidgets.QLineEdit()
        
        filter_button = QtWidgets.QPushButton("Filtrar")
        filter_button.setStyleSheet("QPushButton {\n"
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
"  padding: 2px .8em;\n"
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
        filter_button.clicked.connect(lambda: self.apply_filter(column_index, None, False, text_input.text(), filter_dialog))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(text_input)
        layout.addWidget(filter_button)

        filter_dialog.setLayout(layout)
        filter_dialog.exec()

# Function to obtain the unique matching applied filters 
    def get_unique_values(self, column_index):
        """
        Retrieves unique values from the specified column, taking into account any active filters on other columns.

        Args:
            column_index (int): The index of the column from which to retrieve unique values.

        Returns:
            set: A set of unique values from the specified column that are visible based on the current filters.
        """
        unique_values = set()
        for row in range(self.rowCount()):
            show_row = True
            for col, filters in self.column_filters.items():
                if col != column_index:
                    item = self.item(row, col)
                    if item:
                        item_value = item.text()
                        if filters and item_value not in filters:
                            show_row = False
                            break
            if show_row:
                item = self.item(row, column_index)
                if item:
                    unique_values.add(item.text())
        return unique_values

# Function to get values filtered by all columns
    def get_filtered_values(self):
        """
        Gets the current filter values for all columns.

        Returns:
            dict: A dictionary where each key is a column index and the value is a set of filters applied to that column.
        """
        filtered_values = {}
        for col, filters in self.column_filters.items():
            filtered_values[col] = filters
        return filtered_values

# Function to sort column
    def sort_column(self, column_index, sortOrder):
        """
        Sorts the specified column based on the given order. If the column is a date column, a custom sort method is used.

        Args:
            column_index (int): The index of the column to sort.
            sortOrder (Qt.SortOrder): The order to sort the column (ascending or descending).
        """
        if column_index in [11, 13, 14]:
            self.custom_sort(column_index, sortOrder)
        else:
            self.sortByColumn(column_index, sortOrder)

# Function to sort column based on special datatypes
    def custom_sort(self, column, order):
        """
        Custom sorting method for date columns. Sorts the specified column based on date values.

        Args:
            column (int): The index of the column to sort.
            order (Qt.SortOrder): The order to sort the column (ascending or descending).
        """
        row_count = self.rowCount()

        indexes = list(range(row_count))
        indexes.sort(key=lambda i: QtCore.QDateTime.fromString(self.item(i, column).text(), "dd-MM-yyyy"))

        if order == QtCore.Qt.SortOrder.DescendingOrder:
            indexes.reverse()

        hidden_rows = [row for row in range(row_count) if self.isRowHidden(row)]

        rows = self.rowCount()
        for i in range(rows):
            self.insertRow(i)

        for new_row, old_row in enumerate(indexes):
            for col in range(self.columnCount()):
                item = self.takeItem(old_row + rows, col)
                self.setItem(new_row, col, item)

        for i in range(rows):
            self.removeRow(rows)

        for row in hidden_rows:
            self.setRowHidden(row, True)

# Function with the menu configuration
    def contextMenuEvent(self, event):
        """
        Handles the context menu event for the table. Shows a menu for filtering unique values when the header is right-clicked.

        Args:
            event (QEvent): The event triggered by the context menu action.
        """
        if self.horizontalHeader().visualIndexAt(event.pos().x()) >= 0:
            logical_index = self.horizontalHeader().logicalIndexAt(event.pos().x())
            header_pos = self.mapToGlobal(self.horizontalHeader().pos())
            header_height = self.horizontalHeader().height()
            self.show_unique_values_menu(logical_index, header_pos, header_height)
        else:
            super().contextMenuEvent(event)


class Ui_QueryInvoice_Window(QtWidgets.QMainWindow):
    """
    UI class for the Query Invoice window.
    """
    def __init__(self, username):
        """
        Initializes the Ui_QueryInvoice_Window.
        """
        super().__init__()
        self.username = username
        self.setupUi(self)

    def setupUi(self, QueryInvoice_Window):
        """
        Sets up the user interface for the QueryInvoice_Window.

        Args:
            QueryInvoice_Window (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        QueryInvoice_Window.setObjectName("QueryInvoice_Window")
        QueryInvoice_Window.resize(845, 590)
        QueryInvoice_Window.setMinimumSize(QtCore.QSize(1000, 590))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        QueryInvoice_Window.setWindowIcon(icon)
        QueryInvoice_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=QueryInvoice_Window)
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
        self.tableQueryInvoice = CustomTableWidget()
        self.tableQueryInvoice.setObjectName("tableQueryInvoice")
        self.tableQueryInvoice.setColumnCount(21)
        self.tableQueryInvoice.setRowCount(0)
        for i in range(21):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            item.setFont(font)
            self.tableQueryInvoice.setHorizontalHeaderItem(i, item)
        self.tableQueryInvoice.setSortingEnabled(True)
        self.tableQueryInvoice.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_2.addWidget(self.tableQueryInvoice, 1, 0, 1, 11)
        self.label_SumItems = QtWidgets.QLabel(parent=self.frame)
        self.label_SumItems.setMinimumSize(QtCore.QSize(40, 10))
        self.label_SumItems.setMaximumSize(QtCore.QSize(40, 10))
        self.label_SumItems.setText("")
        self.label_SumItems.setObjectName("label_SumItems")
        self.gridLayout_2.addWidget(self.label_SumItems, 2, 7, 1, 1)
        self.label_SumValue = QtWidgets.QLabel(parent=self.frame)
        self.label_SumValue.setMinimumSize(QtCore.QSize(80, 20))
        self.label_SumValue.setMaximumSize(QtCore.QSize(80, 20))
        self.label_SumValue.setText("")
        self.label_SumValue.setObjectName("label_SumValue")
        self.gridLayout_2.addWidget(self.label_SumValue, 2, 8, 1, 1)
        self.label_CountItems = QtWidgets.QLabel(parent=self.frame)
        self.label_CountItems.setMinimumSize(QtCore.QSize(60, 10))
        self.label_CountItems.setMaximumSize(QtCore.QSize(60, 10))
        self.label_CountItems.setText("")
        self.label_CountItems.setObjectName("label_CountItems")
        self.gridLayout_2.addWidget(self.label_CountItems, 2, 9, 1, 1)
        self.label_CountValue = QtWidgets.QLabel(parent=self.frame)
        self.label_CountValue.setMinimumSize(QtCore.QSize(80, 10))
        self.label_CountValue.setMaximumSize(QtCore.QSize(80, 10))
        self.label_CountValue.setText("")
        self.label_CountValue.setObjectName("label_CountValue")
        self.gridLayout_2.addWidget(self.label_CountValue, 2, 10, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        QueryInvoice_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=QueryInvoice_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 845, 22))
        self.menubar.setObjectName("menubar")
        QueryInvoice_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=QueryInvoice_Window)
        self.statusbar.setObjectName("statusbar")
        QueryInvoice_Window.setStatusBar(self.statusbar)
        self.tableQueryInvoice.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.retranslateUi(QueryInvoice_Window)
        QtCore.QMetaObject.connectSlotsByName(QueryInvoice_Window)
        self.tableQueryInvoice.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tableQueryInvoice.horizontalHeader().sectionClicked.connect(self.on_header_section_clicked)
        self.tableQueryInvoice.itemSelectionChanged.connect(self.countSelectedCells)

        self.query_all_invoices()


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, QueryInvoice_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        QueryInvoice_Window.setWindowTitle(_translate("QueryInvoice_Window", "Consultar Facturas"))
        item = self.tableQueryInvoice.horizontalHeaderItem(0)
        item.setText(_translate("QueryInvoice_Window", "Nº Factura"))
        item = self.tableQueryInvoice.horizontalHeaderItem(1)
        item.setText(_translate("QueryInvoice_Window", "Fecha Factura"))
        item = self.tableQueryInvoice.horizontalHeaderItem(2)
        item.setText(_translate("QueryInvoice_Window", "Cod. Cliente"))
        item = self.tableQueryInvoice.horizontalHeaderItem(3)
        item.setText(_translate("QueryInvoice_Window", "Cliente"))
        item = self.tableQueryInvoice.horizontalHeaderItem(4)
        item.setText(_translate("QueryInvoice_Window", "CIF"))
        item = self.tableQueryInvoice.horizontalHeaderItem(5)
        item.setText(_translate("QueryInvoice_Window", "Cant. Días"))
        item = self.tableQueryInvoice.horizontalHeaderItem(6)
        item.setText(_translate("QueryInvoice_Window", "N/ Ref"))
        item = self.tableQueryInvoice.horizontalHeaderItem(7)
        item.setText(_translate("QueryInvoice_Window", "SbtFact"))
        item = self.tableQueryInvoice.horizontalHeaderItem(8)
        item.setText(_translate("QueryInvoice_Window", "Vto. Prog. 1"))
        item = self.tableQueryInvoice.horizontalHeaderItem(9)
        item.setText(_translate("QueryInvoice_Window", "Vto. Prog. 2"))
        item = self.tableQueryInvoice.horizontalHeaderItem(10)
        item.setText(_translate("QueryInvoice_Window", "IVA"))
        item = self.tableQueryInvoice.horizontalHeaderItem(11)
        item.setText(_translate("QueryInvoice_Window", "IVA Fact."))
        item = self.tableQueryInvoice.horizontalHeaderItem(12)
        item.setText(_translate("QueryInvoice_Window", "Total Fact."))
        item = self.tableQueryInvoice.horizontalHeaderItem(13)
        item.setText(_translate("QueryInvoice_Window", "Grupo"))
        item = self.tableQueryInvoice.horizontalHeaderItem(14)
        item.setText(_translate("QueryInvoice_Window", "Aplicación"))
        item = self.tableQueryInvoice.horizontalHeaderItem(15)
        item.setText(_translate("QueryInvoice_Window", "Total Cantidad"))
        item = self.tableQueryInvoice.horizontalHeaderItem(16)
        item.setText(_translate("QueryInvoice_Window", "Fecha Prev."))
        item = self.tableQueryInvoice.horizontalHeaderItem(17)
        item.setText(_translate("QueryInvoice_Window", "OK"))
        item = self.tableQueryInvoice.horizontalHeaderItem(18)
        item.setText(_translate("QueryInvoice_Window", "S/ Ref"))
        item = self.tableQueryInvoice.horizontalHeaderItem(19)
        item.setText(_translate("QueryInvoice_Window", "Obs."))
        item = self.tableQueryInvoice.horizontalHeaderItem(20)
        item.setText(_translate("QueryInvoice_Window", "País Dest."))

    def query_all_invoices(self):
        """
        Queries the database for all invoices, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.tableQueryInvoice.setRowCount(0)

        commands_queryinvoice = ("""
                        SELECT invoice."num_invoice", TO_CHAR(invoice."date_invoice",'dd/MM/yyyy'), clients."code", clients."name", clients."cif",
                        pay_way."num_days", invoice."our_ref", invoice."tax_base_amount", clients."vto_prog1", clients."vto_prog2",
                        invoice."iva", (invoice."tax_base_amount" * invoice."iva"/100) AS IVAFACT, (invoice."tax_base_amount" + (invoice."tax_base_amount" * invoice."iva"/100)) AS TOTALFACT,
                        invoice."client_group", invoice."application", invoice."total_qty_elements", TO_CHAR(invoice."date_invoice" + INTERVAL '1 day' * pay_way."num_days",'dd/MM/yyyy') AS FCHPREV,
                        TO_CHAR(invoice."pay_date",'dd/MM/yyyy'), invoice."their_ref", invoice."obs_delivnote", country."name"
                        FROM purch_fact.invoice_header AS invoice
                        INNER JOIN purch_fact.clients AS clients ON (invoice."id_client" = clients."id")
                        INNER JOIN purch_fact.pay_way AS pay_way ON (clients."pay_way_id" = pay_way."id")
                        INNER JOIN purch_fact.destination_country AS country ON (invoice."id_dest_country" = country."id")
                        ORDER BY invoice."num_invoice"
                        """)

        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            cur.execute(commands_queryinvoice)
            results=cur.fetchall()
            self.tableQueryInvoice.setRowCount(len(results))
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(21):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableQueryInvoice.setItem(tablerow, column, it)

                self.tableQueryInvoice.setItemDelegateForRow(tablerow, AlignDelegate(self.tableQueryInvoice))
                tablerow+=1

            # self.tableQueryInvoice.verticalHeader().hide()
            self.tableQueryInvoice.setSortingEnabled(False)
            self.tableQueryInvoice.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.tableQueryInvoice.horizontalHeader().setSectionResizeMode(20, QtWidgets.QHeaderView.ResizeMode.Stretch)


        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
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

# Function to conver money strings to float
    def euro_string_to_float(self, euro_str):
        """
        Converts a string representing an amount in euros to a float.

        Args:
            euro_str (str): A string representing the amount in euros (e.g., "1.234,56 €").
        
        Returns:
            float: The numeric value of the amount as a float.
        """
        match = re.match(r'^([\d.,]+)\s€$', euro_str)
        if match:
            number_str = match.group(1)
            number_str = number_str.replace('.', '').replace(',', '.')
            return float(number_str)
        else:
            return 0.0


    def on_item_double_clicked(self, item):
        """
        Opens detailed information when column is double-clicked.
        """
        if item.column() in [0]:
            num_invoice = self.tableQueryInvoice.item(item.row(), 0).text()

            # from InvoiceNew_Window import Ui_InvoiceNew_Window
            # config_obj = configparser.ConfigParser()
            # config_obj.read(r"C:\Program Files\ERP EIPSA\database.ini")
            # dbparam = config_obj["postgresql"]
            # # set your parameters for the database connection URI using the keys from the configfile.ini
            # user_database = dbparam["user"]
            # password_database = dbparam["password"]

            # db_invoices_query = createConnection(user_database, password_database)
            # if not db_invoices_query:
            #     sys.exit()

            # self.invoices_app_query = Ui_InvoiceNew_Window(db_invoices_query, self.username, num_invoice)
            # self.invoices_app_query.showMaximized()

#Function when clicking on table header
    def on_header_section_clicked(self, logical_index):
        """
        Handles the click event on the table header.
        Displays a context menu for unique values in the clicked column header.
        """
        header_pos = self.tableQueryInvoice.horizontalHeader().sectionViewportPosition(logical_index)
        header_height = self.tableQueryInvoice.horizontalHeader().height()
        popup_pos = self.tableQueryInvoice.viewport().mapToGlobal(QtCore.QPoint(header_pos, header_height))
        self.tableQueryInvoice.show_unique_values_menu(logical_index, popup_pos, header_height)

# Function to count selected cells and sum values
    def countSelectedCells(self):
        """
        Counts the number of selected cells and sums their values. Updates the UI labels with the count and sum.
        """
        if len(self.tableQueryInvoice.selectedIndexes()) > 1:
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
            self.label_SumItems.setText("")
            self.label_SumValue.setText("")
            self.label_CountItems.setText("")
            self.label_CountValue.setText("")

            sum_value = sum([self.euro_string_to_float(ix.data()) if (ix.data() is not None and (re.match(r'^[\d.,]+\s€$', ix.data()) and ix.column() in [7, 11, 12]))
                            else (float(ix.data()) if (ix.data() is not None and ix.data().replace(',', '.', 1).replace('.', '', 1).isdigit() and ix.column() in [15]) else 0) for ix in self.tableQueryInvoice.selectedIndexes()])
            count_value = len([ix for ix in self.tableQueryInvoice.selectedIndexes() if ix.data() != ""])
            if sum_value > 0:
                self.label_SumItems.setText("Suma:")
                self.label_SumValue.setText(locale.format_string("%.2f", sum_value, grouping=True))
            if count_value > 0:
                self.label_CountItems.setText("Recuento:")
                self.label_CountValue.setText(str(count_value))
        else:
            self.label_SumItems.setText("")
            self.label_SumValue.setText("")
            self.label_CountItems.setText("")
            self.label_CountValue.setText("")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QueryInvoice_Window = Ui_QueryInvoice_Window('c.zofio')
    QueryInvoice_Window.show()
    sys.exit(app.exec())
