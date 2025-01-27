# Form implementation generated from reading ui file 'NewOrder_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from datetime import *
import psycopg2
from config import config
import os
import re
from MoneyChange import obtain_money_change


basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class Ui_New_Order_Window(object):
    """
    UI class for the New Order window.
    """
    def __init__(self, num_offer):
        """
        Initializes the Ui_NewOffer_Menu with the specified offer number.

        Args:
            num_offer (str): offer number associated with the window.
        """
        self.num_offer = num_offer

    def setupUi(self, New_Order):
        """
        Sets up the user interface for the New_Order.

        Args:
            New_Order (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        New_Order.setObjectName("New_Order")
        New_Order.resize(680, 425)
        New_Order.setMinimumSize(QtCore.QSize(775, 425))
        New_Order.setMaximumSize(QtCore.QSize(775, 425))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        New_Order.setWindowIcon(icon)
        New_Order.setStyleSheet("QWidget {\n"
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
"}\n"
"\n"
"QPushButton:focus{\n"
"    background-color: #019ad2;\n"
"    border-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:focus:pressed {\n"
"    background-color: rgb(1, 140, 190);\n"
"    border-color: rgb(255, 255, 255);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(parent=New_Order)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridlayoutprincipal = QtWidgets.QGridLayout()
        self.gridlayoutprincipal.setObjectName("gridlayoutprincipal")
        self.gridlayoutprincipal.setVerticalSpacing(40)
        self.gridlayoutprincipal.setHorizontalSpacing(15)
        self.label_NumOrder = QtWidgets.QLabel(parent=self.frame)
        self.label_NumOrder.setMinimumSize(QtCore.QSize(105, 25))
        self.label_NumOrder.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumOrder.setFont(font)
        self.label_NumOrder.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_NumOrder.setObjectName("label_NumOrder")
        self.gridlayoutprincipal.addWidget(self.label_NumOrder, 0, 0, 1, 1)
        self.NumOrder_NewOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.NumOrder_NewOrder.setMinimumSize(QtCore.QSize(160, 25))
        self.NumOrder_NewOrder.setMaximumSize(QtCore.QSize(160, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumOrder_NewOrder.setFont(font)
        self.NumOrder_NewOrder.setObjectName("NumOrder_NewOrder")
        self.gridlayoutprincipal.addWidget(self.NumOrder_NewOrder, 0, 1, 1, 1)
        self.label_ExpectDate = QtWidgets.QLabel(parent=self.frame)
        self.label_ExpectDate.setMinimumSize(QtCore.QSize(105, 25))
        self.label_ExpectDate.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_ExpectDate.setFont(font)
        self.label_ExpectDate.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_ExpectDate.setObjectName("label_ExpectDate")
        self.gridlayoutprincipal.addWidget(self.label_ExpectDate, 0, 2, 1, 1)
        self.ExpectDate_NewOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.ExpectDate_NewOrder.setMinimumSize(QtCore.QSize(160, 25))
        self.ExpectDate_NewOrder.setMaximumSize(QtCore.QSize(160, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ExpectDate_NewOrder.setFont(font)
        self.ExpectDate_NewOrder.setObjectName("ExpectDate_NewOrder")
        self.gridlayoutprincipal.addWidget(self.ExpectDate_NewOrder, 0, 3, 1, 1)
        self.label_NumOffer = QtWidgets.QLabel(parent=self.frame)
        self.label_NumOffer.setMinimumSize(QtCore.QSize(105, 25))
        self.label_NumOffer.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumOffer.setFont(font)
        self.label_NumOffer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_NumOffer.setObjectName("label_NumOffer")
        self.gridlayoutprincipal.addWidget(self.label_NumOffer, 1, 0, 1, 1)
        self.NumOffer_NewOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.NumOffer_NewOrder.setMinimumSize(QtCore.QSize(160, 25))
        self.NumOffer_NewOrder.setMaximumSize(QtCore.QSize(160, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumOffer_NewOrder.setFont(font)
        self.NumOffer_NewOrder.setObjectName("NumOffer_NewOrder")
        self.gridlayoutprincipal.addWidget(self.NumOffer_NewOrder, 1, 1, 1, 1)
        self.label_Notes = QtWidgets.QLabel(parent=self.frame)
        self.label_Notes.setMinimumSize(QtCore.QSize(105, 40))
        self.label_Notes.setMaximumSize(QtCore.QSize(105, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Notes.setFont(font)
        self.label_Notes.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_Notes.setObjectName("label_Notes")
        self.gridlayoutprincipal.addWidget(self.label_Notes, 1, 2, 1, 1)
        self.Notes_NewOrder = QtWidgets.QTextEdit(parent=self.frame)
        self.Notes_NewOrder.setMinimumSize(QtCore.QSize(160, 40))
        self.Notes_NewOrder.setMaximumSize(QtCore.QSize(160, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Notes_NewOrder.setFont(font)
        self.Notes_NewOrder.setObjectName("Notes_NewOrder")
        self.gridlayoutprincipal.addWidget(self.Notes_NewOrder, 1, 3, 1, 1)
        self.label_NumRef = QtWidgets.QLabel(parent=self.frame)
        self.label_NumRef.setMinimumSize(QtCore.QSize(105, 25))
        self.label_NumRef.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumRef.setFont(font)
        self.label_NumRef.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_NumRef.setObjectName("label_NumRef")
        self.gridlayoutprincipal.addWidget(self.label_NumRef, 2, 0, 1, 1)
        self.NumRef_NewOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.NumRef_NewOrder.setMinimumSize(QtCore.QSize(160, 25))
        self.NumRef_NewOrder.setMaximumSize(QtCore.QSize(160, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumRef_NewOrder.setFont(font)
        self.NumRef_NewOrder.setObjectName("NumRef_NewOrder")
        self.gridlayoutprincipal.addWidget(self.NumRef_NewOrder, 2, 1, 1, 1)
        self.label_Amount = QtWidgets.QLabel(parent=self.frame)
        self.label_Amount.setMinimumSize(QtCore.QSize(105, 25))
        self.label_Amount.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Amount.setFont(font)
        self.label_Amount.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_Amount.setObjectName("label_Amount")
        self.gridlayoutprincipal.addWidget(self.label_Amount, 2, 2, 1, 1)
        self.Amount_NewOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.Amount_NewOrder.setMinimumSize(QtCore.QSize(160, 25))
        self.Amount_NewOrder.setMaximumSize(QtCore.QSize(160, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Amount_NewOrder.setFont(font)
        self.Amount_NewOrder.setObjectName("Amount_NewOrder")
        self.gridlayoutprincipal.addWidget(self.Amount_NewOrder, 2, 3, 1, 1)
        self.euromoney = QtWidgets.QRadioButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.euromoney.setFont(font)
        self.euromoney.setMinimumSize(QtCore.QSize(25, 20))
        self.euromoney.setMaximumSize(QtCore.QSize(25, 20))
        self.euromoney.setObjectName("euromoney")
        self.gridlayoutprincipal.addWidget(self.euromoney, 2, 4, 1, 1)
        self.dollarmoney = QtWidgets.QRadioButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dollarmoney.setFont(font)
        self.dollarmoney.setMinimumSize(QtCore.QSize(25, 20))
        self.dollarmoney.setMaximumSize(QtCore.QSize(25, 20))
        self.dollarmoney.setObjectName("dollarmoney")
        self.gridlayoutprincipal.addWidget(self.dollarmoney, 2, 5, 1, 1)
        self.label_num_items = QtWidgets.QLabel(parent=self.frame)
        self.label_num_items.setMinimumSize(QtCore.QSize(105, 25))
        self.label_num_items.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_num_items.setFont(font)
        self.label_num_items.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_num_items.setObjectName("label_num_items")
        self.gridlayoutprincipal.addWidget(self.label_num_items, 3, 1, 1, 1)
        self.NumItems_NewOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.NumItems_NewOrder.setMinimumSize(QtCore.QSize(105, 25))
        self.NumItems_NewOrder.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumItems_NewOrder.setFont(font)
        self.NumItems_NewOrder.setObjectName("NumItems_NewOrder")
        self.gridlayoutprincipal.addWidget(self.NumItems_NewOrder, 3, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridlayoutprincipal)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.hLayout1 = QtWidgets.QHBoxLayout()
        self.hLayout1.setObjectName("hLayout1")
        self.Button_NewOrder = QtWidgets.QPushButton(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button_NewOrder.sizePolicy().hasHeightForWidth())
        self.Button_NewOrder.setSizePolicy(sizePolicy)
        self.Button_NewOrder.setMinimumSize(QtCore.QSize(200, 30))
        self.Button_NewOrder.setMaximumSize(QtCore.QSize(200, 30))
        self.Button_NewOrder.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_NewOrder.setAutoDefault(True)
        self.Button_NewOrder.setObjectName("Button_NewOrder")
        self.hLayout1.addWidget(self.Button_NewOrder)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button_Cancel.sizePolicy().hasHeightForWidth())
        self.Button_Cancel.setSizePolicy(sizePolicy)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(200, 30))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(200, 30))
        self.Button_Cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Cancel.setAutoDefault(True)
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.hLayout1.addWidget(self.Button_Cancel)
        self.verticalLayout.addLayout(self.hLayout1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.label_error_neworder = QtWidgets.QLabel(parent=self.frame)
        self.label_error_neworder.setMinimumSize(QtCore.QSize(0, 25))
        self.label_error_neworder.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_error_neworder.setStyleSheet("color: rgb(255, 0, 0);")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_error_neworder.setFont(font)
        self.label_error_neworder.setWordWrap(True)
        self.label_error_neworder.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_error_neworder.setObjectName("label_error_neworder")
        self.verticalLayout.addWidget(self.label_error_neworder)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        New_Order.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=New_Order)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 22))
        self.menubar.setObjectName("menubar")
        New_Order.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=New_Order)
        self.statusbar.setObjectName("statusbar")
        New_Order.setStatusBar(self.statusbar)
        New_Order.setWindowFlags(QtCore.Qt.WindowType.WindowMinimizeButtonHint)

        self.NumOffer_NewOrder.setText(self.num_offer)

        self.retranslateUi(New_Order)
        self.Button_Cancel.clicked.connect(New_Order.close) # type: ignore
        self.Button_NewOrder.clicked.connect(self.NewOrder)
        QtCore.QMetaObject.connectSlotsByName(New_Order)


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, New_Order):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        New_Order.setWindowTitle(_translate("New_Order", "Nuevo Pedido"))
        self.label_NumOrder.setText(_translate("New_Order", "Nº Pedido:"))
        self.label_NumOffer.setText(_translate("New_Order", "Nº Oferta:"))
        self.label_NumRef.setText(_translate("New_Order", "Nº Referencia:"))
        self.label_ExpectDate.setText(_translate("New_Order", "Fecha Prevista:"))
        self.label_Notes.setText(_translate("New_Order", "Notas:"))
        self.label_Amount.setText(_translate("New_Order", "Importe:"))
        self.label_num_items.setText(_translate("New_Order", "Nº Equipos:"))
        self.Button_NewOrder.setText(_translate("New_Order", "Crear Pedido"))
        self.Button_Cancel.setText(_translate("New_Order", "Cancelar"))
        self.euromoney.setText(_translate("New_Order", "€"))
        self.dollarmoney.setText(_translate("New_Order", "$"))


    def NewOrder(self):
        """
        Creates a new entry after validating form inputs.
        """
        numorder=self.NumOrder_NewOrder.text()
        numoffer=self.NumOffer_NewOrder.text()
        numref=self.NumRef_NewOrder.text()
        expectdate=self.ExpectDate_NewOrder.text()
        notes=self.Notes_NewOrder.toPlainText()
        initial_amount=self.Amount_NewOrder.text()
        num_items=self.NumItems_NewOrder.text()
        state="Adjudicada"
        actual_date=date.today()
        actual_date= actual_date.strftime("%d/%m/%Y")

        if numorder=="" or (numoffer=="" or  (numref=="" or (initial_amount=="" or (num_items=="" or (self.euromoney.isChecked()==False and self.dollarmoney.isChecked()==False))))):
            self.label_error_neworder.setText('Rellene todos los campos y seleccione el tipo de moneda. Solo el campo notas pueden estar en blanco')

        elif not re.match(r'^(P-\d{2}/\d{3}-S\d{2}R?|PA-\d{2}/\d{3}[A-Za-z]*)$', numorder):
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Nuevo Pedido")
            dlg.setText("El número de pedido debe tener el siguiente formato\n" +
                        "- P-XX/YYY-SZZ\n" + 
                        "- P-XX/YYY-SZZR\n" + 
                        "- PA-XX/YYY")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()

        else:
            if self.dollarmoney.isChecked()==True:
                result_conversion = self.dollars_to_euros(float(initial_amount))
                euros_amount = str(result_conversion[0])
                change_type = result_conversion[1]
                amount = euros_amount.replace(".",",")

            elif self.euromoney.isChecked()==True:
                amount = initial_amount.replace(".",",")

            commands_offer = ("""
                        SELECT *
                        FROM offers
                        WHERE "num_offer" = %s
                        """)
            commands_order = ("""
                        SELECT *
                        FROM orders
                        WHERE "num_order" = %s
                        """)
            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands one by one
                cur.execute(commands_offer,(numoffer,))
                results_offer=cur.fetchall()
                match_offer=list(filter(lambda x:numoffer in x, results_offer))
                cur.execute(commands_order,(numorder,))
                results_order=cur.fetchall()
                match_order=list(filter(lambda x:numorder in x, results_order))
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

            if len(match_offer)==0:
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Nuevo Pedido")
                dlg.setText("El número de oferta introducido no existe")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()

            elif len(match_order)>0:
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Nuevo Pedido")
                dlg.setText("El número de pedido introducido ya existe")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()

            else:
                commands_neworder = ("""
                            INSERT INTO orders (
                            "num_order","num_offer","num_ref_order","order_date","expected_date","notes","order_amount","items_number"
                            )
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
                            UPDATE offers
                            SET "state" = %s
                            WHERE "num_offer" = %s;
                            """)
                # commands_select_ppi = ("""
                #             SELECT * FROM verification."ppi_verification" WHERE "num_order" = %s
                #             """)
                # commands_select_exp = ("""
                #             SELECT * FROM verification."exp_verification" WHERE "num_order" = %s
                #             """)
                # commands_insert_ppi = ("""
                #             INSERT INTO verification."ppi_verification" (num_order) 
                #             VALUES(%s)
                #             """)
                # commands_insert_exp = ("""
                #             INSERT INTO verification."exp_verification" (num_order) 
                #             VALUES(%s)
                #             """)
                conn = None
                try:
                # read the connection parameters
                    params = config()
                # connect to the PostgreSQL server
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                # execution of commands
                    if self.dollarmoney.isChecked()==True:
                        notes += ' // IMPORTE DE OFERTA EN DOLARES (' + initial_amount + '). Tipo de cambio: ' + str(round(change_type, 2)) + '$ - 1€ ' + actual_date

                    data = (numorder, numoffer, numref, actual_date, expectdate, notes, amount, num_items, state, numoffer)
                    cur.execute(commands_neworder, data)

                    # if numorder[-1] != 'R':
                    #     cur.execute(commands_select_ppi, (numorder,))
                    #     results_ppi = cur.fetchall()
                    #     if len(results_ppi) == 0:
                    #         cur.execute(commands_insert_ppi, (numorder,))

                    #     cur.execute(commands_select_exp, (numorder,))
                    #     results_exp = cur.fetchall()
                    #     if len(results_exp) == 0:
                    #         cur.execute(commands_insert_exp, (numorder,))
                # close communication with the PostgreSQL database server
                    cur.close()
                # commit the changes
                    conn.commit()

                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Crear Pedido")
                    dlg.setText("Pedido creado con éxito")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    dlg.exec()

                    self.NumOrder_NewOrder.setText('')
                    self.NumOffer_NewOrder.setText('')
                    self.NumRef_NewOrder.setText('')
                    self.ExpectDate_NewOrder.setText('')
                    self.Notes_NewOrder.setText('')
                    self.Amount_NewOrder.setText('')

                except (Exception, psycopg2.DatabaseError) as error:
                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Crear Pedido")
                    dlg.setText("Ha ocurrido el siguiente error:\n"
                                + str(error))
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    dlg.exec()
                finally:
                    if conn is not None:
                        conn.close()

                conn = None
                try:
                # read the connection parameters
                    params = config()
                # connect to the PostgreSQL server
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()

                    commands_usernames = ("""SELECT username FROM users_data.registration
                        WHERE profile IN ('Técnico', 'Compras','Taller')
                        """)
                    commands_notification_neworder = ("""INSERT INTO notifications.notifications_orders (
                                            "username","message","state","date_creation"
                                            )
                                            VALUES (%s,%s,%s,%s)
                                            """)
                    commands_project_client = ("""SELECT client, project FROM offers WHERE num_offer = %s""")

                    cur.execute(commands_usernames)
                    results_usernames=cur.fetchall()
                    results_usernames.append(['m.sahuquillo',])

                    cur.execute(commands_project_client, (self.num_offer,))
                    results_project_client=cur.fetchall()

                    for user_data in results_usernames:
                        if numorder[-1] != 'R':
                            if user_data[0] == 'e.carrillo':
                                data = (user_data[0], "Nuevo pedido: " + numorder + "\nProyecto: " + results_project_client[0][1] + "\nCliente: " + results_project_client[0][0], "Pendiente", actual_date)
                            else:
                                data = (user_data[0], "Nuevo pedido: " + numorder, "Pendiente", actual_date)
                            cur.execute(commands_notification_neworder, data)
                        else:
                            if user_data[0] == 'm.sahuquillo':
                                data = ('m.sahuquillo', "Nuevo pedido: " + numorder, "Pendiente", actual_date)
                                cur.execute(commands_notification_neworder, data)

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


# Function to convert dollars to euros
    def dollars_to_euros(self, dollar_amount):
        """
        Converts a dollar amount to euros using the current exchange rate.

        Args:
            dollar_amount (float): The amount in dollars to be converted.
        
        Returns:
            list: A list containing the converted euro amount and the exchange rate used.
            None: If the exchange rate cannot be obtained.
        """
        change_type = obtain_money_change()

        if change_type is not None:
            euros_amount = round(dollar_amount / change_type, 2)
            return [euros_amount, change_type]
        else:
            return None

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     New_Order = QtWidgets.QMainWindow()
#     ui = Ui_New_Order_Window('O-23/095')
#     ui.setupUi(New_Order)
#     New_Order.show()
#     sys.exit(app.exec())
