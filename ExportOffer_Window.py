# Form implementation generated from reading ui file 'ExportOffer_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import psycopg2
from config import config  
from openpyxl import load_workbook
import pandas as pd


class Ui_ExportOffer_Window(object):
    def setupUi(self, ExportOffer_Window):
        ExportOffer_Window.setObjectName("ExportOffer_Window")
        ExportOffer_Window.resize(275, 340)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ExportOffer_Window.sizePolicy().hasHeightForWidth())
        ExportOffer_Window.setSizePolicy(sizePolicy)
        ExportOffer_Window.setMaximumSize(QtCore.QSize(275, 340))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        ExportOffer_Window.setWindowIcon(icon)
        ExportOffer_Window.setAutoFillBackground(False)
        ExportOffer_Window.setStyleSheet("QWidget {\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
".QFrame {\n"
"    border: 2px solid black;\n"
"}")
        ExportOffer_Window.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(parent=ExportOffer_Window)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(230, 300))
        self.frame.setMaximumSize(QtCore.QSize(230, 300))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_numoffer_expoffer = QtWidgets.QLabel(parent=self.frame)
        self.label_numoffer_expoffer.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_numoffer_expoffer.sizePolicy().hasHeightForWidth())
        self.label_numoffer_expoffer.setSizePolicy(sizePolicy)
        self.label_numoffer_expoffer.setMinimumSize(QtCore.QSize(200, 25))
        self.label_numoffer_expoffer.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_numoffer_expoffer.setFont(font)
        self.label_numoffer_expoffer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_numoffer_expoffer.setObjectName("label_numoffer_expoffer")
        self.verticalLayout.addWidget(self.label_numoffer_expoffer, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.numoffer_expoffer = QtWidgets.QLineEdit(parent=self.frame)
        self.numoffer_expoffer.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numoffer_expoffer.sizePolicy().hasHeightForWidth())
        self.numoffer_expoffer.setSizePolicy(sizePolicy)
        self.numoffer_expoffer.setMinimumSize(QtCore.QSize(200, 25))
        self.numoffer_expoffer.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.numoffer_expoffer.setFont(font)
        self.numoffer_expoffer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.numoffer_expoffer.setObjectName("numoffer_expoffer")
        self.verticalLayout.addWidget(self.numoffer_expoffer, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.export_expoffer = QtWidgets.QPushButton(parent=self.frame)
        self.export_expoffer.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.export_expoffer.sizePolicy().hasHeightForWidth())
        self.export_expoffer.setSizePolicy(sizePolicy)
        self.export_expoffer.setMinimumSize(QtCore.QSize(200, 35))
        self.export_expoffer.setMaximumSize(QtCore.QSize(200, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.export_expoffer.setFont(font)
        self.export_expoffer.setStyleSheet("QPushButton {\n"
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
        self.export_expoffer.setAutoDefault(True)
        self.export_expoffer.setObjectName("export_expoffer")
        self.verticalLayout.addWidget(self.export_expoffer, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        ExportOffer_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=ExportOffer_Window)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 275, 22))
        self.menubar.setObjectName("menubar")
        ExportOffer_Window.setMenuBar(self.menubar)

        self.retranslateUi(ExportOffer_Window)
        self.export_expoffer.clicked.connect(self.exportoffer)
        QtCore.QMetaObject.connectSlotsByName(ExportOffer_Window)


    def retranslateUi(self, ExportOffer_Window):
        _translate = QtCore.QCoreApplication.translate
        ExportOffer_Window.setWindowTitle(_translate("ExportOffer_Window", "ERP EIPSA"))
        self.label_numoffer_expoffer.setText(_translate("ExportOffer_Window", "Número Oferta:"))
        self.export_expoffer.setText(_translate("ExportOffer_Window", "Exportar"))


    def exportoffer(self):
        numoffer=self.numoffer_expoffer.text()

        commands = ("""
                    SELECT * 
                    FROM offer
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
            cur.execute(commands,(numoffer,))
            results=cur.fetchall()
            match=list(filter(lambda x:numoffer in x, results))
        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        if numoffer=="" or (numoffer==" " or len(match)==0):
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Exportar Oferta")
            dlg.setText("El número de oferta no se encuentra registrado")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()

            del dlg, new_icon

        else:
            commands = ("""
                        SELECT *
                        FROM offer
                        WHERE "num_offer" = %s
                        """)
            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur=conn.cursor()
                cur.execute(commands,(numoffer,))
                data=cur.fetchall()

                columns=[]
                for elt in cur.description:
                    columns.append(elt[0])
                df = pd.DataFrame(data=data,columns=columns)

                # Export dataframe to an Excel file
                file_path = r"\\nas01\DATOS\Comunes\EIPSA-ERP\Plantillas Excel Ofertas\prueba.xlsx"
                book=load_workbook(file_path)
                writer = pd.ExcelWriter(file_path, engine='openpyxl')
                writer.book = book
                df.to_excel(writer, "Hoja1", startrow=6, index=False, header=False)
                writer.close()

            # close communication with the PostgreSQL database server
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
            dlg.setWindowTitle("Exportar Oferta")
            dlg.setText("Oferta exportada con éxito")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            dlg.exec()

            self.numoffer_expoffer.setText('')

            del dlg, new_icon


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExportOffer_Window = QtWidgets.QMainWindow()
    ui = Ui_ExportOffer_Window()
    ui.setupUi(ExportOffer_Window)
    ExportOffer_Window.show()
    sys.exit(app.exec())
