# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import Signal, pyqtSlot


class ZoomSelector(QComboBox):
    """
    A combo box for selecting and setting zoom levels, with options for predefined and custom zoom percentages.
    Emits signals for zoom mode and zoom factor changes.
    """
    zoom_mode_changed = Signal(QPdfView.ZoomMode)
    zoom_factor_changed = Signal(float)

    def __init__(self, parent):
        """
        Initializes the ZoomSelector, sets up editable mode, adds predefined zoom options, and connects signals.
        """
        super().__init__(parent)
        self.setEditable(True)

        self.addItem("Fit Width")
        self.addItem("Fit Page")
        self.addItem("12%")
        self.addItem("25%")
        self.addItem("33%")
        self.addItem("50%")
        self.addItem("66%")
        self.addItem("75%")
        self.addItem("100%")
        self.addItem("125%")
        self.addItem("150%")
        self.addItem("200%")
        self.addItem("400%")

        self.currentTextChanged.connect(self.on_current_text_changed)
        self.lineEdit().editingFinished.connect(self._editing_finished)

    @pyqtSlot(float)
    def set_zoom_factor(self, zoomFactor):
        """
        Sets the zoom factor and updates the combo box selection to the corresponding percentage.
        """
        percent = int(zoomFactor * 100)
        self.setCurrentText(f"{percent}%")

    @pyqtSlot()
    def reset(self):
        """
        Resets the combo box to the default zoom level (100%).
        """
        self.setCurrentIndex(1)  # 100%

    @pyqtSlot(str)
    def on_current_text_changed(self, text):
        """
        Emits zoom mode and factor signals based on the current text selection.
        """
        if text == "Fit Width":
            self.zoom_mode_changed.emit(QPdfView.ZoomMode.FitToWidth)
        elif text == "Fit Page":
            self.zoom_mode_changed.emit(QPdfView.ZoomMode.FitInView)
        elif text.endswith("%"):
            factor = 1.0
            zoom_level = int(text[:-1])
            factor = zoom_level / 100.0
            self.zoom_mode_changed.emit(QPdfView.ZoomMode.Custom)
            self.zoom_factor_changed.emit(factor)

    @pyqtSlot()
    def _editing_finished(self):
        """
        Handles the event when editing in the combo box line edit is finished.
        """
        self.on_current_text_changed(self.lineEdit().text())
