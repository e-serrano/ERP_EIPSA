import sys
from PyQt6 import QtWidgets
from Login_Window import Ui_Login_Window


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    log_window=QtWidgets.QMainWindow()
    ui=Ui_Login_Window()
    ui.setupUi(log_window)
    log_window.show()
    sys.exit(app.exec())