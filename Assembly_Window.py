from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtSql
from PyQt6.QtCore import Qt
from Database_Connection import createConnection
import configparser
from datetime import *
import os

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter

class ColorDelegate(QtWidgets.QItemDelegate):
    def paint(self, painter, option, index: QtCore.QModelIndex):
        value = index.model().data(index, role=Qt.ItemDataRole.DisplayRole)
        if index.column() == 15 and value <= 50 and value >= 1:
            background_color = QtGui.QColor(255, 255, 0) #Yellow
        elif index.column() == 15 and value < 100  and value > 50:
            background_color = QtGui.QColor(0, 255, 0) #Green
        elif index.column() == 15 and value == 100:
            background_color = QtGui.QColor(0, 102, 204) #Blue
        else:
            background_color = QtGui.QColor(255, 255, 255) #White

        painter.fillRect(option.rect, background_color)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter
        super().paint(painter, option, index)


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
        if index.column() in [0,1]:
            flags &= ~Qt.ItemFlag.ItemIsEditable
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        else:
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def getColumnHeaders(self, visible_columns):
        column_headers = [self.headerData(col, Qt.Orientation.Horizontal) for col in visible_columns]
        return column_headers


class Ui_Assembly_Window(QtWidgets.QMainWindow):
    def __init__(self,db):
        super().__init__()
        self.model = EditableTableModel()
        self.db = db
        self.setupUi(self)

    def closeEvent(self, event):
    # Closing database connection
        if self.model:
            self.model.clear()
        self.closeConnection()

    def closeConnection(self):
    # Closing database connection
        self.tableAssembly.setModel(None)
        del self.model
        if self.db:
            self.db.close()
            del self.db
            if QtSql.QSqlDatabase.contains("qt_sql_default_connection"):
                QtSql.QSqlDatabase.removeDatabase("qt_sql_default_connection")


    def setupUi(self, Assembly_Window):
        self.id_list = []
        data_list = []
        Assembly_Window.setObjectName("Assembly_Window")
        Assembly_Window.resize(400, 561)
        Assembly_Window.setMinimumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Assembly_Window.setWindowIcon(icon)
        Assembly_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=Assembly_Window)
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
        self.tableAssembly=QtWidgets.QTableView(parent=self.frame)
        self.model = EditableTableModel()
        self.tableAssembly.setObjectName("tableAssembly")
        self.gridLayout_2.addWidget(self.tableAssembly, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        Assembly_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Assembly_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        Assembly_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Assembly_Window)
        self.statusbar.setObjectName("statusbar")
        Assembly_Window.setStatusBar(self.statusbar)
        self.tableAssembly.setSortingEnabled(True)
        self.tableAssembly.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        # Assembly_Window.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.retranslateUi(Assembly_Window)
        QtCore.QMetaObject.connectSlotsByName(Assembly_Window)

        self.model.setTable("public.orders")
        self.model.setFilter("num_order LIKE 'P-%' AND num_order NOT LIKE '%R%' AND (porc_deliveries <> 100 OR porc_deliveries IS NULL)")
        self.model.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model.select()
        self.tableAssembly.setModel(self.model)

        for i in range(1,4):
            self.tableAssembly.hideColumn(i)
        for i in range(5,15):
            self.tableAssembly.hideColumn(i)
        for i in range(19,23):
            self.tableAssembly.hideColumn(i)

        headers=['Nº Pedido', '','','','Fecha Contractual','','','','','','','','','','',
                '% Montaje','Fecha Recepción','Fecha Prevista','Observaciones',
                '', '', '', '','OK']

        self.tableAssembly.setItemDelegate(AlignDelegate(self.tableAssembly))
        self.color_delegate = ColorDelegate(self)
        self.tableAssembly.setItemDelegateForColumn(15, self.color_delegate)
        self.tableAssembly.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableAssembly.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableAssembly.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableAssembly.horizontalHeader().setSectionResizeMode(15, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableAssembly.horizontalHeader().setSectionResizeMode(16, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableAssembly.horizontalHeader().setSectionResizeMode(17, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableAssembly.horizontalHeader().setSectionResizeMode(18, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableAssembly.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_2.addWidget(self.tableAssembly, 3, 0, 1, 1)

        self.model.setAllColumnHeaders(headers)

    def retranslateUi(self, Assembly_Window):
        _translate = QtCore.QCoreApplication.translate
        Assembly_Window.setWindowTitle(_translate("EditTags_Window", "Montaje"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     config_obj = configparser.ConfigParser()
#     config_obj.read(r"C:\Program Files\ERP EIPSA\database.ini")
#     dbparam = config_obj["postgresql"]
#     # set your parameters for the database connection URI using the keys from the configfile.ini
#     user_database = dbparam["user"]
#     password_database = dbparam["password"]

#     if not createConnection(user_database, password_database):
#         sys.exit()

#     Assembly_Window = Ui_Assembly_Window()
#     Assembly_Window.show()
#     sys.exit(app.exec())