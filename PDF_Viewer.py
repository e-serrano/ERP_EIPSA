import math
import sys
import tempfile
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QLineEdit)
from PySide6.QtCore import QPoint, QEvent, QUrl, Slot, Qt

from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import QIcon, QPixmap
from PDFViewer_ZoomSelector import ZoomSelector
from PDFViewer_ui import Ui_MainWindow

from pdf_styles import pruebas


ZOOM_MULTIPLIER = math.sqrt(2.0)

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.m_zoomSelector = ZoomSelector(self)
        self.m_pageSelector = QLineEdit(self)
        self.m_document = QPdfDocument(self)
        self.m_fileDialog = None

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

        self.m_zoomSelector.zoom_mode_changed.connect(self.ui.pdfView.setZoomMode)
        self.m_zoomSelector.zoom_factor_changed.connect(self.ui.pdfView.setZoomFactor)
        self.m_zoomSelector.reset()

        self.ui.pdfView.setDocument(self.m_document)

        self.ui.pdfView.zoomFactorChanged.connect(self.m_zoomSelector.set_zoom_factor)

        self.ui.pdfView.setFocusPolicy(Qt.TabFocus)

        self.m_pageSelector.returnPressed.connect(self.page_selected)

        self.installEventFilter(self)

    @Slot(QUrl)
    def open(self, doc_location):
        if doc_location.isLocalFile():
            self.m_document.load(doc_location.toLocalFile())
            document_title = self.m_document.metaData(QPdfDocument.MetaDataField.Title)
            self.setWindowTitle(document_title if document_title else "PDF Viewer")

        else:
            message = f"{doc_location} is not a valid local file"
            print(message, file=sys.stderr)
            QMessageBox.critical(self, "Failed to open", message)


    @Slot(int)
    def page_selected(self):
        page = int(self.m_pageSelector.text())
        nav = self.ui.pdfView.pageNavigator()
        nav.jump(page - 1, QPoint(), nav.currentZoom())

        self.set_main_window_focus()


    @Slot()
    def on_actionQuit_triggered(self):
        self.close()


    @Slot()
    def on_actionZoom_In_triggered(self):
        factor = self.ui.pdfView.zoomFactor() * ZOOM_MULTIPLIER
        self.ui.pdfView.setZoomFactor(factor)


    @Slot()
    def on_actionZoom_Out_triggered(self):
        factor = self.ui.pdfView.zoomFactor() / ZOOM_MULTIPLIER
        self.ui.pdfView.setZoomFactor(factor)


    @Slot()
    def on_actionPrevious_Page_triggered(self):
        nav = self.ui.pdfView.pageNavigator()
        current_page = nav.currentPage()

        if current_page - 1 >= 0:
            nav.jump(current_page - 1, QPoint(), nav.currentZoom())
            self.ui.actionBack.setEnabled(True)
            self.ui.actionForward.setEnabled(True)

        current_page = nav.currentPage()
        if current_page == 0:
            self.ui.actionBack.setEnabled(False)

        self.m_pageSelector.setText(str(current_page + 1))


    @Slot()
    def on_actionNext_Page_triggered(self):
        nav = self.ui.pdfView.pageNavigator()
        current_page = nav.currentPage()
        total_pages = self.m_document.pageCount()

        if current_page + 1 < total_pages:
            nav.jump(current_page + 1, QPoint(), nav.currentZoom())
            self.ui.actionBack.setEnabled(True)
            self.ui.actionForward.setEnabled(True)

        current_page = nav.currentPage()
        if current_page + 1 == total_pages:
            self.ui.actionForward.setEnabled(False)

        self.m_pageSelector.setText(str(current_page + 1))


    @Slot()
    def on_actionContinuous_triggered(self):
        cont_checked = self.ui.actionContinuous.isChecked()
        mode = QPdfView.PageMode.MultiPage if cont_checked else QPdfView.PageMode.SinglePage
        self.ui.pdfView.setPageMode(mode)


    @Slot()
    def on_actionBack_triggered(self):
        nav = self.ui.pdfView.pageNavigator()
        current_page = nav.currentPage()

        if current_page - 1 >= 0:
            nav.jump(current_page - 1, QPoint(), nav.currentZoom())
            self.ui.actionBack.setEnabled(True)
            self.ui.actionForward.setEnabled(True)

        current_page = nav.currentPage()
        if current_page == 0:
            self.ui.actionBack.setEnabled(False)

        self.m_pageSelector.setText(str(current_page + 1))


    @Slot()
    def on_actionForward_triggered(self):
        nav = self.ui.pdfView.pageNavigator()
        current_page = nav.currentPage()
        total_pages = self.m_document.pageCount()

        if current_page + 1 < total_pages:
            nav.jump(current_page + 1, QPoint(), nav.currentZoom())
            self.ui.actionBack.setEnabled(True)
            self.ui.actionForward.setEnabled(True)

        current_page = nav.currentPage()
        if current_page + 1 == total_pages:
            self.ui.actionForward.setEnabled(False)

        self.m_pageSelector.setText(str(current_page + 1))


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Right:
            self.on_actionNext_Page_triggered()
        elif event.key() == Qt.Key.Key_Left:
            self.on_actionPrevious_Page_triggered()
        super().keyPressEvent(event)


    def set_main_window_focus(self):
        self.setFocus()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            self.set_main_window_focus()
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    pdf = pruebas()
    pdf.set_auto_page_break(auto=True, margin=1)
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    for i in range(1, 100):
        pdf.cell(20, 1, f"This is line {i} of the PDF")
        pdf.ln(1)

    pdf_buffer = pdf.output()

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_buffer)
        temp_file_path = temp_file.name

    window.open(QUrl.fromLocalFile(temp_file_path))

    window.showMaximized()

    window.setFocus()
    sys.exit(app.exec())



