import psycopg2
import pyodbc
from PyQt6 import QtSql
from config_keys import HOST_DATABASE, NAME_DATABASE

class Access_Connection():
    def __init__(self, access_file, access_pwd):
        self.conn_str = (
                        fr"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};"
                        fr"DBQ={access_file};"
                        fr"PWD={access_pwd};"
                        )
        self.connection = None

    def __enter__(self):
        self.connection = pyodbc.connect(self.conn_str, readonly=True)
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.connection:
            self.connection.close()


class Database_Connection():
    def __init__(self, config):
        self.config = config
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect(**self.config)
        return self.connection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.connection:
            self.connection.close()



def Create_DBconnection(user: str, password: str, connection_name: str = None) -> QtSql.QSqlDatabase | None:
    """
    Creates a connection to a PostgreSQL database, optionally with a specific connection name.

    Args:
        user (str): Database username.
        password (str): Database password.
        connection_name (str, optional): Name for the database connection. Defaults to None.

    Returns:
        QtSql.QSqlDatabase | None: Database connection object if successful, None otherwise.
    """
    db = QtSql.QSqlDatabase.addDatabase('QPSQL', connection_name) if connection_name else QtSql.QSqlDatabase.addDatabase('QPSQL')
    db.setHostName(HOST_DATABASE)
    db.setDatabaseName(NAME_DATABASE)
    db.setUserName(user)
    db.setPassword(password)

    if not db.open():
        print("Error al abrir la base de datos:", db.lastError().text())
        return None

    return db
