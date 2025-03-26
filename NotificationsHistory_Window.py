# Form implementation generated from reading ui file 'HistoryNotifications_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from config import config
import psycopg2
import os
import configparser
from Database_Connection import createConnection

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


class Ui_HistoryNotifications_Window(QtWidgets.QMainWindow):
    """
    UI class for the History Notifications window.
    """
    def __init__(self, username):
        """
        Initializes the Ui_HistoryNotifications_Window with the specified username.

        Args:
            username (str): username associated with the window.
        """
        super().__init__()
        self.username = username
        self.setupUi(self)

    def setupUi(self, HistoryNotifications_Window):
        """
        Sets up the user interface for the HistoryNotifications_Window.

        Args:
            HistoryNotifications_Window (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        HistoryNotifications_Window.setObjectName("HistoryNotifications_Window")
        HistoryNotifications_Window.resize(400, 561)
        HistoryNotifications_Window.setMinimumSize(QtCore.QSize(600, 575))
        HistoryNotifications_Window.setMaximumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        HistoryNotifications_Window.setWindowIcon(icon)
        HistoryNotifications_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=HistoryNotifications_Window)
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
        # self.Button_Export = QtWidgets.QPushButton(parent=self.frame)
        # self.Button_Export.setMinimumSize(QtCore.QSize(100, 35))
        # self.Button_Export.setMaximumSize(QtCore.QSize(100, 35))
        # self.Button_Export.setObjectName("Button_Export")
        # self.gridLayout_2.addWidget(self.Button_Export, 1, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 2, 1, 1)
        self.tableNotifications = QtWidgets.QTableWidget(parent=self.frame)
        self.tableNotifications.setObjectName("tableWidget")
        self.tableNotifications.setColumnCount(4)
        self.tableNotifications.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableNotifications.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableNotifications.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableNotifications.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        item.setFont(font)
        self.tableNotifications.setHorizontalHeaderItem(3, item)
        self.gridLayout_2.addWidget(self.tableNotifications, 2, 0, 1, 3)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        HistoryNotifications_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=HistoryNotifications_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        HistoryNotifications_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=HistoryNotifications_Window)
        self.statusbar.setObjectName("statusbar")
        HistoryNotifications_Window.setStatusBar(self.statusbar)
        self.tableNotifications.verticalHeader().setVisible(True)
        self.tableNotifications.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableNotifications.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableNotifications.setSortingEnabled(False)
        self.tableNotifications.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        HistoryNotifications_Window.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.retranslateUi(HistoryNotifications_Window)
        QtCore.QMetaObject.connectSlotsByName(HistoryNotifications_Window)

        self.Button_Cancel.clicked.connect(HistoryNotifications_Window.close)
        self.tableNotifications.itemDoubleClicked.connect(self.on_item_double_clicked)
        # self.Button_Export.clicked.connect(self.export_to_excel)
        self.QueryNotification()


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, HistoryNotifications_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        HistoryNotifications_Window.setWindowTitle(_translate("HistoryNotifications_Window", "Notificaciones"))
        item = self.tableNotifications.horizontalHeaderItem(0)
        item.setText(_translate("HistoryNotifications_Window", "Tabla"))
        item = self.tableNotifications.horizontalHeaderItem(1)
        item.setText(_translate("HistoryNotifications_Window", "ID"))
        item = self.tableNotifications.horizontalHeaderItem(2)
        item.setText(_translate("HistoryNotifications_Window", "Mensaje"))
        self.Button_Cancel.setText(_translate("HistoryNotifications_Window", "Salir"))
        # self.Button_Export.setText(_translate("HistoryNotifications_Window", "Exportar"))


    def QueryNotification(self):
        """
        Queries the database for notifications, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.tableNotifications.setRowCount(0)
        query_tables_notifications = """SELECT table_name
                                FROM information_schema.tables
                                WHERE table_schema = 'notifications' AND table_type = 'BASE TABLE';"""
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            cur.execute(query_tables_notifications)
            results=cur.fetchall()
            tables_names=[x[0] for x in results]

            notifications = []

            for table in tables_names:
                commands_notifications = f" SELECT id, message FROM notifications.{table} WHERE username = '{self.username}' AND state = 'Pendiente'"
                cur.execute(commands_notifications)
                results=cur.fetchall()

                for x in results:
                    notifications.append([table,x[0],x[1],])

        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()

            self.tableNotifications.setRowCount(len(notifications))
            tablerow=0

        # fill the Qt Table with the query results
            for row in notifications:
                for column in range(3):
                    value = row[column]
                    if value is None:
                        value = ''
                    it = QtWidgets.QTableWidgetItem(str(value))
                    it.setFlags(it.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self.tableNotifications.setItem(tablerow, column, it)

                self.button = QtWidgets.QPushButton('Eliminar')
                self.tableNotifications.setCellWidget(tablerow, 3, self.button)
                self.button.clicked.connect(self.on_button_clicked)

                tablerow+=1

            self.tableNotifications.verticalHeader().hide()
            self.tableNotifications.setItemDelegate(AlignDelegate(self.tableNotifications))
            self.tableNotifications.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.tableNotifications.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
            self.tableNotifications.hideColumn(0)
            self.tableNotifications.sortByColumn(2, QtCore.Qt.SortOrder.AscendingOrder)

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


    def on_button_clicked(self, row):
        """
        Handles the event when a notification button is clicked.

        Args:
            row (int): The index of the clicked row in the notifications table.
        """
        button = self.sender()  
        index = self.tableNotifications.indexAt(button.pos()) 
        if index.isValid():
            row = index.row()
            table_name = self.tableNotifications.item(row, 0).text()
            id_notification = self.tableNotifications.item(row, 1).text()

        commands_editnotif = f" UPDATE notifications.{table_name} SET state = 'Visto' WHERE id = '{id_notification}'"
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands one by one
            cur.execute(commands_editnotif)
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

        self.QueryNotification()

# Function to check if column index of double clicked cell is equal to first column index
    def on_item_double_clicked(self, item):
        """
        Handles double-click events on items in a QTableWidget. Opens different forms based on the column of the clicked item.
        
        Args:
            item (QtWidgets.QTableWidgetItem): The item that was double-clicked.
        """
        if item.column() == 2 and item.text().split(': ')[0]=='Nuevo pedido':
            num_order = item.text().split(': ')[1].split('\n')[0]
            self.edit_tag(num_order)
        elif item.column() == 1:
            self.id_notification = item.text()
            self.show_dialog(self.id_notification)

# Function to open window for tag edition
    def edit_tag(self, num_order):
        """
        Opens a new window for editing existing tags. 
        """
        from TAGEdit_Technical_Window import Ui_EditTags_Technical_Window
        config_obj = configparser.ConfigParser()
        config_obj.read(r"C:\Program Files\ERP EIPSA\database.ini")
        dbparam = config_obj["postgresql"]
        # set your parameters for the database connection URI using the keys from the configfile.ini
        user_database = dbparam["user"]
        password_database = dbparam["password"]

        db_tags_tech_not = createConnection(user_database, password_database)
        if not db_tags_tech_not:
            sys.exit()  

        self.edit_tags_app = Ui_EditTags_Technical_Window(self.username, db_tags_tech_not, num_order)
        self.edit_tags_app.show()

# Function to show dialog to insert notes
    def show_dialog(self, id_notification):
        """
        Displays a dialog window allowing the user to view and edit notes.
        """
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            commands_notifications = f" SELECT notes, message FROM notifications.notifications_orders WHERE id = {id_notification}"
            cur.execute(commands_notifications)
            results=cur.fetchall()

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

        dlg = QtWidgets.QDialog()
        dlg.setWindowTitle(results[0][1].split('Proyecto')[0].split(': ')[1])
        dlg.setGeometry(50, 50, 900, 600)
        dlg.setWindowModality(QtCore.Qt.WindowModality.NonModal)

        vLayout = QtWidgets.QVBoxLayout(dlg)

        btn = QtWidgets.QPushButton("Guardar")
        vLayout.addWidget(btn)
        btn.clicked.connect(self.save_notes)
        
        self.te = QtWidgets.QTextEdit()
        self.te.setText(str(results[0][0] if results[0][0] is not None else ''))
        self.te.setStyleSheet("background-color: transparent;")
        vLayout.addWidget(self.te)

        # dlg.exec()

        dlg.show()

        self.dialog = dlg

# Function to save notes
    def save_notes(self):
        """
        Saves the supplier order comments to the database.
        """
        id_notification = self.id_notification
        notes_notification = self.te.toPlainText()

        commands_updateorder = ("""
                        UPDATE notifications.notifications_orders
                        SET "notes" = %s
                        WHERE "id" = %s
                        """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of principal command
            data=(notes_notification, id_notification,)
            cur.execute(commands_updateorder, data)
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




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HistoryNotifications_Window = Ui_HistoryNotifications_Window('e.carrillo')
    HistoryNotifications_Window.show()
    sys.exit(app.exec())