import sys
from PyQt6 import QtWidgets
from Login_Window import Ui_Login_Window
import os
from PyQt6 import QtGui, QtCore
import os
import psutil

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"
shutdown_file = r"\\nas01\DATOS\Comunes\ENRIQUE SERRANO\00 ERP\shutdown.txt"  # Ruta del archivo de señal

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_shutdown_signal)
        self.timer.start(1000)  # Verify every 1000 ms (1 second)

    def close_all_instances(self, executable_name):
        """Close all instances of executable selected."""
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process.info['name'] == executable_name:
                print(f"Cerrando proceso: {process.info['name']} (PID: {process.info['pid']})")
                process.terminate()  # Termina el proceso

    def check_shutdown_signal(self):
        """Check if the shutdown signal file indicates a closure."""
        try:
            if os.path.exists(shutdown_file):
                with open(shutdown_file, 'r') as f:
                    content = f.read().strip()  # Read the content of the file
                    if content != "OK":
                        print("Recibiendo comando de cierre...")
                        self.close_all_instances("EIPSA-ERP.exe")
                        self.close()
                        sys.exit()  # Exit the application
        except Exception as e:
            print(f"Error al verificar el archivo de señal: {e}")

if __name__ == "__main__":
    """
    Entry point for the application. Initializes the Qt application and displays the login window if the configuration
    file exists. If the configuration file is not found, displays an error message.

    - Checks if the configuration file `database.ini` exists in the specified directory.
    - If the file exists, creates and shows the login window.
    - If the file does not exist, displays an error message indicating that the configuration file is missing.

    Exits the application when the login window is closed or if the configuration file is missing.
    """
    base_dir = r"C:\Program Files\ERP EIPSA"

    # Full path of .ini file
    ini_file_path = os.path.abspath(os.path.join(base_dir, "database.ini"))
    app = QtWidgets.QApplication(sys.argv)

    if os.path.exists(ini_file_path):
        log_window=MainWindow()
        ui=Ui_Login_Window()
        ui.setupUi(log_window)
        log_window.show()
        sys.exit(app.exec())

    else:
        dlg = QtWidgets.QMessageBox()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle("ERP EIPSA")
        dlg.setText("Archivo de configuraión no encontrado.\nPonte en contacto con el administrador")
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        dlg.exec()
        del dlg, new_icon