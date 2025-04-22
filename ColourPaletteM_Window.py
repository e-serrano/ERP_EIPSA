import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import os

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"

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
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignLeft

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
            state_column_index = index.sibling(index.row(), 1) # Index for column to check text
            value_check = str(state_column_index.data()).upper() # Text for checking
            painter.setPen(QtGui.QColor("black"))

            if any(item in value_check for item in ['316H', '316TI']):
                start_color = QtGui.QColor(92, 197, 229)  # Blue
                end_color = QtGui.QColor(92, 197, 229)  # Blue
                border_color = QtGui.QColor(255, 0, 0)  # Red

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, '634',)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)
                painter.drawText(horizontalPosition, verticalPosition, '634')

            elif '304H' in value_check:
                start_color = QtGui.QColor(255, 255, 0)  # Yellow
                end_color = QtGui.QColor(255, 255, 0)  # Yellow
                border_color = QtGui.QColor(255, 0, 0)  # Red

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, '627',)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)
                painter.drawText(horizontalPosition, verticalPosition, '627')

            elif '321H' in value_check:
                start_color = QtGui.QColor(251, 131, 179)  # Pink
                end_color = QtGui.QColor(251, 131, 179)  # Pink
                border_color = QtGui.QColor(255, 0, 0)  # Red

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, '696',)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)
                painter.drawText(horizontalPosition, verticalPosition, '696')

            elif '310H' in value_check:
                start_color = QtGui.QColor(255, 255, 0)  # Yellow
                end_color = QtGui.QColor(24, 146, 97)  # Dark Green
                border_color = QtGui.QColor(255, 0, 0)  # Red

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '627')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '665')

            elif '347H' in value_check:
                start_color = QtGui.QColor(146, 208, 80)  # Light Green
                end_color = QtGui.QColor(251, 131, 179)  # Pink
                border_color = QtGui.QColor(255, 0, 0)  # Red

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '641')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '696')

            elif '317H' in value_check:
                start_color = QtGui.QColor(92, 197, 229)  # Blue
                end_color = QtGui.QColor(251, 131, 179)  # Pink
                border_color = QtGui.QColor(255, 0, 0)  # Red

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '634')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '696')

            elif 'F9' in value_check:
                start_color = QtGui.QColor(255, 157, 59)  # Orange
                end_color = QtGui.QColor(251, 131, 179)  # Pink

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '672')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '696')

            elif 'A707' in value_check:
                start_color = QtGui.QColor(255, 157, 59)  # Orange
                end_color = QtGui.QColor(24, 146, 97)  # Dark Green

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '672')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '665')

            elif '316' in value_check:
                start_color = QtGui.QColor(92, 197, 229)  # Blue
                end_color = QtGui.QColor(92, 197, 229)  # Blue

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, '634',)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)
                painter.drawText(horizontalPosition, verticalPosition, '634')

            elif '304' in value_check:
                start_color = QtGui.QColor(255, 255, 0)  # Yellow
                end_color = QtGui.QColor(255, 255, 0)  # Yellow

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, '627',)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)
                painter.drawText(horizontalPosition, verticalPosition, '627')

            elif '446' in value_check:
                start_color = QtGui.QColor(255, 255, 0)  # Yellow
                end_color = QtGui.QColor(92, 197, 229)  # Blue

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '627')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '634')

            elif 'MONEL' in value_check:
                start_color = QtGui.QColor(160, 120, 182)  # Purple
                end_color = QtGui.QColor(160, 120, 182)  # Purple

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, '743',)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)
                painter.drawText(horizontalPosition, verticalPosition, '743')

            elif 'HASTELLOY' in value_check:
                start_color = QtGui.QColor(146, 208, 80)  # Light Green
                end_color = QtGui.QColor(255, 255, 0)  # Yellow

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '641')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '627')

            elif '321' in value_check:
                start_color = QtGui.QColor(251, 131, 179)  # Pink
                end_color = QtGui.QColor(251, 131, 179)  # Pink

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, '696',)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)
                painter.drawText(horizontalPosition, verticalPosition, '696')

            elif 'TANTALO' in value_check:
                start_color = QtGui.QColor(255, 87, 87)  # Red
                end_color = QtGui.QColor(92, 197, 229)  # Blue
                border_color = QtGui.QColor(24, 146, 97)  # Dark Green

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.setPen(QtGui.QPen(border_color, 3))
                painter.drawRect(option.rect)
                painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '658')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '634')

            elif 'F11' in value_check:
                start_color = QtGui.QColor(255, 157, 59)  # Orange
                end_color = QtGui.QColor(255, 255, 0)  # Yellow

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '672')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '627')

            elif 'F22' in value_check:
                start_color = QtGui.QColor(255, 157, 59)  # Orange
                end_color = QtGui.QColor(146, 208, 80)  # Light Green

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '672')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '641')

            elif 'LF2' in value_check:
                start_color = QtGui.QColor(255, 157, 59)  # Orange
                end_color = QtGui.QColor(255, 157, 59)  # Orange

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, '672',)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)
                painter.drawText(horizontalPosition, verticalPosition, '672')

            elif '310' in value_check:
                start_color = QtGui.QColor(255, 255, 0)  # Yellow
                end_color = QtGui.QColor(24, 146, 97)  # Dark Green

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '627')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '665')

            elif 'ALLOY 20' in value_check:
                start_color = QtGui.QColor(160, 120, 182)  # Purple
                end_color = QtGui.QColor(92, 197, 229)  # Blue

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '743')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '634')

            elif 'INCONEL 600' in value_check:
                start_color = QtGui.QColor(146, 208, 80)  # Light Green
                end_color = QtGui.QColor(146, 208, 80)  # Light Green

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, '641',)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)
                painter.drawText(horizontalPosition, verticalPosition, '641')

            elif 'N08904' in value_check:
                start_color = QtGui.QColor(160, 120, 182)  # Purple
                end_color = QtGui.QColor(255, 157, 59)  # Orange

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '743')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '672')

            elif any(item in value_check for item in ['F60', '32205', 'SAF 2205']):
                start_color = QtGui.QColor(160, 120, 182)  # Purple
                end_color = QtGui.QColor(146, 208, 80)  # Light Green

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '743')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '641')

            elif any(item in value_check for item in ['F44', '31254']):
                start_color = QtGui.QColor(160, 120, 182)  # Purple
                end_color = QtGui.QColor(251, 131, 179)  # Pink

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '743')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '696')

            elif '825' in value_check:
                start_color = QtGui.QColor(24, 146, 97)  # Dark Green
                end_color = QtGui.QColor(255, 87, 87)  # Red

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '665')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '658')

            elif '601' in value_check:
                start_color = QtGui.QColor(146, 208, 80)  # Light Green
                end_color = QtGui.QColor(92, 197, 229)  # Blue

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '641')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '634')

            elif '625' in value_check:
                start_color = QtGui.QColor(146, 208, 80)  # Light Green
                end_color = QtGui.QColor(255, 87, 87)  # Red

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '641')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '658')

            elif '800' in value_check:
                start_color = QtGui.QColor(24, 146, 97)  # Dark Green
                end_color = QtGui.QColor(24, 146, 97)  # Dark Green

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, '665',)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)
                painter.drawText(horizontalPosition, verticalPosition, '665')

            elif any(item in value_check for item in ['F53', '32750', 'SAF 2507']):
                start_color = QtGui.QColor(160, 120, 182)  # Purple
                end_color = QtGui.QColor(24, 146, 97)  # Dark Green

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '743')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '665')

            elif any(item in value_check for item in ['F51', '31803']):
                start_color = QtGui.QColor(160, 120, 182)  # Purple
                end_color = QtGui.QColor(255, 255, 0)  # Yellow

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '743')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '627')

            elif any(item in value_check for item in ['F55', '32760']):
                start_color = QtGui.QColor(160, 120, 182)  # Purple
                end_color = QtGui.QColor(255, 87, 87)  # Red

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '743')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '658')

            elif any(item in value_check for item in ['C70610', 'CUNI 90-10', 'C70690']):
                start_color = QtGui.QColor(255, 157, 59)  # Orange
                end_color = QtGui.QColor(255, 87, 87)  # Red

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '672')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '658')

            elif '347' in value_check:
                start_color = QtGui.QColor(251, 131, 179)  # Pink
                end_color = QtGui.QColor(146, 208, 80)  # Light Green

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '696')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '641')

            elif '317' in value_check:
                start_color = QtGui.QColor(92, 197, 229)  # Blue
                end_color = QtGui.QColor(251, 131, 179)  # Pink

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '634')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '696')

            elif 'TITANIO' in value_check:
                start_color = QtGui.QColor(255, 255, 0)  # Yellow
                end_color = QtGui.QColor(251, 131, 179)  # Pink

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '627')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '696')

            elif 'ALLOY 699XA' in value_check:
                start_color = QtGui.QColor(146, 208, 80)  # Light Green
                end_color = QtGui.QColor(24, 146, 97)  # Dark Green

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '641')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '665')

            elif any(item in value_check for item in ['HR160', '50CR-50NI']):
                start_color = QtGui.QColor(24, 146, 97)  # Dark Green
                end_color = QtGui.QColor(251, 131, 179)  # Pink

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '665')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '696')

            elif any(item in value_check for item in ['F5', '5CR-1/2MO']):
                start_color = QtGui.QColor(255, 157, 59)  # Orange
                end_color = QtGui.QColor(92, 197, 229)  # Blue

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                painter.drawText(rect_top, QtCore.Qt.AlignmentFlag.AlignCenter, '672')
                painter.drawText(rect_bottom, QtCore.Qt.AlignmentFlag.AlignCenter, '634')

            elif 'ALUMINIO' in value_check:
                start_color = QtGui.QColor(255, 87, 87)  # Red
                end_color = QtGui.QColor(255, 87, 87)  # Red

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

                textRect = painter.boundingRect(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2), QtCore.Qt.TextFlag.TextDontClip | QtCore.Qt.AlignmentFlag.AlignCenter, '658',)
                verticalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).y() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).height() + textRect.height() + 8) / 2)
                horizontalPosition = int(option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).x() + (option.rect.adjusted(0, 0, 0, -option.rect.height() // 2).width() - textRect.width()) / 2)
                painter.drawText(horizontalPosition, verticalPosition, '658')

            else:
                start_color = QtGui.QColor(255, 255, 255)  # White
                end_color = QtGui.QColor(255, 255, 255)  # White

                rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                painter.fillRect(rect_top, start_color)
                painter.fillRect(rect_bottom, end_color)

            if "STELLITE" in value_check:
                    border_color = QtGui.QColor(0, 0, 0)  # Black

                    rect_top = option.rect.adjusted(0, 0, 0, -option.rect.height() // 2)
                    rect_bottom = option.rect.adjusted(0, option.rect.height() // 2, 0, 0)

                    painter.setPen(QtGui.QPen(border_color, 3))
                    painter.drawRect(option.rect)
                    painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 0.01))


class Ui_PaletteColourM_Window(object):
    """
    Main window class for the PaletteColourM. Manages the UI and interactions with the database.
    """
    def setupUi(self, PaletteColourM_Window):
        """
        Sets up the user interface components for the main application window.

        Args:
            PaletteColourM_Window (QtWidgets.QMainWindow): The main window object to set up.
        """
        PaletteColourM_Window.setWindowTitle("Paleta de colores")
        PaletteColourM_Window.setObjectName("PaletteColourM_Window")
        PaletteColourM_Window.resize(790, 595)
        PaletteColourM_Window.setMinimumSize(QtCore.QSize(790, 595))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        PaletteColourM_Window.setWindowIcon(icon)

        self.central_widget = QtWidgets.QWidget()
        PaletteColourM_Window.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Colores', 'Material'])

        self.layout.addWidget(self.table)

        self.data_list = ["MONEL", "", "N08904", "", "F60 / S32205 / SAF 2205", "", "F53 / S32750 / SAF 2507", "",
                        "F55 / S32760", "", "F51 / S31803", "", "ALLOY 20", "", "F44 / S31254", "",
                        "A 105", "", "LF2", "", "F22", "", "A707", "","F11", "", "F5 / 5Cr-1/2Mo", "","F9 / F91", "",
                        "INCONEL 600", "", "ALLOY 699XA", "", "625", "", "HASTELLOY", "", "601", "",
                        "800", "", "825", "", "STELLITE", "", "HR160 / 50Cr-50Ni", "",
                        "304", "", "304H", "", "310", "", "310H", "", "446", "",
                        "316", "", "316H", "", "316Ti", "", "317", "", "317H", "",
                        "321", "", "321H", "", "347", "", "347H", "",
                        "TITANIO", "", "TANTALO", "", "C70610 / C70690 / CuNi 90-10", "", "ALUMINIO"]

        self.populate_table()

    def populate_table(self):
        """Fills the table with data, applies alignment, and adjusts column widths."""
        num_rows = len(self.data_list)
        self.table.setRowCount(num_rows)

        for row, data in enumerate(self.data_list):
            item = QtWidgets.QTableWidgetItem("")
            self.table.setItem(row, 0, item)

            item = QtWidgets.QTableWidgetItem(data)
            self.table.setItem(row, 1, item)

        self.table.setItemDelegate(AlignDelegate(self.table))
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_PaletteColourM_Window()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())


