from PyQt6 import QtGui, QtWidgets
from config import get_path

class MessageHelper:
    DEFAULT_TITLE = "EIPSA ERP"

    @classmethod
    def _create_dialog(cls, text, title = None, icon_type = None) -> QtWidgets.QMessageBox:
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle(title or cls.DEFAULT_TITLE)
        dlg.setText(text)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(icon)

        if icon_type:
            dlg.setIcon(icon_type)
        return dlg

    @classmethod
    def show_message(cls, text, level = "info"):
        """
        Shows informative, critical or warning message
        """
        icon_type = {
            "info": QtWidgets.QMessageBox.Icon.Information,
            "warning": QtWidgets.QMessageBox.Icon.Warning,
            "critical": QtWidgets.QMessageBox.Icon.Critical
        }.get(level, QtWidgets.QMessageBox.Icon.Information)

        dlg = cls._create_dialog(text, icon_type=icon_type)
        dlg.exec()

    @classmethod
    def ask_yes_no(cls, text, title) -> bool:
        """
        Shows dialog to select Yes/No and return True if user selects Yes
        """
        dlg = cls._create_dialog(text, title, icon_type=QtWidgets.QMessageBox.Icon.Warning)
        dlg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        result = dlg.exec()
        return result == QtWidgets.QMessageBox.StandardButton.Yes