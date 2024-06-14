# Form implementation generated from reading ui file 'TAGQueryOthers_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from config import config
import psycopg2
import os
import re
from datetime import *

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

        menu.setStyleSheet("QMenu::item:selected { background-color: #33bdef; }"
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
            self.setRowHidden(row, row in self.general_rows_to_hide)

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
        if column_index in [4]:
            self.custom_sort(column_index, sortOrder)
        else:
            self.sortByColumn(column_index, sortOrder)


    def custom_sort(self, column, order):
    # Obtén la cantidad de filas en la tabla
        if column in [4]:
            row_count = self.rowCount()

            # Crea una lista de índices ordenados según las fechas
            indexes = list(range(row_count))
            indexes.sort(key=lambda i: float(self.item(i, column).text().replace(" €","").replace(".", "").replace(",", ".")) if self.item(i, column).text() else float('inf'))

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

        elif column in [7]:
            row_count = self.rowCount()

            # Crea una lista de índices ordenados según las fechas
            indexes = list(range(row_count))
            indexes.sort(key=lambda i: int(self.item(i, column).text()))

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

class Ui_TAGQueryOthers_Window(QtWidgets.QMainWindow):
    def __init__(self, role):
        super().__init__()
        self.role = role
        self.setupUi(self)


    def setupUi(self, TAGQueryOthers_Window):
        TAGQueryOthers_Window.setObjectName("TAGQueryOthers_Window")
        TAGQueryOthers_Window.resize(400, 561)
        TAGQueryOthers_Window.setMinimumSize(QtCore.QSize(1000, 675))
        # TAGQueryOthers_Window.setMaximumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        TAGQueryOthers_Window.setWindowIcon(icon)
        TAGQueryOthers_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=TAGQueryOthers_Window)
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
        self.label_tag = QtWidgets.QLabel(parent=self.frame)
        self.label_tag.setMinimumSize(QtCore.QSize(105, 25))
        self.label_tag.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_tag.setFont(font)
        self.label_tag.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_tag.setObjectName("label_tag")
        self.gridLayout_2.addWidget(self.label_tag, 1, 0, 1, 1)
        self.tag = QtWidgets.QLineEdit(parent=self.frame)
        self.tag.setMinimumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tag.setFont(font)
        self.tag.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.tag.setObjectName("tag")
        self.gridLayout_2.addWidget(self.tag, 1, 1, 1, 1)
        self.label_description = QtWidgets.QLabel(parent=self.frame)
        self.label_description.setMinimumSize(QtCore.QSize(105, 25))
        self.label_description.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_description.setFont(font)
        self.label_description.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_description.setObjectName("label_description")
        self.gridLayout_2.addWidget(self.label_description, 1, 2, 1, 1)
        self.description = QtWidgets.QLineEdit(parent=self.frame)
        self.description.setMinimumSize(QtCore.QSize(400, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.description.setFont(font)
        self.description.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.description.setObjectName("description")
        self.gridLayout_2.addWidget(self.description, 1, 3, 1, 1)
        self.label_code = QtWidgets.QLabel(parent=self.frame)
        self.label_code.setMinimumSize(QtCore.QSize(105, 25))
        self.label_code.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_code.setFont(font)
        self.label_code.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_code.setObjectName("label_code")
        self.gridLayout_2.addWidget(self.label_code, 1, 4, 1, 1)
        self.code = QtWidgets.QLineEdit(parent=self.frame)
        self.code.setMinimumSize(QtCore.QSize(400, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.code.setFont(font)
        self.code.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.code.setObjectName("code")
        self.gridLayout_2.addWidget(self.code, 1, 5, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 3, 1, 1, 1)
        self.tableTags = CustomTableWidget()
        self.tableTags.setObjectName("tableWidget")
        self.tableTags.setColumnCount(0)
        self.tableTags.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableTags, 5, 0, 1, 6)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 11, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        TAGQueryOthers_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=TAGQueryOthers_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        TAGQueryOthers_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=TAGQueryOthers_Window)
        self.statusbar.setObjectName("statusbar")
        TAGQueryOthers_Window.setStatusBar(self.statusbar)
        self.tableTags.verticalHeader().setVisible(True)
        self.tableTags.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableTags.setSortingEnabled(False)
        self.tableTags.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black; font-weight: bold; font-size: 10pt;}")
        # TAGQueryOthers_Window.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.retranslateUi(TAGQueryOthers_Window)
        QtCore.QMetaObject.connectSlotsByName(TAGQueryOthers_Window)

        self.tableTags.horizontalHeader().sectionDoubleClicked.connect(self.on_header_section_clicked)
        self.tag.returnPressed.connect(self.querytags_filtered)
        self.description.returnPressed.connect(self.querytags_filtered)
        self.code.returnPressed.connect(self.querytags_filtered)

        self.querytags()


    def retranslateUi(self, TAGQueryOthers_Window):
        _translate = QtCore.QCoreApplication.translate
        TAGQueryOthers_Window.setWindowTitle(_translate("TAGQueryOthers_Window", "Consultar TAG Otros"))
        self.label_tag.setText(_translate("TAGQueryOthers_Window", "TAG:"))
        self.label_description.setText(_translate("TAGQueryOthers_Window", "Descripción:"))
        self.label_code.setText(_translate("TAGQueryOthers_Window", "Código:"))

# Function to query tags
    def querytags(self):
        self.tableTags.setRowCount(0)
        query_material = ("""
                        SELECT tags."tag", tags."num_offer", tags."num_order", offers."client", tags."amount", tags."description", tags."code_equipment", tags."dim_drawing", tags."of_drawing"
                        FROM tags_data.tags_others AS tags
                        JOIN offers ON (offers."num_offer" = tags."num_offer")
                        ORDER BY tags."tag"
                        """)

        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute(query_material)
            results=cur.fetchall()

        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()

            self.tableTags.setRowCount(len(results))
            self.tableTags.setColumnCount(9)
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(9):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableTags.setItem(tablerow, column, it)

                tablerow+=1

            column_headers = ['TAG', 'Nº Oferta', 'Nº Pedido', 'Cliente', 'Precio', 'Descripción', 'Código', 'Nº Plano Dim.', 'Nº Plano OF']
            
            self.tableTags.verticalHeader().hide()
            self.tableTags.setItemDelegate(AlignDelegate(self.tableTags))
            self.tableTags.setSortingEnabled(False)
            self.tableTags.setHorizontalHeaderLabels(column_headers)
            self.tableTags.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            if self.role != 'Comercial':
                self.tableTags.hideColumn(4)

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

# Function to query tags when filters are applied
    def querytags_filtered(self):
        self.tableTags.setRowCount(0)

        tag = self.tag.text()
        description = self.description.text()
        code = self.code.text()

        query_material = ("""
                        SELECT tags."tag", tags."num_offer", tags."num_order", offers."client", tags."amount", tags."description", tags."code_equipment", tags."dim_drawing", tags."of_drawing"
                        FROM tags_data.tags_others AS tags
                        JOIN offers ON (offers."num_offer" = tags."num_offer")
                        WHERE (UPPER(tags."tag") LIKE UPPER('%%'||%s||'%%')
                        AND
                        UPPER(tags."description") LIKE UPPER('%%'||%s||'%%')
                        AND
                        UPPER(tags."code_equipment") LIKE UPPER('%%'||%s||'%%'))
                        ORDER BY tags."tag"
                        """)

        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            data = (tag, description, code,)
            cur.execute(query_material, data)
            results=cur.fetchall()

        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()

            self.tableTags.setRowCount(len(results))
            self.tableTags.setColumnCount(9)
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(9):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableTags.setItem(tablerow, column, it)

                tablerow+=1

            column_headers = ['TAG', 'Nº Oferta', 'Nº Pedido', 'Cliente', 'Precio', 'Descripción', 'Código', 'Nº Plano Dim.', 'Nº Plano OF']
            
            self.tableTags.verticalHeader().hide()
            self.tableTags.setItemDelegate(AlignDelegate(self.tableTags))
            self.tableTags.setSortingEnabled(False)
            self.tableTags.setHorizontalHeaderLabels(column_headers)
            self.tableTags.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            if self.role != 'Comercial':
                self.tableTags.hideColumn(4)

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

#Function when clicking on table header
    def on_header_section_clicked(self, logical_index):
        header_pos = self.tableTags.horizontalHeader().sectionViewportPosition(logical_index)
        header_height = self.tableTags.horizontalHeader().height()
        popup_pos = self.tableTags.viewport().mapToGlobal(QtCore.QPoint(header_pos, header_height))
        self.tableTags.show_unique_values_menu(logical_index, popup_pos, header_height)



# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     TAGQueryOthers_Window = Ui_TAGQueryOthers_Window('Comercial')
#     TAGQueryOthers_Window.show()
#     sys.exit(app.exec())