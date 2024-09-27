from config import config
import os
from PyQt6 import QtGui, QtWidgets
import psycopg2
from datetime import *

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"

def inspection(proxy, model, variable):
    """
    Updates inspection data for specific tags in the database based on the provided variable.

    Args:
        proxy (QAbstractProxyModel): The proxy model containing the current data view.
        model (QAbstractItemModel): The model containing the main data.
        variable (str): A variable that determines the type of inspection to be performed. It can be one of
                        the following values:
                        - 'Caudal'
                        - 'Temperatura'
                        - 'Nivel'
    """
    id_list = []

    for row in range(proxy.rowCount()):
        first_column_value = proxy.data(proxy.index(row, 0))
        id_list.append(first_column_value)

    for element in id_list:
        for row in range(model.rowCount()):
            if model.data(model.index(row, 0)) == element:
                target_row = row
                break
        if target_row is not None:
            if variable == 'Caudal':
                ped_type_tag = model.data(model.index(target_row, 112))
                inspection = model.data(model.index(target_row, 68))
            elif variable == 'Temperatura':
                ped_type_tag = model.data(model.index(target_row, 119))
                inspection = model.data(model.index(target_row, 76))
            elif variable == 'Nivel':
                ped_type_tag = model.data(model.index(target_row, 120))
                inspection = model.data(model.index(target_row, 62))

            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                check_tags = f"SELECT * FROM fabrication.tags WHERE code = '{ped_type_tag}'"
                cur.execute(check_tags)
                results=cur.fetchall()
                if len(results) != 0:
                    update_tags = f"UPDATE fabrication.tags SET inspection = '{inspection}' WHERE code = '{ped_type_tag}'"
                    cur.execute(update_tags)
                else:
                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Inspección")
                    dlg.setText(f"El tag '{ped_type_tag}' no se encuentra resgistrado en la base de fabricación")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    dlg.exec()
                    del dlg, new_icon

                check_tags = f"SELECT * FROM fabrication.tags WHERE code = '{ped_type_tag}'"
                cur.execute(check_tags)
                results=cur.fetchall()
                if len(results) != 0:
                    update_faborder = ("UPDATE fabrication.fab_order SET end_date = %s WHERE tag = %s")
                    data = (date.today().strftime("%d/%m/%Y"), ped_type_tag)
                    cur.execute(update_faborder,data)
                else:
                    dlg = QtWidgets.QMessageBox()
                    new_icon = QtGui.QIcon()
                    new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
                    dlg.setWindowIcon(new_icon)
                    dlg.setWindowTitle("Inspección")
                    dlg.setText(f"El tag '{ped_type_tag}' no se encuentra resgistrado en la base de fabricación")
                    dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    dlg.exec()
                    del dlg, new_icon

        # close communication with the PostgreSQL database server
                cur.close()
            # commit the changes
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                dlg = QtWidgets.QMessageBox()
                new_icon = QtGui.QIcon()
                new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
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