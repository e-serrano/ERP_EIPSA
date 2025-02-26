# Form implementation generated from reading ui file 'ExportDocs_Menu.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets

from OfferExport_Window import Ui_ExportOffer_Window
from OrderAccept_Window import Ui_OrderAccept_Window
import os
from config import config
import psycopg2
from Excel_Export_Templates import order_ovr, doc_situation, vendor_progress_report, spares_two_years

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"

class Ui_ExportDocs_Menu(object):
    """
    UI class for the Export Docs Menu window.
    """
    def __init__(self, username):
        """
        Initializes the Ui_ExportDocs_Menu with the specified username.

        Args:
            username (str): username associated with the window.
        """
        self.username = username

    def setupUi(self, ExportDocs_Menu):
        """
        Sets up the user interface for the ExportDocs_Menu.

        Args:
            ExportDocs_Menu (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        ExportDocs_Menu.setObjectName("Type_Tag_Menu")
        ExportDocs_Menu.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        ExportDocs_Menu.resize(300, 500)
        ExportDocs_Menu.setMinimumSize(QtCore.QSize(300, 500))
        ExportDocs_Menu.setMaximumSize(QtCore.QSize(300, 500))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ExportDocs_Menu.setWindowIcon(icon)
        ExportDocs_Menu.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=ExportDocs_Menu)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(275, 425))
        self.frame.setMaximumSize(QtCore.QSize(275, 425))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem5 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem5, 0, 0, 1, 1)
        self.Button_ExportOffer = QtWidgets.QPushButton(parent=self.frame)
        self.Button_ExportOffer.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_ExportOffer.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_ExportOffer.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_ExportOffer.setObjectName("Button_ExportOffer")
        self.gridLayout_2.addWidget(self.Button_ExportOffer, 1, 0, 1, 1)
        self.Button_OrderAccept = QtWidgets.QPushButton(parent=self.frame)
        self.Button_OrderAccept.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_OrderAccept.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_OrderAccept.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_OrderAccept.setObjectName("Button_OrderAccept")
        self.gridLayout_2.addWidget(self.Button_OrderAccept, 2, 0, 1, 1)
        self.Button_OVR = QtWidgets.QPushButton(parent=self.frame)
        self.Button_OVR.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_OVR.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_OVR.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_OVR.setObjectName("Button_OVR")
        self.gridLayout_2.addWidget(self.Button_OVR, 3, 0, 1, 1)
        self.Button_DocSituation = QtWidgets.QPushButton(parent=self.frame)
        self.Button_DocSituation.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_DocSituation.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_DocSituation.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_DocSituation.setObjectName("Button_DocSituation")
        self.gridLayout_2.addWidget(self.Button_DocSituation, 4, 0, 1, 1)
        self.Button_VPR = QtWidgets.QPushButton(parent=self.frame)
        self.Button_VPR.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_VPR.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_VPR.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_VPR.setObjectName("Button_VPR")
        self.gridLayout_2.addWidget(self.Button_VPR, 5, 0, 1, 1)
        self.Button_Spares = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Spares.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Spares.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Spares.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Spares.setObjectName("Button_Spares")
        self.gridLayout_2.addWidget(self.Button_Spares, 6, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(140, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Cancel.setEnabled(True)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.horizontalLayout.addWidget(self.Button_Cancel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 7, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        ExportDocs_Menu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=ExportDocs_Menu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 22))
        self.menubar.setObjectName("menubar")
        ExportDocs_Menu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=ExportDocs_Menu)
        self.statusbar.setObjectName("statusbar")
        ExportDocs_Menu.setStatusBar(self.statusbar)

        self.retranslateUi(ExportDocs_Menu)
        self.Button_Cancel.clicked.connect(ExportDocs_Menu.close) # type: ignore
        self.Button_ExportOffer.clicked.connect(self.export_offer)
        self.Button_OrderAccept.clicked.connect(self.order_accept)
        self.Button_OVR.clicked.connect(self.order_ovr)
        self.Button_DocSituation.clicked.connect(self.doc_situation)
        self.Button_VPR.clicked.connect(self.vendor_progress)
        self.Button_Spares.clicked.connect(self.spares)
        QtCore.QMetaObject.connectSlotsByName(ExportDocs_Menu)


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, ExportDocs_Menu):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        ExportDocs_Menu.setWindowTitle(_translate("ExportDocs_Menu", "Generar Documentos"))
        self.Button_OrderAccept.setText(_translate("ExportDocs_Menu", "Acuse Pedido"))
        self.Button_ExportOffer.setText(_translate("ExportDocs_Menu", "Exportar Oferta"))
        self.Button_OVR.setText(_translate("ExportDocs_Menu", "Generar OVR"))
        self.Button_DocSituation.setText(_translate("ExportDocs_Menu", "Situación Doc."))
        self.Button_VPR.setText(_translate("ExportDocs_Menu", "Generar VPR"))
        self.Button_Spares.setText(_translate("ExportDocs_Menu", "Generar Repuestos"))
        self.Button_Cancel.setText(_translate("ExportDocs_Menu", "Cancelar"))

# Function to export offers in excel format
    def export_offer(self):
        """
        Opens the 'export_offer' window. Sets up the UI for the user.
        """
        self.exportoffer_window=QtWidgets.QMainWindow()
        self.ui=Ui_ExportOffer_Window(self.username)
        self.ui.setupUi(self.exportoffer_window)
        self.exportoffer_window.show()

# Function to export order acceptation in word format
    def order_accept(self):
        """
        Opens the 'order_accept' window. Sets up the UI for the user.
        """
        self.orderaccept_window=QtWidgets.QMainWindow()
        self.ui=Ui_OrderAccept_Window(self.username)
        self.ui.setupUi(self.orderaccept_window)
        self.orderaccept_window.show()

# Function to export order OVR in excel format
    def order_ovr(self):
        """
        Exort OVR data for a given order
        """
        dlg = QtWidgets.QInputDialog()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle('Generar OVR')
        dlg.setLabelText('Introduce un pedido (P-XX/YYY):')

        while True:
            clickedButton = dlg.exec()
            if clickedButton == 1:
                num_order = dlg.textValue()
                if num_order != '':
                    commands_checkorder = ("""
                            SELECT *
                            FROM orders
                            WHERE "num_order" LIKE ('%%'||%s||'%%')
                            """)
                    conn = None
                    try:
                    # read the connection parameters
                        params = config()
                    # connect to the PostgreSQL server
                        conn = psycopg2.connect(**params)
                        cur = conn.cursor()
                    # execution of commands one by one
                        cur.execute(commands_checkorder,(num_order,))
                        results=cur.fetchall()
                    # close communication with the PostgreSQL database server
                        cur.close()
                    # commit the changes
                        conn.commit()

                    except (Exception, psycopg2.DatabaseError) as error:
                        dlg_error_db = QtWidgets.QMessageBox()
                        new_icon = QtGui.QIcon()
                        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                        dlg_error_db.setWindowIcon(new_icon)
                        dlg_error_db.setWindowTitle("ERP EIPSA")
                        dlg_error_db.setText("Ha ocurrido el siguiente error:\n"
                                    + str(error))
                        dlg_error_db.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        dlg_error_db.exec()
                        del dlg_error_db, new_icon

                    finally:
                        if conn is not None:
                            conn.close()

                    if len(results) == 0:
                        dlg_no_order = QtWidgets.QMessageBox()
                        new_icon = QtGui.QIcon()
                        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                        dlg_no_order.setWindowIcon(new_icon)
                        dlg_no_order.setWindowTitle("Generar OVR")
                        dlg_no_order.setText("El número de pedido introducido no existe. Introduce un pedido válido")
                        dlg_no_order.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        dlg_no_order.exec()
                        del dlg, new_icon
                        break

                    else:
                        order_ovr(num_order)
                        break
                dlg_error = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg_error.setWindowIcon(new_icon)
                dlg_error.setWindowTitle("Generar OVR")
                dlg_error.setText("El pedido no puede estar vacío. Introduce un valor válido.")
                dlg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg_error.exec()
                del dlg_error,new_icon
            else:
                break

# Function to export document situation of orders in excel format
    def doc_situation(self):
        """
        Export document situation for a given order
        """
        dlg = QtWidgets.QInputDialog()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle('Situación Docs.')
        dlg.setLabelText('Introduce una referencia (Ej: 1023010920):')

        while True:
            clickedButton = dlg.exec()
            if clickedButton == 1:
                num_order = dlg.textValue()
                if num_order != '':
                    commands_checkorder = ("""
                            SELECT offers."project"
                            FROM orders
                            INNER JOIN offers ON orders."num_offer" = offers."num_offer"
                            WHERE "num_ref_order" LIKE (%s||'%%')
                            """)
                    conn = None
                    try:
                    # read the connection parameters
                        params = config()
                    # connect to the PostgreSQL server
                        conn = psycopg2.connect(**params)
                        cur = conn.cursor()
                    # execution of commands one by one
                        cur.execute(commands_checkorder,(num_order,))
                        results=cur.fetchall()

                        project = results[0][0]
                    # close communication with the PostgreSQL database server
                        cur.close()
                    # commit the changes
                        conn.commit()

                    except (Exception, psycopg2.DatabaseError) as error:
                        dlg_error_db = QtWidgets.QMessageBox()
                        new_icon = QtGui.QIcon()
                        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                        dlg_error_db.setWindowIcon(new_icon)
                        dlg_error_db.setWindowTitle("ERP EIPSA")
                        dlg_error_db.setText("Ha ocurrido el siguiente error:\n"
                                    + str(error))
                        dlg_error_db.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        dlg_error_db.exec()
                        del dlg_error_db, new_icon

                    finally:
                        if conn is not None:
                            conn.close()

                    if len(results) == 0:
                        dlg_no_order = QtWidgets.QMessageBox()
                        new_icon = QtGui.QIcon()
                        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                        dlg_no_order.setWindowIcon(new_icon)
                        dlg_no_order.setWindowTitle("Situación Docs.")
                        dlg_no_order.setText("El número de referencia introducido no existe. Introduce una referencia válido")
                        dlg_no_order.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        dlg_no_order.exec()
                        del dlg_no_order, new_icon
                        break

                    else:
                        try:
                            excel_to_export = doc_situation(num_order, project)
                            excel_to_export.save_excel_doc()

                            dlg_final= QtWidgets.QMessageBox()
                            new_icon = QtGui.QIcon()
                            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                            dlg_final.setWindowIcon(new_icon)
                            dlg_final.setWindowTitle("Situación Docs.")
                            dlg_final.setText("Excel generado con éxito")
                            dlg_final.setIcon(QtWidgets.QMessageBox.Icon.Information)
                            dlg_final.exec()
                            del dlg_final, new_icon
                        
                        except (Exception, psycopg2.DatabaseError) as error:
                            dlg_error_db = QtWidgets.QMessageBox()
                            new_icon = QtGui.QIcon()
                            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                            dlg_error_db.setWindowIcon(new_icon)
                            dlg_error_db.setWindowTitle("ERP EIPSA")
                            dlg_error_db.setText("Ha ocurrido el siguiente error:\n"
                                        + str(error))
                            dlg_error_db.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                            dlg_error_db.exec()
                            del dlg_error_db, new_icon

                        finally:
                            if conn is not None:
                                conn.close()

                        break
                dlg_error = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg_error.setWindowIcon(new_icon)
                dlg_error.setWindowTitle("Situación Docs.")
                dlg_error.setText("La referencia no puede estar vacía. Introduce un valor válido.")
                dlg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg_error.exec()
                del dlg_error,new_icon
            else:
                break

# Function to export document situation of orders in excel format
    def vendor_progress(self):
        """
        Export report of progress for a given order
        """
        dlg = QtWidgets.QInputDialog()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle('VPR')
        dlg.setLabelText('Introduce una referencia (Ej: 1023010920):')

        while True:
            clickedButton = dlg.exec()
            if clickedButton == 1:
                num_ref = dlg.textValue()
                if num_ref != '':
                    commands_checkorder = ("""
                            SELECT orders."num_ref_order"
                            FROM orders
                            WHERE "num_ref_order" LIKE (%s||'%%')
                            """)
                    conn = None
                    try:
                    # read the connection parameters
                        params = config()
                    # connect to the PostgreSQL server
                        conn = psycopg2.connect(**params)
                        cur = conn.cursor()
                    # execution of commands one by one
                        cur.execute(commands_checkorder,(num_ref,))
                        results=cur.fetchall()

                    # close communication with the PostgreSQL database server
                        cur.close()
                    # commit the changes
                        conn.commit()

                    except (Exception, psycopg2.DatabaseError) as error:
                        dlg_error_db = QtWidgets.QMessageBox()
                        new_icon = QtGui.QIcon()
                        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                        dlg_error_db.setWindowIcon(new_icon)
                        dlg_error_db.setWindowTitle("ERP EIPSA")
                        dlg_error_db.setText("Ha ocurrido el siguiente error:\n"
                                    + str(error))
                        dlg_error_db.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        dlg_error_db.exec()
                        del dlg_error_db, new_icon

                    finally:
                        if conn is not None:
                            conn.close()

                    if len(results) == 0:
                        dlg_no_order = QtWidgets.QMessageBox()
                        new_icon = QtGui.QIcon()
                        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                        dlg_no_order.setWindowIcon(new_icon)
                        dlg_no_order.setWindowTitle("VPR")
                        dlg_no_order.setText("El número de referencia introducido no existe. Introduce una referencia válido")
                        dlg_no_order.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        dlg_no_order.exec()
                        del dlg_no_order, new_icon
                        break

                    else:
                        try:
                            excel_to_export = vendor_progress_report(num_ref)
                            excel_to_export.save_excel_doc()

                            dlg_final= QtWidgets.QMessageBox()
                            new_icon = QtGui.QIcon()
                            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                            dlg_final.setWindowIcon(new_icon)
                            dlg_final.setWindowTitle("VPR")
                            dlg_final.setText("Excel generado con éxito")
                            dlg_final.setIcon(QtWidgets.QMessageBox.Icon.Information)
                            dlg_final.exec()
                            del dlg_final, new_icon
                        
                        except (Exception, psycopg2.DatabaseError) as error:
                            dlg_error_db = QtWidgets.QMessageBox()
                            new_icon = QtGui.QIcon()
                            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                            dlg_error_db.setWindowIcon(new_icon)
                            dlg_error_db.setWindowTitle("ERP EIPSA")
                            dlg_error_db.setText("Ha ocurrido el siguiente error:\n"
                                        + str(error))
                            dlg_error_db.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                            dlg_error_db.exec()
                            del dlg_error_db, new_icon

                        finally:
                            if conn is not None:
                                conn.close()

                        break
                dlg_error = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg_error.setWindowIcon(new_icon)
                dlg_error.setWindowTitle("VPR")
                dlg_error.setText("La referencia no puede estar vacía. Introduce un valor válido.")
                dlg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg_error.exec()
                del dlg_error,new_icon
            else:
                break

# Function to export spares in excel format
    def spares(self):
        """
        Exort spares for a given order
        """
        dlg = QtWidgets.QInputDialog()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle('Repuestos 2 años')
        dlg.setLabelText('Introduce un pedido (P-XX/YYY):')

        while True:
            clickedButton = dlg.exec()
            if clickedButton == 1:
                num_order = dlg.textValue()
                if num_order != '':
                    commands_checkorder = ("""
                            SELECT *
                            FROM orders
                            WHERE "num_order" LIKE ('%%'||%s||'%%')
                            """)
                    conn = None
                    try:
                    # read the connection parameters
                        params = config()
                    # connect to the PostgreSQL server
                        conn = psycopg2.connect(**params)
                        cur = conn.cursor()
                    # execution of commands one by one
                        cur.execute(commands_checkorder,(num_order,))
                        results=cur.fetchall()
                    # close communication with the PostgreSQL database server
                        cur.close()
                    # commit the changes
                        conn.commit()

                    except (Exception, psycopg2.DatabaseError) as error:
                        dlg_error_db = QtWidgets.QMessageBox()
                        new_icon = QtGui.QIcon()
                        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                        dlg_error_db.setWindowIcon(new_icon)
                        dlg_error_db.setWindowTitle("ERP EIPSA")
                        dlg_error_db.setText("Ha ocurrido el siguiente error:\n"
                                    + str(error))
                        dlg_error_db.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                        dlg_error_db.exec()
                        del dlg_error_db, new_icon

                    finally:
                        if conn is not None:
                            conn.close()

                    if len(results) == 0:
                        dlg_no_order = QtWidgets.QMessageBox()
                        new_icon = QtGui.QIcon()
                        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                        dlg_no_order.setWindowIcon(new_icon)
                        dlg_no_order.setWindowTitle("Repuestos")
                        dlg_no_order.setText("El número de pedido introducido no existe. Introduce un pedido válido")
                        dlg_no_order.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        dlg_no_order.exec()
                        del dlg, new_icon
                        break

                    else:
                        spares_two_years(num_order)
                        break
                dlg_error = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg_error.setWindowIcon(new_icon)
                dlg_error.setWindowTitle("Repuestos")
                dlg_error.setText("El pedido no puede estar vacío. Introduce un valor válido.")
                dlg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg_error.exec()
                del dlg_error,new_icon
            else:
                break



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ExportDocs_Menu = QtWidgets.QMainWindow()
    ui = Ui_ExportDocs_Menu('l.bravo')
    ui.setupUi(ExportDocs_Menu)
    ExportDocs_Menu.show()
    sys.exit(app.exec())
