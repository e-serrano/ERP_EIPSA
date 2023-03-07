import sys

import pandas as pd
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView

# código para hacer editable tabla

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableView()

        data = pd.DataFrame(
            [[1, 9, 2], [1, 0, -1], [3, 5, 2], [3, 3, 2], [5, 8, 9],], columns=["A", "B", "C"]
        )

        self.model = PandasModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()


import psycopg2
from config import config
def prueba(self):
    commands = (
                """
                CREATE TABLE ssss (
                    vendor_id SERIAL PRIMARY KEY,
                    vendor_name VARCHAR(255) NOT NULL
                )
                """
                )
    conn = None
    try:
    # read the connection parameters
        params = config()
    # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
    # execution of commands one by one
        #for command in commands:
        cur.execute(commands)
    # close communication with the PostgreSQL database server
        cur.close()
    # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


#Sure, here's an example script that shows how to insert data from an Excel file into a PostgreSQL table using Python:

import pandas as pd
import psycopg2

# Connect to PostgreSQL server
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_username",
    password="your_password",
    port="your_port")

# Load Excel file into a pandas DataFrame
excel_file_path = 'path_to_excel_file.xlsx'
df = pd.read_excel(excel_file_path)

# Create a cursor
cursor = conn.cursor()

# Iterate over each row of the DataFrame and insert into PostgreSQL table
table_name = 'your_table_name'
for index, row in df.iterrows():
    values = tuple(row)
    query = f"INSERT INTO {table_name} VALUES {values}"
    cursor.execute(query)

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()