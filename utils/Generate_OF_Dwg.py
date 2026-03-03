from utils.Database_Manager import Database_Connection
from config.config_functions import config_database
import psycopg2
from datetime import *
import os
import pandas as pd
from pypdf import PdfReader, PdfWriter
from utils.Show_Message import MessageHelper
from config.config_keys import ORDERS_PATH
from windows.overlay_pdf import (dwg_of_op_ro_rf, dwg_of_op_ro_rtj,
                                dwg_of_thermowell, dwg_of_sensor)
from psycopg2 import sql
from psycopg2.extras import execute_batch


def generate_of_drawings(numorder):
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
        query_select_drawings_flow = ("""
                SELECT id_tag_flow, item_type, line_size, rating, facing, element_material, plate_type, of_drawing, 'tags_data.tags_flow' as table, 'id_tag_flow' as id_column, tag
                FROM tags_data.tags_flow
                WHERE num_order ILIKE %s AND tag_state = 'PURCHASED' AND position <> 'ZZZ'
                ORDER BY tag
                """)

        query_select_drawings_temp = ("""
                SELECT id_tag_temp, item_type, tw_type, size, rating, facing, material_tw, std_length, ins_length, root_diam, tip_diam, base_tw_diam, geometry,
                of_sensor_drawing, sensor_element, sheath_stem_material, insulation, nipple_ext_material, head_case_material,
                of_drawing, 'tags_data.tags_temp' as table, 'id_tag_temp' as id_column, tag
                FROM tags_data.tags_temp
                WHERE num_order ILIKE %s AND tag_state = 'PURCHASED' AND position <> 'ZZZ'
                ORDER BY tag
                """)

        query_update = sql.SQL("UPDATE {table} SET of_drawing = %s WHERE {id_column} = %s")

        query_update_sensor = sql.SQL("UPDATE {table} SET of_sensor_drawing = %s WHERE {id_column} = %s")

        query_tags_flow = ("SELECT * FROM tags_data.tags_flow WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND position <> 'ZZZ'")

        query_tags_temp = ("SELECT * FROM tags_data.tags_temp WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND position <> 'ZZZ'")

        GROUP_SENSOR_COLS = ["sensor_element", "sheath_stem_material", "insulation", "nipple_ext_material", "head_case_material"]
        
        GROUP_COLS_BY_TABLE = {
            'tags_data.tags_flow':   ["item_type", "line_size", "rating", "facing", "element_material", "plate_type"],
            'tags_data.tags_temp':   ["item_type", "tw_type", "size", "rating", "facing", "material_tw", "std_length", "ins_length", "root_diam", "tip_diam", "base_tw_diam", "geometry"],
            }

        TABLE_CONFIG = {
            "tags_data.tags_flow": {
            "query": query_select_drawings_flow,
            "columns": ["id", "item_type", "line_size", "rating", "facing", "element_material", "plate_type", "of_drawing", "table", "id_column", "tag"],
            "id_column": "id_tag_flow"},

            "tags_data.tags_temp": {
            "query": query_select_drawings_temp,
            "columns": ["id", "item_type", "tw_type", "size", "rating", "facing", "material_tw", "std_length", "ins_length", "root_diam", "tip_diam",
                        "base_tw_diam", "geometry", "of_sensor_drawing", "sensor_element", "sheath_stem_material", "insulation", "nipple_ext_material", "head_case_material",
                        "of_drawing", "table", "id_column", "tag"],
            "id_column": "id_tag_temp"}
            }

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

        mask_flow = (df_final["table"] == "tags_data.tags_flow") & (df_final["of_drawing"].isna() | (df_final["of_drawing"] == ""))
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
                (df_final["of_sensor_drawing"].isna() | (df_final["of_sensor_drawing"] == ""))
            )
            if mask_sensor.any():
                current = assign_of(
                    df=df_final,
                    mask_base=mask_sensor,
                    group_cols=GROUP_SENSOR_COLS,
                    current=current,
                    target_col="of_sensor_drawing"
                )

        mask_temp = (df_final["table"] == "tags_data.tags_temp") & (df_final["of_drawing"].isna() | (df_final["of_drawing"] == ""))
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

        # mask_new = df_final["of_drawing"].isna() | (df_final["of_drawing"] == "")

        # if mask_new.any():
        #     last_drawing = (df_final.loc[~mask_new, "of_drawing"].str.split("/", expand=False).str.split("-", expand=False).str[-1].astype(int).max())

        #     if pd.isna(last_drawing):
        #         last_drawing = 0

        #     current = last_drawing + 1

        #     for table_name, group_cols in GROUP_COLS_BY_TABLE.items():
        #         mask_table_new = (
        #             (df_final["table"] == table_name) &
        #             (df_final["of_drawing"].isna() | (df_final["of_drawing"] == ""))
        #         )

        #         if not mask_table_new.any():
        #             continue

        #         df_table = df_final.loc[mask_table_new].copy()

        #         # Crear grupos robustos (NaN-safe)
        #         df_table["_grp"] = (
        #             df_table[group_cols]
        #             .fillna("__NULL__")
        #             .groupby(group_cols)
        #             .ngroup()
        #         )

        #         for grp_id in df_table["_grp"].unique():

        #             drawing = f"OF-{current:02d}"
        #             current += 1

        #             mask_group = mask_table_new & (
        #                 df_table["_grp"] == grp_id
        #             ).reindex(df_final.index, fill_value=False)

        #             df_final.loc[mask_group, "of_drawing"] = drawing

        #     try:
        #         with Database_Connection(config_database()) as conn:
        #             with conn.cursor() as cur:
        #                 for table_name in df_final["table"].unique():
        #                     rows = df_final[
        #                         (df_final["table"] == table_name) &
        #                         (df_final["of_drawing"].notna())
        #                     ]

        #                     if rows.empty:
        #                         continue

        #                     schema, table = table_name.split(".")
        #                     query = query_update.format(
        #                         table=sql.Identifier(schema, table),
        #                         id_column=sql.Identifier(rows.iloc[0]["id_column"])
        #                     )

        #                     data = [
        #                         (row["of_drawing"], row["id"])
        #                         for _, row in rows.iterrows()
        #                     ]

        #                     execute_batch(cur, query, data, page_size=100)
        #             conn.commit()
        #     except (Exception, psycopg2.DatabaseError) as error:
        #         MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
        #                     + str(error), "critical")

    try:
    # Loop through different types of equipment and create drawings accordingly
        for table_name in df_final["table"].unique():
            if table_name == 'tags_data.tags_flow':
                try:
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(query_tags_flow,(f"%{numorder}%",))
                            results_tags_flow=cur.fetchall()

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")

                columns = ["id_tag_flow", "tag", "tag_state", "num_offer", "num_order", "num_po", "position", "subposition",
                "item_type", "line_size", "rating", "facing", "schedule", "flange_material", "flange_type", "tube_material", "tapping_size",
                "tapping_number", "tapping_orientation", "element_material", "plate_type", "plate_thk", "plate_std", "gasket_material", "bolts_material",
                "nuts_material", "valve_conn", "valve_material_body", "stages_number", "pipe_spec", "aprox_weight", "aprox_length", "nace", "amount", "offer_notes",
                "commercial_changes", "contractual_date", "orif_diam", "dv_diam", "gasket_quantity", "bolts_size", "bolts_quantity", "plug_material", "plug_quantity",
                "jack_screw_material", "jack_screw_size", "jack_screw_quantity", "rtj_porta_material", "rtj_thickness", "rtj_r_type",
                "notes_flange", "notes_stud", "notes_nut", "notes_plate", "notes_gasket", "notes_plugs", "notes_jack_screw",
                "pipe_int_diam", "plate_ext_diam",
                "plate_c_dim", "handle_height", "handle_width", "handle_thickness", "rtj_p_diam", "rtj_e_dim", "rtj_f_dim", "o_flange", "a_flange", "c_flange", "y_flange",
                "x_flange", "r_flange", "d_flange", "t_flange", "bore_bolts_diam", "cones_material", "a_venturi", "d_venturi", "e_venturi", "f_venturi", "g_venturi",
                "c_venturi", "h_venturi", "t_venturi", "technical_changes", "technical_notes", "notes_equipment", "calc_num_doc_eipsa", "dwg_num_doc_eipsa", "purchase_order",
                "purchase_order_date", "purchase_order_notes", "dim_drawing", "dim_drawing_rev", "dim_drawing_date", "of_drawing", "of_drawing_rev", "of_drawing_date",
                "heat_number_plate", "cert_plate", "heat_number_flange", "cert_flange", "pmi_date", "ph1_date", "ph1_manometer", "ph1_pressure", "ph1_state", "ph1_obs",
                "ph2_date", "ph2_manometer", "ph2_pressure", "ph2_state", "ph2_obs", "lp_date", "lp_hn_liq1", "lp_hn_liq2", "lp_hn_liq3", "lp_state", "lp_obs", "hard_date",
                "hard_hardness", "hard_hardness_hb", "hard_ball", "hard_force", "hard_hn", "hard_state", "hard_obs", "final_verif_dim_date", "final_verif_dim_state",
                "final_verif_dim_obs", "final_verif_of_eq_date", "final_verif_of_eq_state", "final_verif_of_eq_obs", "tag_images", "tag_images2", "fab_state", "inspection",
                "irc_date", "rn_delivery", "rn_date", "pos_fact", "subpos_fact", "amount_fact", "diff_amount", "box_br", "box_pl", "description_fact", "notes_fact",
                "invoice_number", "percent_invoiced", "dim_drawing_path", "of_drawing_path", "order_type_tag", "code_equipment", "code_fab_equipment", "translate_equipment",
                "code_orifice_flange", "code_line_flange", "code_gasket", "code_bolts", "code_plugs", "code_extractor", "code_plate", "code_nipple", "code_handle",
                "code_chring", "code_tube", "code_wedge", "code_fab_orifice_flange", "code_fab_line_flange", "code_fab_gasket", "code_fab_bolts", "code_fab_plugs",
                "code_fab_extractor", "code_fab_plate", "code_fab_nipple", "code_fab_handle", "code_fab_chring", "code_fab_tube", "code_fab_wedge", "quant_orifice_flange",
                "quant_line_flange", "quant_gasket", "quant_bolts", "quant_plugs", "quant_extractor", "quant_plate", "quant_nipple", "quant_handle", "quant_chring",
                "quant_tube", "quant_wedge", "trad_orifice_flange", "trad_line_flange", "trad_gasket", "trad_bolts", "trad_plugs", "trad_extractor", "trad_plate", "trad_nipple",
                "trad_handle", "trad_chring", "trad_tube", "trad_wedge", "code_purch_orifice_flange", "code_purch_line_flange", "code_purch_gasket", "code_purch_bolts", "code_purch_plugs", "code_purch_extractor", "code_purch_plate", "code_purch_nipple", "code_purch_handle",
                "code_purch_chring", "code_purch_tube", "code_purch_wedge"]

                df_flow = pd.DataFrame(results_tags_flow, columns=columns)

                df_flow['of_drawing_date'] = pd.to_datetime(df_flow['of_drawing_date']).dt.strftime('%d/%m/%Y').fillna('')

                count_of_drawings = len(df_flow['of_drawing'].unique().tolist())

                for item_type in df_flow["item_type"].unique():
                    if item_type in ['F+P', 'P', 'RO', 'M.RUN']:
                        df_selected = df_flow.iloc[:, [0, 1, 8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 32, 37, 38, 48, 57, 58, 59, 60, 61, 86, 95, 97, 151]].copy()

                        df_final = df_selected[df_selected['item_type'] == item_type].copy()

                        df_final.rename(columns={
                            0: 'id', 1: 'tag', 8: 'type', 9: 'line_size', 10: 'rating',
                            11: 'facing', 12: 'schedule', 13: 'material', 14: 'flange_type', 19:'element_material', 20: 'plate_type', 21: 'plate_thk',
                            32: 'nace', 37: 'orif_diam', 38: 'dv_diam', 48: 'rtj_thickness', 57: 'pipe_int_diam', 58: 'plate_ext_diam',
                            59: 'plate_c_dim', 60: 'handle_height', 61: 'handle_width', 86: 'notes_equipment', 95: 'of_drawing', 97: 'of_drawing_date', 151: 'of_drawing_path'
                        }, inplace=True)

                        grouped_plates = create_df_orifice_plates(df_final)

                        for _, row in grouped_plates.iterrows():
                            writer = PdfWriter()

                            drawing_path = row["of_drawing_path"]
                            if os.path.exists(drawing_path):
                                with open(drawing_path, 'rb') as f:
                                    reader = PdfReader(f)
                                    base_page = reader.pages[0]

                                    if 'RF' in row['connection'] or 'FF' in row['connection']:
                                        pdf_buffer = dwg_of_op_ro_rf(item_type, numorder, count_of_drawings, row["connection"], row["element_material"], row["of_drawing"], row["of_drawing_date"],
                                                                        row["handle_height"], row["handle_width"], row["plate_c_dim"], row["plate_ext_diam"], row["plate_type"],
                                                                        zip(row["tag"], row["line_size"], row["rating"], row["facing"], row["schedule"], row["element_material"], row["pipe_int_diam"],
                                                                        row["orif_diam"], row["plate_thk"], row["dv_diam"], row["w_diam"], row["nace"], row["count"]))
                                    elif 'RTJ' in row['connection']:
                                        pdf_buffer = dwg_of_op_ro_rtj(item_type, numorder, count_of_drawings, row["connection"], row["element_material"], row["of_drawing"], row["of_drawing_date"],
                                                                        row["plate_c_dim"], row["rtj_thickness"],
                                                                        zip(row["tag"], row["line_size"], row["rating"], row["facing"], row["schedule"], row["element_material"], row["pipe_int_diam"],
                                                                        row["orif_diam"], row["plate_thk"], row["dv_diam"], row["w_diam"], row["nace"], row["count"]))

                                    page_overlay = PdfReader(pdf_buffer).pages[0]
                                    
                                    base_page.merge_page(page2=page_overlay)
                                    writer.add_page(base_page)

                                    writer.write(str(output_path_OF / f"{row["of_drawing"][:5]}.pdf"))

            elif table_name == 'tags_data.tags_temp':
                try:
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(query_tags_temp,(f"%{numorder}%",))
                            results_tags_temp=cur.fetchall()

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")

                columns = ["id_tag_temp", "tag", "tag_state", "num_offer", "num_order", "num_po", "position", "subposition",
                        "item_type", "tw_type", "size", "rating", "facing", "std_tw", "material_tw", "std_length", "ins_length",
                        "root_diam", "tip_diam", "bore_diam", "tip_thk", "radius_dim",
                        "sensor_element", "wire_size", "sheath_stem_material", "sheath_stem_diam", "insulation", "temp_inf", "temp_sup",
                        "nipple_ext_material", "nipple_ext_length", "head_case_material", "head_certification", "elec_conn_case_diam", "tt_cerblock",
                        "material_flange_lj", "gasket_material", "puntal", "tube_t", "nace", "amount", "offer_notes", "commercial_changes", "contractual_date",
                        "stress", "geometry", "conical_length", "straigth_length", "calculation_notes", "plug", "base_tw_diam", "notes_tw", "notes_sensor",
                        "length_cut_tw", "dim_a_sensor", "dim_b_sensor", "dim_l_sensor", "technical_changes", "technical_notes",
                        "calc_num_doc_eipsa", "calc_state", "calc_state_date", "dwg_num_doc_eipsa", "dwg_state", "dwg_state_date", "dwg_notes",
                        "purchase_order", "purchase_order_date", "purchase_order_notes", "dim_drawing", "dim_drawing_rev", "dim_drawing_date",
                        "of_sensor_drawing", "of_sensor_drawing_rev", "of_sensor_drawing_date", "of_drawing", "of_drawing_rev", "of_drawing_date",
                        "heat_number_bar", "cert_bar", "heat_number_flange", "cert_flange",
                        "pmi_date", "ph1_date", "ph1_manometer", "ph1_pressure", "ph1_state", "ph1_obs",
                        "ph2_date", "ph2_manometer", "ph2_pressure", "ph2_state", "ph2_obs",
                        "lp_date", "lp_hn_liq1", "lp_hn_liq2", "lp_hn_liq3", "lp_state", "lp_obs",
                        "hard_date", "hard_hardness", "hard_hardness_hb", "hard_ball", "hard_force", "hard_hn", "hard_state", "hard_obs",
                        "final_verif_dim_date", "final_verif_dim_state", "final_verif_dim_obs", "final_verif_of_eq_date", "final_verif_of_eq_state", "final_verif_of_eq_obs",
                        "final_verif_of_sensor_date", "final_verif_of_sensor_state", "final_verif_of_sensor_obs", "tag_images", "tag_images2",
                        "fab_sensor_state", "fab_tw_state", "fab_state", "inspection", "irc_date", "rn_delivery", "rn_date",
                        "pos_fact", "subpos_fact", "amount_fact", "diff_amount", "box_br", "box_pl", "description_fact", "notes_fact", "invoice_number", "percent_invoiced",
                        "dim_drawing_path", "of_drawing_path", "of_sensor_drawing_path", "order_type_tag", "code_equipment", "code_fab_equipment", "translate_equipment",
                        "code_bar", "code_tube", "code_flange", "code_sensor", "code_head", "code_btb",
                        "code_nippleextcomp", "code_spring", "code_puntal", "code_plug", "code_tw", "code_adit",
                        "code_fab_bar", "code_fab_tube", "code_fab_flange", "code_fab_sensor", "code_fab_head", "code_fab_btb",
                        "code_fab_nippleextcomp", "code_fab_spring", "code_fab_puntal", "code_fab_plug", "code_fab_tw", "code_fab_adit",
                        "quant_bar", "quant_tube", "quant_flange", "quant_sensor", "quant_head", "quant_btb",
                        "quant_nippleextcomp", "quant_spring", "quant_puntal", "quant_plug", "quant_tw", "quant_adit",
                        "trad_bar", "trad_tube", "trad_flange", "trad_sensor", "trad_head", "trad_btb",
                        "trad_nippleextcomp", "trad_spring", "trad_puntal", "trad_plug", "trad_tw", "trad_adit",
                        "code_purch_bar", "code_purch_tube", "code_purch_flange", "code_purch_sensor", "code_purch_head", "code_purch_btb",
                        "code_purch_nippleextcomp", "code_purch_spring", "code_purch_puntal", "code_purch_plug", "code_purch_tw", "code_purch_adit"]

                df_temp = pd.DataFrame(results_tags_temp, columns=columns)

                df_temp['of_drawing_date'] = pd.to_datetime(df_temp['of_drawing_date']).dt.strftime('%d/%m/%Y').fillna('')
                df_temp['of_sensor_drawing_date'] = pd.to_datetime(df_temp['of_sensor_drawing_date']).dt.strftime('%d/%m/%Y').fillna('')

                count_of_drawings = len(df_temp['of_drawing'].unique().tolist()) + len(df_temp['of_sensor_drawing'].unique().tolist())

                for item_type in df_temp["item_type"].unique():
                    if item_type in ['TW', 'TW+TE', 'TW+BIM', 'TW+TE+TIT']:
                        df_selected = df_temp.iloc[:, [0, 1, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21,
                        22, 24, 25, 26, 29, 31, 32, 33, 45, 50, 54, 55, 56, 72, 74, 75, 77, 136, 137]].copy()

                        df_final = df_selected[df_selected['item_type'] == item_type].copy()

                        grouped_sensors = create_df_sensors(df_final)

                        for _, row in grouped_sensors.iterrows():
                            writer = PdfWriter()

                            drawing_path = row["of_sensor_drawing_path"]
                            if os.path.exists(drawing_path):
                                with open(drawing_path, 'rb') as f:
                                    reader = PdfReader(f)
                                    base_page = reader.pages[0]

                                    pdf_buffer = dwg_of_sensor(numorder, count_of_drawings, row["sensor_element"], row["sheath_stem_material"], row["sheath_stem_diam"],
                                                row["insulation"], row["nipple_ext_material"], row["head_case_material"], row["head_certification"], row["elec_conn_case_diam"],
                                                row["of_sensor_drawing"], row["of_sensor_drawing_date"], zip(row["tag"], row["dim_a_sensor"], row["dim_b_sensor"], row["dim_l_sensor"]))

                                    page_overlay = PdfReader(pdf_buffer).pages[0]
                                    
                                    base_page.merge_page(page2=page_overlay)
                                    writer.add_page(base_page)

                                    writer.write(str(output_path_OF / f"{row["of_sensor_drawing"][:5]}.pdf"))

                        grouped_tw = create_df_thermowells(df_final)

                        for _, row in grouped_tw.iterrows():
                            writer = PdfWriter()

                            drawing_path = row["of_drawing_path"]
                            if os.path.exists(drawing_path):
                                with open(drawing_path, 'rb') as f:
                                    reader = PdfReader(f)
                                    base_page = reader.pages[0]

                                    pdf_buffer = dwg_of_thermowell(row["tw_type"], numorder, count_of_drawings, row["connection"], row["material_tw"],
                                                row["base_tw_diam"], row["std_length"], row["ins_length"], row["root_diam"], row["tip_diam"], row["bore_diam"], row["tip_thk"], row["radius_dim"],
                                                row["of_drawing"], row["of_drawing_date"], row["tag"])

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


def create_df_orifice_flanges(dataframe):
    df_flanges = dataframe.copy()

    df_flanges.loc[df_flanges['gasket'].str.contains('SPW', na=False), 'gasket'] = 'SPW'
    df_flanges.loc[df_flanges['gasket'].str.contains('Flat', na=False), 'gasket'] = 'Flat'
    df_flanges.loc[df_flanges['gasket'].str.contains('RTJ', na=False), 'gasket'] = 'RTJ'

    df_flanges['drawing_code'] = df_flanges.apply(
    lambda row: 'CBWNO' + str(row['facing']) + ('TH' if str(row['flange_type']) == 'TH' else ('SW' if str(row['flange_type']) == 'SW' else '')) +
                ('-0' if len(str(row['size'])) == 2 else '-') + str(row['size']).split('"')[0] + ('.5' if ' 1/2' in str(row['size']) else '.0') +
                ('-0' + str(row['rating']) if str(row['rating']) in ['150', '300', '600', '900'] else '-' + str(row['rating'])) + ('-SA' if int(row['size'].split('"')[0])> 24 else ''),
    axis=1)

    df_flanges['connection'] = df_flanges.apply(
    lambda row: str(row['size']) + " " + str(row['rating']) + "#" + str(row['facing']),
    axis=1)

    df_flanges['drawing_path'] = df_flanges.apply(
    lambda row: rf"""\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\C-Caudal\B-Bridas\WN-WeldNeck\O-Orificio\{'RF-RaisedFace' if str(row['facing']) == 'RF' else ('FF-FlatFace' if str(row['facing']) == 'FF' else 'RTJ-RingTypeJoint')}\{'' if str(row['flange_type']) in ['WN','16.47-A'] else ('TH-Roscadas' if str(row['flange_type']) == 'TH' else 'SW-SocketWeld')}\{str(row['drawing_code'])}.pdf""",
    axis=1)

    df_grouped = df_flanges.groupby(['drawing_path', 'connection', 'type', 'schedule', 'material', 'tapping_size', 'tapping_num', 'tapping_orientation','gasket', 'flange_type', 'pipe_int_diam']).size().reset_index(name="count")
    grouped_flanges = df_grouped.groupby(['drawing_path', 'connection','type','schedule','material','tapping_size', 'tapping_num', 'tapping_orientation', 'gasket', 'flange_type']).agg({"pipe_int_diam": list, "count": list}).reset_index()

    return grouped_flanges

def create_df_orifice_plates(dataframe):
    df_plates = dataframe.copy()
    df_plates = df_plates.fillna('')

    df_plates['connection'] = df_plates.apply(
    lambda row: row['line_size'] + " " + row['rating'] + "# " + row['facing'],
    axis=1)

    df_plates['w_diam'] = df_plates.apply(
    lambda row: str(0.5 + float(row['dv_diam'].split('=')[1].replace(',','.')) / 2) if str(row['dv_diam']) not in ('None', '', 'N/A') else '',
    axis=1)

    df_plates = df_plates.sort_values(by="tag")

    grouped_plates = df_plates.groupby(['plate_type', 'of_drawing_path', 'connection', 'of_drawing', 'of_drawing_date', 'plate_ext_diam', 'plate_c_dim', 'handle_height', 'handle_width', 'rtj_thickness', 'notes_equipment']).agg(
        {"tag": list, "line_size": list, "rating": list, "facing": list, "schedule": list, "element_material": list, "pipe_int_diam": list,
        "orif_diam": list, "plate_thk": list, "dv_diam": list, "w_diam": list, "nace": list}
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
                                'base_tw_diam', 'geometry', 'std_length', 'ins_length', 'root_diam', 'tip_diam', 'bore_diam', 'tip_thk', 'radius_dim']).agg({"tag": list}).reset_index()

    return grouped_tw

def create_df_sensors(dataframe):
    df_sensors = dataframe.copy()
    df_sensors = df_sensors.fillna('')

    df_sensors = df_sensors.sort_values(by="tag")

    grouped_sensors = df_sensors.groupby(['of_sensor_drawing_path', 'of_sensor_drawing', 'of_sensor_drawing_date', 'sensor_element', 'sheath_stem_material', 'sheath_stem_diam',
                                'insulation', 'root_diam', 'nipple_ext_material', 'head_case_material', 'head_certification', 'elec_conn_case_diam']).agg({"tag": list, "dim_a_sensor": list, "dim_b_sensor": list, "dim_l_sensor": list}).reset_index()

    return grouped_sensors

