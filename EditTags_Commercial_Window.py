# Form implementation generated from reading ui file 'EditTags_Commercial_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtSql
import re
import configparser
from Database_Connection import createConnection


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter


class Ui_EditTags_Window(object):
    def setupUi(self, EditTags_Window):
        EditTags_Window.setObjectName("EditTags_Window")
        EditTags_Window.resize(790, 595)
        EditTags_Window.setMinimumSize(QtCore.QSize(790, 595))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        EditTags_Window.setWindowIcon(icon)
        EditTags_Window.setStyleSheet(
".QFrame {\n"
"    border: 2px solid black;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(parent=EditTags_Window)
        self.centralwidget.setStyleSheet("background-color: rgb(255, 255, 255);")
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
        self.Numorder_EditTags = QtWidgets.QLineEdit(parent=self.frame)
        self.Numorder_EditTags.setMinimumSize(QtCore.QSize(250, 25))
        self.Numorder_EditTags.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Numorder_EditTags.setFont(font)
        self.Numorder_EditTags.setObjectName("Numorder_EditTags")
        self.hLayout1.addWidget(self.Numorder_EditTags)
        self.Button_Clean = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Clean.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_Clean.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_Clean.setAutoDefault(True)
        self.Button_Clean.setStyleSheet("QPushButton {\n"
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
        self.Button_Clean.setObjectName("Button_Clean")
        self.hLayout1.addWidget(self.Button_Clean)
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
        self.Numoffer_EditTags = QtWidgets.QLineEdit(parent=self.frame)
        self.Numoffer_EditTags.setMinimumSize(QtCore.QSize(250, 25))
        self.Numoffer_EditTags.setMaximumSize(QtCore.QSize(250, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Numoffer_EditTags.setFont(font)
        self.Numoffer_EditTags.setObjectName("Numoffer_EditTags")
        self.hLayout2.addWidget(self.Numoffer_EditTags)
        self.Button_Query = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Query.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_Query.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_Query.setAutoDefault(True)
        self.Button_Query.setStyleSheet("QPushButton {\n"
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
        self.Button_Query.setObjectName("Button_Query")
        self.hLayout2.addWidget(self.Button_Query)
        self.gridLayout_2.addLayout(self.hLayout2, 2, 0, 1, 1)
        self.tableEditTags=QtWidgets.QTableView(parent=self.frame)
        self.tableEditTags.setObjectName("tableEditTags")
        self.gridLayout_2.addWidget(self.tableEditTags, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        EditTags_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=EditTags_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 22))
        self.menubar.setObjectName("menubar")
        EditTags_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=EditTags_Window)
        self.statusbar.setObjectName("statusbar")
        EditTags_Window.setStatusBar(self.statusbar)

        self.retranslateUi(EditTags_Window)
        QtCore.QMetaObject.connectSlotsByName(EditTags_Window)
        self.Button_Clean.clicked.connect(self.clean_boxes)
        self.Button_Query.clicked.connect(self.edit_tags)


    def retranslateUi(self, EditTags_Window):
        _translate = QtCore.QCoreApplication.translate
        EditTags_Window.setWindowTitle(_translate("EditTags_Window", "Editar Tags"))
        self.tableEditTags.setSortingEnabled(True)
        self.label_NumOffer.setText(_translate("EditTags_Window", "Nº Oferta:"))
        self.Button_Query.setText(_translate("EditTags_Window", "Buscar"))
        self.label_NumOrder.setText(_translate("EditTags_Window", "Nº Pedido:"))
        self.Button_Clean.setText(_translate("EditTags_Window", "Limpiar Filtros"))


    def clean_boxes(self):
        self.Numorder_EditTags.setText("")
        self.Numoffer_EditTags.setText("")


    def edit_tags(self):
        numorder=self.Numorder_EditTags.text()
        numoffer=self.Numoffer_EditTags.text()

        self.model = QtSql.QSqlTableModel()
        self.model.setTable("orders")
        self.model.setFilter("offer_id LIKE '%%'||'%s'||'%%' AND num_order LIKE '%%'||'%s'||'%%'" % (numoffer,numorder))
        self.model.select()
        self.model.EditStrategy.OnFieldChange

        self.proxy = QtCore.QSortFilterProxyModel(self.tableEditTags)
        self.proxy.setSourceModel(self.model)

        self.tableEditTags=QtWidgets.QTableView(parent=self.frame)
        self.tableEditTags.setModel(self.proxy)

        columns_number=self.model.columnCount()
        for i in range(13,columns_number):
            self.tableEditTags.hideColumn(i)

        self.tableEditTags.verticalHeader().hide()
        self.tableEditTags.setItemDelegate(AlignDelegate(self.tableEditTags))
        self.tableEditTags.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableEditTags.horizontalHeader().setStyleSheet("::section{font: 800 10pt}")
        self.tableEditTags.setObjectName("tableEditTags")
        self.gridLayout_2.addWidget(self.tableEditTags, 3, 0, 1, 1)
        self.tableEditTags.horizontalHeader().sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked)


    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):
        self.logicalIndex   = logicalIndex
        self.menuValues     = QtWidgets.QMenu(self.tableEditTags)
        self.signalMapper   = QtCore.QSignalMapper(self.tableEditTags)  

        valuesUnique = []
        for row in range(self.model.rowCount()):
            value = self.model.record(row).value(self.logicalIndex)
            if value not in valuesUnique:
                if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
                valuesUnique.append(str(value))

        actionAll = QtGui.QAction("All", self.tableEditTags)
        actionAll.triggered.connect(self.on_actionAll_triggered)
        self.menuValues.addAction(actionAll)
        self.menuValues.addSeparator()

        for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):              
            action = QtGui.QAction(str(actionName), self.tableEditTags)
            self.signalMapper.setMapping(action, actionNumber)  
            action.triggered.connect(self.signalMapper.map)  
            self.menuValues.addAction(action)

        self.menuValues.setStyleSheet("QMenu { color: black; }"
"QMenu::item:selected { background-color: #33bdef; }"
"QMenu::item:pressed { background-color: rgb(1, 140, 190); }")
        self.signalMapper.mappedInt.connect(self.on_signalMapper_mapped)  

        headerPos = self.tableEditTags.mapToGlobal(self.tableEditTags.horizontalHeader().pos())        

        posY = headerPos.y() + self.tableEditTags.horizontalHeader().height()
        posX = headerPos.x() + self.tableEditTags.horizontalHeader().sectionPosition(self.logicalIndex)

        self.menuValues.exec(QtCore.QPoint(posX, posY))


    def on_actionAll_triggered(self):
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegularExpression("", QtCore.QRegularExpression.PatternOption(0))

        self.proxy.setFilterRegularExpression(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)


    def on_signalMapper_mapped(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex

        if re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', stringAction):
            stringAction=QtCore.QDate.fromString(stringAction,"dd/MM/yyyy")
            stringAction=stringAction.toString("yyyy-MM-dd")

        filterString = QtCore.QRegularExpression(stringAction, QtCore.QRegularExpression.PatternOption(0))

        self.proxy.setFilterRegularExpression(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)



if __name__ == "__main__":
    import sys

    config_obj = configparser.ConfigParser()
    config_obj.read("database.ini")
    dbparam = config_obj["postgresql"]
    # set your parameters for the database connection URI using the keys from the configfile.ini
    user = dbparam["user"]
    password = dbparam["password"]

    # if not createConnection(user,password):
    #     sys.exit()

    app = QtWidgets.QApplication(sys.argv)
    EditTags_Window = QtWidgets.QMainWindow()
    ui = Ui_EditTags_Window()
    ui.setupUi(EditTags_Window)
    EditTags_Window.show()
    sys.exit(app.exec())
