from utils.Database_Manager import Database_Connection
from utils.Show_Message import MessageHelper
from config.config_functions import config_database
import math
import pandas as pd
from PySide6 import QtWidgets
import psycopg2


def set_prices_flow(proxy, model):
    try:
        valid_flange = ['A105', 'LF2', 'F11', 'F22', 'F5', 'F9', '316', '304']
        valid_gasket = ['CR_CS/316G', 'CRIR_CS/316G/316']
        valid_bolting = ['B72H', 'B72H_FP', 'B7M2HM', 'L7GR7', 'L7MGR7M', 'B16GR4']

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

            tag = str(data(index(row, 1)))
            item_type = str(data(index(row, 8)))
            line_size = str(data(index(row, 9)))
            rating = str(data(index(row, 10)))
            facing = str(data(index(row, 11)))
            flange_material = str(data(index(row, 13)))
            element_material = str(data(index(row, 19)))
            taps_size = str(data(index(row, 16)))
            taps_number = str(data(index(row, 17)))
            plate_thickness = str(data(index(row, 21)))
            gasket_material = str(data(index(row, 23)))
            bolting_material = str(data(index(row, 24))) + " / " + str(data(index(row, 25)))

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

            if (item_type == 'F+P' and
                'NPT' in taps_size and
                '316' in element_code and 
                flange_code in valid_flange and
                gasket_code in valid_gasket and
                bolting_code in valid_bolting):

                if flange_code not in ['316', '304']:
                    flange_code_final = 'A105'
                else:
                    flange_code_final = flange_code

                gasket_code_final = 'CR_CS/316G'
                bolting_code_final = 'B72H'

                code_price = line_size + '-' + rating + '-' + facing + '-' + flange_code_final + '-' + element_code + '-' + taps_number + '-' + plate_thickness + '-' + gasket_code_final + '-' + bolting_code_final

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

            else:
                final_min_price = 'NO TARIFA'
                final_medium_price = 'NO TARIFA'
                final_max_price = 'NO TARIFA'

            items.append([tag, item_type, line_size, rating, facing, flange_material, element_material, taps_number,
                            plate_thickness, gasket_material, bolting_material, final_min_price, final_medium_price, final_max_price])

        df = pd.DataFrame(
            items, columns=[
                'TAG','Tipo','Tamaño','Rating', 'Facing', 'Mat. Brida', 'Mat. Placa', 'Nº Tomas',
                'Esp. Placa', 'Mat. Junta', 'Mat. Torn.', 'MÍNIMO','MEDIO','PVP'
            ])

        output_path , _ = QtWidgets.QFileDialog.getSaveFileName(None, "Guardar Precios Oferta", "", "Archivos de Excel (*.xlsx)")
        if output_path :
            df.to_excel(output_path, index=False)
            MessageHelper.show_message("Excel guardado correctamente", "info")

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                                + str(error), "critical")