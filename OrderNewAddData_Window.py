# Form implementation generated from reading ui file 'NewOrderAddData_Window.ui'
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


basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class Ui_New_OrderAddData_Window(object):
    """
    UI class for the New Order Additional Data window.
    """
    def setupUi(self, New_OrderAddData):
        """
        Sets up the user interface for the New_OrderAddData.

        Args:
            New_OrderAddData (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        New_OrderAddData.setObjectName("New_OrderAddData")
        New_OrderAddData.resize(680, 425)
        New_OrderAddData.setMinimumSize(QtCore.QSize(775, 425))
        # New_OrderAddData.setMaximumSize(QtCore.QSize(775, 425))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        New_OrderAddData.setWindowIcon(icon)
        New_OrderAddData.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=New_OrderAddData)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_NumOffer = QtWidgets.QLabel(parent=self.frame)
        self.label_NumOffer.setMinimumSize(QtCore.QSize(135, 25))
        self.label_NumOffer.setMaximumSize(QtCore.QSize(135, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumOffer.setFont(font)
        self.label_NumOffer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_NumOffer.setObjectName("label_NumOffer")
        self.gridLayout_2.addWidget(self.label_NumOffer, 0, 0, 1, 1)
        self.NumOffer_NewOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.NumOffer_NewOrder.setMinimumSize(QtCore.QSize(130, 25))
        self.NumOffer_NewOrder.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumOffer_NewOrder.setFont(font)
        self.NumOffer_NewOrder.setObjectName("NumOffer_NewOrder")
        self.gridLayout_2.addWidget(self.NumOffer_NewOrder, 0, 1, 1, 1)
        self.label_Project = QtWidgets.QLabel(parent=self.frame)
        self.label_Project.setMinimumSize(QtCore.QSize(135, 25))
        self.label_Project.setMaximumSize(QtCore.QSize(135, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Project.setFont(font)
        self.label_Project.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_Project.setObjectName("label_Project")
        self.gridLayout_2.addWidget(self.label_Project, 0, 2, 1, 1)
        self.Project_NewOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.Project_NewOrder.setMinimumSize(QtCore.QSize(130, 25))
        self.Project_NewOrder.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Project_NewOrder.setFont(font)
        self.Project_NewOrder.setObjectName("Project_NewOrder")
        self.gridLayout_2.addWidget(self.Project_NewOrder, 0, 3, 1, 1)
        self.label_Validity = QtWidgets.QLabel(parent=self.frame)
        self.label_Validity.setMinimumSize(QtCore.QSize(135, 25))
        self.label_Validity.setMaximumSize(QtCore.QSize(135, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Validity.setFont(font)
        self.label_Validity.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_Validity.setObjectName("label_Validity")
        self.gridLayout_2.addWidget(self.label_Validity, 1, 0, 1, 1)
        self.Validity_NewOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.Validity_NewOrder.setMinimumSize(QtCore.QSize(130, 25))
        self.Validity_NewOrder.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Validity_NewOrder.setFont(font)
        self.Validity_NewOrder.setObjectName("Validity_NewOrder")
        self.gridLayout_2.addWidget(self.Validity_NewOrder, 1, 1, 1, 1)
        self.label_DelivTerm = QtWidgets.QLabel(parent=self.frame)
        self.label_DelivTerm.setMinimumSize(QtCore.QSize(110, 25))
        self.label_DelivTerm.setMaximumSize(QtCore.QSize(110, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_DelivTerm.setFont(font)
        self.label_DelivTerm.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_DelivTerm.setObjectName("label_DelivTerm")
        self.gridLayout_2.addWidget(self.label_DelivTerm, 1, 2, 1, 1)
        self.DelivTerm_NewOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.DelivTerm_NewOrder.setMinimumSize(QtCore.QSize(130, 25))
        self.DelivTerm_NewOrder.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DelivTerm_NewOrder.setFont(font)
        self.DelivTerm_NewOrder.setObjectName("DelivTerm_NewOrder")
        self.gridLayout_2.addWidget(self.DelivTerm_NewOrder, 1, 3, 1, 1)
        self.label_DelivTime = QtWidgets.QLabel(parent=self.frame)
        self.label_DelivTime.setMinimumSize(QtCore.QSize(175, 25))
        self.label_DelivTime.setMaximumSize(QtCore.QSize(175, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_DelivTime.setFont(font)
        self.label_DelivTime.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_DelivTime.setObjectName("label_DelivTime")
        self.gridLayout_2.addWidget(self.label_DelivTime, 2, 0, 1, 1)
        self.DelivTime_NewOrder = QtWidgets.QLineEdit(parent=self.frame)
        self.DelivTime_NewOrder.setMinimumSize(QtCore.QSize(130, 25))
        self.DelivTime_NewOrder.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DelivTime_NewOrder.setFont(font)
        self.DelivTime_NewOrder.setObjectName("DelivTime_NewOrder")
        self.gridLayout_2.addWidget(self.DelivTime_NewOrder, 2, 1, 1, 1)
        self.label_PayTerm = QtWidgets.QLabel(parent=self.frame)
        self.label_PayTerm.setMinimumSize(QtCore.QSize(110, 25))
        self.label_PayTerm.setMaximumSize(QtCore.QSize(110, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_PayTerm.setFont(font)
        self.label_PayTerm.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_PayTerm.setObjectName("label_PayTerm")
        self.gridLayout_2.addWidget(self.label_PayTerm, 2, 2, 1, 1)
        self.PayTerm_NewOrder = QtWidgets.QComboBox(parent=self.frame)
        self.PayTerm_NewOrder.setMinimumSize(QtCore.QSize(130, 25))
        self.PayTerm_NewOrder.setMaximumSize(QtCore.QSize(130, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PayTerm_NewOrder.setFont(font)
        self.PayTerm_NewOrder.setObjectName("PayTerm_NewOrder")
        self.gridLayout_2.addWidget(self.PayTerm_NewOrder, 2, 3, 1, 1)
        self.Button_Continue = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Continue.setMinimumSize(QtCore.QSize(10, 30))
        self.Button_Continue.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Button_Continue.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Continue.setAutoDefault(True)
        self.Button_Continue.setObjectName("Button_Continue")
        self.gridLayout_2.addWidget(self.Button_Continue, 3, 0, 1, 2)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(10, 30))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.Button_Cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Cancel.setAutoDefault(True)
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.gridLayout_2.addWidget(self.Button_Cancel, 3, 2, 1, 2)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        New_OrderAddData.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=New_OrderAddData)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 22))
        self.menubar.setObjectName("menubar")
        New_OrderAddData.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=New_OrderAddData)
        self.statusbar.setObjectName("statusbar")
        New_OrderAddData.setStatusBar(self.statusbar)
        New_OrderAddData.setWindowFlags(QtCore.Qt.WindowType.WindowMinimizeButtonHint)

        self.PayTerm_NewOrder.addItems(['', '100% entrega', '100% pedido', '90%-10%', '50%-50%', 'Otros'])

        self.retranslateUi(New_OrderAddData)
        self.Button_Cancel.clicked.connect(New_OrderAddData.close) # type: ignore
        self.Button_Continue.clicked.connect(lambda: self.NewOrder(New_OrderAddData))
        self.NumOffer_NewOrder.returnPressed.connect(self.queryofferdata)
        QtCore.QMetaObject.connectSlotsByName(New_OrderAddData)


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, New_OrderAddData):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        New_OrderAddData.setWindowTitle(_translate("New_OrderAddData", "Info Adicional"))
        self.label_Validity.setText(_translate("New_OrderAddData", "Validez Of. (días):"))
        self.label_NumOffer.setText(_translate("New_OrderAddData", "Nº Oferta:"))
        self.label_Project.setText(_translate("New_OrderAddData", "Proyecto:"))
        self.label_DelivTerm.setText(_translate("New_OrderAddData", "Cond. Entrega:"))
        self.label_DelivTime.setText(_translate("New_OrderAddData", "Pl. Entrega (semanas):"))
        self.label_PayTerm.setText(_translate("New_OrderAddData", "Forma Pago:"))
        self.Button_Continue.setText(_translate("New_OrderAddData", "Continuar"))
        self.Button_Cancel.setText(_translate("New_OrderAddData", "Cancelar"))


    def NewOrder(self, New_OrderAddData):
        """
        Creates a new entry in database after validating form inputs.
        """
        numoffer=self.NumOffer_NewOrder.text()
        validity=self.Validity_NewOrder.text()
        project=self.Project_NewOrder.text()
        delivterm=self.DelivTerm_NewOrder.text()
        delivtime=self.DelivTime_NewOrder.text()
        payterm = ('100_delivery' if self.PayTerm_NewOrder.currentText() == '100% entrega'
                    else ('100_order' if self.PayTerm_NewOrder.currentText() == '100% pedido'
                    else ('90_10' if self.PayTerm_NewOrder.currentText() == '90%-10%'
                    else ('50_50' if self.PayTerm_NewOrder.currentText() == '50%-50%'
                    else ('Others' if self.PayTerm_NewOrder.currentText() == 'Otros' else '')))))

        if numoffer=="" or (validity=="" or  (delivterm=="" or (delivtime=="" or payterm==""))):
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Nuevo Pedido")
            dlg.setText("Todos los campos deben estar rellenos")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()

        else:
            commands_offer = ("""
                        SELECT *
                        FROM offers
                        WHERE "num_offer" = %s
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

            else:
                commands_add_data = ("""
                            UPDATE offers
                            SET "validity" = %s, "delivery_term" = %s, "delivery_time" = %s, "payment_term" = %s, "project" = %s
                            WHERE "num_offer" = %s
                            """)

                conn = None
                try:
                # read the connection parameters
                    params = config()
                # connect to the PostgreSQL server
                    conn = psycopg2.connect(**params)
                    cur = conn.cursor()
                # execution of commands

                    data = (validity, delivterm, delivtime, payterm, project, numoffer)
                    cur.execute(commands_add_data, data)

                # close communication with the PostgreSQL database server
                    cur.close()
                # commit the changes
                    conn.commit()

                    from OrderNew_Window import Ui_New_Order_Window
                    self.new_order_window=QtWidgets.QMainWindow()
                    self.ui=Ui_New_Order_Window(numoffer)
                    self.ui.setupUi(self.new_order_window)
                    self.new_order_window.show()
                    New_OrderAddData.hide()
                    self.ui.Button_Cancel.clicked.connect(New_OrderAddData.show)

                except (Exception, psycopg2.DatabaseError) as error:
                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Nuevo Pedido")
                    dlg.setText("Ha ocurrido el siguiente error:\n"
                                + str(error))
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                    dlg.exec()
                finally:
                    if conn is not None:
                        conn.close()


    def queryofferdata(self):
        """
        Loads the form with the data of the offer inserted
        """
        numoffer=self.NumOffer_NewOrder.text()
    #SQL Query for loading existing data in database
        commands_loaddataoffer = ("""
                    SELECT offers."num_offer", offers."validity", offers."delivery_term", offers."delivery_time", offers."payment_term", offers."project"
                    FROM offers
                    WHERE "num_offer" = %s
                    """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands one by one
            cur.execute(commands_loaddataoffer,(numoffer,))
            results=cur.fetchall()
            match=list(filter(lambda x:numoffer in x, results))
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
            dlg.setWindowTitle("Nuevo Pedido")
            dlg.setText("El número de oferta introducido no existe")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()

        else:
            self.Validity_NewOrder.setText(str(results[0][1]) if str(results[0][1]) != 'None' else '')
            self.DelivTime_NewOrder.setText(str(results[0][3]) if str(results[0][3]) != 'None' else '')
            self.DelivTerm_NewOrder.setText(str(results[0][2]) if str(results[0][2]) != 'None' else '')
            

            payterm_text = ('100% entrega' if str(results[0][4]) == '100_delivery'
                    else ('100% pedido' if str(results[0][4]) == '100_order'
                    else ('90%-10%' if str(results[0][4]) == '90_10'
                    else ('50%-50%' if str(results[0][4]) == '50_50'
                    else ('Otros' if str(results[0][4]) == 'Others' else str(results[0][4]))))))
            
            self.PayTerm_NewOrder.setCurrentText(payterm_text if str(results[0][4]) != 'None' else '')

            self.Project_NewOrder.setText(str(results[0][5]) if str(results[0][5]) != 'None' else '')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    New_OrderAddData = QtWidgets.QMainWindow()
    ui = Ui_New_OrderAddData_Window()
    ui.setupUi(New_OrderAddData)
    New_OrderAddData.show()
    sys.exit(app.exec())
