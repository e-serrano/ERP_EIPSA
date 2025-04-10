import os
from fpdf import FPDF
import io
import pandas as pd
from config import config
import psycopg2
from PyQt6 import QtCore, QtGui, QtWidgets
import openpyxl
from datetime import date

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"

class PDF(FPDF):
    def rotate(self, angle, x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        angle = -angle
        self._out(f"q {angle:.2f} 0 0 {angle:.2f} {x * self.k:.2f} {-y * self.k:.2f} cm")

    def text_rotated(self, x, y, txt, angle):
        self._out("q")
        self.rotate(angle, x, y)
        self.set_xy(x, y)
        self.cell(20, 20, txt)
        self._out("Q") 


# Function to create PDF with specific note in a position
def new_content_notes(technical_note):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        technical_note (str): The content to be added to the PDF.

    Returns:
        io.BytesIO: A byte stream containing the generated PDF.
    """
    pdf = FPDF(unit='mm')
    pdf.add_font('COURIERTXT', '', os.path.abspath(os.path.join(basedir, "Resources/Iconos/COURIERTXT.ttf")))
    pdf.set_font("courier", "", 10)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()
    pdf.set_xy(20,230)
    pdf.set_font("courier", "B", 10)
    pdf.cell(150, 5, "NOTES:")
    pdf.set_xy(20,235)
    pdf.set_font("courier", "", 10)
    pdf.multi_cell(150, 5, str(technical_note)) #x_position, y_position, technical_note)

    return io.BytesIO(pdf.output())


# Function to create PDF with specific text in a position
def new_content_tags(value, type_eq):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        value (str): The content to be added to the PDF.
        type_eq (str): The type of equipment, determining the positioning in the PDF.

    Returns:
        io.BytesIO: A byte stream containing the generated PDF.
    """
    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)

    excel_file = r"\\nas01\DATOS\Comunes\EIPSA-ERP\Plantillas Importación\Importar Tags Cálculos.xlsx"
    df_data = pd.read_excel(excel_file, sheet_name='Posiciones')
    df_data = df_data.set_index('type')

    x_position = df_data['x(mm)'][type_eq]
    y_position = df_data['y(mm)'][type_eq]

    if type_eq == 'MUL':
        pdf.add_page()
        pdf.set_xy(x_position, y_position)
        with pdf.rotation(90):
            pdf.cell(10, 10, value)

    else:
        pdf.add_page()
        pdf.text(x_position, y_position, value)

    return io.BytesIO(pdf.output())


def drawing_number(num_order, info_drawing, counter):
    """
    Generates a PDF containing a new content based on the specified value and equipment type."
    """
    pdf = FPDF(unit='mm')
    pdf.add_font('IDAutomationHC39M', '', os.path.abspath(os.path.join(basedir, "Resources/Iconos/IDAutomationHC39M_Free.ttf")))
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_xy(163, 262)

    pdf.cell(37, 7, f"{str(info_drawing[0].split('.')[0])}/{counter:02d}", align='C')

    # check_ot = f"SELECT * FROM fabrication.fab_order WHERE id = '{num_order + f"{str(info_drawing[0].split('.')[0])}/{counter:02d}"}'"
    # insert_ot = ("""INSERT INTO fabrication.fab_order (
                    # "id","tag","element","qty_element",
                    # "ot_num","qty_ot","start_date")
                    # VALUES (%s,%s,%s,%s,%s,%s,%s)
                    # """)
    num_ot = 123
    conn = None
    try:
    # read the connection parameters
        params = config()
    # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
    # execution of commands
        # excel_file_path = r"\\nas01\DATOS\Comunes\EIPSA Sistemas de Gestion\MasterCTF\Bases\Contador.xlsm"
        # workbook = openpyxl.load_workbook(excel_file_path, keep_vba=True)
        # worksheet = workbook.active
        # num_ot = worksheet['B2'].value
        # cur.execute(check_ot)
        # results=cur.fetchall()
        # if len(results) == 0:
        data=(num_order + "-" + f"{str(info_drawing[0].split('.')[0])}/{counter:02d}", num_order, info_drawing[1], 1, '{:06}'.format(int(num_ot) + 1), info_drawing[2], date.today().strftime("%d/%m/%Y"))
            # cur.execute(insert_ot, data)
            # worksheet['B2'].value = '{:06}'.format(int(num_ot) + 1)
            # workbook.save(excel_file_path)

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
        print(error)
        dlg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        dlg.exec()
        del dlg, new_icon
    finally:
        if conn is not None:
            conn.close()

    
    num_ot_text = '{:06}'.format(int(num_ot) + 1)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("IDAutomationHC39M", size=16)
    pdf.set_x(-9)
    pdf.set_y(160)
    with pdf.rotation(90):
        pdf.cell(60, 10, "*" + num_ot_text + "*", align='C')
    
    pdf.set_font("helvetica", "B", 12)

    return io.BytesIO(pdf.output())


def flange_dwg_flangedTW(num_order, material, count):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        count (int): The number of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        JOIN validation_data.temp_tw_material AS tw_materials ON tw_materials.code_material = colors.material
        WHERE UPPER (tw_materials.tw_material) LIKE UPPER('%%'||%s||'%%')
        ''')
    conn = None
    try:
    # read the connection parameters
        params = config()
    # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
    # execution of commands
        cur.execute(query,(material,))
        results_colors=cur.fetchall()
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

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_line_width(1)
    pdf.set_draw_color(*map(int, first_color.split(',')))
    pdf.rect(25, 8, 178, 280, style='D')

    pdf.set_draw_color(*map(int, second_color.split(',')))
    pdf.rect(23, 6, 182, 284, style='D')

    if border_color is not None:
        pdf.set_draw_color(*map(int, border_color.split(',')))
        pdf.rect(21, 4, 186, 288, style='D')

    pdf.set_xy(26, 248)
    pdf.cell(19, 9, str(count), align='C')

    pdf.set_xy(48, 248)
    pdf.cell(34, 9, str(material), align='C')

    pdf.set_xy(151, 248)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())


def bar_dwg_flangedTW(num_order, material, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.""
    
    Args:
        num_order (str): The order number.
        material (str): The material code.
        item_data (list): The list of items to be included in the PDF.
    """

    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        JOIN validation_data.temp_tw_material AS tw_materials ON tw_materials.code_material = colors.material
        WHERE UPPER (tw_materials.tw_material) LIKE UPPER('%%'||%s||'%%')
        ''')
    conn = None
    try:
    # read the connection parameters
        params = config()
    # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
    # execution of commands
        cur.execute(query,(material,))
        results_colors=cur.fetchall()
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

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_line_width(1)
    pdf.set_draw_color(*map(int, first_color.split(',')))
    pdf.rect(25, 8, 178, 280, style='D')

    pdf.set_draw_color(*map(int, second_color.split(',')))
    pdf.rect(23, 6, 182, 284, style='D')

    if border_color is not None:
        pdf.set_draw_color(*map(int, border_color.split(',')))
        pdf.rect(21, 4, 186, 288, style='D')

    total_count = 0

    pdf.set_xy(27, 19)

    for bore, std_len, cnt in item_data:
        pdf.cell(15, 6.8, str(cnt), align='C')
        pdf.cell(15, 6.8, str(bore), align='C')
        pdf.cell(15, 6.8, str(int(std_len) + 10), align='C')
        pdf.ln()
        y_pos = pdf.get_y()
        pdf.set_xy(27, y_pos)
        total_count += cnt

    pdf.set_xy(26, 248)
    pdf.cell(19, 9, str(total_count), align='C')

    pdf.set_xy(48, 248)
    pdf.cell(34, 9, str(material), align='C')

    pdf.set_xy(151, 248)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())


def flange_dwg_orifice(num_order, material, schedule, tapping, client, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        schedule (str): The schedule of item
        tapping (str): The tapping configuration
        client (str): The client of the order
        item_data (list): The list of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        JOIN validation_data.flow_flange_material AS flange_materials ON flange_materials.code_material = colors.material
        WHERE UPPER (flange_materials.flange_material) LIKE UPPER('%%'||%s||'%%')
        ''')
    conn = None
    try:
    # read the connection parameters
        params = config()
    # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
    # execution of commands
        cur.execute(query,(material,))
        results_colors=cur.fetchall()
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

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_line_width(1)
    pdf.set_draw_color(*map(int, first_color.split(',')))
    pdf.rect(20, 8, 183, 280, style='D')

    pdf.set_draw_color(*map(int, second_color.split(',')))
    pdf.rect(19, 7, 185, 282, style='D')

    if border_color is not None:
        pdf.set_draw_color(*map(int, border_color.split(',')))
        pdf.rect(18, 6, 197, 284, style='D')

    item_data = list(item_data)

    gasket = item_data[0][0]
    pipe_int_diam = item_data[0][1]
    cnt = item_data[0][2]

    pdf.set_draw_color(255, 0, 0)

    if client =='ARAMCO':
        pdf.line(28, 234, 32, 238)
        pdf.line(28, 238, 32, 234)
        pdf.line(33, 231, 58, 231)
    else:
        pdf.line(28, 229, 32, 233)
        pdf.line(28, 233, 32, 229)
        pdf.line(33, 236, 66, 236)
        pdf.line(33, 240.5, 71, 240.5)

    pdf.set_xy(111, 223.5)
    pdf.cell(30, 6, str(tapping.split('(')[0].strip()), align='C')

    if 'SPW' in gasket:
        x_pos = 158.5
        y_pos = 229.5
        pdf.line(100, 240, 201, 240)
    elif 'RTJ' in gasket:
        x_pos = 162.5
        y_pos = 232.5
    else:
        x_pos = 158.5
        y_pos = 230
        pdf.line(100, 233, 201, 233)
    pdf.set_xy(x_pos, y_pos)
    pdf.cell(12.5, 6.5, str(cnt), align='C')
    pdf.cell(13, 6.5, str(schedule), align='C')
    pdf.cell(17, 6.5, str(pipe_int_diam), align='C')

    pdf.set_xy(26, 248)
    pdf.cell(19, 9, str(cnt), align='C')

    pdf.set_xy(48, 248)
    pdf.cell(34, 9, str(material), align='C')

    pdf.set_xy(83, 248)
    pdf.cell(47, 9, str(tapping[-2:-1]) + " TOMAS POR BRIDA", align='C')

    pdf.set_xy(151, 248)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())









