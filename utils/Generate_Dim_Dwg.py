from PySide6 import QtWidgets, QtCore
from utils.Database_Manager import Database_Connection
from config.config_functions import config_database, get_path
from utils.Show_Message import MessageHelper
import psycopg2
import os
from datetime import *
import re
import pandas as pd
from config.config_keys import ORDERS_PATH
from psycopg2 import sql
from psycopg2.extras import execute_batch
from pypdf import PdfReader, PdfWriter
from windows.overlay_pdf import (dwg_dim_flange_plate, dwg_dim_plate, dwg_dim_ro, dwg_dim_ms_ro, dwg_dim_mrun, dwg_dim_venturi, dwg_dim_nozzle,
                                dwg_dim_thermowell,
                                dwg_dim_glass_level,
                                dwg_dim_flange_plate_riyas, dwg_dim_mrun_riyas)
from utils.Helpers import FLOW_COLUMNS, TEMP_COLUMNS, LEVEL_COLUMNS, OTHERS_COLUMNS


def generate_dim_drawings(numorder, client, final_client, project, list_drawings):
    query_tags_data = sql.SQL("""
                            SELECT * FROM {table}
                            WHERE num_order ILIKE %s
                                AND tag_state = 'PURCHASED'
                                AND COALESCE(UPPER(position), '') NOT LIKE '%%ZZZ%%'
                            """)

    query_select_drawings = ("""
            SELECT * FROM (
                SELECT id_tag_flow, dim_drawing, 'tags_data.tags_flow' as table, 'id_tag_flow' as id_column, tag
            FROM tags_data.tags_flow
            WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND COALESCE(UPPER(position), '') NOT LIKE '%%ZZZ%%'
            ORDER BY tag) t_flow

            UNION ALL

            SELECT * FROM (
                SELECT id_tag_temp, dim_drawing, 'tags_data.tags_temp' as table, 'id_tag_temp' as id_column, tag
            FROM tags_data.tags_temp
            WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND COALESCE(UPPER(position), '') NOT LIKE '%%ZZZ%%'
            ORDER BY tag) t_temp

            UNION ALL

            SELECT * FROM (
                SELECT id_tag_level, dim_drawing, 'tags_data.tags_level_new' as table, 'id_tag_level' as id_column, tag
            FROM tags_data.tags_level_new
            WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND COALESCE(UPPER(position), '') NOT LIKE '%%ZZZ%%'
            ORDER BY tag) t_level

            UNION ALL

            SELECT * FROM (
                SELECT id_tag_others, dim_drawing, 'tags_data.tags_others' as table, 'id_tag_others' as id_column, tag
            FROM tags_data.tags_others
            WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND COALESCE(UPPER(position), '') NOT LIKE '%%ZZZ%%'
            ORDER BY tag) t_others
            """)

    query_update_drawings = sql.SQL("""
                                    UPDATE {table}
                                    SET dim_drawing = %s
                                    WHERE {id_column} = %s
                                    """)

    output_path_Dim = None
    order_year = str(datetime.now().year)[:2] + numorder[numorder.rfind("/") - 2:numorder.rfind("/")]

    path = ORDERS_PATH / f"Año {order_year}" / (f"{order_year} Pedidos Almacen" if numorder[:2] == 'PA' else f"{order_year} Pedidos")
    for folder in sorted(os.listdir(path)):
        if 'S00' in numorder:
            if numorder[:8].replace("/", "-") in folder:
                output_path_Dim = path / folder / "3-Fabricacion" / "Planos Dimensionales"
                break
        else:
            if numorder.replace("/", "-") in folder:
                output_path_Dim = path / folder / "3-Fabricacion" / "Planos Dimensionales"
                break

    if not os.path.exists(output_path_Dim):
        os.makedirs(output_path_Dim)

# Fetch tags and existing drawings
    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query_select_drawings,(numorder, numorder, numorder, numorder,))
                
                results_tags_drawings=cur.fetchall()
                df_final = pd.DataFrame(results_tags_drawings, columns=["id", "dim_drawing", "table", "id_column", "tag"])

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

# Set drawing number to tags without drawing
    try:
        mask_new = df_final["dim_drawing"].isna() | (df_final["dim_drawing"] == "")

        last_drawing = (df_final.loc[~mask_new, "dim_drawing"].str.split("-", expand=False).str[-1].astype(int).max())
        if pd.isna(last_drawing):
            last_drawing = 0

        start = last_drawing + 1
        qty_new = mask_new.sum()
        total = len(df_final)
        num_width = 2 if len(str(total)) < 2 else len(str(total))

        # df_final.loc[mask_new, "dim_drawing"] = [f"{i:0{num_width}d}/{total}" for i in range(start, start + qty_new)]

        df_final.loc[mask_new, "dim_drawing"] = [re.sub(r"^P-", "", numorder).replace("/", "-") + "-" + f"{i:0{num_width}d}" for i in range(start, start + qty_new)]

        try:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    for table_name in df_final["table"].dropna().unique():
                        rows = df_final[df_final["table"] == table_name]

                        schema, table = table_name.split(".")
                        
                        query = query_update_drawings.format(
                            table=sql.Identifier(schema, table),
                            id_column=sql.Identifier(rows.iloc[0]["id_column"])
                        )

                        data = [
                            (row["dim_drawing"], row["id"])
                            for _, row in rows.iterrows()
                        ]

                        execute_batch(cur, query, data, page_size=100)
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                        + str(error), "critical")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        MessageHelper.show_message("Ha ocurrido un error numerando planos:\n"
                    "Los planos no se han podido generar", "critical")

# Selecting framework for drawings
    framework, ok = QtWidgets.QInputDialog.getItem(None, "Cajetín", "Selecciona un tipo de cajetín:", ['EIPSA', 'Otro'], 0, False)
    framework_folder = None

    if ok and framework:
        if framework == 'EIPSA':
            framework_folder = 'EIPSA'

        elif framework == 'Otro':
            framework_folder = '-'.join(numorder.split('-')[:2]).replace('/', '-')

    if not framework_folder:
        MessageHelper.show_message("No se ha seleccionado un tipo de cajetín:\n"
                    "Los planos no se han podido generar", "critical")
        return

# Drawing generation
    try:
        for table in df_final["table"].unique():
            if table == 'tags_data.tags_flow':
                try:
                    schema, table_name = table.split(".")
                    query = query_tags_data.format(table=sql.Identifier(schema, table_name))

                    params = [f"%{numorder}%"]
                    if list_drawings:
                        query += sql.SQL(" AND dim_drawing = ANY(%s)")
                        params.append(list_drawings)

                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(query, params)
                            results_tags_flow = cur.fetchall()

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")

                df_flow = pd.DataFrame(results_tags_flow, columns=FLOW_COLUMNS)

                df_flow['dim_drawing_date'] = pd.to_datetime(df_flow['dim_drawing_date']).dt.strftime('%d/%m/%Y').fillna('')

                for _, row in df_flow.iterrows():
                    writer = PdfWriter()

                    if row["item_type"] == "F+P":
                        drawing_path = row["dim_drawing_path"]
                        if drawing_path is None or not os.path.exists(drawing_path):
                            continue

                        reader = PdfReader(drawing_path)
                        base_page = reader.pages[0]
                        if 'P-24/066' in numorder :
                            pdf_buffer = dwg_dim_flange_plate_riyas(numorder, row["tag"],
                                            row["line_size"], row["schedule"], row["rating"], row["facing"],
                                            row["pipe_int_diam"], row["orif_diam"], row["plate_thk"], row["dv_diam"], row["nace"], row['tapping_size'], row["tapping_orientation"], row["aprox_weight"],
                                            row["o_flange"], row["a_flange"], row["c_flange"], row["y_flange"], row["x_flange"], row["r_flange"], row["d_flange"], row["t_flange"], row["bolts_quantity"], row["bore_bolts_diam"],
                                            row["handle_height"], row["handle_width"], row["plate_c_dim"], row["plate_ext_diam"],
                                            row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"], row["plate_type"],
                                            client, final_client, project, row["num_po"],
                                            row["flange_material"], row["bolts_material"], row["nuts_material"], row["element_material"], row["gasket_material"], row["plug_quantity"], row["plug_material"], row["jack_screw_material"],
                                            row["notes_flange"], row["notes_stud"], row["notes_nut"], row["notes_plate"], row["notes_gasket"], row["notes_plugs"], row["notes_jack_screw"],
                                            row["dim_drawing"], row["dim_drawing_date"], total)
                        else:
                            pdf_buffer = dwg_dim_flange_plate(numorder, row["tag"],
                                            row["line_size"], row["schedule"], row["rating"], row["facing"],
                                            row["pipe_int_diam"], row["orif_diam"], row["plate_thk"], row["dv_diam"], row["nace"], row['tapping_size'], row["aprox_weight"],
                                            row["o_flange"], row["a_flange"], row["c_flange"], row["y_flange"], row["x_flange"], row["r_flange"], row["d_flange"], row["t_flange"], row["bolts_quantity"], row["bore_bolts_diam"],
                                            row["handle_height"], row["handle_width"], row["plate_c_dim"], row["plate_ext_diam"],
                                            row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"],
                                            client, final_client, project, row["num_po"],
                                            row["flange_material"], row["bolts_material"], row["nuts_material"], row["element_material"], row["gasket_material"], row["gasket_quantity"],
                                            row["plug_quantity"], row["plug_material"], row["jack_screw_material"],
                                            row["notes_flange"], row["notes_stud"], row["notes_nut"], row["notes_plate"], row["notes_gasket"], row["notes_plugs"], row["notes_jack_screw"],
                                            row["dim_drawing"], total)

                    elif row["item_type"] == "P":
                        drawing_path = row["dim_drawing_path"]
                        if drawing_path is None or not os.path.exists(drawing_path):
                            continue

                        reader = PdfReader(drawing_path)
                        base_page = reader.pages[0]
                        pdf_buffer = dwg_dim_plate(numorder, row["tag"],
                                        row["line_size"], row["schedule"], row["rating"], row["facing"],
                                        row["pipe_int_diam"], row["orif_diam"], row["plate_thk"], row["dv_diam"], row["nace"], row["element_material"],
                                        row["handle_height"], row["handle_width"], row["handle_thickness"], row["plate_c_dim"], row["plate_ext_diam"],
                                        row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"],
                                        client, final_client, project, row["num_po"],
                                        row["dim_drawing"], total)

                    elif row["item_type"] == "RO":
                        drawing_path = row["dim_drawing_path"]
                        if drawing_path is None or not os.path.exists(drawing_path):
                            continue

                        reader = PdfReader(drawing_path)
                        base_page = reader.pages[0]
                        pdf_buffer = dwg_dim_ro(numorder, row["tag"],
                                        row["line_size"], row["schedule"], row["rating"], row["facing"], row["element_material"], row["aprox_weight"],
                                        row["pipe_int_diam"], row["orif_diam"], row["plate_thk"], row["nace"], row["plate_type"],
                                        row["handle_height"], row["handle_width"], row["handle_thickness"], row["plate_ext_diam"],
                                        row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"],
                                        client, final_client, project, row["num_po"],
                                        row["dim_drawing"], total)

                    elif row["item_type"] == "MULTISTAGE RO":
                        drawing_path = row["dim_drawing_path"]
                        if drawing_path is None or not os.path.exists(drawing_path):
                            continue

                        reader = PdfReader(drawing_path)
                        base_page = reader.pages[0]
                        pdf_buffer = dwg_dim_ms_ro(numorder, row["tag"],
                                        row["line_size"], row["schedule"], row["rating"], row["facing"],
                                        row["flange_material"], row["tube_material"], row["element_material"],
                                        row["pipe_int_diam"], row["nace"],
                                        row["stages_number"], row["aprox_length"], row["aprox_weight"],
                                        row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"],
                                        client, final_client, project, row["num_po"],
                                        row["dim_drawing"], total)

                    elif row["item_type"] == "M.RUN":
                        drawing_path = row["dim_drawing_path"]
                        if drawing_path is None or not os.path.exists(drawing_path):
                            continue

                        reader = PdfReader(drawing_path)
                        base_page = reader.pages[0]
                        if 'P-24/066' in numorder :
                            pdf_buffer = dwg_dim_mrun_riyas(numorder, row["tag"],
                                            row["line_size"], row["schedule"], row["rating"], row["facing"],
                                            row["pipe_int_diam"], row["orif_diam"], row["nace"], row['tapping_size'], row["flange_type"],
                                            row["aprox_weight"], row["aprox_length"], row["tube_material"],
                                            row["handle_height"], row["handle_width"], row["plate_c_dim"], row["plate_ext_diam"],
                                            row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"],
                                            client, final_client, project, row["num_po"],
                                            row["flange_material"], row["bolts_material"], row["nuts_material"], row["element_material"], row["gasket_material"], row["plug_quantity"], row["plug_material"], row["jack_screw_material"],
                                            row["notes_flange"], row["notes_stud"], row["notes_nut"], row["notes_plate"], row["notes_gasket"], row["notes_plugs"], row["notes_jack_screw"],
                                            row["dim_drawing"], row["dim_drawing_date"], total)
                        else:
                            pdf_buffer = dwg_dim_mrun(numorder, row["tag"],
                                            row["line_size"], row["schedule"], row["rating"], row["facing"],
                                            row["pipe_int_diam"], row["orif_diam"], row["nace"], row['tapping_size'], row["flange_type"],
                                            row["aprox_weight"], row["aprox_length"], row["tube_material"],
                                            row["handle_height"], row["handle_width"], row["plate_c_dim"], row["plate_ext_diam"],
                                            row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"], row["tapping_number"],
                                            client, final_client, project, row["num_po"],
                                            row["flange_material"], row["bolts_material"], row["nuts_material"], row["element_material"], row["gasket_material"], row["plug_quantity"], row["plug_material"], row["jack_screw_material"],
                                            row["notes_flange"], row["notes_stud"], row["notes_nut"], row["notes_plate"], row["notes_gasket"], row["notes_plugs"], row["notes_jack_screw"],
                                            row["dim_drawing"], total)

                    elif row["item_type"] in ["VFM", "VWM", "VFW", "VWW", "VFC"]:
                        drawing_path = row["dim_drawing_path"]
                        if drawing_path is None or not os.path.exists(drawing_path):
                            continue

                        reader = PdfReader(drawing_path)
                        base_page = reader.pages[0]
                        pdf_buffer = dwg_dim_venturi(numorder, row["item_type"], row["tag"],
                                    row["line_size"], row["schedule"], row["rating"], row["facing"],
                                    row["pipe_int_diam"], row["orif_diam"], row["nace"], row['tapping_size'], row["tapping_number"],
                                    row["aprox_weight"], row["aprox_length"], row["tube_material"], row["cones_material"],
                                    row["a_venturi"], row["d_venturi"], row["e_venturi"], row["f_venturi"], row["g_venturi"], row["c_venturi"], row["h_venturi"], row["t_venturi"],
                                    client, final_client, project, row["num_po"],
                                    row["flange_material"], row["element_material"], row["plug_quantity"], row["plug_material"],
                                    row["notes_flange"], row["notes_plate"], row["notes_plugs"], row["notes_jack_screw"], row["notes_presure_taps"], row["offer_notes"], 
                                    row["dim_drawing"], total)

                    elif 'NOZZLE' in row["item_type"]:
                        drawing_path = row["dim_drawing_path"]
                        if drawing_path is None or not os.path.exists(drawing_path):
                            continue

                        reader = PdfReader(drawing_path)
                        base_page = reader.pages[0]
                        pdf_buffer = dwg_dim_nozzle(numorder, row["tag"],
                                        row["line_size"], row["schedule"], row["rating"], row["facing"],
                                        row["pipe_int_diam"], row["orif_diam"], row["nace"], row['tapping_size'], row["tapping_number"],
                                        row["a_venturi"], row["d_venturi"], row["f_venturi"], row["e_venturi"], row["plateaprox_length_ext_diam"],
                                        row["aprox_weight"], row["tube_material"],
                                        client, final_client, project, row["num_po"],
                                        row["flange_material"], row["element_material"], row["plug_quantity"], row["plug_material"],
                                        row["notes_flange"], row["notes_plate"], row["notes_plugs"],
                                        row["dim_drawing"], total)

                    page_overlay = PdfReader(pdf_buffer).pages[0]

                    base_page.merge_page(page2=page_overlay)
                    writer.add_page(base_page)

                    writer.write(str(output_path_Dim / f'{row["dim_drawing"]}-REV.{row["dim_drawing_rev"]}.pdf'))

            elif table == 'tags_data.tags_temp':
                try:
                    schema, table_name = table.split(".")
                    query = query_tags_data.format(table=sql.Identifier(schema, table_name))

                    params = [f"%{numorder}%"]
                    if list_drawings:
                        query += sql.SQL(" AND dim_drawing = ANY(%s)")
                        params.append(list_drawings)

                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(query, params)
                            results_tags_temp = cur.fetchall()

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")

                df_temp = pd.DataFrame(results_tags_temp, columns=TEMP_COLUMNS)

                df_temp['dim_drawing_date'] = pd.to_datetime(df_temp['dim_drawing_date']).dt.strftime('%d/%m/%Y').fillna('')

                for _, row in df_temp.iterrows():
                    writer = PdfWriter()

                    if row["item_type"] in ["TW", "TW+TE", "TW+TE+TIT"]:
                        framework_path = get_path("4 PLANOS AUTOMATICOS", "CAJETINES", framework_folder, f"{row['item_type']}.pdf")
                        reader = PdfReader(framework_path)
                        base_page = reader.pages[0]

                        dim_drawing_filename = f"{row['dim_drawing_path']}.pdf"
                        dim_drawing_path = get_path("4 PLANOS AUTOMATICOS", "DIMENSIONALES", "02 TEMPERATURA", row["item_type"], dim_drawing_filename)

                        if dim_drawing_path is not None and os.path.exists(dim_drawing_path):
                            page_overlay = PdfReader(dim_drawing_path).pages[0]
                            base_page.merge_page(page2=page_overlay)

                        of_drawing_filename = f"{row['of_drawing_path']}.pdf"
                        of_drawing_path = get_path("4 PLANOS AUTOMATICOS", "DIMENSIONALES", "02 TEMPERATURA", row["item_type"], of_drawing_filename)

                        if of_drawing_path is None or not os.path.exists(of_drawing_path):
                            MessageHelper.show_message(f"No existe el plano {of_drawing_path}", "warning")
                            continue

                        page_overlay = PdfReader(of_drawing_path).pages[0]
                        base_page.merge_page(page2=page_overlay)

                        pdf_buffer = dwg_dim_thermowell(numorder, row["item_type"], row["tag"],
                                    row["ins_length"], row["std_length"], row["sensor_element"], row["wire_size"], row["sheath_stem_diam"], row["sheath_stem_material"], row["nace"],
                                    row["root_diam"], row["tip_diam"], row["bore_diam"], row["tip_thk"], row["radius_dim"],
                                    client, final_client, project, row["num_po"],
                                    row["insulation"], row["elec_conn_case_diam"], row["head_case_material"], row["head_certification"], row["nipple_ext_material"], row["plug"],
                                    row["tw_type"], row["size"], row["rating"], row["facing"], row["material_tw"],
                                    row["dim_drawing"], total)

                        page_overlay = PdfReader(pdf_buffer).pages[0]

                        base_page.merge_page(page2=page_overlay)
                        writer.add_page(base_page)

                        writer.write(str(output_path_Dim / f'{row["dim_drawing"]}-REV.{row["dim_drawing_rev"]}.pdf'))

            elif table == 'tags_data.tags_level_new':
                try:
                    schema, table_name = table.split(".")
                    query = query_tags_data.format(table=sql.Identifier(schema, table_name))

                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(query,(f"%{numorder}%",))
                            results_tags_level=cur.fetchall()

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")

                columns = ["id_tag_level", "tag", "tag_state", "num_offer", "num_order", "num_po", "position", "subposition",
                        "item_type", "model_num", "conn_type", "body_material", "case_cover_material", "gasket_mica", "stud_material", "nuts_material",
                        "nipple_hex", "nipple_hex_material", "valve_type", "valve_conn", "valve_material",
                        "proc_conn_type", "proc_conn_size", "proc_conn_rating", "proc_conn_facing", "proc_conn_material", "visibility", "cc_length", "body_length",
                        "dv_conn", "dv_size", "dv_rating", "dv_facing", "dv_material",
                        "nipple_tub", "nipple_tub_material", "illuminator", "illuminator_connection", "antifrost", "scale_type",
                        "float_material", "flags", "ip_code", "flange_type", "nace", "amount", "offer_notes", "commercial_changes", "contractual_date",
                        "float_dim", "technical_changes", "technical_notes", "dim_drawing", "dim_drawing_rev", "dim_drawing_date",
                        "of_drawing", "of_drawing_rev", "of_date", "dim_drawing_path", "of_drawing_path"]

                df_level = pd.DataFrame(results_tags_level, columns=columns)

                df_level['dim_drawing_date'] = pd.to_datetime(df_level['dim_drawing_date']).dt.strftime('%d/%m/%Y').fillna('')

                for _, row in df_level.iterrows():
                    writer = PdfWriter()

                    if row["item_type"] in ["Transparent", "Reflex"]:
                        drawing_path = row["dim_drawing_path"]
                        if drawing_path is None or not os.path.exists(drawing_path):
                            continue

                        reader = PdfReader(drawing_path)
                        base_page = reader.pages[0]
                        pdf_buffer = dwg_dim_glass_level(numorder, row["tag"], row["item_type"],
                                row["model_num"], row["visibility"], row["cc_length"], row["body_length"],
                                row["proc_conn_type"], row["proc_conn_size"], row["proc_conn_rating"], row["proc_conn_facing"], row["proc_conn_material"], row["nace"],
                                row["body_material"], row["case_cover_material"], row["gasket_mica"], row["nuts_material"], row["stud_material"],
                                row["nipple_hex"], row["nipple_hex_material"], row["valve_type"], row["valve_conn"], row["valve_material"],
                                row["dv_conn"], row["dv_size"], row["dv_rating"], row["dv_facing"], row["dv_material"],
                                row["nipple_tub"], row["nipple_tub_material"], row["illuminator"], row["illuminator_connection"],
                                client, final_client, project, row["num_po"],
                                row["dim_drawing"], total)

                    page_overlay = PdfReader(pdf_buffer).pages[0]

                    base_page.merge_page(page2=page_overlay)
                    writer.add_page(base_page)

                    writer.write(str(output_path_Dim / f'{row["dim_drawing"]}.pdf'))

        MessageHelper.show_message("Planos Generados", "info")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        MessageHelper.show_message("Ha ocurrido un error generando planos:\n"
                    "Los planos no se han podido generar", "critical")