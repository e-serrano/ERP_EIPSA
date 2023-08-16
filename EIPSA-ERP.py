import sys
from PyQt6 import QtWidgets
from Login_Window import Ui_Login_Window
import os
from PyQt6 import QtGui

if __name__ == "__main__":
    base_dir = r"C:\Program Files\ERP EIPSA"

    # Full path of .ini file
    ini_file_path = os.path.join(base_dir, "database.ini")
    app = QtWidgets.QApplication(sys.argv)

    if os.path.exists(ini_file_path):
        log_window=QtWidgets.QMainWindow()
        ui=Ui_Login_Window()
        ui.setupUi(log_window)
        log_window.show()
        sys.exit(app.exec())
    
    else:
        dlg = QtWidgets.QMessageBox()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Recursos/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle("ERP EIPSA")
        dlg.setText("Archivo de configuraión no encontrado.\nPonte en contacto con el administrador")
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        dlg.exec()
        del dlg, new_icon