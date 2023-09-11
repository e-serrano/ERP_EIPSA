# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import pyqtSignal, pyqtSlot


class ZoomSelector(QComboBox):

    zoom_mode_changed = pyqtSignal(QPdfView.ZoomMode)
    zoom_factor_changed = pyqtSignal(float)

    def __init__(self, parent):
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
        percent = int(zoomFactor * 100)
        self.setCurrentText(f"{percent}%")

    @pyqtSlot()
    def reset(self):
        self.setCurrentIndex(1)  # 100%

    @pyqtSlot(str)
    def on_current_text_changed(self, text):
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
        self.on_current_text_changed(self.lineEdit().text())
