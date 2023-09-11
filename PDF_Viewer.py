import os
import math
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6.QtCore import QPointF, QEvent, Qt, QUrl, pyqtSlot
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtGui import QIcon, QPixmap
from PDFViewer_ZoomSelector import ZoomSelector
from PDFViewer_ui import Ui_MainWindow
from tkinter.filedialog import asksaveasfilename
from pdf_styles import pruebas

ZOOM_MULTIPLIER = math.sqrt(2.0)

class PDF_Viewer(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.m_zoomSelector = ZoomSelector(self)
        self.m_pageSelector = QLineEdit(self)
        self.m_document = QPdfDocument(self)
        self.m_fileDialog = None
        self.temp_file_path = None

        icon = QIcon()
        icon.addPixmap(QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Recursos/Iconos/icon.ico"), QIcon.Mode.Normal, QIcon.State.Off)
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
        if doc_location.isLocalFile():
            self.m_document.load(doc_location.toLocalFile())
            document_title = self.m_document.metaData(QPdfDocument.MetaDataField.Title)
            self.setWindowTitle(document_title if document_title else "PDF Viewer")
        else:
            message = f"{doc_location} is not a valid local file"
            print(message, file=sys.stderr)
            QMessageBox.critical(self, "Failed to open", message)

    def closeEvent(self, event):
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
        page = int(self.m_pageSelector.text())
        nav = self.ui.pdfView.pageNavigator()
        nav.jump(page - 1, QPointF(), nav.currentZoom())

        self.set_main_window_focus()


    @pyqtSlot()
    def on_actionQuit_triggered(self):
        self.close()


    @pyqtSlot()
    def on_actionZoom_In_triggered(self):
        factor = self.ui.pdfView.zoomFactor() * ZOOM_MULTIPLIER
        self.ui.pdfView.setZoomFactor(factor)


    @pyqtSlot()
    def on_actionZoom_Out_triggered(self):
        factor = self.ui.pdfView.zoomFactor() / ZOOM_MULTIPLIER
        self.ui.pdfView.setZoomFactor(factor)


    @pyqtSlot()
    def on_actionPrevious_Page_triggered(self):
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
        cont_checked = self.ui.actionContinuous.isChecked()
        mode = QPdfView.PageMode.MultiPage if cont_checked else QPdfView.PageMode.SinglePage
        self.ui.pdfView.setPageMode(mode)


    @pyqtSlot()
    def on_actionBack_triggered(self):
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
        output_path = asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")], title="Guardar Pedido Proveedor")

        if output_path:
            pdf.output(output_path)

            dlg = QMessageBox()
            new_icon = QIcon()
            new_icon.addPixmap(QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Recursos/Iconos/icon.ico"), QIcon.Mode.Normal, QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Imprimir pedido")
            dlg.setText("PDF generado con éxito")
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.exec()
            del dlg,new_icon

    @pyqtSlot()
    def on_actionPrint_triggered(self):
        try:
            os.startfile(r'\\nas01\DATOS\Comunes\EIPSA-ERP\Recursos\pdfviewer\temp\temp.pdf','print')
            PRINTER_DEFAULTS = {"DesiredAccess":win32print.PRINTER_ALL_ACCESS}  
            pHandle = win32print.OpenPrinter('300LN1', PRINTER_DEFAULTS)  
            properties = win32print.GetPrinter(pHandle, 2)
            pDevModeObj = properties["pDevMode"]
            pDevModeObj.Orientation = 2  
            win32print.SetPrinter(pHandle,2,properties,0)
            win32print.ClosePrinter(pHandle)
        except Exception as e:
            print(f"Error al imprimir el PDF: {e}")


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Right:
            self.on_actionNext_Page_triggered()
        elif event.key() == Qt.Key.Key_Left:
            self.on_actionPrevious_Page_triggered()
        super().keyPressEvent(event)


    def set_main_window_focus(self):
        self.setFocus()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            self.set_main_window_focus()
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDF_Viewer()

    pdf = pruebas()
    pdf.set_auto_page_break(auto=True, margin=1)
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    for i in range(1, 100):
        pdf.cell(20, 1, f"This is line {i} of the PDF")
        pdf.ln(1)

    pdf_buffer = pdf.output()

    temp_file_path = os.path.join("//nas01/DATOS/Comunes/EIPSA-ERP/Recursos/pdfviewer/temp", "temp.pdf")

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(pdf_buffer)
        window.temp_file_path = temp_file.name

    pdf.close()

    window.open(QUrl.fromLocalFile(temp_file_path))

    window.showMaximized()

    window.setFocus()
    sys.exit(app.exec())
