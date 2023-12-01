# Form implementation generated from reading ui file 'TAGOfferToOrder_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import pandas as pd
from tkinter.filedialog import askopenfilename
import psycopg2
from config import config
import os
from datetime import *

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class Ui_TAGOfferToOrder_Window(object):
    def setupUi(self, TAGOfferToOrder_Window):
        TAGOfferToOrder_Window.setObjectName("TAGOfferToOrder_Window")
        TAGOfferToOrder_Window.resize(640, 330)
        TAGOfferToOrder_Window.setMinimumSize(QtCore.QSize(640, 330))
        TAGOfferToOrder_Window.setMaximumSize(QtCore.QSize(640, 330))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        TAGOfferToOrder_Window.setWindowIcon(icon)
        TAGOfferToOrder_Window.setStyleSheet("QWidget {\n"
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
        self.centralwidget = QtWidgets.QWidget(parent=TAGOfferToOrder_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hLayout1 = QtWidgets.QHBoxLayout()
        self.hLayout1.setObjectName("hLayout1")
        self.label_SelectFile = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_SelectFile.setFont(font)
        self.label_SelectFile.setObjectName("label_SelectFile")
        self.hLayout1.addWidget(self.label_SelectFile)
        self.Button_Select = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Select.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Select.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Select.setObjectName("Button_Select")
        self.hLayout1.addWidget(self.Button_Select)
        self.verticalLayout.addLayout(self.hLayout1)
        self.label_name_file = QtWidgets.QLabel(parent=self.frame)
        self.label_name_file.setMinimumSize(QtCore.QSize(0, 25))
        self.label_name_file.setMaximumSize(QtCore.QSize(16777215, 25))
        self.label_name_file.setObjectName("label_name_file")
        self.verticalLayout.addWidget(self.label_name_file)
        self.hLayout2 = QtWidgets.QHBoxLayout()
        self.hLayout2.setObjectName("hLayout2")
        self.label_ItemType = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_ItemType.setFont(font)
        self.label_ItemType.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_ItemType.setObjectName("label_ItemType")
        self.hLayout2.addWidget(self.label_ItemType)
        self.vLayout = QtWidgets.QVBoxLayout()
        self.vLayout.setObjectName("vLayout")
        self.radioFlow = QtWidgets.QRadioButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioFlow.setFont(font)
        self.radioFlow.setObjectName("radioFlow")
        self.vLayout.addWidget(self.radioFlow)
        self.radioTemp = QtWidgets.QRadioButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioTemp.setFont(font)
        self.radioTemp.setObjectName("radioTemp")
        self.vLayout.addWidget(self.radioTemp)
        self.radioLevel = QtWidgets.QRadioButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioLevel.setFont(font)
        self.radioLevel.setObjectName("radioLevel")
        self.vLayout.addWidget(self.radioLevel)
        self.radioOthers = QtWidgets.QRadioButton(parent=self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioOthers.setFont(font)
        self.radioOthers.setObjectName("radioOthers")
        self.vLayout.addWidget(self.radioOthers)
        self.hLayout2.addLayout(self.vLayout)
        self.verticalLayout.addLayout(self.hLayout2)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.hLayout3 = QtWidgets.QHBoxLayout()
        self.hLayout3.setObjectName("hLayout3")
        self.Button_Import = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Import.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Import.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Import.setObjectName("Button_Import")
        self.hLayout3.addWidget(self.Button_Import)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(250, 35))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(250, 35))
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.hLayout3.addWidget(self.Button_Cancel)
        self.verticalLayout.addLayout(self.hLayout3)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        TAGOfferToOrder_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=TAGOfferToOrder_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName("menubar")
        TAGOfferToOrder_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=TAGOfferToOrder_Window)
        self.statusbar.setObjectName("statusbar")
        TAGOfferToOrder_Window.setStatusBar(self.statusbar)

        self.retranslateUi(TAGOfferToOrder_Window)
        self.Button_Cancel.clicked.connect(TAGOfferToOrder_Window.close)
        self.Button_Select.clicked.connect(self.browsefiles) # type: ignore
        self.Button_Import.clicked.connect(self.importtag)

        QtCore.QMetaObject.connectSlotsByName(TAGOfferToOrder_Window)


    def retranslateUi(self, TAGOfferToOrder_Window):
        _translate = QtCore.QCoreApplication.translate
        TAGOfferToOrder_Window.setWindowTitle(_translate("TAGOfferToOrder_Window", "TAG Oferta a Pedido"))
        self.label_SelectFile.setText(_translate("TAGOfferToOrder_Window", "Seleccionar archivo:"))
        self.Button_Select.setText(_translate("TAGOfferToOrder_Window", "Seleccionar"))
        self.label_name_file.setText(_translate("TAGOfferToOrder_Window", ""))
        self.label_ItemType.setText(_translate("TAGOfferToOrder_Window", "Tipo de equipo:"))
        self.radioFlow.setText(_translate("TAGOfferToOrder_Window", "Caudal"))
        self.radioTemp.setText(_translate("TAGOfferToOrder_Window", "Temperatura"))
        self.radioLevel.setText(_translate("TAGOfferToOrder_Window", "Nivel"))
        self.radioOthers.setText(_translate("TAGOfferToOrder_Window", "Otros"))
        self.Button_Import.setText(_translate("TAGOfferToOrder_Window", "Importar"))
        self.Button_Cancel.setText(_translate("TAGOfferToOrder_Window", "Cancelar"))


    def browsefiles(self):
        fname = askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx")],
                            title="Seleccionar archivo Excel")
        if fname:
            self.label_name_file.setText("Archivo: " + fname)


    def importtag(self):
        if self.label_name_file.text()=='':
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("ERP EIPSA")
            dlg.setText("Selecciona un archivo para importar")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()
            del dlg, new_icon

        else:
            excel_file=self.label_name_file.text().split("Archivo: ")[1]

            params = config()
            conn = psycopg2.connect(**params)
            cursor = conn.cursor()

        #Importing excel file into dataframe
            df_table = pd.read_excel(excel_file, na_values=['N/A'], keep_default_na=False, skiprows=7)
            df_table = df_table.astype(str)
            df_table.replace('nan', 'N/A', inplace=True)

            if self.radioFlow.isChecked()==True:
                table_name='tags_data.tags_flow'
                df_final = df_table.iloc[:,:32]
            elif self.radioTemp.isChecked()==True:
                table_name='tags_data.tags_temp'
                df_final = df_table.iloc[:,:37]
            elif self.radioLevel.isChecked()==True:
                table_name= 'tags_data.tags_level'
                df_final = df_table.iloc[:,:38]
            elif self.radioOthers.isChecked()==True:
                table_name= '' 
            else:
                table_name= '' 
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                dlg.setWindowIcon(new_icon)
                dlg.setWindowTitle("ERP EIPSA")
                dlg.setText("Selecciona un tipo de equipo")
                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                dlg.exec()
                del dlg, new_icon

            if table_name != '':
                try:
                    for index, row in df_final.iterrows():
                        if "ID" in row and "tag" in row and "tag_state" in row:
                            id_value = row["ID"]
                            tag_value = row["tag"]
                            state_value = row["tag_state"]
                            new_num_order = row["num_order"]
                            new_num_po = row["num_po"]
                            new_position = row["position"]
                            new_subposition = row["subposition"]

                        # Creating the SET clause with proper formatting
                            set_clause = f'"tag_state" = \'{state_value}\', "num_order" = \'{new_num_order}\', "num_po" = \'{new_num_po}\', "position" = \'{new_position}\', "subposition" = \'{new_subposition}\''

                        # Creating the WHERE clause with proper formatting
                            if self.radioFlow.isChecked()==True:
                                where_clause = f'"id_tag_flow" = \'{id_value}\' AND "tag" = \'{tag_value}\''
                            elif self.radioTemp.isChecked()==True:
                                where_clause = f'"id_tag_temp" = \'{id_value}\' AND "tag" = \'{tag_value}\''
                            elif self.radioLevel.isChecked()==True:
                                where_clause = f'"id_tag_level" = \'{id_value}\' AND "tag" = \'{tag_value}\''

                        # Creating the update query and executing it
                            sql_update = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause}'
                            if self.radioFlow.isChecked()==True:
                                sql_check = f'SELECT * FROM {table_name} WHERE "id_tag_flow" = \'{id_value}\' AND "tag" = \'{tag_value}\''
                            elif self.radioTemp.isChecked()==True:
                                sql_check = f'SELECT * FROM {table_name} WHERE "id_tag_temp" = \'{id_value}\' AND "tag" = \'{tag_value}\''
                            elif self.radioLevel.isChecked()==True:
                                sql_check = f'SELECT * FROM {table_name} WHERE "id_tag_level" = \'{id_value}\' AND "tag" = \'{tag_value}\''
                            cursor.execute(sql_check)
                            result_check=cursor.fetchall()

                            if len(result_check) == 0:
                                dlg = QtWidgets.QMessageBox()
                                new_icon = QtGui.QIcon()
                                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                                dlg.setWindowIcon(new_icon)
                                dlg.setWindowTitle("ERP EIPSA")
                                dlg.setText(f"El ID \'{id_value}\' no se corresponde con el TAG \'{tag_value}\' \n"
                                            "Este TAG no se actualizará")
                                dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                                dlg.exec()
                                del dlg, new_icon

                            cursor.execute(sql_update)

                # Closing cursor and database connection
                    conn.commit()
                    cursor.close()

                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("ERP EIPSA")
                    dlg.setText("Datos importados con éxito")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    dlg.exec()
                    del dlg, new_icon

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

            self.label_name_file.setText("")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    TAGOfferToOrder_Window = QtWidgets.QMainWindow()
    ui = Ui_TAGOfferToOrder_Window()
    ui.setupUi(TAGOfferToOrder_Window)
    TAGOfferToOrder_Window.show()
    sys.exit(app.exec())