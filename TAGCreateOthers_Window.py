# Form implementation generated from reading ui file 'CreateTAGOthers_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from config import config
import psycopg2
import os

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class Ui_CreateTAGOthers_Window(object):
    def setupUi(self, CreateTAGOthers_Window):
        CreateTAGOthers_Window.setObjectName("CreateTAGOthers_Window")
        CreateTAGOthers_Window.resize(1255, 511)
        CreateTAGOthers_Window.setMinimumSize(QtCore.QSize(1000, 555))
        CreateTAGOthers_Window.setMaximumSize(QtCore.QSize(1000, 555))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        CreateTAGOthers_Window.setWindowIcon(icon)
        CreateTAGOthers_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=CreateTAGOthers_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout")
        self.label_TAG = QtWidgets.QLabel(parent=self.frame)
        self.label_TAG.setMinimumSize(QtCore.QSize(90, 25))
        self.label_TAG.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_TAG.setFont(font)
        self.label_TAG.setObjectName("label_TAG")
        self.gridLayout_2.addWidget(self.label_TAG, 0, 0, 1, 1)
        self.TAG_CreatetagO = QtWidgets.QLineEdit(parent=self.frame)
        self.TAG_CreatetagO.setMinimumSize(QtCore.QSize(150, 25))
        # self.TAG_CreatetagO.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TAG_CreatetagO.setFont(font)
        self.TAG_CreatetagO.setObjectName("TAG_CreatetagO")
        self.gridLayout_2.addWidget(self.TAG_CreatetagO, 0, 1, 1, 3)
        self.label_NumOffer = QtWidgets.QLabel(parent=self.frame)
        self.label_NumOffer.setMinimumSize(QtCore.QSize(90, 25))
        self.label_NumOffer.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumOffer.setFont(font)
        self.label_NumOffer.setObjectName("label_NumOffer")
        self.gridLayout_2.addWidget(self.label_NumOffer, 1, 0, 1, 1)
        self.NumOffer_CreatetagO = QtWidgets.QLineEdit(parent=self.frame)
        self.NumOffer_CreatetagO.setMinimumSize(QtCore.QSize(150, 25))
        self.NumOffer_CreatetagO.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumOffer_CreatetagO.setFont(font)
        self.NumOffer_CreatetagO.setObjectName("NumOffer_CreatetagO")
        self.gridLayout_2.addWidget(self.NumOffer_CreatetagO, 1, 1, 1, 1)
        self.label_NumOrder = QtWidgets.QLabel(parent=self.frame)
        self.label_NumOrder.setMinimumSize(QtCore.QSize(90, 25))
        self.label_NumOrder.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumOrder.setFont(font)
        self.label_NumOrder.setObjectName("label_NumOrder")
        self.gridLayout_2.addWidget(self.label_NumOrder, 2, 0, 1, 1)
        self.NumOrder_CreatetagO = QtWidgets.QLineEdit(parent=self.frame)
        self.NumOrder_CreatetagO.setMinimumSize(QtCore.QSize(150, 25))
        self.NumOrder_CreatetagO.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumOrder_CreatetagO.setFont(font)
        self.NumOrder_CreatetagO.setObjectName("NumOrder_CreatetagO")
        self.gridLayout_2.addWidget(self.NumOrder_CreatetagO, 2, 1, 1, 1)
        self.label_NumPO = QtWidgets.QLabel(parent=self.frame)
        self.label_NumPO.setMinimumSize(QtCore.QSize(90, 25))
        self.label_NumPO.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumPO.setFont(font)
        self.label_NumPO.setObjectName("label_NumPO")
        self.gridLayout_2.addWidget(self.label_NumPO, 3, 0, 1, 1)
        self.NumPO_CreatetagO = QtWidgets.QLineEdit(parent=self.frame)
        self.NumPO_CreatetagO.setMinimumSize(QtCore.QSize(150, 25))
        self.NumPO_CreatetagO.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumPO_CreatetagO.setFont(font)
        self.NumPO_CreatetagO.setObjectName("NumPO_CreatetagO")
        self.gridLayout_2.addWidget(self.NumPO_CreatetagO, 3, 1, 1, 1)
        self.label_Pos = QtWidgets.QLabel(parent=self.frame)
        self.label_Pos.setMinimumSize(QtCore.QSize(90, 25))
        self.label_Pos.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Pos.setFont(font)
        self.label_Pos.setObjectName("label_Pos")
        self.gridLayout_2.addWidget(self.label_Pos, 4, 0, 1, 1)
        self.Pos_CreatetagO = QtWidgets.QLineEdit(parent=self.frame)
        self.Pos_CreatetagO.setMinimumSize(QtCore.QSize(150, 25))
        self.Pos_CreatetagO.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Pos_CreatetagO.setFont(font)
        self.Pos_CreatetagO.setObjectName("Pos_CreatetagO")
        self.gridLayout_2.addWidget(self.Pos_CreatetagO, 4, 1, 1, 1)
        self.label_SubPos = QtWidgets.QLabel(parent=self.frame)
        self.label_SubPos.setMinimumSize(QtCore.QSize(90, 25))
        self.label_SubPos.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_SubPos.setFont(font)
        self.label_SubPos.setObjectName("label_SubPos")
        self.gridLayout_2.addWidget(self.label_SubPos, 5, 0, 1, 1)
        self.Subpos_CreatetagO = QtWidgets.QLineEdit(parent=self.frame)
        self.Subpos_CreatetagO.setMinimumSize(QtCore.QSize(150, 25))
        self.Subpos_CreatetagO.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Subpos_CreatetagO.setFont(font)
        self.Subpos_CreatetagO.setObjectName("Subpos_CreatetagO")
        self.gridLayout_2.addWidget(self.Subpos_CreatetagO, 5, 1, 1, 1)
        self.label_Description = QtWidgets.QLabel(parent=self.frame)
        self.label_Description.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Description.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Description.setFont(font)
        self.label_Description.setObjectName("label_Description")
        self.gridLayout_2.addWidget(self.label_Description, 1, 2, 1, 1)
        self.Description_CreatetagO = QtWidgets.QTextEdit(parent=self.frame)
        self.Description_CreatetagO.setMinimumSize(QtCore.QSize(375, 65))
        self.Description_CreatetagO.setMaximumSize(QtCore.QSize(375, 65))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Description_CreatetagO.setFont(font)
        self.Description_CreatetagO.setObjectName("Description_CreatetagO")
        self.gridLayout_2.addWidget(self.Description_CreatetagO, 1, 3, 1, 1)
        self.label_Code = QtWidgets.QLabel(parent=self.frame)
        self.label_Code.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Code.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Code.setFont(font)
        self.label_Code.setObjectName("label_Code")
        self.gridLayout_2.addWidget(self.label_Code, 2, 2, 1, 1)
        self.Code_CreatetagO = QtWidgets.QLineEdit(parent=self.frame)
        self.Code_CreatetagO.setMinimumSize(QtCore.QSize(375, 25))
        self.Code_CreatetagO.setMaximumSize(QtCore.QSize(375, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Code_CreatetagO.setFont(font)
        self.Code_CreatetagO.setObjectName("Code_CreatetagO")
        self.gridLayout_2.addWidget(self.Code_CreatetagO, 2, 3, 1, 1)
        self.label_Nace = QtWidgets.QLabel(parent=self.frame)
        self.label_Nace.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Nace.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Nace.setFont(font)
        self.label_Nace.setObjectName("label_Nace")
        self.gridLayout_2.addWidget(self.label_Nace, 3, 2, 1, 1)
        self.Nace_CreatetagO = QtWidgets.QComboBox(parent=self.frame)
        self.Nace_CreatetagO.setMinimumSize(QtCore.QSize(375, 25))
        self.Nace_CreatetagO.setMaximumSize(QtCore.QSize(375, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Nace_CreatetagO.setFont(font)
        self.Nace_CreatetagO.setObjectName("Nace_CreatetagO")
        self.gridLayout_2.addWidget(self.Nace_CreatetagO, 3, 3, 1, 1)
        self.label_Amount = QtWidgets.QLabel(parent=self.frame)
        self.label_Amount.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Amount.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Amount.setFont(font)
        self.label_Amount.setObjectName("label_Amount")
        self.gridLayout_2.addWidget(self.label_Amount, 4, 2, 1, 1)
        self.Amount_CreatetagO = QtWidgets.QLineEdit(parent=self.frame)
        self.Amount_CreatetagO.setMinimumSize(QtCore.QSize(375, 25))
        self.Amount_CreatetagO.setMaximumSize(QtCore.QSize(375, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Amount_CreatetagO.setFont(font)
        self.Amount_CreatetagO.setObjectName("Amount_CreatetagO")
        self.gridLayout_2.addWidget(self.Amount_CreatetagO, 4, 3, 1, 1)
        self.label_Notes = QtWidgets.QLabel(parent=self.frame)
        self.label_Notes.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Notes.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Notes.setFont(font)
        self.label_Notes.setObjectName("label_Notes")
        self.gridLayout_2.addWidget(self.label_Notes, 5, 2, 1, 1)
        self.Notes_CreatetagO = QtWidgets.QTextEdit(parent=self.frame)
        self.Notes_CreatetagO.setMinimumSize(QtCore.QSize(375, 65))
        self.Notes_CreatetagO.setMaximumSize(QtCore.QSize(375, 65))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Notes_CreatetagO.setFont(font)
        self.Notes_CreatetagO.setObjectName("Notes_CreatetagO")
        self.gridLayout_2.addWidget(self.Notes_CreatetagO, 5, 3, 1, 1)
        self.Button_Create = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Create.setMinimumSize(QtCore.QSize(200, 35))
        self.Button_Create.setMaximumSize(QtCore.QSize(16777215, 35))
        self.Button_Create.setObjectName("Button_Create")
        self.gridLayout_2.addWidget(self.Button_Create, 6, 0, 1, 2)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(200, 35))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(16777215, 35))
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.gridLayout_2.addWidget(self.Button_Cancel, 6, 2, 1, 2)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        CreateTAGOthers_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=CreateTAGOthers_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1255, 22))
        self.menubar.setObjectName("menubar")
        CreateTAGOthers_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=CreateTAGOthers_Window)
        self.statusbar.setObjectName("statusbar")
        CreateTAGOthers_Window.setStatusBar(self.statusbar)

        commands_comboboxes = [
            "SELECT nace FROM validation_data.others_nace"
            ]

        all_results = []

        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            for query in commands_comboboxes:
                cur.execute(query)
                results=cur.fetchall()
                all_results.append(results)
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

        self.Nace_CreatetagO.addItems(sorted([x[0] for x in all_results[0]]))

        self.retranslateUi(CreateTAGOthers_Window)
        self.Button_Cancel.clicked.connect(CreateTAGOthers_Window.close) # type: ignore
        self.Button_Create.clicked.connect(self.createtagO) # type: ignore
        self.NumOrder_CreatetagO.returnPressed.connect(self.queryoffernumber)
        QtCore.QMetaObject.connectSlotsByName(CreateTAGOthers_Window)


    def retranslateUi(self, CreateTAGOthers_Window):
        _translate = QtCore.QCoreApplication.translate
        CreateTAGOthers_Window.setWindowTitle(_translate("CreateTAGOthers_Window", "Crear TAG Otros"))
        self.label_TAG.setText(_translate("CreateTAGOthers_Window", "*TAG:"))
        self.label_NumOffer.setText(_translate("CreateTAGOthers_Window", "*Nº Oferta:"))
        self.label_NumOrder.setText(_translate("CreateTAGOthers_Window", "Nº Pedido:"))
        self.label_NumPO.setText(_translate("CreateTAGOthers_Window", "Nº PO:"))
        self.label_Pos.setText(_translate("CreateTAGOthers_Window", "Posición:"))
        self.label_SubPos.setText(_translate("CreateTAGOthers_Window", "Sub-Pos:"))
        self.label_Amount.setText(_translate("CreateTAGOthers_Window", "Importe (€):"))
        self.label_Nace.setText(_translate("CreateTAGOthers_Window", "NACE:"))
        self.label_Notes.setText(_translate("CreateTAGOthers_Window", "Notas:"))
        self.label_Description.setText(_translate("CreateTAGOthers_Window", "*Descripción:"))
        self.label_Code.setText(_translate("CreateTAGOthers_Window", "Código Eq.:"))
        self.Button_Create.setText(_translate("CreateTAGOthers_Window", "Crear"))
        self.Button_Cancel.setText(_translate("CreateTAGOthers_Window","Cancelar"))


    def createtagO(self):
        tag=self.TAG_CreatetagO.text()
        tag_state='QUOTED'
        numoffer=self.NumOffer_CreatetagO.text()
        numorder=self.NumOrder_CreatetagO.text() if self.NumOrder_CreatetagO.text() != '' else None
        num_po=self.NumPO_CreatetagO.text()
        pos=self.Pos_CreatetagO.text()
        subpos=self.Subpos_CreatetagO.text()
        description=self.Description_CreatetagO.toPlainText()
        code_equipment=self.Code_CreatetagO.text()
        nace=self.Nace_CreatetagO.currentText()
        notes=self.Notes_CreatetagO.toPlainText()
        amount=self.Amount_CreatetagO.text()
        amount=amount.replace(".",",")

        if ((tag=="" or tag==" ") or (description=="" or description==" ") or (numoffer=="" or numoffer==" ")):
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Crear TAG Otros")
            dlg.setText("Rellene los campos con * mínimo")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()

        else:
            commands_inserttagothers = ("""
                            INSERT INTO tags_data.tags_others(
                            "tag","tag_state","num_offer","num_order","num_po",
                            "position","subposition","description","code_equipment","nace",
                            "offer_notes","amount"
                            )
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """)
            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands one by one
                data = (tag,tag_state,numoffer,numorder,num_po,
                        pos,subpos,description,code_equipment,nace,
                        notes,amount)
                cur.execute(commands_inserttagothers, data)
            # close communication with the PostgreSQL database server
                cur.close()
            # commit the changes
                conn.commit()

                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Crear Tag")
                dlg.setText("Tag creado con éxito")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                dlg.exec()

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


    def queryoffernumber(self):
        numorder=self.NumOrder_CreatetagO.text()
    #SQL Query for loading existing data in database
        commands_loadofferorder = ("""
                    SELECT "num_order","num_offer","num_ref_order"
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
            cur.execute(commands_loadofferorder,(numorder,))
            results=cur.fetchall()
            match=list(filter(lambda x:numorder in x, results))
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

        if len(match)==0:
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Crear Tag")
            dlg.setText("El número de oferta introducido no existe")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()

        else:
            self.NumOffer_CreatetagO.setText(str(results[0][1]))
            self.NumPO_CreatetagO.setText(str(results[0][2]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    CreateTAGOthers_Window = QtWidgets.QMainWindow()
    ui = Ui_CreateTAGOthers_Window()
    ui.setupUi(CreateTAGOthers_Window)
    CreateTAGOthers_Window.show()
    sys.exit(app.exec())