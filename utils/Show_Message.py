from PySide6 import QtGui, QtWidgets
from config.config_functions import get_path

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
    def _create_input_dialog(cls, label, title=None) -> QtWidgets.QInputDialog:
        dlg = QtWidgets.QInputDialog()
        dlg.setWindowTitle(title or cls.DEFAULT_TITLE)
        dlg.setLabelText(label)

        icon = QtGui.QIcon()
        icon.addPixmap( QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off )
        dlg.setWindowIcon(icon)

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

    @classmethod
    def ask_text(cls, label, title=None):
        """ Shows an input dialog and returns the entered text.
        Returns None if the user cancels the dialog. """
        dlg = cls._create_input_dialog(label, title)
        if dlg.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            return dlg.textValue()

        return None

    @classmethod
    def ask_text_required(cls, label, title=None, error_message=None):
        while True:
            value = cls.ask_text(label, title)

            if value is None:
                return None

            if value:
                return value

            if error_message:
                cls.show_message(error_message, "warning")

    @classmethod
    def ask_item(cls, items, label, title=None, current=0, editable=False):
        """
        Shows an input dialog with a list of options.

        Returns:
            tuple[str, bool]: selected item and whether the user accepted.
        """
        dlg = cls._create_input_dialog(label, title)

        dlg.setComboBoxItems(items)
        dlg.setComboBoxEditable(editable)

        combo = dlg.findChild(QtWidgets.QComboBox)
        if combo:
            combo.setCurrentIndex(current)

        result = dlg.exec()

        return dlg.textValue(), result == QtWidgets.QDialog.DialogCode.Accepted