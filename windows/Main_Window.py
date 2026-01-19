import sys
from PySide6 import QtWidgets, QtCore
from windows.Login_Window import Ui_Login_Window
import os
import psutil
from utils.Show_Message import MessageHelper
from config.config_functions import get_path
from config.config_keys import INI_FILE_PATH
from pathlib import Path


shutdown_file = get_path("Resources", "Logging", "shutdown.txt")


def get_functions_dir():
    # PRODUCCIÓN: ejecutando exe
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        return os.path.join(base_dir, "01 FUNCIONES")

    # DESARROLLO: ejecutando python normal
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return base_dir


FUNCTIONS_DIR = get_functions_dir()

if FUNCTIONS_DIR not in sys.path:
    sys.path.insert(0, FUNCTIONS_DIR)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_shutdown_signal)
        self.timer.start(3000)  # Verify every 3000 ms (3 second)

    def close_all_instances(self, executable_name):
        """Close all instances of executable selected."""

        for process in psutil.process_iter(attrs=["pid", "name"]):
            if process.info["name"] == executable_name:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except psutil.TimeoutExpired:
                    process.kill()

    def check_shutdown_signal(self):
        """Check if the shutdown signal file indicates a closure."""
        # try:
        #     with Database_Connection(config_database()) as conn:
        #         cur = conn.cursor()
        #         cur.execute("SELECT action FROM logging.erp_control WHERE id = TRUE")
        #         row = cur.fetchone()

        #     if row and row[0].lower() == "shutdown":
        #         self.close_all_instances("EIPSA-ERP.exe")
        #         self.close()
        #     else:
        #         print('Estado normal (OK), aplicación sigue funcionando')
        # except (Exception, psycopg2.DatabaseError) as error:
        #     MessageHelper.show_message(f"Ocurrió un error en la base de datos:\n{error}", "critical")

        try:
            if os.path.exists(shutdown_file):
                with open(shutdown_file, 'r') as f:
                    content = f.read().strip()  # Read the content of the file
                    if content != "OK":
                        print("Recibiendo comando de cierre...")
                        self.close_all_instances("EIPSA-ERP.exe")
                        self.close_all_instances("EIPSA-ERP_CLOUD.exe")
                        self.close()
                        sys.exit()  # Exit the application
        except Exception as e:
            print(f"Error al verificar el archivo de señal: {e}")

def start_app():
    """
    Entry point for the application. Initializes the Qt application and displays the login window if the configuration
    file exists. If the configuration file is not found, displays an error message.

    - Checks if the configuration file `database.ini` exists in the specified directory.
    - If the file exists, creates and shows the login window.
    - If the file does not exist, displays an error message indicating that the configuration file is missing.

    Exits the application when the login window is closed or if the configuration file is missing.
    """
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    if INI_FILE_PATH.exists():
        ini_file = INI_FILE_PATH
    else:
        ini_file = Path(r"C:\Program Files\ERP EIPSA\database.ini")

    if ini_file.exists():
        log_window=MainWindow()
        ui=Ui_Login_Window()
        ui.setupUi(log_window)
        log_window.show()
        sys.exit(app.exec())

    else:
        MessageHelper.show_message("Archivo de configuración no encontrado.\nPonte en contacto con el administrador", "critical")