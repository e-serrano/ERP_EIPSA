from utils.Database_Manager import Database_Connection
from config.config_functions import config_database
from utils.Show_Message import MessageHelper
import psycopg2
import os
from datetime import *
import pandas as pd
from config.config_keys import ORDERS_PATH
from psycopg2 import sql
from psycopg2.extras import execute_batch
from pypdf import PdfReader, PdfWriter
from windows.overlay_pdf import (dwg_dim_flange_plate, dwg_dim_plate, dwg_dim_ro, dwg_dim_ms_ro, dwg_dim_mrun, dwg_dim_venturi, dwg_dim_nozzle,
                                dwg_dim_thermowell,
                                dwg_dim_glass_level,
                                dwg_dim_flange_plate_riyas, dwg_dim_mrun_riyas)


def generate_dim_drawings(numorder, client, final_client, project, num_po):
    query_tags_flow = ("SELECT * FROM tags_data.tags_flow WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND position <> 'ZZZ'")
    query_tags_temp = ("SELECT * FROM tags_data.tags_temp WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND position <> 'ZZZ'")
    query_tags_level = ("SELECT * FROM tags_data.tags_level_new WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND position <> 'ZZZ'")

    query_select_drawings = ("""
            SELECT * FROM (
                SELECT id_tag_flow, dim_drawing, 'tags_data.tags_flow' as table, 'id_tag_flow' as id_column, tag
                FROM tags_data.tags_flow
                WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND position <> 'ZZZ'
                ORDER BY tag) t_flow

            UNION ALL

            SELECT * FROM (
                SELECT id_tag_temp, dim_drawing, 'tags_data.tags_temp' as table, 'id_tag_temp' as id_column, tag
            FROM tags_data.tags_temp
            WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND position <> 'ZZZ'
            ORDER BY tag) t_temp

            UNION ALL

            SELECT * FROM (
                SELECT id_tag_level, dim_drawing, 'tags_data.tags_level_new' as table, 'id_tag_level' as id_column, tag
            FROM tags_data.tags_level_new
            WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND position <> 'ZZZ'
            ORDER BY tag) t_level

            UNION ALL

            SELECT * FROM (
                SELECT id_tag_others, dim_drawing, 'tags_data.tags_others' as table, 'id_tag_others' as id_column, tag
            FROM tags_data.tags_others
            WHERE num_order ILIKE %s and tag_state = 'PURCHASED' AND position <> 'ZZZ'
            ORDER BY tag) t_others
            """)

    query_update_drawings = sql.SQL("UPDATE {table} SET dim_drawing = %s WHERE {id_column} = %s")

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
                cur.execute(query_select_drawings,(f"%{numorder}%", f"%{numorder}%", f"%{numorder}%", f"%{numorder}%",))
                results_tags_drawings=cur.fetchall()
                df_final = pd.DataFrame(results_tags_drawings, columns=["id", "dim_drawing", "table", "id_column", "tag"])
    except (Exception, psycopg2.DatabaseError) as error:
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

        df_final.loc[mask_new, "dim_drawing"] = [numorder[2:].replace("/", "-") + "-" + f"{i:0{num_width}d}" for i in range(start, start + qty_new)]

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

# Drawing generation
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

                df_flow['dim_drawing_date'] = pd.to_datetime(df_flow['dim_drawing_date']).dt.strftime('%d/%m/%Y').fillna('')

                for _, row in df_flow.iterrows():
                    writer = PdfWriter()

                    drawing_path = row["dim_drawing_path"]
                    if os.path.exists(drawing_path):
                        with open(drawing_path, 'rb') as f:
                            # reader = PdfReader(f)
                            reader = PdfReader(drawing_path)
                            base_page = reader.pages[0]

                            if row["item_type"] == "F+P":
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
                                                            row["dim_drawing"][-2:], row["dim_drawing_date"], total)
                                else:
                                    pdf_buffer = dwg_dim_flange_plate(numorder, row["tag"],
                                                                row["line_size"], row["schedule"], row["rating"], row["facing"],
                                                                row["pipe_int_diam"], row["orif_diam"], row["plate_thk"], row["dv_diam"], row["nace"], row['tapping_size'],
                                                                row["o_flange"], row["a_flange"], row["c_flange"], row["y_flange"], row["x_flange"], row["r_flange"], row["d_flange"], row["t_flange"], row["bolts_quantity"], row["bore_bolts_diam"],
                                                                row["handle_height"], row["handle_width"], row["plate_c_dim"], row["plate_ext_diam"],
                                                                row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"],
                                                                client, final_client, project, row["num_po"],
                                                                row["flange_material"], row["bolts_material"], row["nuts_material"], row["element_material"], row["gasket_material"], row["plug_quantity"], row["plug_material"], row["jack_screw_material"],
                                                                row["notes_flange"], row["notes_stud"], row["notes_nut"], row["notes_plate"], row["notes_gasket"], row["notes_plugs"], row["notes_jack_screw"],
                                                                row["dim_drawing"][-2:], row["dim_drawing_date"], total)

                            elif row["item_type"] == "P":
                                pdf_buffer = dwg_dim_plate(numorder, row["tag"],
                                                            row["line_size"], row["schedule"], row["rating"], row["facing"],
                                                            row["pipe_int_diam"], row["orif_diam"], row["plate_thk"], row["dv_diam"], row["nace"], row["element_material"],
                                                            row["handle_height"], row["handle_width"], row["plate_c_dim"], row["plate_ext_diam"],
                                                            row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"],
                                                            client, final_client, project, row["num_po"],
                                                            row["dim_drawing"][-2:], row["dim_drawing_date"], total)

                            elif row["item_type"] == "RO":
                                pdf_buffer = dwg_dim_ro(numorder, row["tag"],
                                                            row["line_size"], row["schedule"], row["rating"], row["facing"], row["element_material"],
                                                            row["pipe_int_diam"], row["orif_diam"], row["plate_thk"], row["nace"], row["plate_type"],
                                                            row["handle_height"], row["handle_width"], row["handle_thickness"], row["plate_ext_diam"],
                                                            row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"],
                                                            client, final_client, project, row["num_po"],
                                                            row["dim_drawing"][-2:], row["dim_drawing_date"], total)

                            elif row["item_type"] == "MULTISTAGE RO":
                                pdf_buffer = dwg_dim_ms_ro(numorder, row["tag"],
                                                            row["line_size"], row["schedule"], row["rating"], row["facing"],
                                                            row["flange_material"], row["tube_material"], row["element_material"],
                                                            row["pipe_int_diam"], row["nace"],
                                                            row["stages_number"], row["aprox_length"],
                                                            row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"],
                                                            client, final_client, project, row["num_po"],
                                                            row["dim_drawing"][-2:], row["dim_drawing_date"], total)

                            elif row["item_type"] == "M.RUN":
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
                                                                row["dim_drawing"][-2:], row["dim_drawing_date"], total)
                                else:
                                    pdf_buffer = dwg_dim_mrun(numorder, row["tag"],
                                                                row["line_size"], row["schedule"], row["rating"], row["facing"],
                                                                row["pipe_int_diam"], row["orif_diam"], row["nace"], row['tapping_size'], row["flange_type"],
                                                                row["aprox_weight"], row["aprox_length"], row["tube_material"],
                                                                row["handle_height"], row["handle_width"], row["plate_c_dim"], row["plate_ext_diam"],
                                                                row["rtj_thickness"], row["rtj_r_type"], row["rtj_p_diam"], row["rtj_e_dim"], row["rtj_f_dim"],
                                                                client, final_client, project, row["num_po"],
                                                                row["flange_material"], row["bolts_material"], row["nuts_material"], row["element_material"], row["gasket_material"], row["plug_quantity"], row["plug_material"], row["jack_screw_material"],
                                                                row["notes_flange"], row["notes_stud"], row["notes_nut"], row["notes_plate"], row["notes_gasket"], row["notes_plugs"], row["notes_jack_screw"],
                                                                row["dim_drawing"][-2:], row["dim_drawing_date"], total)

                            elif row["item_type"] in ["VFM", "VWM", "VFW", "VWW", "VFC"]:
                                pdf_buffer = dwg_dim_venturi(numorder, row["item_type"], row["tag"],
                                                                row["line_size"], row["schedule"], row["rating"], row["facing"],
                                                                row["pipe_int_diam"], row["orif_diam"], row["nace"], row['tapping_size'], row["tapping_number"],
                                                                row["aprox_weight"], row["aprox_length"], row["tube_material"], row["cones_material"],
                                                                row["a_venturi"], row["d_venturi"], row["e_venturi"], row["f_venturi"], row["g_venturi"], row["c_venturi"], row["h_venturi"], row["t_venturi"],
                                                                client, final_client, project, row["num_po"],
                                                                row["flange_material"], row["element_material"], row["plug_quantity"], row["plug_material"],
                                                                row["notes_flange"], row["notes_plate"], row["notes_plugs"],
                                                                row["dim_drawing"][-2:], row["dim_drawing_date"], total)

                            elif 'NOZZLE' in row["item_type"]:
                                pdf_buffer = dwg_dim_nozzle(numorder, row["tag"],
                                                            row["line_size"], row["schedule"], row["rating"], row["facing"],
                                                            row["pipe_int_diam"], row["orif_diam"], row["nace"], row['tapping_size'], row["tapping_number"],
                                                            row["a_venturi"], row["d_venturi"], row["f_venturi"], row["e_venturi"], row["plateaprox_length_ext_diam"],
                                                            row["aprox_weight"], row["tube_material"],
                                                            client, final_client, project, row["num_po"],
                                                            row["flange_material"], row["element_material"], row["plug_quantity"], row["plug_material"],
                                                            row["notes_flange"], row["notes_plate"], row["notes_plugs"],
                                                            row["dim_drawing"][-2:], row["dim_drawing_date"], total)

                            page_overlay = PdfReader(pdf_buffer).pages[0]

                            base_page.merge_page(page2=page_overlay)
                            writer.add_page(base_page)

                            writer.write(str(output_path_Dim / f'{row["dim_drawing"]}.pdf'))

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
                        "of_sensor_drawing", "of_sensor_drawing_rev", "of_sensor_drawing_date", "of_drawing", "of_drawing_rev", "of_date",
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

                df_temp['dim_drawing_date'] = pd.to_datetime(df_temp['dim_drawing_date']).dt.strftime('%d/%m/%Y').fillna('')

                for _, row in df_temp.iterrows():
                    writer = PdfWriter()

                    drawing_path = row["dim_drawing_path"]
                    if drawing_path is not None and os.path.exists(drawing_path):
                        with open(drawing_path, 'rb') as f:
                            # reader = PdfReader(f)
                            reader = PdfReader(drawing_path)
                            base_page = reader.pages[0]

                            if row["item_type"] == "TW+TE":
                                pdf_buffer = dwg_dim_thermowell(numorder, row["tag"], row["item_type"],
                                            row["ins_length"], row["std_length"], row["sensor_element"], row["wire_size"], row["sheath_stem_diam"], row["sheath_stem_material"], row["nace"],
                                            row["root_diam"], row["tip_diam"], row["bore_diam"], row["tip_thk"], row["radius_dim"],
                                            client, final_client, project, row["num_po"],
                                            row["insulation"], row["elec_conn_case_diam"], row["head_case_material"], row["head_certification"], row["nipple_ext_material"],
                                            row["tw_type"], row["size"], row["rating"], row["facing"], row["std_tw"], row["material_tw"],
                                            row["dim_drawing"][-2:], row["dim_drawing_date"], total)

                            page_overlay = PdfReader(pdf_buffer).pages[0]

                            base_page.merge_page(page2=page_overlay)
                            writer.add_page(base_page)

                            writer.write(str(output_path_Dim / f'{row["dim_drawing"]}.pdf'))

            elif table_name == 'tags_data.tags_level_new':
                try:
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(query_tags_level,(f"%{numorder}%",))
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

                    drawing_path = row["dim_drawing_path"]
                    if drawing_path is not None and os.path.exists(drawing_path):
                        with open(drawing_path, 'rb') as f:
                            # reader = PdfReader(f)
                            reader = PdfReader(drawing_path)
                            base_page = reader.pages[0]

                            if row["item_type"] in ["Transparent", "Reflex"]:
                                pdf_buffer = dwg_dim_glass_level(numorder, row["tag"], row["item_type"],
                                            row["model_num"], row["visibility"], row["cc_length"], row["body_length"],
                                            row["proc_conn_type"], row["proc_conn_size"], row["proc_conn_rating"], row["proc_conn_facing"], row["proc_conn_material"], row["nace"],
                                            row["body_material"], row["case_cover_material"], row["gasket_mica"], row["nuts_material"], row["stud_material"],
                                            row["nipple_hex"], row["nipple_hex_material"], row["valve_type"], row["valve_conn"], row["valve_material"],
                                            row["dv_conn"], row["dv_size"], row["dv_rating"], row["dv_facing"], row["dv_material"],
                                            row["nipple_tub"], row["nipple_tub_material"], row["illuminator"], row["illuminator_connection"],
                                            client, final_client, project, row["num_po"],
                                            row["dim_drawing"][-2:], row["dim_drawing_date"], total)

                            page_overlay = PdfReader(pdf_buffer).pages[0]

                            base_page.merge_page(page2=page_overlay)
                            writer.add_page(base_page)

                            writer.write(str(output_path_Dim / f'{row["dim_drawing"]}.pdf'))

        MessageHelper.show_message("Planos Generados", "info")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        MessageHelper.show_message("Ha ocurrido un error generando planos:\n"
                    "Los planos no se han podido generar", "critical")