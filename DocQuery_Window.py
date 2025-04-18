# Form implementation generated from reading ui file 'QueryDoc_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config
import pandas as pd
from PyQt6.QtWidgets import QFileDialog
import os
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
        Initializes the style option for the item, setting its display alignment to center and setting color for cells.

        Args:
            option (QtWidgets.QStyleOptionViewItem): The style option to initialize.
            index (QtCore.QModelIndex): The model index of the item.
        """
        super(AlignDelegate, self).initStyleOption(option, index)

        if index.column() == 15:
            option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignLeft
        else:
            option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter

        if index.column() == 11:  # Check column and paint when apply
            value = index.data()

            if value == "Aprobado":  
                color = QtGui.QColor(146, 208, 80)  # Green
            elif value == "Eliminado":
                color = QtGui.QColor(255, 0, 0)  # Red
            else:
                color = QtGui.QColor(255, 255, 255)  # White for rest

            option.backgroundBrush = color

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
        # if column_index in self.column_filters:
        #     del self.column_filters[column_index]
        # if column_index in self.checkbox_states:
        #     del self.checkbox_states[column_index]
        # if column_index in self.rows_hidden:
        #     for item in self.rows_hidden[column_index]:
        #         self.setRowHidden(item, False)
        #         if item in self.general_rows_to_hide:
        #             self.general_rows_to_hide.remove(item)
        #     del self.rows_hidden[column_index]
        # header_item = self.horizontalHeaderItem(column_index)
        # header_item.setIcon(QtGui.QIcon())

        if column_index in self.column_filters:
            del self.column_filters[column_index]
        if column_index in self.checkbox_states:
            del self.checkbox_states[column_index]
        if column_index in self.rows_hidden:
            del self.rows_hidden[column_index]

        # Recalculate hidden global rows
        self.general_rows_to_hide = set()
        for col_hidden_rows in self.rows_hidden.values():
            self.general_rows_to_hide.update(col_hidden_rows)

        # Show or hide rows according to remaining filters
        for row in range(self.rowCount()):
            self.setRowHidden(row, row in self.general_rows_to_hide)

        # Reset header icon for column
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
        # if column_index not in self.column_filters:
        #     self.column_filters[column_index] = set()

        # if text_filter is None:
        #     if value is None:
        #         self.column_filters[column_index] = set()
        #     elif checked:
        #         self.column_filters[column_index].add(value)
        #     elif value in self.column_filters[column_index]:
        #         self.column_filters[column_index].remove(value)

        # rows_to_hide = set()
        # for row in range(self.rowCount()):
        #     show_row = True

        #     # Check filters for all columns
        #     for col, filters in self.column_filters.items():
        #         item = self.item(row, col)
        #         if item:
        #             item_value = item.text()
        #             if text_filter is None:
        #                 if filters and item_value not in filters:
        #                     show_row = False
        #                     break

        # # Filtering by text
        #     if text_filter is not None:
        #         filter_dialog.accept()
        #         item = self.item(row, column_index)
        #         if item:
        #             if text_filter.upper() in item.text().upper():
        #                 self.column_filters[column_index].add(item.text())
        #             else:
        #                 show_row = False

        #     if not show_row:
        #         if row not in self.general_rows_to_hide:
        #             self.general_rows_to_hide.add(row)
        #             rows_to_hide.add(row)
        #     else:
        #         if row in self.general_rows_to_hide:
        #             self.general_rows_to_hide.remove(row)

        # # Update hidden rows for this column depending on checkboxes
        # if checked and text_filter is None:
        #     if column_index not in self.rows_hidden:
        #         self.rows_hidden[column_index] = set(rows_to_hide)
        #     else:
        #         self.rows_hidden[column_index].update(rows_to_hide)

        # # Update hidden rows for this column depending on filtered text
        # if text_filter is not None and value is None:
        #     if column_index not in self.rows_hidden:
        #         self.rows_hidden[column_index] = set(rows_to_hide)
        #     else:
        #         self.rows_hidden[column_index].update(rows_to_hide)

        # # Iterate over all rows to hide them as necessary
        # for row in range(self.rowCount()):
        #     self.setRowHidden(row, row in self.general_rows_to_hide)

        # header_item = self.horizontalHeaderItem(column_index)
        # if len(self.general_rows_to_hide) > 0:
        #     header_item.setIcon(QtGui.QIcon(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Filter_Active.png"))))
        # else:
        #     header_item.setIcon(QtGui.QIcon())

        if column_index not in self.column_filters:
            self.column_filters[column_index] = set()
        if column_index not in self.rows_hidden:
            self.rows_hidden[column_index] = set()

        # Manejo del filtro por checkboxes
        if text_filter is None:
            if value is None:  # Eliminar todos los filtros de la columna
                self.column_filters[column_index] = set()
                self.rows_hidden[column_index] = set()
            elif checked:  # Agregar un valor permitido
                self.column_filters[column_index].add(value)
            elif value in self.column_filters[column_index]:  # Quitar un valor permitido
                self.column_filters[column_index].remove(value)

        # Crear un conjunto temporal para filas ocultas por este filtro
        rows_to_hide = set()
        for row in range(self.rowCount()):
            show_row = True

            # Filtro por checkboxes
            if text_filter is None:
                item = self.item(row, column_index)
                if item and self.column_filters[column_index] and item.text() not in self.column_filters[column_index]:
                    show_row = False

            # Filtro por texto
            if text_filter is not None:
                filter_dialog.accept()
                item = self.item(row, column_index)
                if item and text_filter.upper() not in item.text().upper():
                    show_row = False

            if not show_row:
                rows_to_hide.add(row)

        # Actualizar filas ocultas para esta columna
        if text_filter is not None and value is None:
            self.rows_hidden[column_index] = rows_to_hide
        elif text_filter is None:
            self.rows_hidden[column_index] = rows_to_hide

        # Recalcular las filas globalmente ocultas combinando todos los filtros por columna
        self.general_rows_to_hide = set()
        for col_hidden_rows in self.rows_hidden.values():
            self.general_rows_to_hide.update(col_hidden_rows)

        # Ocultar o mostrar filas según `self.general_rows_to_hide`
        for row in range(self.rowCount()):
            self.setRowHidden(row, row in self.general_rows_to_hide)

        # Actualizar el ícono del encabezado
        header_item = self.horizontalHeaderItem(column_index)
        if self.rows_hidden[column_index]:
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
        if column_index in [1,2,13]:
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
        indexes.sort(key=lambda i: QtCore.QDateTime.fromString(self.item(i, column).text(), "dd/MM/yyyy"))

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

class Ui_QueryDoc_Window(QtWidgets.QMainWindow):
    """
    UI class for the Query Doc window.
    """
    def __init__(self):
        """
        Initializes the Ui_QueryDoc_Window.
        """
        super().__init__()
        self.setupUi(self)

    def setupUi(self, QueryDoc_Window):
        """
        Sets up the user interface for the QueryDoc_Window.

        Args:
            QueryDoc_Window (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        QueryDoc_Window.setObjectName("QueryDoc_Window")
        QueryDoc_Window.resize(845, 654)
        QueryDoc_Window.setMinimumSize(QtCore.QSize(1500, 790))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        QueryDoc_Window.setWindowIcon(icon)
        QueryDoc_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=QueryDoc_Window)
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
        self.gridLayout_2.addItem(spacerItem2, 0, 0, 1, 2)
        self.Button_Export = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Export.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_Export.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_Export.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_Export.setObjectName("Button_Export")
        self.gridLayout_2.addWidget(self.Button_Export, 1, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 1, 1, 1)
        self.tableQueryDoc = CustomTableWidget()
        self.tableQueryDoc.setObjectName("tableQueryDoc")
        self.tableQueryDoc.setColumnCount(16)
        self.tableQueryDoc.setRowCount(0)
        for i in range(16):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            item.setFont(font)
            self.tableQueryDoc.setHorizontalHeaderItem(i, item)
        self.tableQueryDoc.setSortingEnabled(False)
        self.tableQueryDoc.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableQueryDoc.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_2.addWidget(self.tableQueryDoc, 2, 0, 1, 11)
        self.label_CountItems = QtWidgets.QLabel(parent=self.frame)
        self.label_CountItems.setMinimumSize(QtCore.QSize(60, 10))
        self.label_CountItems.setMaximumSize(QtCore.QSize(60, 10))
        self.label_CountItems.setText("")
        self.label_CountItems.setObjectName("label_CountItems")
        self.gridLayout_2.addWidget(self.label_CountItems, 4, 9, 1, 1)
        self.label_CountValue = QtWidgets.QLabel(parent=self.frame)
        self.label_CountValue.setMinimumSize(QtCore.QSize(80, 10))
        self.label_CountValue.setMaximumSize(QtCore.QSize(80, 10))
        self.label_CountValue.setText("")
        self.label_CountValue.setObjectName("label_CountValue")
        self.gridLayout_2.addWidget(self.label_CountValue, 4, 10, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        QueryDoc_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=QueryDoc_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 845, 22))
        self.menubar.setObjectName("menubar")
        QueryDoc_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=QueryDoc_Window)
        self.statusbar.setObjectName("statusbar")
        QueryDoc_Window.setStatusBar(self.statusbar)

        self.retranslateUi(QueryDoc_Window)
        QtCore.QMetaObject.connectSlotsByName(QueryDoc_Window)

        self.Button_Export.clicked.connect(self.export_to_excel)
        self.tableQueryDoc.horizontalHeader().sectionClicked.connect(self.on_header_section_clicked)
        self.tableQueryDoc.itemSelectionChanged.connect(self.countSelectedCells)
        self.query_all_docs()


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, QueryDoc_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        QueryDoc_Window.setWindowTitle(_translate("QueryDoc_Window", "Consultar Documentación"))
        item = self.tableQueryDoc.horizontalHeaderItem(0)
        item.setText(_translate("QueryDoc_Window", "Nº Pedido"))
        item = self.tableQueryDoc.horizontalHeaderItem(1)
        item.setText(_translate("QueryDoc_Window", "Fecha Pedido"))
        item = self.tableQueryDoc.horizontalHeaderItem(2)
        item.setText(_translate("QueryDoc_Window", "Fecha Prevista"))
        item = self.tableQueryDoc.horizontalHeaderItem(3)
        item.setText(_translate("QueryDoc_Window", "Nº PO"))
        item = self.tableQueryDoc.horizontalHeaderItem(4)
        item.setText(_translate("QueryDoc_Window", "Cliente"))
        item = self.tableQueryDoc.horizontalHeaderItem(5)
        item.setText(_translate("QueryDoc_Window", "Material"))
        item = self.tableQueryDoc.horizontalHeaderItem(6)
        item.setText(_translate("QueryDoc_Window", "Nº Doc. Cliente"))
        item = self.tableQueryDoc.horizontalHeaderItem(7)
        item.setText(_translate("QueryDoc_Window", "Nº Doc. EIPSA"))
        item = self.tableQueryDoc.horizontalHeaderItem(8)
        item.setText(_translate("QueryDoc_Window", "Título"))
        item = self.tableQueryDoc.horizontalHeaderItem(9)
        item.setText(_translate("QueryDoc_Window", "Tipo Doc."))
        item = self.tableQueryDoc.horizontalHeaderItem(10)
        item.setText(_translate("QueryDoc_Window", "Crítico"))
        item = self.tableQueryDoc.horizontalHeaderItem(11)
        item.setText(_translate("QueryDoc_Window", "Estado"))
        item = self.tableQueryDoc.horizontalHeaderItem(12)
        item.setText(_translate("QueryDoc_Window", "Nº Revisión"))
        item = self.tableQueryDoc.horizontalHeaderItem(13)
        item.setText(_translate("QueryDoc_Window", "Fecha"))
        item = self.tableQueryDoc.horizontalHeaderItem(14)
        item.setText(_translate("QueryDoc_Window", "Seguimiento"))
        item = self.tableQueryDoc.horizontalHeaderItem(15)
        item.setText(_translate("QueryDoc_Window", "Historial Rev."))
        self.Button_Export.setText(_translate("QueryDoc_Window", "Exportar"))

    def query_all_docs(self):
        """
        Queries the database for documents, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.tableQueryDoc.setRowCount(0)
        commands_queryalldoc = ("""
                        SELECT documentation."num_order", TO_CHAR(orders."order_date", 'DD-MM-YYYY'), TO_CHAR(orders."expected_date", 'DD-MM-YYYY'), orders."num_ref_order", offers."client", product_type."variable", documentation."num_doc_client",
                        documentation."num_doc_eipsa", documentation."doc_title", document_type."doc_type", documentation."critical", documentation."state",
                        documentation."revision", "state_date", documentation."tracking", hist_doc."hist_rev_column"
                        FROM documentation
                        INNER JOIN orders ON (orders."num_order" = documentation."num_order")
                        INNER JOIN offers ON (offers."num_offer" = orders."num_offer")
                        INNER JOIN document_type ON (document_type."id" = documentation."doc_type_id")
                        LEFT JOIN hist_doc ON (hist_doc."num_doc_eipsa" = documentation."num_doc_eipsa")
                        INNER JOIN product_type ON (product_type."material" = offers."material")
                        ORDER BY documentation."num_order"
                        """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            cur.execute(commands_queryalldoc)
            results=cur.fetchall()

            self.tableQueryDoc.setRowCount(len(results))
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(16):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableQueryDoc.setItem(tablerow, column, it)

                tablerow+=1

            self.tableQueryDoc.verticalHeader().hide()
            self.tableQueryDoc.setSortingEnabled(False)
            self.tableQueryDoc.setItemDelegate(AlignDelegate(self.tableQueryDoc))
            self.tableQueryDoc.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

            for i in range(1,15):
                self.tableQueryDoc.horizontalHeader().setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeMode.Interactive)
                self.tableQueryDoc.setColumnWidth(i, 100)

            self.tableQueryDoc.itemDoubleClicked.connect(self.expand_cell)

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

    def expand_cell(self, item):
        """
        Displays the content of a cell in a dialog box. Useful for viewing larger text fields 
        in a table more comfortably.

        Args:
            item (QTableWidgetItem): The table item to be expanded.
        """
        if item.column() in [14, 15]:
            cell_content = item.text()
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Documentación")
            dlg.setText(cell_content)
            dlg.exec()

    def export_to_excel(self):
        """
        Exports the visible data from the table to an Excel file. If no data is loaded, displays a warning message.
        """
        if self.tableQueryDoc.rowCount() > 0:
            file_name, _ = QFileDialog.getSaveFileName(self, "Guardar como Excel", "", "Archivos Excel (*.xlsx);;Todos los archivos (*)")

            if file_name:
                df = pd.DataFrame()
                for col in range(self.tableQueryDoc.columnCount()):
                    header = self.tableQueryDoc.horizontalHeaderItem(col).text()
                    column_data = []
                    for row in range(self.tableQueryDoc.rowCount()):
                        if not self.tableQueryDoc.isRowHidden(row):
                            column_data.append(self.tableQueryDoc.item(row, col).text())
                    df[header] = column_data

                with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)

                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Consultar Documentación")
                dlg.setText("Datos exportados con éxito")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                dlg.exec()
                del dlg,new_icon

        else:
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Consultar Documentación")
            dlg.setText("No hay datos para exportar")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            del dlg,new_icon

#Function when clicking on table header
    def on_header_section_clicked(self, logical_index):
        """
        Handles the click event on the table header.
        Displays a context menu for unique values in the clicked column header.
        """
        header_pos = self.tableQueryDoc.horizontalHeader().sectionViewportPosition(logical_index)
        header_height = self.tableQueryDoc.horizontalHeader().height()
        popup_pos = self.tableQueryDoc.viewport().mapToGlobal(QtCore.QPoint(header_pos, header_height))
        self.tableQueryDoc.show_unique_values_menu(logical_index, popup_pos, header_height)

    def countSelectedCells(self):
        """
        Counts the number of selected cells and sums their values. Updates the UI labels with the count and sum.
        """
        if len(self.tableQueryDoc.selectedIndexes()) > 1:
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

            self.label_CountItems.setText("")
            self.label_CountValue.setText("")

            count_value = len([ix for ix in self.tableQueryDoc.selectedIndexes() if ix.data() != ""])

            if count_value > 0:
                self.label_CountItems.setText("Recuento:")
                self.label_CountValue.setText(str(count_value))
        else:
            self.label_CountItems.setText("")
            self.label_CountValue.setText("")






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QueryDoc_Window = Ui_QueryDoc_Window()
    QueryDoc_Window.show()
    sys.exit(app.exec())