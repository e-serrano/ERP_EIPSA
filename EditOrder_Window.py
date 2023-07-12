# Form implementation generated from reading ui file 'EditOrder_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config


class Ui_Edit_Order_Window(object):
    def setupUi(self, Edit_Order_Window):
        Edit_Order_Window.setObjectName("Edit_Order_Window")
        Edit_Order_Window.resize(680, 425)
        Edit_Order_Window.setMinimumSize(QtCore.QSize(680, 425))
        Edit_Order_Window.setMaximumSize(QtCore.QSize(680, 425))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Edit_Order_Window.setWindowIcon(icon)
        Edit_Order_Window.setStyleSheet("QWidget {\n"
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
"QPushButton:focus:pressed {\n"
"    background-color: rgb(1, 140, 190);\n"
"    border-color: rgb(255, 255, 255);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(parent=Edit_Order_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setObjectName("hLayout")
        self.vLayout1 = QtWidgets.QVBoxLayout()
        self.vLayout1.setContentsMargins(0, -1, 0, -1)
        self.vLayout1.setObjectName("vLayout1")
        self.label_NumOrder = QtWidgets.QLabel(parent=self.frame)
        self.label_NumOrder.setMinimumSize(QtCore.QSize(105, 25))
        self.label_NumOrder.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumOrder.setFont(font)
        self.label_NumOrder.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_NumOrder.setObjectName("label_NumOrder")
        self.vLayout1.addWidget(self.label_NumOrder)
        spacerItem1 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout1.addItem(spacerItem1)
        self.label_NumOffer = QtWidgets.QLabel(parent=self.frame)
        self.label_NumOffer.setMinimumSize(QtCore.QSize(105, 25))
        self.label_NumOffer.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumOffer.setFont(font)
        self.label_NumOffer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_NumOffer.setObjectName("label_NumOffer")
        self.vLayout1.addWidget(self.label_NumOffer)
        spacerItem2 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout1.addItem(spacerItem2)
        self.label_NumRef = QtWidgets.QLabel(parent=self.frame)
        self.label_NumRef.setMinimumSize(QtCore.QSize(105, 25))
        self.label_NumRef.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumRef.setFont(font)
        self.label_NumRef.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_NumRef.setObjectName("label_NumRef")
        self.vLayout1.addWidget(self.label_NumRef)
        self.hLayout.addLayout(self.vLayout1)
        self.vLayout2 = QtWidgets.QVBoxLayout()
        self.vLayout2.setObjectName("vLayout2")
        self.NumOrder_EditOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.NumOrder_EditOrder.setMinimumSize(QtCore.QSize(175, 25))
        self.NumOrder_EditOrder.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumOrder_EditOrder.setFont(font)
        self.NumOrder_EditOrder.setObjectName("NumOrder_EditOrder")
        self.vLayout2.addWidget(self.NumOrder_EditOrder)
        spacerItem3 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout2.addItem(spacerItem3)
        self.NumOffer_EditOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.NumOffer_EditOrder.setMinimumSize(QtCore.QSize(175, 25))
        self.NumOffer_EditOrder.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumOffer_EditOrder.setFont(font)
        self.NumOffer_EditOrder.setObjectName("NumOffer_EditOrder")
        self.vLayout2.addWidget(self.NumOffer_EditOrder)
        spacerItem4 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout2.addItem(spacerItem4)
        self.NumRef_EditOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.NumRef_EditOrder.setMinimumSize(QtCore.QSize(175, 25))
        self.NumRef_EditOrder.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumRef_EditOrder.setFont(font)
        self.NumRef_EditOrder.setObjectName("NumRef_EditOrder")
        self.vLayout2.addWidget(self.NumRef_EditOrder)
        self.hLayout.addLayout(self.vLayout2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hLayout.addItem(spacerItem5)
        self.vLayout3 = QtWidgets.QVBoxLayout()
        self.vLayout3.setObjectName("vLayout3")
        self.label_ContracDate = QtWidgets.QLabel(parent=self.frame)
        self.label_ContracDate.setMinimumSize(QtCore.QSize(130, 25))
        self.label_ContracDate.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_ContracDate.setFont(font)
        self.label_ContracDate.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_ContracDate.setObjectName("label_ContracDate")
        self.vLayout3.addWidget(self.label_ContracDate)
        spacerItem6 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout3.addItem(spacerItem6)
        self.label_Notes = QtWidgets.QLabel(parent=self.frame)
        self.label_Notes.setMinimumSize(QtCore.QSize(130, 40))
        self.label_Notes.setMaximumSize(QtCore.QSize(130, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Notes.setFont(font)
        self.label_Notes.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_Notes.setObjectName("label_Notes")
        self.vLayout3.addWidget(self.label_Notes)
        spacerItem7 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout3.addItem(spacerItem7)
        self.label_Amount = QtWidgets.QLabel(parent=self.frame)
        self.label_Amount.setMinimumSize(QtCore.QSize(130, 25))
        self.label_Amount.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Amount.setFont(font)
        self.label_Amount.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_Amount.setObjectName("label_Amount")
        self.vLayout3.addWidget(self.label_Amount)
        self.hLayout.addLayout(self.vLayout3)
        self.vlLayout4 = QtWidgets.QVBoxLayout()
        self.vlLayout4.setObjectName("vlLayout4")
        self.ContracDate_EditOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.ContracDate_EditOrder.setMinimumSize(QtCore.QSize(175, 25))
        self.ContracDate_EditOrder.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ContracDate_EditOrder.setFont(font)
        self.ContracDate_EditOrder.setObjectName("ContracDate_EditOrder")
        self.vlLayout4.addWidget(self.ContracDate_EditOrder)
        spacerItem8 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vlLayout4.addItem(spacerItem8)
        self.Notes_EditOrder = QtWidgets.QTextEdit(parent=self.frame)
        self.Notes_EditOrder.setMinimumSize(QtCore.QSize(175, 40))
        self.Notes_EditOrder.setMaximumSize(QtCore.QSize(175, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Notes_EditOrder.setFont(font)
        self.Notes_EditOrder.setObjectName("Notes_EditOrder")
        self.vlLayout4.addWidget(self.Notes_EditOrder)
        spacerItem9 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vlLayout4.addItem(spacerItem9)
        self.Amount_EditOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.Amount_EditOrder.setMinimumSize(QtCore.QSize(175, 25))
        self.Amount_EditOrder.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Amount_EditOrder.setFont(font)
        self.Amount_EditOrder.setObjectName("Amount_EditOrder")
        self.vlLayout4.addWidget(self.Amount_EditOrder)
        self.hLayout.addLayout(self.vlLayout4)
        self.verticalLayout.addLayout(self.hLayout)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem10)
        self.hLayout1 = QtWidgets.QHBoxLayout()
        self.hLayout1.setObjectName("hLayout1")
        self.Button_EditOrder = QtWidgets.QPushButton(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button_EditOrder.sizePolicy().hasHeightForWidth())
        self.Button_EditOrder.setSizePolicy(sizePolicy)
        self.Button_EditOrder.setMinimumSize(QtCore.QSize(200, 30))
        self.Button_EditOrder.setMaximumSize(QtCore.QSize(200, 30))
        self.Button_EditOrder.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_EditOrder.setStyleSheet("QPushButton:focus{\n"
"    background-color: #019ad2;\n"
"    border-color: rgb(0, 0, 0);\n"
"}"
)
        self.Button_EditOrder.setAutoDefault(True)
        self.Button_EditOrder.setObjectName("Button_EditOrder")
        self.hLayout1.addWidget(self.Button_EditOrder)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button_Cancel.sizePolicy().hasHeightForWidth())
        self.Button_Cancel.setSizePolicy(sizePolicy)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(200, 30))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(200, 30))
        self.Button_Cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Cancel.setStyleSheet("QPushButton:focus{\n"
"    background-color: #019ad2;\n"
"    border-color: rgb(0, 0, 0);\n"
"}"
)
        self.Button_Cancel.setAutoDefault(True)
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.hLayout1.addWidget(self.Button_Cancel)
        self.verticalLayout.addLayout(self.hLayout1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        Edit_Order_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Edit_Order_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 22))
        self.menubar.setObjectName("menubar")
        Edit_Order_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Edit_Order_Window)
        self.statusbar.setObjectName("statusbar")
        Edit_Order_Window.setStatusBar(self.statusbar)

        self.retranslateUi(Edit_Order_Window)
        self.Button_Cancel.clicked.connect(Edit_Order_Window.close) # type: ignore
        self.Button_EditOrder.clicked.connect(self.editorder) # type: ignore
        self.NumOrder_EditOrder.returnPressed.connect(self.queryorderdata)
        QtCore.QMetaObject.connectSlotsByName(Edit_Order_Window)


    def retranslateUi(self, Edit_Order_Window):
        _translate = QtCore.QCoreApplication.translate
        Edit_Order_Window.setWindowTitle(_translate("Edit_Order_Window", "Editar Pedido"))
        self.label_NumOrder.setText(_translate("Edit_Order_Window", "Nº Pedido:"))
        self.label_NumOffer.setText(_translate("Edit_Order_Window", "Nº Oferta:"))
        self.label_NumRef.setText(_translate("Edit_Order_Window", "Nº Referencia:"))
        self.label_ContracDate.setText(_translate("Edit_Order_Window", "Fecha Contractual:"))
        self.label_Notes.setText(_translate("Edit_Order_Window", "Notas:"))
        self.label_Amount.setText(_translate("Edit_Order_Window", "Importe (€):"))
        self.Button_EditOrder.setText(_translate("Edit_Order_Window", "Editar Pedido"))
        self.Button_Cancel.setText(_translate("Edit_Order_Window", "Cancelar"))


    def editorder(self):
        numorder=self.NumOrder_EditOrder.text()
        numoffer=self.NumOffer_EditOrder.text()
        numref=self.NumRef_EditOrder.text()
        contracdate=self.ContracDate_EditOrder.text()
        notes=self.Notes_EditOrder.toPlainText()
        amount=self.Amount_EditOrder.text()

        #SQL Query for checking if order number exists in database
        commands_checkorder = ("""
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
            cur.execute(commands_checkorder,(numorder,))
            results=cur.fetchall()
            match=list(filter(lambda x:numorder in x, results))
        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        if numorder=="" or (numorder==" " or len(match)==0):
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Editar Pedido")
            dlg.setText("Introduce un número de pedido válido")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()

        else:
            #SQL Query for updating values in database
            commands_editorder = ("""
                        UPDATE orders
                        SET "num_offer" = %s, "num_ref_order" = %s, "contract_date" = %s, "notes" = %s, "order_amount" = %s
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
                data=(numoffer,numref,contracdate,notes,amount,numorder,)
                cur.execute(commands_editorder,data)
            # close communication with the PostgreSQL database server
                cur.close()
            # commit the changes
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Editar Pedido")
            dlg.setText("Pedido editado con exito")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            dlg.exec()

            self.NumOrder_EditOrder.setText('')
            self.NumOffer_EditOrder.setText('')
            self.NumRef_EditOrder.setText('')
            self.ContracDate_EditOrder.setText('')
            self.Notes_EditOrder.setText('')
            self.Amount_EditOrder.setText('')

            del dlg, new_icon


    def queryorderdata(self):
        numorder=self.NumOrder_EditOrder.text()
    #SQL Query for loading existing data in database
        commands_loaddataorder = ("""
                    SELECT "num_order","num_offer","num_ref_order",TO_CHAR("contract_date", 'DD-MM-YYYY'),"notes","order_amount"
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
            cur.execute(commands_loaddataorder,(numorder,))
            results=cur.fetchall()
            match=list(filter(lambda x:numorder in x, results))
        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        if len(match)==0:
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Editar Pedido")
            dlg.setText("El número de pedido introducido no existe")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()

        else:
            self.NumOffer_EditOrder.setText(str(results[0][1]))
            self.NumRef_EditOrder.setText(str(results[0][2]))
            self.ContracDate_EditOrder.setText(str(results[0][3]))
            self.Notes_EditOrder.setText(str(results[0][4]))
            self.Amount_EditOrder.setText(str(results[0][5]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Edit_Order_Window = QtWidgets.QMainWindow()
    ui = Ui_Edit_Order_Window()
    ui.setupUi(Edit_Order_Window)
    Edit_Order_Window.show()
    sys.exit(app.exec())
