from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtSql
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QTextDocument, QTextCursor
from Create_FabOrder_Window import Ui_CreateFabOrder_Window
from Create_MatOrder import flow_matorder, temp_matorder, level_matorder
from Create_Inspection import inspection
from Database_Connection import createConnection
from config import config
import psycopg2
import re
import configparser
import locale
from datetime import *
import os
import pandas as pd
from tkinter.filedialog import asksaveasfilename
from PyQt6.QtCore import QDate

basedir = os.path.dirname(__file__)

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter


class EditableTableModel(QtSql.QSqlTableModel):
    updateFailed = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, column_range=None):
        super().__init__(parent)
        self.column_range = column_range

    def setAllColumnHeaders(self, headers):
        for column, header in enumerate(headers):
            self.setHeaderData(column, Qt.Orientation.Horizontal, header, Qt.ItemDataRole.DisplayRole)

    def setIndividualColumnHeader(self, column, header):
        self.setHeaderData(column, Qt.Orientation.Horizontal, header, Qt.ItemDataRole.DisplayRole)

    def setIconColumnHeader(self, column, icon):
        self.setHeaderData(column, QtCore.Qt.Orientation.Horizontal, icon, Qt.ItemDataRole.DecorationRole)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return super().headerData(section, orientation, role)
        return super().headerData(section, orientation, role)

    def flags(self, index):
        flags = super().flags(index)
        if index.column() == 0:
            flags &= ~Qt.ItemFlag.ItemIsEditable
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        else:
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def getColumnHeaders(self, visible_columns):
        column_headers = [self.headerData(col, Qt.Orientation.Horizontal) for col in visible_columns]
        return column_headers


class Ui_Deliveries_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = EditableTableModel()
        self.setupUi(self)


    def setupUi(self, Deliveries_Window):
        self.id_list = []
        data_list = []
        Deliveries_Window.setObjectName("Deliveries_Window")
        Deliveries_Window.resize(400, 561)
        Deliveries_Window.setMinimumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(basedir, "Resources/Iconos/icon.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
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
        self.tableDeliveries=QtWidgets.QTableView(parent=self.frame)
        self.model = EditableTableModel()
        self.tableDeliveries.setObjectName("tableDeliveries")
        self.gridLayout_2.addWidget(self.tableDeliveries, 1, 0, 1, 1)
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
        self.model.setFilter("porc_deliveries <> 100 OR porc_deliveries IS NULL")
        self.model.select()
        self.tableDeliveries.setModel(self.model)

        for i in range(1,19):
            self.tableDeliveries.hideColumn(i)

        headers=['Nº Pedido', '','','','','','','','','','','','','','','','','','',
                '% Real Envío', 'Fecha Último Envío', 'Fecha Entregas Parciales', 'Observaciones']

        self.tableDeliveries.setItemDelegate(AlignDelegate(self.tableDeliveries))
        self.tableDeliveries.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableDeliveries.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_2.addWidget(self.tableDeliveries, 3, 0, 1, 1)

        self.model.setAllColumnHeaders(headers)

    def retranslateUi(self, Deliveries_Window):
        _translate = QtCore.QCoreApplication.translate
        Deliveries_Window.setWindowTitle(_translate("EditTags_Window", "Envíos"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    config_obj = configparser.ConfigParser()
    config_obj.read(r"C:\Program Files\ERP EIPSA\database.ini")
    dbparam = config_obj["postgresql"]
    # set your parameters for the database connection URI using the keys from the configfile.ini
    user_database = dbparam["user"]
    password_database = dbparam["password"]

    if not createConnection(user_database, password_database):
        sys.exit()

    Deliveries_Window = Ui_Deliveries_Window()
    Deliveries_Window.show()
    sys.exit(app.exec())