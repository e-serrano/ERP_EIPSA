from PySide6 import QtCore, QtGui, QtWidgets
from PySide6 import QtSql
from PySide6.QtCore import Qt
from utils.Database_Manager import Create_DBconnection
from datetime import *
import re
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QMimeData, QDate
from PySide6.QtGui import QKeySequence
import sys
from config.config_functions import config_database, get_path
import psycopg2
import pandas as pd
from utils.Database_Manager import Database_Connection


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

class ColorDelegate(QtWidgets.QItemDelegate):
    """
    A custom item delegate for applying background colors to cells in a QTableView or QTableWidget.

    Inherits from:
        QtWidgets.QItemDelegate: Provides custom rendering for table items.
    """
    def __init__(self, parent=None):
        """
        Initializes the ColorDelegate, setting up the color mapping from the database.

        Args:
            parent (QtWidgets.QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.colors_dict = self.get_colors_from_database()

    def get_colors_from_database(self):
        """
        Retrieves color information from the database and builds a dictionary mapping orders to their colors.

        Returns:
            dict: A dictionary where the keys are order numbers and the values are tuples of QColor objects for two types of background colors.
        """
        colors_dict = {}

        try:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    commands_colors = "SELECT num_order, bg_color, bg_color_assembly  FROM orders"
                    cur.execute(commands_colors)
                    results = cur.fetchall()

            for result in results:
                order, color_w, color_a = result
                if color_w is not None:
                    # Extraemos los valores RGB de la cadena hexadecimal
                    r, g, b = re.findall(r'\w\w', color_w)
                    color_w = QtGui.QColor(int(r, 16), int(g, 16), int(b, 16))
                else: 
                    color_w = QtGui.QColor(255, 255, 255, 0)
                
                if color_a is not None:
                    # Extraemos los valores RGB de la cadena hexadecimal
                    r, g, b = re.findall(r'\w\w', color_a)
                    color_a = QtGui.QColor(int(r, 16), int(g, 16), int(b, 16))
                else: 
                    color_a = QtGui.QColor(255, 255, 255, 0)

                colors_dict[order] = (color_w, color_a)

        except (Exception, psycopg2.DatabaseError) as error:
            # Handle the error appropriately
            pass

        return colors_dict

    def paint(self, painter, option, index: QtCore.QModelIndex):
        """
        Paints the background color of the item based on its column and value.

        Args:
            painter (QtGui.QPainter): The painter used for painting.
            option (QtWidgets.QStyleOptionViewItem): The style option for the item.
            index (QtCore.QModelIndex): The model index of the item.
        """
        value = index.model().data(index, role=Qt.ItemDataRole.DisplayRole)
        background_color = QtGui.QColor(255, 255, 255, 0)

        if index.column() == 16:
            if isinstance(value, int):
                if value <= 50 and value >= 1:
                    background_color = QtGui.QColor(240, 208, 88) #Yellow
                elif value == 99:
                    background_color = QtGui.QColor(24, 146, 97) #Dark Green
                elif value < 99  and value > 50:
                    background_color = QtGui.QColor(0, 255, 0) #Green
                elif value == 100:
                    background_color = QtGui.QColor(0, 102, 204) #Blue
                else:
                    background_color = QtGui.QColor(255, 255, 255, 0) #White

        elif index.column() == 4:
            if isinstance(value, (date, datetime)):
                if value <= QtCore.QDate.currentDate():
                    background_color = QtGui.QColor(255, 0, 0) #Red
                elif (value.toPython() - QtCore.QDate.currentDate().toPython()).days <= 15:
                    background_color = QtGui.QColor(237, 125, 49) #Orange
                elif (value.toPython() - QtCore.QDate.currentDate().toPython()).days <= 30:
                    background_color = QtGui.QColor(255, 125, 255) #Pink

        elif index.column() == 14:
            state_column_index = index.sibling(index.row(), 0)
            order = str(state_column_index.data())

            if order in self.colors_dict:
                background_color = self.colors_dict[order][0]
            else:
                background_color = QtGui.QColor(255, 255, 255, 0)

        elif index.column() == 19:
            state_column_index = index.sibling(index.row(), 0)
            order = str(state_column_index.data())

            if order in self.colors_dict:
                background_color = self.colors_dict[order][1]
            else:
                background_color = QtGui.QColor(255, 255, 255, 0)

        painter.fillRect(option.rect, background_color)
        option.displayAlignment = QtCore.Qt.AlignmentFlag.AlignCenter

        super().paint(painter, option, index)

class CustomProxyModel_P(QtCore.QSortFilterProxyModel):
    """
    A custom proxy model that filters table rows based on expressions set for specific columns.

    Attributes:
        _filters (dict): A dictionary to store filter expressions for columns.
        header_names (dict): A dictionary to store header names for the table.

    Properties:
        filters: Getter for the current filter dictionary.

    """
    def __init__(self, parent=None):
        """
        Get the current filter expressions applied to columns.

        Returns:
            dict: Dictionary of column filters.
        """
        super().__init__(parent)
        self._filters = dict()
        self.header_names = {}

    @property
    def filters(self):
        """
        Get the current filter expressions applied to columns.

        Returns:
            dict: Dictionary of column filters.
        """
        return self._filters

    def setFilter(self, list_expresions, column, action_name=None):
        """
        Updates filters for a specified column based on provided expressions and action name.

        Args:
            list_expresions (list): List of filter expressions to be applied.
            column (int): Column index to which the filters are applied.
            action_name (str, optional): Action to determine how filters are updated. Defaults to None.
        """
        for expresion in list_expresions:
            if expresion or expresion == '':
                if column in self.filters:
                    if action_name or action_name == '':
                        self.filters[column].remove(expresion)
                    else:
                        self.filters[column].append(expresion)
                else:
                    self.filters[column] = [expresion]
            elif column in self.filters:
                if action_name or action_name == '':
                    self.filters[column].remove(expresion)
                    if not self.filters[column]:
                        del self.filters[column]
                else:
                    del self.filters[column]
        self.invalidateFilter()


    def filterAcceptsRow(self, source_row, source_parent):
        """
        Check if a row passes the filter criteria based on the column filters.

        Args:
            source_row (int): The row number in the source model.
            source_parent (QModelIndex): The parent index of the row.

        Returns:
            bool: True if the row meets the filter criteria, False otherwise.
        """
        for column, expresions in self.filters.items():
            text = self.sourceModel().index(source_row, column, source_parent).data()

            if isinstance(text, QtCore.QDate): #Check if filters are QDate. If True, convert to text
                text = text.toString("yyyy-MM-dd")

            for expresion in expresions:
                if expresion == '':  # If expression is empty, match empty cells
                    if text == '':
                        break

                elif re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', str(expresion)):
                    expresion = QtCore.QDate.fromString(expresion, "dd/MM/yyyy")
                    expresion = expresion.toString("yyyy-MM-dd")
                    regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                    if regex.match(str(text)).hasMatch():
                        break

                else:
                    regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                    if regex.match(str(text)).hasMatch():
                        break

            else:
                return False
        return True

class EditableTableModel_P(QtSql.QSqlTableModel):
    """
    A custom SQL table model that supports editable columns, headers, and special flagging behavior based on user permissions.

    Signals:
        updateFailed (str): Signal emitted when an update to the model fails.
    """
    updateFailed = QtCore.Signal(str)

    def __init__(self, parent=None, column_range=None, database=None):
        """
        Initialize the model with user permissions and optional database and column range.

        Args:
            username (str): The username for permission-based actions.
            parent (QObject, optional): Parent object for the model. Defaults to None.
            column_range (list, optional): A list specifying the range of columns. Defaults to None.
        """
        super().__init__(parent, database)
        self.column_range = column_range

    def setAllColumnHeaders(self, headers):
        """
        Set headers for all columns in the model.

        Args:
            headers (list): A list of header names.
        """
        for column, header in enumerate(headers):
            self.setHeaderData(column, Qt.Orientation.Horizontal, header, Qt.ItemDataRole.DisplayRole)

    def setIndividualColumnHeader(self, column, header):
        """
        Set the header for a specific column.

        Args:
            column (int): The column index.
            header (str): The header name.
        """
        self.setHeaderData(column, Qt.Orientation.Horizontal, header, Qt.ItemDataRole.DisplayRole)

    def setIconColumnHeader(self, column, icon):
        """
        Set an icon in the header for a specific column.

        Args:
            column (int): The column index.
            icon (QIcon): The icon to display in the header.
        """
        self.setHeaderData(column, QtCore.Qt.Orientation.Horizontal, icon, Qt.ItemDataRole.DecorationRole)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        """
        Retrieve the header data for a specific section of the model.

        Args:
            section (int): The section index (column or row).
            orientation (Qt.Orientation): The orientation (horizontal or vertical).
            role (Qt.ItemDataRole, optional): The role for the header data. Defaults to DisplayRole.

        Returns:
            QVariant: The header data for the specified section.
        """
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return super().headerData(section, orientation, role)
        return super().headerData(section, orientation, role)

    def flags(self, index):
        """
        Get the item flags for a given index, controlling editability and selection based on user permissions.

        Args:
            index (QModelIndex): The index of the item.

        Returns:
            Qt.ItemFlags: The flags for the specified item.
        """
        flags = super().flags(index)
        if index.column() in [0,4,14,25]:
            flags &= ~Qt.ItemFlag.ItemIsEditable
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        else:
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def getColumnHeaders(self, visible_columns):
        """
        Retrieve the headers for the specified visible columns.

        Args:
            visible_columns (list): List of column indices that are visible.

        Returns:
            list: A list of column headers for the visible columns.
        """
        column_headers = [self.headerData(col, Qt.Orientation.Horizontal) for col in visible_columns]
        return column_headers

class CustomProxyModel_PA(QtCore.QSortFilterProxyModel):
    """
    A custom proxy model that filters table rows based on expressions set for specific columns.

    Attributes:
        _filters (dict): A dictionary to store filter expressions for columns.
        header_names (dict): A dictionary to store header names for the table.

    Properties:
        filters: Getter for the current filter dictionary.

    """
    def __init__(self, parent=None):
        """
        Get the current filter expressions applied to columns.

        Returns:
            dict: Dictionary of column filters.
        """
        super().__init__(parent)
        self._filters = dict()
        self.header_names = {}

    @property
    def filters(self):
        """
        Get the current filter expressions applied to columns.

        Returns:
            dict: Dictionary of column filters.
        """
        return self._filters

    def setFilter(self, list_expresions, column, action_name=None):
        """
        Updates filters for a specified column based on provided expressions and action name.

        Args:
            list_expresions (list): List of filter expressions to be applied.
            column (int): Column index to which the filters are applied.
            action_name (str, optional): Action to determine how filters are updated. Defaults to None.
        """
        for expresion in list_expresions:
            if expresion or expresion == '':
                if column in self.filters:
                    if action_name or action_name == '':
                        self.filters[column].remove(expresion)
                    else:
                        self.filters[column].append(expresion)
                else:
                    self.filters[column] = [expresion]
            elif column in self.filters:
                if action_name or action_name == '':
                    self.filters[column].remove(expresion)
                    if not self.filters[column]:
                        del self.filters[column]
                else:
                    del self.filters[column]
        self.invalidateFilter()


    def filterAcceptsRow(self, source_row, source_parent):
        """
        Check if a row passes the filter criteria based on the column filters.

        Args:
            source_row (int): The row number in the source model.
            source_parent (QModelIndex): The parent index of the row.

        Returns:
            bool: True if the row meets the filter criteria, False otherwise.
        """
        for column, expresions in self.filters.items():
            text = self.sourceModel().index(source_row, column, source_parent).data()

            if isinstance(text, QtCore.QDate): #Check if filters are QDate. If True, convert to text
                text = text.toString("yyyy-MM-dd")

            for expresion in expresions:
                if expresion == '':  # If expression is empty, match empty cells
                    if text == '':
                        break

                elif re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', str(expresion)):
                    expresion = QtCore.QDate.fromString(expresion, "dd/MM/yyyy")
                    expresion = expresion.toString("yyyy-MM-dd")
                    regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                    if regex.match(str(text)).hasMatch():
                        break

                else:
                    regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                    if regex.match(str(text)).hasMatch():
                        break

            else:
                return False
        return True

class EditableTableModel_PA(QtSql.QSqlTableModel):
    """
    A custom SQL table model that supports editable columns, headers, and special flagging behavior based on user permissions.

    Signals:
        updateFailed (str): Signal emitted when an update to the model fails.
    """
    updateFailed = QtCore.Signal(str)

    def __init__(self, parent=None, column_range=None, database=None):
        """
        Initialize the model with user permissions and optional database and column range.

        Args:
            username (str): The username for permission-based actions.
            parent (QObject, optional): Parent object for the model. Defaults to None.
            column_range (list, optional): A list specifying the range of columns. Defaults to None.
        """
        super().__init__(parent, database)
        self.column_range = column_range

    def setAllColumnHeaders(self, headers):
        """
        Set headers for all columns in the model.

        Args:
            headers (list): A list of header names.
        """
        for column, header in enumerate(headers):
            self.setHeaderData(column, Qt.Orientation.Horizontal, header, Qt.ItemDataRole.DisplayRole)

    def setIndividualColumnHeader(self, column, header):
        """
        Set the header for a specific column.

        Args:
            column (int): The column index.
            header (str): The header name.
        """
        self.setHeaderData(column, Qt.Orientation.Horizontal, header, Qt.ItemDataRole.DisplayRole)

    def setIconColumnHeader(self, column, icon):
        """
        Set an icon in the header for a specific column.

        Args:
            column (int): The column index.
            icon (QIcon): The icon to display in the header.
        """
        self.setHeaderData(column, QtCore.Qt.Orientation.Horizontal, icon, Qt.ItemDataRole.DecorationRole)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        """
        Retrieve the header data for a specific section of the model.

        Args:
            section (int): The section index (column or row).
            orientation (Qt.Orientation): The orientation (horizontal or vertical).
            role (Qt.ItemDataRole, optional): The role for the header data. Defaults to DisplayRole.

        Returns:
            QVariant: The header data for the specified section.
        """
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return super().headerData(section, orientation, role)
        return super().headerData(section, orientation, role)

    def flags(self, index):
        """
        Get the item flags for a given index, controlling editability and selection based on user permissions.

        Args:
            index (QModelIndex): The index of the item.

        Returns:
            Qt.ItemFlags: The flags for the specified item.
        """
        flags = super().flags(index)
        if index.column() in [0,4,14,25]:
            flags &= ~Qt.ItemFlag.ItemIsEditable
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        else:
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

class CustomProxyModel_AL(QtCore.QSortFilterProxyModel):
    """
    A custom proxy model that filters table rows based on expressions set for specific columns.

    Attributes:
        _filters (dict): A dictionary to store filter expressions for columns.
        header_names (dict): A dictionary to store header names for the table.

    Properties:
        filters: Getter for the current filter dictionary.

    """
    def __init__(self, parent=None):
        """
        Get the current filter expressions applied to columns.

        Returns:
            dict: Dictionary of column filters.
        """
        super().__init__(parent)
        self._filters = dict()
        self.header_names = {}

    @property
    def filters(self):
        """
        Get the current filter expressions applied to columns.

        Returns:
            dict: Dictionary of column filters.
        """
        return self._filters

    def setFilter(self, list_expresions, column, action_name=None):
        """
        Updates filters for a specified column based on provided expressions and action name.

        Args:
            list_expresions (list): List of filter expressions to be applied.
            column (int): Column index to which the filters are applied.
            action_name (str, optional): Action to determine how filters are updated. Defaults to None.
        """
        for expresion in list_expresions:
            if expresion or expresion == '':
                if column in self.filters:
                    if action_name or action_name == '':
                        self.filters[column].remove(expresion)
                    else:
                        self.filters[column].append(expresion)
                else:
                    self.filters[column] = [expresion]
            elif column in self.filters:
                if action_name or action_name == '':
                    self.filters[column].remove(expresion)
                    if not self.filters[column]:
                        del self.filters[column]
                else:
                    del self.filters[column]
        self.invalidateFilter()


    def filterAcceptsRow(self, source_row, source_parent):
        """
        Check if a row passes the filter criteria based on the column filters.

        Args:
            source_row (int): The row number in the source model.
            source_parent (QModelIndex): The parent index of the row.

        Returns:
            bool: True if the row meets the filter criteria, False otherwise.
        """
        for column, expresions in self.filters.items():
            text = self.sourceModel().index(source_row, column, source_parent).data()

            if isinstance(text, QtCore.QDate): #Check if filters are QDate. If True, convert to text
                text = text.toString("yyyy-MM-dd")

            for expresion in expresions:
                if expresion == '':  # If expression is empty, match empty cells
                    if text == '':
                        break

                elif re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', str(expresion)):
                    expresion = QtCore.QDate.fromString(expresion, "dd/MM/yyyy")
                    expresion = expresion.toString("yyyy-MM-dd")
                    regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                    if regex.match(str(text)).hasMatch():
                        break

                else:
                    regex = QtCore.QRegularExpression(f".*{re.escape(str(expresion))}.*", QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
                    if regex.match(str(text)).hasMatch():
                        break
            else:
                return False
        return True

class EditableTableModel_AL(QtSql.QSqlTableModel):
    """
    A custom SQL table model that supports editable columns, headers, and special flagging behavior based on user permissions.

    Signals:
        updateFailed (str): Signal emitted when an update to the model fails.
    """
    updateFailed = QtCore.Signal(str)

    def __init__(self, parent=None, column_range=None, database=None):
        """
        Initialize the model with user permissions and optional database and column range.

        Args:
            username (str): The username for permission-based actions.
            parent (QObject, optional): Parent object for the model. Defaults to None.
            column_range (list, optional): A list specifying the range of columns. Defaults to None.
        """
        super().__init__(parent, database)
        self.column_range = column_range

    def setAllColumnHeaders(self, headers):
        """
        Set headers for all columns in the model.

        Args:
            headers (list): A list of header names.
        """
        for column, header in enumerate(headers):
            self.setHeaderData(column, Qt.Orientation.Horizontal, header, Qt.ItemDataRole.DisplayRole)

    def setIndividualColumnHeader(self, column, header):
        """
        Set the header for a specific column.

        Args:
            column (int): The column index.
            header (str): The header name.
        """
        self.setHeaderData(column, Qt.Orientation.Horizontal, header, Qt.ItemDataRole.DisplayRole)

    def setIconColumnHeader(self, column, icon):
        """
        Set an icon in the header for a specific column.

        Args:
            column (int): The column index.
            icon (QIcon): The icon to display in the header.
        """
        self.setHeaderData(column, QtCore.Qt.Orientation.Horizontal, icon, Qt.ItemDataRole.DecorationRole)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        """
        Retrieve the header data for a specific section of the model.

        Args:
            section (int): The section index (column or row).
            orientation (Qt.Orientation): The orientation (horizontal or vertical).
            role (Qt.ItemDataRole, optional): The role for the header data. Defaults to DisplayRole.

        Returns:
            QVariant: The header data for the specified section.
        """
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return super().headerData(section, orientation, role)
        return super().headerData(section, orientation, role)

    def flags(self, index):
        """
        Get the item flags for a given index, controlling editability and selection based on user permissions.

        Args:
            index (QModelIndex): The index of the item.

        Returns:
            Qt.ItemFlags: The flags for the specified item.
        """
        flags = super().flags(index)
        if index.column() in [0,1]:
            flags &= ~Qt.ItemFlag.ItemIsEditable
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
        else:
            return flags | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def getColumnHeaders(self, visible_columns):
        """
        Retrieve the headers for the specified visible columns.

        Args:
            visible_columns (list): List of column indices that are visible.

        Returns:
            list: A list of column headers for the visible columns.
        """
        column_headers = [self.headerData(col, Qt.Orientation.Horizontal) for col in visible_columns]
        return column_headers


class Ui_Assembly_Window(QtWidgets.QMainWindow):
    """
    A main window for managing Assembly-related data, including models and proxies for tables.

    Inherits from:
        QtWidgets.QMainWindow: A top-level window that provides a main application window.
    
    Attributes:
        model_P (EditableTableModel_P): The model for table P.
        proxy_P (CustomProxyModel_P): The proxy model for table P.
        model_PA (EditableTableModel_PA): The model for table PA.
        proxy_PA (CustomProxyModel_PA): The proxy model for table PA.
        checkbox_states_P (dict): A dictionary tracking checkbox states for table P.
        dict_valuesuniques_P (dict): A dictionary of unique values for table P.
        dict_ordersort_P (dict): A dictionary for sorting orders in table P.
        action_checkbox_map_P (dict): A mapping of actions to checkboxes for table P.
        checkbox_filters_P (dict): A dictionary of filters applied to checkboxes for table P.
        checkbox_states_PA (dict): A dictionary tracking checkbox states for table PA.
        dict_valuesuniques_PA (dict): A dictionary of unique values for table PA.
        dict_ordersort_PA (dict): A dictionary for sorting orders in table PA.
        action_checkbox_map_PA (dict): A mapping of actions to checkboxes for table PA.
        checkbox_filters_PA (dict): A dictionary of filters applied to checkboxes for table PA.
        db (object): The database connection object.
        username (str): The username of the currently logged-in user.
    """
    def __init__(self, db, username):
        """
        Initializes the Ui_Assembly_Window, setting up models, proxies, and internal state.

        Args:
            db (object): The database connection object.
            username (str): The username of the currently logged-in user.
        """
        super().__init__()
        self.model_P = EditableTableModel_P(database=db)
        self.proxy_P = CustomProxyModel_P()
        self.model_PA = EditableTableModel_PA(database=db)
        self.proxy_PA = CustomProxyModel_PA()
        self.model_AL = EditableTableModel_AL(database=db)
        self.proxy_AL = CustomProxyModel_AL()
        self.checkbox_states_P = {}
        self.dict_valuesuniques_P = {}
        self.dict_ordersort_P = {}
        self.action_checkbox_map_P = {}
        self.checkbox_filters_P = {}
        self.checkbox_states_PA = {}
        self.dict_valuesuniques_PA = {}
        self.dict_ordersort_PA = {}
        self.action_checkbox_map_PA = {}
        self.checkbox_filters_PA = {}
        self.checkbox_states_AL = {}
        self.dict_valuesuniques_AL = {}
        self.dict_ordersort_AL = {}
        self.action_checkbox_map_AL = {}
        self.checkbox_filters_AL = {}
        self.db = db
        self.username = username
        self.open_windows = {}
        self.model_P.dataChanged.connect(self.saveChanges)
        self.model_PA.dataChanged.connect(self.saveChanges)
        self.model_AL.dataChanged.connect(self.saveChanges)
        self.setupUi(self)

    def closeEvent(self, event):
        """
        Handles the close event to clean up resources.

        Args:
            event (QtGui.QCloseEvent): The close event.
        """
        try:
            if self.model_P:
                self.model_P.clear()
            if self.model_PA:
                self.model_PA.clear()
            self.closeConnection()
        except Exception as e:
            print("Error during close event:", e)

    def closeConnection(self):
        """
        Closes the database connection and cleans up resources.
        """
        try:
            self.tableAssembly_P.setModel(None)
            del self.model_P
            self.tableAssembly_PA.setModel(None)
            del self.model_PA
            if self.db:
                self.db.close()
                del self.db
                if QtSql.QSqlDatabase.contains("Assembly_connection"):
                    QtSql.QSqlDatabase.removeDatabase("Assembly_connection")
        except Exception as e:
            print("Error closing connection:", e)


    def setupUi(self, Assembly_Window):
        """
        Sets up the user interface components for the main application window.

        Args:
            Assembly_Window (QtWidgets.QMainWindow): The main window object to set up.
        """
        self.id_list = []
        data_list = []
        Assembly_Window.setObjectName("Assembly_Window")
        Assembly_Window.resize(400, 561)
        Assembly_Window.setMinimumSize(QtCore.QSize(600, 575))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Assembly_Window.setWindowIcon(icon)
        Assembly_Window.setStyleSheet(
"QPushButton {\n"
"background-color: #33bdef;\n"
"  border: 1px solid transparent;\n"
"  border-radius: 3px;\n"
"  color: #fff;\n"
"  font-family: -apple-system,system-ui,\"Segoe UI\",\"Liberation Sans\",sans-serif;\n"
"  font-size: 15px;\n"
"  font-weight: 800;\n"
"  line-height: 1.15385;\n"
"  margin: 0;\n"
"  outline: none;\n"
"  padding: 8px .8em;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  vertical-align: baseline;\n"
"  white-space: nowrap;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #019ad2;\n"
"    border-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(1, 140, 190);\n"
"    border-color: rgb(255, 255, 255);\n"
"}\n"
"QMenu {\n"
"background-color: white;\n"
"color: black;\n"
"}\n"
"QMenu::item {\n"
"background-color: white;\n"
"color: black;\n"
"}\n"
"QMenu::item:selected {background-color: rgb(3, 174, 236);}")
        self.centralwidget = QtWidgets.QWidget(parent=Assembly_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.hcab=QtWidgets.QHBoxLayout()
        self.hcab.setObjectName("hcab")
        self.toolExpExcel = QtWidgets.QToolButton(self.frame)
        self.toolExpExcel.setObjectName("ExpExcel_Button")
        self.toolExpExcel.setToolTip("Exportar a Excel")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "Excel.png"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolExpExcel.setIcon(icon)
        self.toolExpExcel.setIconSize(QtCore.QSize(25, 25))
        self.hcab.addWidget(self.toolExpExcel)
        self.hcabspacer=QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hcab.addItem(self.hcabspacer)
        self.gridLayout_2.addLayout(self.hcab, 0, 0, 1, 1)
        self.tabwidget = QtWidgets.QTabWidget(self.frame)
        self.tabwidget.setObjectName("tabwidget")
        self.tab_P = QtWidgets.QWidget()
        self.tab_P.setObjectName("tab_P")
        self.tabwidget.addTab(self.tab_P, "P-")
        self.tab_PA = QtWidgets.QWidget()
        self.tab_PA.setObjectName("tab_PA")
        self.tabwidget.addTab(self.tab_PA, "PA-")
        self.tab_AL = QtWidgets.QWidget()
        self.tab_AL.setObjectName("tab_AL")
        self.tabwidget.addTab(self.tab_AL, "AL-")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_P)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_PA)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_AL)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.hLayout_P = QtWidgets.QHBoxLayout()
        self.hLayout_P.setObjectName("hLayout_P")
        self.Button_ShowRef_P = QtWidgets.QPushButton(parent=self.frame)
        self.Button_ShowRef_P.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_ShowRef_P.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_ShowRef_P.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_ShowRef_P.setObjectName("Button_ShowRef_P")
        self.hLayout_P.addWidget(self.Button_ShowRef_P)
        self.Button_All_P = QtWidgets.QPushButton(parent=self.frame)
        self.Button_All_P.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_All_P.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_All_P.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_All_P.setObjectName("Button_All_P")
        self.hLayout_P.addWidget(self.Button_All_P)
        self.Button_BG_P = QtWidgets.QPushButton(parent=self.frame)
        self.Button_BG_P.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_BG_P.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_BG_P.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_BG_P.setObjectName("Button_BG_P")
        self.hLayout_P.addWidget(self.Button_BG_P)
        self.gridLayout_3.addLayout(self.hLayout_P, 1, 0, 1, 1)
        self.tableAssembly_P=QtWidgets.QTableView(parent=self.frame)
        self.model_P = EditableTableModel_P(database=self.db)
        self.tableAssembly_P.setObjectName("tableAssembly_P")
        self.gridLayout_3.addWidget(self.tableAssembly_P, 2, 0, 1, 1)
        self.hLayout_PA = QtWidgets.QHBoxLayout()
        self.hLayout_PA.setObjectName("hLayout_PA")
        self.Button_ShowRef_PA = QtWidgets.QPushButton(parent=self.frame)
        self.Button_ShowRef_PA.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_ShowRef_PA.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_ShowRef_PA.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_ShowRef_PA.setObjectName("Button_ShowRef_PA")
        self.hLayout_PA.addWidget(self.Button_ShowRef_PA)
        self.Button_All_PA = QtWidgets.QPushButton(parent=self.frame)
        self.Button_All_PA.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_All_PA.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_All_PA.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_All_PA.setObjectName("Button_All_PA")
        self.hLayout_PA.addWidget(self.Button_All_PA)
        self.Button_BG_PA = QtWidgets.QPushButton(parent=self.frame)
        self.Button_BG_PA.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_BG_PA.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_BG_PA.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_BG_PA.setObjectName("Button_BG_PA")
        self.hLayout_PA.addWidget(self.Button_BG_PA)
        self.gridLayout_4.addLayout(self.hLayout_PA, 1, 0, 1, 1)
        self.tableAssembly_PA=QtWidgets.QTableView(parent=self.frame)
        self.model_PA = EditableTableModel_PA(database=self.db)
        self.tableAssembly_PA.setObjectName("tableAssembly_PA")
        self.gridLayout_4.addWidget(self.tableAssembly_PA, 2, 0, 1, 1)

        self.hLayout_AL = QtWidgets.QHBoxLayout()
        self.hLayout_AL.setObjectName("hLayout_AL")
        self.Button_All_AL = QtWidgets.QPushButton(parent=self.frame)
        self.Button_All_AL.setMinimumSize(QtCore.QSize(150, 35))
        self.Button_All_AL.setMaximumSize(QtCore.QSize(150, 35))
        self.Button_All_AL.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.Button_All_AL.setObjectName("Button_All_AL")
        self.hLayout_AL.addWidget(self.Button_All_AL)
        self.gridLayout_5.addLayout(self.hLayout_AL, 1, 0, 1, 1)
        self.tableAssembly_AL=QtWidgets.QTableView(parent=self.frame)
        self.model_AL = EditableTableModel_AL(database=self.db)
        self.tableAssembly_AL.setObjectName("tableAssembly_AL")
        self.gridLayout_5.addWidget(self.tableAssembly_AL, 2, 0, 1, 1)

        self.gridLayout_2.addWidget(self.tabwidget, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        Assembly_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Assembly_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 22))
        self.menubar.setObjectName("menubar")
        Assembly_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Assembly_Window)
        self.statusbar.setObjectName("statusbar")
        Assembly_Window.setStatusBar(self.statusbar)
        self.tableAssembly_P.setSortingEnabled(True)
        self.tableAssembly_P.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        self.tableAssembly_PA.setSortingEnabled(True)
        self.tableAssembly_PA.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        self.tableAssembly_AL.setSortingEnabled(True)
        self.tableAssembly_AL.horizontalHeader().setStyleSheet("QHeaderView::section {background-color: #33bdef; border: 1px solid black;}")
        # Assembly_Window.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.retranslateUi(Assembly_Window)
        QtCore.QMetaObject.connectSlotsByName(Assembly_Window)

        self.query_data()
        self.toolExpExcel.clicked.connect(self.exporttoexcel)

        description_action_p = QtGui.QAction("Descripción a Albarán", self)
        description_action_p.triggered.connect(lambda: self.insert_description(self.tableAssembly_P))

        self.context_menu_row = QtWidgets.QMenu(self)
        self.context_menu_row.addAction(description_action_p)

        self.tableAssembly_P.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.tableAssembly_P.addActions([description_action_p])

        description_action_pa = QtGui.QAction("Descripción a Albarán", self)
        description_action_pa.triggered.connect(lambda: self.insert_description(self.tableAssembly_PA))

        self.context_menu_row = QtWidgets.QMenu(self)
        self.context_menu_row.addAction(description_action_pa)

        self.tableAssembly_PA.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.tableAssembly_PA.addActions([description_action_pa])

# Function to translate and updates the text of various UI elements
    def retranslateUi(self, Assembly_Window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        Assembly_Window.setWindowTitle(_translate("EditTags_Window", "Montaje"))
        self.Button_All_P.setText(_translate("EditTags_Window", "Ver Todos"))
        self.Button_All_PA.setText(_translate("EditTags_Window", "Ver Todos"))
        self.Button_All_AL.setText(_translate("EditTags_Window", "Ver Todos"))
        self.Button_BG_P.setText(_translate("EditTags_Window", "Pintar Fondo"))
        self.Button_BG_PA.setText(_translate("EditTags_Window", "Pintar Fondo"))
        self.Button_ShowRef_P.setText(_translate("EditTags_Window", "Ver Nº Ref"))
        self.Button_ShowRef_PA.setText(_translate("EditTags_Window", "Ver Nº Ref"))

# Function to load orders on tables
    def query_data(self):
        """
        Queries the database for orders not delivered, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model_P.setTable("public.orders")
        self.model_P.setFilter("num_order LIKE 'P-%' AND num_order NOT LIKE '%R%' AND (porc_deliveries <> 100 OR porc_deliveries IS NULL)")
        self.model_P.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model_P.select()
        self.proxy_P.setSourceModel(self.model_P)
        self.tableAssembly_P.setModel(self.proxy_P)

        self.model_PA.setTable("public.orders")
        self.model_PA.setFilter("num_order LIKE 'PA-%' AND num_order NOT LIKE '%R%' AND (porc_deliveries <> 100 OR porc_deliveries IS NULL)")
        self.model_PA.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model_PA.select()
        self.proxy_PA.setSourceModel(self.model_PA)
        self.tableAssembly_PA.setModel(self.proxy_PA)

        self.model_AL.setTable("public.orders_warehouse")
        # self.model_AL.setFilter("num_order LIKE 'PA-%' AND num_order NOT LIKE '%R%' AND (porc_deliveries <> 100 OR porc_deliveries IS NULL)")
        self.model_AL.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model_AL.select()
        self.proxy_AL.setSourceModel(self.model_AL)
        self.tableAssembly_AL.setModel(self.proxy_AL)

    # Getting the unique values for each column of the model
        for column in range(self.model_P.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_P:
                self.checkbox_states_P[column] = {}
                self.checkbox_states_P[column]['Seleccionar todo'] = True
                for row in range(self.model_P.rowCount()):
                    value = self.model_P.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_P[column][str(value)] = True
                self.dict_valuesuniques_P[column] = list_valuesUnique

    # Getting the unique values for each column of the model
        for column in range(self.model_PA.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_PA:
                self.checkbox_states_PA[column] = {}
                self.checkbox_states_PA[column]['Seleccionar todo'] = True
                for row in range(self.model_PA.rowCount()):
                    value = self.model_PA.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_PA[column][str(value)] = True
                self.dict_valuesuniques_PA[column] = list_valuesUnique

    # Getting the unique values for each column of the model
        for column in range(self.model_AL.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_AL:
                self.checkbox_states_AL[column] = {}
                self.checkbox_states_AL[column]['Seleccionar todo'] = True
                for row in range(self.model_AL.rowCount()):
                    value = self.model_AL.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_AL[column][str(value)] = True
                self.dict_valuesuniques_AL[column] = list_valuesUnique

        for i in range(1,4):
            self.tableAssembly_P.hideColumn(i)
            self.tableAssembly_PA.hideColumn(i)
        for i in range(5,16):
            self.tableAssembly_P.hideColumn(i)
            self.tableAssembly_PA.hideColumn(i)
        for i in range(22,23):
            self.tableAssembly_P.hideColumn(i)
            self.tableAssembly_PA.hideColumn(i)
        self.tableAssembly_P.hideColumn(24)
        self.tableAssembly_PA.hideColumn(24)
        self.tableAssembly_P.hideColumn(25)
        self.tableAssembly_PA.hideColumn(25)
        for i in range(27,33):
            self.tableAssembly_P.hideColumn(i)
            self.tableAssembly_PA.hideColumn(i)

        for i in range(34, self.model_P.columnCount()):
            self.tableAssembly_P.hideColumn(i)
        for i in range(34, self.model_PA.columnCount()):
            self.tableAssembly_PA.hideColumn(i)

        headers=['Nº Pedido', '','Nº Ref','','F. Cont.','','','','','','','','','','F. Prev. Taller','',
                '% Montaje','Cambios %','F. Rec.','F. Prev. Montaje','Observaciones', 'Fecha Aviso',
                '', 'Fecha Envío', '', '','OK', '', '', '', '', '','','Extras']
        
        headers_AL=['Nº Pedido', 'Fecha Pedido', 'Tipo Equipo', 'Cantidad', 'Detalle', 'Observaciones']

        self.tableAssembly_P.setItemDelegate(AlignDelegate(self.tableAssembly_P))
        self.color_delegate = ColorDelegate(self)
        self.tableAssembly_P.setItemDelegateForColumn(4, self.color_delegate)
        self.tableAssembly_P.setItemDelegateForColumn(14, self.color_delegate)
        self.tableAssembly_P.setItemDelegateForColumn(16, self.color_delegate)
        self.tableAssembly_P.setItemDelegateForColumn(19, self.color_delegate)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(16, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(17, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(18, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(19, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly_P.horizontalHeader().setSectionResizeMode(20, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableAssembly_P.horizontalHeader().setSectionResizeMode(25, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableAssembly_P.horizontalHeader().setDefaultSectionSize(80)
        self.tableAssembly_P.horizontalHeader().resizeSection(16, 60)
        self.tableAssembly_P.horizontalHeader().resizeSection(20, 700)
        self.tableAssembly_P.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_3.addWidget(self.tableAssembly_P, 3, 0, 1, 1)

        self.model_P.setAllColumnHeaders(headers)

        self.Button_All_P.clicked.connect(self.query_all_P_Assembly)
        self.Button_BG_P.clicked.connect(lambda event: self.colour_picker(self.tableAssembly_P))
        self.Button_ShowRef_P.clicked.connect(lambda event: self.show_ref(self.tableAssembly_P, self.Button_ShowRef_P))
        self.tableAssembly_P.setSortingEnabled(False)
        self.tableAssembly_P.horizontalHeader().sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked_P)
        self.tableAssembly_P.doubleClicked.connect(self.query_order)
        self.model_P.dataChanged.connect(self.saveChanges)

        self.tableAssembly_PA.setItemDelegate(AlignDelegate(self.tableAssembly_PA))
        self.color_delegate = ColorDelegate(self)
        self.tableAssembly_PA.setItemDelegateForColumn(4, self.color_delegate)
        self.tableAssembly_PA.setItemDelegateForColumn(14, self.color_delegate)
        self.tableAssembly_PA.setItemDelegateForColumn(16, self.color_delegate)
        self.tableAssembly_PA.setItemDelegateForColumn(19, self.color_delegate)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(16, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(17, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(18, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(19, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly_PA.horizontalHeader().setSectionResizeMode(20, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableAssembly_PA.horizontalHeader().setSectionResizeMode(25, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableAssembly_PA.horizontalHeader().setDefaultSectionSize(80)
        self.tableAssembly_PA.horizontalHeader().resizeSection(16, 60)
        self.tableAssembly_PA.horizontalHeader().resizeSection(20, 700)
        self.tableAssembly_PA.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_4.addWidget(self.tableAssembly_PA, 3, 0, 1, 1)

        self.model_PA.setAllColumnHeaders(headers)

        self.Button_All_PA.clicked.connect(self.query_all_PA_Assembly)
        self.Button_BG_PA.clicked.connect(lambda event: self.colour_picker(self.tableAssembly_PA))
        self.Button_ShowRef_PA.clicked.connect(lambda event: self.show_ref(self.tableAssembly_PA, self.Button_ShowRef_PA))
        self.tableAssembly_PA.setSortingEnabled(False)
        self.tableAssembly_PA.horizontalHeader().sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked_PA)
        self.tableAssembly_PA.doubleClicked.connect(self.query_order)
        self.model_PA.dataChanged.connect(self.saveChanges)

        self.tableAssembly_AL.setItemDelegate(AlignDelegate(self.tableAssembly_AL))
        self.tableAssembly_AL.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableAssembly_AL.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableAssembly_AL.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableAssembly_AL.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_5.addWidget(self.tableAssembly_AL, 3, 0, 1, 1)

        self.model_AL.setAllColumnHeaders(headers_AL)

        self.Button_All_AL.clicked.connect(self.query_all_AL_Assembly)
        self.tableAssembly_AL.setSortingEnabled(False)
        self.tableAssembly_AL.horizontalHeader().sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked_AL)
        # self.tableAssembly_AL.doubleClicked.connect(self.query_order)
        self.model_AL.dataChanged.connect(self.saveChanges)

        self.tableAssembly_P.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableAssembly_P, self.model_P, self.proxy_P)
        self.tableAssembly_PA.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableAssembly_PA, self.model_PA, self.proxy_PA)

# Function to load all P and PA
    def query_all_P_Assembly(self):
        """
        Queries the database for all orders P-, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model_P.dataChanged.disconnect(self.saveChanges)
        self.delete_allFilters_P()
        self.model_P.setTable("public.orders")
        self.model_P.setFilter("num_order LIKE 'P-%' AND num_order NOT LIKE '%R%'")
        self.model_P.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model_P.select()
        self.proxy_P.setSourceModel(self.model_P)
        self.tableAssembly_P.setModel(self.proxy_P)

        # Getting the unique values for each column of the model
        for column in range(self.model_P.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_P:
                self.checkbox_states_P[column] = {}
                self.checkbox_states_P[column]['Seleccionar todo'] = True
                for row in range(self.model_P.rowCount()):
                    value = self.model_P.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_P[column][str(value)] = True
                self.dict_valuesuniques_P[column] = list_valuesUnique

        for i in range(1,4):
            self.tableAssembly_P.hideColumn(i)
        for i in range(5,16):
            self.tableAssembly_P.hideColumn(i)
        for i in range(22,23):
            self.tableAssembly_P.hideColumn(i)
        self.tableAssembly_P.hideColumn(24)
        self.tableAssembly_P.hideColumn(25)
        for i in range(27,33):
            self.tableAssembly_P.hideColumn(i)

        for i in range(34, self.model_P.columnCount()):
            self.tableAssembly_P.hideColumn(i)

        headers=['Nº Pedido', '','Nº Ref','','F. Cont.','','','','','','','','','','F. Prev. Taller','',
                '% Montaje','Cambios %','F. Rec.','F. Prev. Montaje','Observaciones', 'Fecha Aviso',
                '', 'Fecha Envío', '', '','OK', '', '', '', '', '','','Extras']

        self.tableAssembly_P.setItemDelegate(AlignDelegate(self.tableAssembly_P))
        self.color_delegate = ColorDelegate(self)
        self.tableAssembly_P.setItemDelegateForColumn(4, self.color_delegate)
        self.tableAssembly_P.setItemDelegateForColumn(14, self.color_delegate)
        self.tableAssembly_P.setItemDelegateForColumn(16, self.color_delegate)
        self.tableAssembly_P.setItemDelegateForColumn(19, self.color_delegate)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(16, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(17, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(18, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(19, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(20, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableAssembly_P.horizontalHeader().setSectionResizeMode(25, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableAssembly_P.horizontalHeader().setDefaultSectionSize(80)
        self.tableAssembly_P.horizontalHeader().resizeSection(16, 60)
        self.tableAssembly_P.horizontalHeader().resizeSection(20, 700)
        self.tableAssembly_P.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_3.addWidget(self.tableAssembly_P, 2, 0, 1, 1)

        self.model_P.setAllColumnHeaders(headers)
        self.model_P.dataChanged.connect(self.saveChanges)

        self.tableAssembly_P.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableAssembly_P, self.model_P, self.proxy_P)

    def query_all_PA_Assembly(self):
        """
        Queries the database for all orders PA-, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model_PA.dataChanged.disconnect(self.saveChanges)
        self.delete_allFilters_PA()
        self.model_PA.setTable("public.orders")
        self.model_PA.setFilter("num_order LIKE 'PA-%' AND num_order NOT LIKE '%R%'")
        self.model_PA.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model_PA.select()
        self.proxy_PA.setSourceModel(self.model_PA)
        self.tableAssembly_PA.setModel(self.proxy_PA)

        # Getting the unique values for each column of the model
        for column in range(self.model_PA.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_PA:
                self.checkbox_states_PA[column] = {}
                self.checkbox_states_PA[column]['Seleccionar todo'] = True
                for row in range(self.model_PA.rowCount()):
                    value = self.model_PA.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_PA[column][str(value)] = True
                self.dict_valuesuniques_PA[column] = list_valuesUnique

        for i in range(1,4):
            self.tableAssembly_PA.hideColumn(i)
        for i in range(5,16):
            self.tableAssembly_PA.hideColumn(i)
        for i in range(22,23):
            self.tableAssembly_PA.hideColumn(i)
        self.tableAssembly_PA.hideColumn(24)
        self.tableAssembly_PA.hideColumn(25)
        for i in range(27,33):
            self.tableAssembly_PA.hideColumn(i)

        for i in range(34, self.model_PA.columnCount()):
            self.tableAssembly_PA.hideColumn(i)

        headers=['Nº Pedido', '','Nº Ref','','F. Cont.','','','','','','','','','','F. Prev. Taller','',
                '% Montaje','Cambios %','F. Rec.','F. Prev. Montaje','Observaciones', 'Fecha Aviso',
                '', 'Fecha Envío', '', '','OK', '', '', '', '', '','','Extras']

        self.tableAssembly_PA.setItemDelegate(AlignDelegate(self.tableAssembly_PA))
        self.color_delegate = ColorDelegate(self)
        self.tableAssembly_PA.setItemDelegateForColumn(4, self.color_delegate)
        self.tableAssembly_PA.setItemDelegateForColumn(14, self.color_delegate)
        self.tableAssembly_PA.setItemDelegateForColumn(16, self.color_delegate)
        self.tableAssembly_PA.setItemDelegateForColumn(19, self.color_delegate)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(16, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(17, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(18, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(19, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        # self.tableAssembly.horizontalHeader().setSectionResizeMode(20, QtWidgets.QHeaderView.ResizeMode.Interactive)
        self.tableAssembly_PA.horizontalHeader().setSectionResizeMode(25, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableAssembly_PA.horizontalHeader().setDefaultSectionSize(80)
        self.tableAssembly_PA.horizontalHeader().resizeSection(16, 60)
        self.tableAssembly_PA.horizontalHeader().resizeSection(20, 700)
        self.tableAssembly_PA.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_4.addWidget(self.tableAssembly_PA, 2, 0, 1, 1)

        self.model_PA.setAllColumnHeaders(headers)
        self.model_PA.dataChanged.connect(self.saveChanges)

        self.tableAssembly_PA.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableAssembly_PA, self.model_PA, self.proxy_PA)


# Functions to delete all filters when tool button is clicked
    def delete_allFilters_P(self):
        columns_number=self.model_P.columnCount()
        for index in range(columns_number):
            if index in self.proxy_P.filters:
                del self.proxy_P.filters[index]
            self.model_P.setIconColumnHeader(index, '')

        self.checkbox_states_P = {}
        self.dict_valuesuniques_P = {}
        self.dict_ordersort_P = {}
        self.checkbox_filters_P = {}

        self.proxy_P.invalidateFilter()
        self.tableAssembly_P.setModel(None)
        self.tableAssembly_P.setModel(self.proxy_P)

        # Getting the unique values for each column of the model
        for column in range(self.model_P.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_P:
                self.checkbox_states_P[column] = {}
                self.checkbox_states_P[column]['Seleccionar todo'] = True
                for row in range(self.model_P.rowCount()):
                    value = self.model_P.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_P[column][value] = True
                self.dict_valuesuniques_P[column] = list_valuesUnique

    def delete_allFilters_PA(self):
        columns_number=self.model_PA.columnCount()
        for index in range(columns_number):
            if index in self.proxy_PA.filters:
                del self.proxy_PA.filters[index]
            self.model_PA.setIconColumnHeader(index, '')

        self.checkbox_states_PA = {}
        self.dict_valuesuniques_PA = {}
        self.dict_ordersort_PA = {}
        self.checkbox_filters_PA = {}

        self.proxy_PA.invalidateFilter()
        self.tableAssembly_PA.setModel(None)
        self.tableAssembly_PA.setModel(self.proxy_P)

        # Getting the unique values for each column of the model
        for column in range(self.model_PA.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_PA:
                self.checkbox_states_PA[column] = {}
                self.checkbox_states_PA[column]['Seleccionar todo'] = True
                for row in range(self.model_PA.rowCount()):
                    value = self.model_PA.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_PA[column][value] = True
                self.dict_valuesuniques_PA[column] = list_valuesUnique


# Function to save changes into database
    def saveChanges(self):
        """
        Saves changes made to the data models and updates unique values for each column.
        """
        self.model_P.submitAll()

        for column in range(self.model_P.columnCount()):
            list_valuesUnique = []
            for row in range(self.model_P.rowCount()):
                value = self.model_P.record(row).value(column)
                if value not in list_valuesUnique:
                    if isinstance(value, QtCore.QDate):
                        value=value.toString("dd/MM/yyyy")
                    list_valuesUnique.append(str(value))
                    if value not in self.checkbox_states_P[column]:
                        self.checkbox_states_P[column][value] = True
            self.dict_valuesuniques_P[column] = list_valuesUnique

        self.model_PA.submitAll()

        for column in range(self.model_PA.columnCount()):
            list_valuesUnique = []
            for row in range(self.model_PA.rowCount()):
                value = self.model_PA.record(row).value(column)
                if value not in list_valuesUnique:
                    if isinstance(value, QtCore.QDate):
                        value=value.toString("dd/MM/yyyy")
                    list_valuesUnique.append(str(value))
                    if value not in self.checkbox_states_PA[column]:
                        self.checkbox_states_PA[column][value] = True
            self.dict_valuesuniques_PA[column] = list_valuesUnique

        self.model_AL.submitAll()

        for column in range(self.model_AL.columnCount()):
            list_valuesUnique = []
            for row in range(self.model_AL.rowCount()):
                value = self.model_AL.record(row).value(column)
                if value not in list_valuesUnique:
                    if isinstance(value, QtCore.QDate):
                        value=value.toString("dd/MM/yyyy")
                    list_valuesUnique.append(str(value))
                    if value not in self.checkbox_states_AL[column]:
                        self.checkbox_states_AL[column][value] = True
            self.dict_valuesuniques_AL[column] = list_valuesUnique


# Function when header of each table is clicked
    def on_view_horizontalHeader_sectionClicked_P(self, logicalIndex):
        """
        Displays a menu when a column header is clicked. The menu includes options for sorting, filtering, and managing column visibility.
        
        Args:
            logicalIndex (int): Index of the clicked column.
        """
        self.logicalIndex = logicalIndex
        self.menuValues = QtWidgets.QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(self.tableAssembly_P)

        valuesUnique_view = []
        for row in range(self.tableAssembly_P.model().rowCount()):
            index = self.tableAssembly_P.model().index(row, self.logicalIndex)
            value = index.data(Qt.ItemDataRole.DisplayRole)
            if value not in valuesUnique_view:
                if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
                valuesUnique_view.append(value)

        actionSortAscending = QtGui.QAction("Ordenar Ascendente", self.tableAssembly_P)
        actionSortAscending.triggered.connect(self.on_actionSortAscending_triggered_P)
        self.menuValues.addAction(actionSortAscending)
        actionSortDescending = QtGui.QAction("Ordenar Descendente", self.tableAssembly_P)
        actionSortDescending.triggered.connect(self.on_actionSortDescending_triggered_P)
        self.menuValues.addAction(actionSortDescending)
        self.menuValues.addSeparator()

        actionDeleteFilterColumn = QtGui.QAction("Quitar Filtro", self.tableAssembly_P)
        actionDeleteFilterColumn.triggered.connect(self.on_actionDeleteFilterColumn_triggered_P)
        self.menuValues.addAction(actionDeleteFilterColumn)
        self.menuValues.addSeparator()

        actionTextFilter = QtGui.QAction("Buscar...", self.tableAssembly_P)
        actionTextFilter.triggered.connect(self.on_actionTextFilter_triggered_P)
        self.menuValues.addAction(actionTextFilter)
        self.menuValues.addSeparator()

        # scroll_menu = QtWidgets.QScrollArea()
        # scroll_menu.setStyleSheet("background-color: rgb(255, 255, 255)")
        # scroll_menu.setWidgetResizable(True)
        # scroll_widget = QtWidgets.QWidget(scroll_menu)
        # scroll_menu.setWidget(scroll_widget)
        # scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

        # checkbox_all_widget = QtWidgets.QCheckBox('Seleccionar todo')

        # if not self.checkbox_states_P[self.logicalIndex]['Seleccionar todo'] == True:
        #     checkbox_all_widget.setChecked(False)
        # else:
        #     checkbox_all_widget.setChecked(True)
        
        # checkbox_all_widget.toggled.connect(lambda checked, name='Seleccionar todo': self.on_select_all_toggled_P(checked, name))

        # scroll_layout.addWidget(checkbox_all_widget)
        # self.action_checkbox_map_P['Seleccionar todo'] = checkbox_all_widget

        # if len(self.dict_ordersort_P) != 0 and self.logicalIndex in self.dict_ordersort_P:
        #     list_uniquevalues = sorted(list(set(self.dict_valuesuniques_P[self.logicalIndex])))
        # else:
        #     list_uniquevalues = sorted(list(set(valuesUnique_view)))

        # for actionName in list_uniquevalues:
        #     checkbox_widget = QtWidgets.QCheckBox(str(actionName))

        #     if self.logicalIndex not in self.checkbox_filters_P:
        #         checkbox_widget.setChecked(True)
        #     elif actionName not in self.checkbox_filters_P[self.logicalIndex]:
        #         checkbox_widget.setChecked(False)
        #     else:
        #         checkbox_widget.setChecked(True)

        #     checkbox_widget.toggled.connect(lambda checked, name=actionName: self.on_checkbox_toggled_P(checked, name))

        #     scroll_layout.addWidget(checkbox_widget)
        #     self.action_checkbox_map_P[actionName] = checkbox_widget

        # action_scroll_menu = QtWidgets.QWidgetAction(self.menuValues)
        # action_scroll_menu.setDefaultWidget(scroll_menu)
        # self.menuValues.addAction(action_scroll_menu)

        # self.menuValues.addSeparator()

        # accept_button = QtGui.QAction("ACEPTAR", self.tableAssembly_P)
        # accept_button.triggered.connect(self.menu_acceptbutton_triggered_P)

        # cancel_button = QtGui.QAction("CANCELAR", self.tableAssembly_P)
        # cancel_button.triggered.connect(self.menu_cancelbutton_triggered)

        # self.menuValues.addAction(accept_button)
        # self.menuValues.addAction(cancel_button)

        self.menuValues.setStyleSheet("QMenu { color: black; }"
                                        "QMenu { background-color: rgb(255, 255, 255); }"
                                        "QMenu::item:selected { background-color: #33bdef; }"
                                        "QMenu::item:pressed { background-color: rgb(1, 140, 190); }")

        headerPos = self.tableAssembly_P.mapToGlobal(self.tableAssembly_P.horizontalHeader().pos())        

        posY = headerPos.y() + self.tableAssembly_P.horizontalHeader().height()
        scrollX = self.tableAssembly_P.horizontalScrollBar().value()
        xInView = self.tableAssembly_P.horizontalHeader().sectionViewportPosition(logicalIndex)
        posX = headerPos.x() + xInView - scrollX

        self.menuValues.exec(QtCore.QPoint(posX, posY))

    def on_view_horizontalHeader_sectionClicked_PA(self, logicalIndex):
        """
        Displays a menu when a column header is clicked. The menu includes options for sorting, filtering, and managing column visibility.
        
        Args:
            logicalIndex (int): Index of the clicked column.
        """
        self.logicalIndex = logicalIndex
        self.menuValues = QtWidgets.QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(self.tableAssembly_PA)

        valuesUnique_view = []
        for row in range(self.tableAssembly_PA.model().rowCount()):
            index = self.tableAssembly_PA.model().index(row, self.logicalIndex)
            value = index.data(Qt.ItemDataRole.DisplayRole)
            if value not in valuesUnique_view:
                if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
                valuesUnique_view.append(value)

        actionSortAscending = QtGui.QAction("Ordenar Ascendente", self.tableAssembly_PA)
        actionSortAscending.triggered.connect(self.on_actionSortAscending_triggered_PA)
        self.menuValues.addAction(actionSortAscending)
        actionSortDescending = QtGui.QAction("Ordenar Descendente", self.tableAssembly_PA)
        actionSortDescending.triggered.connect(self.on_actionSortDescending_triggered_PA)
        self.menuValues.addAction(actionSortDescending)
        self.menuValues.addSeparator()

        actionDeleteFilterColumn = QtGui.QAction("Quitar Filtro", self.tableAssembly_PA)
        actionDeleteFilterColumn.triggered.connect(self.on_actionDeleteFilterColumn_triggered_PA)
        self.menuValues.addAction(actionDeleteFilterColumn)
        self.menuValues.addSeparator()

        actionTextFilter = QtGui.QAction("Buscar...", self.tableAssembly_PA)
        actionTextFilter.triggered.connect(self.on_actionTextFilter_triggered_PA)
        self.menuValues.addAction(actionTextFilter)
        self.menuValues.addSeparator()

        # scroll_menu = QtWidgets.QScrollArea()
        # scroll_menu.setStyleSheet("background-color: rgb(255, 255, 255)")
        # scroll_menu.setWidgetResizable(True)
        # scroll_widget = QtWidgets.QWidget(scroll_menu)
        # scroll_menu.setWidget(scroll_widget)
        # scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

        # checkbox_all_widget = QtWidgets.QCheckBox('Seleccionar todo')

        # if not self.checkbox_states_PA[self.logicalIndex]['Seleccionar todo'] == True:
        #     checkbox_all_widget.setChecked(False)
        # else:
        #     checkbox_all_widget.setChecked(True)
        
        # checkbox_all_widget.toggled.connect(lambda checked, name='Seleccionar todo': self.on_select_all_toggled_PA(checked, name))

        # scroll_layout.addWidget(checkbox_all_widget)
        # self.action_checkbox_map_PA['Seleccionar todo'] = checkbox_all_widget

        # if len(self.dict_ordersort_PA) != 0 and self.logicalIndex in self.dict_ordersort_PA:
        #     list_uniquevalues = sorted(list(set(self.dict_valuesuniques_PA[self.logicalIndex])))
        # else:
        #     list_uniquevalues = sorted(list(set(valuesUnique_view)))

        # for actionName in list_uniquevalues:
        #     checkbox_widget = QtWidgets.QCheckBox(str(actionName))

        #     if self.logicalIndex not in self.checkbox_filters_PA:
        #         checkbox_widget.setChecked(True)
        #     elif actionName not in self.checkbox_filters_PA[self.logicalIndex]:
        #         checkbox_widget.setChecked(False)
        #     else:
        #         checkbox_widget.setChecked(True)

        #     checkbox_widget.toggled.connect(lambda checked, name=actionName: self.on_checkbox_toggled_PA(checked, name))

        #     scroll_layout.addWidget(checkbox_widget)
        #     self.action_checkbox_map_PA[actionName] = checkbox_widget

        # action_scroll_menu = QtWidgets.QWidgetAction(self.menuValues)
        # action_scroll_menu.setDefaultWidget(scroll_menu)
        # self.menuValues.addAction(action_scroll_menu)

        # self.menuValues.addSeparator()

        # accept_button = QtGui.QAction("ACEPTAR", self.tableAssembly_PA)
        # accept_button.triggered.connect(self.menu_acceptbutton_triggered_PA)

        # cancel_button = QtGui.QAction("CANCELAR", self.tableAssembly_PA)
        # cancel_button.triggered.connect(self.menu_cancelbutton_triggered)

        # self.menuValues.addAction(accept_button)
        # self.menuValues.addAction(cancel_button)

        self.menuValues.setStyleSheet("QMenu { color: black; }"
                                        "QMenu { background-color: rgb(255, 255, 255); }"
                                        "QMenu::item:selected { background-color: #33bdef; }"
                                        "QMenu::item:pressed { background-color: rgb(1, 140, 190); }")

        headerPos = self.tableAssembly_PA.mapToGlobal(self.tableAssembly_PA.horizontalHeader().pos())        

        posY = headerPos.y() + self.tableAssembly_PA.horizontalHeader().height()
        scrollX = self.tableAssembly_PA.horizontalScrollBar().value()
        xInView = self.tableAssembly_PA.horizontalHeader().sectionViewportPosition(logicalIndex)
        posX = headerPos.x() + xInView - scrollX

        self.menuValues.exec(QtCore.QPoint(posX, posY))


# Function when cancel button of menu is clicked
    def menu_cancelbutton_triggered(self):
        """
        Hides the menu when the cancel button is clicked.
        """
        self.menuValues.hide()


# Function when accept button of menu is clicked for each table
    def menu_acceptbutton_triggered_P(self):
        """
        Applies the selected filters and updates the table model with the new filters.
        """
        for column, filters in self.checkbox_filters_P.items():
            if filters:
                self.proxy_P.setFilter(filters, column)
            else:
                self.proxy_P.setFilter(None, column)

    def menu_acceptbutton_triggered_PA(self):
        """
        Applies the selected filters and updates the table model with the new filters.
        """
        for column, filters in self.checkbox_filters_PA.items():
            if filters:
                self.proxy_PA.setFilter(filters, column)
            else:
                self.proxy_PA.setFilter(None, column)


# Function when select all checkbox is clicked for each table
    def on_select_all_toggled_P(self, checked, action_name):
        """
        Toggles the state of all checkboxes in the filter menu when the 'Select All' checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the 'Select All' checkbox.
            action_name (str): The name of the action (usually 'Select All').
        """
        filterColumn = self.logicalIndex
        imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
        icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))

        if checked:
            for checkbox_name, checkbox_widget in self.action_checkbox_map_P.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states_P[self.logicalIndex][checkbox_name] = checked

            if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map_P.values()):
                self.model_P.setIconColumnHeader(filterColumn, icono)
            else:
                self.model_P.setIconColumnHeader(filterColumn, '')
        
        else:
            for checkbox_name, checkbox_widget in self.action_checkbox_map_P.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states_P[self.logicalIndex][checkbox_widget.text()] = checked

# Function when select all checkbox is clicked
    def on_select_all_toggled_PA(self, checked, action_name):
        """
        Toggles the state of all checkboxes in the filter menu when the 'Select All' checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the 'Select All' checkbox.
            action_name (str): The name of the action (usually 'Select All').
        """
        filterColumn = self.logicalIndex
        imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
        icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))

        if checked:
            for checkbox_name, checkbox_widget in self.action_checkbox_map_PA.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states_PA[self.logicalIndex][checkbox_name] = checked

            if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map_PA.values()):
                self.model_PA.setIconColumnHeader(filterColumn, icono)
            else:
                self.model_PA.setIconColumnHeader(filterColumn, '')
        
        else:
            for checkbox_name, checkbox_widget in self.action_checkbox_map_PA.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states_PA[self.logicalIndex][checkbox_widget.text()] = checked


# Function when checkbox of header menu is clicked for each table
    def on_checkbox_toggled_P(self, checked, action_name):
        """
        Updates the filter state when an individual checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the checkbox.
            action_name (str): The name of the checkbox.
        """
        filterColumn = self.logicalIndex
        imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
        icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))

        if checked:
            if filterColumn not in self.checkbox_filters_P:
                self.checkbox_filters_P[filterColumn] = [action_name]
            else:
                if action_name not in self.checkbox_filters_P[filterColumn]:
                    self.checkbox_filters_P[filterColumn].append(action_name)
        else:
            if filterColumn in self.checkbox_filters_P and action_name in self.checkbox_filters_P[filterColumn]:
                self.checkbox_filters_P[filterColumn].remove(action_name)

        if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map_P.values()):
            self.model_P.setIconColumnHeader(filterColumn, '')
        else:
            self.model_P.setIconColumnHeader(filterColumn, icono)

    def on_checkbox_toggled_PA(self, checked, action_name):
        """
        Updates the filter state when an individual checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the checkbox.
            action_name (str): The name of the checkbox.
        """
        filterColumn = self.logicalIndex
        imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
        icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))

        if checked:
            if filterColumn not in self.checkbox_filters_PA:
                self.checkbox_filters_PA[filterColumn] = [action_name]
            else:
                if action_name not in self.checkbox_filters_PA[filterColumn]:
                    self.checkbox_filters_PA[filterColumn].append(action_name)
        else:
            if filterColumn in self.checkbox_filters_PA and action_name in self.checkbox_filters_PA[filterColumn]:
                self.checkbox_filters_PA[filterColumn].remove(action_name)

        if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map_PA.values()):
            self.model_PA.setIconColumnHeader(filterColumn, '')
        else:
            self.model_PA.setIconColumnHeader(filterColumn, icono)


# Function to delete individual column filter for each table
    def on_actionDeleteFilterColumn_triggered_P(self):
        """
        Removes the filter from the selected column and updates the table model.
        """
        filterColumn = self.logicalIndex
        if filterColumn in self.proxy_P.filters:
            del self.proxy_P.filters[filterColumn]
        self.model_P.setIconColumnHeader(filterColumn, '')
        self.proxy_P.invalidateFilter()

        # self.tableAssembly.setModel(None)
        self.tableAssembly_P.setModel(self.proxy_P)

        if filterColumn in self.checkbox_filters_P:
            del self.checkbox_filters_P[filterColumn]

        self.checkbox_states_P[self.logicalIndex].clear()
        self.checkbox_states_P[self.logicalIndex]['Seleccionar todo'] = True
        for row in range(self.tableAssembly_P.model().rowCount()):
            value = self.model_P.record(row).value(filterColumn)
            if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
            self.checkbox_states_P[self.logicalIndex][str(value)] = True

    def on_actionDeleteFilterColumn_triggered_PA(self):
        """
        Removes the filter from the selected column and updates the table model.
        """
        filterColumn = self.logicalIndex
        if filterColumn in self.proxy_PA.filters:
            del self.proxy_PA.filters[filterColumn]
        self.model_PA.setIconColumnHeader(filterColumn, '')
        self.proxy_PA.invalidateFilter()

        # self.tableAssembly.setModel(None)
        self.tableAssembly_PA.setModel(self.proxy_PA)

        if filterColumn in self.checkbox_filters_PA:
            del self.checkbox_filters_PA[filterColumn]

        self.checkbox_states_PA[self.logicalIndex].clear()
        self.checkbox_states_PA[self.logicalIndex]['Seleccionar todo'] = True
        for row in range(self.tableAssembly_PA.model().rowCount()):
            value = self.model_PA.record(row).value(filterColumn)
            if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
            self.checkbox_states_PA[self.logicalIndex][str(value)] = True


# Function to order column ascending for each table
    def on_actionSortAscending_triggered_P(self):
        """
        Sorts the selected column in ascending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.AscendingOrder
        self.tableAssembly_P.sortByColumn(sortColumn, sortOrder)

    def on_actionSortAscending_triggered_PA(self):
        """
        Sorts the selected column in ascending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.AscendingOrder
        self.tableAssembly_PA.sortByColumn(sortColumn, sortOrder)


# Function to order column descending for each table
    def on_actionSortDescending_triggered_P(self):
        """
        Sorts the selected column in descending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.DescendingOrder
        self.tableAssembly_P.sortByColumn(sortColumn, sortOrder)

    def on_actionSortDescending_triggered_PA(self):
        """
        Sorts the selected column in descending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.DescendingOrder
        self.tableAssembly_PA.sortByColumn(sortColumn, sortOrder)


# Function when text is searched for each table
    def on_actionTextFilter_triggered_P(self):
        """
        Opens a dialog to enter a text filter and applies it to the selected column.
        """
        filterColumn = self.logicalIndex
        dlg = QtWidgets.QInputDialog()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle('Buscar')
        clickedButton=dlg.exec()

        if clickedButton == 1:
            stringAction = dlg.textValue()
            if re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', stringAction):
                stringAction=QtCore.QDate.fromString(stringAction,"dd/MM/yyyy")
                stringAction=stringAction.toString("yyyy-MM-dd")

            filterString = QtCore.QRegularExpression(stringAction, QtCore.QRegularExpression.PatternOption(0))
            # del self.proxy.filters[filterColumn]
            self.proxy_P.setFilter([stringAction], filterColumn)

            imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
            icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))
            self.model_P.setIconColumnHeader(filterColumn, icono)

    def on_actionTextFilter_triggered_PA(self):
        """
        Opens a dialog to enter a text filter and applies it to the selected column.
        """
        filterColumn = self.logicalIndex
        dlg = QtWidgets.QInputDialog()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle('Buscar')
        clickedButton=dlg.exec()

        if clickedButton == 1:
            stringAction = dlg.textValue()
            if re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', stringAction):
                stringAction=QtCore.QDate.fromString(stringAction,"dd/MM/yyyy")
                stringAction=stringAction.toString("yyyy-MM-dd")

            filterString = QtCore.QRegularExpression(stringAction, QtCore.QRegularExpression.PatternOption(0))
            # del self.proxy.filters[filterColumn]
            self.proxy_PA.setFilter([stringAction], filterColumn)

            imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
            icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))
            self.model_PA.setIconColumnHeader(filterColumn, icono)


# Function for key events
    def custom_keyPressEvent(self, event, table, model, proxy):
        """
        Handles custom key events for cell operations in the table, including delete, copy, paste, and custom shortcuts.

        Args:
            event (QtGui.QKeyEvent): The key event to handle.
            table (QtWidgets.QTableView or QtWidgets.QTableWidget): The table that is handling the event.
            model (QtCore.QAbstractItemModel): The model associated with the table.
            proxy (QtCore.QSortFilterProxyModel): The proxy model used for filtering or sorting, if applicable.
        """
        if event.key() == QtCore.Qt.Key.Key_Delete: # Event when delete key is pressed
            selected_indexes = table.selectionModel().selectedIndexes()
            if not selected_indexes:
                return
            
            model = table.model()
            model_indexes = [model.mapToSource(index) for index in selected_indexes]

            if isinstance(model, QtCore.QSortFilterProxyModel):
                model_indexes = [model.mapToSource(index) for index in selected_indexes]
                for index in model_indexes:
                    model.sourceModel().setData(index, None)
            else:
                model_indexes = selected_indexes
                for index in model_indexes:
                    model.setData(index, None)

        elif event.modifiers() and QtCore.Qt.KeyboardModifier.ControlModifier: # Event when ctrl + comma is pressed
            if event.key() == QtCore.Qt.Key.Key_Comma:
                selected_indexes = table.selectionModel().selectedIndexes()
                if not selected_indexes:
                    return

                model = table.model()

                if isinstance(model, QtCore.QSortFilterProxyModel):
                    model_indexes = [model.mapToSource(index) for index in selected_indexes]
                    for index in model_indexes:
                        model.sourceModel().setData(index, date.today().strftime("%d/%m/%Y"))
                else:
                    model_indexes = selected_indexes
                    for index in model_indexes:
                        model.setData(index, date.today().strftime("%d/%m/%Y"))

        elif event.matches(QKeySequence.StandardKey.Copy): # Event for copy (ctrl + c)
            selected_indexes = table.selectionModel().selectedIndexes()
            if not selected_indexes:
                return
            
            model = table.model()
            model_indexes = [model.mapToSource(index) for index in selected_indexes]

            mime_data = QMimeData()
            data = bytearray()

            for index in model_indexes:
                data += str(model.data(index)).encode('utf-8') + b'\t'

            mime_data.setData("text/plain", data)

            clipboard = QApplication.clipboard()
            clipboard.setMimeData(mime_data)

        elif event.matches(QKeySequence.StandardKey.Paste): # Event for paste (ctrl + v)
            if table.selectionModel() != None:

                clipboard = QApplication.clipboard()
                mime_data = clipboard.mimeData()

                if not mime_data.hasFormat("text/plain"):
                    return

                data = mime_data.data("text/plain").data()
                values = data.split(b'\t')

                selected_indexes = table.selectionModel().selectedIndexes()
                if not selected_indexes:
                    return
                
                model = table.model()
                model_indexes = [model.mapToSource(index) for index in selected_indexes]

                for index, value in zip(model_indexes, values):
                    model.setData(index, value.decode('utf-8'))

                model.submitAll()

        elif event.matches(QKeySequence.StandardKey.MoveToNextLine): # Event for down cursor pressed
            if table.selectionModel() != None:
                selected_indexes = table.selectionModel().selectedIndexes()
                if len(selected_indexes) == 1:
                    for index in selected_indexes:
                        current_row = index.row()
                        current_column = index.column()

                    new_row = current_row + 1 if current_row < model.rowCount() - 1 else current_row

                    table.selectionModel().clearSelection()
                    new_selection = QtCore.QItemSelection(QtCore.QModelIndex(model.index(new_row, current_column)), QtCore.QModelIndex(model.index(new_row, current_column)))
                    table.selectionModel().select(new_selection, QtCore.QItemSelectionModel.SelectionFlag.Select)
                    table.selectionModel().setCurrentIndex(model.index(new_row, current_column), QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect)

        elif event.matches(QKeySequence.StandardKey.MoveToPreviousLine): # Event for up cursor pressed
            if table.selectionModel() != None:
                selected_indexes = table.selectionModel().selectedIndexes()
                if len(selected_indexes) == 1:
                    for index in selected_indexes:
                        current_row = index.row()
                        current_column = index.column()

                    new_row = current_row - 1 if current_row > 0 else 0

                    table.selectionModel().clearSelection()
                    new_selection = QtCore.QItemSelection(QtCore.QModelIndex(model.index(new_row, current_column)), QtCore.QModelIndex(model.index(new_row, current_column)))
                    table.selectionModel().select(new_selection, QtCore.QItemSelectionModel.SelectionFlag.Select)
                    table.selectionModel().setCurrentIndex(model.index(new_row, current_column), QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect)

        elif event.matches(QKeySequence.StandardKey.MoveToNextChar): # Event for right cursor pressed
            if table.selectionModel() != None:
                selected_indexes = table.selectionModel().selectedIndexes()
                if len(selected_indexes) == 1:
                    for index in selected_indexes:
                        current_row = index.row()
                        current_column = index.column()

                    new_column = current_column + 1 if current_column < model.columnCount() - 1 else current_column

                    table.selectionModel().clearSelection()
                    new_selection = QtCore.QItemSelection(QtCore.QModelIndex(model.index(current_row, new_column)), QtCore.QModelIndex(model.index(current_row, new_column)))
                    table.selectionModel().select(new_selection, QtCore.QItemSelectionModel.SelectionFlag.Select)
                    table.selectionModel().setCurrentIndex(model.index(current_row, new_column), QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect)

        elif event.matches(QKeySequence.StandardKey.MoveToPreviousChar): # Event for left cursor pressed
            if table.selectionModel() != None:
                selected_indexes = table.selectionModel().selectedIndexes()
                if len(selected_indexes) == 1:
                    for index in selected_indexes:
                        current_row = index.row()
                        current_column = index.column()

                    new_column = current_column - 1 if current_column > 1 else 1

                    table.selectionModel().clearSelection()
                    new_selection = QtCore.QItemSelection(QtCore.QModelIndex(model.index(current_row, new_column)), QtCore.QModelIndex(model.index(current_row, new_column)))
                    table.selectionModel().select(new_selection, QtCore.QItemSelectionModel.SelectionFlag.Select)
                    table.selectionModel().setCurrentIndex(model.index(current_row, new_column), QtCore.QItemSelectionModel.SelectionFlag.ClearAndSelect)

        elif event.matches(QKeySequence.StandardKey.InsertParagraphSeparator): # Event for enter pressed
            current_index = table.selectionModel().selectedIndexes()[0]

            if current_index.isValid():
                table.edit(current_index)

        super().keyPressEvent(event)

# Function open order index
    def query_order(self, item):
        """
        Opens a window showing drawing index for the selected order number.
        """
        if item.column() == 0:
            num_order = item.data()
            from windows.WorkshopDrawingIndex_Window import Ui_WorkshopDrawingIndex_Window
            dbparam = config_database()
            user_database = dbparam["user"]
            password_database = dbparam["password"]

            db_index = Create_DBconnection(user_database, password_database, 'drawing' + num_order + '-a')

            if not db_index:
                sys.exit()

            self.index_drawing_window = Ui_WorkshopDrawingIndex_Window(db_index, self.username, num_order)
            self.index_drawing_window.showMaximized()

            self.index_drawing_window.closeEvent = lambda event: self.close_drawing_window(num_order, event)

# Function to handle the close event of the drawing window
    def close_drawing_window(self, num_order, event):
        """
        Handles the close event of index drawing window.

        Args:
            num_order (str): The order number associated with the window being closed.
            event (QCloseEvent): The close event that should be accepted to allow the window to close properly.
        """
        if num_order in self.open_windows:
            del self.open_windows[num_order]
        event.accept()


# Function to open colour picker
    def colour_picker(self, table):
        """
        Opens a color picker dialog to set the background color for selected table items.
        """
        scroll_position = table.verticalScrollBar().value()
        selected_indexes = table.selectionModel().selectedIndexes()

        if not selected_indexes:
            return

        bg_color = QtWidgets.QColorDialog.getColor(QtGui.QColor(0, 0, 0), self)
        hex_color = bg_color.name()

        for index in selected_indexes:
            state_column_index = index.sibling(index.row(), 0)
            value = str(state_column_index.data())

            try:
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        for index in selected_indexes:
                            state_column_index = index.sibling(index.row(), 0)
                            value = str(state_column_index.data())
                        
                            commands_colors = "UPDATE orders SET bg_color_assembly = %s WHERE num_order = %s"
                            cur.execute(commands_colors, (hex_color, value,))
                    conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                # Handle the error appropriately
                pass

        self.query_data()

        # table.selectionModel().select(index, QtCore.QItemSelectionModel.SelectionFlag.Select)
        # table.verticalScrollBar().setSliderPosition(scroll_position)


# Function to export data to excel
    def exporttoexcel(self):
        """
        Exports the visible data from the table to an Excel file. If no data is loaded, displays a warning message.

        Shows a message box if there is no data to export and allows the user to save the data to an Excel file.
        """

        final_data1 = []
        final_data2 = []
        final_data3 = []

        visible_columns = [col for col in range(self.model_P.columnCount()) if not self.tableAssembly_P.isColumnHidden(col)]
        visible_headers = self.model_P.getColumnHeaders(visible_columns)
        for row in range(self.proxy_P.rowCount()):
            tag_data = []
            for column in visible_columns:
                value = self.proxy_P.data(self.proxy_P.index(row, column))
                if isinstance(value, QDate):
                    value = value.toString("dd/MM/yyyy")
                elif column in [11,21]:
                    value = int(value) if value != '' else 0
                tag_data.append(value)
            final_data1.append(tag_data)

        final_data1.insert(0, visible_headers)
        df_P = pd.DataFrame(final_data1)
        df_P.columns = df_P.iloc[0]
        df_P = df_P[1:]

        visible_columns = [col for col in range(self.model_PA.columnCount()) if not self.tableAssembly_PA.isColumnHidden(col)]
        visible_headers = self.model_PA.getColumnHeaders(visible_columns)
        for row in range(self.proxy_PA.rowCount()):
            tag_data = []
            for column in visible_columns:
                value = self.proxy_PA.data(self.proxy_PA.index(row, column))
                if isinstance(value, QDate):
                    value = value.toString("dd/MM/yyyy")
                elif column in [16,21]:
                    value = int(value) if value != '' else 0
                tag_data.append(value)
            final_data2.append(tag_data)

        final_data2.insert(0, visible_headers)
        df_PA = pd.DataFrame(final_data2)
        df_PA.columns = df_PA.iloc[0]
        df_PA = df_PA[1:]

        visible_columns = [col for col in range(self.model_AL.columnCount()) if not self.tableAssembly_AL.isColumnHidden(col)]
        visible_headers = self.model_AL.getColumnHeaders(visible_columns)
        for row in range(self.proxy_AL.rowCount()):
            tag_data = []
            for column in visible_columns:
                value = self.proxy_AL.data(self.proxy_AL.index(row, column))
                if isinstance(value, QDate):
                    value = value.toString("dd/MM/yyyy")
                elif column in [3]:
                    value = int(value) if value != '' else 0
                tag_data.append(value)
            final_data3.append(tag_data)

        final_data3.insert(0, visible_headers)
        df_AL = pd.DataFrame(final_data3)
        df_AL.columns = df_AL.iloc[0]
        df_AL = df_AL[1:]

        output_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Guardar Excel", "", "Archivos de Excel (*.xlsx)")
        if output_path:
            if not output_path.lower().endswith(".xlsx"):
                output_path += ".xlsx"
            df_P.to_excel(output_path, index=False, header=True)
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                df_P.to_excel(writer, sheet_name='P-', index=False)
                df_PA.to_excel(writer, sheet_name='PA-', index=False)
                df_AL.to_excel(writer, sheet_name='AL-', index=False)


# Function to load data
    def query_all_AL_Assembly(self):
        """
        Queries the database for all orders AL-, configures and populates tables with the query results, 
        and updates the UI accordingly. Handles potential database errors and updates the UI with appropriate messages.
        """
        self.model_AL.dataChanged.disconnect(self.saveChanges)
        self.delete_allFilters_AL()
        self.model_AL.setTable("public.orders_warehouse")
        # self.model_AL.setFilter("num_order LIKE 'PA-%' AND num_order NOT LIKE '%R%'")
        self.model_AL.setSort(0, QtCore.Qt.SortOrder.AscendingOrder)
        self.model_AL.select()
        self.proxy_AL.setSourceModel(self.model_AL)
        self.tableAssembly_AL.setModel(self.proxy_AL)

        # Getting the unique values for each column of the model
        for column in range(self.model_AL.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_AL:
                self.checkbox_states_AL[column] = {}
                self.checkbox_states_AL[column]['Seleccionar todo'] = True
                for row in range(self.model_AL.rowCount()):
                    value = self.model_AL.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_AL[column][str(value)] = True
                self.dict_valuesuniques_AL[column] = list_valuesUnique

        headers_AL=['Nº Pedido', 'Fecha Pedido', 'Tipo Equipo', 'Cantidad', 'Detalle', 'Observaciones']

        self.tableAssembly_AL.setItemDelegate(AlignDelegate(self.tableAssembly_AL))
        self.tableAssembly_AL.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableAssembly_AL.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableAssembly_AL.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableAssembly_AL.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")
        self.gridLayout_5.addWidget(self.tableAssembly_AL, 3, 0, 1, 1)

        self.model_AL.setAllColumnHeaders(headers_AL)

        self.Button_All_AL.clicked.connect(self.query_all_AL_Assembly)
        self.tableAssembly_AL.setSortingEnabled(False)
        self.tableAssembly_AL.horizontalHeader().sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked_AL)
        self.tableAssembly_AL.doubleClicked.connect(self.query_order)
        self.model_AL.dataChanged.connect(self.saveChanges)

        self.tableAssembly_AL.keyPressEvent = lambda event: self.custom_keyPressEvent(event, self.tableAssembly_AL, self.model_PA, self.proxy_PA)

# Function to delete all filters
    def delete_allFilters_AL(self):
        """
        Resets all filters and updates the table model with unique values for each column.
        """
        columns_number=self.model_AL.columnCount()
        for index in range(columns_number):
            if index in self.proxy_AL.filters:
                del self.proxy_AL.filters[index]
            self.model_PA.setIconColumnHeader(index, '')

        self.checkbox_states_AL = {}
        self.dict_valuesuniques_AL = {}
        self.dict_ordersort_AL = {}
        self.checkbox_filters_AL = {}

        self.proxy_AL.invalidateFilter()
        self.tableAssembly_AL.setModel(None)
        self.tableAssembly_AL.setModel(self.proxy_AL)

        # Getting the unique values for each column of the model
        for column in range(self.model_AL.columnCount()):
            list_valuesUnique = []
            if column not in self.checkbox_states_AL:
                self.checkbox_states_AL[column] = {}
                self.checkbox_states_AL[column]['Seleccionar todo'] = True
                for row in range(self.model_AL.rowCount()):
                    value = self.model_AL.record(row).value(column)
                    if value not in list_valuesUnique:
                        if isinstance(value, QtCore.QDate):
                            value=value.toString("dd/MM/yyyy")
                        list_valuesUnique.append(str(value))
                        self.checkbox_states_AL[column][value] = True
                self.dict_valuesuniques_AL[column] = list_valuesUnique

# Function when header is clicked
    def on_view_horizontalHeader_sectionClicked_AL(self, logicalIndex):
        """
        Displays a menu when a column header is clicked. The menu includes options for sorting, filtering, and managing column visibility.
        
        Args:
            logicalIndex (int): Index of the clicked column.
        """
        self.logicalIndex = logicalIndex
        self.menuValues = QtWidgets.QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(self.tableAssembly_AL)

        valuesUnique_view = []
        for row in range(self.tableAssembly_AL.model().rowCount()):
            index = self.tableAssembly_AL.model().index(row, self.logicalIndex)
            value = index.data(Qt.ItemDataRole.DisplayRole)
            if value not in valuesUnique_view:
                if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
                valuesUnique_view.append(value)

        actionSortAscending = QtGui.QAction("Ordenar Ascendente", self.tableAssembly_AL)
        actionSortAscending.triggered.connect(self.on_actionSortAscending_triggered_AL)
        self.menuValues.addAction(actionSortAscending)
        actionSortDescending = QtGui.QAction("Ordenar Descendente", self.tableAssembly_AL)
        actionSortDescending.triggered.connect(self.on_actionSortDescending_triggered_AL)
        self.menuValues.addAction(actionSortDescending)
        self.menuValues.addSeparator()

        actionDeleteFilterColumn = QtGui.QAction("Quitar Filtro", self.tableAssembly_AL)
        actionDeleteFilterColumn.triggered.connect(self.on_actionDeleteFilterColumn_triggered_AL)
        self.menuValues.addAction(actionDeleteFilterColumn)
        self.menuValues.addSeparator()

        actionTextFilter = QtGui.QAction("Buscar...", self.tableAssembly_AL)
        actionTextFilter.triggered.connect(self.on_actionTextFilter_triggered_AL)
        self.menuValues.addAction(actionTextFilter)
        self.menuValues.addSeparator()

        scroll_menu = QtWidgets.QScrollArea()
        scroll_menu.setStyleSheet("background-color: rgb(255, 255, 255)")
        scroll_menu.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget(scroll_menu)
        scroll_menu.setWidget(scroll_widget)
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)

        checkbox_all_widget = QtWidgets.QCheckBox('Seleccionar todo')

        if not self.checkbox_states_AL[self.logicalIndex]['Seleccionar todo'] == True:
            checkbox_all_widget.setChecked(False)
        else:
            checkbox_all_widget.setChecked(True)
        
        checkbox_all_widget.toggled.connect(lambda checked, name='Seleccionar todo': self.on_select_all_toggled_AL(checked, name))

        scroll_layout.addWidget(checkbox_all_widget)
        self.action_checkbox_map_AL['Seleccionar todo'] = checkbox_all_widget

        if len(self.dict_ordersort_AL) != 0 and self.logicalIndex in self.dict_ordersort_AL:
            list_uniquevalues = sorted(list(set(self.dict_valuesuniques_AL[self.logicalIndex])))
        else:
            list_uniquevalues = sorted(list(set(valuesUnique_view)))

        for actionName in list_uniquevalues:
            checkbox_widget = QtWidgets.QCheckBox(str(actionName))

            if self.logicalIndex not in self.checkbox_filters_AL:
                checkbox_widget.setChecked(True)
            elif actionName not in self.checkbox_filters_AL[self.logicalIndex]:
                checkbox_widget.setChecked(False)
            else:
                checkbox_widget.setChecked(True)

            checkbox_widget.toggled.connect(lambda checked, name=actionName: self.on_checkbox_toggled_AL(checked, name))

            scroll_layout.addWidget(checkbox_widget)
            self.action_checkbox_map_AL[actionName] = checkbox_widget

        action_scroll_menu = QtWidgets.QWidgetAction(self.menuValues)
        action_scroll_menu.setDefaultWidget(scroll_menu)
        self.menuValues.addAction(action_scroll_menu)

        self.menuValues.addSeparator()

        accept_button = QtGui.QAction("ACEPTAR", self.tableAssembly_AL)
        accept_button.triggered.connect(self.menu_acceptbutton_triggered_AL)

        cancel_button = QtGui.QAction("CANCELAR", self.tableAssembly_AL)
        cancel_button.triggered.connect(self.menu_cancelbutton_triggered)

        self.menuValues.addAction(accept_button)
        self.menuValues.addAction(cancel_button)

        self.menuValues.setStyleSheet("QMenu { color: black; }"
                                        "QMenu { background-color: rgb(255, 255, 255); }"
                                        "QMenu::item:selected { background-color: #33bdef; }"
                                        "QMenu::item:pressed { background-color: rgb(1, 140, 190); }")

        headerPos = self.tableAssembly_AL.mapToGlobal(self.tableAssembly_AL.horizontalHeader().pos())        

        posY = headerPos.y() + self.tableAssembly_AL.horizontalHeader().height()
        scrollX = self.tableAssembly_AL.horizontalScrollBar().value()
        xInView = self.tableAssembly_AL.horizontalHeader().sectionViewportPosition(logicalIndex)
        posX = headerPos.x() + xInView - scrollX

        self.menuValues.exec(QtCore.QPoint(posX, posY))

# Function when accept button of menu is clicked
    def menu_acceptbutton_triggered_AL(self):
        """
        Applies the selected filters and updates the table model with the new filters.
        """
        for column, filters in self.checkbox_filters_AL.items():
            if filters:
                self.proxy_AL.setFilter(filters, column)
            else:
                self.proxy_AL.setFilter(None, column)

# Function when select all checkbox is clicked
    def on_select_all_toggled_AL(self, checked, action_name):
        """
        Toggles the state of all checkboxes in the filter menu when the 'Select All' checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the 'Select All' checkbox.
            action_name (str): The name of the action (usually 'Select All').
        """
        filterColumn = self.logicalIndex
        imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
        icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))

        if checked:
            for checkbox_name, checkbox_widget in self.action_checkbox_map_AL.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states_PA[self.logicalIndex][checkbox_name] = checked

            if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map_AL.values()):
                self.model_AL.setIconColumnHeader(filterColumn, icono)
            else:
                self.model_AL.setIconColumnHeader(filterColumn, '')
        
        else:
            for checkbox_name, checkbox_widget in self.action_checkbox_map_AL.items():
                checkbox_widget.setChecked(checked)
                self.checkbox_states_AL[self.logicalIndex][checkbox_widget.text()] = checked

# Function when checkbox of header menu is clicked
    def on_checkbox_toggled_AL(self, checked, action_name):
        """
        Updates the filter state when an individual checkbox is toggled.
        
        Args:
            checked (bool): The checked state of the checkbox.
            action_name (str): The name of the checkbox.
        """
        filterColumn = self.logicalIndex
        imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
        icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))

        if checked:
            if filterColumn not in self.checkbox_filters_AL:
                self.checkbox_filters_AL[filterColumn] = [action_name]
            else:
                if action_name not in self.checkbox_filters_AL[filterColumn]:
                    self.checkbox_filters_AL[filterColumn].append(action_name)
        else:
            if filterColumn in self.checkbox_filters_AL and action_name in self.checkbox_filters_AL[filterColumn]:
                self.checkbox_filters_AL[filterColumn].remove(action_name)

        if all(checkbox_widget.isChecked() for checkbox_widget in self.action_checkbox_map_AL.values()):
            self.model_AL.setIconColumnHeader(filterColumn, '')
        else:
            self.model_AL.setIconColumnHeader(filterColumn, icono)

# Function to delete individual column filter
    def on_actionDeleteFilterColumn_triggered_AL(self):
        """
        Removes the filter from the selected column and updates the table model.
        """
        filterColumn = self.logicalIndex
        if filterColumn in self.proxy_AL.filters:
            del self.proxy_AL.filters[filterColumn]
        self.model_AL.setIconColumnHeader(filterColumn, '')
        self.proxy_AL.invalidateFilter()

        # self.tableAssembly.setModel(None)
        self.tableAssembly_AL.setModel(self.proxy_AL)

        if filterColumn in self.checkbox_filters_AL:
            del self.checkbox_filters_AL[filterColumn]

        self.checkbox_states_AL[self.logicalIndex].clear()
        self.checkbox_states_AL[self.logicalIndex]['Seleccionar todo'] = True
        for row in range(self.tableAssembly_AL.model().rowCount()):
            value = self.model_AL.record(row).value(filterColumn)
            if isinstance(value, QtCore.QDate):
                    value=value.toString("dd/MM/yyyy")
            self.checkbox_states_AL[self.logicalIndex][str(value)] = True

        self.tableAssembly_AL.setItemDelegate(AlignDelegate(self.tableAssembly_AL))
        self.tableAssembly_AL.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.tableAssembly_AL.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableAssembly_AL.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableAssembly_AL.horizontalHeader().setStyleSheet("::section{font: 800 10pt; background-color: #33bdef; border: 1px solid black;}")

# Function to order column ascending
    def on_actionSortAscending_triggered_AL(self):
        """
        Sorts the selected column in ascending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.AscendingOrder
        self.tableAssembly_AL.sortByColumn(sortColumn, sortOrder)

# Function to order column descending
    def on_actionSortDescending_triggered_AL(self):
        """
        Sorts the selected column in descending order.
        """
        sortColumn = self.logicalIndex
        sortOrder = Qt.SortOrder.DescendingOrder
        self.tableAssembly_AL.sortByColumn(sortColumn, sortOrder)

# Function when text is searched
    def on_actionTextFilter_triggered_AL(self):
        """
        Opens a dialog to enter a text filter and applies it to the selected column.
        """
        filterColumn = self.logicalIndex
        dlg = QtWidgets.QInputDialog()
        new_icon = QtGui.QIcon()
        new_icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlg.setWindowIcon(new_icon)
        dlg.setWindowTitle('Buscar')
        clickedButton=dlg.exec()

        if clickedButton == 1:
            stringAction = dlg.textValue()
            if re.fullmatch(r'^(?:3[01]|[12][0-9]|0?[1-9])([\-/.])(0?[1-9]|1[1-2])\1\d{4}$', stringAction):
                stringAction=QtCore.QDate.fromString(stringAction,"dd/MM/yyyy")
                stringAction=stringAction.toString("yyyy-MM-dd")

            filterString = QtCore.QRegularExpression(stringAction, QtCore.QRegularExpression.PatternOption(0))
            # del self.proxy.filters[filterColumn]
            self.proxy_AL.setFilter([stringAction], filterColumn)

            imagen_path = str(get_path("Resources", "Iconos", "Filter_Active.png"))
            icono = QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage(imagen_path)))
            self.model_AL.setIconColumnHeader(filterColumn, icono)





# Function to show or hide reference number in the table
    def show_ref(self, table, button):
        if table.isColumnHidden(2):
            table.showColumn(2)
            button.setText("Ocultar Nº Ref")
        else:
            table.hideColumn(2)
            button.setText("Ver Nº Ref")


# Function to insert order description in delivery note
    def insert_description(self, table):
        """
        Inserts the description of the selected drawing into the delivery note description field.

        Args:
            table (QtWidgets.QTableView or QtWidgets.QTableWidget): The table from which to get the selected drawing description.
        """
        selection_model = table.selectionModel()

        if not selection_model.hasSelection():
            return

        model = table.model()

        selected_indexes = selection_model.selectedIndexes()
        if len(selected_indexes) == 1:
            # Obtaining first columns values
            item_index = model.index(selected_indexes[0].row(), 20)
            if item_index.isValid():
                description = model.data(item_index)

            dlg = QtWidgets.QInputDialog()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle('Descripción Albarán')
            dlg.setLabelText('Inserte número albarán:')

            while True:
                clickedButton = dlg.exec()
                if clickedButton == 1:
                    delivnote_number = dlg.textValue()
                    if delivnote_number != '':
                        conn = None
                        try:
                        # read the connection parameters
                            params = config_database()
                        # connect to the PostgreSQL server
                            conn = psycopg2.connect(**params)
                            cur = conn.cursor()
                        # execution of commands
                            commands_update = f"""UPDATE purch_fact.invoice_header SET description_dispatch = '{description}' WHERE num_delivnote = '{delivnote_number}'"""
                            cur.execute(commands_update)

                        # close communication with the PostgreSQL database server
                            cur.close()
                        # commit the changes
                            conn.commit()

                            dlg = QtWidgets.QMessageBox()
                            new_icon = QtGui.QIcon()
                            new_icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                            dlg.setWindowIcon(new_icon)
                            dlg.setWindowTitle("Descripción Albarán")
                            dlg.setText("Descripción añadida")
                            dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                            dlg.exec()
                            del dlg,new_icon

                        except (Exception, psycopg2.DatabaseError) as error:
                            dlg = QtWidgets.QMessageBox()
                            new_icon = QtGui.QIcon()
                            new_icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                            dlg.setWindowIcon(new_icon)
                            dlg.setWindowTitle("ERP EIPSA")
                            dlg.setText("Ha ocurrido el siguiente error:\n"
                                        + str(error))
                            dlg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                            dlg.exec()
                            del dlg, new_icon
                        finally:
                            if conn is not None:
                                conn.close()
                        break
                    dlg_error = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(str(get_path("Resources", "Iconos", "icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg_error.setWindowIcon(new_icon)
                    dlg_error.setWindowTitle("Descripción Albarán")
                    dlg_error.setText("El número de albarán no puede estar vacío")
                    dlg_error.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    dlg_error.exec()
                    del dlg_error,new_icon
                else:
                    break



if __name__ == "__main__":
    import sys
    import os

    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    app = QtWidgets.QApplication(sys.argv)
    dbparam = config_database()
    user_database = dbparam["user"]
    password_database = dbparam["password"]

    # Genera un nombre único para la conexión basado en el nombre de usuario y el contador
    db_manufacture = Create_DBconnection(user_database, password_database, 'Assembly_connection')

    if not db_manufacture:
        sys.exit()

    Assembly_window = Ui_Assembly_Window(db_manufacture,'j.sanz')
    Assembly_window.show()
    sys.exit(app.exec())