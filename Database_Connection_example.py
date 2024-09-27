from PyQt6 import QtSql

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
    db=QtSql.QSqlDatabase.addDatabase('driver', connection_name) #change the value for yor database driver
    db.setHostName('host_number') #change the value for your host number
    db.setDatabaseName('database_name') #change the value for your database name
    db.setUserName(user)
    db.setPassword(password)
    if not db.open():
        print("Error al abrir la base de datos", db.lastError().text())
        return None
    return db


def createConnection(user,password):
    """
    Creates a default connection to a PostgreSQL database without a specific connection name.

     Args:
        user (str): The username for the database connection.
        password (str): The password for the database connection.

    Returns:
        QtSql.QSqlDatabase: The database connection object if successful, None otherwise.
    """
    db=QtSql.QSqlDatabase.addDatabase('driver') #change the value for yor database driver
    db.setHostName('host_number') #change the value for your host number
    db.setDatabaseName('database_name') #change the value for your database name
    db.setUserName(user)
    db.setPassword(password)
    db.open()
    print(db.lastError().text())
    return True