from utils.Database_Manager import Database_Connection
from config.config_functions import config_database, get_path
import psycopg2
from datetime import *
import os
import pandas as pd
from pypdf import PdfReader, PdfWriter, PageObject
from utils.Show_Message import MessageHelper
from utils.Helpers import FLOW_COLUMNS, TEMP_COLUMNS, LEVEL_COLUMNS, OTHERS_COLUMNS
from config.config_keys import ORDERS_PATH
from windows.overlay_pdf import (dwg_of_op_ro_rf, dwg_of_op_ro_rtj, dwg_of_ms_ro,
                                dwg_of_thermowell, dwg_of_sensor)
from psycopg2 import sql
from psycopg2.extras import execute_batch


def generate_of_drawings(numorder, list_drawings):
    query_select_drawings_flow = ("""
                SELECT id_tag_flow, item_type, line_size, rating, facing, element_material, plate_type, of_drawing, rtj_thickness, plate_thk, 'tags_data.tags_flow' as table, 'id_tag_flow' as id_column, tag
                FROM tags_data.tags_flow
                WHERE num_order ILIKE %s AND tag_state = 'PURCHASED' AND COALESCE(UPPER(position), '') NOT LIKE '%%ZZZ%%'
                ORDER BY tag
                """)

    query_select_drawings_temp = ("""
            SELECT id_tag_temp, item_type, tw_type, size, rating, facing, material_tw, std_length, ins_length, root_diam, tip_diam, base_tw_diam, geometry,
            of_sensor_drawing, sensor_element, sheath_stem_material, insulation, nipple_ext_material, head_case_material,
            of_drawing, 'tags_data.tags_temp' as table, 'id_tag_temp' as id_column, tag
            FROM tags_data.tags_temp
            WHERE num_order ILIKE %s AND tag_state = 'PURCHASED' AND COALESCE(UPPER(position), '') NOT LIKE '%%ZZZ%%'
            ORDER BY tag
            """)

    query_update = sql.SQL("UPDATE {table} SET of_drawing = %s WHERE {id_column} = %s")

    query_update_sensor = sql.SQL("UPDATE {table} SET of_sensor_drawing = %s WHERE {id_column} = %s")

    query_tags_data = sql.SQL("""SELECT *
                        FROM {table}
                        WHERE num_order ILIKE %s
                            AND tag_state = 'PURCHASED'
                            AND COALESCE(UPPER(position), '') NOT LIKE '%%ZZZ%%'""")

    GROUP_SENSOR_COLS = ["sensor_element", "sheath_stem_material", "insulation", "nipple_ext_material", "head_case_material"]

    GROUP_COLS_BY_TABLE = {
        'tags_data.tags_flow':   ["item_type", "line_size", "rating", "facing", "element_material", "plate_type", "rtj_thickness", "plate_thk"],
        'tags_data.tags_temp':   ["item_type", "tw_type", "size", "rating", "facing", "material_tw", "std_length", "ins_length", "root_diam", "tip_diam", "base_tw_diam", "geometry"],
        }

    TABLE_CONFIG = {
        "tags_data.tags_flow": {
        "query": query_select_drawings_flow,
        "columns": ["id", "item_type", "line_size", "rating", "facing", "element_material", "plate_type", "of_drawing", "rtj_thickness", "plate_thk", "table", "id_column", "tag"],
        "id_column": "id_tag_flow"},

        "tags_data.tags_temp": {
        "query": query_select_drawings_temp,
        "columns": ["id", "item_type", "tw_type", "size", "rating", "facing", "material_tw", "std_length", "ins_length", "root_diam", "tip_diam",
                    "base_tw_diam", "geometry", "of_sensor_drawing", "sensor_element", "sheath_stem_material", "insulation", "nipple_ext_material", "head_case_material",
                    "of_drawing", "table", "id_column", "tag"],
        "id_column": "id_tag_temp"}
        }

    order_year = str(datetime.now().year)[:2] + numorder[numorder.rfind("/") - 2:numorder.rfind("/")]

    path = ORDERS_PATH / f"Año {order_year}" / (f"{order_year} Pedidos Almacen" if numorder[:2] == 'PA' else f"{order_year} Pedidos")
    for folder in sorted(os.listdir(path)):
        if 'S00' in numorder:
            if numorder[:8].replace("/", "-") in folder:
                output_path_OF = path / folder / "3-Fabricacion" / "Planos OF"
                break
        else:
            if numorder.replace("/", "-") in folder:
                output_path_OF = path / folder / "3-Fabricacion" / "Planos OF"
                break

    if not os.path.exists(output_path_OF):
        os.makedirs(output_path_OF)

    try:
        dfs = []

        with Database_Connection(config_database()) as conn:
            for table_name, cfg in TABLE_CONFIG.items():
                df = load_df_from_query(
                    conn,
                    cfg["query"],
                    (f"%{numorder}%",),
                    cfg["columns"],
                    table_name,
                    cfg["id_column"]
                )

                if not df.empty:
                    dfs.append(df)

        df_final = pd.concat(dfs, ignore_index=True, sort=False)

        existing_of = df_final["of_drawing"].dropna()
        if not existing_of.empty:
            last_drawing = existing_of.str.split("-", expand=True)[1].astype(int).max()
        else:
            last_drawing = 0

        current = last_drawing + 1

        mask_flow = (
            (df_final["table"] == "tags_data.tags_flow") &
            (df_final["of_drawing"].isna() | (df_final["of_drawing"].astype(str).str.strip() == ""))
        )
        if mask_flow.any():
            current = assign_of(
                df=df_final,
                mask_base=mask_flow,
                group_cols=GROUP_COLS_BY_TABLE["tags_data.tags_flow"],
                current=current,
                target_col="of_drawing"
            )

        if "of_sensor_drawing" in df_final.columns:
            mask_sensor = (
                (df_final["table"] == "tags_data.tags_temp") &
                (df_final["sensor_element"].notna() &(df_final["sensor_element"].astype(str).str.strip() != "N/A")) &
                (df_final["of_sensor_drawing"].isna() | (df_final["of_sensor_drawing"].astype(str).str.strip() == ""))
            )
            if mask_sensor.any():
                current = assign_of(
                    df=df_final,
                    mask_base=mask_sensor,
                    group_cols=GROUP_SENSOR_COLS,
                    current=current,
                    target_col="of_sensor_drawing"
                )

        mask_temp = (
            (df_final["table"] == "tags_data.tags_temp") & 
            (df_final["of_drawing"].isna() | (df_final["of_drawing"].astype(str).str.strip() == ""))
        )
        if mask_temp.any():
            current = assign_of(
                df=df_final,
                mask_base=mask_temp,
                group_cols=GROUP_COLS_BY_TABLE["tags_data.tags_temp"],
                current=current,
                target_col="of_drawing"
            )

        try:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    for table_name in df_final["table"].unique():
                        rows = df_final[df_final["table"] == table_name]
                        if rows.empty:
                            continue

                        schema, table = table_name.split(".")
                        id_col = sql.Identifier(rows.iloc[0]["id_column"])

                        # SENSOR (solo TEMP)
                        if table_name == "tags_data.tags_temp":
                            data_sensor = [
                                (r["of_sensor_drawing"], r["id"])
                                for _, r in rows.iterrows() if pd.notna(r["of_sensor_drawing"])
                            ]
                            if data_sensor:
                                execute_batch(
                                    cur,
                                    query_update_sensor.format(table=sql.Identifier(schema, table), id_column=id_col),
                                    data_sensor,
                                    page_size=100
                                )

                        # OF_DRAWING
                        data_drawing = [
                            (r["of_drawing"], r["id"])
                            for _, r in rows.iterrows() if pd.notna(r["of_drawing"])
                        ]
                        if data_drawing:
                            execute_batch(
                                cur,
                                query_update.format(table=sql.Identifier(schema, table), id_column=id_col),
                                data_drawing,
                                page_size=100
                            )
                conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            MessageHelper.show_message("Ha ocurrido el siguiente error:\n" + str(error), "critical")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error, 'error')
        MessageHelper.show_message("Ha ocurrido un error:\n"
                    "Los planos no se han podido generar", "critical")

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                query_of_flow = ("SELECT of_drawing FROM tags_data.tags_flow WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND COALESCE(UPPER(position), '') NOT LIKE '%%ZZZ%%'")
                cur.execute(query_of_flow,(f"%{numorder}%",))
                results_tags_flow=cur.fetchall()

                query_of_temp = ("SELECT of_drawing, of_sensor_drawing FROM tags_data.tags_temp WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND COALESCE(UPPER(position), '') NOT LIKE '%%ZZZ%%'")
                cur.execute(query_of_temp,(f"%{numorder}%",))
                results_tags_temp=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    df_flow = pd.DataFrame(results_tags_flow, columns=['of_drawing'])
    df_temp = pd.DataFrame(results_tags_temp, columns=['of_drawing', 'of_sensor_drawing'])

    count_of_drawings = pd.concat([
            df_flow['of_drawing'],
            df_temp['of_drawing'],
            df_temp['of_sensor_drawing']
        ]).nunique()

    try:
    # Loop through different types of equipment and create drawings accordingly
        for table in df_final["table"].unique():
            if table == 'tags_data.tags_flow':
                try:
                    schema, table_name = table.split(".")
                    query = query_tags_data.format(table=sql.Identifier(schema, table_name))
                    params = [f"%{numorder}%"]

                    if list_drawings:
                        query += sql.SQL(" AND of_drawing = ANY(%s)")
                        params.append(list_drawings)

                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(query, params)
                            results_tags_flow=cur.fetchall()

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")

                df_flow = pd.DataFrame(results_tags_flow, columns=FLOW_COLUMNS)
                df_flow['of_drawing_date'] = pd.to_datetime(df_flow['of_drawing_date']).dt.strftime('%d/%m/%Y').fillna('')

                for item_type in df_flow["item_type"].unique():
                    if item_type in ['F+P', 'P', 'RO', 'M.RUN']:
                        df_final = df_flow[df_flow['item_type'] == item_type].copy()

                        grouped_plates = create_df_orifice_plates(df_final)

                        for _, row in grouped_plates.iterrows():
                            writer = PdfWriter()

                            of_drawing_path = row["of_drawing_path"]
                            if of_drawing_path is None or not os.path.exists(of_drawing_path):
                                MessageHelper.show_message(f"La ruta está vacía o el plano {row['of_drawing_path']} no se ha encontrado en la ruta especificada.", "warning")
                                continue

                            reader = PdfReader(of_drawing_path)
                            base_page_template = reader.pages[0]

                            if 'RF' in row['connection'] or 'FF' in row['connection']:
                                pdf_buffer = dwg_of_op_ro_rf(item_type, numorder, count_of_drawings, row["connection"], row["element_material"], row["of_drawing"], row["of_drawing_date"], row["of_drawing_rev"],
                                                                row["handle_height"], row["handle_width"], row["handle_thickness"], row["plate_c_dim"], row["plate_ext_diam"], row["plate_type"],
                                                                zip(row["tag"], row["line_size"], row["rating"], row["facing"], row["schedule"], row["element_material"], row["pipe_int_diam"],
                                                                row["orif_diam"], row["plate_thk"], row["dv_diam"], row["w_diam"], row["count"], row["of_drawing_rev"]))

                            elif 'RTJ' in row['connection']:
                                pdf_buffer = dwg_of_op_ro_rtj(item_type, numorder, count_of_drawings, row["connection"], row["element_material"], row["of_drawing"], row["of_drawing_date"], row["of_drawing_rev"],
                                                                row["plate_c_dim"], row["rtj_thickness"], row["plate_type"], row["handle_height"],
                                                                zip(row["tag"], row["line_size"], row["rating"], row["facing"], row["schedule"], row["element_material"], row["pipe_int_diam"],
                                                                row["orif_diam"], row["plate_thk"], row["dv_diam"], row["w_diam"], row["count"]))

                            pdf_overlay = PdfReader(pdf_buffer)

                            for overlay_page in pdf_overlay.pages:
                                base_page = PageObject.create_blank_page(
                                    width=base_page_template.mediabox.width,
                                    height=base_page_template.mediabox.height
                                )
                                base_page.merge_page(base_page_template)
                                base_page.merge_page(overlay_page)
                                writer.add_page(base_page)

                            writer.write(str(output_path_OF / f"{row["of_drawing"][:5]}.pdf"))

                    elif item_type == "MULTISTAGE RO":
                        df_final = df_flow[df_flow['item_type'] == item_type].copy()

                        grouped_ms = create_df_multistage_ro(df_final)

                        for _, row in grouped_ms.iterrows():
                            writer = PdfWriter()
                            of_drawing_path = row["of_drawing_path"]

                            if of_drawing_path is None or not os.path.exists(of_drawing_path):
                                MessageHelper.show_message(f"La ruta está vacía o el plano {row['of_drawing_path']} no se ha encontrado en la ruta especificada.", "warning")
                                continue

                            reader = PdfReader(of_drawing_path)
                            base_page_template = reader.pages[0]
                            pdf_buffer = dwg_of_ms_ro(numorder, count_of_drawings,
                                            row["flange_material"], row["tube_material"], row["element_material"],
                                            row["of_drawing"],
                                            zip(row["tag"], row["line_size"], row["rating"], row["facing"], row["schedule"],
                                                row["stages_number"], row["pipe_int_diam"], row["aprox_length"], row["nace"], row["count"]))
                            pdf_overlay = PdfReader(pdf_buffer)
                            
                            for overlay_page in pdf_overlay.pages:
                                base_page = PageObject.create_blank_page(
                                    width=base_page_template.mediabox.width,
                                    height=base_page_template.mediabox.height
                                )
                                base_page.merge_page(base_page_template)
                                base_page.merge_page(overlay_page)
                                writer.add_page(base_page)

                            writer.write(str(output_path_OF / f"{row["of_drawing"][:5]}.pdf"))

            elif table == 'tags_data.tags_temp':
                try:
                    schema, table_name = table.split(".")
                    query = query_tags_data.format(table=sql.Identifier(schema, table_name))

                    params = [f"%{numorder}%"]
                    if list_drawings:
                        query += sql.SQL(" AND (of_drawing = ANY(%s) OR of_sensor_drawing = ANY(%s))")
                        params.extend([list_drawings, list_drawings])

                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(query, params)
                            results_tags_temp = cur.fetchall()

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")

                df_temp = pd.DataFrame(results_tags_temp, columns=TEMP_COLUMNS)
                df_temp['of_drawing_date'] = pd.to_datetime(df_temp['of_drawing_date']).dt.strftime('%d/%m/%Y').fillna('')
                df_temp['of_sensor_drawing_date'] = pd.to_datetime(df_temp['of_sensor_drawing_date']).dt.strftime('%d/%m/%Y').fillna('')

                for item_type in df_temp["item_type"].unique():
                    if item_type in ['TW+TE', 'TW+TE+TIT']:
                        df_final = df_temp[df_temp['item_type'] == item_type].copy()

                        grouped_sensors = create_df_sensors(df_final)

                        for _, row in grouped_sensors.iterrows():
                            writer = PdfWriter()

                            of_drawing_filename = f"{row['of_sensor_drawing_path']}.pdf"
                            of_drawing_path = get_path("4 PLANOS AUTOMATICOS", "OF", "02 TEMPERATURA", of_drawing_filename)

                            if of_drawing_path is None or not os.path.exists(of_drawing_path):
                                continue

                            reader = PdfReader(of_drawing_path)
                            base_page_template = reader.pages[0]

                            pdf_buffer = dwg_of_sensor(numorder, count_of_drawings, row["sensor_element"], row["sheath_stem_material"], row["sheath_stem_diam"],
                                        row["insulation"], row["nipple_ext_material"], row["head_case_material"], row["head_certification"], row["elec_conn_case_diam"],
                                        row["of_sensor_drawing"], zip(row["tag"], row["dim_a_sensor"], row["dim_b_sensor"], row["dim_l_sensor"], row["of_sensor_drawing_rev"]))

                            pdf_overlay = PdfReader(pdf_buffer)

                            for overlay_page in pdf_overlay.pages:
                                base_page = PageObject.create_blank_page(
                                    width=base_page_template.mediabox.width,
                                    height=base_page_template.mediabox.height
                                )
                                base_page.merge_page(base_page_template)
                                base_page.merge_page(overlay_page)
                                writer.add_page(base_page)

                            writer.write(str(output_path_OF / f"{row["of_sensor_drawing"][:5]}.pdf"))

                        grouped_tw = create_df_thermowells(df_final)

                        for _, row in grouped_tw.iterrows():
                            writer = PdfWriter()

                            of_drawing_filename = f"{row['of_drawing_path']}.pdf"
                            of_drawing_path = get_path("4 PLANOS AUTOMATICOS", "OF", "02 TEMPERATURA", of_drawing_filename)

                            if of_drawing_path is None or not os.path.exists(of_drawing_path):
                                continue

                            reader = PdfReader(of_drawing_path)
                            base_page = reader.pages[0]

                            pdf_buffer = dwg_of_thermowell(row["tw_type"], numorder, count_of_drawings, row["connection"], row["material_tw"],
                                        row["base_tw_diam"], row["std_length"], row["ins_length"],
                                        row["root_diam"], row["tip_diam"], row["bore_diam"], row["tip_thk"], row["radius_dim"],
                                        row["conical_length"], row["straight_length"], row["puntal"],
                                        row["of_drawing"], zip(row["tag"], row["of_drawing_rev"]))

                            page_overlay = PdfReader(pdf_buffer).pages[0]
                            
                            base_page.merge_page(page2=page_overlay)
                            writer.add_page(base_page)

                            writer.write(str(output_path_OF / f"{row["of_drawing"][:5]}.pdf"))

                    elif item_type in ['TW', 'TW+BIM']:
                        df_final = df_temp[df_temp['item_type'] == item_type].copy()

                        grouped_tw = create_df_thermowells(df_final)

                        for _, row in grouped_tw.iterrows():
                            writer = PdfWriter()

                            of_drawing_filename = f"{row['of_drawing_path']}.pdf"
                            of_drawing_path = get_path("4 PLANOS AUTOMATICOS", "OF", "02 TEMPERATURA", of_drawing_filename)

                            if of_drawing_path is None or not os.path.exists(of_drawing_path):
                                continue

                            reader = PdfReader(of_drawing_path)
                            base_page = reader.pages[0]

                            pdf_buffer = dwg_of_thermowell(row["tw_type"], numorder, count_of_drawings, row["connection"], row["material_tw"],
                                        row["base_tw_diam"], row["std_length"], row["ins_length"],
                                        row["root_diam"], row["tip_diam"], row["bore_diam"], row["tip_thk"], row["radius_dim"],
                                        row["conical_length"], row["straight_length"], row["puntal"],
                                        row["of_drawing"], zip(row["tag"], row["of_drawing_rev"]))

                            page_overlay = PdfReader(pdf_buffer).pages[0]

                            base_page.merge_page(page2=page_overlay)
                            writer.add_page(base_page)

                            writer.write(str(output_path_OF / f"{row["of_drawing"][:5]}.pdf"))

        MessageHelper.show_message("Planos Generados", "info")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error, 'error2')
        MessageHelper.show_message("Ha ocurrido un error:\n"
                    "Los planos no se han podido generar", "critical")


def load_df_from_query(conn, query, params, columns, table_name, id_column):
    with conn.cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()

    if not rows:
        return pd.DataFrame(columns=columns)

    df = pd.DataFrame(rows, columns=columns)
    df["table"] = table_name
    df["id_column"] = id_column

    return df

def assign_of(df, mask_base, group_cols, current, target_col):
    df_work = df.loc[mask_base].copy()

    df_work["_grp"] = df_work[group_cols].fillna("__NULL__").groupby(group_cols).ngroup()

    for grp_id in df_work["_grp"].unique():
        of_value = f"OF-{current:02d}"
        current += 1

        mask_grp = mask_base & (df_work["_grp"] == grp_id).reindex(df.index, fill_value=False)
        df.loc[mask_grp, target_col] = of_value

    return current


def create_df_orifice_plates(dataframe):
    df_plates = dataframe.copy()
    df_plates = df_plates.fillna('')

    df_plates['connection'] = df_plates.apply(
    lambda row: row['line_size'].split('"/')[1] if '"/' in row['line_size'] else row['line_size'] + " " + row['rating'] + "# " + row['facing'],
    axis=1)

    df_plates['w_diam'] = df_plates.apply(
    lambda row: str(0.5 + float(row['dv_diam'].split('=')[1].replace(',','.')) / 2) if str(row['dv_diam']) not in ('None', '', 'N/A', 'N.A.') else '',
    axis=1)

    df_plates = df_plates.sort_values(by="tag")

    grouped_plates = df_plates.groupby(['plate_type', 'of_drawing_path', 'connection', 'of_drawing', 'of_drawing_date',
        'plate_ext_diam', 'plate_c_dim', 'handle_height', 'handle_width', 'handle_thickness', 'rtj_thickness']).agg(
        {"tag": list, "line_size": list, "rating": list, "facing": list, "schedule": list, "element_material": list, "pipe_int_diam": list,
        "orif_diam": list, "plate_thk": list, "dv_diam": list, "w_diam": list, 'of_drawing_rev': list}
        ).reset_index()

    grouped_plates["count"] = grouped_plates["tag"].apply(lambda x: [1] * len(x))

    return grouped_plates

def create_df_thermowells(dataframe):
    df_tw = dataframe.copy()
    df_tw = df_tw.fillna('')

    df_tw['connection'] = df_tw.apply(
    lambda row: row['size'] + " " + row['rating'] + "# " + row['facing'],
    axis=1)

    df_tw = df_tw.sort_values(by="tag")

    grouped_tw = df_tw.groupby(['of_drawing_path', 'tw_type', 'connection', 'of_drawing', 'of_drawing_date', 'material_tw',
                                'base_tw_diam', 'geometry', 'std_length', 'ins_length',
                                'root_diam', 'tip_diam', 'bore_diam', 'tip_thk', 'radius_dim', 'conical_length', 'straight_length', 'puntal']).agg({"tag": list, "of_drawing_rev": list}).reset_index()

    return grouped_tw

def create_df_sensors(dataframe):
    df_sensors = dataframe.copy()
    df_sensors = df_sensors.fillna('')

    # df_sensors = df_sensors.sort_values(by="tag")

    df_sensors["dim_l_sensor_float"] = df_sensors["dim_l_sensor"].astype(float)
    df_sensors = df_sensors.sort_values(["dim_l_sensor_float", "tag"]).drop(columns="dim_l_sensor_float")

    grouped_sensors = df_sensors.groupby(['of_sensor_drawing_path', 'of_sensor_drawing', 'of_sensor_drawing_date', 'sensor_element', 'sheath_stem_material', 'sheath_stem_diam',
                                'insulation', 'nipple_ext_material', 'head_case_material', 'head_certification', 'elec_conn_case_diam']).agg(
                                    {"tag": list, "dim_a_sensor": list, "dim_b_sensor": list, "dim_l_sensor": list, "of_sensor_drawing_rev": list}).reset_index()

    return grouped_sensors

def create_df_multistage_ro(dataframe):
    df_ms_ro = dataframe.copy()
    df_ms_ro = df_ms_ro.fillna('')

    df_ms_ro = df_ms_ro.sort_values(by="tag")

    grouped_ms_ro = df_ms_ro.groupby(['of_drawing_path', 'of_drawing', 'flange_material', 'tube_material', 'element_material',
                                    'rtj_thickness', 'rtj_r_type', 'rtj_p_diam', 'rtj_e_dim', 'rtj_f_dim']).agg(
                                        {"tag": list, "line_size": list, "rating": list, "facing": list, "schedule": list,
                                        "stages_number": list, "pipe_int_diam": list, "aprox_length": list, "nace": list}).reset_index()

    grouped_ms_ro["count"] = grouped_ms_ro["tag"].apply(lambda x: [1] * len(x))
    
    return grouped_ms_ro
