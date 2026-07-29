from config.config_functions import config_database, config_sql_engine
import psycopg2
from windows.Excel_Export_Templates import material_order
import pandas as pd
from datetime import *
import PySide6.QtCore
from PySide6.QtWidgets import QFileDialog
import openpyxl
import re
from utils.Database_Manager import Database_Connection
from utils.Show_Message import MessageHelper
from fractions import Fraction


def flow_matorder(proxy, model, numorder, numorder_pedmat, variable, state):
    """
    Processes material raw orders for flow items by inserting new entries into the fabrication orders database.

    Args:
        proxy (QAbstractProxyModel): The proxy model containing the current data view.
        model (QAbstractItemModel): The model containing the main data.
        numorder (str): The order number to process.
        numorder_pedmat (str): The base order number for material orders.
        variable (str): A variable that determines the type of processing to be done. The specific usage
                        of this variable is not detailed in the function.

    Returns:
        None: This function does not return a value but modifies the database state.
    """
    id_list=[]
    orifice_flange_list = []
    line_flange_list = []
    gasket_list = []
    bolts_list = []
    plugs_list = []
    extractor_list = []
    plate_list = []
    nipple_list = []
    handle_list = []
    chring_list = []
    tube_list = []
    piece2_list = []
    bar_handle_list = []

    proxy_data = proxy.data
    proxy_index = proxy.index

    data = model.data
    index = model.index

    if numorder[0] == 'P':
        id_list = [
            proxy_data(proxy_index(row, 0))
            for row in range(proxy.rowCount())
            if proxy_data(proxy_index(row, 2)) == "PURCHASED" and "ZZZ" not in proxy_data(proxy_index(row, 6)).upper()
        ]
    elif numorder[0] == 'O':
        id_list = [
            proxy_data(proxy_index(row, 0))
            for row in range(proxy.rowCount())
            if proxy_data(proxy_index(row, 2)) == "QUOTED" and str(proxy_data(proxy_index(row, 5))) == ''
        ]

    commands_numot = ("""SELECT "ot_num"
                        FROM fabrication.fab_order
                        WHERE NOT "ot_num" LIKE '90%'
                        ORDER BY "ot_num" ASC
                        """)

    check_otpedmat = f"SELECT * FROM fabrication.fab_order WHERE id = '{numorder_pedmat + '-PEDMAT'}'"

    commands_otpedmat = ("""
                            INSERT INTO fabrication.fab_order (
                            "id","tag","element","qty_element",
                            "ot_num","qty_ot","start_date")
                            VALUES (%s,%s,%s,%s,%s,%s,%s)
                            """)

    if state == 'Offer':
        num_ot = '0'
    else:
        try:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(commands_numot)
                    results=cur.fetchall()
                    num_ot=results[-1][0]

            excel_file_path = r"\\ERP-EIPSA-DATOS\Comunes\EIPSA Sistemas de Gestion\MasterCTF\Bases\Contador.xlsm"
            workbook = openpyxl.load_workbook(excel_file_path, keep_vba=True)
            worksheet = workbook.active
            num_ot = worksheet['B2'].value
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(check_otpedmat)
                    results=cur.fetchall()

            if len(results) == 0:
                data_numot=(numorder_pedmat + '-PEDMAT', numorder_pedmat, 'PEDIDO DE MATERIALES', 1, '{:06}'.format(int(num_ot) + 1), len(id_list), date.today().strftime("%d/%m/%Y"))
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(commands_otpedmat, data_numot)
                    conn.commit()

                worksheet['B2'].value = '{:06}'.format(int(num_ot) + 1)
                workbook.save(excel_file_path)

        except (Exception, psycopg2.DatabaseError) as error:
            MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                        + str(error), "critical")

    row_map = {
        data(index(row, 0)): row
        for row in range(model.rowCount())
    }

    for element in id_list:
        row = row_map.get(element)
        if row is None:
            continue

        row_data = [
            data(index(row, c))
            for c in range(model.columnCount())
        ]

        flange_material = row_data[13]
        sch = row_data[12]
        design_flange = str(row_data[65]).replace('.', ',') # pipe internal diameter
        size = f"{row_data[9]} {row_data[10]} {row_data[11]}"
        quantity_equipment = int(row_data[35])

        all_list_parts =[]

        # setting list for eache element [code_element, code_fab_element, trad_element, design_element, process_element, material_element, qty_element, code_purch_element]
        code_orifice_flange = row_data[166]
        if code_orifice_flange:
            orifice_flange_list.append([
                code_orifice_flange,
                row_data[178], # code fab orifice flange
                row_data[202], # trad orifice flange
                sch,
                design_flange,
                "", #row_data[37],
                flange_material,
                int(row_data[190]) * quantity_equipment, # quantity orifice flange per equipment * number of equipments
                row_data[214] # code purch orifice flange
                ])
            all_list_parts.append(orifice_flange_list)

        code_line_flange = row_data[167]
        if code_line_flange:
            line_flange_list.append([
                code_line_flange,
                row_data[179], # code fab line flange
                row_data[203], # trad line flange
                sch,
                design_flange,
                "", #row_data[37],
                flange_material,
                int(row_data[191]) * quantity_equipment, # quantity line flange per equipment * number of equipments
                row_data[215] # code purch line flange
                ])
            all_list_parts.append(line_flange_list)

        code_gasket = row_data[168]
        if code_gasket:
            gasket_list.append([
                code_gasket,
                row_data[180], # code fab gasket
                row_data[204], # trad gasket
                size,
                '',
                '',
                '',
                int(row_data[46]) * quantity_equipment, # quantity gasket per equipment * number of equipments
                row_data[216]]) # code purch gasket
            all_list_parts.append(gasket_list)

        code_bolts = row_data[169]
        if code_bolts:
            bolts_list.append([
                code_bolts,
                row_data[181], # code fab bolts
                row_data[205], # trad bolts
                size,
                ('esp. placa ' + row_data[21]),
                '',
                row_data[24] + " / " + row_data[25],
                (int(row_data[48]) if row_data[48] != '' else 0) * quantity_equipment, # quantity bolts per equipment * number of equipments
                row_data[217]]) # code purch bolts
            all_list_parts.append(bolts_list)

        code_plugs = row_data[170]
        if code_plugs != '':
            plugs_list.append([
                code_plugs,
                row_data[182], # code fab plug
                row_data[206], # trad plug
                '',
                '',
                '',
                row_data[49], # material plug
                (int(row_data[50]) if row_data[50] != '' else 0) * quantity_equipment, # quantity plugs per equipment * quantity of equipment
                row_data[218]
                ])
            all_list_parts.append(plugs_list)

        code_extractor = row_data[171]
        if code_extractor:
            extractor_list.append([
                code_extractor,
                row_data[183], # code fab extractor
                row_data[207], # trad extractor
                size,
                ('esp. placa ' + row_data[21]),
                '',
                row_data[51],
                int(row_data[53]) * quantity_equipment, # quantity extractor per equipment * number of equipments
                row_data[219] # code purch extractor
                ])
            all_list_parts.append(extractor_list)

        code_plate = row_data[172]
        if code_plate:
            plate_list.append([
                code_plate,
                row_data[184], # code fab plate
                row_data[208], # trad plate
                ('ESP ' + row_data[21] + 'mm'),
                row_data[66],
                'ARAMCO' if row_data[22] =='ARA' else '',
                row_data[19],
                int(row_data[28] if row_data[8] == "MULTISTAGE RO" else 1) * quantity_equipment, # quantity of plates per equipment * number of equipments
                row_data[220] # code purch plate
                ])
            all_list_parts.append(plate_list)

        code_nipple = row_data[173]
        if code_nipple:
            nipple_list.append([
                code_nipple,
                row_data[185], # code fab nipple
                row_data[209], # trad nipple
                '',
                '',
                '',
                row_data[13],
                int(row_data[197]) * quantity_equipment, # quantity nipple per equipment * quantity of equipments
                row_data[221] # code purch nipple
                ])
            all_list_parts.append(nipple_list)

        code_handle = row_data[174]
        if code_handle and row_data[21] not in ['3', '1/8" (3)']:
            handle_list.append([
                code_handle,
                row_data[186], # code fab handle
                row_data[210], # trad handle
                '' if row_data[11] == 'RTJ' else (row_data[68] + "x" + row_data[69] + "x" + row_data[70] +' mm'),
                '' if row_data[11] == 'RTJ' else row_data[22],
                '',
                '316SS',
                1 * quantity_equipment, # quantity of handles per equipment * quantity of equipments
                row_data[222] # code purch handle
                ])
            all_list_parts.append(handle_list)

        if code_handle and row_data[21] not in ['3', '1/8" (3)'] and row_data[11] == 'RTJ':
            bar_handle_list.append([
                'Barra Mango RTJ',
                'Barra Mango RTJ',
                'BARRA MANGO',
                '',
                '',
                '',
                '316SS',
                ((int(float(row_data[68])) - 30) if 'datos' not in row_data[68] else 0) * quantity_equipment, # length of bar handle per equipment * quantity of equipments
                ''
                ])
            all_list_parts.append(bar_handle_list)

        code_chring = row_data[175]
        if code_chring:
            chring_list.append([
                code_chring,
                row_data[187], # code fab chring
                row_data[211], # trad chring
                'ESP ' if row_data[11] == "RTJ" else 'ESP 38,5mm ACABADO',
                'ø' + str(row_data[66]),
                '', #row_data[37],
                row_data[19],
                1 * quantity_equipment, # quantity chring per equipment * quantity of equipments
                row_data[223] # code purch chring
                ])
            all_list_parts.append(chring_list)

        code_tube = row_data[176]
        if code_tube:
            tube_list.append([
                code_tube,
                row_data[188], # code fab tube
                row_data[212], # trad tube
                sch,
                design_flange,
                '',
                row_data[15],
                float(row_data[200]) * quantity_equipment, # quantity tube per equipment (length of tube) * quantity of equipments
                row_data[224] # code purch tube
                ])
            all_list_parts.append(tube_list)

        code_piece2 = row_data[177]
        if code_piece2:
            commands_thk = ("""
                SELECT wall_thk
                FROM validation_data.pipe_diam
                WHERE (line_size = %s
                AND
                sch = %s)
                """)

            try:
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(commands_thk,(row_data[9], row_data[12],))
                        results=cur.fetchone()
                        thkmin=results[0]

            except (Exception, psycopg2.DatabaseError) as error:
                MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                            + str(error), "critical")

            commands_flangecode = ("""
                SELECT code
                FROM validation_data.flow_flange_material
                WHERE flange_material = %s
                """)

            commands_sheetmaterial = ("""
                SELECT sheet_material
                FROM validation_data.flow_sheet_material
                WHERE code = %s
                """)

            try:
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(commands_flangecode,(row_data[13],))
                        results=cur.fetchone()
                        code=results[0]

                        cur.execute(commands_sheetmaterial,(code,))
                        results=cur.fetchall()
                        materialpiece2 = results[0]

            except (Exception, psycopg2.DatabaseError) as error:
                MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                            + str(error), "critical")

            piece2_list.append([
                code_piece2,
                row_data[189], # code fab wedge
                row_data[213], # trad wedge
                ('Th mín ' + thkmin + 'mm'),
                '',
                '',
                materialpiece2,
                1 * quantity_equipment, # quantity of wedge parts per equipment * quantity of equipments
                row_data[225] # code purch wedge
                ])
            all_list_parts.append(piece2_list)

        if state == 'Order':
            columns_equipments = ["code_equipment", "code_fab_equipment", "translate_equipment", "section_type",
                                "f_orifice_flange", "qty_f_orifice_flange", "f_line_flange", "qty_f_line_flange",
                                "f_gasket", "qty_f_gasket", "f_bolts", "qty_f_bolts",
                                "f_plug", "qty_f_plug", "f_extractor", "qty_f_extractor",
                                "f_plate", "qty_f_plate", "f_nipple", "qty_f_nipple",
                                "f_handle", "qty_f_handle", "f_chring", "qty_f_chring",
                                "f_tube", "qty_f_tube", "f_piece2", "qty_f_piece2"]
            columns_parts = ["code_part", "code_fab_part", "code_element", "model", "design", "process", "material", "section_type"]
            columns_tags = ["code", "equipment", "num_order","order_material","contractual_date","inspection"]

            values_equipments = [row_data[163], row_data[164], row_data[165], "Q-CAUD",
                                row_data[166], row_data[190], row_data[167], row_data[191],
                                row_data[168], row_data[192], row_data[169], row_data[193],
                                row_data[170], row_data[194], row_data[171], row_data[195],
                                row_data[172], row_data[196], row_data[173], row_data[197],
                                row_data[174], row_data[198], row_data[175], row_data[199],
                                row_data[176], row_data[200], row_data[177], row_data[201]]

            values_tags = [row_data[4] + "-" + row_data[8] + "-" + row_data[1], 
                            row_data[163], row_data[4], row_data[98],
                            row_data[43], row_data[145]]

            columns_equipments  = ", ".join([f'"{column}"' for column in columns_equipments])
            values_equipments =  ", ".join(['NULL' if value == '' or value == 0 else
                                            (str(value) if isinstance(value, (int, float)) else
                                            f"'{str(value)}'")
                                            for value in values_equipments])

            columns_tags  = ", ".join([f'"{column}"' for column in columns_tags])
            values_tags =  ", ".join(['NULL' if value == '' or value == PySide6.QtCore.QDate() else 
                                    (str(value) if isinstance(value, (int, float)) else 
                                    (f"'{value.toString('yyyy-MM-dd')}'" if isinstance(value, PySide6.QtCore.QDate) else 
                                    f"'{str(value)}'"))
                                    for value in values_tags])

            columns_parts = ", ".join([f'"{column}"' for column in columns_parts])

            commands_equipments = f"INSERT INTO fabrication.equipments ({columns_equipments}) VALUES ({values_equipments})"
            commands_tags = f"INSERT INTO fabrication.tags ({columns_tags}) VALUES ({values_tags})"

            check_equipments = f"SELECT * FROM fabrication.equipments WHERE code_equipment = '{row_data[163]}'"

            try:
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(check_equipments)
                        results=cur.fetchall()

                if len(results) == 0:
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(commands_equipments)
                        conn.commit()

                else:
                    set_clause = ", ".join([f"{column} = {value}" for column, value in zip(columns_equipments.split(", ")[1:], values_equipments.split(", ")[1:])])
                    update_equipments = f"UPDATE fabrication.equipments SET {set_clause} WHERE code_equipment = '{row_data[163]}'"
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(update_equipments)
                        conn.commit()

                for list_part in all_list_parts:
                    check_parts = f"SELECT * FROM fabrication.parts WHERE code_part = '{list_part[0][0]}'"
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(check_parts)
                            results=cur.fetchall()

                    if len(results) == 0:
                        list_part_modified = list_part[0][:8].copy()
                        list_part_modified[-1] = 'Q-CAUD'
                        values_parts = ", ".join('NULL' if value == '' else (str(value) if isinstance(value, (int, float)) else f"'{str(value)}'") for value in list_part_modified)
                        commands_parts = f"INSERT INTO fabrication.parts ({columns_parts}) VALUES ({values_parts})"
                        with Database_Connection(config_database()) as conn:
                            with conn.cursor() as cur:
                                cur.execute(commands_parts)
                            conn.commit()

                    else:
                        list_part_modified = list_part[0][:8].copy()
                        list_part_modified[-1] = 'Q-CAUD'
                        values_parts = ", ".join('NULL' if value == '' else (str(value) if isinstance(value, (int, float)) else f"'{str(value)}'") for value in list_part_modified)
                        set_clause = ", ".join([f"{column} = {value}" for column, value in zip(columns_parts.split(", ")[1:], values_parts.split(", ")[1:])])
                        update_parts = f"UPDATE fabrication.parts SET {set_clause} WHERE code_part = '{list_part[0][0]}'"
                        with Database_Connection(config_database()) as conn:
                            with conn.cursor() as cur:
                                cur.execute(update_parts)
                            conn.commit()

                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(commands_tags)
                    conn.commit()

            except (Exception, psycopg2.DatabaseError) as error:
                MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                            + str(error), "critical")

# Turn all lists in dataframe and grouped in order to sum same items
    data_lists = [
    (orifice_flange_list, "df_orifice_flange"),
    (line_flange_list, "df_line_flange"),
    (gasket_list, "df_gasket"),
    (bolts_list, "df_bolts"),
    (plugs_list, "df_plugs"),
    (extractor_list, "df_extractor"),
    (plate_list, "df_plate"),
    (nipple_list, "df_nipple"),
    (handle_list, "df_handle"),
    (chring_list, "df_chring"),
    (tube_list, "df_tube"),
    (piece2_list, "df_piece2"),
    (bar_handle_list, "df_bar_handle")]

    data_frames_with_data = []

    for data_list, df_name in data_lists:
        if data_list:
            sublists = [sublist[2:] for sublist in data_list]
            df = pd.DataFrame(sublists, columns=['descripción', 'modelo', 'diseño', 'proceso', 'material', 'cantidad', 'suministro'])
            df = df.groupby(['descripción', 'modelo', 'diseño', 'proceso', 'material', 'suministro'])['cantidad'].sum().reset_index()
            data_frames_with_data.append(df)

    if data_frames_with_data:
        df_final = pd.concat(data_frames_with_data, ignore_index=True)

        values_supplies = df_final['suministro'].dropna().unique().tolist()

        query = """
        SELECT reference AS suministro, physical_stock AS st_fisico, available_stock AS st_disponible, pending_stock as st_pend, virtual_stock AS st_virtual
        FROM purch_fact.supplies
        WHERE reference IN %(values)s
        """

        with Database_Connection(config_database()) as conn:
            df_supplies = pd.read_sql(query, config_sql_engine(), params={"values": tuple(values_supplies)})

        df_final = (df_final.merge(df_supplies, on='suministro', how='left')
                    [['descripción', 'modelo', 'diseño', 'proceso', 'material', 'cantidad', 'suministro',
                        'st_fisico', 'st_disponible', 'st_pend', 'st_virtual']])

        df_final['almacen_si'] = ''
        df_final['almacen_no'] = ''
        df_final['proveedor'] = ''
        df_final['fecha_pedido'] = ''
        df_final['fecha_prevista'] = ''

        df_final = df_final[
            ['descripción', 'modelo', 'diseño', 'proceso', 'material',
            'cantidad', 'almacen_si', 'almacen_no', 'suministro',
            'proveedor', 'fecha_pedido', 'fecha_prevista',
            'st_fisico', 'st_disponible', 'st_pend', 'st_virtual']
        ]

    commands_client_order = ("""
                SELECT orders."num_order",orders."num_offer",offers."client"
                FROM offers
                INNER JOIN orders ON (offers."num_offer"=orders."num_offer")
                WHERE UPPER(orders."num_order") LIKE UPPER('%%'||%s||'%%')
                """)

    commands_client_offer = ("""
                SELECT offers."num_offer",offers."client"
                FROM offers
                WHERE UPPER(offers."num_offer") LIKE UPPER('%%'||%s||'%%')
                """)

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                if state == 'Order':
                    cur.execute(commands_client_order,(numorder,))
                    results=cur.fetchone()
                    client=results[2]
                else:
                    cur.execute(commands_client_offer,(numorder,))
                    results=cur.fetchone()
                    client=results[1]

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    excel_mat_order = material_order(df_final, numorder_pedmat, client, variable, num_ot)
    excel_mat_order.save_excel()


def temp_matorder(proxy, model, numorder, numorder_pedmat, variable, state):
    """
    Processes material raw orders for temp items by inserting new entries into the fabrication orders database.

    Args:
        proxy (QAbstractProxyModel): The proxy model containing the current data view.
        model (QAbstractItemModel): The model containing the main data.
        numorder (str): The order number to process.
        numorder_pedmat (str): The base order number for material orders.
        variable (str): A variable that determines the type of processing to be done. The specific usage
                        of this variable is not detailed in the function.

    Returns:
        None: This function does not return a value but modifies the database state.
    """
    id_list=[]
    bar_list = []
    tube_list = []
    flange_list = []
    sensor_list = []
    head_list = []
    btb_list = []
    nipple_list = []
    spring_list = []
    plug_list = []
    puntal_list = []
    tw_list = []
    extcable_list = []

    proxy_data = proxy.data
    proxy_index = proxy.index

    data = model.data
    index = model.index

    if numorder[0] == 'P':
        id_list = [
            proxy_data(proxy_index(row, 0))
            for row in range(proxy.rowCount())
            if proxy_data(proxy_index(row, 2)) == "PURCHASED" and "ZZZ" not in proxy_data(proxy_index(row, 6)).upper()
        ]
    elif numorder[0] == 'O':
        id_list = [
            proxy_data(proxy_index(row, 0))
            for row in range(proxy.rowCount())
            if proxy_data(proxy_index(row, 2)) == "QUOTED" and str(proxy_data(proxy_index(row, 5))) == ''
        ]

    commands_numot = ("""SELECT "ot_num"
                        FROM fabrication.fab_order
                        WHERE NOT "ot_num" LIKE '90%'
                        ORDER BY "ot_num" ASC
                        """)

    check_otpedmat = f"SELECT * FROM fabrication.fab_order WHERE id = '{numorder_pedmat + '-PEDMAT'}'"

    commands_otpedmat = ("""
                            INSERT INTO fabrication.fab_order (
                            "id","tag","element","qty_element",
                            "ot_num","qty_ot","start_date")
                            VALUES (%s,%s,%s,%s,%s,%s,%s)
                            """)

    if state == 'Offer':
        num_ot = '0'
    else:
        try:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(commands_numot)
                    results=cur.fetchall()
                    num_ot=results[-1][0]

            excel_file_path = r"\\ERP-EIPSA-DATOS\Comunes\EIPSA Sistemas de Gestion\MasterCTF\Bases\Contador.xlsm"
            workbook = openpyxl.load_workbook(excel_file_path, keep_vba=True)
            worksheet = workbook.active
            num_ot = worksheet['B2'].value

            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(check_otpedmat)
                    results=cur.fetchall()

            if len(results) == 0:
                data_numot=(numorder_pedmat + '-PEDMAT', numorder_pedmat, 'PEDIDO DE MATERIALES', 1, '{:06}'.format(int(num_ot) + 1), len(id_list), date.today().strftime("%d/%m/%Y"))
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(commands_otpedmat, data_numot)
                    conn.commit()

                worksheet['B2'].value = '{:06}'.format(int(num_ot) + 1)
                workbook.save(excel_file_path)

        except (Exception, psycopg2.DatabaseError) as error:
            MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                        + str(error), "critical")

    row_map = {
        data(index(row, 0)): row
        for row in range(model.rowCount())
    }

    for element in id_list:
        row = row_map.get(element)
        if row is None:
            continue

        row_data = [
            data(index(row, c))
            for c in range(model.columnCount())
        ]

        all_list_parts =[]

        tw_type = row_data[9]
        quantity_equipment = int(row_data[42])

        # setting list for eache element [code_element, code_fab_element, trad_element, design_elemente, process_element, material_element, qty_element, code_purch_element]
        code_bar = row_data[147]
        if code_bar:
            bar_list.append([
                code_bar,
                row_data[159],
                row_data[183] if 'Helical' not in tw_type else
                    'VAINA HELICOIDAL' + (' BRIDADA ' + row_data[10] + ' ' + row_data[11] + ' ' + row_data[12] if tw_type == 'Flanged Helical' else ''),
                ('U=' + row_data[16] + ' /L=' + row_data[15] if 'Stone' in tw_type or 'Helical' in tw_type
                        else 'Barra ø=' + (row_data[57])),
                ('RAÍZ ø=' + row_data[17]) if tw_type == 'Van-Stone TW' else '',
                '',
                row_data[14],
                (float(row_data[171]) if 'Helical' not in tw_type else 1) * quantity_equipment,
                row_data[195]
                ])
            all_list_parts.append(bar_list)

        code_tube = row_data[148]
        if code_tube:
            tube_list.append([
                code_tube,
                row_data[160],
                row_data[184],
                row_data[38],
                '',
                '',
                row_data[14],
                float(row_data[172] * quantity_equipment),
                row_data[196]
                ])
            all_list_parts.append(tube_list)

        code_flange = row_data[149]
        if code_flange:
            tw_types_list = ['Buttweld TW','Forged Flanged TW','Threaded Helical','Van-Stone Helical','VORTICRACK']
            flange_list.append([
                code_flange,
                row_data[161],
                row_data[185] if tw_type not in tw_types_list else '',
                '',
                '',
                '',
                (row_data[35] if tw_type == 'Van-Stone TW' else (row_data[14] if tw_type not in tw_types_list else '')),
                (1 if tw_type not in tw_types_list else 0) * quantity_equipment,
                row_data[197]
                ])
            all_list_parts.append(flange_list)

        code_sensor = row_data[150]
        if code_sensor:
            sensor_list.append([
                code_sensor,
                row_data[162],
                row_data[186],
                (row_data[33] + '-' + row_data[32]) if code_sensor[:4] == 'Bime' else '',
                (row_data[27] + '-' + row_data[28]) if code_sensor[:4] == 'Bime' else '',
                '',
                'PLATINO' if row_data[186][:5] == 'PT100' else ('AC. INOX.' if row_data[24] == 'St.Steel' else row_data[24]),
                (1 if (row_data[186][:5] == 'PT100' or code_sensor[:4] == 'Bime') else ((float(row_data[63])/1000) if row_data[63] != '' else 0)) * quantity_equipment,
                row_data[198]
                ])
            all_list_parts.append(sensor_list)

        code_head = row_data[151]
        if code_head:
            head_list.append([
                code_head,
                row_data[163],
                row_data[187],
                row_data[31],
                '',
                row_data[33],
                ('ALUMINIO' if row_data[31][-2:] == 'AL' 
                    else ('AC.CARBONO' if row_data[31][-2:] == 'CS' 
                    else ('AC.INOXIDABLE' if row_data[31][-2:] == 'SS' 
                    else 'MATERIAL CABEZA NO DEFINIDO'))),
                1 * quantity_equipment,
                row_data[198]
                ])
            all_list_parts.append(head_list)

        code_btb = row_data[152]
        if code_btb:
            btb_list.append([
                code_btb,
                row_data[164],
                row_data[188],
                ("RANGO " + row_data[27] + '-' + row_data[28]) if code_btb[:2] == 'BI' else '',
                '',
                '',
                row_data[24] if code_btb[:2] == 'BI' else ('CERÁMICO' if code_btb[:2] == 'CE' else ''),
                float(row_data[176]) * quantity_equipment,
                row_data[200]
                ])
            all_list_parts.append(btb_list)

        code_nipple = row_data[153]
        if code_nipple:
            nipple_list.append([
                code_nipple,
                row_data[165],
                row_data[189],
                ('' if row_data[30] == 'N/A' or row_data[30]=='' else row_data[30]),
                '',
                '',
                'A-105/A106' if row_data[189][row_data[189].find('('):row_data[189].find('(')+9] == '(CS)' else 'AISI-316',
                1 * quantity_equipment,
                row_data[201]
                ])
            all_list_parts.append(nipple_list)

        code_spring = row_data[154]
        if code_spring:
            spring_list.append([
                code_spring,
                row_data[166],
                row_data[190],
                '',
                '',
                '',
                'AC.INOX',
                1 * quantity_equipment,
                row_data[202]
                ])
            all_list_parts.append(spring_list)

        code_puntal = row_data[155]
        if code_puntal:
            puntal_list.append([
                code_puntal,
                row_data[167],
                row_data[191],
                '',
                '',
                '',
                row_data[14],
                float(code_puntal[1:8])/1000 * quantity_equipment,
                row_data[203]
                ])
            all_list_parts.append(puntal_list)

        code_plug = row_data[156]
        if code_plug:
            plug_list.append([
                code_plug,
                row_data[168],
                row_data[192],
                '',
                '',
                '',
                row_data[192][row_data[192].find('('):row_data[192].find('(')+9],
                1 * quantity_equipment,
                row_data[204]
                ])
            all_list_parts.append(plug_list)

        code_tw = row_data[157]
        if code_tw and ('Van-Stone TW' in tw_type or 'Forged' in tw_type or 'VORTICRACK' in tw_type):
            tw_list.append([
                code_tw,
                row_data[169],
                row_data[193],
                'U=' + row_data[16] + ' / L=' + row_data[15],
                '',
                '',
                row_data[14],
                float(row_data[181]) * quantity_equipment,
                row_data[205]
                ])
            all_list_parts.append(tw_list)

        code_extcable = row_data[158]
        if code_extcable != '':
            extcable_list.append([
                code_extcable,
                row_data[170],
                row_data[194],
                '',
                '',
                '',
                'AC. INOX.' if row_data[24] in ['AISI-304', 'AISI-310', 'AISI-316', 'AISI-321', 'St.Steel'] else row_data[24],
                (float(row_data[182]) if row_data[182] != '' else 0) * quantity_equipment,
                row_data[206]
                ])
            all_list_parts.append(extcable_list)

        if state == 'Order':
            columns_equipments = ["code_equipment", "code_fab_equipment", "translate_equipment", "section_type",
                                        "t_bar", "qty_t_bar", "t_tube", "qty_t_tube",
                                        "t_flange", "qty_t_flange", "t_sensor", "qty_t_sensor",
                                        "t_head", "qty_t_head", "t_btb", "qty_t_btb",
                                        "t_nippleextcomp", "qty_t_nippleextcomp", "t_spring", "qty_t_spring",
                                        "t_puntal", "qty_t_puntal", "t_plug", "qty_t_plug",
                                        "t_tw", "qty_t_tw", "t_extcable", "qty_t_extcable"]

            columns_parts = ["code_part", "code_fab_part", "code_element", "model", "design", "process", "material", "section_type"]
            columns_tags = ["code", "equipment", "num_order", "order_material", "contractual_date", "inspection"]

            values_equipments = [row_data[144], row_data[145], row_data[146], "T-TEMP",
                                row_data[147], row_data[171], row_data[148], row_data[172],
                                row_data[149], row_data[173], row_data[150], row_data[174],
                                row_data[151], row_data[175], row_data[152], row_data[176],
                                row_data[153], row_data[177], row_data[154], row_data[178],
                                row_data[155], row_data[179], row_data[156], row_data[180],
                                row_data[157], row_data[181], row_data[158], row_data[182]]

            values_tags = [row_data[4] + "-" + row_data[8] + "-" + row_data[1], 
                            row_data[144], row_data[4], row_data[70],
                            row_data[50], row_data[122]]

            columns_equipments  = ", ".join([f'"{column}"' for column in columns_equipments])
            values_equipments =  ", ".join(['NULL' if value == '' or value == 0 else
                                            (str(value) if isinstance(value, (int, float)) else
                                            f"'{str(value)}'")
                                            for value in values_equipments])

            columns_tags  = ", ".join([f'"{column}"' for column in columns_tags])
            values_tags =  ", ".join(['NULL' if value == '' or value == PySide6.QtCore.QDate() else
                                        (str(value) if isinstance(value, (int, float)) else
                                        (f"'{value.toString('yyyy-MM-dd')}'" if isinstance(value, PySide6.QtCore.QDate)
                                        else f"'{str(value)}'"))
                                        for value in values_tags])

            columns_parts = ", ".join([f'"{column}"' for column in columns_parts])

            commands_equipments = f"INSERT INTO fabrication.equipments ({columns_equipments}) VALUES ({values_equipments})"
            commands_tags = f"INSERT INTO fabrication.tags ({columns_tags}) VALUES ({values_tags})"

            check_equipments = f"SELECT * FROM fabrication.equipments WHERE code_equipment = '{row_data[144]}'"
            try:
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(check_equipments)
                        results=cur.fetchall()

                if len(results) == 0:
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(commands_equipments)
                        conn.commit()

                else:
                    set_clause = ", ".join([f"{column} = {value}" for column, value in zip(columns_equipments.split(", ")[1:], values_equipments.split(", ")[1:])])
                    update_equipments = f"UPDATE fabrication.equipments SET {set_clause} WHERE code_equipment = '{row_data[144]}'"
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(update_equipments)
                        conn.commit()

                for list_part in all_list_parts:
                    check_parts = f"SELECT * FROM fabrication.parts WHERE code_part = '{list_part[0][0]}'"
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(check_parts)
                            results=cur.fetchall()

                    if len(results) == 0:
                        list_part_modified = list_part[0][:8].copy()
                        list_part_modified[-1] = 'T-TEMP'
                        values_parts = ", ".join('NULL' if value == '' else (str(value) if isinstance(value, (int, float)) else f"'{str(value)}'") for value in list_part_modified)
                        commands_parts = f"INSERT INTO fabrication.parts ({columns_parts}) VALUES ({values_parts})"
                        with Database_Connection(config_database()) as conn:
                            with conn.cursor() as cur:
                                cur.execute(commands_parts)
                            conn.commit()
                    else:
                        list_part_modified = list_part[0][:8].copy()
                        list_part_modified[-1] = 'T-TEMP'
                        values_parts = ", ".join('NULL' if value == '' else (str(value) if isinstance(value, (int, float)) else f"'{str(value)}'") for value in list_part_modified)
                        set_clause = ", ".join([f"{column} = {value}" for column, value in zip(columns_parts.split(", ")[1:], values_parts.split(", ")[1:])])
                        update_parts = f"UPDATE fabrication.parts SET {set_clause} WHERE code_part = '{list_part[0][0]}'"
                        with Database_Connection(config_database()) as conn:
                            with conn.cursor() as cur:
                                cur.execute(update_parts)
                            conn.commit()

                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(commands_tags)
                    conn.commit()

            except (Exception, psycopg2.DatabaseError) as error:
                MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                            + str(error), "critical")

# Turn all lists in dataframe and grouped in order to sum same items
    data_lists = [
    (bar_list, "df_bar"),
    (tube_list, "df_tube"),
    (flange_list, "df_flange"),
    (sensor_list, "df_sensor"),
    (head_list, "df_head"),
    (btb_list, "df_btb"),
    (nipple_list, "df_nipple"),
    (spring_list, "df_spring"),
    (plug_list, "df_plug"),
    (puntal_list, "df_puntal"),
    (extcable_list, "df_extcable"),
    (tw_list, "df_tw")]

    data_frames_with_data = []

    for data_list, df_name in data_lists:
        if data_list:
            sublists = [sublist[2:] for sublist in data_list]
            df = pd.DataFrame(sublists, columns=['descripción', 'modelo', 'diseño', 'proceso', 'material', 'cantidad', 'suministro'])
            df = df.groupby(['descripción', 'modelo', 'diseño', 'proceso', 'material', 'suministro'])['cantidad'].sum().reset_index()
            data_frames_with_data.append(df)

    if data_frames_with_data:
        df_final = pd.concat(data_frames_with_data, ignore_index=True)

        values_supplies = df_final['suministro'].dropna().unique().tolist()

        query = """
        SELECT reference AS suministro, physical_stock AS st_fisico, available_stock AS st_disponible, pending_stock as st_pend, virtual_stock AS st_virtual
        FROM purch_fact.supplies
        WHERE reference IN %(values)s
        """

        with Database_Connection(config_database()) as conn:
            df_supplies = pd.read_sql(query, config_sql_engine(), params={"values": tuple(values_supplies)})

        df_final = (df_final.merge(df_supplies, on='suministro', how='left')
                    [['descripción', 'modelo', 'diseño', 'proceso', 'material', 'cantidad', 'suministro',
                        'st_fisico', 'st_disponible', 'st_pend', 'st_virtual']])

        df_final['almacen_si'] = ''
        df_final['almacen_no'] = ''
        df_final['proveedor'] = ''
        df_final['fecha_pedido'] = ''
        df_final['fecha_prevista'] = ''

        df_final = df_final[
            ['descripción', 'modelo', 'diseño', 'proceso', 'material',
            'cantidad', 'almacen_si', 'almacen_no', 'suministro',
            'proveedor', 'fecha_pedido', 'fecha_prevista',
            'st_fisico', 'st_disponible', 'st_pend', 'st_virtual']
        ]

    commands_client_order = ("""
                SELECT orders."num_order",orders."num_offer",offers."client"
                FROM offers
                INNER JOIN orders ON (offers."num_offer"=orders."num_offer")
                WHERE UPPER(orders."num_order") LIKE UPPER('%%'||%s||'%%')
                """)

    commands_client_offer = ("""
                SELECT offers."num_offer",offers."client"
                FROM offers
                WHERE UPPER(offers."num_offer") LIKE UPPER('%%'||%s||'%%')
                """)

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                if state == 'Order':
                    cur.execute(commands_client_order,(numorder,))
                    results=cur.fetchone()
                    client=results[2]
                else:
                    cur.execute(commands_client_offer,(numorder,))
                    results=cur.fetchone()
                    client=results[1]

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    excel_mat_order = material_order(df_final, numorder_pedmat, client, variable, num_ot)
    excel_mat_order.save_excel()


def level_matorder(proxy, model, numorder, numorder_pedmat, variable, state):
    """
    Processes material raw orders for level items by inserting new entries into the fabrication orders database.

    Args:
        proxy (QAbstractProxyModel): The proxy model containing the current data view.
        model (QAbstractItemModel): The model containing the main data.
        numorder (str): The order number to process.
        numorder_pedmat (str): The base order number for material orders.
        variable (str): A variable that determines the type of processing to be done. The specific usage
                        of this variable is not detailed in the function.

    Returns:
        None: This function does not return a value but modifies the database state.
    """
    def expand_illuminators_from_list(illuminator_list):
        """
        Expand combinations like '1 x 1-I 218-T + 2 x 1-I 228-T'
        mantaining fields and original structure.
        """
        rows = []
        for item in illuminator_list:
            code_ill, codefab_ill, tradcod, model, design, process, material, qty = item

            parts = [p.strip() for p in str(tradcod).split("+")]
            for p in parts:
                match = re.match(r"(\d+)\s*x\s*(1-I\s*\d+-T)", p)
                if match:
                    quantity = int(match.group(1)) * qty
                    illuminator = "ILUMINADOR " + match.group(2).replace(" ", "")
                    supply = "ILUMINADOR"
                    rows.append([
                        code_ill, codefab_ill, illuminator, model, design, process, material, quantity, supply
                    ])
        return rows

    id_list = []
    body_list = []
    cover_list = []
    glass_list = []
    gasket_list = []
    mica_list = []
    bolts_list = []
    nipplehex_list = []
    valve_list = []
    flangevalve_list = []
    nippletube_list = []
    dv_list = []
    plug_list = []
    antifrost_list = []
    illuminator_list = []

    proxy_data = proxy.data
    proxy_index = proxy.index

    data = model.data
    index = model.index

    if numorder[0] == 'P':
        id_list = [
            proxy_data(proxy_index(row, 0))
            for row in range(proxy.rowCount())
            if proxy_data(proxy_index(row, 2)) == "PURCHASED" and "ZZZ" not in proxy_data(proxy_index(row, 6)).upper()
        ]
    elif numorder[0] == 'O':
        id_list = [
            proxy_data(proxy_index(row, 0))
            for row in range(proxy.rowCount())
            if proxy_data(proxy_index(row, 2)) == "QUOTED" and str(proxy_data(proxy_index(row, 5))) == ''
        ]

    commands_numot = ("""SELECT "ot_num"
                        FROM fabrication.fab_order
                        WHERE NOT "ot_num" LIKE '90%'
                        ORDER BY "ot_num" ASC
                        """)

    check_otpedmat = f"SELECT * FROM fabrication.fab_order WHERE id = '{numorder_pedmat + '-PEDMAT'}'"

    commands_otpedmat = ("""
                            INSERT INTO fabrication.fab_order (
                            "id","tag","element","qty_element",
                            "ot_num","qty_ot","start_date")
                            VALUES (%s,%s,%s,%s,%s,%s,%s)
                            """)

    if state == 'Offer':
        num_ot = '0'
    else:
        try:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(commands_numot)
                    results=cur.fetchall()
                    num_ot=results[-1][0]

            excel_file_path = r"\\ERP-EIPSA-DATOS\Comunes\EIPSA Sistemas de Gestion\MasterCTF\Bases\Contador.xlsm"
            workbook = openpyxl.load_workbook(excel_file_path, keep_vba=True)
            worksheet = workbook.active
            num_ot = worksheet['B2'].value

            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(check_otpedmat)
                    results=cur.fetchall()

            if len(results) == 0:
                data_numot=(numorder_pedmat + '-PEDMAT', numorder_pedmat, 'PEDIDO DE MATERIALES', 1, '{:06}'.format(int(num_ot) + 1), len(id_list), date.today().strftime("%d/%m/%Y"))
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(commands_otpedmat, data_numot)
                    conn.commit()

                worksheet['B2'].value = '{:06}'.format(int(num_ot) + 1)
                workbook.save(excel_file_path)

        except (Exception, psycopg2.DatabaseError) as error:
            MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                        + str(error), "critical")

    row_map = {
        data(index(row, 0)): row
        for row in range(model.rowCount())
    }

    for element in id_list:
        row = row_map.get(element)
        if row is None:
            continue

        row_data = [
            data(index(row, c))
            for c in range(model.columnCount())
        ]

        code_scale = row_data[94]
        code_fab_scale = row_data[95]

        code_float = row_data[106]
        codefab_float = row_data[107]

        all_list_parts = []

        model_num = row_data[9]
        model_value = model_num[:6] if model_num[2:4] !='HH' else model_num[:7]
        level_type = row_data[8]
        conn_type = row_data[15]
        nipplehexdim = row_data[32][:8]
        nippletubedim = row_data[33][:8]
        cc_length = int(row_data[17])

        # setting list for eache element [code_element, code_fab_element, trad_element, design_elemente, process_element, material_element, qty_element, code_purch_element]
        code_body = row_data[73]
        if code_body:
            body_list.append([
                code_body,
                row_data[74],
                row_data[125],
                nipplehexdim,
                '40x40' if model_value[2:3] != 'H' else ('100x50'if model_value[2:4] != 'HH' else '80x40'),
                (nipplehexdim + '-M'),
                'A-105' if row_data[10] == 'Carbon Steel' else row_data[10],
                row_data[75],
                row_data[185]
                ])
            all_list_parts.append(body_list)

        code_cover = row_data[76]
        if code_cover:
            commands_coverdim = ("""
                SELECT *
                FROM validation_data.level_cover_dim
                WHERE cover = %s
                """)

            try:
                cover_num = model_value[2:6] if model_value[2:4] !='HH' else model_value[3:7]
                cover_num = cover_num[:2] + '1' + cover_num[3:]
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(commands_coverdim,(cover_num,))
                        results=cur.fetchone()
                        length=results[1]
                        bores=results[2]

            except (Exception, psycopg2.DatabaseError) as error:
                MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                            + str(error), "critical")

            cover_list.append([
                code_cover,
                row_data[77],
                row_data[126],
                ('L=' + str(length)),
                '80x30' if model_value[2:4] != 'HH' else '90x40',
                (str(bores) + ' taladros'),
                'A-105' if row_data[27] == 'Carbon Steel' else row_data[27],
                row_data[78],
                row_data[186]
                ])
            all_list_parts.append(cover_list)

        code_glass = row_data[103]
        if code_glass:
            glass_list.append([
                code_glass,
                row_data[104],
                row_data[135],
                'TRANSPARENCIA' if level_type == 'Transparent' else 'REFLEXIÓN',
                '',
                '',
                'BOROSILICATO',
                row_data[105],
                row_data[195]
                ])
            all_list_parts.append(glass_list)

        code_gasket = row_data[100]
        if code_gasket:
            gasket_list.append([
                code_gasket,
                row_data[101],
                row_data[134],
                'TRANSPARENCIA' if level_type == 'Transparent' else 'REFLEXIÓN',
                '',
                '',
                'GRAFOIL',
                row_data[102],
                row_data[194]
                ])
            all_list_parts.append(gasket_list)

        code_mica = row_data[109]
        if code_mica:
            mica_list.append([
                code_mica,
                row_data[110],
                row_data[137],
                'TRANSPARENCIA',
                '',
                '',
                'MICA',
                row_data[111],
                row_data[197]
                ])
            all_list_parts.append(mica_list)

        code_bolts = row_data[79]
        if code_bolts:
            bolts_list.append([
                code_bolts,
                row_data[80],
                row_data[127],
                'TRANSPARENCIA' if level_type == 'Transparent' else 'REFLEXIÓN',
                '' if model_value[2:4] == 'HH' else ('M10x132 mm' if level_type == 'Transparent' else ''),
                '' if model_value[2:4] == 'HH' else ('cabeza exag 17 e/c' if level_type == 'Transparent' else ''),
                'B7/2H' if level_type in ['Transparent','Reflex'] else row_data[24],
                row_data[81],
                row_data[187]
                ])
            all_list_parts.append(bolts_list)

        code_nipplehex = row_data[82]
        if code_nipplehex:
            nipplehex_list.append([
                code_nipplehex,
                row_data[83],
                row_data[128],
                (str((cc_length-int(get_number_before_mm(row_data[125]))-72)/2+22) + ' mm'),
                '',
                '',
                'A-105' if row_data[10] == 'Carbon Steel' else row_data[10], 
                row_data[84],
                row_data[188]
                ])
            all_list_parts.append(nipplehex_list)

        code_valve = row_data[85]
        if code_valve:
            valve_list.append([
                code_valve,
                row_data[86],
                row_data[129],
                nipplehexdim[:4] + ' x ' + row_data[20],
                nipplehexdim[-3:] + '-H',
                '',
                'A-105' if row_data[18][-2:] == 'NB' else '316 SS',
                row_data[87],
                row_data[189]
                ])
            all_list_parts.append(valve_list)

        code_flangevalve = row_data[88]
        if code_flangevalve:
            flangevalve_list.append([
                code_flangevalve,
                row_data[89],
                row_data[130],
                '',
                '',
                '',
                'A-105' if row_data[10] == 'Carbon Steel' else row_data[10],
                row_data[90],
                row_data[190]
                ])
            all_list_parts.append(flangevalve_list)

        code_dv = row_data[91]
        if code_dv:
            dv_list.append([
                code_dv,
                row_data[92],
                row_data[131],
                '',
                '',
                '',
                'A-105' if row_data[10] == 'Carbon Steel' else row_data[10],
                row_data[93],
                row_data[191]
                ])
            all_list_parts.append(dv_list)

            if data(index(row, 127))[:3] == 'VÁL':
                plug_list.append([
                    'TAPÓN NORMAL ' + data(index(row, 20)) + data(index(row, 21)),
                    '',
                    '',
                    '',
                    'A-105' if data(index(row, 10)) == 'Carbon Steel' else data(index(row, 10)),
                    2,
                    'TA ' + data(index(row, 20)) + data(index(row, 21)),
                    '',
                    ''
                    ])

        code_nippletube = row_data[118]
        if code_nippletube:
            nippletube_list.append([
                code_nippletube,
                row_data[119],
                row_data[140],
                '80 mm',
                '',
                '',
                'A-106' if row_data[10] in ['Carbon Steel','ASTM A350 LF2 CL2'] else row_data[10],
                row_data[120],
                row_data[200]
                ])
            all_list_parts.append(nippletube_list)

        code_illuminator = row_data[97]
        if code_illuminator:
            illuminator_list.append([
                code_illuminator,
                row_data[98],
                row_data[133],
                '',
                '',
                '',
                'HIERRO',
                row_data[99],
                row_data[193]
                ])
            all_list_parts.append(illuminator_list)

        code_antifrost = row_data[121]
        if code_antifrost:
            antifrost_list.append([
                code_antifrost,
                row_data[122],
                row_data[141],
                '',
                '',
                '',
                'METACRILATO',
                row_data[123],
                row_data[201]
                ])
            all_list_parts.append(antifrost_list)

        columns_equipments = ["code_equipment", "code_fab_equipment", "translate_equipment", "section_type",
                                        "l_body", "qty_l_body", "l_cover", "qty_l_cover",
                                        "l_studs", "qty_l_studs", "l_nipplehex", "qty_l_nipplehex",
                                        "l_valve", "qty_l_valve", "l_flange", "qty_l_flange",
                                        "l_dv", "qty_l_dv", "l_scale", "qty_l_scale",
                                        "l_illuminator", "qty_l_illuminator", "l_gasketglass", "qty_l_gasketglass",
                                        "l_glass", "qty_l_glass", "l_float", "qty_l_float",
                                        "l_mica", "qty_l_mica", "l_flags", "qty_l_flags",
                                        "l_gasketflange", "qty_l_gasketflange", "l_nippletub", "qty_l_nippletub",
                                        "l_antifrost", "qty_l_antifrost"]

        columns_parts = ["code_part", "code_fab_part", "code_element", "model", "design", "process", "material", "section_type"]

        columns_tags = ["code", "equipment", "num_order","order_material","contractual_date","inspection"]

        values_equipments = [row_data[70], row_data[71], row_data[72], "N-Niveles",
                            row_data[73], row_data[75], row_data[76], row_data[78],
                            row_data[79], row_data[81], row_data[82], row_data[84],
                            row_data[85], row_data[87], row_data[88], row_data[90],
                            row_data[91], row_data[93], row_data[94], row_data[96],
                            row_data[97], row_data[99], row_data[100], row_data[102],
                            row_data[103], row_data[105], row_data[106], row_data[108],
                            row_data[109], row_data[111], row_data[112], row_data[114],
                            row_data[115], row_data[117], row_data[118], row_data[120],
                            row_data[121], row_data[123]]

        values_tags = [row_data[4] + "-" + row_data[8] + "-" + row_data[1], 
                        row_data[70], row_data[4], row_data[52],
                        row_data[42], row_data[66]]

        columns_equipments  = ", ".join([f'"{column}"' for column in columns_equipments])
        values_equipments =  ", ".join(['NULL' if value == '' or value == 0 else
                                        (str(value) if isinstance(value, (int, float)) else
                                        f"'{str(value)}'")
                                        for value in values_equipments])

        columns_tags  = ", ".join([f'"{column}"' for column in columns_tags])
        values_tags =  ", ".join(['NULL' if value == '' or value == PySide6.QtCore.QDate() else
                                (str(value) if isinstance(value, (int, float)) else
                                (f"'{value.toString('yyyy-MM-dd')}'" if isinstance(value, PySide6.QtCore.QDate) else
                                f"'{str(value)}'"))
                                for value in values_tags])

        columns_parts = ", ".join([f'"{column}"' for column in columns_parts])

        commands_equipments = f"INSERT INTO fabrication.equipments ({columns_equipments}) VALUES ({values_equipments})"
        commands_tags = f"INSERT INTO fabrication.tags ({columns_tags}) VALUES ({values_tags})"

        check_equipments = f"SELECT * FROM fabrication.equipments WHERE code_equipment = '{row_data[70]}'"

        if state == 'Order':
            try:
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(check_equipments)
                        results=cur.fetchall()

                if len(results) == 0:
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(commands_equipments)
                        conn.commit()

                else:
                    set_clause = ", ".join([f"{column} = {value}" for column, value in zip(columns_equipments.split(", ")[1:], values_equipments.split(", ")[1:])])
                    update_equipments = f"UPDATE fabrication.equipments SET {set_clause} WHERE code_equipment = '{row_data[70]}'"
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(update_equipments)
                        conn.cursor()

                for list_part in all_list_parts:
                    check_parts = f"SELECT * FROM fabrication.parts WHERE code_part = '{list_part[0][0]}'"
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(check_parts)
                            results=cur.fetchall()

                    if len(results) == 0:
                        list_part_modified = list_part[0][:8].copy()
                        list_part_modified[-1] = 'N-Niveles'
                        values_parts = ", ".join('NULL' if value == '' else (str(value) if isinstance(value, (int, float)) else f"'{str(value)}'") for value in list_part_modified)
                        commands_parts = f"INSERT INTO fabrication.parts ({columns_parts}) VALUES ({values_parts})"
                        with Database_Connection(config_database()) as conn:
                            with conn.cursor() as cur:
                                cur.execute(commands_parts)
                            conn.commit()

                    else:
                        list_part_modified = list_part[0][:8].copy()
                        list_part_modified[-1] = 'N-Niveles'
                        values_parts = ", ".join('NULL' if value == '' else (str(value) if isinstance(value, (int, float)) else f"'{str(value)}'") for value in list_part_modified)
                        set_clause = ", ".join([f"{column} = {value}" for column, value in zip(columns_parts.split(", ")[1:], values_parts.split(", ")[1:])])
                        update_parts = f"UPDATE fabrication.parts SET {set_clause} WHERE code_part = '{list_part[0][0]}'"
                        with Database_Connection(config_database()) as conn:
                            with conn.cursor() as cur:
                                cur.execute(update_parts)
                            conn.commit()

                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(commands_tags)
                    conn.commit()

            except (Exception, psycopg2.DatabaseError) as error:
                MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                            + str(error), "critical")

# Turn all lists in dataframe and grouped in order to sum same items
    data_lists = [
    (body_list, "df_body"),
    (cover_list, "df_cover"),
    (glass_list, "df_glass"),
    (gasket_list, "df_gasket"),
    (mica_list, "df_mica"),
    (bolts_list, "df_bolts"),
    (nipplehex_list, "df_nipplehex"),
    (valve_list, "df_valve"),
    (flangevalve_list, "df_flangevalve"),
    (nippletube_list, "df_nippletube"),
    (dv_list, "df_list"),
    (antifrost_list, "df_antifrost"),
    (expand_illuminators_from_list(illuminator_list), "df_illuminator"),
    (plug_list, "df_plug")]

    data_frames_with_data = []

    for data_list, df_name in data_lists:
        if data_list:
            sublists = [sublist[2:] for sublist in data_list]
            df = pd.DataFrame(sublists, columns=['descripción', 'modelo', 'diseño', 'proceso', 'material', 'cantidad', 'suministro'])
            df = df.groupby(['descripción', 'modelo', 'diseño', 'proceso', 'material', 'suministro'])['cantidad'].sum().reset_index()
            data_frames_with_data.append(df)

    if data_frames_with_data:
        df_final = pd.concat(data_frames_with_data, ignore_index=True)

        values_supplies = df_final['suministro'].dropna().unique().tolist()

        query = """
        SELECT reference AS suministro, physical_stock AS st_fisico, available_stock AS st_disponible, pending_stock as st_pend, virtual_stock AS st_virtual
        FROM purch_fact.supplies
        WHERE reference IN %(values)s
        """

        with Database_Connection(config_database()) as conn:
            df_supplies = pd.read_sql(query, config_sql_engine(), params={"values": tuple(values_supplies)})

        df_final = (df_final.merge(df_supplies, on='suministro', how='left')
                    [['descripción', 'modelo', 'diseño', 'proceso', 'material', 'cantidad', 'suministro',
                        'st_fisico', 'st_disponible', 'st_pend', 'st_virtual']])

        df_final['almacen_si'] = ''
        df_final['almacen_no'] = ''
        df_final['proveedor'] = ''
        df_final['fecha_pedido'] = ''
        df_final['fecha_prevista'] = ''

        df_final = df_final[
            ['descripción', 'modelo', 'diseño', 'proceso', 'material',
            'cantidad', 'almacen_si', 'almacen_no', 'suministro',
            'proveedor', 'fecha_pedido', 'fecha_prevista',
            'st_fisico', 'st_disponible', 'st_pend', 'st_virtual']
        ]

    commands_client_order = ("""
                SELECT orders."num_order",orders."num_offer",offers."client"
                FROM offers
                INNER JOIN orders ON (offers."num_offer"=orders."num_offer")
                WHERE UPPER(orders."num_order") LIKE UPPER('%%'||%s||'%%')
                """)

    commands_client_offer = ("""
                SELECT offers."num_offer",offers."client"
                FROM offers
                WHERE UPPER(offers."num_offer") LIKE UPPER('%%'||%s||'%%')
                """)

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                if state == 'Order':
                    cur.execute(commands_client_order,(numorder,))
                    results=cur.fetchone()
                    client=results[2]
                else:
                    cur.execute(commands_client_offer,(numorder,))
                    results=cur.fetchone()
                    client=results[1]

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    excel_mat_order = material_order(df_final, numorder_pedmat, client, variable, num_ot)
    excel_mat_order.save_excel()


def others_matorder(proxy, model, numorder, numorder_pedmat, variable, state):
    """
    Processes material raw orders for others items by inserting new entries into the fabrication orders database.

    Args:
        proxy (QAbstractProxyModel): The proxy model containing the current data view.
        model (QAbstractItemModel): The model containing the main data.
        numorder (str): The order number to process.
        numorder_pedmat (str): The base order number for material orders.
        variable (str): A variable that determines the type of processing to be done. The specific usage
                        of this variable is not detailed in the function.

    Returns:
        None: This function does not return a value but modifies the database state.
    """
    id_list = []

    list_valves_210 = ['V-9305','V-9575','V-9576','2V-210']

    proxy_data = proxy.data
    proxy_index = proxy.index

    data = model.data
    index = model.index

    id_list = [
        proxy_data(proxy_index(row, 0))
        for row in range(proxy.rowCount())
        if proxy_data(proxy_index(row, 2)) == "QUOTED" and str(proxy_data(proxy_index(row, 5))) == ''
    ]

    row_map = {
        data(index(row, 0)): row
        for row in range(model.rowCount())
    }

    commands_numot = ("""SELECT "ot_num"
                        FROM fabrication.fab_order
                        WHERE NOT "ot_num" LIKE '90%'
                        ORDER BY "ot_num" ASC
                        """)

    check_otpedmat = f"SELECT * FROM fabrication.fab_order WHERE id = '{numorder_pedmat + '-PEDMAT'}'"

    commands_otpedmat = ("""
                            INSERT INTO fabrication.fab_order (
                            "id","tag","element","qty_element",
                            "ot_num","qty_ot","start_date")
                            VALUES (%s,%s,%s,%s,%s,%s,%s)
                            """)

    if state == 'Offer':
        num_ot = '0'
    else:
        try:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(commands_numot)
                    results=cur.fetchall()
                    num_ot=results[-1][0]

            excel_file_path = r"\\ERP-EIPSA-DATOS\Comunes\EIPSA Sistemas de Gestion\MasterCTF\Bases\Contador.xlsm"
            workbook = openpyxl.load_workbook(excel_file_path, keep_vba=True)
            worksheet = workbook.active
            num_ot = worksheet['B2'].value

            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(check_otpedmat)
                    results=cur.fetchall()

            if len(results) == 0:
                data_numot=(numorder_pedmat + '-PEDMAT', numorder_pedmat, 'PEDIDO DE MATERIALES', 1, '{:06}'.format(int(num_ot) + 1), len(id_list), date.today().strftime("%d/%m/%Y"))
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(commands_otpedmat, data_numot)
                    conn.commit()

                worksheet['B2'].value = '{:06}'.format(int(num_ot) + 1)
                workbook.save(excel_file_path)

        except (Exception, psycopg2.DatabaseError) as error:
            MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                        + str(error), "critical")

    if len(id_list) != 0:
        model_list = []
        valve_model_list = []
        list_1 = []
        list_2 = []
        list_3 = []
        list_4 = []
        list_5 = []
        list_6 = []
        list_7 = []
        list_8 = []
        list_9 = []
        list_10 = []
        list_11 = []
        list_12 = []
        list_13 = []
        list_14 = []
        list_15 = []
        list_16 = []
        list_17 = []
        list_18 = []

        for element in id_list:
            row = row_map.get(element)
            if row is None:
                continue
    
            row_data = [
                data(index(row, c))
                for c in range(model.columnCount())
            ]

            description = row_data[8]

            # Order for 2V-210 valves
            if any(valve in description for valve in list_valves_210):
                model_valve = re.match(r'(V-\d+-[A-Za-z0-9]+)', description).group(0)
                material_valve = (re.match(r'(V-\d+-[A-Za-z0-9]+)(.*)', description).group(2).lstrip(' - ').strip()).split(' / ')[0]
                sch_valve = re.search(r'V-\d+-(\w+)', description).group(1)

                tradcodvalve = 'VÁLVULA 2V-210 SCH ' + sch_valve + (' BRIDADA ' + description.split(' / ')[1].strip()) if '# RF' in description else ''
                schvalve = 'MOD.: ' + model_valve
                designvalve = ''
                processvalve = ''
                materialvalve = material_valve
                qtyvalve = 1
                valve_model_list.append([tradcodvalve,schvalve,designvalve,processvalve,materialvalve,qtyvalve])

                list_1.append(['VOLANTE','VÁLVULA 2V-210 - 1500#','','',materialvalve,1, ''])
                list_2.append(['ARANDELA VÁLVULA','VÁLVULA 2V-210 - 1500#','','','AC. INOX',1, ''])
                list_3.append(['VÁSTAGO','VÁLVULA 2V-210 - 1500#','','','AISI-316 + STELLITE',1, ''])
                list_4.append(['GUÍA VÁSTAGO/TUERCA (ø25 x LONG 37 mm) (EXAG 22 ec/ x 6 mm)','VÁLVULA 2V-210 - 1500#','','','AC. INOX' if materialvalve == '316' else 'AC. CARBONO',1, ''])
                list_5.append(['CAPELLI (HORQUILLA)','VÁLVULA 2V-210 - 1500#','','',materialvalve,1, ''])
                list_6.append(['FLANGETE','VÁLVULA 2V-210 - 1500#','','',materialvalve,1, ''])
                list_7.append(['PRENSA (ø25 x LONG 20 mm)','VÁLVULA 2V-210 - 1500#','','','AC. INOX' if materialvalve == '316' else 'AC. CARBONO',1, ''])
                list_8.append(['EMPAQUETADURA','VÁLVULA 2V-210 - 1500#','','','GRAFITO',1, ''])
                list_9.append(['TORNILLO CUADRADO (2 ud. POR VÁLVULA)','VÁLVULA 2V-210 - 1500#','','','AC. INOX',2, ''])
                list_10.append(['TORNILLO REDONDO (4 ud. POR VÁLVULA)','VÁLVULA 2V-210 - 1500#','','','AC. INOX',4, ''])
                list_11.append(['TUERCAS M10 2H','VÁLVULA 2V-210 - 1500#','','','A1942H',4, ''])
                list_12.append(['JUNTA ESPIROMETÁLICA 42x30x3,2mm','VÁLVULA 2V-210 - 1500#','','','AISI-316 + GRAFITO',1, ''])
                list_13.append(['CUERPO VÁLVULA 2V-210 - 1500#','','','',materialvalve,1, ''])
                list_14.append(['ASIENTO (ø20 x 16 mm)','VÁLVULA 2V-210 - 1500#','','','AISI-316 + STELLITE',1, ''])
                list_15.append(['BRIDA VÁLVULA '+ description.split(' / ')[1].strip(),'VÁLVULA 2V-210 - 1500#','','',materialvalve,1, '']) if '# RF' in description else ''
                list_16.append(['TAPÓN PURGADOR 1/2" NPT-M','','','',materialvalve,1, ''])
                list_17.append(['TORNILLO TAPÓN PURGADOR','','','','AC. INOX',1, ''])
                if len(description.split(' / ')) > 2: 
                    list_18.append(['NIPLO ' + description.split(' / ')[2],'','','','AC. INOX' if materialvalve == '316' else 'AC. CARBONO',1, '']) 

                data_lists = [
                (valve_model_list, "df_valvemodel"),
                (list_1, "df_list1"),
                (list_2, "df_list2"),
                (list_3, "df_list3"),
                (list_4, "df_list4"),
                (list_5, "df_list5"),
                (list_6, "df_list6"),
                (list_7, "df_list7"),
                (list_8, "df_list8"),
                (list_9, "df_list9"),
                (list_10, "df_list10"),
                (list_11, "df_list11"),
                (list_12, "df_list12"),
                (list_13, "df_list13"),
                (list_14, "df_list14"),
                (list_15, "df_list15"),
                (list_16, "df_list16"),
                (list_17, "df_list17"),
                (list_18, "df_list18")]

        # Order for CN-32219
            elif 'CN-32219' in description:
                list_1.append(['BRIDA BLIND 4" 900# RTJ', 'ø293 x 53 mm', '', '', '321', 1, ''])
                list_2.append(['TUBO 1/4" SCH 40S (ø13,5 x ESP 2,3 mm)','(2323x' + 1 +')+(1753x' + 1 + ')+(1183x' + 1 + ')', '', '', '321', str(round(5260 / 1000, 2)), ''])
                list_3.append(['TUBO 3" SCH 80S','2664 x ' * 1, '', '', '321', str(round(2680 / 1000, 2)), ''])
                list_4.append(['BARRA ø25 x LONG. 30 mm (1/4" NPT-H)','', '', '', '321', 1, ''])
                list_5.append(['BARRA ø25 x LONG. 40 mm (1/4" NPT-H x 1/4" SW)','REDUCCIÓN 1/4"SW A 1/4" NPT-H', '', '', '321', 3, ''])
                list_6.append(['ACCESORIO FIJACIÓN BARRA ø20 x LONG 34 mm', '', '', '', '321', 3, ''])
                list_7.append(['CAP SOLDADO BARRA ø90 x LONG 67 mm', '', '', '', '321', 1, ''])
                list_8.append(['EMPTAPÓN DE PURGA 1/4" NPT-M (EXAG. 17 e/c x LONG. 31 mm)AQUETADURA', 'EXAG. 17 e/c (ø20 mm)', '', '', '321', 1, ''])

                data_lists = [
                (list_1, "df_list1"),
                (list_2, "df_list2"),
                (list_3, "df_list3"),
                (list_4, "df_list4"),
                (list_5, "df_list5"),
                (list_6, "df_list6"),
                (list_7, "df_list7"),
                (list_8, "df_list8")]

            elif 'D-3355/2' in description:
                list_1.append(['BRIDA DE LÍNEA 5" 600# RF', 'ø331 x 51 mm', '', '', 'AISI-321', 1, ''])
                list_2.append(['TUBO 3" SCH XXS', str(len(id_list)) + 'x2430', '', '', 'AISI-321', 2.43, ''])
                list_3.append(['CAP 3" SCH XXS (ø88.89 mm X 64 mm)', 'LONGITUD 64 MM', '', '', 'AISI-321', 1, ''])
                list_4.append(['MANGUITO 1/4" NPT x 1/4" SW', 'ø25,4 x LONG 35 mm', '', '', 'AISI-321', 3, ''])
                list_5.append(['TAPÓM EXAGONAL 1/4" NPT-H (PARA MANGUITO DRENAJE)', 'ø29 x LONG 27 mm', '', '', 'AISI-321', 1, ''])
                list_6.append(['MANGUITO DE DRENAJE', 'ø25,4 x LONG 140 mm', 'exag. 25 e/c', '', 'AISI-321', 1, ''])
                list_7.append(['TAPÓN DE CONTACTO (VAINA EXTERIOR CON VAINA INTERIOR)', 'ø25 x LONG 42 mm', '', '', 'AISI-321', 3, ''])
                list_8.append(['TUBO 1/4" SCH 40S (ø13.5 X 2.3 mm ESP)', str(len(id_list)) + 'x1134', '', '', 'AISI-321', 1.134, ''])
                list_9.append(['TUBO 1/4" SCH 40S (ø13.5 X 2.3 mm ESP)', str(len(id_list)) + 'x1654', '', '', 'AISI-321', 1.654, ''])
                list_10.append(['TUBO 1/4" SCH 40S (ø13.5 X 2.3 mm ESP)', str(len(id_list)) + 'x2174', '', '', 'AISI-321', 2.174, ''])
                list_11.append(['TAPOÓN CIERRES PARA TUBOS 1/4"', 'ø8,9 x LONG 6 MM', 'SALE DE VARILLA ø12', '', 'AISI-321', 3, ''])

                data_lists = [
                (list_1, "df_list1"),
                (list_2, "df_list2"),
                (list_3, "df_list3"),
                (list_4, "df_list4"),
                (list_5, "df_list5"),
                (list_6, "df_list6"),
                (list_7, "df_list7"),
                (list_8, "df_list8"),
                (list_9, "df_list9"),
                (list_10, "df_list10"),
                (list_11, "df_list11")]

            else:
                tradcod = str(description)
                sch = ''
                design = ''
                process = ''
                material = ''
                qty = 1
                model_list.append([tradcod,sch,design,process,material,qty])

                data_lists = [
                (model_list, "df_model"),]

        data_frames_with_data = []

        for data_list, df_name in data_lists:
            if data_list:
                sublists = [sublist[2:] for sublist in data_list]
                df = pd.DataFrame(sublists, columns=['descripción', 'modelo', 'diseño', 'proceso', 'material', 'cantidad', 'suministro'])
                df = df.groupby(['descripción', 'modelo', 'diseño', 'proceso', 'material', 'suministro'])['cantidad'].sum().reset_index()
                data_frames_with_data.append(df)

        if data_frames_with_data:
            df_final = pd.concat(data_frames_with_data, ignore_index=True)

            values_supplies = df_final['suministro'].dropna().unique().tolist()

            query = """
            SELECT reference AS suministro, physical_stock AS st_fisico, available_stock AS st_disponible, pending_stock as st_pend, virtual_stock AS st_virtual
            FROM purch_fact.supplies
            WHERE reference IN %(values)s
            """

            with Database_Connection(config_database()) as conn:
                df_supplies = pd.read_sql(query, config_sql_engine(), params={"values": tuple(values_supplies)})

            df_final = (df_final.merge(df_supplies, on='suministro', how='left')
                        [['descripción', 'modelo', 'diseño', 'proceso', 'material', 'cantidad', 'suministro',
                            'st_fisico', 'st_disponible', 'st_pend', 'st_virtual']])

            df_final['almacen_si'] = ''
            df_final['almacen_no'] = ''
            df_final['proveedor'] = ''
            df_final['fecha_pedido'] = ''
            df_final['fecha_prevista'] = ''

            df_final = df_final[
                ['descripción', 'modelo', 'diseño', 'proceso', 'material',
                'cantidad', 'almacen_si', 'almacen_no', 'suministro',
                'proveedor', 'fecha_pedido', 'fecha_prevista',
                'st_fisico', 'st_disponible', 'st_pend', 'st_virtual']
            ]

    commands_client_order = ("""
                SELECT orders."num_order",orders."num_offer",offers."client"
                FROM offers
                INNER JOIN orders ON (offers."num_offer"=orders."num_offer")
                WHERE UPPER(orders."num_order") LIKE UPPER('%%'||%s||'%%')
                """)

    commands_client_offer = ("""
                SELECT offers."num_offer",offers."client"
                FROM offers
                WHERE UPPER(offers."num_offer") LIKE UPPER('%%'||%s||'%%')
                """)

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                if state == 'Order':
                    cur.execute(commands_client_order,(numorder,))
                    results=cur.fetchone()
                    client=results[2]
                else:
                    cur.execute(commands_client_offer,(numorder,))
                    results=cur.fetchone()
                    client=results[1]

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    excel_mat_order = material_order(df_final, numorder_pedmat, client, variable, num_ot)
    excel_mat_order.save_excel()


def material_list(proxy, model, variable, numoffer):
    id_list = []
    flow_list = []
    temp_list = []
    level_list = []

    query_offer_data = ("SELECT client, project FROM offers WHERE num_offer = %s")

    proxy_data = proxy.data
    proxy_index = proxy.index

    data = model.data
    index = model.index

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cur:
            cur.execute(query_offer_data,(numoffer,))
            results = cur.fetchall()
            client_value = results[0][0]
            project_value = results[0][1]

    id_list = [
        proxy_data(proxy_index(row, 0))
        for row in range(proxy.rowCount())
        if proxy_data(proxy_index(row, 2)) == "QUOTED" and str(proxy_data(proxy_index(row, 5))) == ''
    ]

    row_map = {
        data(index(row, 0)): row
        for row in range(model.rowCount())
    }

    if variable == 'Caudal':
        for element in id_list:
            row = row_map.get(element)
            if row is None:
                continue

            row_data = [data(index(row, c)) for c in range(model.columnCount())]
            # appending [type_value, flange_material_value, element_material_value, size_value, rating_value, facing_value, schedule_value, qty_value]
            flow_list.append([
                row_data[8],
                row_data[13],
                row_data[19],
                row_data[9],
                int(row_data[10]) if row_data[10] not in ['N/A', 'HOLD', 'OTHERS'] else row_data[10],
                row_data[11],
                row_data[12],
                1 * int(row_data[35])
                ])

    elif variable == 'Temperatura':
        for element in id_list:
            row = row_map.get(element)
            if row is None:
                continue
            # [type_value, tw_type_value, tw_material_value, size_value, rating_value, facing_value, insertion_value, qty_value]
            row_data = [data(index(row, c)) for c in range(model.columnCount())]
            temp_list.append([
                row_data[8],
                row_data[9],
                row_data[14],
                row_data[10],
                int(row_data[11]) if row_data[11] not in ['N/A', 'HOLD', 'OTHERS', 'NPT-M'] else row_data[11],
                row_data[12],
                row_data[16],
                1 * int(row_data[42])
                ])

    elif variable == 'Nivel':
        for element in id_list:
            row = row_map.get(element)
            if row is None:
                continue
            row_data = [data(index(row, c)) for c in range(model.columnCount())]
            type_value = row_data[8]
            if type_value == 'Magnetic':
                # [type_value, body_material, conn_size, conn_rating, conn_facing, c-c_length, float_material, bolting_material, qty_value]
                level_list.append([
                    row_data[8],
                    row_data[10],
                    row_data[12],
                    int(row_data[13]) if row_data[13] != 'N/A' else row_data[13],
                    row_data[14],
                    row_data[17],
                    row_data[26],
                    row_data[24],
                    1
                    ])
            else:
                # [type_value, body_material, conn_size, conn_rating, conn_facing, c-c_length, cover_material, bolting_material, qty_value]
                level_list.append([
                    row_data[8],
                    row_data[10],
                    row_data[12],
                    int(row_data[13]) if row_data[13] != 'N/A' else row_data[13],
                    row_data[14],
                    row_data[27],
                    row_data[26],
                    row_data[24],
                    1
                    ])

    dfs = []
    if flow_list:
        cols = ['TIPO', 'MAT. BRIDA', 'MAT. ELEMENTO', 'TAMAÑO', 'RATING', 'FACING', 'SCHEDULE', 'Nº EQUIPOS']
        df = pd.DataFrame(flow_list, columns=cols)
        df = df.groupby(cols[:-1], as_index=False)['Nº EQUIPOS'].sum()
        df["tam_num"] = df["TAMAÑO"].apply(size_to_float)
        df_sorted = df.sort_values(["TIPO", "MAT. BRIDA", "tam_num"]).drop(columns="tam_num")
        dfs.append(df_sorted)

    if temp_list:
        cols = ['TIPO', 'TIPO TW', 'MAT. TW', 'TAMAÑO', 'RATING', 'FACING', 'INSERCIÓN', 'Nº EQUIPOS']
        df = pd.DataFrame(temp_list, columns=cols)
        df = df.groupby(cols[:-1], as_index=False)['Nº EQUIPOS'].sum()
        df["tam_num"] = df["TAMAÑO"].apply(size_to_float)
        df_sorted = df.sort_values(["TIPO", "TIPO TW", "MAT. TW", "tam_num"]).drop(columns="tam_num")
        dfs.append(df_sorted)

    if level_list:
        cols = ['TIPO', 'MAT. CUERPO', 'TAMAÑO', 'RATING', 'FACING', 'LONG. C-C', 'MAT. CUBIERTA / FLOTADOR', 'MAT. TORN', 'Nº EQUIPOS']
        df = pd.DataFrame(level_list, columns=cols)
        df = df.groupby(cols[:-1], as_index=False)['Nº EQUIPOS'].sum()
        df["tam_num"] = df["TAMAÑO"].apply(size_to_float)
        df_sorted = df.sort_values(["TIPO", "MAT. CUERPO", "MAT. CUBIERTA / FLOTADOR", "LONG. C-C", "tam_num"]).drop(columns="tam_num")
        dfs.append(df_sorted)

    df_final = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

    path, _ = QFileDialog.getSaveFileName(
    None,
    "Guardar lista de materiales oferta",
    "",
    "Excel Files (*.xlsx)"
    )
    if path:
        with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
            sheet = "Materiales"
            bold = writer.book.add_format({'bold': True})

            worksheet = writer.book.add_worksheet(sheet)
            writer.sheets[sheet] = worksheet

            worksheet.write(0, 0, numoffer, bold)
            worksheet.write(0, 1, client_value, bold)
            worksheet.write(0, 2, project_value, bold)
            worksheet.write(0, 3, variable, bold)
            worksheet.write(0, 6, date.today().strftime("%d/%m/%Y"), bold)

            row = 3
            for type_equipment, df_type in df_final.groupby("TIPO"):
                df_type.to_excel(writer, sheet_name=sheet, startrow=row, index=False)

                total = df_type["Nº EQUIPOS"].sum() #calculate total quantity for type dataframe

                row += len(df_type) + 1  # +1 header

                # write TOTAL and total value
                worksheet.write(row, len(df_type.columns)-2, "TOTAL", bold)
                worksheet.write(row, len(df_type.columns)-1, total, bold)

                row += 2  # total + blank row
        MessageHelper.show_message("Guardado con éxito", "info")


def get_number_before_mm(text):
    """
    Extracts the integer value that appears before the 'mm' substring in the given text.

    Args:
        text (str): The input string to search for the number.

    Returns:
        int or None: The extracted integer value if found, or None if no match is found.
    """
    match = re.search(r'(\d+)\s*mm', text)
    if match:
        return int(match.group(1))
    return None


def size_to_float(size):
    size = size.replace('"', '')

    if 'N/A' in size:
        return 'N/A'
    
    if 'HOLD' in size:
        return 'HOLD'

    if '-' in size:              # ejemplo 1-1/2
        whole, frac = size.split('-')
        return float(whole) + float(Fraction(frac))

    if '/' in size:              # ejemplo 1/2
        return float(Fraction(size))

    return float(size) 


def flow_material_list(proxy, model):
    """
    Processes material raw orders for flow items by inserting new entries into the fabrication orders database.

    Args:
        proxy (QAbstractProxyModel): The proxy model containing the current data view.
        model (QAbstractItemModel): The model containing the main data.

    Returns:
        df_final: This function returns a dataframe with the resume of materials.
    """

    parts = []

    proxy_data = proxy.data
    proxy_index = proxy.index

    data = model.data
    index = model.index

    id_list = [
        proxy_data(proxy_index(row, 0))
        for row in range(proxy.rowCount())
        if proxy_data(proxy_index(row, 2)) == "QUOTED"
        and str(proxy_data(proxy_index(row, 5))) == ''
    ]

    row_map = {
        data(index(row, 0)): row
        for row in range(model.rowCount())
    }

    flange_code_cache = {}
    sheet_material_cache = {}
    pipe_thk_cache = {}

    for element in id_list:
        row = row_map.get(element)
        if row is None:
            continue

        row_data = [
            data(index(row, c))
            for c in range(model.columnCount())
        ]

        flange_material = row_data[13]
        sch = row_data[12]
        design = str(row_data[65]).replace('.', ',') # pipe internal diameter
        size = f"{row_data[9]} {row_data[10]} {row_data[11]}"
        quantity_equipment = int(row_data[35])

        code_orifice_flange = row_data[166]
        if code_orifice_flange:
            parts.append([
                row_data[202], # trad orifice flange
                sch,
                design,
                "", #row_data[37],
                flange_material,
                int(row_data[190]) * quantity_equipment, # quantity orifice flange per equipment * number of equipments
                row_data[214] # code purch orifice flange
            ])

        code_line_flange = row_data[167]
        if code_line_flange:
            parts.append([
                row_data[203], # trad line flange
                sch,
                design,
                "", #row_data[37],
                flange_material,
                int(row_data[191]) * quantity_equipment, # quantity line flange per equipment * number of equipments
                row_data[215] # code purch line flange
            ])

        code_gasket = row_data[168]
        if code_gasket:
            parts.append([
                row_data[204], # trad gasket
                size,
                '',
                '',
                '',
                int(row_data[46]) * quantity_equipment, # quantity gasket per equipment * number of equipments
                row_data[216] # code purch gasket
            ]) 

        code_bolts = row_data[169]
        if code_bolts:
            qty = int(row_data[48]) if row_data[48] != '' else 0
            parts.append([
                row_data[205], # trad bolts
                size,
                ('esp. placa ' + row_data[21]),
                '',
                row_data[24] + " / " + row_data[25],
                qty * quantity_equipment, # quantity bolts per equipment * number of equipments
                row_data[217] # code purch bolts
            ])

        code_plugs = row_data[170]
        if code_plugs != '':
            parts.append([
                row_data[206], # trad plug
                '',
                '',
                '',
                row_data[49], # material plug
                (int(row_data[50]) if row_data[50] != '' else 0) * quantity_equipment, # quantity plugs per equipment * quantity of equipment
                row_data[218]
                ])

        code_extractor = row_data[171]
        if code_extractor:
            parts.append([
                row_data[207], # trad extractor
                size,
                ('esp. placa ' + row_data[21]),
                '',
                row_data[51],
                int(row_data[53]) * quantity_equipment, # quantity extractor per equipment * number of equipments
                row_data[219] # code purch extractor
            ])

        code_plate = row_data[172]
        if code_plate:
            qty = int(float(row_data[28])) if row_data[8] == "MULTISTAGE RO" else 1
            process = 'ARAMCO' if row_data[22] == 'ARA' else ''

            parts.append([
                row_data[208], # trad plate
                ('ESP ' + row_data[21] + 'mm'),
                row_data[66],
                process,
                row_data[19],
                qty * quantity_equipment, # quantity of plates per equipment * number of equipments
                row_data[220] # code purch plate
            ])

        code_handle = row_data[174]
        if code_handle and row_data[21] not in ['3', '1/8" (3)']:
            if row_data[11] == 'RTJ':
                modelhandle = ''
                designhandle = ''

                parts.append([
                    'BARRA MANGO', # trad handle
                    '',
                    '',
                    '',
                    '316SS',
                    ((int(float(row_data[68])) - 30) if 'datos' not in row_data[68] else 0) * quantity_equipment, # length of bar handle per equipment * quantity of equipments
                    '' # code purch handle
                    ])
            else:
                modelhandle = f"{row_data[68]}x{row_data[69]}x{row_data[70]} mm"
                designhandle = row_data[22]

            parts.append([
                row_data[210], # trad handle
                modelhandle,
                designhandle,
                '',
                '316SS',
                1 * quantity_equipment, # quantity of handles per equipment * number of equipments
                row_data[222] # code purch handle
            ])

        code_ch_ring = row_data[175]
        if code_ch_ring:
            schchring = 'ESP ' if row_data[11] == "RTJ" else 'ESP 38,5mm ACABADO'

            parts.append([
                row_data[211], # trad chring
                schchring,
                'ø' + str(row_data[66]),
                '', #row_data[37],
                row_data[19],
                1 * quantity_equipment, # quantity chring per equipment * quantity of equipments
                row_data[223] # code purch chring
            ])

        code_tube = row_data[176]
        if code_tube:
            parts.append([
                row_data[212], # trad tube
                sch,
                design,
                '',
                row_data[15],
                float(row_data[200]) * quantity_equipment, # quantity tube per equipment (length of tube) * quantity of equipments
                row_data[224] # code purch tube
            ])

        code_piece2 = row_data[177]
        if code_piece2:
            line_size = row_data[9]
            sch = row_data[12]
            flange_material = row_data[13]

            thk_key = (line_size, sch)

            if thk_key not in pipe_thk_cache:
                try:
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute("""
                                SELECT wall_thk
                                FROM validation_data.pipe_diam
                                WHERE line_size = %s
                                AND sch = %s
                            """,(line_size, sch))

                            pipe_thk_cache[thk_key] = cur.fetchone()[0]

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message(
                        "Ha ocurrido el siguiente error:\n" + str(error),
                        "critical"
                    )
                    pipe_thk_cache[thk_key] = ''

            thkmin = pipe_thk_cache[thk_key]

            modelpiece2 = 'Th mín ' + str(thkmin) + 'mm'

            if flange_material not in flange_code_cache:
                try:
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute("""
                                SELECT code
                                FROM validation_data.flow_flange_material
                                WHERE flange_material = %s
                            """,(flange_material,))

                            flange_code_cache[flange_material] = cur.fetchone()[0]

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message(
                        "Ha ocurrido el siguiente error:\n" + str(error),
                        "critical"
                    )
                    flange_code_cache[flange_material] = None

            flange_code = flange_code_cache[flange_material]

            if flange_code not in sheet_material_cache:
                try:
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute("""
                                SELECT sheet_material
                                FROM validation_data.flow_sheet_material
                                WHERE code = %s
                            """,(flange_code,))

                            sheet_material_cache[flange_code] = cur.fetchone()[0]

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message(
                        "Ha ocurrido el siguiente error:\n" + str(error),
                        "critical"
                    )
                    sheet_material_cache[flange_code] = ''

            materialpiece2 = sheet_material_cache[flange_code]

            parts.append([
                row_data[213], # trad wedge
                modelpiece2,
                '',
                '',
                materialpiece2,
                1 * quantity_equipment, # quantity of wedge parts per equipment * quantity of equipments
                row_data[225] # code purch wedge
            ])

    df = pd.DataFrame(
        parts,
        columns=[
            'descripción','modelo','diseño','proceso',
            'material','cantidad','suministro'
        ]
    )

    df = (
        df.groupby(
            ['descripción','modelo','diseño','proceso','material','suministro']
        )['cantidad']
        .sum()
        .reset_index()
    )

    return df


def temp_material_list(proxy, model):
    """
    Processes material raw orders for temp items by inserting new entries into the fabrication orders database.

    Args:
        proxy (QAbstractProxyModel): The proxy model containing the current data view.
        model (QAbstractItemModel): The model containing the main data.

    Returns:
        df_final: This function returns a dataframe with the resume of materials.
    """
    parts = []

    proxy_data = proxy.data
    proxy_index = proxy.index

    data = model.data
    index = model.index

    id_list = [
        proxy_data(proxy_index(row, 0))
        for row in range(proxy.rowCount())
        if proxy_data(proxy_index(row, 2)) == "QUOTED"
        and str(proxy_data(proxy_index(row, 5))) == ''
    ]

    row_map = {
        data(index(row, 0)): row
        for row in range(model.rowCount())
    }

    for element in id_list:
        row = row_map.get(element)
        if row is None:
            continue

        row_data = [
            data(index(row, c))
            for c in range(model.columnCount())
        ]

        tw_type = row_data[9]
        quantity_equipment = int(row_data[42])

        code_bar = row_data[147]
        if code_bar :
            parts.append([
                row_data[183] if 'Helical' not in tw_type else
                    'VAINA HELICOIDAL' + (' BRIDADA ' + row_data[10] + ' ' + row_data[11] + ' ' + row_data[12] if tw_type == 'Flanged Helical' else ''),
                'U=' + row_data[16] + ' /L=' + row_data[15] if ('Stone' in tw_type or 'Helical' in tw_type) else
                    'Barra ø=' + (row_data[57]),
                'RAÍZ ø=' + row_data[17] if tw_type == 'Van-Stone TW' else '',
                '',
                row_data[14],
                (float(row_data[171]) if 'Helical' not in tw_type else 1)  * quantity_equipment,
                row_data[195]
                ])

        code_tube = row_data[148]
        if code_tube:
            parts.append([
                row_data[184],
                row_data[38],
                '',
                '',
                row_data[14],
                float(row_data[172])  * quantity_equipment,
                row_data[197]
                ])

        code_flange = row_data[149]
        if code_flange:
            list_tw = ['Buttweld TW','Forged Flanged TW','Threaded Helical','Van-Stone Helical','VORTICRACK']
            parts.append([
                row_data[185] if tw_type not in list_tw else '',
                '',
                '',
                '',
                row_data[35] if tw_type == 'Van-Stone TW'
                    else (row_data[14] if tw_type not in list_tw else ''),
                (1 if tw_type not in list_tw else 0) * quantity_equipment,
                row_data[197]
                ])

        code_sensor = row_data[150]
        if code_sensor:
            parts.append([
                row_data[186],
                row_data[33] + '-' + row_data[32] if code_sensor[:4] == 'Bime' else '',
                row_data[27] + '-' + row_data[28] if code_sensor[:4] == 'Bime' else '',
                'PLATINO' if row_data[186][:5] == 'PT100' else
                    ('AC. INOX.' if row_data[24] == 'St.Steel' else
                    row_data[24]),
                (1 if row_data[186][:5] == 'PT100' or code_sensor[:4] == 'Bime' else
                    (float(row_data[63])/1000) if row_data[63] != '' else
                    0) * quantity_equipment,
                row_data[198]
                ])

        code_head = row_data[151]
        if code_head:
            parts.append([
                row_data[187],
                row_data[31],
                '',
                row_data[33],
                ('ALUMINIO' if row_data[31][-2:] == 'AL' 
                            else ('AC.CARBONO' if row_data[31][-2:] == 'CS' 
                            else ('AC.INOXIDABLE' if row_data[31][-2:] == 'SS' 
                            else 'MATERIAL CABEZA NO DEFINIDO'))),
                1 * quantity_equipment,
                row_data[198]
                ])

        code_btb = row_data[152]
        if code_btb:
            parts.append([
                row_data[188],
                ("RANGO " + row_data[27] + '-' + row_data[28]) if code_btb[:2] == 'BI' else '',
                '',
                '',
                row_data[24] if code_btb[:2] == 'BI' else ('CERÁMICO' if code_btb[:2] == 'CE' else ''),
                float(row_data[176]) * quantity_equipment,
                row_data[200]
                ])

        code_nipple = row_data[153]
        if code_nipple:
            trad = row_data[189]
            model = row_data[30]
            parts.append([
                trad,
                '' if model == 'N/A' or model =='' else model,
                '',
                '',
                'A-105/A106' if trad[trad.find('('):trad.find('(')+9] == '(CS)' else 'AISI-316',
                1 * quantity_equipment,
                row_data[201]
                ])

        code_spring = row_data[154]
        if code_spring:
            parts.append([
                row_data[190],
                '',
                '',
                '',
                'AC.INOX',
                1 * quantity_equipment,
                row_data[202]
                ])

        code_puntal = row_data[155]
        if code_puntal:
            parts.append([
                row_data[191],
                '',
                '',
                '',
                row_data[14],
                (float(code_puntal[1:8])/1000 if code_puntal not in ['N/A', 'HO'] else 0) * quantity_equipment,
                row_data[203]
                ])

        code_plug = row_data[156]
        if code_plug:
            trad = row_data[192]
            parts.append([
                trad,
                '',
                '',
                '',
                trad[trad.find('('):trad.find('(')+9],
                1 * quantity_equipment,
                row_data[204]
                ])

        code_tw = row_data[157]
        if code_tw and ('Van-Stone TW' in tw_type or 'Forged' in tw_type):
            parts.append([
                row_data[193],
                'U=' + row_data[16] + ' / L=' + row_data[15],
                '',
                '',
                row_data[14],
                int(row_data[181]) * quantity_equipment,
                row_data[205]
                ])

        code_extcable = row_data[158]
        if code_extcable:
            parts.append([
                row_data[194],
                '',
                '',
                '',
                'AC. INOX.' if row_data[24] in ['AISI-304', 'AISI-310', 'AISI-316', 'AISI-321', 'St.Steel'] else row_data[24],
                (float(row_data[182]) if row_data[182] != '' else 0) * quantity_equipment,
                row_data[206]
                ])

    df = pd.DataFrame(
        parts,
        columns=[
            'descripción','modelo','diseño','proceso',
            'material','cantidad','suministro'
        ]
    )

    df = (
        df.groupby(
            ['descripción','modelo','diseño','proceso','material','suministro']
        )['cantidad']
        .sum()
        .reset_index()
    )

    return df


def level_material_list(proxy, model):
    """
    Processes material raw orders for level items by inserting new entries into the fabrication orders database.

    Args:
        proxy (QAbstractProxyModel): The proxy model containing the current data view.
        model (QAbstractItemModel): The model containing the main data.

    Returns:
        df_final: This function returns a dataframe with the resume of materials.
    """

    def expand_illuminators_from_list(illuminator_list):
        """
        Expand combinations like '1 x 1-I 218-T + 2 x 1-I 228-T'
        mantaining fields and original structure.
        """
        rows = []
        for item in illuminator_list:
            tradcod, model, design, process, material, qty = item

            parts = [p.strip() for p in str(tradcod).split("+")]
            for p in parts:
                match = re.match(r"(\d+)\s*x\s*(1-I\s*\d+-T)", p)
                if match:
                    quantity = int(match.group(1)) * qty
                    illuminator = "ILUMINADOR " + match.group(2).replace(" ", "")
                    rows.append([
                        illuminator, model, design, process, material, quantity
                    ])
        return rows

    parts = []

    proxy_data = proxy.data
    proxy_index = proxy.index

    data = model.data
    index = model.index

    id_list = [
        proxy_data(proxy_index(row, 0))
        for row in range(proxy.rowCount())
        if proxy_data(proxy_index(row, 2)) == "QUOTED"
        and str(proxy_data(proxy_index(row, 5))) == ''
    ]

    row_map = {
        data(index(row, 0)): row
        for row in range(model.rowCount())
    }

    for element in id_list:
        row = row_map.get(element)
        if row is None:
            continue

        row_data = [
            data(index(row, c))
            for c in range(model.columnCount())
        ]

        model_num = row_data[9]
        model_value = model_num[:6] if model_num[2:4] !='HH' else model_num[:7]
        level_type = row_data[8]
        conn_type = row_data[15]
        nipplehexdim = row_data[32][:8]
        nippletubedim = row_data[33][:8]
        cc_length = int(row_data[17])

        code_body = row_data[73]
        if code_body:
            if level_type in ['Transparent', 'Reflex']:
                parts.append([
                    row_data[122],
                    nipplehexdim,
                    '40x40' if model_value[2:3] != 'H' else ('100x50'if model_value[2:4] != 'HH' else '80x40'),
                    (nipplehexdim + '-M'),
                    'A-105' if row_data[10] == 'Carbon Steel' else row_data[10],
                    row_data[75],
                    row_data[185]
                    ])
            else:
                parts.append([
                    data(index(row, 125)),
                    '',
                    '',
                    '',
                    'A-105' if data(index(row, 10)) == 'Carbon Steel' else data(index(row, 10)),
                    data(index(row, 75)),
                    data(index(row, 185))
                    ])

        code_cover = data(index(row, 76))
        if code_cover:
            commands_coverdim = ("""
                SELECT *
                FROM validation_data.level_cover_dim
                WHERE cover = %s
                """)

            try:
                cover_num = model_value[2:6] if model_value[2:4] !='HH' else model_value[3:7]
                cover_num = cover_num[:2] + '1' + cover_num[3:]
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(commands_coverdim,(cover_num,))
                        results=cur.fetchone()
                        length=results[1]
                        bores=results[2]

            except (Exception, psycopg2.DatabaseError) as error:
                MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                            + str(error), "critical")

            parts.append([
                row_data[126],
                ('L=' + str(length)),
                '80x30' if model_value[2:4] != 'HH' else '90x40',
                (str(bores) + ' taladros'),
                'A-105' if row_data[27] == 'Carbon Steel' else row_data[27],
                row_data[78],
                row_data[186]
                ])

        code_bolts = row_data[79]
        if code_bolts :
            parts.append([
                row_data[127],
                'TRANSPARENCIA' if level_type == 'Transparent' else 'REFLEXIÓN',
                '' if model_value[2:4] == 'HH' else ('M10x132 mm' if level_type == 'Transparent' else ''),
                '' if model_value[2:4] == 'HH' else ('cabeza exag 17 e/c' if level_type == 'Transparent' else ''),
                'B7/2H' if level_type in ['Transparent','Reflex'] else row_data[24],
                row_data[81],
                row_data[187]
                ])

        code_nipplehex = row_data[82]
        if code_nipplehex:
            parts.append([
                row_data[128],
                (str((cc_length-int(get_number_before_mm(row_data[125]))-72)/2+22) + ' mm'),
                '',
                '',
                'A-105' if row_data[10] == 'Carbon Steel' else row_data[10],
                row_data[84],
                row_data[188]
                ])

        code_valve = row_data[85]
        if code_valve:
            parts.append([
                row_data[129],
                nipplehexdim[:4] + ' x ' + row_data[20],
                nipplehexdim[-3:] + '-H',
                '',
                'A-105' if row_data[18][-2:] == 'NB' else '316 SS',
                row_data[87],
                row_data[189]
                ])

        code_flangevalve = row_data[88]
        if code_flangevalve:
            parts.append([
                row_data[130],
                '',
                '',
                '',
                'A-105' if row_data[10] == 'Carbon Steel' else row_data[10],
                row_data[90],
                row_data[190]
                ])

        code_dv = row_data[91]
        if code_dv:
            parts.append([
                row_data[131],
                '',
                '',
                '',
                'A-105' if row_data[10] == 'Carbon Steel' else row_data[10],
                row_data[93],
                row_data[191]
                ])

            if row_data[131][:3] == 'VÁL':
                parts.append([
                    'TAPÓN NORMAL ' + row_data[20] + row_data[21],
                    '',
                    '',
                    '',
                    'A-105' if row_data[10] == 'Carbon Steel' else row_data[10],
                    2,
                    'TA ' + row_data[20] + row_data[21]
                    ])

        code_gasket = row_data[100]
        if code_gasket:
            parts.append([
                row_data[134],
                'TRANSPARENCIA' if level_type == 'Transparent' else 'REFLEXIÓN',
                '',
                '',
                'GRAFOIL',
                row_data[102],
                row_data[194]
                ])

        code_glass = row_data[103]
        if code_glass:
            parts.append([
                row_data[135],
                'TRANSPARENCIA' if level_type == 'Transparent' else 'REFLEXIÓN',
                '',
                '',
                'BOROSILICATO',
                row_data[105],
                row_data[195]
                ])

        code_mica = row_data[109]
        if code_mica:
            parts.append([
                row_data[137],
                'TRANSPARENCIA',
                '',
                '',
                'MICA',
                row_data[111],
                row_data[197]
                ])

        code_nippletube = row_data[118]
        if code_nippletube:
            parts.append([
                row_data[140],
                '80 mm',
                '',
                '',
                'A-106' if row_data[10] in ['Carbon Steel','ASTM A350 LF2 CL2'] else row_data[10],
                row_data[120],
                row_data[200]
                ])

        code_antifrost = row_data[121]
        if code_antifrost:
            parts.append([
                row_data[141],
                '',
                '',
                '',
                'METACRILATO',
                row_data[123],
                row_data[201]
                ])

        code_illuminator = row_data[97]
        if code_illuminator:
            item = [
                row_data[133],
                '',
                '',
                '',
                'HIERRO',
                row_data[99],
                row_data[193]
                ]

            for r in expand_illuminators_from_list(item):
                parts.append(r)

        code_scale = row_data[94]
        code_float = row_data[106]

    df = pd.DataFrame(
        parts,
        columns=[
            'descripción','modelo','diseño','proceso',
            'material','cantidad','suministro'
        ]
    )

    df = (
        df.groupby(
            ['descripción','modelo','diseño','proceso','material','suministro']
        )['cantidad']
        .sum()
        .reset_index()
    )

    return df


def others_material_list(proxy, model):
    """
    Processes material raw orders for others items by inserting new entries into the fabrication orders database.

    Args:
        proxy (QAbstractProxyModel): The proxy model containing the current data view.
        model (QAbstractItemModel): The model containing the main data.
        numorder (str): The order number to process.
        numorder_pedmat (str): The base order number for material orders.
        variable (str): A variable that determines the type of processing to be done. The specific usage
                        of this variable is not detailed in the function.

    Returns:
        None: This function does not return a value but modifies the database state.
    """
    parts = []

    list_valves_210 = ['V-9305','V-9575','V-9576','2V-210']

    proxy_data = proxy.data
    proxy_index = proxy.index

    data = model.data
    index = model.index

    id_list = [
        proxy_data(proxy_index(row, 0))
        for row in range(proxy.rowCount())
        if proxy_data(proxy_index(row, 2)) == "QUOTED"
        and str(proxy_data(proxy_index(row, 5))) == ''
    ]

    row_map = {
        data(index(row, 0)): row
        for row in range(model.rowCount())
    }

    for element in id_list:
        row = row_map.get(element)
        if row is None:
            continue

        row_data = [
            data(index(row, c))
            for c in range(model.columnCount())
        ]

        parts = []
        description = row_data[8]

    # Order for 2V-210 valves
        if any(valve in description for valve in list_valves_210):
            model_valve = re.match(r'(V-\d+-[A-Za-z0-9]+)', description).group(0)
            material_valve = (re.match(r'(V-\d+-[A-Za-z0-9]+)(.*)', description).group(2).lstrip(' - ').strip()).split(' / ')[0]
            sch_valve = re.search(r'V-\d+-(\w+)', description).group(1)

            parts.append([
                'VÁLVULA 2V-210 SCH ' + sch_valve + (' BRIDADA ' + description.split(' / ')[1].strip()) if '# RF' in description else '',
                'MOD.: ' + model_valve,
                '',
                '',
                material_valve,
                1,
                ''])

            parts.append(['VOLANTE','VÁLVULA 2V-210 - 1500#','','',material_valve,1, ''])
            parts.append(['ARANDELA VÁLVULA','VÁLVULA 2V-210 - 1500#','','','AC. INOX',1, ''])
            parts.append(['VÁSTAGO','VÁLVULA 2V-210 - 1500#','','','AISI-316 + STELLITE',1, ''])
            parts.append(['GUÍA VÁSTAGO/TUERCA (ø25 x LONG 37 mm) (EXAG 22 ec/ x 6 mm)','VÁLVULA 2V-210 - 1500#','','','AC. INOX' if material_valve == '316' else 'AC. CARBONO',1, ''])
            parts.append(['CAPELLI (HORQUILLA)','VÁLVULA 2V-210 - 1500#','','',material_valve,1, ''])
            parts.append(['FLANGETE','VÁLVULA 2V-210 - 1500#','','',material_valve,1, ''])
            parts.append(['PRENSA (ø25 x LONG 20 mm)','VÁLVULA 2V-210 - 1500#','','','AC. INOX' if material_valve == '316' else 'AC. CARBONO',1, ''])
            parts.append(['EMPAQUETADURA','VÁLVULA 2V-210 - 1500#','','','GRAFITO',1, ''])
            parts.append(['TORNILLO CUADRADO (2 ud. POR VÁLVULA)','VÁLVULA 2V-210 - 1500#','','','AC. INOX',2, ''])
            parts.append(['TORNILLO REDONDO (4 ud. POR VÁLVULA)','VÁLVULA 2V-210 - 1500#','','','AC. INOX',4, ''])
            parts.append(['TUERCAS M10 2H','VÁLVULA 2V-210 - 1500#','','','A1942H',4, ''])
            parts.append(['JUNTA ESPIROMETÁLICA 42x30x3,2mm','VÁLVULA 2V-210 - 1500#','','','AISI-316 + GRAFITO',1, ''])
            parts.append(['CUERPO VÁLVULA 2V-210 - 1500#','','','',material_valve,1, ''])
            parts.append(['ASIENTO (ø20 x 16 mm)','VÁLVULA 2V-210 - 1500#','','','AISI-316 + STELLITE',1, ''])
            parts.append(['BRIDA VÁLVULA '+ description.split(' / ')[1].strip(),'VÁLVULA 2V-210 - 1500#','','',material_valve,1, '']) if '# RF' in description else ''
            parts.append(['TAPÓN PURGADOR 1/2" NPT-M','','','',material_valve,1, ''])
            parts.append(['TORNILLO TAPÓN PURGADOR','','','','AC. INOX',1, ''])
            if len(description.split(' / ')) > 2: 
                parts.append(['NIPLO ' + description.split(' / ')[2],'','','','AC. INOX' if material_valve == '316' else 'AC. CARBONO',1, '']) 

    # Order for CN-32219
        elif 'CN-32219' in description:
            parts.append(['BRIDA BLIND 4" 900# RTJ', 'ø293 x 53 mm', '', '', '321', 1, ''])
            parts.append(['TUBO 1/4" SCH 40S (ø13,5 x ESP 2,3 mm)','(2323x' + 1 +')+(1753x' + 1 + ')+(1183x' + 1 + ')', '', '', '321', str(round(5260 / 1000, 2)), ''])
            parts.append(['TUBO 3" SCH 80S','2664 x ' * 1, '', '', '321', str(round(2680 / 1000, 2)), ''])
            parts.append(['BARRA ø25 x LONG. 30 mm (1/4" NPT-H)','', '', '', '321', 1, ''])
            parts.append(['BARRA ø25 x LONG. 40 mm (1/4" NPT-H x 1/4" SW)','REDUCCIÓN 1/4"SW A 1/4" NPT-H', '', '', '321', 3, ''])
            parts.append(['ACCESORIO FIJACIÓN BARRA ø20 x LONG 34 mm', '', '', '', '321', 3, ''])
            parts.append(['CAP SOLDADO BARRA ø90 x LONG 67 mm', '', '', '', '321', 1, ''])
            parts.append(['EMPTAPÓN DE PURGA 1/4" NPT-M (EXAG. 17 e/c x LONG. 31 mm)AQUETADURA', 'EXAG. 17 e/c (ø20 mm)', '', '', '321', 1, ''])

        elif 'D-3355/2' in description:
            parts.append(['BRIDA DE LÍNEA 5" 600# RF', 'ø331 x 51 mm', '', '', 'AISI-321', 1, ''])
            parts.append(['TUBO 3" SCH XXS', str(len(id_list)) + 'x2430', '', '', 'AISI-321', 2.43, ''])
            parts.append(['CAP 3" SCH XXS (ø88.89 mm X 64 mm)', 'LONGITUD 64 MM', '', '', 'AISI-321', 1, ''])
            parts.append(['MANGUITO 1/4" NPT x 1/4" SW', 'ø25,4 x LONG 35 mm', '', '', 'AISI-321', 3, ''])
            parts.append(['TAPÓM EXAGONAL 1/4" NPT-H (PARA MANGUITO DRENAJE)', 'ø29 x LONG 27 mm', '', '', 'AISI-321', 1, ''])
            parts.append(['MANGUITO DE DRENAJE', 'ø25,4 x LONG 140 mm', 'exag. 25 e/c', '', 'AISI-321', 1, ''])
            parts.append(['TAPÓN DE CONTACTO (VAINA EXTERIOR CON VAINA INTERIOR)', 'ø25 x LONG 42 mm', '', '', 'AISI-321', 3, ''])
            parts.append(['TUBO 1/4" SCH 40S (ø13.5 X 2.3 mm ESP)', str(len(id_list)) + 'x1134', '', '', 'AISI-321', 1.134, ''])
            parts.append(['TUBO 1/4" SCH 40S (ø13.5 X 2.3 mm ESP)', str(len(id_list)) + 'x1654', '', '', 'AISI-321', 1.654, ''])
            parts.append(['TUBO 1/4" SCH 40S (ø13.5 X 2.3 mm ESP)', str(len(id_list)) + 'x2174', '', '', 'AISI-321', 2.174, ''])
            parts.append(['TAPOÓN CIERRES PARA TUBOS 1/4"', 'ø8,9 x LONG 6 MM', 'SALE DE VARILLA ø12', '', 'AISI-321', 3, ''])

        else:
            parts.append([
                str(description),
                '',
                '',
                '',
                '',
                1,
                ''
                ])

    df = pd.DataFrame(
        parts,
        columns=[
            'descripción','modelo','diseño','proceso',
            'material','cantidad','suministro'
        ]
    )

    df = (
        df.groupby(
            ['descripción','modelo','diseño','proceso','material','suministro']
        )['cantidad']
        .sum()
        .reset_index()
    )

    return df


def general_material_list(proxy, model, variable, numoffer):
    id_list = []
    flow_list = []
    temp_list = []
    level_list = []

    query_offer_data = ("SELECT client, project FROM offers WHERE num_offer = %s")

    proxy_data = proxy.data
    proxy_index = proxy.index

    data = model.data
    index = model.index

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cur:
            cur.execute(query_offer_data,(numoffer,))
            results = cur.fetchall()
            client_value = results[0][0]
            project_value = results[0][1]

    id_list = [
        proxy_data(proxy_index(row, 0))
        for row in range(proxy.rowCount())
        if proxy_data(proxy_index(row, 2)) == "QUOTED" and str(proxy_data(proxy_index(row, 5))) == ''
    ]

    row_map = {
        data(index(row, 0)): row
        for row in range(model.rowCount())
    }

    for element in id_list:
        row = row_map.get(element)
        if row is None:
            continue

        row_data = [
            data(index(row, c))
            for c in range(model.columnCount())
        ]

        if variable == 'Caudal':
            # appending [type_value, flange_material_value, element_material_value, size_value, rating_value, facing_value, schedule_value, qty_value]
            flow_list.append([
                row_data[8],
                row_data[13],
                row_data[19],
                row_data[9],
                int(row_data[10]) if row_data[10] != 'N/A' else row_data[10],
                row_data[11],
                row_data[12],
                1 * int(row_data[35])
                ])

        if variable == 'Temperatura':
            # [type_value, tw_type_value, tw_material_value, size_value, rating_value, facing_value, insertion_value, qty_value]
            temp_list.append([
                row_data[8],
                row_data[9],
                row_data[14],
                row_data[10],
                row_data[11] if row_data[11] != 'N/A' else row_data[11],
                row_data[12],
                row_data[16],
                1 * int(row_data[38])
                ])

        if variable == 'Nivel':
            type_value = row_data[8]
            if type_value == 'Magnetic':
                # [type_value, body_material, conn_size, conn_rating, conn_facing, c-c_length, float_material, bolting_material, qty_value]
                level_list.append([
                    row_data[8],
                    row_data[10],
                    row_data[12],
                    int(row_data[13]) if row_data[13] != 'N/A' else row_data[13],
                    row_data[14],
                    row_data[17],
                    row_data[26],
                    row_data[24],
                    1
                    ])
            else:
                # [type_value, body_material, conn_size, conn_rating, conn_facing, c-c_length, cover_material, bolting_material, qty_value]
                level_list.append([
                    row_data[8],
                    row_data[10],
                    row_data[12],
                    int(row_data[13]) if row_data[13] != 'N/A' else row_data[13],
                    row_data[14],
                    row_data[27],
                    row_data[26],
                    row_data[24],
                    1
                    ])

        if variable == 'Others':
            df = None

    if flow_list:
        cols = ['TIPO', 'MAT. BRIDA', 'MAT. ELEMENTO', 'TAMAÑO', 'RATING', 'FACING', 'SCHEDULE', 'Nº EQUIPOS']
        df = pd.DataFrame(flow_list, columns=cols)

    if temp_list:
        cols = ['TIPO', 'TIPO TW', 'MAT. TW', 'TAMAÑO', 'RATING', 'FACING', 'INSERCIÓN', 'Nº EQUIPOS']
        df = pd.DataFrame(temp_list, columns=cols)

    if level_list:
        cols = ['TIPO', 'MAT. CUERPO', 'TAMAÑO', 'RATING', 'FACING', 'LONG. C-C', 'MAT. CUBIERTA / FLOTADOR', 'MAT. TORN', 'Nº EQUIPOS']
        df = pd.DataFrame(level_list, columns=cols)

    return df
