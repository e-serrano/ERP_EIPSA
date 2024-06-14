# Form implementation generated from reading ui file 'PurchasingGeneralQuery_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import re
from PyQt6 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config
import locale
import pandas as pd
import os
from datetime import *
from openpyxl.styles import NamedStyle
import tkinter as tk
from tkinter import filedialog

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter


class CustomTableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_filters=[]
        self.column_filters = {}
        self.column_actions = {}
        self.checkbox_states = {}
        self.rows_hidden = {}
        self.general_rows_to_hide = set()

# Function to show the menu
    def show_unique_values_menu(self, column_index, header_pos, header_height):
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
        if column_index not in self.checkbox_states:
            self.checkbox_states[column_index] = {}

        for checkbox in checkboxes:
            checkbox.setCheckState(QtCore.Qt.CheckState(state))

        self.checkbox_states[column_index]["Seleccionar todo"] = state


# Function to apply filters to table
    def apply_filter(self, column_index, value, checked, text_filter=None, filter_dialog=None):
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
            hidden = False

            for col, filters in self.column_filters.items():
                if filters:
                    item = self.item(row, col)
                    item_value = item.text() if item else ""
                    if item_value not in filters:
                        hidden = True
                        break

            self.setRowHidden(row, hidden)

        header_item = self.horizontalHeaderItem(column_index)
        if len(self.general_rows_to_hide) > 0:
            header_item.setIcon(QtGui.QIcon(os.path.abspath(os.path.join(basedir, "Resources/Iconos/Filter_Active.png"))))
        else:
            header_item.setIcon(QtGui.QIcon())


    def filter_by_text(self, column_index):
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
        filtered_values = {}
        for col, filters in self.column_filters.items():
            filtered_values[col] = filters
        return filtered_values

# Function to sort column
    def sort_column(self, column_index, sortOrder):
        if column_index in [11, 13, 14]:
            self.custom_sort(column_index, sortOrder)
        else:
            self.sortByColumn(column_index, sortOrder)


    def custom_sort(self, column, order):
    # Obtén la cantidad de filas en la tabla
        row_count = self.rowCount()

        # Crea una lista de índices ordenados según las fechas
        indexes = list(range(row_count))
        indexes.sort(key=lambda i: QtCore.QDateTime.fromString(self.item(i, column).text(), "dd/MM/yyyy"))

        # Si el orden es descendente, invierte la lista
        if order == QtCore.Qt.SortOrder.DescendingOrder:
            indexes.reverse()

        # Guarda el estado actual de las filas ocultas
        hidden_rows = [row for row in range(row_count) if self.isRowHidden(row)]

        # Actualiza las filas en la tabla en el orden ordenado
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
        if self.horizontalHeader().visualIndexAt(event.pos().x()) >= 0:
            logical_index = self.horizontalHeader().logicalIndexAt(event.pos().x())
            header_pos = self.mapToGlobal(self.horizontalHeader().pos())
            header_height = self.horizontalHeader().height()
            self.show_unique_values_menu(logical_index, header_pos, header_height)
        else:
            super().contextMenuEvent(event)


class Ui_PurchasingGeneralQuery_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, PurchasingGeneralQuery_Window):
        PurchasingGeneralQuery_Window.setObjectName("PurchasingGeneralQuery_Window")
        PurchasingGeneralQuery_Window.resize(845, 590)
        PurchasingGeneralQuery_Window.setMinimumSize(QtCore.QSize(1000, 590))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        PurchasingGeneralQuery_Window.setWindowIcon(icon)
        PurchasingGeneralQuery_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=PurchasingGeneralQuery_Window)
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
        self.label_Order= QtWidgets.QLabel(parent=self.frame)
        self.label_Order.setMinimumSize(QtCore.QSize(90, 25))
        self.label_Order.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Order.setFont(font)
        self.label_Order.setObjectName("label_Order")
        self.gridLayout_2.addWidget(self.label_Order, 1, 0, 1, 1)
        self.Order_Query = QtWidgets.QLineEdit(parent=self.frame)
        self.Order_Query.setMinimumSize(QtCore.QSize(120, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Order_Query.setFont(font)
        self.Order_Query.setObjectName("Order_Query")
        self.gridLayout_2.addWidget(self.Order_Query, 1, 1, 1, 2)
        self.Button_Delete = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Delete.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_Delete.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_Delete.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_Delete.setObjectName("Button_Delete")
        self.gridLayout_2.addWidget(self.Button_Delete, 1, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.tableQueryPurchase = CustomTableWidget()
        self.tableQueryPurchase.setObjectName("tableQueryPurchase")
        self.tableQueryPurchase.setColumnCount(7)
        self.tableQueryPurchase.setRowCount(0)
        for i in range(7):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            item.setFont(font)
            self.tableQueryPurchase.setHorizontalHeaderItem(i, item)
        self.tableQueryPurchase.setSortingEnabled(True)
        self.tableQueryPurchase.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_2.addWidget(self.tableQueryPurchase, 3, 0, 1, 11)
        self.label_SumItems = QtWidgets.QLabel(parent=self.frame)
        self.label_SumItems.setMinimumSize(QtCore.QSize(40, 10))
        self.label_SumItems.setMaximumSize(QtCore.QSize(40, 10))
        self.label_SumItems.setText("")
        self.label_SumItems.setObjectName("label_SumItems")
        self.gridLayout_2.addWidget(self.label_SumItems, 4, 7, 1, 1)
        self.label_SumValue = QtWidgets.QLabel(parent=self.frame)
        self.label_SumValue.setMinimumSize(QtCore.QSize(80, 20))
        self.label_SumValue.setMaximumSize(QtCore.QSize(80, 20))
        self.label_SumValue.setText("")
        self.label_SumValue.setObjectName("label_SumValue")
        self.gridLayout_2.addWidget(self.label_SumValue, 4, 8, 1, 1)
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
        PurchasingGeneralQuery_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=PurchasingGeneralQuery_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 845, 22))
        self.menubar.setObjectName("menubar")
        PurchasingGeneralQuery_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=PurchasingGeneralQuery_Window)
        self.statusbar.setObjectName("statusbar")
        PurchasingGeneralQuery_Window.setStatusBar(self.statusbar)
        self.tableQueryPurchase.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.retranslateUi(PurchasingGeneralQuery_Window)
        QtCore.QMetaObject.connectSlotsByName(PurchasingGeneralQuery_Window)
        self.Order_Query.returnPressed.connect(self.query_filtered)
        self.tableQueryPurchase.itemSelectionChanged.connect(self.countSelectedCells)
        self.tableQueryPurchase.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tableQueryPurchase.horizontalHeader().sectionClicked.connect(self.on_header_section_clicked)
        self.Button_Delete.clicked.connect(self.query_all)

        self.query_all()


    def retranslateUi(self, PurchasingGeneralQuery_Window):
        _translate = QtCore.QCoreApplication.translate
        PurchasingGeneralQuery_Window.setWindowTitle(_translate("PurchasingGeneralQuery_Window", "Consultar Compras"))
        item = self.tableQueryPurchase.horizontalHeaderItem(0)
        item.setText(_translate("PurchasingGeneralQuery_Window", "ID"))
        item = self.tableQueryPurchase.horizontalHeaderItem(1)
        item.setText(_translate("PurchasingGeneralQuery_Window", "Nº Pedido"))
        item = self.tableQueryPurchase.horizontalHeaderItem(2)
        item.setText(_translate("PurchasingGeneralQuery_Window", "Fecha Pedido"))
        item = self.tableQueryPurchase.horizontalHeaderItem(3)
        item.setText(_translate("PurchasingGeneralQuery_Window", "Fecha Entrega Aprox."))
        item = self.tableQueryPurchase.horizontalHeaderItem(4)
        item.setText(_translate("PurchasingGeneralQuery_Window", "Fecha Entrega 1"))
        item = self.tableQueryPurchase.horizontalHeaderItem(5)
        item.setText(_translate("PurchasingGeneralQuery_Window", "Fecha Entrega 2"))
        item = self.tableQueryPurchase.horizontalHeaderItem(6)
        item.setText(_translate("PurchasingGeneralQuery_Window", "Fecha Entrega 3"))
        self.label_Order.setText(_translate("PurchasingGeneralQuery_Window", "Nº Pedido:"))
        self.Button_Delete.setText(_translate("PurchasingGeneralQuery_Window", "Ver Todos"))


    def delete_all_filters(self):
        for column in range(self.tableQueryPurchase.columnCount()):
            if column in self.tableQueryPurchase.rows_hidden:
                for item in self.tableQueryPurchase.rows_hidden[column]:
                    self.tableQueryPurchase.setRowHidden(item, False)
            header_item = self.tableQueryPurchase.horizontalHeaderItem(column)
            header_item.setIcon(QtGui.QIcon())

        self.tableQueryPurchase.list_filters=[]
        self.tableQueryPurchase.column_filters = {}
        self.tableQueryPurchase.column_actions = {}
        self.tableQueryPurchase.checkbox_states = {}
        self.tableQueryPurchase.rows_hidden = {}
        self.tableQueryPurchase.general_rows_to_hide = set()


    def query_all(self):
        self.tableQueryPurchase.setRowCount(0)

        commands_query_all = ("""
                        (SELECT purchase."id", purchase."notes", TO_CHAR(purchase."order_date",'dd/MM/yyyy'), TO_CHAR(purchase."delivery_date",'dd/MM/yyyy'),
                        TO_CHAR(purchase."deliv_date_1",'dd/MM/yyyy'), TO_CHAR(purchase."deliv_date_2",'dd/MM/yyyy'), TO_CHAR(purchase."deliv_date_3",'dd/MM/yyyy')
                        FROM purch_fact.supplier_ord_header AS purchase
                        ORDER BY purchase."order_date" DESC)
                        """)

        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            cur.execute(commands_query_all)
            results=cur.fetchall()
            self.tableQueryPurchase.setRowCount(len(results))
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(7):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableQueryPurchase.setItem(tablerow, column, it)

                self.tableQueryPurchase.setItemDelegateForRow(tablerow, AlignDelegate(self.tableQueryPurchase))
                tablerow+=1

            self.tableQueryPurchase.verticalHeader().hide()
            self.tableQueryPurchase.setSortingEnabled(False)
            self.tableQueryPurchase.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)


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


    def query_filtered(self):
        self.tableQueryPurchase.setRowCount(0)
        order = self.Order_Query.text()

        commands_query_filtered = ("""
                        (SELECT purchase."id", purchase."notes", TO_CHAR(purchase."order_date",'dd/MM/yyyy'), TO_CHAR(purchase."delivery_date",'dd/MM/yyyy'),
                        TO_CHAR(purchase."deliv_date_1",'dd/MM/yyyy'), TO_CHAR(purchase."deliv_date_2",'dd/MM/yyyy'), TO_CHAR(purchase."deliv_date_3",'dd/MM/yyyy')
                        FROM purch_fact.supplier_ord_header AS purchase
                        WHERE UPPER(purchase."notes") LIKE UPPER('%%'||%s||'%%')
                        ORDER BY purchase."order_date" DESC)
                        """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            data=(order,)
            cur.execute(commands_query_filtered, data)

            results=cur.fetchall()
            self.tableQueryPurchase.setRowCount(len(results))
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(7):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableQueryPurchase.setItem(tablerow, column, it)

                self.tableQueryPurchase.setItemDelegateForRow(tablerow, AlignDelegate(self.tableQueryPurchase))
                tablerow+=1

            self.tableQueryPurchase.verticalHeader().hide()
            self.tableQueryPurchase.setSortingEnabled(False)
            self.tableQueryPurchase.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)


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


    def countSelectedCells(self):
        if len(self.tableQueryPurchase.selectedIndexes()) > 1:
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
            self.label_SumItems.setText("")
            self.label_SumValue.setText("")
            self.label_CountItems.setText("")
            self.label_CountValue.setText("")

            sum_value = sum([self.euro_string_to_float(ix.data()) if (ix.data() is not None and (re.match(r'^[\d.,]+\s€$', ix.data()) and ix.column() == 7))
                            else (float(ix.data()) if (ix.data() is not None and ix.data().replace(',', '.', 1).replace('.', '', 1).isdigit() and ix.column() == 7) else 0) for ix in self.tableQueryPurchase.selectedIndexes()])
            count_value = len([ix for ix in self.tableQueryPurchase.selectedIndexes() if ix.data() != ""])
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


    def euro_string_to_float(self, euro_str):
        match = re.match(r'^([\d.,]+)\s€$', euro_str)
        if match:
            number_str = match.group(1)
            number_str = number_str.replace('.', '').replace(',', '.')
            return float(number_str)
        else:
            return 0.0


    def on_item_double_clicked(self, item):
        from PurchasingDetailQuery_Window import Ui_PurchasingDetailQuery_Window
        row_selected = item.row()
        id_purchase=self.tableQueryPurchase.item(row_selected, 0).text()
        self.purchasedetail_query_window=QtWidgets.QMainWindow()
        self.ui=Ui_PurchasingDetailQuery_Window(id_purchase)
        self.ui.setupUi(self.purchasedetail_query_window)
        self.purchasedetail_query_window.showMaximized()


    def export_data(self):
        if self.tableQueryPurchase.rowCount() > 0:
            df = pd.DataFrame()
            for col in range(self.tableQueryPurchase.columnCount()):
                header = self.tableQueryPurchase.horizontalHeaderItem(col).text()
                column_data = []
                for row in range(self.tableQueryPurchase.rowCount()):
                    if not self.tableQueryPurchase.isRowHidden(row):
                        item = self.tableQueryPurchase.item(row,col)
                        if item is not None:
                            if col in [11, 13, 14]:  # date column
                                date_str = item.text()
                                if date_str:  
                                    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                                    column_data.append(date_obj)
                                else:
                                    column_data.append('')
                            elif col in [7]:  # currency columns
                                currency_str = item.text()
                                if currency_str:
                                    currency_str=currency_str.replace(".","")
                                    currency_str=currency_str.replace(",",".")
                                    currency_str=currency_str[:currency_str.find(" €")]
                                    currency_value = float(currency_str)
                                    column_data.append(currency_value)
                                else:
                                    column_data.append('')
                            elif col in [10]:  # integer columns
                                integer_str = item.text()
                                if integer_str:
                                    integer_value = int(integer_str)
                                    column_data.append(integer_value)
                                else:
                                    column_data.append('')
                            else:
                                column_data.append(item.text())
                        else:
                            column_data.append('')
                df[header] = column_data

            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])

            if file_path:
                # df.to_excel(file_path, index=False)
                writer = pd.ExcelWriter(file_path, engine='openpyxl')
                df.to_excel(writer, index=False, sheet_name='Sheet1')

                # Set date format
                date_style = NamedStyle(name='date_style', number_format='DD/MM/YYYY')
                currency_style  = NamedStyle(name='currency_style ', number_format='#,##0.00" €"')
                for col_num in range(1, self.tableQueryPurchase.columnCount() + 1):
                    if col_num in [12,14,15]:  
                        for row_num in range(2, self.tableQueryPurchase.rowCount() + 2):
                            cell = writer.sheets['Sheet1'].cell(row=row_num, column=col_num)
                            cell.style = date_style

                    elif col_num in [8]:  
                        for row_num in range(2, self.tableQueryPurchase.rowCount() + 2):
                            cell = writer.sheets['Sheet1'].cell(row=row_num, column=col_num)
                            cell.style = currency_style

                writer._save()

            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Consultar Oferta")
            dlg.setText("Datos exportados con éxito")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            dlg.exec()
            del dlg,new_icon

        else:
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Consultar Oferta")
            dlg.setText("No hay datos para exportar")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            del dlg,new_icon


#Function when clicking on table header
    def on_header_section_clicked(self, logical_index):
        header_pos = self.tableQueryPurchase.horizontalHeader().sectionViewportPosition(logical_index)
        header_height = self.tableQueryPurchase.horizontalHeader().height()
        popup_pos = self.tableQueryPurchase.viewport().mapToGlobal(QtCore.QPoint(header_pos, header_height))
        self.tableQueryPurchase.show_unique_values_menu(logical_index, popup_pos, header_height)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PurchasingGeneralQuery_Window = Ui_PurchasingGeneralQuery_Window()
    PurchasingGeneralQuery_Window.show()
    sys.exit(app.exec())
