from config.config_functions import config_database, get_path
import os
from PySide6 import QtGui, QtWidgets
import psycopg2
from datetime import *
from utils.Database_Manager import Database_Connection
from utils.Show_Message import MessageHelper


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

            try:
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        check_tags = f"SELECT * FROM fabrication.tags WHERE code = '{ped_type_tag}'"
                        cur.execute(check_tags)
                        results=cur.fetchall()
                        if len(results) != 0:
                            update_tags = f"UPDATE fabrication.tags SET inspection = '{inspection}' WHERE code = '{ped_type_tag}'"
                            cur.execute(update_tags)
                        else:
                            MessageHelper.show_message(f"El tag '{ped_type_tag}' no se encuentra resgistrado en la base de fabricación", "warning")

                        check_tags = f"SELECT * FROM fabrication.tags WHERE code = '{ped_type_tag}'"
                        cur.execute(check_tags)
                        results=cur.fetchall()
                        if len(results) != 0:
                            update_faborder = ("UPDATE fabrication.fab_order SET end_date = %s WHERE tag = %s")
                            data = (date.today().strftime("%d/%m/%Y"), ped_type_tag)
                            cur.execute(update_faborder,data)
                        else:
                            MessageHelper.show_message(f"El tag '{ped_type_tag}' no se encuentra resgistrado en la base de fabricación", "warning")


                    conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                            + str(error), "critical")