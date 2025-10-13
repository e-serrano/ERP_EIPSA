import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import os

basedir = r"\\ERP-EIPSA-DATOS\DATOS\Comunes\EIPSA-ERP"

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    """
    A custom item delegate for aligning cell content in a QTableView or QTableWidget to the center.

    Inherits from:
        QtWidgets.QStyledItemDelegate: Provides custom rendering and editing for table items.

    """
    def initStyleOption(self, option, index):
        """
        Initializes the style option for the item, setting its display alignment to center.

        Args:
            option (QtWidgets.QStyleOptionViewItem): The style option to initialize.
            index (QtCore.QModelIndex): The model index of the item.
        """
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter

    def paint(self, painter, option, index):
        """
        Custom paint method to render the cell content and apply background colors 
        based on specific conditions for a column's value.

        Args:
            painter (QPainter): The painter used to render the cell.
            option (QStyleOptionViewItem): The style options for the cell.
            index (QModelIndex): The index of the cell being painted.
        """
        super().paint(painter, option, index)

        if index.column() == 0:  # Column to paint
            original_text = str(index.data()) # Index for column to check text
            painter.setPen(QtGui.QColor("black"))

            if 'B7-NORMALIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(0, 0, 0)

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'B7-FLUOROPOLIMERIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(0, 0, 0)
                border_color = QtGui.QColor(0, 0, 255)  # Blue

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'B7M-NORMALIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(0, 0, 0)
                border_color = QtGui.QColor(0, 0, 0)  # Black

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'B7M-FLUOROPOLIMERIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(0, 0, 0)
                border_color = QtGui.QColor(0, 255, 0)  # Green

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'B8-NORMALIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(255, 0, 0) # Red

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'B8-FLUOROPOLIMERIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(255, 0, 0) # Red
                border_color = QtGui.QColor(0, 0, 255)  # Blue

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'B8M-NORMALIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(255, 0, 0) # Red
                border_color = QtGui.QColor(0, 0, 0)  # Black

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'B8M-FLUOROPOLIMERIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(255, 0, 0) # Red
                border_color = QtGui.QColor(0, 255, 0)  # Green

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'B16-NORMALIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(226, 226, 0) # Yellow

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'B16-FLUOROPOLIMERIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(226, 226, 0) # Yellow
                border_color = QtGui.QColor(0, 0, 255)  # Blue

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'B16M-NORMALIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(226, 226, 0) # Yellow
                border_color = QtGui.QColor(0, 0, 0)  # Black

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'B16M-FLUOROPOLIMERIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(226, 226, 0) # Yellow
                border_color = QtGui.QColor(0, 255, 0)  # Green

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'L7-NORMALIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(255, 128, 0) # Orange

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'L7-FLUOROPOLIMERIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(255, 128, 0) # Orange
                border_color = QtGui.QColor(0, 0, 255)  # Blue

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'L7M-NORMALIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(255, 128, 0) # Orange
                border_color = QtGui.QColor(0, 0, 0)  # Black

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'L7M-FLUOROPOLIMERIZADO' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(255, 128, 0) # Orange
                border_color = QtGui.QColor(0, 255, 0)  # Green

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            elif 'TORNILLERÍA GALVANIZADA' in original_text:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(170, 0, 255) # Purple

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)

            else:
                bg_color = QtGui.QColor(255, 255, 255)  # White
                painter.fillRect(option.rect, bg_color)

                text_color = QtGui.QColor(0, 0, 0) # Black

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, original_text,)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)

                painter.setPen(QtGui.QPen(text_color))
                painter.drawText(horizontalPosition, verticalPosition, original_text)


class Ui_PaletteColourT_Window(object):
    """
    Main window class for the PaletteColourT. Manages the UI and interactions with the database.
    """
    def setupUi(self, PaletteColourT_Window):
        """
        Sets up the user interface components for the main application window.

        Args:
            PaletteColourT_Window (QtWidgets.QMainWindow): The main window object to set up.
        """
        PaletteColourT_Window.setWindowTitle("Paleta de colores")
        PaletteColourT_Window.setObjectName("PaletteColourT_Window")
        PaletteColourT_Window.resize(790, 595)
        PaletteColourT_Window.setMinimumSize(QtCore.QSize(790, 595))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        PaletteColourT_Window.setWindowIcon(icon)

        self.central_widget = QtWidgets.QWidget()
        PaletteColourT_Window.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Material', 'Formato'])

        self.layout.addWidget(self.table)

        self.data_list = ["B7-NORMALIZADO", "", "B7-FLUOROPOLIMERIZADO", "", "B7M-NORMALIZADO", "", "B7M-FLUOROPOLIMERIZADO", "",
                        "B8-NORMALIZADO", "", "B8-FLUOROPOLIMERIZADO", "", "B8M-NORMALIZADO", "", "B8M-FLUOROPOLIMERIZADO", "",
                        "B16-NORMALIZADO", "", "B16-FLUOROPOLIMERIZADO", "", "B16M-NORMALIZADO", "", "B16M-FLUOROPOLIMERIZADO", "",
                        "L7-NORMALIZADO", "", "L7-FLUOROPOLIMERIZADO", "", "L7M-NORMALIZADO", "", "L7M-FLUOROPOLIMERIZADO", "",
                        "TORNILLERÍA GALVANIZADA",]
        
        self.chr_list = ["Letra en negro", "", "Letra en negro + línea azul", "", "Letra en negro + línea negra", "", "Letra en negro + línea verde", "",
                        "Letra en rojo", "", "Letra en rojo + línea azul", "", "Letra en rojo + línea negra", "", "Letra en rojo + línea verde", "",
                        "Letra en amarillo", "", "Letra en amarillo + línea azul", "", "Letra en amarillo + línea negra", "", "Letra en amarillo + línea verde", "",
                        "Letra en naranja", "", "Letra en naranja + línea azul", "", "Letra en naranja + línea negra", "", "Letra en naranja + línea verde", "",
                        "Letra en morado",]

        self.populate_table()

    def populate_table(self):
        """Fills the table with data, applies alignment, and adjusts column widths."""
        num_rows = len(self.data_list)
        self.table.setRowCount(num_rows)

        for row, data in enumerate(self.data_list):
            item = QtWidgets.QTableWidgetItem(data)
            self.table.setItem(row, 0, item)

        for row, data in enumerate(self.chr_list):
            item = QtWidgets.QTableWidgetItem(data)
            self.table.setItem(row, 1, item)

        self.table.setItemDelegate(AlignDelegate(self.table))
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)




# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = QtWidgets.QMainWindow()
#     ui = Ui_PaletteColourT_Window()
#     ui.setupUi(window)
#     window.show()
#     sys.exit(app.exec())


