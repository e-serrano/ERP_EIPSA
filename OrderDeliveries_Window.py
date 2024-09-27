# Form implementation generated from reading ui file 'DeliveriesOrder_Window.ui'
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
import tkinter as tk
from tkinter import filedialog
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QTextDocument, QTextCursor
from PyQt6.QtCore import Qt
import os
from datetime import *
from openpyxl import Workbook
from openpyxl.styles import NamedStyle

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


class Ui_DeliveriesOrder_Window(QtWidgets.QMainWindow):
    """
    UI class for the Deliveries Order window.
    """
    def __init__(self, num_order):
        """
        Initializes the Ui_DeliveriesOrder_Window with the specified order number.

        Args:
            num_order (str): order number associated with the window.
        """
        super().__init__()
        self.numorder = num_order
        self.setupUi(self)

    def setupUi(self, DeliveriesOrder_Window):
        """
        Sets up the user interface for the DeliveriesOrder_Window.

        Args:
            DeliveriesOrder_Window (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        DeliveriesOrder_Window.setObjectName("DeliveriesOrder_Window")
        DeliveriesOrder_Window.resize(950, 700)
        DeliveriesOrder_Window.setMinimumSize(QtCore.QSize(950, 700))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        DeliveriesOrder_Window.setWindowIcon(icon)
        DeliveriesOrder_Window.setStyleSheet("QWidget {\n"
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
"  padding: 4px .8em;\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=DeliveriesOrder_Window)
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
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(10)
        self.gridLayout_3.setHorizontalSpacing(6)
        # self.label_NumOrder = QtWidgets.QLabel(parent=self.frame)
        # self.label_NumOrder.setMinimumSize(QtCore.QSize(80, 25))
        # self.label_NumOrder.setMaximumSize(QtCore.QSize(80, 25))
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # font.setBold(True)
        # self.label_NumOrder.setFont(font)
        # self.label_NumOrder.setObjectName("label_NumOrder")
        # self.gridLayout_3.addWidget(self.label_NumOrder, 0, 0, 1, 1)
        # self.Numorder_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        # self.Numorder_QueryOrder.setMinimumSize(QtCore.QSize(350, 25))
        # self.Numorder_QueryOrder.setMaximumSize(QtCore.QSize(350, 25))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.Numorder_QueryOrder.setFont(font)
        # self.Numorder_QueryOrder.setObjectName("Numorder_QueryOrder")
        # self.gridLayout_3.addWidget(self.Numorder_QueryOrder, 0, 1, 1, 1)
        # self.label_FinalClient = QtWidgets.QLabel(parent=self.frame)
        # self.label_FinalClient.setMinimumSize(QtCore.QSize(90, 25))
        # self.label_FinalClient.setMaximumSize(QtCore.QSize(90, 25))
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # font.setBold(True)
        # self.label_FinalClient.setFont(font)
        # self.label_FinalClient.setObjectName("label_FinalClient")
        # self.gridLayout_3.addWidget(self.label_FinalClient, 0, 2, 1, 1)
        # self.Finalclient_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        # self.Finalclient_QueryOrder.setMinimumSize(QtCore.QSize(250, 25))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.Finalclient_QueryOrder.setFont(font)
        # self.Finalclient_QueryOrder.setObjectName("Finalclient_QueryOrder")
        # self.gridLayout_3.addWidget(self.Finalclient_QueryOrder, 0, 3, 1, 3)
        # self.label_NumOffer = QtWidgets.QLabel(parent=self.frame)
        # self.label_NumOffer.setMinimumSize(QtCore.QSize(80, 25))
        # self.label_NumOffer.setMaximumSize(QtCore.QSize(80, 25))
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # font.setBold(True)
        # self.label_NumOffer.setFont(font)
        # self.label_NumOffer.setObjectName("label_NumOffer")
        # self.gridLayout_3.addWidget(self.label_NumOffer, 1, 0, 1, 1)
        # self.Numoffer_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        # self.Numoffer_QueryOrder.setMinimumSize(QtCore.QSize(350, 25))
        # self.Numoffer_QueryOrder.setMaximumSize(QtCore.QSize(350, 25))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.Numoffer_QueryOrder.setFont(font)
        # self.Numoffer_QueryOrder.setObjectName("Numoffer_QueryOrder")
        # self.gridLayout_3.addWidget(self.Numoffer_QueryOrder, 1, 1, 1, 1)
        # self.label_EqType = QtWidgets.QLabel(parent=self.frame)
        # self.label_EqType.setMinimumSize(QtCore.QSize(90, 25))
        # self.label_EqType.setMaximumSize(QtCore.QSize(90, 25))
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # font.setBold(True)
        # self.label_EqType.setFont(font)
        # self.label_EqType.setObjectName("label_EqType")
        # self.gridLayout_3.addWidget(self.label_EqType, 1, 2, 1, 1)
        # self.EqType_QueryOrder = QtWidgets.QComboBox(parent=self.frame)
        # self.EqType_QueryOrder.setMinimumSize(QtCore.QSize(250, 25))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.EqType_QueryOrder.setFont(font)
        # self.EqType_QueryOrder.setObjectName("EqType_QueryOrder")
        # self.gridLayout_3.addWidget(self.EqType_QueryOrder, 1, 3, 1, 3)
        # self.label_RefNum = QtWidgets.QLabel(parent=self.frame)
        # self.label_RefNum.setMinimumSize(QtCore.QSize(80, 25))
        # self.label_RefNum.setMaximumSize(QtCore.QSize(80, 25))
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # font.setBold(True)
        # self.label_RefNum.setFont(font)
        # self.label_RefNum.setObjectName("label_RefNum")
        # self.gridLayout_3.addWidget(self.label_RefNum, 2, 0, 1, 1)
        # self.Ref_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        # self.Ref_QueryOrder.setMinimumSize(QtCore.QSize(350, 25))
        # self.Ref_QueryOrder.setMaximumSize(QtCore.QSize(350, 25))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.Ref_QueryOrder.setFont(font)
        # self.Ref_QueryOrder.setObjectName("Ref_QueryOrder")
        # self.gridLayout_3.addWidget(self.Ref_QueryOrder, 2, 1, 1, 1)
        # self.label_Months= QtWidgets.QLabel(parent=self.frame)
        # self.label_Months.setMinimumSize(QtCore.QSize(90, 25))
        # self.label_Months.setMaximumSize(QtCore.QSize(90, 25))
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # font.setBold(True)
        # self.label_Months.setFont(font)
        # self.label_Months.setObjectName("label_Months")
        # self.gridLayout_3.addWidget(self.label_Months, 2, 2, 1, 1)
        # self.Month1_QueryOrder = QtWidgets.QComboBox(parent=self.frame)
        # self.Month1_QueryOrder.setMinimumSize(QtCore.QSize(120, 25))
        # self.Month1_QueryOrder.setMaximumSize(QtCore.QSize(120, 25))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.Month1_QueryOrder.setFont(font)
        # self.Month1_QueryOrder.setObjectName("Month1_QueryOrder")
        # self.gridLayout_3.addWidget(self.Month1_QueryOrder, 2, 3, 1, 1)
        # self.Month2_QueryOrder = QtWidgets.QComboBox(parent=self.frame)
        # self.Month2_QueryOrder.setMinimumSize(QtCore.QSize(120, 25))
        # self.Month2_QueryOrder.setMaximumSize(QtCore.QSize(120, 25))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.Month2_QueryOrder.setFont(font)
        # self.Month2_QueryOrder.setObjectName("Month2_QueryOrder")
        # self.gridLayout_3.addWidget(self.Month2_QueryOrder, 2, 4, 1, 1)
        # self.Year_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        # self.Year_QueryOrder.setMinimumSize(QtCore.QSize(120, 25))
        # self.Year_QueryOrder.setMaximumSize(QtCore.QSize(120, 25))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.Year_QueryOrder.setFont(font)
        # self.Year_QueryOrder.setObjectName("Year_QueryOrder")
        # self.gridLayout_3.addWidget(self.Year_QueryOrder, 2, 5, 1, 1)
        # self.label_Client = QtWidgets.QLabel(parent=self.frame)
        # self.label_Client.setMinimumSize(QtCore.QSize(80, 25))
        # self.label_Client.setMaximumSize(QtCore.QSize(80, 25))
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # font.setBold(True)
        # self.label_Client.setFont(font)
        # self.label_Client.setObjectName("label_Client")
        # self.gridLayout_3.addWidget(self.label_Client, 3, 0, 1, 1)
        # self.Client_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        # self.Client_QueryOrder.setMinimumSize(QtCore.QSize(350, 25))
        # self.Client_QueryOrder.setMaximumSize(QtCore.QSize(350, 25))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.Client_QueryOrder.setFont(font)
        # self.Client_QueryOrder.setObjectName("Client_QueryOrder")
        # self.gridLayout_3.addWidget(self.Client_QueryOrder, 3, 1, 1, 1)
        # self.label_Amount = QtWidgets.QLabel(parent=self.frame)
        # self.label_Amount.setMinimumSize(QtCore.QSize(90, 25))
        # self.label_Amount.setMaximumSize(QtCore.QSize(90, 25))
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # font.setBold(True)
        # self.label_Amount.setFont(font)
        # self.label_Amount.setObjectName("label_Amount")
        # self.gridLayout_3.addWidget(self.label_Amount, 3, 2, 1, 1)
        # self.Amount_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        # self.Amount_QueryOrder.setMinimumSize(QtCore.QSize(250, 25))
        # font = QtGui.QFont()
        # font.setPointSize(10)
        # self.Amount_QueryOrder.setFont(font)
        # self.Amount_QueryOrder.setObjectName("Amount_QueryOrder")
        # self.gridLayout_3.addWidget(self.Amount_QueryOrder, 3, 3, 1, 3)
        # self.gridLayout_2.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        # spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        # self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        # self.hLayout5 = QtWidgets.QHBoxLayout()
        # self.hLayout5.setObjectName("hLayout5")
        # self.Button_Clean = QtWidgets.QPushButton(parent=self.frame)
        # self.Button_Clean.setMinimumSize(QtCore.QSize(150, 30))
        # self.Button_Clean.setMaximumSize(QtCore.QSize(150, 30))
        # self.Button_Clean.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        # self.Button_Clean.setObjectName("Button_Clean")
        # self.hLayout5.addWidget(self.Button_Clean)
        # self.Button_Query = QtWidgets.QPushButton(parent=self.frame)
        # self.Button_Query.setMinimumSize(QtCore.QSize(150, 30))
        # self.Button_Query.setMaximumSize(QtCore.QSize(150, 30))
        # self.Button_Query.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        # self.Button_Query.setObjectName("Button_Query")
        # self.hLayout5.addWidget(self.Button_Query)
        # self.Button_Export = QtWidgets.QPushButton(parent=self.frame)
        # self.Button_Export.setMinimumSize(QtCore.QSize(150, 30))
        # self.Button_Export.setMaximumSize(QtCore.QSize(150, 30))
        # self.Button_Export.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        # self.Button_Export.setObjectName("Button_Export")
        # self.hLayout5.addWidget(self.Button_Export)
        # self.gridLayout_2.addLayout(self.hLayout5, 4, 0, 1, 1)
        # spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        # self.gridLayout_2.addItem(spacerItem2, 5, 0, 1, 1)
        self.tableQueryOrder = QtWidgets.QTableWidget(parent=self.frame)
        self.tableQueryOrder.setAlternatingRowColors(False)
        self.tableQueryOrder.setObjectName("tableQueryOrder")
        self.tableQueryOrder.setColumnCount(9)
        self.tableQueryOrder.setRowCount(0)
        for i in range(9):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            item.setFont(font)
            self.tableQueryOrder.setHorizontalHeaderItem(i, item)
        self.tableQueryOrder.setSortingEnabled(True)
        self.tableQueryOrder.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_2.addWidget(self.tableQueryOrder, 5, 0, 1, 1)
        # self.hLayout6 = QtWidgets.QHBoxLayout()
        # self.hLayout6.setObjectName("hLayout6")
        # spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        # self.hLayout6.addItem(spacerItem3)
        # self.label_SumItems = QtWidgets.QLabel(parent=self.frame)
        # self.label_SumItems.setMinimumSize(QtCore.QSize(40, 10))
        # self.label_SumItems.setMaximumSize(QtCore.QSize(40, 10))
        # self.label_SumItems.setText("")
        # self.label_SumItems.setObjectName("label_SumItems")
        # self.hLayout6.addWidget(self.label_SumItems)
        # self.label_SumValue = QtWidgets.QLabel(parent=self.frame)
        # self.label_SumValue.setMinimumSize(QtCore.QSize(80, 20))
        # self.label_SumValue.setMaximumSize(QtCore.QSize(80, 20))
        # self.label_SumValue.setText("")
        # self.label_SumValue.setObjectName("label_SumValue")
        # self.hLayout6.addWidget(self.label_SumValue)
        # self.label_CountItems = QtWidgets.QLabel(parent=self.frame)
        # self.label_CountItems.setMinimumSize(QtCore.QSize(60, 10))
        # self.label_CountItems.setMaximumSize(QtCore.QSize(60, 10))
        # self.label_CountItems.setText("")
        # self.label_CountItems.setObjectName("label_CountItems")
        # self.hLayout6.addWidget(self.label_CountItems)
        # self.label_CountValue = QtWidgets.QLabel(parent=self.frame)
        # self.label_CountValue.setMinimumSize(QtCore.QSize(80, 10))
        # self.label_CountValue.setMaximumSize(QtCore.QSize(80, 10))
        # self.label_CountValue.setText("")
        # self.label_CountValue.setObjectName("label_CountValue")
        # self.hLayout6.addWidget(self.label_CountValue)
        # self.gridLayout_2.addLayout(self.hLayout6, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        DeliveriesOrder_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=DeliveriesOrder_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 22))
        self.menubar.setObjectName("menubar")
        DeliveriesOrder_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=DeliveriesOrder_Window)
        self.statusbar.setObjectName("statusbar")
        DeliveriesOrder_Window.setStatusBar(self.statusbar)
        self.tableQueryOrder.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        # commands_comboboxes1queryoffer = ("""
        #                 SELECT *
        #                 FROM product_type
        #                 """)
        # conn = None
        # try:
        # # read the connection parameters
        #     params = config()
        # # connect to the PostgreSQL server
        #     conn = psycopg2.connect(**params)
        #     cur = conn.cursor()
        # # execution of commands one by one
        #     cur.execute(commands_comboboxes1queryoffer)
        #     results1=cur.fetchall()
        # # close communication with the PostgreSQL database server
        #     cur.close()
        # # commit the changes
        #     conn.commit()
        # except (Exception, psycopg2.DatabaseError) as error:
        #     dlg = QtWidgets.QMessageBox()
        #     new_icon = QtGui.QIcon()
        #     new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        #     dlg.setWindowIcon(new_icon)
        #     dlg.setWindowTitle("ERP EIPSA")
        #     dlg.setText("Ha ocurrido el siguiente error:\n"
        #                 + str(error))
        #     dlg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        #     dlg.exec()
        #     del dlg, new_icon
        # finally:
        #     if conn is not None:
        #         conn.close()

        # list_material=[''] + list(set([x[1] for x in results1]))
        # self.EqType_QueryOrder.addItems(sorted(list_material))

        # list_months = [''] + [str(x) for x in range(1,13)]
        # self.Month1_QueryOrder.addItems(list_months)
        # self.Month2_QueryOrder.addItems(list_months)

        self.retranslateUi(DeliveriesOrder_Window)
        QtCore.QMetaObject.connectSlotsByName(DeliveriesOrder_Window)
        # self.Button_Clean.clicked.connect(self.clean_boxes) # type: ignore
        # self.Button_Query.clicked.connect(self.query_order) # type: ignore
        # self.Button_Export.clicked.connect(self.export_data)  # type: ignore
        # self.Numorder_QueryOrder.returnPressed.connect(self.query_order)
        # self.Numoffer_QueryOrder.returnPressed.connect(self.query_order)
        # self.Ref_QueryOrder.returnPressed.connect(self.query_order)
        # self.Client_QueryOrder.returnPressed.connect(self.query_order)
        # self.Finalclient_QueryOrder.returnPressed.connect(self.query_order)
        # self.Amount_QueryOrder.returnPressed.connect(self.query_order)
        # self.EqType_QueryOrder.currentIndexChanged.connect(self.query_order)
        # self.Month1_QueryOrder.currentIndexChanged.connect(self.query_order)
        # self.Month2_QueryOrder.currentIndexChanged.connect(self.query_order)
        # self.Year_QueryOrder.returnPressed.connect(self.query_order)
        # self.tableQueryOrder.itemSelectionChanged.connect(self.countSelectedCells)
        self.tableQueryOrder.itemDoubleClicked.connect(self.expand_cell)

        self.query_order()


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, DeliveriesOrder_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        DeliveriesOrder_Window.setWindowTitle(_translate("DeliveriesOrder_Window", "Consultar Pedido"))
        self.tableQueryOrder.setSortingEnabled(True)
        item = self.tableQueryOrder.horizontalHeaderItem(0)
        item.setText(_translate("DeliveriesOrder_Window", "Nº Pedido"))
        item = self.tableQueryOrder.horizontalHeaderItem(1)
        item.setText(_translate("DeliveriesOrder_Window", "Nº Factura"))
        item = self.tableQueryOrder.horizontalHeaderItem(2)
        item.setText(_translate("DeliveriesOrder_Window", "Nº Albarán"))
        item = self.tableQueryOrder.horizontalHeaderItem(3)
        item.setText(_translate("DeliveriesOrder_Window", "Destino"))
        item = self.tableQueryOrder.horizontalHeaderItem(4)
        item.setText(_translate("DeliveriesOrder_Window", "Bultos"))
        item = self.tableQueryOrder.horizontalHeaderItem(5)
        item.setText(_translate("DeliveriesOrder_Window", "Peso"))
        item = self.tableQueryOrder.horizontalHeaderItem(6)
        item.setText(_translate("DeliveriesOrder_Window", "Descripción"))
        item = self.tableQueryOrder.horizontalHeaderItem(7)
        item.setText(_translate("DeliveriesOrder_Window", "Transporte"))
        item = self.tableQueryOrder.horizontalHeaderItem(8)
        item.setText(_translate("DeliveriesOrder_Window", "Fecha"))


    def query_order(self):
        """
        Queries the database of desired data for selected order, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.tableQueryOrder.setRowCount(0)
        commands_queryorder = ("""
                    SELECT dispatch."our_ref", dispatch."num_invoice", dispatch."num_delivnote", dispatch."destination_dispatch", dispatch."boxes_dispatch", dispatch."weight_dispatch", dispatch."description_dispatch", dispatch."transportation_dispatch", dispatch."date_dispatch"
                    FROM purch_fact.invoice_header AS dispatch
                    WHERE (UPPER(dispatch."our_ref") LIKE UPPER('%%'||%s||'%%')
                    )
                    ORDER BY dispatch."our_ref"
                    """)
        
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            data=(self.numorder,)
            cur.execute(commands_queryorder, data)
            results=cur.fetchall()

            self.tableQueryOrder.setRowCount(len(results))
            tablerow=0

        # fill the Qt Table with the query results
            for row in results:
                for column in range(9):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableQueryOrder.setItem(tablerow, column, it)

                tablerow+=1

            # self.tableQueryOrder.verticalHeader().hide()
            self.tableQueryOrder.setItemDelegate(AlignDelegate(self.tableQueryOrder))
            self.tableQueryOrder.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.tableQueryOrder.horizontalHeader().setSectionResizeMode(8,QtWidgets.QHeaderView.ResizeMode.Stretch)

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
        if item.column() in [6]:
            cell_content = item.text()
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Pedidos")
            dlg.setText(cell_content)
            dlg.exec()

    def export_data(self):
        """
        Exports the visible data from the table to an Excel file. If no data is loaded, displays a warning message.
        """
        num_rows = self.tableQueryOrder.rowCount()
        if num_rows > 0:
            num_columns = 12

            column_names = [self.tableQueryOrder.horizontalHeaderItem(col).text() for col in range(num_columns)]

            df = pd.DataFrame(columns=column_names)

            for row in range(num_rows):
                row_data = []
                for col in range(num_columns):
                    item = self.tableQueryOrder.item(row,col)
                    if item is not None:
                        if col == 3:  # date column
                            date_str = item.text()
                            if date_str:  
                                date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                                row_data.append(date_obj)
                            else:
                                row_data.append('')
                        elif col in [11,12]:  # currency columns
                            currency_str = item.text()
                            if currency_str:
                                currency_str=currency_str.replace(".","")
                                currency_str=currency_str.replace(",",".")
                                currency_str=currency_str[:currency_str.find(" €")]
                                currency_value = float(currency_str)
                                row_data.append(currency_value)
                            else:
                                row_data.append('')
                        else:
                            row_data.append(item.text())
                    else:
                        row_data.append('')
                df.loc[row] = row_data

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
                for col_num in range(1, num_columns + 1):
                    if col_num == 4:  
                        for row_num in range(2, num_rows + 2):
                            cell = writer.sheets['Sheet1'].cell(row=row_num, column=col_num)
                            cell.style = date_style

                    elif col_num in [12,13]:  
                        for row_num in range(2, num_rows + 2):
                            cell = writer.sheets['Sheet1'].cell(row=row_num, column=col_num)
                            cell.style = currency_style

                writer._save()


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     DeliveriesOrder_Window = Ui_DeliveriesOrder_Window('P-23/001')
#     DeliveriesOrder_Window.show()
#     sys.exit(app.exec())
