import os
import math
import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit
from PyQt6.QtCore import QPointF, QEvent, Qt, QUrl, pyqtSlot
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtGui import QIcon, QPixmap
from PDFViewer_ZoomSelector import ZoomSelector
from PDFViewer_ui import Ui_MainWindow
from tkinter.filedialog import asksaveasfilename
import shutil
import win32api
import psutil
import time

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"

ZOOM_MULTIPLIER = math.sqrt(2.0)

class PDF_Viewer(QMainWindow):
    """
    A PDF viewer application with functionalities for zooming, navigating pages, printing, and saving PDF documents.
    """
    def __init__(self, parent=None):
        """
        Initializes the PDF viewer, sets up UI components, and connects signals and slots.
        """
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.m_zoomSelector = ZoomSelector(self)
        self.m_pageSelector = QLineEdit(self)
        self.m_document = QPdfDocument(self)
        self.m_fileDialog = None
        self.temp_file_path = None

        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QIcon.Mode.Normal, QIcon.State.Off)
        self.setWindowIcon(icon)

        self.ui.setupUi(self)

        self.m_zoomSelector.setMaximumWidth(150)
        self.ui.mainToolBar.insertWidget(self.ui.actionZoom_In, self.m_zoomSelector)
        self.m_pageSelector.setFixedWidth(50)

        self.ui.mainToolBar.insertWidget(self.ui.actionForward, self.m_pageSelector)
        self.m_pageSelector.setText(str(1))
        self.ui.actionForward.setEnabled(True)

        self.ui.actionPrint.setEnabled(True)
        self.ui.actionSave.setEnabled(True)

        self.m_zoomSelector.zoom_mode_changed.connect(self.ui.pdfView.setZoomMode)
        self.m_zoomSelector.zoom_factor_changed.connect(self.ui.pdfView.setZoomFactor)
        self.m_zoomSelector.reset()

        self.ui.pdfView.setDocument(self.m_document)

        self.ui.pdfView.zoomFactorChanged.connect(self.m_zoomSelector.set_zoom_factor)

        self.ui.pdfView.setFocusPolicy(Qt.FocusPolicy.TabFocus)

        self.m_pageSelector.returnPressed.connect(self.page_selected)

        self.installEventFilter(self)


    @pyqtSlot(QUrl)
    def open(self, doc_location):
        """
        Opens and loads a PDF document from the given local file URL.

        Args:
            doc_location (QUrl): The URL of the local file to open.
        """
        self.temp_file_path = doc_location

        if doc_location.isLocalFile():
            self.m_document.load(doc_location.toLocalFile())
            document_title = self.m_document.metaData(QPdfDocument.MetaDataField.Title)
            self.setWindowTitle(document_title if document_title else "PDF Viewer")
        else:
            message = f"{doc_location} is not a valid local file"
            print(message, file=sys.stderr)
            QMessageBox.critical(self, "Failed to open", message)

    def closeEvent(self, event):
        """
        Handles the close event of the main window, including optional cleanup.
        """
        # Eliminar el archivo temporal cuando se cierra la ventana
        pass
        # if self.temp_file_path:
        #     try:
        #         # os.remove(self.temp_file_path)
        #         print(f"Archivo temporal eliminado: {self.temp_file_path}")
        #     except Exception as e:
        #         print(f"Error al eliminar el archivo temporal: {e}")

        # event.accept()


    def page_selected(self):
        """
        Navigates to the page specified in the page selector.
        """
        page = int(self.m_pageSelector.text())
        nav = self.ui.pdfView.pageNavigator()
        nav.jump(page - 1, QPointF(), nav.currentZoom())

        self.set_main_window_focus()


    @pyqtSlot()
    def on_actionQuit_triggered(self):
        """
        Closes the application.
        """
        self.close()


    @pyqtSlot()
    def on_actionZoom_In_triggered(self):
        """
        Zooms in on the PDF view.
        """
        factor = self.ui.pdfView.zoomFactor() * ZOOM_MULTIPLIER
        self.ui.pdfView.setZoomFactor(factor)


    @pyqtSlot()
    def on_actionZoom_Out_triggered(self):
        """
        Zooms out on the PDF view.
        """
        factor = self.ui.pdfView.zoomFactor() / ZOOM_MULTIPLIER
        self.ui.pdfView.setZoomFactor(factor)


    @pyqtSlot()
    def on_actionPrevious_Page_triggered(self):
        """
        Navigates to the previous page in the PDF.
        """
        nav = self.ui.pdfView.pageNavigator()
        current_page = nav.currentPage()

        if current_page - 1 >= 0:
            nav.jump(current_page - 1, QPointF(), nav.currentZoom())
            self.ui.actionBack.setEnabled(True)
            self.ui.actionForward.setEnabled(True)

        current_page = nav.currentPage()
        if current_page == 0:
            self.ui.actionBack.setEnabled(False)

        self.m_pageSelector.setText(str(current_page + 1))


    @pyqtSlot()
    def on_actionNext_Page_triggered(self):
        """
        Navigates to the next page in the PDF.
        """
        nav = self.ui.pdfView.pageNavigator()
        current_page = nav.currentPage()
        total_pages = self.m_document.pageCount()

        if current_page + 1 < total_pages:
            nav.jump(current_page + 1, QPointF(), nav.currentZoom())
            self.ui.actionBack.setEnabled(True)
            self.ui.actionForward.setEnabled(True)

        current_page = nav.currentPage()
        if current_page + 1 == total_pages:
            self.ui.actionForward.setEnabled(False)

        self.m_pageSelector.setText(str(current_page + 1))


    @pyqtSlot()
    def on_actionContinuous_triggered(self):
        """
        Toggles between continuous and single-page view modes.
        """
        cont_checked = self.ui.actionContinuous.isChecked()
        mode = QPdfView.PageMode.MultiPage if cont_checked else QPdfView.PageMode.SinglePage
        self.ui.pdfView.setPageMode(mode)


    @pyqtSlot()
    def on_actionBack_triggered(self):
        """
        Navigates to the previous page or view.
        """
        nav = self.ui.pdfView.pageNavigator()
        current_page = nav.currentPage()

        if current_page - 1 >= 0:
            nav.jump(current_page - 1, QPointF(), nav.currentZoom())
            self.ui.actionBack.setEnabled(True)
            self.ui.actionForward.setEnabled(True)

        current_page = nav.currentPage()
        if current_page == 0:
            self.ui.actionBack.setEnabled(False)

        self.m_pageSelector.setText(str(current_page + 1))


    @pyqtSlot()
    def on_actionForward_triggered(self):
        """
        Navigates to the next page or view.
        """
        nav = self.ui.pdfView.pageNavigator()
        current_page = nav.currentPage()
        total_pages = self.m_document.pageCount()

        if current_page + 1 < total_pages:
            nav.jump(current_page + 1, QPointF(), nav.currentZoom())
            self.ui.actionBack.setEnabled(True)
            self.ui.actionForward.setEnabled(True)

        current_page = nav.currentPage()
        if current_page + 1 == total_pages:
            self.ui.actionForward.setEnabled(False)

        self.m_pageSelector.setText(str(current_page + 1))

    @pyqtSlot()
    def on_actionSave_triggered(self):
        """
        Saves the current PDF to a specified location.
        """
        temp_file_path = self.temp_file_path.toLocalFile().replace('/', '\\')
        output_path = asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")], title="Guardar PDF")

        if output_path:
            shutil.copyfile(temp_file_path, output_path)

            dlg = QMessageBox()
            new_icon = QIcon()
            new_icon.addPixmap(QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QIcon.Mode.Normal, QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Imprimir pedido")
            dlg.setText("PDF generado con éxito")
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.exec()
            del dlg,new_icon

            # os.remove(temp_file_path)

    @pyqtSlot()
    def on_actionPrint_triggered(self):
        """
        Prints the current PDF.
        """
        print(self.temp_file_path)
        temp_file_path = self.temp_file_path.toLocalFile().replace('/', '\\')

        try:
            win32api.ShellExecute(0, "print", temp_file_path, None, ".", 0) # Printing the temp file
            # os.remove(temp_file_path) # Deleting the temp file
        except Exception as e:
            dlg = QMessageBox()
            new_icon = QIcon()
            new_icon.addPixmap(QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QIcon.Mode.Normal, QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Imprimir pedido")
            print(e)
            dlg.setText("Ha ocurrido un error. No se pudo imprimir el PDF")
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.exec()
            del dlg,new_icon

        self.close_adobe_reader()

    def close_adobe_reader(self):
        """
        Closes any running Adobe Reader processes.
        """
        time.sleep(5)
        for process in psutil.process_iter(['pid', 'name']):
            try:
                process_name = process.info['name'].lower()
                if 'adobe' in process_name or 'acrobat' in process_name:
                    # print(f"Cerrando {process.info['name']} con PID {process.info['pid']}")
                    process.terminate()  # Termina el proceso
                    process.wait()  # Espera a que el proceso termine
                    # print(f"{process.info['name']} ha sido cerrado.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        self.close()


    def keyPressEvent(self, event):
        """
        Handles custom key events for page navigation.

        Args:
            event (QtGui.QKeyEvent): The key event to handle.
        """
        if event.key() == Qt.Key.Key_Right:
            self.on_actionNext_Page_triggered()
        elif event.key() == Qt.Key.Key_Left:
            self.on_actionPrevious_Page_triggered()
        super().keyPressEvent(event)


    def set_main_window_focus(self):
        """
        Sets focus to the main window.
        """
        self.setFocus()

    def eventFilter(self, obj, event):
        """
        Filters events to ensure focus is set to the main window on mouse clicks.

        Args:
            obj (QObject): The object that received the event.
            event (QEvent): The event to filter.

        Returns:
            bool: True if the event is handled; otherwise, False.
        """
        if event.type() == QEvent.Type.MouseButtonPress:
            self.set_main_window_focus()
        return super().eventFilter(obj, event)
