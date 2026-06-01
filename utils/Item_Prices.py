from utils.Database_Manager import Database_Connection
from utils.Show_Message import MessageHelper
from config.config_functions import config_database
import math
import pandas as pd
from PySide6 import QtWidgets
import psycopg2
import bisect


def set_prices_flow(proxy, model):
    try:
        valid_flange = ['A105', 'LF2', 'F11', 'F22', 'F5', 'F9']
        valid_gasket = ['CR_CS/316G', 'CRIR_CS/316G/316']
        valid_bolting = ['B72H', 'B72H_FP', 'B7M2HM', 'L7GR7', 'L7MGR7M', 'B16GR4']

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

        for element in id_list:
            row = row_map.get(element)
            if row is None:
                continue

            id_tag = data(index(row, 0))
            tag = str(data(index(row, 1)))
            item_type = str(data(index(row, 8)))
            line_size = str(data(index(row, 9)))
            rating = str(data(index(row, 10)))
            facing = str(data(index(row, 11)))
            schedule = str(data(index(row, 12)))
            flange_material = str(data(index(row, 13)))
            taps_size = str(data(index(row, 16)))
            taps_number = str(data(index(row, 17)))
            element_material = str(data(index(row, 19)))
            plate_type = str(data(index(row, 20)))
            plate_thickness = str(data(index(row, 21)))
            gasket_material = str(data(index(row, 23)))
            bolting_material = str(data(index(row, 24))) + " / " + str(data(index(row, 25)))
            bolting_size = str(data(index(row, 43)))
            bolting_quantity = str(data(index(row, 44)))
            plug_quantity = str(data(index(row, 45)))
            jack_screw_size = str(data(index(row, 46)))
            jack_screw_material = str(data(index(row, 47)))

            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT code_price FROM validation_data.flow_flange_material WHERE flange_material = %s", (flange_material,))
                    flange_code = cur.fetchone()[0]

                    cur.execute("SELECT code_price FROM validation_data.flow_element_material WHERE element_material = %s", (element_material,))
                    element_code = cur.fetchone()[0]

                    cur.execute("SELECT code_price FROM validation_data.flow_gasket_material WHERE gasket_material = %s", (gasket_material,))
                    gasket_code = cur.fetchone()[0]

                    cur.execute("SELECT code_price FROM validation_data.flow_bolts_nuts_material WHERE bolts_nuts_material = %s", (bolting_material,))
                    bolting_code = cur.fetchone()[0]

                    cur.execute("SELECT code_price FROM validation_data.flow_extractor_material WHERE extractor_material = %s", (jack_screw_material,))
                    jack_screw_code = cur.fetchone()[0]

            if (item_type == 'F+P' and
                'NPT' in taps_size):

                flange_code_final = 'A105' if flange_code in valid_flange else flange_code
                gasket_code_final = 'CR_CS/316G' if gasket_code in valid_gasket else gasket_code
                bolting_code_final = 'B72H' if bolting_code in valid_bolting else bolting_code

                code_price = line_size + '-' + rating + '-' + facing + '-' + flange_code_final + '-' + element_code + '-' + taps_number + '-' + plate_thickness + '-' + gasket_code_final + '-' + bolting_code_final

                price_data = None
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.flow_prices WHERE code = %s", (code_price,))
                        price_data = cur.fetchone()

                if price_data is None:
                    code_flange = line_size + '-' + rating + '-' + facing + '-' + flange_code_final + '-' + taps_number
                    code_gasket = line_size + '-' + rating + '-' + facing + '-' + gasket_code
                    code_bolts = (bolting_size if bolting_size != '' else '-') + '-' + bolting_code_final
                    code_jack_screw = (jack_screw_size if jack_screw_size != '' else '-') + '-' + jack_screw_code
                    if 'RTJ' in facing:
                        code_plate = line_size + '-' + rating + '-' + facing + '-' + element_code
                    else:
                        code_plate = line_size + '-' + rating + '-' + facing + '-' + element_code + '-' + plate_thickness
                    code_plugs = taps_size[:-1] + '-A105'

                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute("SELECT material, machining, workforce, extra FROM purch_fact.prices_flow_flange WHERE code = %s", (code_flange,))
                            price_data_flange = cur.fetchone()

                            cur.execute("SELECT material FROM purch_fact.prices_flow_gasket WHERE code = %s", (code_gasket,))
                            price_data_gasket = cur.fetchone()

                            cur.execute("SELECT material FROM purch_fact.prices_flow_bolting WHERE code = %s", (code_bolts,))
                            price_data_bolting = cur.fetchone()

                            cur.execute("SELECT material, elaboration FROM purch_fact.prices_flow_jack_screw WHERE code = %s", (code_jack_screw,))
                            price_data_jack_screw = cur.fetchone()

                            cur.execute("SELECT weight_material, elaboration, workforce FROM purch_fact.prices_flow_plates WHERE code = %s", (code_plate,))
                            price_data_plate = cur.fetchone()

                    if price_data_flange is None:
                        final_min_price, final_medium_price, final_max_price = 'FALTAN DATOS', 'CÁLCULO', 'BRIDAS'

                    elif price_data_gasket is None:
                        final_min_price, final_medium_price, final_max_price = 'FALTAN DATOS', 'CÁLCULO', 'JUNTAS'

                    elif price_data_bolting is None:
                        final_min_price, final_medium_price, final_max_price = 'FALTAN DATOS', 'CÁLCULO', 'TORNILLERIA'

                    elif price_data_jack_screw is None:
                        final_min_price, final_medium_price, final_max_price = 'FALTAN DATOS', 'CÁLCULO', 'EXTRACTORES'

                    elif price_data_plate is None:
                        final_min_price, final_medium_price, final_max_price = 'FALTAN DATOS', 'CÁLCULO', 'PLACA'

                    else:
                        with Database_Connection(config_database()) as conn:
                            with conn.cursor() as cur:
                                cur.execute("SELECT price FROM purch_fact.prices_flow_weight_material WHERE code_material = %s", (element_code,))
                                price_data_material = cur.fetchone()

                        cost_flange = (2 * float(price_data_flange[0]) + float(price_data_flange[1]) + float(price_data_flange[2]) + float(price_data_flange[3]) +
                                        2 * float(price_data_gasket[0]) + 
                                        int(bolting_quantity) * float(price_data_bolting[0]) +
                                        2 * (float(price_data_jack_screw[0]) + float(price_data_jack_screw[1]))
                                        )

                        if facing == 'RTJ':
                            final_cost_plate = float(price_data_plate[0])
                        else:
                            cost_plate = (float(price_data_plate[0]) * float(price_data_material[0])) + float(price_data_plate[1]) + float(price_data_plate[2])
                            final_cost_plate = 1.10 * 1.12 * cost_plate

                        final_cost_flange = 1.10 * 1.12 * cost_flange

                        final_cost_equipment = final_cost_flange + final_cost_plate

                        final_min_price = math.ceil(float(final_cost_equipment) * 1.5 / 5) * 5
                        final_medium_price = math.ceil(float(final_cost_equipment) * 1.7 / 5) * 5
                        final_max_price = math.ceil(float(final_cost_equipment) * 2 / 5) * 5

                else:
                    min_price, medium_price, max_price = price_data[0], price_data[1], price_data[2]

                # Multipliers based on gasket codes
                    if gasket_code == 'CRIR_CS/316G/316':
                        multiplier_gasket = 1.02
                    else:
                        multiplier_gasket = 1

                # Multipliers based on bolting codes
                    if bolting_code in ['B7M2HM', 'L7GR7']:
                        multiplier_bolting = 1.015
                    elif bolting_code in ['L7MGR7M']:
                        multiplier_bolting = 1.025
                    elif bolting_code in ['B16GR4']:
                        multiplier_bolting = 1.02
                    elif bolting_code in ['B72H_FP']:
                        if rating == '300':
                            multiplier_bolting = 1.045
                        else:
                            multiplier_bolting = 1.07
                    else:
                        multiplier_bolting = 1

                # Multipliers based on flange material codes
                    if flange_code_final == 'A105':
                        if flange_code == 'LF2':
                            multiplier_flange = 1.3
                        elif flange_code == 'F11':
                            if line_size in ['2"', '3"', '4"'] or (line_size + rating) == '6"300':
                                multiplier_flange = 4
                            elif int(line_size[:2]) > 10:
                                multiplier_flange = 1.8
                            else:
                                multiplier_flange = 2
                        elif flange_code == 'F22':
                            if line_size in ['2"', '3"', '4"'] or (line_size + rating) == '6"300':
                                multiplier_flange = 3.2
                            elif int(line_size[:2]) > 10:
                                multiplier_flange = 1.8
                            else:
                                multiplier_flange = 2
                        elif flange_code == 'F5':
                            if line_size in ['2"', '3"', '4"'] or (line_size + rating) == '6"300':
                                multiplier_flange = 2
                            elif int(line_size[:2]) > 10:
                                multiplier_flange = 1.5
                            else:
                                multiplier_flange = 1.8
                        elif flange_code == 'F9':
                            if line_size in ['2"', '3"', '4"'] or (line_size + rating) == '6"300':
                                multiplier_flange = 4.2
                            elif int(line_size[:2]) > 10:
                                multiplier_flange = 2.8
                            else:
                                multiplier_flange = 3.5
                        else:
                            multiplier_flange = 1
                    else:
                        multiplier_flange = 1

                    final_min_price = math.ceil(float(min_price) * multiplier_flange * multiplier_gasket * multiplier_bolting / 5) * 5
                    final_medium_price = math.ceil(float(medium_price) * multiplier_flange * multiplier_gasket * multiplier_bolting / 5) * 5
                    final_max_price = math.ceil(float(max_price) * multiplier_flange * multiplier_gasket * multiplier_bolting / 5) * 5

            elif (item_type == 'M.RUN' and
                'NPT' in taps_size and
                '316' in element_code and 
                flange_code in ['A105', '316'] and
                gasket_code in valid_gasket and
                bolting_code in valid_bolting):

                gasket_code_final = 'CR_CS/316G'
                bolting_code_final = 'B72H'

                code_price = item_type + '-' + line_size + '-' + rating + '-' + facing + '-' + schedule + '-' + flange_code + '-' + element_code + '-' + gasket_code_final + '-' + bolting_code_final

                price_data = None
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.flow_prices WHERE code = %s", (code_price,))
                        price_data = cur.fetchone()

                if price_data is None:
                    final_min_price = 'NO TARIFA'
                    final_medium_price = 'NO TARIFA'
                    final_max_price = 'NO TARIFA'
                else:
                    min_price = price_data[0]
                    medium_price = price_data[1]
                    max_price = price_data[2]

                # Multipliers based on gasket codes
                    if gasket_code == 'CRIR_CS/316G/316':
                        multiplier_gasket = 1.02
                    else:
                        multiplier_gasket = 1

                # Multipliers based on bolting codes
                    if bolting_code in ['B7M2HM', 'L7GR7']:
                        multiplier_bolting = 1.015
                    elif bolting_code in ['L7MGR7M']:
                        multiplier_bolting = 1.025
                    elif bolting_code in ['B16GR4']:
                        multiplier_bolting = 1.02
                    elif bolting_code in ['B72H_FP']:
                        if rating == '300':
                            multiplier_bolting = 1.045
                        else:
                            multiplier_bolting = 1.07
                    else:
                        multiplier_bolting = 1

                    final_min_price = math.ceil(float(min_price) * multiplier_gasket * multiplier_bolting / 5) * 5
                    final_medium_price = math.ceil(float(medium_price) * multiplier_gasket * multiplier_bolting / 5) * 5
                    final_max_price = math.ceil(float(max_price) * multiplier_gasket * multiplier_bolting / 5) * 5

            elif(item_type == 'RO' and
                '316' in element_code and
                plate_type == 'RO'):

                code_price = item_type + '-' + line_size + '-' + rating + '-' + facing + '-' + plate_thickness

                price_data = None
                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.flow_prices WHERE code = %s", (code_price,))
                        price_data = cur.fetchone()

                if price_data is None:
                    final_min_price = 'NO TARIFA'
                    final_medium_price = 'NO TARIFA'
                    final_max_price = 'NO TARIFA'
                else:
                    min_price = price_data[0]
                    medium_price = price_data[1]
                    max_price = price_data[2]

                    final_min_price = math.ceil(float(min_price) / 5) * 5
                    final_medium_price = math.ceil(float(medium_price) / 5) * 5
                    final_max_price = math.ceil(float(max_price) / 5) * 5

            else:
                final_min_price = 'NO TARIFA'
                final_medium_price = 'NO TARIFA'
                final_max_price = 'NO TARIFA'

            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    query_update = ("""UPDATE tags_data.tags_flow
                                    SET min_price = %s, medium_price = %s, pvp_price = %s
                                    WHERE id_tag_flow = %s""")
                    cur.execute(query_update, (str(final_min_price).replace('.', ','), str(final_medium_price).replace('.', ','), str(final_max_price).replace('.', ','), id_tag))
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")


def set_prices_temp(proxy, model):
    try:
        valid_materials = ['316', '304', '321', '347', 'ALLOY825', 'INC625', 'MONEL400', 'HASTELLOY276']
        valid_heads = ['EI47', 'EI45', 'EI46', 'EI50/68', 'N/A']
        valid_nipple = ['TU_UNI_A105', 'TU_UNI_SS', 'N/A']
        valid_length = [152, 253, 355, 457, 559, 660, 761, 863, 1016]

        proxy_data = proxy.data
        proxy_index = proxy.index

        data = model.data
        index = model.index

        validation_map_codes = {}
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT tw_material, code_price FROM validation_data.temp_tw_material")
                validation_map_codes['material'] = {row[0]: row[1] for row in cur.fetchall()}

                cur.execute("SELECT head_case_material, code_price FROM validation_data.temp_head_case_material")
                validation_map_codes['head'] = {row[0]: row[1] for row in cur.fetchall()}

                cur.execute("SELECT nipple_ext_material,code_price FROM validation_data.temp_nipple_ext_material")
                validation_map_codes['nipple'] = {row[0]: row[1] for row in cur.fetchall()}

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

            id_tag = data(index(row, 0))
            tag = str(data(index(row, 1)))
            item_type = str(data(index(row, 8)))
            tw_type = str(data(index(row, 9)))
            size = str(data(index(row, 10)))
            rating = str(data(index(row, 11)))
            facing = str(data(index(row, 12)))
            material_tw = str(data(index(row, 14)))
            ins_length = str(data(index(row, 16)))
            sensor = str(data(index(row, 22)))
            nipple_ext_material = str(data(index(row, 29)))
            head_case_material = str(data(index(row, 31)))
            base_tw_diam = str(data(index(row, 50)))

            material_code = validation_map_codes['material'].get(material_tw)
            head_code = validation_map_codes['head'].get(head_case_material)
            nipple_code = validation_map_codes['nipple'].get(nipple_ext_material)

            if (item_type in ('TW+TE', 'TW+TE+TIT', 'TW') and
                tw_type in ['Flanged TW', 'Buttweld TW', 'Socket TW', 'Threaded TW'] and
                head_code in valid_heads and
                nipple_code in valid_nipple):

                length_code = valid_length[bisect.bisect_left(valid_length, int(ins_length))] if int(ins_length) <= valid_length[-1] else None
                base_diam_code = '35' if int(base_tw_diam) <= 35 else base_tw_diam

                code_bar = material_code + '-' + str(base_diam_code) + '-' + str(length_code)
                code_flange = material_code + '-' + size + '-' + rating + '-' + facing + '-FLANGE'
                code_welding = material_code + '-' + size + '-' + rating + '-WELDING'
                code_sensor = ('SENSOR-' + str(length_code)) if 'T/C' in sensor or 'PT100' in sensor else 'N/A'

                price_data_bar = None
                price_data_flange = None
                price_data_welding = None
                price_data_sensor = None
                price_data_head = None
                price_data_nipple = None

                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.temp_prices WHERE code = %s", (code_bar,))
                        price_data_bar = cur.fetchone()

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.temp_prices WHERE code = %s", (code_flange,))
                        price_data_flange = cur.fetchone()
                        price_data_flange = price_data_flange if tw_type == 'Flanged TW' else ((0, 0, 0) if tw_type in ['Buttweld TW', 'Socket TW', 'Threaded TW'] else None)

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.temp_prices WHERE code = %s", (code_welding,))
                        price_data_welding = cur.fetchone()
                        price_data_welding = price_data_welding if tw_type == 'Flanged TW' else ((0, 0, 0) if tw_type in ['Buttweld TW', 'Socket TW', 'Threaded TW'] else None)

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.temp_prices WHERE code = %s", (code_sensor,))
                        price_data_sensor = cur.fetchone()
                        price_data_sensor = price_data_sensor if 'T/C' in sensor or 'PT100' in sensor else ((0, 0, 0) if sensor == 'N/A' else None)

                        if price_data_sensor is not None:
                            if 'T/C' in sensor and 'Double' in sensor:
                                price_data_sensor = tuple(int(price) + 20 for price in price_data_sensor)
                            elif 'PT100' in sensor and 'Single' in sensor:
                                price_data_sensor = tuple(int(price) + 20 for price in price_data_sensor)
                            elif 'PT100' in sensor and 'Double' in sensor:
                                price_data_sensor = tuple(int(price) + 30 for price in price_data_sensor)

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.temp_prices WHERE code = %s", (head_code,))
                        price_data_head = cur.fetchone()
                        price_data_head = price_data_head if head_code != 'N/A' else (0, 0, 0)

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.temp_prices WHERE code = %s", (nipple_code,))
                        price_data_nipple = cur.fetchone()
                        price_data_nipple = price_data_nipple if nipple_code != 'N/A' else (0, 0, 0)

                if any(value is None for value in [price_data_bar, price_data_flange, price_data_welding, price_data_sensor]):
                    code_flange = size + '-' + rating + '-' + facing + '-' + material_code

                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute("SELECT weight, preparation, drilling_tw, roughing, polished, drilling_flange, welding, cleaning, assembly, test_inspection FROM purch_fact.prices_temp_bar WHERE code = %s", (code_bar,))
                            price_data_bar = cur.fetchone()

                            cur.execute("SELECT weight, material, elaboration, workforce FROM purch_fact.prices_temp_flange WHERE code = %s", (code_flange,))
                            price_data_flange = cur.fetchone()

                            cur.execute("SELECT welding FROM purch_fact.prices_temp_flange WHERE code = %s", (code_flange,))
                            price_data_welding = cur.fetchone()

                            cur.execute("SELECT price FROM purch_fact.prices_temp_weight_material WHERE code_material = %s", (material_code,))
                            price_data_material = cur.fetchone()

                    if price_data_material is None:
                        price_material = 0
                    else:
                        price_material = price_data_material[0]

                    if price_data_flange is None:
                        cost_bar = 0
                    else:
                        cost_material_bar = 1.1 * (float(price_data_bar[0]) * float(price_material))
                        cost_elaboration_bar = (float(price_data_bar[1]) + float(price_data_bar[2]) + float(price_data_bar[3]) + float(price_data_bar[4]) + float(price_data_bar[5]) + 
                                            float(price_data_bar[6]) + float(price_data_bar[7]) + float(price_data_bar[8]) + float(price_data_bar[9]))

                        cost_bar = 1.12 * (cost_material_bar + 1.2 * cost_elaboration_bar)

                    min_price_bar = math.ceil(float(cost_bar) * 1.5 / 5) * 5
                    medium_price_bar = math.ceil(float(cost_bar) * 1.7 / 5) * 5
                    max_price_bar = math.ceil(float(cost_bar) * 2 / 5) * 5

                    if tw_type == 'Flanged TW':
                        if price_data_flange is None:
                            cost_flange = 0
                        else:
                            cost_material_flange = 1.1 * ((float(price_data_flange[0]) * float(price_material)) if price_data_flange[1] == '1' else float(price_data_flange[1]))
                            cost_elaboration_flange = 1.1 * float(price_data_flange[2]) + float(price_data_flange[3])

                            cost_flange = cost_material_flange + cost_elaboration_flange

                        min_price_flange = math.ceil(float(cost_flange) * 1.5 / 5) * 5
                        medium_price_flange = math.ceil(float(cost_flange) * 1.7 / 5) * 5
                        max_price_flange = math.ceil(float(cost_flange) * 2 / 5) * 5
                    else:
                        min_price_flange = 0
                        medium_price_flange = 0
                        max_price_flange = 0

                    cost_welding = float(price_data_welding[0]) if price_data_welding is not None else 0

                    min_price_welding = math.ceil(float(cost_welding) * 1.5 / 5) * 5
                    medium_price_welding = math.ceil(float(cost_welding) * 1.7 / 5) * 5
                    max_price_welding = math.ceil(float(cost_welding) * 2 / 5) * 5

                    min_price_sensor, medium_price_sensor, max_price_sensor = price_data_sensor
                    min_price_head, medium_price_head, max_price_head = price_data_head
                    min_price_nipple, medium_price_nipple, max_price_nipple = price_data_nipple

                    total_min_price = float(min_price_bar) + float(min_price_flange) + float(min_price_welding) + float(min_price_sensor) + float(min_price_head) + float(min_price_nipple)
                    total_medium_price = float(medium_price_bar) + float(medium_price_flange) + float(medium_price_welding) + float(medium_price_sensor) + float(medium_price_head) + float(medium_price_nipple)
                    total_max_price = float(max_price_bar) + float(max_price_flange) + float(max_price_welding) + float(max_price_sensor) + float(max_price_head) + float(max_price_nipple)

                    if price_data_bar is None:
                        final_min_price, final_medium_price, final_max_price = 'FALTAN DATOS', 'CÁLCULO', 'VAINA'
                    elif price_data_flange is None:
                        final_min_price, final_medium_price, final_max_price = 'FALTAN DATOS', 'CÁLCULO', 'BRIDA'
                    elif price_data_welding is None:
                        final_min_price, final_medium_price, final_max_price = 'FALTAN DATOS', 'CÁLCULO', 'SOLDADURA'
                    else:
                        final_min_price = math.ceil(total_min_price / 5) * 5
                        final_medium_price = math.ceil(total_medium_price / 5) * 5
                        final_max_price = math.ceil(total_max_price / 5) * 5

                else:
                    min_price_bar, medium_price_bar, max_price_bar = price_data_bar
                    min_price_flange, medium_price_flange, max_price_flange = price_data_flange
                    min_price_welding, medium_price_welding, max_price_welding = price_data_welding
                    min_price_sensor, medium_price_sensor, max_price_sensor = price_data_sensor
                    min_price_head, medium_price_head, max_price_head = price_data_head
                    min_price_nipple, medium_price_nipple, max_price_nipple = price_data_nipple

                    total_min_price = float(min_price_bar) + float(min_price_flange) + float(min_price_welding) + float(min_price_sensor) + float(min_price_head) + float(min_price_nipple)
                    total_medium_price = float(medium_price_bar) + float(medium_price_flange) + float(medium_price_welding) + float(medium_price_sensor) + float(medium_price_head) + float(medium_price_nipple)
                    total_max_price = float(max_price_bar) + float(max_price_flange) + float(max_price_welding) + float(max_price_sensor) + float(max_price_head) + float(max_price_nipple)

                    final_min_price = math.ceil(total_min_price / 5) * 5
                    final_medium_price = math.ceil(total_medium_price / 5) * 5
                    final_max_price = math.ceil(total_max_price / 5) * 5

            else:
                final_min_price = 'NO TARIFA'
                final_medium_price = 'NO TARIFA'
                final_max_price = 'NO TARIFA'

            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    query_update = ("""UPDATE tags_data.tags_temp
                                    SET min_price = %s, medium_price = %s, pvp_price = %s
                                    WHERE id_tag_temp = %s""")
                    cur.execute(query_update, (str(final_min_price).replace('.', ','), str(final_medium_price).replace('.', ','), str(final_max_price).replace('.', ','), id_tag))
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")


def set_prices_level(proxy, model):
    try:
        valid_materials = ['A105', '316']
        valid_valves = ['2V260NB', '2V260NC']
        valid_flange_sizes = ['1"', '"1-1/2"', '3/4"']
        valid_flange_ratings = ['150', '300', '600']
        valid_proc_conn_types = ['Flanged', 'Butt Weld', 'Socket Weld', 'Threaded']

        items = []

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

        for element in id_list:
            row = row_map.get(element)
            if row is None:
                continue

            id_tag = data(index(row, 0))
            tag = str(data(index(row, 1)))
            item_type = str(data(index(row, 8)))
            model_num = str(data(index(row, 9)))
            body_material = str(data(index(row, 10)))
            proc_conn_type = str(data(index(row, 11)))
            proc_conn_size = str(data(index(row, 12)))
            proc_conn_rating = str(data(index(row, 13)))
            valve_type = str(data(index(row, 18)))
            dv_conn = str(data(index(row, 19)))
            dv_size = str(data(index(row, 20)))
            dv_rating = str(data(index(row, 21)))
            gasket_mica = str(data(index(row, 23)))
            illuminator = str(data(index(row, 25)))
            nipple_hex = str(data(index(row, 32)))
            nipple_tub = str(data(index(row, 33)))

            nipple_hex_size = '1/2"' if '1/2"' in nipple_hex else ('3/4"' if '3/4"' in nipple_hex else '')
            nipple_tub_size = '1/2"' if '1/2"' in nipple_tub else ('3/4"' if '3/4"' in nipple_tub else '')

            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT code_price FROM validation_data.level_body_mat WHERE body_mat = %s", (body_material,))
                    body_code = cur.fetchone()
                    body_code = body_code[0] if body_code is not None else None

            if (item_type in ['Reflex', 'Transparent'] and
                body_code in valid_materials and
                valve_type in valid_valves and
                proc_conn_size in valid_flange_sizes and
                proc_conn_rating in valid_flange_ratings and
                proc_conn_type in valid_proc_conn_types):

                code_price_body = model_num + '-' + body_code
                code_price_flange = proc_conn_size + proc_conn_rating + '-' + body_code
                code_price_valve_purge = 'TMGV-' + body_code
                code_price_flange_purge = dv_size + dv_rating + '-' + body_code
                code_price_nipple_hex = 'NIPLO ' + nipple_hex_size + '-' + body_code
                code_price_nipple_tub = 'NIPLO ' + nipple_tub_size + '-' + body_code
                code_price_boq = 'BOQ-' + proc_conn_size + '-' + body_code
                code_price_illuminator = body_code + '-ILUM'

                with Database_Connection(config_database()) as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.level_prices WHERE code = %s", (code_price_body,))
                        price_data_body = cur.fetchone()

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.level_prices WHERE code = %s", (code_price_flange,))
                        price_data_flange = cur.fetchone()

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.level_prices WHERE code = %s", (valve_type,))
                        price_data_valve = cur.fetchone()

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.level_prices WHERE code = %s", (code_price_valve_purge,))
                        price_data_valve_purge = cur.fetchone()

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.level_prices WHERE code = %s", (code_price_nipple_hex,))
                        price_data_nipple_hex = cur.fetchone()

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.level_prices WHERE code = %s", (code_price_nipple_tub,))
                        price_data_nipple_tub = cur.fetchone()

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.level_prices WHERE code = %s", (code_price_boq,))
                        price_data_boq = cur.fetchone()

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.level_prices WHERE code = %s", (code_price_illuminator,))
                        price_data_illuminator = cur.fetchone()

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.level_prices WHERE code = %s", (code_price_flange_purge,))
                        price_data_flange_purge = cur.fetchone()

                        cur.execute("SELECT min_price, medium_price, max_price FROM purch_fact.level_prices WHERE code = %s", ('MICA',))
                        price_data_mica = cur.fetchone()

                min_price_body, medium_price_body, max_price_body = (0, 0, 0) if price_data_body is None else (price_data_body[0], price_data_body[1], price_data_body[2])
                min_price_flange, medium_price_flange, max_price_flange = (0, 0, 0) if price_data_flange is None else (price_data_flange[0], price_data_flange[1], price_data_flange[2])
                min_price_valve, medium_price_valve, max_price_valve = (0, 0, 0) if price_data_valve is None else (price_data_valve[0], price_data_valve[1], price_data_valve[2])
                min_price_valve_purge, medium_price_valve_purge, max_price_valve_purge = (0, 0, 0) if price_data_valve_purge is None else (price_data_valve_purge[0], price_data_valve_purge[1], price_data_valve_purge[2])
                min_price_flange_purge, medium_price_flange_purge, max_price_flange_purge = (0, 0, 0) if price_data_flange_purge is None else (price_data_flange_purge[0], price_data_flange_purge[1], price_data_flange_purge[2])
                min_price_nipple_hex, medium_price_nipple_hex, max_price_nipple_hex = (0, 0, 0) if price_data_nipple_hex is None else (price_data_nipple_hex[0], price_data_nipple_hex[1], price_data_nipple_hex[2])
                min_price_nipple_tub, medium_price_nipple_tub, max_price_nipple_tub = (0, 0, 0) if price_data_nipple_tub is None else (price_data_nipple_tub[0], price_data_nipple_tub[1], price_data_nipple_tub[2])
                min_price_boq, medium_price_boq, max_price_boq = (0, 0, 0) if price_data_boq is None else (price_data_boq[0], price_data_boq[1], price_data_boq[2])
                min_price_illuminator, medium_price_illuminator, max_price_illuminator = (0, 0, 0) if price_data_illuminator is None else (price_data_illuminator[0], price_data_illuminator[1], price_data_illuminator[2])

                price_mica = price_data_mica[0] if price_data_mica is not None else 0

                total_min_price = (float(min_price_body) + 2 * float(min_price_nipple_hex) + 2 * float(min_price_valve) + 
                                    2 * (float(min_price_flange) if proc_conn_type == 'Flanged' else float(min_price_boq)) + 
                                    2 * ((float(min_price_nipple_tub) if dv_conn in ['FLANGED', 'VALVE'] else 0) + 
                                            float(min_price_valve_purge) if dv_conn == 'VALVE' else
                                            (float(min_price_flange_purge) if dv_conn == 'FLANGED' else 0)) +
                                    (float(min_price_illuminator) if illuminator == 'YES' else 0) + 
                                    (int(price_mica) * int(model_num[4]) if 'MICA' in gasket_mica else 0)
                                    )

                total_medium_price = (float(medium_price_body) + 2 * float(medium_price_nipple_hex) + 2 * float(medium_price_valve) + 
                                    2 * (float(medium_price_flange) if proc_conn_type == 'Flanged' else float(medium_price_boq)) + 
                                    2 * ((float(medium_price_nipple_tub) if dv_conn in ['FLANGED', 'VALVE'] else 0) + 
                                            float(medium_price_valve_purge) if dv_conn == 'VALVE' else (float(medium_price_flange_purge) if dv_conn == 'FLANGED' else 0)) +
                                    (float(medium_price_illuminator) if illuminator == 'YES' else 0) + 
                                    (int(price_mica) * int(model_num[4]) if 'MICA' in gasket_mica else 0)
                                    )

                total_max_price = (float(max_price_body) + 2 * float(max_price_nipple_hex) + 2 * float(max_price_valve) + 
                                    2 * (float(max_price_flange) if proc_conn_type == 'Flanged' else float(max_price_boq)) + 
                                    2 * ((float(max_price_nipple_tub) if dv_conn in ['FLANGED', 'VALVE'] else 0) + 
                                            float(max_price_valve_purge) if dv_conn == 'VALVE' else (float(max_price_flange_purge) if dv_conn == 'FLANGED' else 0)) +
                                    (float(max_price_illuminator) if illuminator == 'YES' else 0) + 
                                    (int(price_mica) * int(model_num[4]) if 'MICA' in gasket_mica else 0)
                                    )

                final_min_price = math.ceil(float(total_min_price)/ 5) * 5
                final_medium_price = math.ceil(float(total_medium_price) / 5) * 5
                final_max_price = math.ceil(float(total_max_price) / 5) * 5

            else:
                final_min_price = 'NO TARIFA'
                final_medium_price = 'NO TARIFA'
                final_max_price = 'NO TARIFA'

            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    query_update = ("""UPDATE tags_data.tags_level
                                    SET min_price = %s, medium_price = %s, pvp_price = %s
                                    WHERE id_tag_level = %s""")
                    cur.execute(query_update, (str(final_min_price).replace('.', ','), str(final_medium_price).replace('.', ','), str(final_max_price).replace('.', ','), id_tag))
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")


