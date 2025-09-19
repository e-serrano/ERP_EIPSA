from PyQt6 import QtGui, QtWidgets
from config import get_path


def show_message(text, level="info"):
    dlg = QtWidgets.QMessageBox()
    new_icon = QtGui.QIcon()
    new_icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    dlg.setWindowIcon(new_icon)
    dlg.setWindowTitle("EIPSA ERP")
    dlg.setText(text)
    
    if level == "warning":
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
    elif level == "critical":
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
    else:
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)

    dlg.exec()