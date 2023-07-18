# Form implementation generated from reading ui file 'QueryOrder_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter


class Ui_QueryOrder_Window(object):
    def setupUi(self, QueryOrder_Window):
        QueryOrder_Window.setObjectName("QueryOrder_Window")
        QueryOrder_Window.resize(790, 595)
        QueryOrder_Window.setMinimumSize(QtCore.QSize(790, 595))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        QueryOrder_Window.setWindowIcon(icon)
        QueryOrder_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=QueryOrder_Window)
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
        self.hLayout1 = QtWidgets.QHBoxLayout()
        self.hLayout1.setObjectName("hLayout1")
        self.label_NumOrder = QtWidgets.QLabel(parent=self.frame)
        self.label_NumOrder.setMinimumSize(QtCore.QSize(80, 25))
        self.label_NumOrder.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumOrder.setFont(font)
        self.label_NumOrder.setObjectName("label_NumOrder")
        self.hLayout1.addWidget(self.label_NumOrder)
        self.Numorder_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.Numorder_QueryOrder.setMinimumSize(QtCore.QSize(250, 25))
        self.Numorder_QueryOrder.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Numorder_QueryOrder.setFont(font)
        self.Numorder_QueryOrder.setObjectName("Numorder_QueryOrder")
        self.hLayout1.addWidget(self.Numorder_QueryOrder)
        self.label_Client = QtWidgets.QLabel(parent=self.frame)
        self.label_Client.setMinimumSize(QtCore.QSize(90, 25))
        self.label_Client.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Client.setFont(font)
        self.label_Client.setObjectName("label_Client")
        self.hLayout1.addWidget(self.label_Client)
        self.Client_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.Client_QueryOrder.setMinimumSize(QtCore.QSize(250, 25))
        self.Client_QueryOrder.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Client_QueryOrder.setFont(font)
        self.Client_QueryOrder.setObjectName("Client_QueryOrder")
        self.hLayout1.addWidget(self.Client_QueryOrder)
        self.gridLayout_2.addLayout(self.hLayout1, 1, 0, 1, 1)
        self.hLayout2 = QtWidgets.QHBoxLayout()
        self.hLayout2.setObjectName("hLayout2")
        self.label_NumOffer = QtWidgets.QLabel(parent=self.frame)
        self.label_NumOffer.setMinimumSize(QtCore.QSize(80, 25))
        self.label_NumOffer.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumOffer.setFont(font)
        self.label_NumOffer.setObjectName("label_NumOffer")
        self.hLayout2.addWidget(self.label_NumOffer)
        self.Numoffer_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.Numoffer_QueryOrder.setMinimumSize(QtCore.QSize(250, 25))
        self.Numoffer_QueryOrder.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Numoffer_QueryOrder.setFont(font)
        self.Numoffer_QueryOrder.setObjectName("Numoffer_QueryOrder")
        self.hLayout2.addWidget(self.Numoffer_QueryOrder)
        self.label_FinalClient = QtWidgets.QLabel(parent=self.frame)
        self.label_FinalClient.setMinimumSize(QtCore.QSize(90, 25))
        self.label_FinalClient.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_FinalClient.setFont(font)
        self.label_FinalClient.setObjectName("label_FinalClient")
        self.hLayout2.addWidget(self.label_FinalClient)
        self.Finalclient_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.Finalclient_QueryOrder.setMinimumSize(QtCore.QSize(250, 25))
        self.Finalclient_QueryOrder.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Finalclient_QueryOrder.setFont(font)
        self.Finalclient_QueryOrder.setObjectName("Finalclient_QueryOrder")
        self.hLayout2.addWidget(self.Finalclient_QueryOrder)
        self.gridLayout_2.addLayout(self.hLayout2, 2, 0, 1, 1)
        self.hLayout3 = QtWidgets.QHBoxLayout()
        self.hLayout3.setObjectName("hLayout3")
        self.label_Year = QtWidgets.QLabel(parent=self.frame)
        self.label_Year.setMinimumSize(QtCore.QSize(80, 25))
        self.label_Year.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Year.setFont(font)
        self.label_Year.setObjectName("label_Year")
        self.hLayout3.addWidget(self.label_Year)
        self.Year_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.Year_QueryOrder.setMinimumSize(QtCore.QSize(250, 25))
        self.Year_QueryOrder.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Year_QueryOrder.setFont(font)
        self.Year_QueryOrder.setObjectName("Year_QueryOrder")
        self.hLayout3.addWidget(self.Year_QueryOrder)
        self.label_EqType = QtWidgets.QLabel(parent=self.frame)
        self.label_EqType.setMinimumSize(QtCore.QSize(90, 25))
        self.label_EqType.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_EqType.setFont(font)
        self.label_EqType.setObjectName("label_EqType")
        self.hLayout3.addWidget(self.label_EqType)
        self.EqType_QueryOrder = QtWidgets.QComboBox(parent=self.frame)
        self.EqType_QueryOrder.setMinimumSize(QtCore.QSize(250, 25))
        self.EqType_QueryOrder.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.EqType_QueryOrder.setFont(font)
        self.EqType_QueryOrder.setObjectName("EqType_QueryOrder")
        self.hLayout3.addWidget(self.EqType_QueryOrder)
        self.gridLayout_2.addLayout(self.hLayout3, 3, 0, 1, 1)
        self.hLayout4 = QtWidgets.QHBoxLayout()
        self.hLayout4.setObjectName("hLayout4")
        self.label_RefNum = QtWidgets.QLabel(parent=self.frame)
        self.label_RefNum.setMinimumSize(QtCore.QSize(80, 25))
        self.label_RefNum.setMaximumSize(QtCore.QSize(80, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_RefNum.setFont(font)
        self.label_RefNum.setObjectName("label_RefNum")
        self.hLayout4.addWidget(self.label_RefNum)
        self.Ref_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.Ref_QueryOrder.setMinimumSize(QtCore.QSize(250, 25))
        self.Ref_QueryOrder.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Ref_QueryOrder.setFont(font)
        self.Ref_QueryOrder.setObjectName("Ref_QueryOrder")
        self.hLayout4.addWidget(self.Ref_QueryOrder)
        self.label_Amount = QtWidgets.QLabel(parent=self.frame)
        self.label_Amount.setMinimumSize(QtCore.QSize(90, 25))
        self.label_Amount.setMaximumSize(QtCore.QSize(90, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Amount.setFont(font)
        self.label_Amount.setObjectName("label_Amount")
        self.hLayout4.addWidget(self.label_Amount)
        self.Amount_QueryOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.Amount_QueryOrder.setMinimumSize(QtCore.QSize(250, 25))
        self.Amount_QueryOrder.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Amount_QueryOrder.setFont(font)
        self.Amount_QueryOrder.setObjectName("Amount_QueryOrder")
        self.hLayout4.addWidget(self.Amount_QueryOrder)
        self.gridLayout_2.addLayout(self.hLayout4, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 5, 0, 1, 1)
        self.hLayout5 = QtWidgets.QHBoxLayout()
        self.hLayout5.setObjectName("hLayout5")
        self.Button_Clean = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Clean.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_Clean.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_Clean.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_Clean.setObjectName("Button_Clean")
        self.hLayout5.addWidget(self.Button_Clean)
        self.Button_Query = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Query.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_Query.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_Query.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_Query.setObjectName("Button_Query")
        self.hLayout5.addWidget(self.Button_Query)
        self.gridLayout_2.addLayout(self.hLayout5, 6, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem2, 7, 0, 1, 1)
        self.tableQueryOrder = QtWidgets.QTableWidget(parent=self.frame)
        self.tableQueryOrder.setAlternatingRowColors(False)
        self.tableQueryOrder.setObjectName("tableQueryOrder")
        self.tableQueryOrder.setColumnCount(7)
        self.tableQueryOrder.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableQueryOrder.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableQueryOrder.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableQueryOrder.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableQueryOrder.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableQueryOrder.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableQueryOrder.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableQueryOrder.setHorizontalHeaderItem(6, item)
        self.tableQueryOrder.setSortingEnabled(True)
        self.gridLayout_2.addWidget(self.tableQueryOrder, 8, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        QueryOrder_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=QueryOrder_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 22))
        self.menubar.setObjectName("menubar")
        QueryOrder_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=QueryOrder_Window)
        self.statusbar.setObjectName("statusbar")
        QueryOrder_Window.setStatusBar(self.statusbar)
        self.tableQueryOrder.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.retranslateUi(QueryOrder_Window)
        QtCore.QMetaObject.connectSlotsByName(QueryOrder_Window)
        self.Button_Clean.clicked.connect(self.clean_boxes) # type: ignore
        self.Button_Query.clicked.connect(self.query_order) # type: ignore
        self.Numorder_QueryOrder.returnPressed.connect(self.query_order)

        list_material=['','Caudal','Temperatura','Nivel','Otros']
        self.EqType_QueryOrder.addItems(list_material)


    def retranslateUi(self, QueryOrder_Window):
        _translate = QtCore.QCoreApplication.translate
        QueryOrder_Window.setWindowTitle(_translate("QueryOrder_Window", "Consultar Pedido"))
        self.tableQueryOrder.setSortingEnabled(True)
        item = self.tableQueryOrder.horizontalHeaderItem(0)
        item.setText(_translate("QueryOrder_Window", "Nº Pedido"))
        item = self.tableQueryOrder.horizontalHeaderItem(1)
        item.setText(_translate("QueryOrder_Window", "Nº Oferta"))
        item = self.tableQueryOrder.horizontalHeaderItem(2)
        item.setText(_translate("QueryOrder_Window", "Nº Referencia"))
        item = self.tableQueryOrder.horizontalHeaderItem(3)
        item.setText(_translate("QueryOrder_Window", "Cliente"))
        item = self.tableQueryOrder.horizontalHeaderItem(4)
        item.setText(_translate("QueryOrder_Window", "Cliente Final"))
        item = self.tableQueryOrder.horizontalHeaderItem(5)
        item.setText(_translate("QueryOrder_Window", "Tipo Equipo"))
        item = self.tableQueryOrder.horizontalHeaderItem(6)
        item.setText(_translate("QueryOrder_Window", "Importe (€)"))
        self.label_Year.setText(_translate("QueryOrder_Window", "Año:"))
        self.label_EqType.setText(_translate("QueryOrder_Window", "Tipo Equipo:"))
        self.label_NumOffer.setText(_translate("QueryOrder_Window", "Nº Oferta:"))
        self.label_FinalClient.setText(_translate("QueryOrder_Window", "Cliente Final:"))
        self.label_NumOrder.setText(_translate("QueryOrder_Window", "Nº Pedido:"))
        self.label_Client.setText(_translate("QueryOrder_Window", "Cliente:"))
        self.Button_Clean.setText(_translate("QueryOrder_Window", "Limpiar Filtros"))
        self.Button_Query.setText(_translate("QueryOrder_Window", "Buscar"))
        self.label_RefNum.setText(_translate("QueryOrder_Window", "Referencia:"))
        self.label_Amount.setText(_translate("QueryOrder_Window", "Importe (€):"))


    def clean_boxes(self):
        self.Numorder_QueryOrder.setText("")
        self.Numoffer_QueryOrder.setText("")
        self.Client_QueryOrder.setText("")
        self.Year_QueryOrder.setText("")
        self.Finalclient_QueryOrder.setText("")
        self.Ref_QueryOrder.setText("")
        self.Amount_QueryOrder.setText("")
        self.EqType_QueryOrder.setCurrentText("")


    def query_order(self):
        numorder=self.Numorder_QueryOrder.text()
        numoffer=self.Numoffer_QueryOrder.text()
        client=self.Client_QueryOrder.text()
        year=self.Year_QueryOrder.text()
        finalclient=self.Finalclient_QueryOrder.text()
        ref=self.Ref_QueryOrder.text()
        amount=self.Amount_QueryOrder.text()
        amount=amount.replace(".",",")
        eqtype=self.EqType_QueryOrder.currentText()

        if ((numorder=="" or numorder==" ") and (numoffer=="" or numoffer==" ") and (client=="" or client==" ") 
        and (year=="" or year==" ") and (finalclient=="" or finalclient==" ") and (ref=="" or ref==" ")
        and (amount=="" or amount==" ") and (eqtype=="" or eqtype==" ")):
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Consultar Pedido")
            dlg.setText("Introduce un filtro en alguno de los campos")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()

        else:
            commands_queryorder = ("""
                        SELECT orders."num_order",orders."num_offer",orders."num_ref_order",offers."client",offers."final_client",product_type."variable",orders."order_amount"
                        FROM offers
                        INNER JOIN orders ON (offers."num_offer"=orders."num_offer")
                        INNER JOIN product_type ON (offers."material"=product_type."material")
                        WHERE (UPPER(orders."num_order") LIKE UPPER('%%'||%s||'%%')
                        AND
                        UPPER(orders."num_offer") LIKE UPPER('%%'||%s||'%%')
                        AND
                        UPPER(orders."num_ref_order") LIKE UPPER('%%'||%s||'%%')
                        AND
                        UPPER(offers."client") LIKE UPPER('%%'||%s||'%%')
                        AND
                        UPPER(offers."final_client") LIKE UPPER('%%'||%s||'%%')
                        AND
                        product_type."variable" LIKE '%%'||%s||'%%'
                        AND
                        orders."order_amount"::text LIKE '%%'||%s||'%%'
                        AND
                        orders."order_year"::text LIKE '%%'||%s||'%%'
                        )
                        ORDER BY orders."num_order"
                        """)
            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands
                data=(numorder,numoffer,ref,client,finalclient,eqtype,amount,year,)
                cur.execute(commands_queryorder, data)
                results=cur.fetchall()
                self.tableQueryOrder.setRowCount(len(results))
                tablerow=0

            # fill the Qt Table with the query results
                for row in results:
                    for column in range(7):
                        it=QtWidgets.QTableWidgetItem(str(row[column]))
                        it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                        self.tableQueryOrder.setItem(tablerow, column, it)

                    tablerow+=1

                self.tableQueryOrder.verticalHeader().hide()
                self.tableQueryOrder.setItemDelegate(AlignDelegate(self.tableQueryOrder))

            # close communication with the PostgreSQL database server
                cur.close()
            # commit the changes
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if conn is not None:
                    conn.close()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    QueryOrder_Window = QtWidgets.QMainWindow()
    ui = Ui_QueryOrder_Window()
    ui.setupUi(QueryOrder_Window)
    QueryOrder_Window.show()
    sys.exit(app.exec())
