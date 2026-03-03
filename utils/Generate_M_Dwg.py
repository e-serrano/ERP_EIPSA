from utils.Database_Manager import Database_Connection
from config.config_functions import config_database
from utils.Show_Message import MessageHelper
import psycopg2
import os
from datetime import *
import pandas as pd
import numpy as np
from config.config_keys import ORDERS_PATH
from pypdf import PdfReader, PdfWriter
from windows.overlay_pdf import (flange_dwg_orifice, flange_dwg_line, tube_dwg_meterrun, welding_dwg_meterrun,
                                drawing_number, flange_dwg_orifice)

from windows.overlay_pdf import (flange_dwg_flangedTW, bar_dwg_flangedTW, bar_dwg_notflangedTW,
                        flange_dwg_orifice, flange_dwg_line,
                        tube_dwg_meterrun, welding_dwg_meterrun,
                        loose_valves_dwg_dim,
                        dwg_dim_32218_32219, dwg_m_welding_32218_32219, dwg_m_32218_32219,
                        dwg_m_landscape, general_dwg_m, drawing_number, drawing_number_landscape)



def generate_m_drawings(username, numorder):
    output_path_M = None
    order_year = str(datetime.now().year)[:2] + numorder[numorder.rfind("/") - 2:numorder.rfind("/")]

    path = ORDERS_PATH / f"Año {order_year}" / (f"{order_year} Pedidos Almacen" if numorder[:2] == 'PA' else f"{order_year} Pedidos")
    for folder in sorted(os.listdir(path)):
        if 'S00' in numorder:
            if numorder[:8].replace("/", "-") in folder:
                output_path_M = path / folder / "3-Fabricacion" / "Planos M"
                break
        else:
            if numorder.replace("/", "-") in folder:
                output_path_M = path / folder / "3-Fabricacion" / "Planos M"
                break

    if not os.path.exists(output_path_M):
        os.makedirs(output_path_M)

    query_flow = ('''
        SELECT tags_data.tags_flow."num_order"
        FROM tags_data.tags_flow
        WHERE UPPER (tags_data.tags_flow."num_order") LIKE UPPER('%%'||%s||'%%')
        ''')

    query_temp = ('''
        SELECT tags_data.tags_temp."num_order"
        FROM tags_data.tags_temp
        WHERE UPPER (tags_data.tags_temp."num_order") LIKE UPPER('%%'||%s||'%%')
        ''')

    query_level = ('''
        SELECT tags_data.tags_level."num_order"
        FROM tags_data.tags_level
        WHERE UPPER (tags_data.tags_level."num_order") LIKE UPPER('%%'||%s||'%%')
        ''')

    query_others = ('''
        SELECT tags_data.tags_others."num_order"
        FROM tags_data.tags_others
        WHERE UPPER (tags_data.tags_others."num_order") LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query_flow,(numorder,))
                results_flow=cur.fetchall()
                cur.execute(query_temp,(numorder,))
                results_temp=cur.fetchall()
                cur.execute(query_level,(numorder,))
                results_level=cur.fetchall()
                cur.execute(query_others,(numorder,))
                results_others=cur.fetchall()

        if len(results_flow) != 0 and len(results_temp) != 0:
            variable = 'Caudal + Temperatura'
            table_toquery = "tags_data.tags_flow"
        elif len(results_flow) != 0:
            variable = 'Caudal'
            table_toquery = "tags_data.tags_flow"
        elif len(results_temp) != 0:
            variable = 'Temperatura'
            table_toquery = "tags_data.tags_temp"
        elif len(results_level) != 0:
            variable = 'Nivel'
            table_toquery = "tags_data.tags_level"
        elif len(results_others) != 0:
            variable = 'Otros'
            table_toquery = "tags_data.tags_others"
        else:
            variable = ''
            table_toquery = ""

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    commands_select_m_drawing = ("""
        SELECT drawing_number
        FROM verification."m_drawing_verification"
        WHERE "num_order" = %s
        ORDER BY drawing_number DESC
        """)

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:  
                cur.execute(commands_select_m_drawing,(numorder,))
                results_drawings_m=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    dict_drawings = {}
    counter_drawings = 0
    # if len(results_drawings_m) == 0:
    #     counter_drawings = 0
    # else:
    #     counter_drawings = int(results_drawings_m[0][0][-2:])

    try:
        if table_toquery == "tags_data.tags_temp":
        # Obtain the data from the database for temperature tags and create the correspondig dataframe with the necessary columns
            query = ('''
                SELECT *
                FROM tags_data.tags_temp
                WHERE UPPER (num_order) LIKE UPPER('%%'||%s||'%%') and tag_state = 'PURCHASED'
                ''')

            try:
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(query,(numorder,))
                        results_tags=cur.fetchall()

                df_general = pd.DataFrame(results_tags)

            except (Exception, psycopg2.DatabaseError) as error:
                MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                            + str(error), "critical")

            df_selected = df_general.iloc[:, [0, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 50, 51]].copy()
            df_selected.rename(columns={
                0: 'id', 9: 'type', 10: 'size', 11: 'rating',
                12: 'facing', 13: 'std_tw', 14: 'material', 15: 'std_length', 17: 'root_diam', 18: 'tip_diam',
                19: 'bore_diam', 20: 'tip_thk', 50: 'base_tw_diam', 51: 'notes_tw'
            }, inplace=True)

        # Loop through different types of equipment and create drawings accordingly
            for item in df_selected['type'].unique().tolist():
                if item == 'Flanged TW':
                    df_selected = df_selected[df_selected['type'] == 'Flanged TW'].copy()

                    grouped_flanges = create_df_flanges_flanged_tw(df_selected)
                    total_count = grouped_flanges['count'].explode().sum() 

                    for _, row in grouped_flanges.iterrows():
                        counter_drawings += 1

                        writer = PdfWriter()

                        drawing_path = row["drawing_path"]
                        if os.path.exists(drawing_path):
                            reader = PdfReader(drawing_path)
                            page_overlay = PdfReader(flange_dwg_flangedTW(numorder, row["material"], row["count"][0])).pages[0]

                            if row["base_tw_diam"] == 32:
                                reader.pages[0].merge_page(page2=page_overlay)
                                writer.add_page(reader.pages[0])
                            elif row["base_tw_diam"] == 35:
                                reader.pages[1].merge_page(page2=page_overlay)
                                writer.add_page(reader.pages[1])
                            elif row["base_tw_diam"] == 30:
                                reader.pages[2].merge_page(page2=page_overlay)
                                writer.add_page(reader.pages[2])
                            elif row["base_tw_diam"] == 38:
                                reader.pages[3].merge_page(page2=page_overlay)
                                writer.add_page(reader.pages[3])

                            writer.write(str(output_path_M / f"M-{counter_drawings:02d}.pdf"))
                            dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", str(sum(row["count"])) + " BPC " + str(row["connection"]) + " " +str(row["material"]), str(sum(row["count"]))]
                        else:
                            dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", "FALTA PLANO // " + str(sum(row["count"])) + " BPC " + str(row["connection"]) + " " +str(row["material"]), str(sum(row["count"]))]

                    grouped_bars = create_df_bars_flanged_tw(df_selected)
                    total_count = grouped_bars['count'].explode().sum() 

                    for _, row in grouped_bars.iterrows():
                        counter_drawings += 1

                        writer = PdfWriter()

                        drawing_path = row["drawing_path"]
                        if os.path.exists(drawing_path):
                            reader = PdfReader(drawing_path)
                            page_overlay = PdfReader(bar_dwg_flangedTW(numorder, row["material"], row["base_tw_diam"], zip(row["bore_diam"], row["std_length"], row["p_length"], row["count"]))).pages[0]

                            reader.pages[0].merge_page(page2=page_overlay)
                            writer.add_page(reader.pages[0])

                            writer.write(str(output_path_M / f"M-{counter_drawings:02d}.pdf"))
                            dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", str(sum(row["count"])) + " Vainas C+R Ø" + str(row["base_tw_diam"]) + " " + str(row["material"]), str(sum(row["count"]))]
                        else:
                            dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", "FALTA PLANO // " + str(sum(row["count"])) + " Vainas C+R Ø" + str(row["base_tw_diam"]) + " " + str(row["material"]), str(sum(row["count"]))]

                elif item in ['Buttweld TW', 'Socket TW']:
                    df_selected = df_selected[df_selected['type'].isin(['Buttweld TW', 'Socket TW'])].copy()

                    grouped_bars = create_df_not_flanged_tw(df_selected, item)
                    total_count = grouped_bars['count'].explode().sum() 

                    for _, row in grouped_bars.iterrows():
                        counter_drawings += 1

                        writer = PdfWriter()

                        drawing_path = row["drawing_path"]
                        if os.path.exists(drawing_path):
                            reader = PdfReader(drawing_path)
                            page_overlay = PdfReader(bar_dwg_notflangedTW(numorder, row["material"], row['base_tw_diam'], zip(row["bore_diam"], row["std_length"], row["p_length"], row["count"]))).pages[0]

                            reader.pages[0].merge_page(page2=page_overlay)
                            writer.add_page(reader.pages[0])

                            writer.write(str(output_path_M / f"M-{counter_drawings:02d}.pdf"))
                            dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", str(total_count) + " Vainas C+R Ø" + str(row["base_tw_diam"]) + " " + str(row["material"]), total_count]
                        else:
                            dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", "FALTA PLANO // " + str(total_count) + " Vainas C+R Ø" + str(row["base_tw_diam"]) + " " + str(row["material"]), total_count]

        # Loop to add the drawing number and insert into the database
            for key, value in dict_drawings.items():
                if os.path.exists(key):
                    writer = PdfWriter()
                    reader = PdfReader(key)
                    page_overlay = PdfReader(drawing_number(numorder, value, counter_drawings)).pages[0]
                    reader.pages[0].merge_page(page2=page_overlay)
                    writer.add_page(reader.pages[0])

                    writer.write(key)

                query_insert_drawing = ("""
                    INSERT INTO verification."m_drawing_verification" (num_order, drawing_number, drawing_description, printed_date, printed_state)
                    VALUES (%s, %s, %s, %s, %s)
                    """)

                try:
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(query_insert_drawing,(numorder,value[0][:4] + f"/{counter_drawings:02d}", value[1], str(datetime.today().strftime('%d/%m/%Y')), 'Realizado por Julio' if username == 'j.zofio' else 'Realizado por Jose Alberto'))
                        conn.commit()

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")

        elif table_toquery == "tags_data.tags_flow":
        # Obtain the data from the database for flow tags and create the correspondig dataframe with the necessary columns
            query = ('''
                SELECT *
                FROM tags_data.tags_flow
                WHERE UPPER (num_order) LIKE UPPER('%%'||%s||'%%') and tag_state = 'PURCHASED'
                ''')

            try:
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute(query,(numorder,))
                        results_tags=cur.fetchall()

                df_general = pd.DataFrame(results_tags)

            except (Exception, psycopg2.DatabaseError) as error:
                MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                            + str(error), "critical")

            df_selected = df_general.iloc[:, [0, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 23, 57, 86]].copy()
            df_selected.rename(columns={
                0: 'id', 8: 'type', 9: 'size', 10: 'rating',
                11: 'facing', 12: 'schedule', 13: 'material', 14:'flange_type',
                15: 'tube_material', 16: 'tapping_size', 17: 'tapping_number', 18: 'tapping_orientation', 
                23: 'gasket', 57: 'pipe_int_diam', 86: 'notes_equipment'
            }, inplace=True)

            df_selected['tapping'] = df_selected.apply(
            lambda row: str(row['tapping_size']) + " (" + str(row['tapping_number']) + ")",
            axis=1)

        # Loop through different types of equipment and create drawings accordingly
            for item in df_selected['type'].unique().tolist():

                if item in ['F+P', 'F']:
                    df_selected_fp = df_selected[df_selected['type'] == item].copy()

                    grouped_flanges = create_df_orifice_flanges(df_selected_fp)
                    total_count = grouped_flanges['count'].explode().sum() 

                    for _, row in grouped_flanges.iterrows():
                        counter_drawings += 1

                        writer = PdfWriter()

                        drawing_path = row["drawing_path"]
                        if os.path.exists(drawing_path):
                            with open(drawing_path, 'rb') as f:
                                reader = PdfReader(f)
                                base_page = reader.pages[0]

                                pdf_buffer = flange_dwg_orifice(numorder, row["type"], row["material"], row["schedule"], row["tapping_size"], row["tapping_num"], row["tapping_orientation"], row["gasket"], row["flange_type"], zip(row["pipe_int_diam"], row["count"]))

                                page_overlay = PdfReader(pdf_buffer).pages[0]
                                
                                base_page.merge_page(page2=page_overlay)
                                writer.add_page(base_page)

                                writer.write(str(output_path_M / f"M-{counter_drawings:02d}.pdf"))
                                dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", str(2*sum(row['count'])) + "-BO" + str(row["flange_type"]) + " " + str(row["connection"]) + " SCH " + str(row["schedule"])  + " " + str(row["material"]) + " " + str(row["tapping"][-2:-1]) + " TOMAS + " + "2 EXTRACTORES", 2*sum(row['count'])]
                        else:
                            dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", "FALTA PLANO // " + str(2*sum(row['count'])) + "-BO" + str(row["flange_type"]) + " " + str(row["connection"]) + " SCH " + str(row["schedule"])  + " " + str(row["material"]) + " " + str(row["tapping"][-2:-1]) + " TOMAS + " + "2 EXTRACTORES", 2*sum(row['count'])]

                elif item == 'M.RUN':
                    df_selected_mrun = df_selected[df_selected['type'] == 'M.RUN'].copy()

                    df_selected_transformed = transform_df_mrun(df_selected_mrun)

                    grouped_orifice_flanges = create_df_orifice_flanges_mrun(df_selected_transformed)
                    total_count = grouped_orifice_flanges['count'].explode().sum()

                    for _, row in grouped_orifice_flanges.iterrows():
                        counter_drawings += 1

                        writer = PdfWriter()

                        drawing_path = row["drawing_path"]
                        if os.path.exists(drawing_path):
                            with open(drawing_path, 'rb') as f:
                                reader = PdfReader(f)
                                base_page = reader.pages[0]

                                pdf_buffer = flange_dwg_orifice(numorder, row["type"], row["material"], row["schedule"], row["tapping"], row["gasket"], row["type_orifice_flange"], zip(row["final_pipe_int_diam"], row["orifice_flange_height"], row["count"]))

                                page_overlay = PdfReader(pdf_buffer).pages[0]
                                
                                base_page.merge_page(page2=page_overlay)
                                writer.add_page(base_page)

                                writer.write(str(output_path_M / f"M-{counter_drawings:02d}.pdf"))
                                dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", str(2*sum(row['count'])) + "-BO" + str(row["type_orifice_flange"]) + " " + str(row["connection"]) + " SCH " + str(row["schedule"])  + " " + str(row["material"]) + " " + str(row["tapping"][-2:-1]) + " TOMAS + " + "2 EXTRACTORES", 2*sum(row['count'])]
                        else:
                            dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", "FALTA PLANO // " + str(2*sum(row['count'])) + "-BO" + str(row["type_orifice_flange"]) + " " + str(row["connection"]) + " SCH " + str(row["schedule"])  + " " + str(row["material"]) + " " + str(row["tapping"][-2:-1]) + " TOMAS + " + "2 EXTRACTORES", 2*sum(row['count'])]

                    grouped_line_flanges = create_df_line_flanges_mrun(df_selected_transformed)
                    total_count = grouped_line_flanges['count'].explode().sum()

                    for _, row in grouped_line_flanges.iterrows():
                        counter_drawings += 1

                        writer = PdfWriter()

                        drawing_path = row["drawing_path"]
                        if os.path.exists(drawing_path):
                            with open(drawing_path, 'rb') as f:
                                reader = PdfReader(f)
                                base_page = reader.pages[0]

                                pdf_buffer = flange_dwg_line(numorder, row["material"], row["schedule"], row["type_line_flange"], row["reduction"], row["connection"], zip(row["final_pipe_int_diam"], row["line_flange_height"], row["count"]))

                                page_overlay = PdfReader(pdf_buffer).pages[0]
                                
                                base_page.merge_page(page2=page_overlay)
                                writer.add_page(base_page)

                                writer.write(str(output_path_M / f"M-{counter_drawings:02d}.pdf"))
                                dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", str(2*sum(row['count'])) + "-BL" + str(row["type_line_flange"]) + " " + str(row["connection"]) + " SCH " + str(row["schedule"])  + " " + str(row["material"]), 2*sum(row['count'])]
                        else:
                            dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", "FALTA PLANO // " + str(2*sum(row['count'])) + "-BL" + str(row["type_line_flange"]) + " " + str(row["connection"]) + " SCH " + str(row["schedule"])  + " " + str(row["material"]), 2*sum(row['count'])]

                    grouped_tubes = create_df_tubes_mrun(df_selected_transformed)
                    total_count = grouped_tubes['count'].explode().sum()

                    for _, row in grouped_tubes.iterrows():
                        counter_drawings += 1

                        writer = PdfWriter()

                        drawing_path = row["drawing_path"]
                        if os.path.exists(drawing_path):
                            with open(drawing_path, 'rb') as f:
                                reader = PdfReader(f)
                                base_page = reader.pages[0]

                                pdf_buffer = tube_dwg_meterrun(numorder, row["size_orifice_flange"], row["sch_orifice_flange"], row["tube_material"], row["calibrated"], zip(row["final_pipe_int_diam"], row["pipe_ext_diam"], row["length_long"], row["length_short"], row["welding_type_orifice"], row["welding_type_line"], row["count"]))

                                page_overlay = PdfReader(pdf_buffer).pages[0]
                                
                                base_page.merge_page(page2=page_overlay)
                                writer.add_page(base_page)

                                writer.write(str(output_path_M / f"M-{counter_drawings:02d}.pdf"))
                                dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", "CORTE TUBOS TRAMO " + str(row["size_orifice_flange"]) + " SCH " + str(row["sch_orifice_flange"])  + " " + str(row["tube_material"]), sum(row['count'])]
                        else:
                            dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", "FALTA PLANO // CORTE TUBOS TRAMO " + str(row["size_orifice_flange"]) + " SCH " + str(row["sch_orifice_flange"])  + " " + str(row["tube_material"]), sum(row['count'])]

                    grouped_welding = create_df_welding_mrun(df_selected_transformed)
                    total_count = grouped_welding['count'].explode().sum()

                    for _, row in grouped_welding.iterrows():
                        counter_drawings += 1

                        writer = PdfWriter()

                        drawing_path = row["drawing_path"]
                        if os.path.exists(drawing_path):
                            with open(drawing_path, 'rb') as f:
                                reader = PdfReader(f)
                                base_page = reader.pages[0]

                                pdf_buffer = welding_dwg_meterrun(numorder, row["material"], row["flange_type"], zip(row["count"]))

                                page_overlay = PdfReader(pdf_buffer).pages[0]

                                if row["flange_type"] == 'WN':
                                    reader.pages[0].merge_page(page2=page_overlay)
                                    writer.add_page(reader.pages[0])
                                elif row["flange_type"] == 'SW/WN':
                                    reader.pages[1].merge_page(page2=page_overlay)
                                    writer.add_page(reader.pages[1])
                                elif row["flange_type"] == 'SO/WN':
                                    reader.pages[2].merge_page(page2=page_overlay)
                                    writer.add_page(reader.pages[2])
                                elif row["flange_type"] == 'SO/WN':
                                    reader.pages[3].merge_page(page2=page_overlay)
                                    writer.add_page(reader.pages[3])
                                elif row["flange_type"] == 'SW/SO':
                                    reader.pages[4].merge_page(page2=page_overlay)
                                    writer.add_page(reader.pages[4])
                                elif row["flange_type"] == 'SO':
                                    reader.pages[5].merge_page(page2=page_overlay)
                                    writer.add_page(reader.pages[5])

                                writer.write(str(output_path_M / f"M-{counter_drawings:02d}.pdf"))
                                dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", "DETALLES SOLDADURA TIPO " + str(row["flange_type"]) + " " + str(row["material"]), sum(row['count'])]
                        else:
                            dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", "FALTA PLANO // DETALLES SOLDADURA TIPO " + str(row["flange_type"]) + " " + str(row["material"]), sum(row['count'])]

                else:
                    pass

        # Loop to add the drawing number and insert into the database
            for key, value in dict_drawings.items():
                if os.path.exists(key):
                    writer = PdfWriter()
                    reader = PdfReader(key)
                    page_overlay = PdfReader(drawing_number(numorder, value, counter_drawings)).pages[0]
                    reader.pages[0].merge_page(page2=page_overlay)
                    writer.add_page(reader.pages[0])

                    writer.write(key)

                query_insert_drawing = ("""
                    INSERT INTO verification."m_drawing_verification" (num_order, drawing_number, drawing_description, printed_date, printed_state)
                    VALUES (%s, %s, %s, %s, %s)
                    """)

                try:
                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(query_insert_drawing,(numorder,value[0][:4] + f"/{counter_drawings:02d}", value[1], str(datetime.today().strftime('%d/%m/%Y')), 'Realizado por Julio' if username == 'j.zofio' else 'Realizado por Jose Alberto'))
                        conn.commit()

                except (Exception, psycopg2.DatabaseError) as error:
                    MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")

        # elif table_toquery == "tags_data.tags_level":
        #     print('c')

        # elif table_toquery == "tags_data.tags_others":
        # # Obtain the data from the database for temperature tags and create the correspondig dataframe with the necessary columns
        #     query = ('''
        #         SELECT *
        #         FROM tags_data.tags_others
        #         WHERE UPPER (num_order) LIKE UPPER('%%'||%s||'%%') and tag_state = 'PURCHASED'
        #         ''')

        #     try:
        #         with Database_Connection(config_database()) as conn:
        #             with conn.cursor() as cur:
        #                 cur.execute(query,(numorder,))
        #                 results_tags=cur.fetchall()

        #         df_general = pd.DataFrame(results_tags)

        #     except (Exception, psycopg2.DatabaseError) as error:
        #         MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
        #                     + str(error), "critical")

        #     df_selected = df_general.iloc[:, [0, 8, 9, 15]].copy()
        #     df_selected.rename(columns={
        #         0: 'id', 8: 'description', 9: 'code_equipment', 15: 'dim_drawing'
        #     }, inplace=True)

        # # Loop through different types of equipment and create drawings accordingly
        #     for item in df_selected['description'].unique().tolist():
        #         if '2V260' in item:
        #             df_selected_final = df_selected[df_selected['description'].str.contains('2V260')].copy()

        #             df_grouped = df_selected_final.groupby(['description', 'dim_drawing']).size().reset_index(name="count")
        #             grouped_valves = df_grouped.groupby(['description', 'dim_drawing']).agg({"count": list}).reset_index()
        #             total_count = grouped_valves['count'].explode().sum()

        #             drawings_dict = {}

        #             for _, row in grouped_valves.iterrows():
        #                 material = 'A105' if row['description'].split('-')[1] == 'NB' else '316'
        #                 connection_1 = '3/4" NPT' if row['description'].split('-')[2] == '1N' else '1/2" NPT'
        #                 connection_2 = '3/4" NPT' if row['description'].split('-')[3] == '1N' else '1/2" NPT'
        #                 connection_3 = 'Flanged' if row['description'].split('-')[4] == 'F' else 'Welded'
        #                 vent_drain = 'Tapón purga' if row['description'].split('-')[5] == 'Q' else 'Tapón'
        #                 exterior_size = row['description'].split(' / ')[1]

        #                 if connection_3 == 'Flanged':
        #                     coded_connection = (('-0' + exterior_size.split(' ')[0].split('"')[0] if len(exterior_size.split(' ')[0]) == 2 else '-') + ('.5' if ' 1/2' in exterior_size.split(' ')[0] else ('0.75' if '3/4' in exterior_size.split(' ')[0] else '.0')) +
        #                                         ('-0' + str(exterior_size.split(' ')[1].split('#')[0]) if str(exterior_size.split(' ')[1].split('#')[0]) in ['150', '300', '600', '900'] else '-' + ' ' + str(exterior_size.split(' ')[2])))

        #                 if coded_connection in ['-0.75-0150', '-0.75-0300', '01-0150', '01-0300', '1.5-0150']:
        #                     drawing_path_1 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\N-Nivel\V-Visuales\V-Valvulas\B-Bridas\B-220.260\D-Desbaste\NVVBBD-F Forja.pdf"
        #                 else:
        #                     drawing_path_1 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\N-Nivel\V-Visuales\V-Valvulas\B-Bridas\B-220.260\D-Desbaste\NVVBBD-B-{coded_connection}.pdf"
        #                 drawing_path_2 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\N-Nivel\V-Visuales\V-Valvulas\C-Conjuntos\F-Forja\B-220.260\N-260.70.80\X-Comunes\NVVCFBNX-1.0 DesbPCCuerpoVlvBrd.pdf"
        #                 drawing_path_3 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\N-Nivel\V-Visuales\V-Valvulas\C-Conjuntos\F-Forja\B-220.260\N-260.70.80\X-Comunes\NVVCFBNX-1.1 MecCuerpoVlvBrd.pdf"
        #                 drawing_path_4 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\N-Nivel\V-Visuales\V-Valvulas\B-Bridas\B-220.260\A-Acabado\{'RF-RaisedFace' if exterior_size.split(' ')[2] == 'RF' else 'RTJ-RingTypeJoint'}\NVVBBA{'RF' if exterior_size.split(' ')[2] == 'RF' else 'RTJ'}{coded_connection}.pdf"
        #                 if 'BP' in client:
        #                     drawing_path_5 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\X-Comunes\TP-Tapones Purgadores\{'XTP-01.2 TaponPrg 0.50-AISI304L.pdf' if material == '316' else 'XTP-01.3 TaponPrg 0.50-A105 forjado.pdf'}"
        #                 else:
        #                     drawing_path_5 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\X-Comunes\TP-Tapones Purgadores\{'XTP-01.2 TaponPrg 0.50-AISI304L.pdf' if material == '316' else 'XTP-01.4 TaponPrg 0.50-A105 de barra.pdf'}"
        #                 drawing_path_6 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\X-Comunes\TP-Tapones Purgadores\XTP-02 TornilloTaponPrg.pdf"
                        
        #                 description_1 = 'Bridas de desgaste PC ' + exterior_size
        #                 description_2 = 'Cuerpos Válvula 2V260 ' + material
        #                 description_3 = 'Mecanizado conjunto brida-cuerpo ' + material
        #                 description_4 = 'Plano acabado brida ' + exterior_size + ' ' + material
        #                 description_5 = 'Tapones Purgadores ' + material
        #                 description_6 = 'Tornillos Purgadores 304'

        #                 drawings_dict.update({drawing_path_1: description_1,
        #                                     drawing_path_2: description_2,
        #                                     drawing_path_3: description_3,
        #                                     drawing_path_4: description_4,
        #                                     drawing_path_5: description_5,
        #                                     drawing_path_6: description_6})

        #                 if connection_3 == 'Flanged':
        #                     dim_drawing = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\N-Nivel\V-Visuales\V-Valvulas\C-Conjuntos\F-Forja\B-220.260\N-260.70.80\E-260 Estandar\NVVCFBNE-1 Cnj V-260 Brid.pdf"
        #                 else:
        #                     dim_drawing = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\N-Nivel\V-Visuales\V-Valvulas\C-Conjuntos\F-Forja\B-220.260\N-260.70.80\E-260 Estandar\NVVCFBNE-2 Cnj V-260 Boqt.pdf"
        #                 description_dim = str(total_count) + ' válvulas ' + item
        #                 dim_drawing_number = row['dim_drawing']

        #             # Write equipment data
        #                 writer = PdfWriter()
        #                 reader = PdfReader(dim_drawing)
        #                 page_overlay = PdfReader(loose_valves_dwg_dim(numorder, material, connection_1, connection_2, exterior_size, zip(row["count"]))).pages[0]
        #                 reader.pages[0].merge_page(page2=page_overlay)
        #                 writer.add_page(reader.pages[0])
        #                 writer.write(f"{output_path_M}DIM-{dim_drawing_number[:2]}.pdf")

        #             # Write Drawing data
        #                 writer = PdfWriter()
        #                 reader = PdfReader(f"{output_path_M}DIM-{dim_drawing_number[:2]}.pdf")
        #                 page_overlay = PdfReader(drawing_number(numorder, [dim_drawing_number[:2], description_dim, total_count], 1)).pages[0]
        #                 reader.pages[0].merge_page(page2=page_overlay)
        #                 writer.add_page(reader.pages[0])

        #                 writer.write(f"{output_path_M}DIM-{dim_drawing_number[:2]}.pdf")

        #                 query_update_drawing = ("""
        #                     UPDATE verification.workshop_dim_drawings 
        #                     SET drawing_description= %s, printed_date= %s, printed_state= %s
        #                     WHERE num_order = %s AND drawing_number = %s
        #                     """)

        #                 try:
        #                     with Database_Connection(config_database()) as conn:
        #                         with conn.cursor() as cur:
        #                             cur.execute(query_update_drawing,(description_dim, str(datetime.today().strftime('%d/%m/%Y')), 'Realizado por Julio' if username == 'j.zofio' else 'Realizado por Jose Alberto', numorder, '01/01'))
        #                         conn.commit()
        #                 except (Exception, psycopg2.DatabaseError) as error:
        #                     MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
        #                                 + str(error), "critical")

        #                 for drawing, description in drawings_dict.items():
        #                     counter_drawings += 1
        #                     with open(drawing, 'rb') as f:
        #                         writer = PdfWriter()
        #                         reader = PdfReader(f)
        #                         base_page = reader.pages[0]

        #                         if counter_drawings in [2, 3]:
        #                             pdf_buffer = dwg_m_landscape(numorder, zip(row["count"]), material)
        #                         elif counter_drawings in [1, 4, 5]:
        #                             pdf_buffer = general_dwg_m(numorder, zip(row["count"]))
        #                         else:
        #                             pdf_buffer = general_dwg_m(numorder, zip(row["count"]), '304')

        #                         page_overlay = PdfReader(pdf_buffer).pages[0]
                                
        #                         base_page.merge_page(page2=page_overlay)
        #                         writer.add_page(base_page)

        #                         writer.write(str(output_path_M / f"M-{counter_drawings:02d}.pdf"))
        #                         dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", str(sum(row['count'])) + " " + description, sum(row['count'])]

        #         elif 'CN-32218-A1' in item:
        #             df_selected_final = df_selected[df_selected['description'].str.contains('CN-32218-A1')].copy()

        #             df_grouped = df_selected_final.groupby(['description', 'dim_drawing']).size().reset_index(name="count")
        #             grouped_equipment = df_grouped.groupby(['description', 'dim_drawing']).agg({"count": list}).reset_index()
        #             total_count = grouped_equipment['count'].explode().sum()

        #             dim_drawing = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\A-CN32218-A1\TVMTUA-0.0 Cnj CN-32218-A1.pdf"
        #             dim_description = str(total_count) + ' Vainas Múltiples Tubo 3" CN-32218'
        #             dim_drawing_number = grouped_equipment.iloc[0]['dim_drawing']

        #             dict_drawings_M = drawings_tw_32218(total_count)

        #         # Write equipment data
        #             writer = PdfWriter()
        #             reader = PdfReader(dim_drawing)
        #             page_overlay = PdfReader(dwg_dim_32218_32219(numorder, '321', zip(str(total_count)))).pages[0]

        #             base_page = reader.pages[0]

        #             base_page.merge_page(page2=page_overlay)
        #             writer.add_page(reader.pages[0])
        #             writer.write(str(output_path_Dim / f"{dim_drawing_number[:2]}.pdf"))

        #         # Write Drawing data
        #             writer = PdfWriter()
        #             reader = PdfReader(str(output_path_Dim / f"{dim_drawing_number[:2]}.pdf"))
        #             page_overlay = PdfReader(drawing_number_landscape(numorder, [dim_drawing_number[:2], dim_description, total_count], 1)).pages[0]
        #             reader.pages[0].merge_page(page2=page_overlay)
        #             writer.add_page(reader.pages[0])

        #             writer.write(str(output_path_Dim / f"{dim_drawing_number[:2]}.pdf"))

        #             query_update_drawing = ("""
        #                 UPDATE verification.workshop_dim_drawings 
        #                 SET printed_date= %s, printed_state= %s
        #                 WHERE num_order = %s AND drawing_number = %s
        #                 """)

        #             try:
        #                 with Database_Connection(config_database()) as conn:
        #                     with conn.cursor() as cur:
        #                         cur.execute(query_update_drawing,(str(datetime.today().strftime('%d/%m/%Y')), 'Realizado por Julio' if username == 'j.zofio' else 'Realizado por Jose Alberto', numorder, dim_drawing_number))
        #                     conn.commit()

        #             except (Exception, psycopg2.DatabaseError) as error:
        #                 MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
        #                             + str(error), "critical")

        #             for drawing, description in dict_drawings_M.items():
        #                 counter_drawings += 1
        #                 with open(drawing, 'rb') as f:
        #                     writer = PdfWriter()
        #                     reader = PdfReader(f)
        #                     base_page = reader.pages[0]

        #                     if counter_drawings == 1:
        #                         pdf_buffer = dwg_m_welding_32218_32219(numorder, '321', zip(str(total_count)))
        #                     else:
        #                         pdf_buffer = dwg_m_32218_32219(numorder, '321', zip(str(3*int(total_count)))) if any(code in drawing for code in ['TVMTUA-1.3', 'TVMTUX-3', 'TVMTUX-1']) else dwg_m_32218_32219(numorder, '321', zip(str(total_count)))

        #                     page_overlay = PdfReader(pdf_buffer).pages[0]
                            
        #                     base_page.merge_page(page2=page_overlay)
        #                     writer.add_page(base_page)

        #                     writer.write(str(output_path_M / f"M-{counter_drawings:02d}.pdf"))
        #                     dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", description, str(total_count)]

        #         elif 'CN-32219-A1' in item:
        #             df_selected_final = df_selected[df_selected['description'].str.contains('CN-32219-A1')].copy()

        #             df_grouped = df_selected_final.groupby(['description', 'dim_drawing']).size().reset_index(name="count")
        #             grouped_equipment = df_grouped.groupby(['description', 'dim_drawing']).agg({"count": list}).reset_index()
        #             total_count = grouped_equipment['count'].explode().sum()

        #             dim_drawing = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\B-CN32219-A1\TVMTUB-0.0 Cnj CN-32219-A1.pdf"
        #             dim_description = str(total_count) + ' Vainas Múltiples Tubo 3"'
        #             dim_drawing_number = grouped_equipment.iloc[0]['dim_drawing']

        #             dict_drawings_M = drawings_tw_32219(total_count)

        #         # Write equipment data
        #             writer = PdfWriter()
        #             reader = PdfReader(dim_drawing)
        #             page_overlay = PdfReader(dwg_dim_32218_32219(numorder, '321', zip(str(total_count)))).pages[0]

        #             base_page = reader.pages[0]

        #             base_page.merge_page(page2=page_overlay)
        #             writer.add_page(reader.pages[0])
        #             writer.write(str(output_path_Dim / f"{dim_drawing_number[:2]}.pdf"))

        #         # Write Drawing data
        #             writer = PdfWriter()
        #             reader = PdfReader(str(output_path_Dim / f"{dim_drawing_number[:2]}.pdf"))
        #             page_overlay = PdfReader(drawing_number_landscape(numorder, [dim_drawing_number[:2], dim_description, total_count], 1)).pages[0]
        #             reader.pages[0].merge_page(page2=page_overlay)
        #             writer.add_page(reader.pages[0])

        #             writer.write(str(output_path_Dim / f"{dim_drawing_number[:2]}.pdf"))

        #             query_update_drawing = ("""
        #                 UPDATE verification.workshop_dim_drawings 
        #                 SET printed_date= %s, printed_state= %s
        #                 WHERE num_order = %s AND drawing_number = %s
        #                 """)

        #             try:
        #                 with Database_Connection(config_database()) as conn:
        #                     with conn.cursor() as cur:
        #                         cur.execute(query_update_drawing,(str(datetime.today().strftime('%d/%m/%Y')), 'Realizado por Julio' if username == 'j.zofio' else 'Realizado por Jose Alberto', numorder, dim_drawing_number))
        #                     conn.commit()

        #             except (Exception, psycopg2.DatabaseError) as error:
        #                 MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
        #                             + str(error), "critical")

        #             for drawing, description in dict_drawings_M.items():
        #                 counter_drawings += 1
        #                 with open(drawing, 'rb') as f:
        #                     writer = PdfWriter()
        #                     reader = PdfReader(f)
        #                     base_page = reader.pages[0]

        #                     if counter_drawings == 1:
        #                         pdf_buffer = dwg_m_welding_32218_32219(numorder, '321', zip(str(total_count)))
        #                     else:
        #                         pdf_buffer = dwg_m_32218_32219(numorder, '321', zip(str(3*int(total_count)))) if any(code in drawing for code in ['TVMTUB-1.3', 'TVMTUX-3', 'TVMTUX-1']) else dwg_m_32218_32219(numorder, '321', zip(str(total_count)))

        #                     page_overlay = PdfReader(pdf_buffer).pages[0]
                            
        #                     base_page.merge_page(page2=page_overlay)
        #                     writer.add_page(base_page)

        #                     writer.write(str(output_path_M / f"M-{counter_drawings:02d}.pdf"))
        #                     dict_drawings[str(output_path_M / f"M-{counter_drawings:02d}.pdf")] = [f"M-{counter_drawings:02d}.pdf", description, str(total_count)]

        # # Loop to add the drawing number and insert into the database
        #     for key, value in dict_drawings.items():
        #         if os.path.exists(key):
        #             writer = PdfWriter()
        #             reader = PdfReader(key)
        #             if any(term in value[1] for term in ['2V260', 'conjunto brida-cuerpo', 'Mapa Soldaduras']):
        #                 page_overlay = PdfReader(drawing_number_landscape(numorder, value, counter_drawings)).pages[0]
        #             else:
        #                 page_overlay = PdfReader(drawing_number(numorder, value, counter_drawings)).pages[0]
        #             reader.pages[0].merge_page(page2=page_overlay)
        #             writer.add_page(reader.pages[0])

        #             writer.write(key)

        #         query_insert_drawing = ("""
        #             INSERT INTO verification."m_drawing_verification" (num_order, drawing_number, drawing_description, printed_date, printed_state)
        #             VALUES (%s, %s, %s, %s, %s)
        #             """)

        #         try:
        #             with Database_Connection(config_database()) as conn:
        #                 with conn.cursor() as cur:
        #                     cur.execute(query_insert_drawing,(numorder,value[0][:4] + f"/{counter_drawings:02d}", value[1], str(datetime.today().strftime('%d/%m/%Y')), 'Realizado por Julio' if username == 'j.zofio' else 'Realizado por Jose Alberto'))
        #                 conn.commit()

        #         except (Exception, psycopg2.DatabaseError) as error:
        #             MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
        #                         + str(error), "critical")

        MessageHelper.show_message("Planos Generados", "info")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        MessageHelper.show_message("Ha ocurrido un error:\n"
                    "Los planos no se han podido generar", "critical")







# Functions to create dataframes for items drawings
def create_df_flanges_flanged_tw(dataframe):
    dataframe['drawing_code'] = dataframe.apply(
    lambda row: 'TBPC' + ('RF' if str(row['facing']) == 'FF' else str(row['facing'])) +
                '-0' + str(row['size'])[0] + ('.5' if '1/2' in str(row['size']) else '.0') +
                ('-0' + str(row['rating']) if str(row['rating']) in ['150', '300', '600', '900'] else '-' + str(row['rating'])),
    axis=1)

    dataframe['connection'] = dataframe.apply(
    lambda row: str(row['size']) + " " + str(row['rating']) + "#" + str(row['facing']),
    axis=1)
    
    dataframe['drawing_path'] = dataframe.apply(
    lambda row: rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\B-Bridas\PC-Penetracion Completa\{'RTJ-RingTypeJoint'if str(row['facing']) == 'RTJ' else 'RF-RaisedFace'}\{str(row['drawing_code'])}.pdf",
    axis=1)

    dataframe = dataframe[~dataframe['notes_tw'].str.contains('FORJADA', case=False, na=False)].copy()
    df_grouped = dataframe.groupby(['drawing_path','connection','base_tw_diam','material']).size().reset_index(name='count')
    grouped_flanges = df_grouped.groupby(['drawing_path','connection','base_tw_diam','material']).agg({"count": list}).reset_index()

    return grouped_flanges

def create_df_bars_flanged_tw(dataframe):
    # For thermowell with base below 35 mm, p_lenght is 3 mm shorter
    dataframe['p_length'] = dataframe.apply(lambda row: int(row['std_length']) - float(row['tip_thk']) - 3,axis=1)

    dataframe['drawing_code'] = dataframe.apply(
    lambda row: 'TVSCP-Ø' + str(int(row['base_diam'])) + ' Corte-Taladro',
    axis=1)

    dataframe['drawing_path'] = dataframe.apply(
    lambda row: rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\S-Soldadas\C-Cilindricas\P-Preparación\{str(row['drawing_code'])}.pdf",
    axis=1)

    dataframe = dataframe[~dataframe['notes_tw'].str.contains('FORJADA', case=False, na=False)].copy()
    df_grouped = dataframe.groupby(["drawing_path",'base_tw_diam','material', "bore_diam", "std_length","p_length"]).size().reset_index(name="count")
    grouped_bars = df_grouped.groupby(['drawing_path','base_tw_diam','material']).agg({"bore_diam":list, "std_length": list, "p_length": list, "count": list}).reset_index()

    return grouped_bars

def create_df_not_flanged_tw(dataframe, item):
    # For thermowell with base below 35 mm, p_lenght is 3 mm shorter
    dataframe['p_length'] = dataframe.apply(lambda row: int(row['std_length']) - float(row['tip_thk']) - 1,axis=1)

    dataframe['drawing_code'] = dataframe.apply(
    lambda row: 'TVSCP-Ø' + str(row['base_tw_diam']) + ' Corte-Taladro' if float(row['base_tw_diam']) <= 40 else 'TVSCP-ØSuperiores Corte-Taladro',
    axis=1)

    dataframe['drawing_path'] = dataframe.apply(
    lambda row: rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\S-Soldadas\C-Cilindricas\P-Preparación\{str(row['drawing_code'])}.pdf",
    axis=1)

    dataframe = dataframe[~dataframe['notes_tw'].str.contains('FORJADA', case=False, na=False)].copy()
    df_grouped = dataframe.groupby(["drawing_path",'base_tw_diam','material', "bore_diam", "std_length", "p_length"]).size().reset_index(name="count")
    grouped_bars = df_grouped.groupby(['drawing_path','base_tw_diam','material']).agg({"bore_diam":list, "std_length": list, "p_length": list, "count": list}).reset_index()

    return grouped_bars

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

def transform_df_mrun(dataframe):
    dataframe['pipe_int_diam'] = pd.to_numeric(dataframe['pipe_int_diam'], errors='coerce')

    materials = ['ASTM A105', 'ASTM A105+GALV', 'ASTM A105N', 'ASTM A350 LF2 CL1', 'ASTM A350 LF2 CL2']
    sizes_floor = ['3/4"', '1-1/2"', '2"/1-1/2"']
    sizes_ceil  = ['1/2"', '1"', '2"/1"']
    schedules = ['40', '80', 'STD', 'XS']

    # Creating boolean mask
    mask_floor = (dataframe['material'].isin(materials)) & \
                (dataframe['size'].isin(sizes_floor)) & \
                (dataframe['schedule'].isin(schedules))

    mask_ceil = (dataframe['material'].isin(materials)) & \
                (dataframe['size'].isin(sizes_ceil)) & \
                (dataframe['schedule'].isin(schedules))

    # Apply vectorized floor y ceil
    dataframe['final_pipe_int_diam'] = np.where(mask_floor,
                                                np.floor(dataframe['pipe_int_diam']),
                                                np.where(mask_ceil,
                                                        np.ceil(dataframe['pipe_int_diam']),
                                                        dataframe['pipe_int_diam']))

    dataframe['calibrated'] = dataframe.apply(
        lambda row: 'YES' if (row['material'] in ['ASTM A105', 'ASTM A105+GALV', 'ASTM A105N', 'ASTM A350 LF2 CL1', 'ASTM A350 LF2 CL2']
        and row['size'] in ['3/4"', '1-1/2"', '1/2"', '1"', '2"/1-1/2"', '2"/1"']
        and row['schedule'] in ['40', '80', 'STD', 'XS'])
        else 'NO',
        axis=1
    )

    dataframe['taps'] = dataframe.apply(lambda row: 'CORNER' if 'CORNER' in str(row['notes_equipment']).upper() else 'FLANGE',axis=1)

    dataframe['reduction'] = dataframe.apply(lambda row: 'REDUCTION' if '"/' in row['size'] else '',axis=1)

    dataframe['size_orifice_flange'] = dataframe['size'].apply(lambda x: str(x).split('"/')[1] if '"/' in str(x) else x)
    dataframe['rating_orifice_flange'] = dataframe['rating'].apply(lambda x: str(x).split('/')[1] if '/' in str(x) else x)
    dataframe['type_orifice_flange'] = dataframe['flange_type'].apply(lambda x: str(x).split('/')[1] if '/' in str(x) else x)
    dataframe['sch_orifice_flange'] = dataframe['schedule'].apply(lambda x: str(x).split('/')[1] if '/' in str(x) else x)

    dataframe['size_line_flange'] = dataframe['size'].apply(lambda x: str(x).split('"/', 1)[0] + '"' if '"/' in str(x) else x)
    dataframe['rating_line_flange'] = dataframe['rating'].apply(lambda x: str(x).split('/')[0])
    dataframe['type_line_flange'] = dataframe['flange_type'].apply(lambda x: str(x).split('/')[0])
    dataframe['sch_line_flange'] = dataframe['schedule'].apply(lambda x: str(x).split('/')[0])

    dataframe['welding_type_orifice'] = dataframe['flange_type'].map({'WN': 'A', 'SW/SO': 'B', 'SW/WN': 'A'})
    dataframe['welding_type_line'] = dataframe['flange_type'].map({'WN': 'A', 'SW/SO': 'C', 'SW/WN': 'C'})

    dataframe['orifice_flange_code'] = dataframe.apply(lambda row: ('B16.36-' if row['type_orifice_flange'] == 'WN' else 'Socket-') + row['size_orifice_flange'] + '-' + row['rating_orifice_flange'], axis=1)
    dataframe['line_flange_code'] = dataframe.apply(lambda row: ('B16.5-' if row['type_line_flange'] == 'WN' else ('Socket-' if row['type_line_flange'] == 'SW' else 'SlipOn-')) + row['size_line_flange'] + '-' + row['rating_line_flange'], axis=1)

    query_flanges_rf = ("""SELECT code_flange, dim_h, dim_y
                    FROM verification.flanges_verification""")
    query_flanges_rtj = ("""SELECT code_flange, dim_e, dim_y
                    FROM verification.flanges_verification""")
    query_flanges_ff = ("""SELECT code_flange, dim_h
                    FROM verification.flanges_verification""")

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query_flanges_rf)
                results_flanges_rf=cur.fetchall()
                cur.execute(query_flanges_rtj)
                results_flanges_rtj=cur.fetchall()
                cur.execute(query_flanges_ff)
                results_flanges_ff=cur.fetchall()

        flanges_rf = {}
        for item in results_flanges_rf:
            flanges_rf[item[0]] = float(item[1].replace(',', '.') if item[1] != 'N/A' else 0) + float(item[2].replace(',', '.') if item[2] != 'N/A' else 0)

        flanges_rtj = {}
        for item in results_flanges_rtj:
            flanges_rtj[item[0]] = float(item[1].replace(',', '.') if item[1] != 'N/A' else 0) + float(item[2].replace(',', '.') if item[2] != 'N/A' else 0)

        flanges_ff = {}
        for item in results_flanges_ff:
            flanges_ff[item[0]] = float(item[1].replace(',', '.') if item[1] != 'N/A' else 0)

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    dataframe['orifice_flange_height'] = np.select(
        [
            dataframe['facing'].str.contains('RF', na=False),
            dataframe['facing'].str.contains('RTJ', na=False)
        ],
        [
            dataframe['orifice_flange_code'].map(flanges_rf),
            dataframe['orifice_flange_code'].map(flanges_rtj)
        ],
        default=dataframe['orifice_flange_code'].map(flanges_ff)
    ).astype(float)

    dataframe['orifice_flange_height'] = np.floor(dataframe['orifice_flange_height'] - np.where(dataframe['type_orifice_flange'] == 'WN', 1.5, 0))

    dataframe['line_flange_height'] = np.select(
        [
            dataframe['facing'].str.contains('RF', na=False),
            dataframe['facing'].str.contains('RTJ', na=False)
        ],
        [
            dataframe['line_flange_code'].map(flanges_rf),
            dataframe['line_flange_code'].map(flanges_rtj)
        ],
        default=dataframe['line_flange_code'].map(flanges_ff)
    ).astype(float)

    dataframe['line_flange_height'] = np.floor(dataframe['line_flange_height'] - np.where(dataframe['type_line_flange'] == 'WN', 1.5, 0))

    return dataframe

def create_df_orifice_flanges_mrun(dataframe):
    df_orifice_flanges = dataframe.copy()

    df_orifice_flanges.loc[df_orifice_flanges['gasket'].str.contains('SPW', na=False), 'gasket'] = 'SPW'
    df_orifice_flanges.loc[df_orifice_flanges['gasket'].str.contains('Flat', na=False), 'gasket'] = 'Flat'
    df_orifice_flanges.loc[df_orifice_flanges['gasket'].str.contains('RTJ', na=False), 'gasket'] = 'RTJ'

    df_orifice_flanges['drawing_code'] = df_orifice_flanges.apply(
    lambda row: 'CMRB' + str(row['type_orifice_flange']) + ('O' if row['type_orifice_flange'] == 'WN' else '') + str(row['facing']) + ('' if 'CORNER' not in str(row["notes_equipment"]) else 'Q') +
                ('-0' if len(str(row['size_orifice_flange'])) == 2 else '-') + str(row['size_orifice_flange']).split('"')[0] + ('.5' if ' 1/2' in str(row['size_orifice_flange']) else '.0') +
                ('-0' + str(row['rating_orifice_flange']) if str(row['rating_orifice_flange']) in ['150', '300', '600', '900'] else '-' + str(row['rating_orifice_flange'])),
    axis=1)

    df_orifice_flanges['connection'] = df_orifice_flanges.apply(
    lambda row: str(row['size_orifice_flange']) + " " + str(row['rating_orifice_flange']) + "#" + str(row['facing']),
    axis=1)

    df_orifice_flanges['drawing_path'] = df_orifice_flanges.apply(
    lambda row: rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\C-Caudal\MR-MeterRun\B-Bridas\WN-WeldNeck\O-Orificio\{'RF-RaisedFace' if str(row['facing']) == 'RF' else ('FF-FlatFace' if str(row['facing']) == 'FF' else 'RTJ-RingTypeJoint')}\{str(row['drawing_code'])}.pdf" if 'CORNER' not in str(row["notes_equipment"]) else rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\C-Caudal\MR-MeterRun\B-Bridas\WN-WeldNeck\O-Orificio\{'RF-RaisedFace' if str(row['facing']) == 'RF' else ('FF-FlatFace' if str(row['facing']) == 'FF' else 'RTJ-RingTypeJoint')}\Q-CornerTaps\{str(row['drawing_code'])}.pdf",
    axis=1)

    df_grouped = df_orifice_flanges.groupby(['drawing_path','connection', 'schedule', 'material', 'tapping', 'gasket', 'type_orifice_flange', 'type', 'final_pipe_int_diam', 'orifice_flange_height']).size().reset_index(name="count")
    grouped_orifice_flanges = df_grouped.groupby(['drawing_path','connection','schedule','material','tapping', 'gasket', 'type_orifice_flange', "type"]).agg({"final_pipe_int_diam": list, "orifice_flange_height": list, "count": list}).reset_index()

    return grouped_orifice_flanges

def create_df_line_flanges_mrun(dataframe):
    df_line_flanges = dataframe.copy()

    df_line_flanges['drawing_code'] = df_line_flanges.apply(
    lambda row: 'CB' + str(row['type_line_flange']) + ('L'if row['type_line_flange'] == 'WN' else '') + str(row['facing']) +
                ('-0' if len(str(row['size_line_flange'])) == 2 else '-') + str(row['size_line_flange']).split('"')[0] + ('.5' if ' 1/2' in str(row['size_line_flange']) else '.0') +
                ('-0' + str(row['rating_line_flange']) if str(row['rating_line_flange']) in ['150', '300', '600', '900'] else '-' + str(row['rating_line_flange'])),
    axis=1)

    df_line_flanges['connection'] = df_line_flanges.apply(
    lambda row: str(row['size']) + " " + str(row['rating_line_flange']) + "# " + str(row['facing']),
    axis=1)

    df_line_flanges['drawing_path'] = df_line_flanges.apply(
    lambda row: rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\C-Caudal\B-Bridas\WN-WeldNeck\L-Línea\{'RF-RaisedFace' if str(row['facing']) == 'RF' else ('FF-FlatFace' if str(row['facing']) == 'FF' else 'RTJ-RingTypeJoint')}\{str(row['drawing_code'])}.pdf" if row["reduction"] != 'REDUCTION' else rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\C-Caudal\MR-MeterRun\B-Bridas\WN-WeldNeck\L-Línea\RF-RaisedFace\R-Reducciones\CMRBWNLRFR-00 CnjGen Reducc.pdf",
    axis=1)

    df_grouped = df_line_flanges.groupby(['drawing_path','connection', 'schedule', 'material', 'type_line_flange', 'reduction', 'final_pipe_int_diam', 'line_flange_height']).size().reset_index(name="count")
    grouped_line_flanges = df_grouped.groupby(['drawing_path','connection','schedule','material', 'type_line_flange', 'reduction']).agg({"final_pipe_int_diam": list, "line_flange_height":list, "count": list}).reset_index()

    return grouped_line_flanges

def create_df_tubes_mrun(dataframe):
    df_tubes = dataframe.copy()

    df_tubes['connection'] = df_tubes.apply(
    lambda row: str(row['size_orifice_flange']) + " " + str(row['rating_orifice_flange']) + "# " + str(row['facing']),
    axis=1)

    query_mruns = ('''
        SELECT *
        FROM validation_data.mrun_lengths
        ''')
    
    query_ext_diam = ('''
        SELECT line_size, out_diam
        FROM validation_data.pipe_diam
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query_mruns)
                results_mrun=cur.fetchall()

                cur.execute(query_ext_diam)
                results_ext_diam=cur.fetchall()

                mrun_lengths = {item[1] : [item[2], item[3]] for item in results_mrun}
                pipe_ext_diam = {item[0] : item[1] for item in results_ext_diam}

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    df_tubes[['length_long', 'length_short']] = df_tubes['size_orifice_flange'].map(mrun_lengths).apply(pd.Series)

    adjustments_long = {'WN': 1, 'SW/WN': 2, 'SO/WN': -0.5, 'SW/SO': -2, 'SO': -5}
    adjustments_short = {'WN': -4, 'SW/WN': -3, 'SO/WN': -5.5, 'SW/SO': -7, 'SO': -10}

    df_tubes['length_long'] = (
        df_tubes['length_long'].astype(float)
        - df_tubes['orifice_flange_height']
        - df_tubes['line_flange_height']
        + df_tubes['flange_type'].map(adjustments_long).fillna(0)
    )

    df_tubes['length_short'] = (
        df_tubes['length_short'].astype(float)
        - df_tubes['orifice_flange_height']
        - df_tubes['line_flange_height']
        + df_tubes['flange_type'].map(adjustments_short).fillna(0)
    )

    df_tubes['pipe_ext_diam'] = df_tubes['size_orifice_flange'].map(pipe_ext_diam)

    df_tubes['drawing_path'] = df_tubes.apply(
    lambda row: rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\C-Caudal\MR-MeterRun\B-Bridas\X-Comunes\CMRBX-01b TuboMeterRun.pdf",
    axis=1)

    query_inner_in_diam = ('''
    SELECT line_size, sch, in_diam FROM validation_data.pipe_diam
    ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query_inner_in_diam)
                df_diam = pd.DataFrame(cur.fetchall(), columns=['line_size', 'sch', 'in_diam'])

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    df_tubes = df_tubes.merge(df_diam, how='left', left_on=['size_orifice_flange', 'sch_orifice_flange'], right_on=['line_size', 'sch'])
    df_tubes['final_pipe_int_diam'] = df_tubes['in_diam']

    df_grouped = df_tubes.groupby(['drawing_path','size_orifice_flange', 'sch_orifice_flange', 'tube_material', 'calibrated', 'final_pipe_int_diam', 'pipe_ext_diam', 'length_long', 'length_short', 'welding_type_orifice', 'welding_type_line']).size().reset_index(name="count")
    grouped_tubes = df_grouped.groupby(['drawing_path','size_orifice_flange','sch_orifice_flange','tube_material', 'calibrated']).agg({"final_pipe_int_diam": list, "pipe_ext_diam": list, "length_long": list, "length_short": list, "welding_type_orifice": list, "welding_type_line": list, "count": list}).reset_index()

    return grouped_tubes

def create_df_welding_mrun(dataframe):
    df_welding = dataframe.copy()

    df_welding['drawing_path'] = df_welding.apply(
    lambda row: rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\C-Caudal\MR-MeterRun\B-Bridas\X-Comunes\CMRBX-01a TiposAcabadoSoldadura.pdf",
    axis=1)

    df_grouped = df_welding.groupby(['drawing_path','material', 'flange_type']).size().reset_index(name="count")
    grouped_welding = df_grouped.groupby(['drawing_path', 'material', 'flange_type']).agg({"count": list}).reset_index()
    return grouped_welding

def drawings_tw_32218(equipment_count):
    drawings_dict = {}

    drawing_path_1 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\A-CN32218-A1\TVMTUA-1.0 ConjVainaMultipleTubo.pdf"
    drawing_path_2 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\A-CN32218-A1\TVMTUA-1.1 04.00-0600-RF BridaUnion.pdf"
    drawing_path_3 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\A-CN32218-A1\TVMTUA-1.2 TuboVaina.pdf"
    drawing_path_4 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\X-Comunes\TVMTUX-2 TaponCierreVaina.pdf"
    drawing_path_5 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\A-CN32218-A1\TVMTUA-1.3 TuboSensor.pdf"
    drawing_path_6 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\X-Comunes\TVMTUX-3 AccesorioFijacion.pdf"
    drawing_path_7 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\X-Comunes\TVMTUX-1 Reduccion 0.25 SW-NPT.pdf"
    drawing_path_8 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\X-Comunes\TVMTUX-4 SopTaponPurgador.pdf"
    drawing_path_9 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\X-Comunes\TA-Tapones\P-Purgadores\XTAP-¼Inx TaponPrg ¼″NPT AISI321.pdf"
    
    description_1 = 'Mapa Soldaduras'
    description_2 = str(equipment_count) + ' Bridas 4" 600# RF 321'
    description_3 = str(equipment_count) + ' Tubos Vaina 3" SCH 80S 321'
    description_4 = str(equipment_count) + ' Tapones Cierre Vaina 321'
    description_5 = str(3 * int(equipment_count)) + ' Tubo Vaina 1/4" SCH 40S 321'
    description_6 = str(3 * int(equipment_count)) + ' Accesorios Fijación 321'
    description_7 = str(3 * int(equipment_count)) + ' Reducciones 321'
    description_8 = str(equipment_count) + ' Soportes de tapón 321'
    description_9 = str(equipment_count) + ' Tapones Purgadores 321'

    drawings_dict.update({drawing_path_1: description_1,
                        drawing_path_2: description_2,
                        drawing_path_3: description_3,
                        drawing_path_4: description_4,
                        drawing_path_5: description_5,
                        drawing_path_6: description_6,
                        drawing_path_7: description_7,
                        drawing_path_8: description_8,
                        drawing_path_9: description_9})

    return drawings_dict

def drawings_tw_32219(equipment_count):
    drawings_dict = {}

    drawing_path_1 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\B-CN32219-A1\TVMTUB-1.0 ConjVainaMultipleTubo.pdf"
    drawing_path_2 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\B-CN32219-A1\TVMTUB-1.1 04.00-0900-RTJ BridaUnion.pdf"
    drawing_path_3 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\B-CN32219-A1\TVMTUB-1.2 TuboVaina.pdf"
    drawing_path_4 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\X-Comunes\TVMTUX-2 TaponCierreVaina.pdf"
    drawing_path_5 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\B-CN32219-A1\TVMTUB-1.3 TuboSensor.pdf"
    drawing_path_6 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\X-Comunes\TVMTUX-3 AccesorioFijacion.pdf"
    drawing_path_7 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\X-Comunes\TVMTUX-1 Reduccion 0.25 SW-NPT.pdf"
    drawing_path_8 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\T-Temperatura\V-Vainas\M- Multiples\TU-Tipo Tubo\X-Comunes\TVMTUX-4 SopTaponPurgador.pdf"
    drawing_path_9 = rf"\\ERP-EIPSA-DATOS\Comunes\TALLER\Taller24\X-Comunes\TA-Tapones\P-Purgadores\XTAP-¼Inx TaponPrg ¼″NPT AISI321.pdf"
    
    description_1 = 'Mapa Soldaduras'
    description_2 = str(equipment_count) + ' Bridas 4" 900# RTJ 321'
    description_3 = str(equipment_count) + ' Tubos Vaina 3" SCH 80S 321'
    description_4 = str(equipment_count) + ' Tapones Cierre Vaina 321'
    description_5 = str(3 * int(equipment_count)) + ' Tubo Vaina 1/4" SCH 40S 321'
    description_6 = str(3 * int(equipment_count)) + ' Accesorios Fijación 321'
    description_7 = str(3 * int(equipment_count)) + ' Reducciones 321'
    description_8 = str(equipment_count) + ' Soportes de tapón 321'
    description_9 = str(equipment_count) + ' Tapones Purgadores 321'

    drawings_dict.update({drawing_path_1: description_1,
                        drawing_path_2: description_2,
                        drawing_path_3: description_3,
                        drawing_path_4: description_4,
                        drawing_path_5: description_5,
                        drawing_path_6: description_6,
                        drawing_path_7: description_7,
                        drawing_path_8: description_8,
                        drawing_path_9: description_9})

    return drawings_dict
