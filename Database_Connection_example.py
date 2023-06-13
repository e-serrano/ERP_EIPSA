from PyQt6 import QtSql

def createConnection(user,password):
    db=QtSql.QSqlDatabase.addDatabase('driver') #change the value for yor database driver
    db.setHostName('host_number') #change the value for your host number
    db.setDatabaseName('database_name') #change the value for your database name
    db.setUserName(user)
    db.setPassword(password)
    db.open()
    print(db.lastError().text())
    return True