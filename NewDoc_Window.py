# Form implementation generated from reading ui file 'NewDoc_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config


class Ui_New_Doc_Window(object):
    def setupUi(self, New_Doc_Window):
        New_Doc_Window.setObjectName("New_Doc_Window")
        New_Doc_Window.resize(670, 425)
        New_Doc_Window.setMinimumSize(QtCore.QSize(670, 425))
        New_Doc_Window.setMaximumSize(QtCore.QSize(670, 425))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        New_Doc_Window.setWindowIcon(icon)
        New_Doc_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=New_Doc_Window)
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
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout1.addItem(spacerItem1)
        self.label_NumDocEipsa = QtWidgets.QLabel(parent=self.frame)
        self.label_NumDocEipsa.setMinimumSize(QtCore.QSize(105, 25))
        self.label_NumDocEipsa.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumDocEipsa.setFont(font)
        self.label_NumDocEipsa.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_NumDocEipsa.setObjectName("label_NumDocEipsa")
        self.vLayout1.addWidget(self.label_NumDocEipsa)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout1.addItem(spacerItem2)
        self.label_TitleDoc = QtWidgets.QLabel(parent=self.frame)
        self.label_TitleDoc.setMinimumSize(QtCore.QSize(105, 25))
        self.label_TitleDoc.setMaximumSize(QtCore.QSize(105, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_TitleDoc.setFont(font)
        self.label_TitleDoc.setObjectName("label_TitleDoc")
        self.vLayout1.addWidget(self.label_TitleDoc)
        self.hLayout.addLayout(self.vLayout1)
        self.vLayout2 = QtWidgets.QVBoxLayout()
        self.vLayout2.setObjectName("vLayout2")
        self.NumOrder_NewDoc = QtWidgets.QLineEdit(parent=self.frame)
        self.NumOrder_NewDoc.setMinimumSize(QtCore.QSize(175, 25))
        self.NumOrder_NewDoc.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumOrder_NewDoc.setFont(font)
        self.NumOrder_NewDoc.setObjectName("NumOrder_NewDoc")
        self.vLayout2.addWidget(self.NumOrder_NewDoc)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout2.addItem(spacerItem3)
        self.NumDocEipsa_NewDoc = QtWidgets.QLineEdit(parent=self.frame)
        self.NumDocEipsa_NewDoc.setMinimumSize(QtCore.QSize(175, 25))
        self.NumDocEipsa_NewDoc.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumDocEipsa_NewDoc.setFont(font)
        self.NumDocEipsa_NewDoc.setObjectName("NumDocEipsa_NewDoc")
        self.vLayout2.addWidget(self.NumDocEipsa_NewDoc)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout2.addItem(spacerItem4)
        self.TitleDoc_NewDoc = QtWidgets.QLineEdit(parent=self.frame)
        self.TitleDoc_NewDoc.setMinimumSize(QtCore.QSize(175, 25))
        self.TitleDoc_NewDoc.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TitleDoc_NewDoc.setFont(font)
        self.TitleDoc_NewDoc.setObjectName("TitleDoc_NewDoc")
        self.vLayout2.addWidget(self.TitleDoc_NewDoc)
        self.hLayout.addLayout(self.vLayout2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hLayout.addItem(spacerItem5)
        self.vLayout3 = QtWidgets.QVBoxLayout()
        self.vLayout3.setObjectName("vLayout3")
        self.label_DocType = QtWidgets.QLabel(parent=self.frame)
        self.label_DocType.setMinimumSize(QtCore.QSize(130, 25))
        self.label_DocType.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_DocType.setFont(font)
        self.label_DocType.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_DocType.setObjectName("label_DocType")
        self.vLayout3.addWidget(self.label_DocType)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout3.addItem(spacerItem6)
        self.label_NumDocClient = QtWidgets.QLabel(parent=self.frame)
        self.label_NumDocClient.setMinimumSize(QtCore.QSize(130, 25))
        self.label_NumDocClient.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumDocClient.setFont(font)
        self.label_NumDocClient.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_NumDocClient.setObjectName("label_NumDocClient")
        self.vLayout3.addWidget(self.label_NumDocClient)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vLayout3.addItem(spacerItem7)
        self.label_Critical = QtWidgets.QLabel(parent=self.frame)
        self.label_Critical.setMinimumSize(QtCore.QSize(130, 25))
        self.label_Critical.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Critical.setFont(font)
        self.label_Critical.setObjectName("label_Critical")
        self.vLayout3.addWidget(self.label_Critical)
        self.hLayout.addLayout(self.vLayout3)
        self.vlLayout4 = QtWidgets.QVBoxLayout()
        self.vlLayout4.setObjectName("vlLayout4")
        self.DocType_NewDoc = QtWidgets.QComboBox(parent=self.frame)
        self.DocType_NewDoc.setMinimumSize(QtCore.QSize(175, 25))
        self.DocType_NewDoc.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DocType_NewDoc.setFont(font)
        self.DocType_NewDoc.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.DocType_NewDoc.setObjectName("DocType_NewDoc")
        self.vlLayout4.addWidget(self.DocType_NewDoc)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vlLayout4.addItem(spacerItem8)
        self.NumDocClient_NewDoc = QtWidgets.QLineEdit(parent=self.frame)
        self.NumDocClient_NewDoc.setMinimumSize(QtCore.QSize(175, 25))
        self.NumDocClient_NewDoc.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumDocClient_NewDoc.setFont(font)
        self.NumDocClient_NewDoc.setObjectName("NumDocClient_NewDoc")
        self.vlLayout4.addWidget(self.NumDocClient_NewDoc)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vlLayout4.addItem(spacerItem9)
        self.Critical_NewDoc = QtWidgets.QComboBox(parent=self.frame)
        self.Critical_NewDoc.setMinimumSize(QtCore.QSize(175, 25))
        self.Critical_NewDoc.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Critical_NewDoc.setFont(font)
        self.Critical_NewDoc.setObjectName("Critical_NewDoc")
        self.vlLayout4.addWidget(self.Critical_NewDoc)
        self.hLayout.addLayout(self.vlLayout4)
        self.verticalLayout.addLayout(self.hLayout)
        spacerItem10 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem10)
        self.hLayout2 = QtWidgets.QHBoxLayout()
        self.hLayout2.setObjectName("hLayout2")
        self.Button_NewDoc = QtWidgets.QPushButton(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button_NewDoc.sizePolicy().hasHeightForWidth())
        self.Button_NewDoc.setSizePolicy(sizePolicy)
        self.Button_NewDoc.setMinimumSize(QtCore.QSize(200, 30))
        self.Button_NewDoc.setMaximumSize(QtCore.QSize(200, 30))
        self.Button_NewDoc.setObjectName("Button_NewDoc")
        self.hLayout2.addWidget(self.Button_NewDoc)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button_Cancel.sizePolicy().hasHeightForWidth())
        self.Button_Cancel.setSizePolicy(sizePolicy)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(200, 30))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(200, 30))
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.hLayout2.addWidget(self.Button_Cancel)
        self.verticalLayout.addLayout(self.hLayout2)
        spacerItem11 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem11)
        self.label_error = QtWidgets.QLabel(parent=self.frame)
        self.label_error.setMaximumSize(QtCore.QSize(630, 35))
        self.label_error.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_error.setText("")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_error.setFont(font)
        self.label_error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_error.setObjectName("label_error")
        self.verticalLayout.addWidget(self.label_error)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        New_Doc_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=New_Doc_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 22))
        self.menubar.setObjectName("menubar")
        New_Doc_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=New_Doc_Window)
        self.statusbar.setObjectName("statusbar")
        New_Doc_Window.setStatusBar(self.statusbar)

        self.retranslateUi(New_Doc_Window)
        self.Button_Cancel.clicked.connect(New_Doc_Window.close) # type: ignore
        self.Button_NewDoc.clicked.connect(lambda: self.NewDoc(New_Doc_Window))
        QtCore.QMetaObject.connectSlotsByName(New_Doc_Window)

        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands one by one
            cur.execute("""SELECT * FROM document_type""")
            results_doctype=cur.fetchall()
        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        list_typedoc=[x[1] for x in results_doctype]
        self.DocType_NewDoc.addItems(sorted(list_typedoc))
        list_critical=['No','Sí']
        self.Critical_NewDoc.addItems(list_critical)


    def retranslateUi(self, New_Doc_Window):
        _translate = QtCore.QCoreApplication.translate
        New_Doc_Window.setWindowTitle(_translate("New_Doc_Window", "Nuevo Documento"))
        self.label_NumOrder.setText(_translate("New_Doc_Window", "Nº Pedido:"))
        self.label_NumDocEipsa.setText(_translate("New_Doc_Window", "Nº Doc. EIPSA:"))
        self.label_TitleDoc.setText(_translate("New_Doc_Window", "Título Doc.:"))
        self.label_DocType.setText(_translate("New_Doc_Window", "Tipo Documento:"))
        self.label_NumDocClient.setText(_translate("New_Doc_Window", "Nº Doc. Cliente:"))
        self.label_Critical.setText(_translate("New_Doc_Window", "Crítico:"))
        self.Button_NewDoc.setText(_translate("New_Doc_Window", "Crear Documento"))
        self.Button_Cancel.setText(_translate("New_Doc_Window", "Cancelar"))


    def NewDoc(self,New_Doc_Window):
        neworder=self.NumOrder_NewDoc.text()
        numdoceipsa=self.NumDocEipsa_NewDoc.text()
        doctype=self.DocType_NewDoc.currentText()
        numdocclient=self.NumDocClient_NewDoc.text()
        titledoc=self.TitleDoc_NewDoc.text()
        critical=self.Critical_NewDoc.currentText()

        if neworder=="" or (numdoceipsa=="" or  (numdocclient=="" or titledoc=="")):
            self.label_error.setText('Rellene todos los campos')

        else:
        #SQL Query for checking if document number exists in database
            commands_checkdocument = ("""
                        SELECT * 
                        FROM documentation
                        WHERE "num_doc_eipsa" = %s
                        """)
            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands one by one
                cur.execute(commands_checkdocument,(numdoceipsa,))
                results=cur.fetchall()
                match=list(filter(lambda x:numdoceipsa in x, results))
            # close communication with the PostgreSQL database server
                cur.close()
            # commit the changes
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()

            if len(match)>0:
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("Crear Documento")
                dlg.setText("El número de documento EIPSA introducido ya está registrado")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()

                del dlg,new_icon

            else:
                commands_newdoc = ("""
                            INSERT INTO documentation (
                            "num_order","num_doc_eipsa","num_doc_client","doc_type_id","doc_title","critical"
                            )
                            VALUES (%s,%s,%s,%s,%s,%s)
                            """)
                conn = None
                try:
                # read the connection parameters
                    params = config()
                # connect to the PostgreSQL server
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                # execution of commands
                    query_doctype = "SELECT id FROM document_type WHERE doc_type = %s"
                    cur.execute(query_doctype, (doctype,))
                # get results from query
                    resultado = cur.fetchone()
                # get id from table
                    id_doctype = resultado[0]
                # execution of principal command
                    data=(neworder, numdoceipsa, numdocclient, id_doctype, titledoc,critical,)
                    cur.execute(commands_newdoc, data)
                # close communication with the PostgreSQL database server
                    cur.close()
                # commit the changes
                    conn.commit()

                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Crear Documento")
                    dlg.setText("Documento creado con éxito")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    dlg.exec()

                    self.NumOrder_NewDoc.setText('')
                    self.NumDocEipsa_NewDoc.setText('')
                    self.NumDocClient_NewDoc.setText('')
                    self.TitleDoc_NewDoc.setText('')

                    del dlg,new_icon

                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if conn is not None:
                        conn.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    New_Doc_Window = QtWidgets.QMainWindow()
    ui = Ui_New_Doc_Window()
    ui.setupUi(New_Doc_Window)
    New_Doc_Window.show()
    sys.exit(app.exec())
