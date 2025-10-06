from PyQt6 import QtSql
from config_keys import HOST_DATABASE, NAME_DATABASE

def createConnection_name(user, password, connection_name):
    """
    Creates a connection to a PostgreSQL database with a specified connection name.

    Args:
        user (str): The username for the database connection.
        password (str): The password for the database connection.
        connection_name (str): The name of the database connection.

    Returns:
        QtSql.QSqlDatabase: The database connection object if successful, None otherwise.
    """
    db=QtSql.QSqlDatabase.addDatabase('QPSQL', connection_name)
    db.setHostName(HOST_DATABASE)
    db.setDatabaseName(NAME_DATABASE)
    db.setUserName(user)
    db.setPassword(password)
    if not db.open():
        print("Error al abrir la base de datos", db.lastError().text())
        return None
    return db

def createConnection(user, password):
    """
    Creates a default connection to a PostgreSQL database without a specific connection name.

    Args:
        user (str): The username for the database connection.
        password (str): The password for the database connection.

    Returns:
        QtSql.QSqlDatabase: The database connection object if successful, None otherwise.
    """
    db=QtSql.QSqlDatabase.addDatabase('QPSQL')
    db.setHostName(HOST_DATABASE)
    db.setDatabaseName(NAME_DATABASE)
    db.setUserName(user)
    db.setPassword(password)
    if not db.open():
        print("Error al abrir la base de datos", db.lastError().text())
        return None
    return db