# Form implementation generated from reading ui file 'TestLiquidQuery_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from config import config
import psycopg2
import os
import locale
import re

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.colors_dict = self.get_colors_from_database()

    def get_colors_from_database(self):
        colors_dict = {}

        conn = None
        try:
            # read the connection parameters
            params = config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # execution of commands
            commands_colors = "SELECT state_verif, r_channel, g_channel, b_channel FROM verification.states_verification"
            cur.execute(commands_colors)
            results = cur.fetchall()

            for result in results:
                state, red, green, blue = result
                colors_dict[state] = QtGui.QColor(red, green, blue)

            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            # Handle the error appropriately
            pass
        finally:
            if conn is not None:
                conn.close()

        return colors_dict

    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter

        header_estado = "Estado"
        state_column = -1

        table_widget = option.widget

        for column in range(table_widget.columnCount()):
            header_item = table_widget.horizontalHeaderItem(column)
            if header_item and header_item.text() == header_estado:
                state_column = column
                break

        if index.column() == 2 and state_column != -1:
            state_column_index = index.sibling(index.row(), state_column)
            value = str(state_column_index.data())

            if value in self.colors_dict:
                text_color = self.colors_dict[value]
            else:
                text_color = QtGui.QColor(255, 255, 255)

            option.palette.setBrush(QtGui.QPalette.ColorRole.Text, text_color)


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
        if self.horizontalHeaderItem(column_index).text() == 'Fecha':
            self.custom_sort_date(column_index, sortOrder)
        elif self.horizontalHeaderItem(column_index).text() == 'Cantidad':
            self.custom_sort_int(column_index, sortOrder)
        else:
            self.sortByColumn(column_index, sortOrder)


    def custom_sort_date(self, column, order):
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

    def custom_sort_int(self, column, order):
    # Obtén la cantidad de filas en la tabla
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


class Ui_TestLiquidQuery_Window(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setupUi(self)


    def setupUi(self, TestLiquidQuery_Window):
        TestLiquidQuery_Window.setObjectName("TestLiquidQuery_Window")
        TestLiquidQuery_Window.resize(400, 561)
        TestLiquidQuery_Window.setMinimumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        TestLiquidQuery_Window.setWindowIcon(icon)
        if self.username == 'm.gil':
            TestLiquidQuery_Window.setStyleSheet("QWidget {\n"
"background-color: #121212; color: rgb(255, 255, 255)\n"
"}\n"
"\n"
".QFrame {\n"
"    border: 2px solid white;\n"
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
        else:
            TestLiquidQuery_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=TestLiquidQuery_Window)
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
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.gridLayout_2.addWidget(self.Button_Cancel, 1, 0, 1, 1)
        self.Button_All = QtWidgets.QPushButton(parent=self.frame)
        self.Button_All.setMinimumSize(QtCore.QSize(120, 35))
        self.Button_All.setMaximumSize(QtCore.QSize(120, 35))
        self.Button_All.setObjectName("Button_All")
        self.gridLayout_2.addWidget(self.Button_All, 1, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 2, 1, 1)
        self.tableTags = CustomTableWidget()
        self.tableTags.setObjectName("tableWidget")
        self.tableTags.setColumnCount(13)
        self.tableTags.setRowCount(0)
        for i in range (13):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            item.setFont(font)
            self.tableTags.setHorizontalHeaderItem(i, item)
        self.gridLayout_2.addWidget(self.tableTags, 2, 0, 1, 8)
        self.label_SumItems = QtWidgets.QLabel(parent=self.frame)
        self.label_SumItems.setMinimumSize(QtCore.QSize(40, 10))
        self.label_SumItems.setMaximumSize(QtCore.QSize(40, 10))
        self.label_SumItems.setText("")
        self.label_SumItems.setObjectName("label_SumItems")
        self.gridLayout_2.addWidget(self.label_SumItems, 3, 4, 1, 1)
        self.label_SumValue = QtWidgets.QLabel(parent=self.frame)
        self.label_SumValue.setMinimumSize(QtCore.QSize(80, 20))
        self.label_SumValue.setMaximumSize(QtCore.QSize(80, 20))
        self.label_SumValue.setText("")
        self.label_SumValue.setObjectName("label_SumValue")
        self.gridLayout_2.addWidget(self.label_SumValue, 3, 5, 1, 1)
        self.label_CountItems = QtWidgets.QLabel(parent=self.frame)
        self.label_CountItems.setMinimumSize(QtCore.QSize(60, 10))
        self.label_CountItems.setMaximumSize(QtCore.QSize(60, 10))
        self.label_CountItems.setText("")
        self.label_CountItems.setObjectName("label_CountItems")
        self.gridLayout_2.addWidget(self.label_CountItems, 3, 6, 1, 1)
        self.label_CountValue = QtWidgets.QLabel(parent=self.frame)
        self.label_CountValue.setMinimumSize(QtCore.QSize(80, 10))
        self.label_CountValue.setMaximumSize(QtCore.QSize(80, 10))
        self.label_CountValue.setText("")
        self.label_CountValue.setObjectName("label_CountValue")
        self.gridLayout_2.addWidget(self.label_CountValue, 3, 7, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        TestLiquidQuery_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=TestLiquidQuery_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        TestLiquidQuery_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=TestLiquidQuery_Window)
        self.statusbar.setObjectName("statusbar")
        TestLiquidQuery_Window.setStatusBar(self.statusbar)
        self.tableTags.verticalHeader().setVisible(True)
        self.tableTags.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableTags.setSortingEnabled(False)
        if self.username == 'm.gil':
            self.tableTags.setStyleSheet("gridline-color: rgb(128, 128, 128);")
            self.tableTags.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid white; font-weight: bold; font-size: 10pt;}")
        else:
            self.tableTags.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        TestLiquidQuery_Window.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.retranslateUi(TestLiquidQuery_Window)
        QtCore.QMetaObject.connectSlotsByName(TestLiquidQuery_Window)

        self.Button_Cancel.clicked.connect(TestLiquidQuery_Window.close)
        self.Button_All.clicked.connect(self.querytags_all)
        self.tableTags.horizontalHeader().sectionDoubleClicked.connect(self.on_header_section_clicked)
        self.tableTags.itemSelectionChanged.connect(self.countSelectedCells)
        self.tableTags.itemDoubleClicked.connect(self.double_click)
        self.querytags()


    def retranslateUi(self, TestLiquidQuery_Window):
        _translate = QtCore.QCoreApplication.translate
        TestLiquidQuery_Window.setWindowTitle(_translate("TestLiquidQuery_Window", "Líquidos Penetrantes"))
        item = self.tableTags.horizontalHeaderItem(0)
        item.setText(_translate("TestLiquidQuery_Window", "ID"))
        item = self.tableTags.horizontalHeaderItem(1)
        item.setText(_translate("TestLiquidQuery_Window", "Nº Pedido"))
        item = self.tableTags.horizontalHeaderItem(2)
        item.setText(_translate("TestLiquidQuery_Window", "TAG"))
        item = self.tableTags.horizontalHeaderItem(3)
        item.setText(_translate("TestLiquidQuery_Window", "Descripción"))
        item = self.tableTags.horizontalHeaderItem(4)
        item.setText(_translate("TestLiquidQuery_Window", "OF Equipo"))
        item = self.tableTags.horizontalHeaderItem(5)
        item.setText(_translate("TestLiquidQuery_Window", "OF Sensor"))
        item = self.tableTags.horizontalHeaderItem(6)
        item.setText(_translate("TestLiquidQuery_Window", "Fecha"))
        item = self.tableTags.horizontalHeaderItem(7)
        item.setText(_translate("TestLiquidQuery_Window", "9PR5"))
        item = self.tableTags.horizontalHeaderItem(8)
        item.setText(_translate("TestLiquidQuery_Window", "9D1B"))
        item = self.tableTags.horizontalHeaderItem(9)
        item.setText(_translate("TestLiquidQuery_Window", "996PB"))
        item = self.tableTags.horizontalHeaderItem(10)
        item.setText(_translate("TestLiquidQuery_Window", "Estado"))
        item = self.tableTags.horizontalHeaderItem(11)
        item.setText(_translate("TestLiquidQuery_Window", "Observaciones"))
        item = self.tableTags.horizontalHeaderItem(12)
        item.setText(_translate("TestLiquidQuery_Window", "Cantidad"))
        self.Button_Cancel.setText(_translate("TestLiquidQuery_Window", "Cancelar"))
        self.Button_All.setText(_translate("TestLiquidQuery_Window", "Ver Todos"))


    def querytags(self):
        self.tableTags.setRowCount(0)
        query_tags = ("""
                        SELECT id_tag_flow, num_order, tag, item_type, of_drawing, NULL as of_sensor_drawing, TO_CHAR(lp_date, 'DD/MM/YYYY'), lp_hn_liq1, lp_hn_liq2, lp_hn_liq3, lp_state, lp_obs, 1 FROM tags_data.tags_flow WHERE lp_date IS NOT NULL AND EXTRACT(YEAR FROM lp_date) IN (EXTRACT(YEAR FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE) - 1)
                        UNION
                        SELECT id_tag_temp, num_order, tag, item_type, of_drawing, of_sensor_drawing, TO_CHAR(lp_date, 'DD/MM/YYYY'), lp_hn_liq1, lp_hn_liq2, lp_hn_liq3, lp_state, lp_obs, 1 FROM tags_data.tags_temp WHERE lp_date IS NOT NULL AND EXTRACT(YEAR FROM lp_date) IN (EXTRACT(YEAR FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE) - 1)
                        UNION
                        SELECT id_tag_level, num_order, tag, item_type, of_drawing, NULL as of_sensor_drawing, TO_CHAR(lp_date, 'DD/MM/YYYY'), lp_hn_liq1, lp_hn_liq2, lp_hn_liq3, lp_state, lp_obs, 1 FROM tags_data.tags_level WHERE lp_date IS NOT NULL AND EXTRACT(YEAR FROM lp_date) IN (EXTRACT(YEAR FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE) - 1)
                        UNION
                        SELECT id_tag_others, num_order, tag, description, of_drawing, NULL as of_sensor_drawing, TO_CHAR(lp_date, 'DD/MM/YYYY'), lp_hn_liq1, lp_hn_liq2, lp_hn_liq3, lp_state, lp_obs, 1 FROM tags_data.tags_others WHERE lp_date IS NOT NULL AND EXTRACT(YEAR FROM lp_date) IN (EXTRACT(YEAR FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE) - 1)
                        UNION
                        SELECT id, num_order, tag, item_type, NULL as of_drawing, NULL as of_sensor_drawing, TO_CHAR(test_date, 'DD/MM/YYYY'), hn_liq1, hn_liq2, hn_liq3, test_state, obs, quantity FROM verification.test_liquid WHERE EXTRACT(YEAR FROM test_date) IN (EXTRACT(YEAR FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE) - 1)
                        """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            cur.execute(query_tags)
            results=cur.fetchall()

        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()

            self.tableTags.setRowCount(len(results))
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(13):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableTags.setItem(tablerow, column, it)

                tablerow+=1

            self.tableTags.verticalHeader().hide()
            self.tableTags.setItemDelegate(AlignDelegate(self.tableTags))
            self.tableTags.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
            self.tableTags.horizontalHeader().setMinimumSectionSize(120)
            self.tableTags.horizontalHeader().setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.tableTags.setColumnWidth(2, 200)
            self.tableTags.setSortingEnabled(False)
            self.tableTags.hideColumn(0)
            self.tableTags.custom_sort_date(6, QtCore.Qt.SortOrder.DescendingOrder)

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


    def querytags_all(self):
        self.tableTags.setRowCount(0)
        query_tags = ("""
                        SELECT id_tag_flow, num_order, tag, item_type, of_drawing, NULL as of_sensor_drawing, TO_CHAR(lp_date, 'DD/MM/YYYY'), lp_hn_liq1, lp_hn_liq2, lp_hn_liq3, lp_state, lp_obs, 1 FROM tags_data.tags_flow WHERE lp_date IS NOT NULL
                        UNION
                        SELECT id_tag_temp, num_order, tag, item_type, of_drawing, of_sensor_drawing, TO_CHAR(lp_date, 'DD/MM/YYYY'), lp_hn_liq1, lp_hn_liq2, lp_hn_liq3, lp_state, lp_obs, 1 FROM tags_data.tags_temp WHERE lp_date IS NOT NULL
                        UNION
                        SELECT id_tag_level, num_order, tag, item_type, of_drawing, NULL as of_sensor_drawing, TO_CHAR(lp_date, 'DD/MM/YYYY'), lp_hn_liq1, lp_hn_liq2, lp_hn_liq3, lp_state, lp_obs, 1 FROM tags_data.tags_level WHERE lp_date IS NOT NULL
                        UNION
                        SELECT id_tag_others, num_order, tag, description, of_drawing, NULL as of_sensor_drawing, TO_CHAR(lp_date, 'DD/MM/YYYY'), lp_hn_liq1, lp_hn_liq2, lp_hn_liq3, lp_state, lp_obs, 1 FROM tags_data.tags_others WHERE lp_date IS NOT NULL
                        UNION
                        SELECT id, num_order, tag, item_type, NULL as of_drawing, NULL as of_sensor_drawing, TO_CHAR(test_date, 'DD/MM/YYYY'), hn_liq1, hn_liq2, hn_liq3, test_state, obs, quantity FROM verification.test_liquid
                        """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            cur.execute(query_tags)
            results=cur.fetchall()

        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()

            self.tableTags.setRowCount(len(results))
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(13):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableTags.setItem(tablerow, column, it)

                tablerow+=1

            self.tableTags.verticalHeader().hide()
            self.tableTags.setItemDelegate(AlignDelegate(self.tableTags))
            self.tableTags.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
            self.tableTags.horizontalHeader().setMinimumSectionSize(120)
            self.tableTags.horizontalHeader().setSectionResizeMode(12, QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.tableTags.setColumnWidth(2, 200)
            self.tableTags.setSortingEnabled(False)
            self.tableTags.hideColumn(0)
            self.tableTags.custom_sort_date(6, QtCore.Qt.SortOrder.DescendingOrder)

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

    def double_click(self, item):
        if item.column() in [2]:
            self.expand_cell(item)
        else:
            self.edit_data(item)


    def edit_data(self, item):
        row = item.row()
        num_order = self.tableTags.item(row, 1).text()

        if num_order in ['ALMACÉN', 'ALMACEN', 'INTERNO', 'PROTOTIPOS']:
            from TestLiquidEdit_Window import Ui_TestLiquidEdit_Window
            id_item = self.tableTags.item(row, 0).text()
            num_order = self.tableTags.item(row, 1).text()
            tag = self.tableTags.item(row, 2).text()
            description = self.tableTags.item(row, 3).text()
            test_date = self.tableTags.item(row, 6).text()
            liq1 = self.tableTags.item(row, 7).text()
            liq2 = self.tableTags.item(row, 8).text()
            liq3 = self.tableTags.item(row, 9).text()
            state = self.tableTags.item(row, 10).text()
            obs = self.tableTags.item(row, 11).text()
            qty = self.tableTags.item(row, 12).text()

            self.edit_testliquid_window=QtWidgets.QMainWindow()
            self.ui=Ui_TestLiquidEdit_Window(self.username, id_item, num_order, tag, description, test_date, liq1, liq2, liq3, state, qty, obs)
            self.ui.setupUi(self.edit_testliquid_window)
            self.edit_testliquid_window.show()
            self.ui.Button_Cancel.clicked.connect(self.querytags)


    def expand_cell(self, item):
        cell_content = item.text()
        dlg = QtWidgets.QMessageBox()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle("Pruebas")
        dlg.setText(cell_content)
        dlg.exec()

    
    def countSelectedCells(self):
        if len(self.tableTags.selectedIndexes()) > 1:
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
            self.label_SumItems.setText("")
            self.label_SumValue.setText("")
            self.label_CountItems.setText("")
            self.label_CountValue.setText("")

            sum_value = sum([(float(ix.data()) if (ix.data() is not None and ix.data().replace(',', '.', 1).replace('.', '', 1).isdigit() and ix.column() == 12) else 0) for ix in self.tableTags.selectedIndexes()])
            count_value = len([ix for ix in self.tableTags.selectedIndexes() if ix.data() != ""])
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


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     TestLiquidQuery_Window = Ui_TestLiquidQuery_Window('m.gil')
#     TestLiquidQuery_Window.show()
#     sys.exit(app.exec())