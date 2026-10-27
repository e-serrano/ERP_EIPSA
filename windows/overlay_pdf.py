from fpdf import FPDF
import os
import io
import re
import math
import pandas as pd
from config.config_functions import config_database, get_path
import psycopg2
from PySide6 import QtWidgets
import openpyxl
from datetime import date
from utils.Database_Manager import Database_Connection
from utils.Show_Message import MessageHelper

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

    def fixed_height_multicell(self, w, total_h, txt, align_mc, fill=False):
        """
        Creates a multi-line cell with a fixed total height, dividing text into lines.

        Parameters:
            w (float): The width of the cell.
            total_h (float): The total height of the cell.
            txt (str): The text to be placed in the cell.
            align_mc (str): The alignment of the text.
            border (str, optional): Border settings for the cell. Defaults to ''.
            fill (bool, optional): Whether to fill the cell with color. Defaults to False.
        """
        txt = txt.replace('\r\n', '\n').replace('\r', '\n')
        paragraphs = txt.split('\n') 
        lines = []
        for paragraph in paragraphs:
            words = paragraph.split() # Divide text in words
            line = ''
            for word in words:
                if self.get_string_width(line + word + ' ') > w - 0.5:
                    lines.append(line) # Add line to line list and starts a new one
                    line = word + ' '
                else:
                    line += word + ' ' # Add word to actual line
            lines.append(line) # Add last line to line list

        if not lines:
            return

        line_height = total_h / len(lines) # Calculate height of each line to get a total height = total_h

        x, y = self.get_x(), self.get_y() # Save actual position

        for line in lines:
            # Print each line with the calculated height
            self.multi_cell(w, line_height, line, align=align_mc, fill=fill)
            self.set_x(x)

        self.set_xy(x, y + total_h)

    def draw_revision_triangle(pdf, x, y, size=4, rev="1"):
        """
        x, y   -> base position (mm)
        size   -> triangle size
        rev    -> revision number
        """

        # Triángulo
        pdf.set_draw_color(255, 0, 0)
        pdf.set_line_width(0.4)

        pdf.line(x, y, x + size, y + size * 2)
        pdf.line(x + size, y + size * 2, x + size * 2, y)
        pdf.line(x + size * 2, y, x, y)

        # Texto revisión
        pdf.set_text_color(255, 0, 0)
        pdf.set_font("Arial", size=6)
        pdf.text(x + size * 0.9, y + size * 1.3, rev)


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
    pdf.add_font('COURIERTXT', '', str(get_path("Resources", "Iconos", "COURIERTXT.ttf")))
    pdf.set_font("courier", "", 10)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()
    pdf.set_xy(20,250)
    pdf.set_font("courier", "B", 10)
    pdf.cell(150, 5, "NOTES:")
    pdf.set_xy(20,255)
    pdf.set_font("courier", "", 10)
    pdf.multi_cell(150, 5, str(technical_note)) #x_position, y_position, technical_note

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

    excel_file = r"\\ERP-EIPSA-DATOS\Comunes\EIPSA-ERP\Plantillas Importación\Importar Tags Cálculos.xlsx"
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




def general_dwg(num_ot, material=None):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        material (str): The material code.
    """
    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.image(str(get_path("Resources", "Iconos", "QualityStamp.png")), x = 3, y = 10, w = 19, h = 11)

    pdf.set_draw_color(255, 0, 0)

    if material is None:
        material = 'A105'

    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf.set_line_width(1)
    pdf.set_draw_color(*map(int, first_color.split(',')))
    pdf.rect(20, 5, 185, 286, style='D')

    pdf.set_draw_color(*map(int, second_color.split(',')))
    pdf.rect(19, 4, 187, 288, style='D')

    if border_color is not None:
        pdf.set_draw_color(*map(int, border_color.split(',')))
        pdf.rect(18, 3, 189, 290, style='D')

    pdf.add_font('IDAutomationHC39M', '', str(get_path("Resources", "Iconos", "IDAutomationHC39M_Free.ttf")))
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("IDAutomationHC39M", size=16)
    pdf.set_x(-9)
    pdf.set_y(160)
    with pdf.rotation(90):
        pdf.cell(60, 10, "*" + num_ot + "*", align='C')

    return io.BytesIO(pdf.output())


def general_dwg_landscape(num_ot, material=None):
    """
    Generates a PDF containing a new content based on the specified value and equipment type."
    """
    pdf = FPDF(unit='mm')
    
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    x_center = pdf.w / 2
    y_center = pdf.h / 2

    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf.add_page()
    with pdf.rotation(angle=-90, x=52, y=1):
        pdf.image(str(get_path("Resources", "Iconos", "QualityStamp.png")), x = 52, y = 1, w = 13, h = 10)

    pdf.set_line_width(1)
    pdf.set_draw_color(*map(int, first_color.split(',')))
    pdf.rect(3, 3, 203, 291, style='D')

    pdf.set_draw_color(*map(int, second_color.split(',')))
    pdf.rect(2, 2, 205, 293, style='D')

    if border_color is not None:
        pdf.set_draw_color(*map(int, border_color.split(',')))
        pdf.rect(1, 1, 207, 295, style='D')

    pdf.set_xy(80, 10)

    pdf.set_text_color(0, 0, 0)
    pdf.add_font('IDAutomationHC39M', '', str(get_path("Resources", "Iconos", "IDAutomationHC39M_Free.ttf")))
    pdf.set_font("IDAutomationHC39M", size=16)
    # with pdf.rotation(180, x_center, y_center):
    pdf.cell(10, 10, "*" + num_ot + "*", align='C')

    pdf.set_font("helvetica", "B", 12)

    return io.BytesIO(pdf.output())


def drawing_number(num_order, info_drawing, counter):
    """
    Generates a PDF containing a new content based on the specified value and equipment type."
    """
    pdf = FPDF(unit='mm')
    pdf.add_font('IDAutomationHC39M', '', str(get_path("Resources", "Iconos", "IDAutomationHC39M_Free.ttf")))
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_xy(163, 262)

    pdf.cell(37, 7, f"{str(info_drawing[0].split('.')[0])}/{counter:02d}", align='C')

    order_id = f"{num_order} - {info_drawing[0].split('.')[0]}/{counter:02d} - {info_drawing[1]}"

    check_ot = f"SELECT * FROM fabrication.fab_order WHERE id = '{order_id}'"

    insert_ot = ("""INSERT INTO fabrication.fab_order (
                    "id","tag","element","qty_element",
                    "ot_num","qty_ot","start_date")
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """)

    try:
        excel_file_path = r"\\ERP-EIPSA-DATOS\Comunes\EIPSA Sistemas de Gestion\MasterCTF\Bases\Contador.xlsm"
        workbook = openpyxl.load_workbook(excel_file_path, keep_vba=True)
        worksheet = workbook.active
        num_ot = worksheet['B2'].value

        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(check_ot)
                results=cur.fetchall()

        if len(results) == 0:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    data=(order_id, num_order, info_drawing[1], 1, '{:06}'.format(int(num_ot) + 1), int(info_drawing[2]), date.today().strftime("%d/%m/%Y"))
                    cur.execute(insert_ot, data)
                conn.commit()

            worksheet['B2'].value = '{:06}'.format(int(num_ot) + 1)
            workbook.save(excel_file_path)
            workbook.close()

            num_ot_text = '{:06}'.format(int(num_ot) + 1)

        else:
            num_ot = '{:06}'.format(int(results[0][4]))
            num_ot_text = '{:06}'.format(int(num_ot))

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("IDAutomationHC39M", size=16)
    pdf.set_x(-9)
    pdf.set_y(160)
    with pdf.rotation(90):
        pdf.cell(60, 10, "*" + num_ot_text + "*", align='C')
    
    pdf.set_font("helvetica", "B", 12)

    return io.BytesIO(pdf.output()), num_ot_text

def drawing_number_x(num_order, info_drawing, counter):
    """
    Generates a PDF containing a new content based on the specified value and equipment type."
    """
    pdf = FPDF(unit='mm')
    pdf.add_font('IDAutomationHC39M', '', str(get_path("Resources", "Iconos", "IDAutomationHC39M_Free.ttf")))
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_xy(163, 262)

    pdf.cell(37, 7, f"{str(info_drawing[0].split('.')[0])}/{counter:02d}", align='C')

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("IDAutomationHC39M", size=16)
    pdf.set_x(-9)
    pdf.set_y(160)
    # with pdf.rotation(90):
    #     pdf.cell(60, 10, "*" + num_ot_text + "*", align='C')
    
    pdf.set_font("helvetica", "B", 12)

    return io.BytesIO(pdf.output())


def drawing_number_landscape(num_order, info_drawing, counter):
    """
    Generates a PDF containing a new content based on the specified value and equipment type."
    """
    pdf = FPDF(unit='mm')
    pdf.add_font('IDAutomationHC39M', '', str(get_path("Resources", "Iconos", "IDAutomationHC39M_Free.ttf")))
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_xy(20, 265)
    with pdf.rotation(270):
        pdf.cell(23, 4, f"{str(info_drawing[0].split('.')[0])}/{counter:02d}", align='C')

    order_id = f"{num_order} - {info_drawing[0].split('.')[0]}/{counter:02d} - {info_drawing[1]}"

    check_ot = f"SELECT * FROM fabrication.fab_order WHERE id = '{order_id}'"

    insert_ot = ("""INSERT INTO fabrication.fab_order (
                    "id","tag","element","qty_element",
                    "ot_num","qty_ot","start_date")
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """)

    try:
        excel_file_path = r"\\ERP-EIPSA-DATOS\Comunes\EIPSA Sistemas de Gestion\MasterCTF\Bases\Contador.xlsm"
        workbook = openpyxl.load_workbook(excel_file_path, keep_vba=True)
        worksheet = workbook.active
        num_ot = worksheet['B2'].value

        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(check_ot)
                results=cur.fetchall()

        if len(results) == 0:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    data=(order_id, num_order, info_drawing[1], 1, '{:06}'.format(int(num_ot) + 1), int(info_drawing[2]), date.today().strftime("%d/%m/%Y"))
                    cur.execute(insert_ot, data)
                conn.commit()

            worksheet['B2'].value = '{:06}'.format(int(num_ot) + 1)
            workbook.save(excel_file_path)

            num_ot_text = '{:06}'.format(int(num_ot) + 1)

        else:
            num_ot = '{:06}'.format(int(results[0][4]))
            num_ot_text = '{:06}'.format(int(num_ot))

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("IDAutomationHC39M", size=16)
    pdf.set_x(160)
    pdf.set_y(8)
    # with pdf.rotation(90):
    pdf.cell(60, 10, "*" + num_ot_text + "*", align='C')

    pdf.set_font("helvetica", "B", 12)

    return io.BytesIO(pdf.output()), num_ot_text

def drawing_number_landscape_x(num_order, info_drawing, counter):
    """
    Generates a PDF containing a new content based on the specified value and equipment type."
    """
    pdf = FPDF(unit='mm')
    pdf.add_font('IDAutomationHC39M', '', str(get_path("Resources", "Iconos", "IDAutomationHC39M_Free.ttf")))
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_xy(18, 263)
    with pdf.rotation(270):
        pdf.cell(23, 4, f"{str(info_drawing[0].split('.')[0])}/{counter:02d}", align='C')

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("IDAutomationHC39M", size=16)
    pdf.set_x(160)
    pdf.set_y(8)
    # with pdf.rotation(90):
    # pdf.cell(60, 10, "*" + num_ot_text + "*", align='C')

    pdf.set_font("helvetica", "B", 12)

    return io.BytesIO(pdf.output())


def general_dwg_m(num_order, item_data, material=None):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        item_data (list): The list of items to be included in the PDF.
    """
    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    cnt = sum(count for count in list(item_data)) if isinstance(item_data, list) else item_data

    pdf.set_draw_color(255, 0, 0)

    pdf.set_xy(27, 248)
    pdf.cell(20, 10, str(cnt), align='C')

    if material is not None:
        pdf.set_xy(47, 248)
        pdf.set_font("helvetica", "B", 8)
        pdf.cell(36, 9, str(material), align='C')

    if material is None:
        material = 'A105'

    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf.set_line_width(1)
    pdf.set_draw_color(*map(int, first_color.split(',')))
    pdf.rect(20, 8, 183, 280, style='D')

    pdf.set_draw_color(*map(int, second_color.split(',')))
    pdf.rect(19, 7, 185, 282, style='D')

    if border_color is not None:
        pdf.set_draw_color(*map(int, border_color.split(',')))
        pdf.rect(18, 6, 197, 284, style='D')

    pdf.set_xy(151, 248)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def dwg_m_landscape(num_order, item_data, material=None):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        item_data (list): The list of items to be included in the PDF.
    """
    if material is None:
        material = 'A105'

    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_line_width(1)
    pdf.set_draw_color(*map(int, first_color.split(',')))
    pdf.rect(3, 3, 203, 291, style='D')

    pdf.set_draw_color(*map(int, second_color.split(',')))
    pdf.rect(2, 2, 205, 293, style='D')

    if border_color is not None:
        pdf.set_draw_color(*map(int, border_color.split(',')))
        pdf.rect(1, 1, 207, 295, style='D')

    cnt = sum(count for count in list(item_data)) if isinstance(item_data, list) else item_data

    pdf.set_draw_color(255, 0, 0)

    pdf.set_xy(35, 166)
    with pdf.rotation(270):
        pdf.cell(10, 10, str(cnt), align='C')

    pdf.set_xy(35, 254)
    with pdf.rotation(270):
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(30, 6, str(num_order), align='C')

    return io.BytesIO(pdf.output())


# Function to create M drawings PDF
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

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

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

def bar_dwg_flangedTW(num_order, material, base_diam, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.""
    
    Args:
        num_order (str): The order number.
        material (str): The material code.
        base_diam (int): The base diameter of equipment
        item_data (list): The list of items to be included in the PDF.
    """

    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        JOIN validation_data.temp_tw_material AS tw_materials ON tw_materials.code_material = colors.material
        WHERE UPPER (tw_materials.tw_material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

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

    for bore, std_len, p_length, cnt in item_data:
        pdf.cell(15, 6.8, str(cnt), align='C')
        pdf.cell(15, 6.8, str(bore), align='C')
        if float(base_diam) <= 35:
            pdf.cell(15, 6.8, str(int(p_length)), align='C')
        elif float(base_diam) <= 40:
            pdf.cell(15, 6.8, str(int(p_length) + 3), align='C')
        else:
            pdf.cell(15, 6.8, str(int(p_length) + 5), align='C')

        if float(base_diam) <= 35:
            pdf.cell(15, 6.8, str(int(std_len) + 10), align='C')
        elif float(base_diam) <= 40:
            pdf.cell(15, 6.8, str(int(std_len) + 10 + 3), align='C')
        else:
            pdf.cell(15, 6.8, str(int(std_len) + 10 + 5), align='C')

        pdf.ln()
        y_pos = pdf.get_y()
        pdf.set_xy(27, y_pos)
        total_count += int(cnt)

    pdf.set_xy(172, 208)
    with pdf.rotation(90):
        pdf.cell(11, 7, str(int(std_len) + 10 - int(p_length)), align='C')
    
    pdf.set_xy(26, 248)
    pdf.cell(19, 9, str(total_count), align='C')

    pdf.set_xy(48, 248)
    pdf.cell(34, 9, str(material), align='C')

    pdf.set_xy(151, 248)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def tube_dwg_flangedTW(num_order, material, item_data):
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

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

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

    pdf.set_xy(142, 16)

    for std_len, cnt in item_data:
        pdf.cell(12, 7.1, str(cnt), align='C')
        pdf.cell(10, 7.1, str(int(std_len) - 264), align='C')
        pdf.cell(10, 7.1, str(int(std_len) + 1), align='C')

        pdf.ln()
        y_pos = pdf.get_y()
        pdf.set_xy(142, y_pos)
        total_count += int(cnt)

    pdf.set_xy(26, 248)
    pdf.cell(19, 9, str(total_count), align='C')

    pdf.set_xy(48, 248)
    pdf.cell(34, 9, str(material), align='C')

    pdf.set_xy(151, 248)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def bar_dwg_notflangedTW(num_order, material, base_diam, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.""
    
    Args:
        num_order (str): The order number.
        material (str): The material code.
        base_diam (str): The base diameter of equipment
        item_data (list): The list of items to be included in the PDF.
    """

    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        JOIN validation_data.temp_tw_material AS tw_materials ON tw_materials.code_material = colors.material
        WHERE UPPER (tw_materials.tw_material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

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

    for bore, std_len, p_length, cnt in item_data:
        pdf.cell(15, 6.8, str(cnt), align='C')
        pdf.cell(15, 6.8, str(bore), align='C')

        if float(base_diam) < 38:
            pdf.cell(15, 6.8, str(int(p_length)), align='C')
        elif float(base_diam) < 45:
            pdf.cell(15, 6.8, str(int(p_length) + 3), align='C')
        else:
            pdf.cell(15, 6.8, str(int(p_length) + 5), align='C')

        if float(base_diam) < 38:
            pdf.cell(15, 6.8, str(int(std_len) + 10), align='C')
        elif float(base_diam) < 45:
            pdf.cell(15, 6.8, str(int(std_len) + 10 + 3), align='C')
        else:
            pdf.cell(15, 6.8, str(int(std_len) + 10 + 5), align='C')

        pdf.ln()
        y_pos = pdf.get_y()
        pdf.set_xy(27, y_pos)
        total_count += cnt

    pdf.set_xy(172, 208)
    with pdf.rotation(90):
        pdf.cell(11, 7, str(int(std_len) + 10 - int(p_length)), align='C')

    pdf.set_xy(26, 248)
    pdf.cell(19, 9, str(total_count), align='C')

    pdf.set_xy(48, 248)
    pdf.cell(34, 9, str(material), align='C')

    pdf.set_xy(151, 248)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def flange_dwg_orifice(num_order, type, material, schedule, tapping_size, tapping_num, tapping_orientation, gasket, type_flange, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        type (str): The type of equipment.
        material (str): The material code.
        schedule (str): The schedule of item
        tapping (str): The tapping configuration
        gasket (str): The type of gasket.
        type_flange (str): The type of flange.
        item_data (list): The list of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        JOIN validation_data.flow_flange_material AS flange_materials ON flange_materials.code_material = colors.material
        WHERE UPPER (flange_materials.flange_material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf = PDF()
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

    if type == 'M.RUN':
        pipe_int_diam = item_data[0][0]
        flange_height = item_data[0][1]
        cnt = item_data[0][2] * len(item_data)
    else:
        pipe_int_diam = item_data[0][0]
        cnt = item_data[0][1] * len(item_data)

    pdf.set_draw_color(255, 0, 0)

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_xy(29, 200)
    pdf.fixed_height_multicell(100, 6.5, "ORIENTACIÓN TOMAS: " + str(tapping_orientation), 'L')
    
    pdf.set_xy(29, 210)
    pdf.fixed_height_multicell(100, 6.5, "EXTRACTORES A UN TALADRO A LA IZQUIERDA DE LA TOMA\nSEGÚN PLANO GENERAL", 'L')
    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.line(28, 234, 32, 238)
    pdf.line(28, 238, 32, 234)
    pdf.line(27, 231, 58, 231)

    if type == 'M.RUN':
        if type_flange == 'WN':
            pdf.set_line_width(0.5)
            pdf.set_draw_color(49, 49, 229)
            pdf.line(135, 31, 160, 14)

            pdf.circle(130, 31, 5, style='D')

            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_xy(160, 14)
            pdf.cell(0.1, 0.1, "ACABADO TIPO A")

            pdf.set_draw_color(255, 0, 0)
            pdf.set_line_width(1)
            pdf.line(192, 68, 195, 75)

            pdf.set_xy(193, 87)
            with pdf.rotation(90):
                pdf.cell(0.1, 0.1, f"{flange_height:.1f}")
        else:
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_xy(160, 14)
            pdf.cell(0.1, 0.1, "ACABADO TIPO B")

    pdf.set_xy(111, 223.5)
    pdf.cell(30, 6, str(tapping_size), align='C')

    if gasket != 'N/A':
        if 'SPW' in gasket.upper():
            x_pos = 158.5
            y_pos = 229.5
            pdf.line(100, 240, 201, 240)
        elif 'RTJ' in gasket.upper():
            x_pos = 162.5
            y_pos = 232.5
        elif 'FLAT' in gasket.upper():
            x_pos = 158.5
            y_pos = 236
            pdf.line(100, 233, 201, 233)
        pdf.set_xy(x_pos, y_pos)
        pdf.cell(12.5, 6.5, str(2*cnt), align='C')
        pdf.cell(13, 6.5, str(schedule), align='C')
        pdf.cell(17, 6.5, str(pipe_int_diam), align='C')
    else:
        x_pos = 158.5
        y_pos = 229.5
        pdf.set_xy(x_pos, y_pos)
        pdf.cell(12.5, 6.5, str(2*cnt), align='C')
        pdf.cell(13, 6.5, str(schedule), align='C')
        pdf.cell(17, 6.5, str(pipe_int_diam), align='C')

    pdf.set_xy(26, 248)
    pdf.cell(19, 9, str(2*cnt), align='C')

    pdf.set_xy(48, 248)
    pdf.set_font("helvetica", "B", 8)
    pdf.cell(34, 9, str(material), align='C')

    pdf.set_xy(83, 248)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(47, 9, str(int(tapping_num)) + " POR BRIDA", align='C')

    pdf.set_xy(151, 248)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def flange_dwg_line(num_order, material, schedule, type_flange, reduction, connection, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        schedule (str): The schedule of item.
        type_flange (str): The type of flange.
        reduction (str): If reduction exists.
        connection (str): The type of connection.
        item_data (list): The list of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        JOIN validation_data.flow_flange_material AS flange_materials ON flange_materials.code_material = colors.material
        WHERE UPPER (flange_materials.flange_material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication([])

        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf = FPDF(unit='mm')
    pdf.set_auto_page_break(auto=False)
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)
    pdf.set_draw_color(255, 0, 0)

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
    cnt = item_data[0][2]

    if reduction != 'REDUCTION':
        pipe_int_diam = item_data[0][0]
        flange_height = item_data[0][1]

        if type_flange == 'WN':
            pdf.line(192, 68, 195, 75)

            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_xy(38, 60)
            pdf.cell(20, 5, "A", align='C')

            pdf.set_xy(193, 95)
            with pdf.rotation(90):
                pdf.cell(0.1, 0.1, f"{flange_height:.1f}")
        elif type_flange == 'SW':
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_xy(160, 14)
            pdf.cell(0.1, 0.1, "ACABADO TIPO C")
        else:
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_xy(160, 14)
            pdf.cell(0.1, 0.1, "ACABADO TIPO B")

        pdf.set_xy(93, 250)
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(10, 5, str(schedule), align='C')

        pdf.set_xy(108, 250)
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(14, 5, str(pipe_int_diam), align='C')

    else:
        outter_size = connection.split(' ')[0].rsplit('"/',1)[0].strip() + '"'
        inner_size = connection.split(' ')[0].rsplit('"/',1)[1].strip()
        outter_sch = schedule.split(' / ')[0].strip() if '/' in schedule else schedule
        inner_sch = schedule.split(' / ')[1].strip() if '/' in schedule else schedule
        rating = connection.split('#')[0].split(' ')[1].strip()
        facing = connection.split(' ')[2].strip()

        query_outter_in_diam = ('''
        SELECT in_diam FROM validation_data.pipe_diam
        WHERE line_size = %s and sch = %s
        ''')

        query_inner_in_diam = ('''
        SELECT in_diam FROM validation_data.pipe_diam
        WHERE line_size = %s and sch = %s
        ''')

        query_outter_flange_size_rf = ('''
        SELECT dim_o, dim_w, dim_rf, dim_x, num_tal, dim_lrf, dim_tf, dim_h, dim_y FROM verification.flanges_verification
        WHERE code_flange = %s
        ''')

        query_inner_flange_size_rf = ('''
        SELECT dim_ah FROM verification.flanges_verification
        WHERE code_flange = %s
        ''')

        try:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(query_outter_in_diam, (outter_size,outter_sch,))
                    results_outter_in_diam=cur.fetchall()

                    cur.execute(query_inner_in_diam, (inner_size,inner_sch,))
                    results_inner_in_diam=cur.fetchall()

                    if facing in ['RF', 'FF']:
                        cur.execute(query_outter_flange_size_rf, ('B16.5-' + outter_size + '-' + rating,))
                        results_outter_flange=cur.fetchall()

                        cur.execute(query_inner_flange_size_rf, ('B16.5-' + inner_size + '-' + rating,))
                        results_inner_flange=cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            app = QtWidgets.QApplication.instance()
            if app is None:
                app = QtWidgets.QApplication([])

            MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

        j_diam_outter = results_outter_in_diam[0][0]
        j_diam_innner = results_inner_in_diam[0][0]
        dim_o = results_outter_flange[0][0]
        dim_w = results_outter_flange[0][1]
        dim_rf = results_outter_flange[0][2]
        dim_x = results_outter_flange[0][3]
        num_tal = results_outter_flange[0][4]
        dim_lrf = results_outter_flange[0][5]
        dim_tf = results_outter_flange[0][6]
        dim_h = results_outter_flange[0][7]
        dim_y = results_outter_flange[0][8]
        dim_ah = results_inner_flange[0][0]

        pdf.set_font('Helvetica', 'B', 8)

        pdf.set_xy(105, 223)
        pdf.cell(10, 5, str(dim_o), align='C')

        pdf.set_xy(104, 216)
        pdf.cell(10, 5, str(dim_rf), align='C')

        pdf.set_xy(105, 209)
        pdf.cell(10, 5, str(j_diam_outter), align='C')

        pdf.set_xy(104, 123)
        pdf.cell(10, 5, str(dim_x), align='C')

        pdf.set_xy(167, 69)
        pdf.cell(10, 5, f"{float(dim_w.replace(',','.')) / 2:.1f}", align='C')

        pdf.set_xy(161, 166)
        pdf.cell(4, 5, str(num_tal), align='C')

        pdf.set_xy(172, 166)
        pdf.cell(7, 5, str(dim_lrf), align='C')

        pdf.set_xy(184, 196)
        with pdf.rotation(90):
            pdf.cell(5, 5, f"{(float(dim_h.replace(',','.')) + float(dim_tf.replace(',','.'))):.1f}")

        pdf.set_xy(184, 174)
        with pdf.rotation(90):
            pdf.cell(5, 5, f"{round(float(dim_y.replace(',','.')) - float(dim_h.replace(',','.')) - float(dim_tf.replace(',','.')), 1):.1f}")

        pdf.set_xy(175, 148)
        with pdf.rotation(90):
            pdf.cell(5, 5, str('??'))

        pdf.set_xy(30, 184)
        with pdf.rotation(90):
            pdf.cell(5, 5, str(dim_y))

        pdf.set_xy(106, 137)
        pdf.cell(9, 5, str(j_diam_innner), align='C')

        pdf.set_xy(104, 130)
        pdf.cell(10, 5, str(dim_ah), align='C')

        pdf.set_xy(124, 266)
        pdf.cell(10, 5, str(rating), align='C')

        pdf.set_xy(113, 272)
        pdf.cell(10, 5, str(outter_size.split('"')[0]), align='C')

        pdf.set_xy(150, 272)
        pdf.cell(10, 5, str(inner_size.split('"')[0]), align='C')

    pdf.set_xy(26, 248)
    pdf.cell(19, 9, str(2*cnt), align='C')

    pdf.set_xy(48, 248)
    pdf.set_font("helvetica", "B", 8)
    pdf.cell(34, 9, str(material), align='C')

    pdf.set_xy(83, 248)
    pdf.cell(46, 9, 'SCH ' + str(schedule), align='C')

    pdf.set_xy(151, 248)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def tube_dwg_meterrun(num_order, size, schedule, tube_material, calibrated, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        size (str): The size of the tube.
        schedule (str): The schedule of item
        tube_material (str): The material code of the tube.
        calibrated (bool): Indicates if the tube is calibrated.
        item_data (list): The list of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        JOIN validation_data.flow_tube_material AS tube_materials ON tube_materials.code_material = colors.material
        WHERE UPPER (tube_materials.tube_material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(tube_material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

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

    final_pipe_int_diam = item_data[0][0]
    pipe_ext_diam = item_data[0][1]
    length_1 = item_data[0][2]
    length_2 = item_data[0][3]
    welding_type_orifice = item_data[0][4]
    welding_type_line = item_data[0][5]
    cnt = item_data[0][6]

    pdf.set_draw_color(255, 0, 0)

    pdf.set_xy(65, 183)
    pdf.set_font("helvetica", "B", 12)
    if calibrated == 'YES':
        pdf.cell(40, 8, "TUBO CALIBRADO " + str(size), align='C')

        query = ("SELECT calibrated_int, calibrated_ext FROM validation_data.pipe_diam WHERE line_size = %s and sch = %s")
        try:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(query,(size, schedule))
                    results_tube_calibrated=cur.fetchall()
                    final_pipe_int_diam = results_tube_calibrated[0][0]
                    pipe_ext_diam = results_tube_calibrated[0][1]

        except (Exception, psycopg2.DatabaseError) as error:
            MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                        + str(error), "critical")

    else:
        pdf.cell(40, 8, "TUBO " + str(size) + " SCH " + str(schedule), align='C')

    pdf.set_xy(39, 210)
    pdf.cell(14, 5, str(cnt), align='C')
    pdf.cell(45, 5, str(welding_type_orifice), align='C')
    pdf.cell(44, 5, str(welding_type_line), align='C')
    pdf.cell(14, 5, str(length_1), align='C')
    pdf.cell(15, 5, str(final_pipe_int_diam), align='C')
    pdf.cell(15, 5, str(pipe_ext_diam), align='C')

    pdf.set_xy(39, 216)
    pdf.cell(14, 5, str(cnt), align='C')
    pdf.cell(45, 5, str(welding_type_orifice), align='C')
    pdf.cell(44, 5, str(welding_type_line), align='C')
    pdf.cell(14, 5, str(length_2), align='C')
    pdf.cell(15, 5, str(final_pipe_int_diam), align='C')
    pdf.cell(15, 5, str(pipe_ext_diam), align='C')

    pdf.set_xy(27, 248)
    pdf.cell(20, 10, str(cnt), align='C')
    
    pdf.set_xy(47, 248)
    pdf.set_font("helvetica", "B", 8)
    pdf.cell(36, 9, str(tube_material), align='C')

    pdf.set_xy(151, 248)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def welding_dwg_meterrun(num_order, material, flange_type, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        flange_type (str): The type of flange.
        item_data (list): The list of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        JOIN validation_data.flow_flange_material AS flange_materials ON flange_materials.code_material = colors.material
        WHERE UPPER (flange_materials.flange_material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

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

    cnt = item_data[0][0]

    pdf.set_draw_color(255, 0, 0)

    pdf.set_xy(27, 248)
    pdf.cell(20, 10, str(4*cnt), align='C')
    
    pdf.set_xy(47, 248)
    pdf.set_font("helvetica", "B", 8)
    pdf.cell(36, 9, str(material), align='C')

    pdf.set_xy(151, 248)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def dwg_m_welding_32218_32219(num_order, material, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        item_data (list): The list of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_line_width(1)
    pdf.set_draw_color(*map(int, first_color.split(',')))
    pdf.rect(3, 15, 203, 277, style='D')

    pdf.set_draw_color(*map(int, second_color.split(',')))
    pdf.rect(2, 13, 205, 279, style='D')

    if border_color is not None:
        pdf.set_draw_color(*map(int, border_color.split(',')))
        pdf.rect(1, 11, 207, 281, style='D')

    item_data = list(item_data)

    cnt = item_data[0][0]

    pdf.set_draw_color(255, 0, 0)

    pdf.set_xy(31, 179)
    with pdf.rotation(270):
        pdf.cell(10, 7, str(cnt), align='C')

    pdf.set_xy(31, 260)
    with pdf.rotation(270):
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(30, 7, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def dwg_m_32218_32219(num_order, material, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        item_data (list): The list of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

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

    cnt = item_data[0][0]

    pdf.set_draw_color(255, 0, 0)

    pdf.set_xy(27, 248)
    pdf.cell(20, 10, str(cnt), align='C')

    pdf.set_xy(151, 248)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def body_dwg_level(num_order, material, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        item_data (list): The list of items to be included in the PDF.
    """

    positions = {'4': 143,
                '5': 153,
                '6': 163,
                '7': 173,
                '8': 183,
                '9': 193}

    item_data = list(item_data)
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_line_width(1)
    pdf.set_draw_color(*map(int, first_color.split(',')))
    pdf.rect(3, 3, 203, 291, style='D')

    pdf.set_draw_color(*map(int, second_color.split(',')))
    pdf.rect(2, 2, 205, 293, style='D')

    if border_color is not None:
        pdf.set_draw_color(*map(int, border_color.split(',')))
        pdf.rect(1, 1, 207, 295, style='D')

    pdf.set_draw_color(255, 0, 0)

    x, y = 81, 134
    for model_num, nipple_conn, count in item_data:
        y = positions.get(str(model_num[-1]), y)
        if '1/2' in str(nipple_conn):
            y += 5

        pdf.set_xy(210 - y, x)
        with pdf.rotation(270):
            pdf.cell(9, 5, str(count), align='C')

    total_count = sum(count for _, _, count in item_data)
    pdf.set_xy(33, 166)
    with pdf.rotation(270):
        pdf.cell(14, 10, f"{total_count}", align='C')

    pdf.set_xy(33, 256)
    with pdf.rotation(270):
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(36, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def cover_dwg_level(num_order, material, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        item_data (list): The list of items to be included in the PDF.
    """

    positions = {'211': 187,
                '212': 193,
                '213': 199,
                '214': 205,
                '215': 212,
                '216': 218,
                '217': 224,
                '218': 231,
                '219': 237}

    item_data = list(item_data)

    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_line_width(1)
    pdf.set_draw_color(*map(int, first_color.split(',')))
    pdf.rect(3, 3, 203, 291, style='D')

    pdf.set_draw_color(*map(int, second_color.split(',')))
    pdf.rect(2, 2, 205, 293, style='D')

    if border_color is not None:
        pdf.set_draw_color(*map(int, border_color.split(',')))
        pdf.rect(1, 1, 207, 295, style='D')

    pdf.set_draw_color(255, 0, 0)

    x, y = 187, 187
    for section, qty, count in item_data:
        y = positions.get(str(section), y)

        pdf.set_xy(x, y)
        pdf.cell(9, 6, str(int(qty) * int(count)), align='C')

    total_count = sum(int(qty) * int(count) for _, qty, count in item_data)
    pdf.set_xy(26, 248)
    pdf.cell(19, 9, str(total_count), align='C')

    pdf.set_xy(151, 248)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def valves_dwg_level(num_order, valve_type, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        valve_type (str): The type of valve.
        item_data (list): The list of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    item_data = list(item_data)
    material = 'A105' if 'NB' in valve_type else '316'
    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

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
        pdf.rect(18, 6, 187, 284, style='D')

    pdf.set_draw_color(255, 0, 0)

    y = 146
    for exterior_size, connection_1, connection_2, cnt in item_data:
        if (str(connection_1).split(' ')[0] + ' NPT') != (str(connection_2).split(' ')[0] + ' NPT'):
            pdf.set_xy(44, y)
            pdf.cell(27, 9, str(cnt), align='C')
        else:
            pdf.set_xy(44, y)
            pdf.cell(27, 9, str(2 * int(cnt)), align='C')

        pdf.set_xy(72, y)
        pdf.cell(27, 9, str(material), align='C')

        pdf.set_xy(100, y)
        pdf.cell(27, 9, str(exterior_size), align='C')

        pdf.set_xy(128, y)
        pdf.cell(27, 9, str(connection_1).split(' ')[0] + ' NPT', align='C')

        pdf.set_xy(156, y)
        pdf.cell(27, 9, str(connection_2).split(' ')[0] + ' NPT', align='C')

        if (str(connection_1).split(' ')[0] + ' NPT') != (str(connection_2).split(' ')[0] + ' NPT'):
            pdf.set_xy(44, y + 9)
            pdf.cell(27, 9, str(cnt), align='C')

            pdf.set_xy(72, y + 9)
            pdf.cell(27, 9, str(material), align='C')

            pdf.set_xy(100, y + 9)
            pdf.cell(27, 9, str(exterior_size), align='C')

            pdf.set_xy(128, y + 9)
            pdf.cell(27, 9, str(connection_2).split(' ')[0] + ' NPT', align='C')

            pdf.set_xy(156, y + 9)
            pdf.cell(27, 9, str(connection_1).split(' ')[0] + ' NPT', align='C')

        y += 9

    total_count = sum(int(count) for _, _, _, count in item_data)
    pdf.set_xy(27, 248)
    pdf.cell(20, 10, str(2*total_count), align='C')
    
    pdf.set_xy(47, 248)
    pdf.set_font("helvetica", "B", 8)
    pdf.cell(36, 9, str(material), align='C')

    pdf.set_xy(151, 248)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def nipple_hex_dwg_level(num_order, material, count):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material of item
        item_data (list): The list of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

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
        pdf.rect(18, 6, 187, 284, style='D')

    pdf.set_draw_color(255, 0, 0)

    total_count = sum(count)
    pdf.set_xy(27, 248)
    pdf.cell(20, 10, str(total_count), align='C')

    pdf.set_xy(38, 98)
    pdf.cell(16, 7, str(total_count), align='C')
    pdf.cell(23, 7, "86", align='C') # revisar longitud niplo, formula para normal; 86 para conexion lateral

    pdf.set_xy(47, 248)
    pdf.set_font("helvetica", "B", 8)
    pdf.cell(36, 9, str(material), align='C')

    pdf.set_xy(151, 248)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

# Functions to create Dimensional drawings PDFs
def loose_valves_dwg_dim(num_order, material, connection_1, connection_2, exterior_size, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        connection_1 (str): The first side connection type.
        connection_2 (str): The second side connection type.
        exterior_size (str): The process size connection
        item_data (list): The list of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

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
        pdf.rect(18, 6, 187, 284, style='D')

    cnt = item_data
    

    pdf.set_draw_color(255, 0, 0)

    pdf.set_xy(44, 146)
    if cnt % 2 == 0:
        cnt = cnt / 2
        pdf.cell(28, 9, str(cnt), align='C')
        pdf.cell(28, 9, str(material), align='C')
        pdf.cell(28, 9, str(exterior_size), align='C')
        pdf.cell(28, 9, str(connection_1), align='C')
        pdf.cell(28, 9, str(connection_2), align='C')

        pdf.set_xy(53, 146)
        pdf.cell(28, 9, str(cnt), align='C')
        pdf.cell(28, 9, str(material), align='C')
        pdf.cell(28, 9, str(exterior_size), align='C')
        pdf.cell(28, 9, str(connection_2), align='C')
        pdf.cell(28, 9, str(connection_1), align='C')
    else:
        pdf.cell(28, 9, str(cnt), align='C')
        pdf.cell(28, 9, str(material), align='C')
        pdf.cell(28, 9, str(exterior_size), align='C')
        pdf.cell(28, 9, str(connection_1), align='C')
        pdf.cell(28, 9, str(connection_2), align='C')

    pdf.set_xy(27, 248)
    pdf.cell(20, 10, str(cnt), align='C')
    
    pdf.set_xy(47, 248)
    pdf.set_font("helvetica", "B", 8)
    pdf.cell(36, 9, str(material), align='C')

    pdf.set_xy(151, 248)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(49, 9, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def dwg_dim_32218_32219(num_order, material, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.

    Args:
        num_order (str): The order number.
        material (str): The material code.
        item_data (list): The list of items to be included in the PDF.
    """
    query = ('''
        SELECT colors.bg_color_1, colors.bg_color_2, colors.border_color
        FROM validation_data.material_color_code AS colors
        WHERE UPPER (colors.material) LIKE UPPER('%%'||%s||'%%')
        ''')

    try:
        with Database_Connection(config_database()) as conn:
            with conn.cursor() as cur:
                cur.execute(query,(material,))
                results_colors=cur.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        MessageHelper.show_message("Ha ocurrido el siguiente error:\n"
                    + str(error), "critical")

    first_color = results_colors[0][0]
    second_color = results_colors[0][1]
    border_color = results_colors[0][2]

    pdf = FPDF(unit='mm')
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(49, 49, 229)

    pdf.add_page()

    pdf.set_line_width(1)
    pdf.set_draw_color(*map(int, first_color.split(',')))
    pdf.rect(6, 19, 198, 270, style='D')

    pdf.set_draw_color(*map(int, second_color.split(',')))
    pdf.rect(5, 18, 200, 272, style='D')

    if border_color is not None:
        pdf.set_draw_color(*map(int, border_color.split(',')))
        pdf.rect(4, 17, 202, 274, style='D')

    item_data = list(item_data)

    cnt = item_data[0][0]

    pdf.set_draw_color(255, 0, 0)

    pdf.set_xy(33, 179)
    with pdf.rotation(270):
        pdf.cell(10, 10, str(cnt), align='C')

    pdf.set_xy(31, 260)
    with pdf.rotation(270):
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(30, 6, str(num_order), align='C')

    return io.BytesIO(pdf.output())

def dwg_dim_flange_plate(num_order: str, tag: str,
                        size: str, schedule: str, rating: str, facing: str,
                        pipe_int_diam: str, bore_diam: str, thickness: str, dv_diam: str, notes: str, tapping_size:str, aprox_weight:str,
                        o_diam: str, a_diam: str, c_flange: str, y_flange: str, x_diam: str, r_diam: str, d_diam: str, t_flange: str, n_bores: str, diam_bores: str,
                        handle_height: str, handle_width: str, plate_c_dim: str, plate_ext_diam: str,
                        rtj_thickness: str, rtj_r_type: str, rtj_p_diam: str, rtj_e_diam: str, rtj_f_diam: str,
                        engineering: str, customer: str, project: str, po_number: str,
                        flange_material: str, stud_material: str, nut_material: str, plate_material: str, gasket_material: str, gasket_qty: str,
                        plug_qty: str, plug_material: str, screw_material: str,
                        notes_flange: str, notes_stud: str, notes_nut: str, notes_plate: str, notes_gasket: str, notes_plugs: str, notes_jack_screw: str,
                        drawing_number: str, counter: int) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    query_revisions = ("""SELECT DISTINCT ON (dim_drawing_rev) dim_drawing_rev, TO_CHAR(MAX(dim_drawing_date), 'dd/mm/yyyy')
                        FROM tags_data.tags_flow
                        WHERE tag = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                        GROUP BY dim_drawing_rev
                        ORDER BY dim_drawing_rev DESC
                        LIMIT 4;""")

    query_data_prev_revision = ("""
                                SELECT tag, line_size, rating, facing, schedule,
                                pipe_int_diam, orif_diam, dv_diam, plate_thk, nace, tapping_size,
                                flange_material, bolts_material, nuts_material, element_material, gasket_material, gasket_quantity,
                                plug_quantity, plug_material, jack_screw_material, bolts_quantity,
                                notes_flange, notes_stud, notes_nuts, notes_plate,
                                notes_gasket, notes_plug, notes_jack_screw
                                FROM tags_data.tags_flow
                                WHERE tag = %s AND dim_drawing_rev = %s
                                """)

    pattern_torn = r"^(A\d+\s+Gr\.[A-Z0-9\.]+(?:\s+Cl\.\d+)?)(?:\s+(.*))?$"
    match_stud = re.match(pattern_torn, stud_material)
    match_nut = re.match(pattern_torn, nut_material)
    match_jack_screw = re.match(pattern_torn, screw_material)

    if match_stud:
        stud_material = match_stud.group(1)
        notes_stud = (match_stud.group(2) if match_stud.group(2) else '') + ((" // " + notes_stud) if notes_stud else '')

    if match_nut:
        nut_material = match_nut.group(1)
        notes_nut = (match_nut.group(2) if match_nut.group(2) else '') + ((" // " + notes_nut) if notes_nut else '')

    if match_jack_screw:
        screw_material = match_jack_screw.group(1)
        notes_jack_screw = (match_jack_screw.group(2) if match_jack_screw.group(2) else '') + ((" // " + notes_jack_screw) if notes_jack_screw else '')

# get data from previous revision to compare and mark changes in the PDF
    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_revisions, (tag, num_order,))
            results_revisions = cursor.fetchall()
            actual_revision = int(results_revisions[0][0])
            prev_revision = int(results_revisions[1][0]) if int(actual_revision) > 0 else None

            row = (None,) * 28

            if prev_revision is not None:
                cursor.execute(query_data_prev_revision, (tag, str(prev_revision),))
                row = cursor.fetchone() or (None,) * 28

            (tag_prev, size_prev, rating_prev, facing_prev, schedule_prev,
            pipe_int_diam_prev, orif_diam_prev, dv_diam_prev, thickness_prev, notes_prev, tapping_size_prev,
            flange_material_prev, bolts_material_prev, nuts_material_prev, element_material_prev, gasket_material_prev, gasket_qty_prev,
            plug_qty_prev, plug_material_prev, jack_screw_material_prev, n_bores_prev,
            notes_flange_prev, notes_stud_prev, notes_nuts_prev, notes_plate_prev,
            notes_gasket_prev, notes_plug_prev, notes_jack_screw_prev
            ) = row

    pdf = PDF()
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

# Tapping Size
    if not 'FL' in str(tapping_size):
        pdf.set_xy(183, 40)
        with pdf.rotation(270):
            pdf.cell(21, 5, str(tapping_size), align='C')
            tapping_size != tapping_size_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 198, y = 41, w = 2, h = 2)

# Equipment tag and principal dimensions
    pdf.set_xy(195, 166)
    with pdf.rotation(270):
        x_pos = pdf.get_x()
        y_pos = pdf.get_y()
        pdf.cell(21, 5, str(tag), align='C')
        pdf.cell(23, 2.5, str(size) + " " + str(rating) + " WN " + ('RTJ' if 'RTJ' in str(facing) else str(facing)), align='C')
        pdf.set_xy(x_pos + 21, y_pos + 2.5)
        pdf.cell(23, 2.5, f"{"SCH " + str(schedule)}", align='C')
        pdf.set_xy(x_pos + 21 + 23, y_pos)
        pdf.cell(11, 5, str(pipe_int_diam), align='C')
        pdf.cell(11, 5, str(bore_diam), align='C')
        pdf.cell(12, 5, str(thickness), align='C')
        pdf.cell(11, 5, str(dv_diam) if str(dv_diam) != 'None' else 'N/A', align='C')
        pdf.fixed_height_multicell(30, 5, (str(notes) if str(notes) not in  ['None', 'NO', 'N/A'] else '') +
                    ('/ISO 15156' if num_order[:8] == 'P-26/027' and str(notes) not in  ['None', 'NO', 'N/A'] else '') + 
                    ('\n' + aprox_weight if num_order[:8] == 'P-26/027' else ''), 'L')

        tag != tag_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 214, y = 168, w = 2, h = 2)
        size != size_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 237, y = 168, w = 2, h = 2)
        rating != rating_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 237, y = 168, w = 2, h = 2)
        facing != facing_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 237, y = 168, w = 2, h = 2)
        schedule != schedule_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 237, y = 168, w = 2, h = 2)
        pipe_int_diam != pipe_int_diam_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 248, y = 168, w = 2, h = 2)
        bore_diam != orif_diam_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 259, y = 168, w = 2, h = 2)
        thickness != thickness_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 261, y = 168, w = 2, h = 2)
        dv_diam != dv_diam_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 272, y = 168, w = 2, h = 2)
        notes != notes_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 283, y = 168, w = 2, h = 2)

# Flange dimensions
    pdf.set_xy(88, 23)
    with pdf.rotation(270):
        pdf.cell(9, 4, f"{size + ' / ' + rtj_r_type}" if 'RTJ' in str(facing) else f"{size}", align='C')
        pdf.cell(12, 4, str(o_diam), align='C')
        pdf.cell(12, 4, str(a_diam), align='C')
        pdf.cell(12, 4, str(c_flange), align='C')
        pdf.cell(12, 4, str(y_flange), align='C')
        pdf.cell(12, 4, str(x_diam), align='C')
        pdf.cell(12, 4, str(r_diam), align='C')
        pdf.cell(12, 4, str(d_diam), align='C')
        pdf.cell(8, 4, str(t_flange), align='C')
        pdf.cell(9, 4, str(n_bores), align='C')
        pdf.cell(14, 4, str(diam_bores), align='C')

        size != size_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 214, y = 25.5, w = 2, h = 2)

# Plate dimensions
    pdf.set_xy(19, 111)
    with pdf.rotation(270):
        pdf.cell(12, 4, f"{size + ' / ' + rtj_r_type}" if 'RTJ' in str(facing) else f"{size}", align='C')
        pdf.cell(10, 4, f"{rtj_p_diam}" if 'RTJ' in str(facing) else f"{handle_height}", align='C')
        pdf.cell(9, 4, f"{rtj_thickness}" if 'RTJ' in str(facing) else f"{handle_width}", align='C')
        pdf.cell(8, 4, f"{plate_c_dim}" if plate_c_dim != 'N/A' else '', align='C')
        pdf.cell(11, 4, f"{handle_height}" if 'RTJ' in str(facing) else f"{plate_ext_diam}", align='C')

        size != size_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 18, y = 111.5, w = 2, h = 2)

    pdf.set_xy(52, 66)
    with pdf.rotation(270):
        pdf.cell(28, 6, "SURFACE: 125-250 Ra" if facing == 'RF' else ("SURFACE: 63-125 Ra" if facing == 'RF63-125' else ''), align='C')

# Project data
    pdf.set_xy(102, 222)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{engineering}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{customer}", 'C')
        pdf.set_xy(x, y + 10)
        pdf.fixed_height_multicell(38, 9, f"{project}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 9, f"{po_number}", 'C')

# Materials and quantities
# Jack Screw data
    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(69, 215)
    with pdf.rotation(270):
        pdf.cell(23, 4, f"{screw_material}", align='C')
        screw_material != jack_screw_material_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 90, y = 217, w = 2, h = 2)
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 4, notes_jack_screw if notes_jack_screw else '', 'L')

# Plug data
    if int(plug_qty) > 0:
        pdf.set_font("Helvetica", "", 6)
        pdf.set_xy(65, 206.5)
        with pdf.rotation(270):
            y_pos = pdf.get_y()
            x_pos = pdf.get_x()
            pdf.cell(8.5, 4, f"{int(plug_qty)}", align='C')
            pdf.set_font("Helvetica", "", 5)
            plug_qty != plug_qty_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 71.5, y = 208.5, w = 2, h = 2)
            pdf.cell(23, 4, f"{plug_material}", align='C')
            plug_material != plug_material_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 94.5, y = 208.5, w = 2, h = 2)
            pdf.set_xy(x_pos + 31.5, y_pos)
            pdf.set_font("Helvetica", "", 5)
            pdf.fixed_height_multicell(55, 4, notes_plugs if notes_plugs else '', 'L')

# Gasket data
    gasket_type = 'SPIRAL GASKETS' if 'SPW' in gasket_material else ('FLAT GASKETS' if 'FLAT' in gasket_material.upper() else '')
    if 'SPW' in gasket_material:
        match = re.search(r"F:([^/)]*)", gasket_material)
        if match:
            material = match.group(1)
            gasket_main_material = ('AISI-' + material) if len(material.split('+')[0]) == 3 else material

    elif 'FLAT' in gasket_material.upper():
        gasket_main_material = 'SYNTHETIC FIBER'

    elif 'ORTJ' in gasket_material.upper():
        gasket_main_material = gasket_material.split(";")[0].replace("ORTJ Type", "").strip() + (' Galvanized' if 'GALV' in gasket_material.upper() else '')

    else:
        gasket_main_material = 'ASTM A694 F60'

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(61, 206.5)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(8.5, 5, f"{int(gasket_qty)}", align='C')
        pdf.set_font("Helvetica", "", 6) if 'ORTJ' in gasket_material.upper() else pdf.set_font("Helvetica", "", 5)
        gasket_qty != gasket_qty_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 67.5, y = 208.5, w = 2, h = 2)
        pdf.fixed_height_multicell(23, 4, f"{gasket_type + ' ' + gasket_main_material}", 'C')
        gasket_material != gasket_material_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 90.5, y = 208.5, w = 2, h = 2)
        pdf.set_xy(x_pos + 31.5, y_pos + 0.75)
        pdf.set_font("Helvetica", "", 5.5)
        pdf.fixed_height_multicell(55, 3, notes_gasket if notes_gasket else '', 'L')

# Plate data
    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(57, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.fixed_height_multicell(23, 4, f"{plate_material}", 'C')
        plate_material != element_material_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 78, y = 217, w = 2, h = 2)
        pdf.set_font("Helvetica", "", 5)
        pdf.set_xy(x_pos + 23, y_pos)
        pdf.fixed_height_multicell(55, 4, notes_plate if notes_plate else '', 'L')

# Nuts data
    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(53, 206.5)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(8.5, 5, f"{str(int(n_bores)*2)}", align='C')
        n_bores != n_bores_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 59.5, y = 208.5, w = 2, h = 2)
        pdf.fixed_height_multicell(23, 4, f"{nut_material}", 'C')
        nut_material != nuts_material_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 82.5, y = 208.5, w = 2, h = 2)
        pdf.set_font("Helvetica", "", 5)
        pdf.set_xy(x_pos + 31.5, y_pos)
        pdf.fixed_height_multicell(55, 4, notes_nut if notes_nut else '', 'L')

# Bolts data
    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(49, 206.5)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(8.5, 5, f"{str(int(n_bores))}", align='C')
        n_bores != n_bores_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 55.5, y = 208.5, w = 2, h = 2)
        pdf.fixed_height_multicell(23, 4, f"{stud_material}", 'C')
        stud_material != bolts_material_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 78.5, y = 208.5, w = 2, h = 2)
        pdf.set_font("Helvetica", "", 5)
        pdf.set_xy(x_pos + 31.5, y_pos)
        pdf.fixed_height_multicell(55, 4, notes_stud if notes_stud else '', 'L')

# Flange data
    pdf.set_font("Helvetica", "", 5)
    pdf.set_xy(44, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(23, 4, f"{flange_material}", align='C')
        flange_material != flange_material_prev and actual_revision != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(actual_revision) + ".png")), x = 65, y = 217, w = 2, h = 2)
        pdf.set_font("Helvetica", "", 5)
        pdf.set_xy(x_pos + 23, y_pos)
        pdf.fixed_height_multicell(55, 4, notes_flange if notes_flange else '', 'L')

# Drawing information
    pdf.set_font("Helvetica", "", 6)
    write_revisions_horizontal(pdf, results_revisions)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(31, 256)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order)}-{int(drawing_number.split("-")[-1]):02d}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{int(drawing_number.split("-")[-1]):02d}/{counter:02d}", align='C')

    pdf.set_font("Helvetica", "U", 10)
    pdf.set_xy(105, 50)
    with pdf.rotation(270):
        pdf.cell(28, 6, "RANGE OF SURFACE: 125-250 Ra" if facing == 'RF' else ("RANGE OF SURFACE: 63-125 Ra" if facing == 'RF63-125' else ''), align='C')

    return io.BytesIO(pdf.output())

def dwg_dim_plate(num_order: str, tag: str,
                size: str, schedule: str, rating: str, facing: str,
                pipe_int_diam: str, bore_diam: str, thickness: str, dv_diam: str, notes: str, plate_material: str,
                handle_height: str, handle_width: str, handle_thickness:str, plate_c_dim: str, plate_ext_diam: str,
                rtj_thickness: str, rtj_r_type: str, rtj_p_diam: str, rtj_e_diam: str, rtj_f_diam: str,
                engineering: str, customer: str, project: str, po_number: str,
                drawing_number: str, counter: int) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    query_revisions = ("""SELECT dim_drawing_rev, TO_CHAR(dim_drawing_date, 'dd/mm/yyyy')
                        FROM tags_data.tags_flow
                        WHERE tag = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                        ORDER BY dim_drawing_rev DESC
                        LIMIT 4;""")

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_revisions, (tag, num_order,))
            results_revisions = cursor.fetchall()

    pdf = PDF()
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    pdf.set_font("Helvetica", "", 7)
    pdf.set_xy(185, 108)
    with pdf.rotation(270):
        pdf.cell(3, 4, str(handle_thickness), align='C')

    # Tapping Size
    pdf.set_xy(196, 156)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(22, 6, str(tag), align='C')
        pdf.cell(18, 3, "", align='C')
        pdf.set_font("Helvetica", "", 5.5)
        pdf.fixed_height_multicell(20.5, 6, str(plate_material), 'C')
        pdf.set_xy(x_pos + 22 + 18 + 17.5, y_pos)
        pdf.set_font("Helvetica", "", 6)
        pdf.cell(9.5, 6, str(pipe_int_diam), align='C')
        pdf.cell(9, 6, str(bore_diam), align='C')
        pdf.cell(9, 6, str(thickness), align='C')
        pdf.cell(10.5, 6, str(dv_diam), align='C')
        pdf.cell(10, 6, "", align='C')
        pdf.fixed_height_multicell(26, 6, '' if str(notes) in ['None', 'NO', 'N/A'] else str(notes), 'L')

    pdf.set_xy(196, 178)
    with pdf.rotation(270):
        pdf.cell(18, 3, str(size) + " " + str(rating) + " " + ('RTJ' if 'RTJ' in str(facing) else str(facing)), align='C')

    pdf.set_xy(193, 178)
    with pdf.rotation(270):
        pdf.cell(18, 3, "SCH " + str(schedule), align='C')

    # Plate dimensions
    pdf.set_xy(138, 75)
    with pdf.rotation(270):
        pdf.cell(12, 4, "SURFACE: 125-250 Ra" if facing == 'RF' else ("SURFACE: 63-125 Ra" if facing == 'RF63-125' else ''), align='C')

    pdf.set_xy(52, 28.5)
    with pdf.rotation(270):
        pdf.cell(12, 4, f"{size + ' / ' + rtj_r_type}" if 'RTJ' in str(facing) else f"{size}", align='C')
        pdf.cell(10, 4, f"{rtj_p_diam}" if 'RTJ' in str(facing) else f"{handle_height}", align='C')
        pdf.cell(9, 4, f"{rtj_thickness}" if 'RTJ' in str(facing) else f"{handle_width}", align='C')
        pdf.cell(8, 4, f"{plate_c_dim}", align='C')
        pdf.cell(11, 4, f"{handle_height}" if 'RTJ' in str(facing) else f"{plate_ext_diam}", align='C')

    # Project data
    pdf.set_xy(56, 222)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{engineering}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{customer}", 'C')

    pdf.set_xy(46, 222)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{project}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{po_number}", 'C')

    # Drawing information
    pdf.set_font("Helvetica", "", 6)
    write_revisions_horizontal(pdf, results_revisions)
    # pdf.set_xy(21, 177.75)
    # with pdf.rotation(270):
    #     pdf.cell(10, 3, f"{drawing_date}", align='C')

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(33, 256)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order)}-{int(drawing_number.split("-")[-1]):02d}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{int(drawing_number.split("-")[-1]):02d}/{counter:02d}", align='C')

    return io.BytesIO(pdf.output())

def dwg_dim_ro(num_order: str, tag: str,
                    size: str, schedule: str, rating: str, facing: str, plate_material:str, weight: str,
                    pipe_int_diam: str, bore_diam: str, thickness: str, notes: str, plate_type: str,
                    handle_height: str, handle_width: str, handle_thickness: str, plate_ext_diam: str,
                    rtj_thickness: str, rtj_r_type: str, rtj_p_diam: str, rtj_e_diam: str, rtj_f_diam: str,
                    engineering: str, customer: str, project: str, po_number: str,
                    drawing_number: str, counter: int) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    query_revisions = ("""SELECT DISTINCT ON (dim_drawing_rev) dim_drawing_rev, TO_CHAR(MAX(dim_drawing_date), 'dd/mm/yyyy')
                    FROM tags_data.tags_flow
                    WHERE tag = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                    GROUP BY dim_drawing_rev
                    ORDER BY dim_drawing_rev DESC
                    LIMIT 4;""")

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_revisions, (tag, num_order,))
            results_revisions = cursor.fetchall()

    pdf = PDF()
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    # Equipment tag and principal dimensions
    if facing in ['RF', 'FF']:
        pdf.set_font("Helvetica", "", 7)
        pdf.set_xy(184, 108) # 203, 135
        with pdf.rotation(270):
            pdf.cell(3, 4, str(handle_thickness), align='C')

    # Equipment tag and principal dimensions
    pdf.set_font("Helvetica", "", 5.5)
    pdf.set_xy(195, 156)
    with pdf.rotation(270):
        x_pos = pdf.get_x()
        y_pos = pdf.get_y()
        pdf.cell(22, 5, str(tag), align='C')
        pdf.cell(17, 5, "", align='C')
        pdf.fixed_height_multicell(20, 4, f"{plate_material.replace(" +", "\n+").replace(" (", "\n(")}", 'C')
        pdf.set_xy(x_pos + 58, y_pos)
        pdf.cell(9, 5, str(pipe_int_diam), align='C')
        pdf.cell(9, 5, str(bore_diam), align='C')
        pdf.cell(9, 5, str(thickness), align='C')
        pdf.cell(20, 5, ((str(notes) + ' // ') if str(notes) not in  ['None', 'NO', 'N/A'] else ' ') + str(weight), align='L')

    pdf.set_xy(196, 178)
    with pdf.rotation(270):
        pdf.cell(18, 3, str(size) + " " + str(rating) + "# " + ('RTJ' if 'RTJ' in str(facing) else str(facing)), align='C')

    pdf.set_xy(193, 178)
    with pdf.rotation(270):
        pdf.cell(18, 3, "SCH " + str(schedule), align='C')

    # Plate dimensions
    pdf.set_xy(138, 75)
    with pdf.rotation(270):
        pdf.cell(12, 4, "SURFACE: 125-250 Ra" if facing in ['RF', 'FF'] else ("SURFACE: 63-125 Ra" if facing == 'RF63-125' else ''), align='C')

    pdf.set_xy(52, 33)
    with pdf.rotation(270):
        pdf.cell(12, 4, f"{size + ' / ' + rtj_r_type}" if 'RTJ' in str(facing) else f"{size}", align='C')
        pdf.cell(10, 4, f"{rtj_p_diam}" if 'RTJ' in str(facing) else f"{handle_height}", align='C')
        pdf.cell(9, 4, f"{rtj_thickness}" if 'RTJ' in str(facing) else f"{handle_width}", align='C')
        pdf.cell(11, 4, f"{handle_height}" if 'RTJ' in str(facing) else f"{plate_ext_diam}", align='C')

    # Project data
    pdf.set_xy(56, 222)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{engineering}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{customer}", 'C')

    pdf.set_xy(46, 222)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{project}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{po_number}", 'C')

    # Drawing information
    pdf.set_font("Helvetica", "", 6)
    write_revisions_horizontal(pdf, results_revisions)
    # pdf.set_xy(21, 177.75)
    # with pdf.rotation(270):
    #     pdf.cell(10, 3, f"{drawing_date}", align='C')

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(33, 256)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order)}-{int(drawing_number.split("-")[-1]):02d}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{int(drawing_number.split("-")[-1]):02d}/{counter:02d}", align='C')

    return io.BytesIO(pdf.output())

def dwg_dim_ms_ro(num_order: str, tag: str,
                    size: str, schedule: str, rating: str, facing: str,
                    flange_material: str, tube_material: str, plate_material: str,
                    pipe_int_diam: str, notes: str,
                    stages_number: str, approx_length: str, approx_weight: str,
                    rtj_thickness: str, rtj_r_type: str, rtj_p_diam: str, rtj_e_diam: str, rtj_f_diam: str,
                    engineering: str, customer: str, project: str, po_number: str,
                    drawing_number: str, counter: int) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    query_revisions = ("""SELECT dim_drawing_rev, TO_CHAR(dim_drawing_date, 'dd/mm/yyyy')
                        FROM tags_data.tags_flow
                        WHERE tag = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                        ORDER BY dim_drawing_rev DESC
                        LIMIT 4;""")

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_revisions, (tag, num_order,))
            results_revisions = cursor.fetchall()

    pdf = PDF()
    pdf.set_font("Helvetica", "", 5.5)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    # Equipment tag and principal dimensions
    pdf.set_xy(195, 156)
    with pdf.rotation(270):
        pdf.cell(22, 5, str(tag), align='C')
        pdf.cell(18, 5, "", align='C')
        pdf.cell(18, 5, str(stages_number), align='C')
        pdf.cell(9, 5, str(pipe_int_diam), align='C')
        pdf.cell(18, 5, str(approx_length), align='C')
        pdf.cell(11, 5, str(approx_weight) if str(approx_weight) not in ['None', 'NO', 'N/A'] else '' + 
                        " / " if (str(approx_weight) not in ['None', 'NO', 'N/A'] and str(notes) not in ['None', 'NO', 'N/A']) else '' + 
                        (str(notes) if str(notes) not in ['None', 'NO', 'N/A'] else ''), align='C')

    pdf.set_xy(195, 178)
    with pdf.rotation(270):
        pdf.cell(18, 3, str(size) + " " + str(rating) + " WN " + str(facing), align='C')
    
    pdf.set_xy(193, 178)
    with pdf.rotation(270):
        pdf.cell(18, 3, "SCH " + str(schedule), align='C')

    # Equipment data
    pdf.set_xy(58, 206)
    with pdf.rotation(270):
        pdf.cell(9, 5, str(stages_number), align='C')
        pdf.cell(22, 5, '', align='C')
        pdf.fixed_height_multicell(26, 5, str(plate_material), 'C')
    
    pdf.set_xy(53, 206)
    with pdf.rotation(270):
        pdf.cell(9, 5, str(int(stages_number) - 1), align='C')
        pdf.cell(22, 5, str(size) + " SCH " + str(schedule), align='C')
        pdf.cell(26, 5, str(tube_material), align='C')

    pdf.set_xy(48, 215)
    with pdf.rotation(270):
        pdf.cell(22, 5, str(size) + " " + str(rating) + " WN " + str(facing), align='C')
        pdf.cell(26, 5, str(flange_material), align='C')

    # Project data
    pdf.set_xy(78, 222)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{engineering}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{customer}", 'C')

    pdf.set_xy(68, 222)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{project}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{po_number}", 'C')

    # Drawing information
    pdf.set_font("Helvetica", "", 5.5)
    write_revisions_horizontal(pdf, results_revisions)
    # pdf.set_xy(21, 177.75)
    # with pdf.rotation(270):
    #     pdf.cell(10, 3, f"{drawing_date}", align='C')

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(33, 256)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order)}-{int(drawing_number.split("-")[-1]):02d}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{int(drawing_number.split("-")[-1]):02d}/{counter:02d}", align='C')

    return io.BytesIO(pdf.output())

def dwg_dim_mrun(num_order: str, tag: str,
                    size: str, schedule: str, rating: str, facing: str,
                    pipe_int_diam: str, bore_diam: str, notes: str, tapping_size: str, flange_type: str,
                    weight: str, length: str, tube_material: str,
                    handle_height: str, handle_width: str, plate_c_dim: str, plate_ext_diam: str,
                    rtj_thickness: str, rtj_r_type: str, rtj_p_diam: str, rtj_e_diam: str, rtj_f_diam: str, tapping_number: str,
                    engineering: str, customer: str, project: str, po_number: str,
                    flange_material: str, stud_material: str, nut_material: str, plate_material: str, gasket_material: str, plug_qty: str, plug_material: str, screw_material: str,
                    notes_flange: str, notes_stud: str, notes_nut: str, notes_plate: str, notes_gasket: str, notes_plugs: str, notes_jack_screw: str,
                    drawing_number: str, counter: int) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    query_revisions = ("""SELECT dim_drawing_rev, TO_CHAR(dim_drawing_date, 'dd/mm/yyyy')
                        FROM tags_data.tags_flow
                        WHERE tag = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                        ORDER BY dim_drawing_rev DESC
                        LIMIT 4;""")

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_revisions, (tag, num_order,))
            results_revisions = cursor.fetchall()

    pdf = PDF()
    pdf.add_font('DejaVuSansCondensed', '', str(get_path("Resources", "Iconos", "DejaVuSansCondensed.ttf")))
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    size_orifice_flange = str(size).split('"/')[1] if '"/' in str(size) else size
    rating_orifice_flange = str(rating).split('/')[1] if '/' in str(rating) else rating
    type_orifice_flange = str(flange_type).split('/')[1] if '/' in str(flange_type) else flange_type

    size_line_flange = str(size).split('"/', 1)[0] + '"' if '"/' in str(size) else size
    rating_line_flange = str(rating).split('/')[0]
    type_line_flange = str(flange_type).split('/')[0]

    query_mrun_lengths = ("""
                            SELECT length_1, length_2
                            FROM validation_data.mrun_lengths
                            WHERE connection = %s   
                            """)

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cur:
            cur.execute(query_mrun_lengths, (size,))
            results_lengths = cur.fetchall()
            length_1 = results_lengths[0][0]
            length_2 = results_lengths[0][1]

    # Equipment tag and principal dimensions
    pdf.set_font('DejaVuSansCondensed','', size=6)
    pdf.set_xy(191.25, 151)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(29, 4, str(tag), align='C')
        pdf.cell(8, 4,  str(length_1), align='C')
        pdf.cell(9, 4, str(length_2), align='C')
        pdf.cell(8, 4, str(length), align='C')
        pdf.cell(9, 4, str(pipe_int_diam), align='C')
        pdf.cell(21, 2, str(size_orifice_flange) + " " + str(rating_orifice_flange) + "# " + str(type_orifice_flange) + " " + str(facing), align='C')
        pdf.set_xy(x_pos + 63, y_pos + 2)
        pdf.cell(21, 2, f"SCH {schedule}", align='C')
        pdf.set_xy(x_pos + 63 + 21, y_pos)
        pdf.cell(21, 2, str(size_line_flange) + " " + str(rating_line_flange) + "# " + str(type_line_flange) + " " + str(facing), align='C')
        pdf.set_xy(x_pos + 63 + 21, y_pos + 2)
        pdf.cell(21, 2, f"SCH {schedule}", align='C')
        pdf.set_xy(x_pos + 63 + 21 + 21, y_pos)
        pdf.cell(10, 4, str(bore_diam), align='C')
        pdf.fixed_height_multicell(20, 4, f"{weight + ' ' + ('NACE' if str(notes) not in ['None', 'NO', 'N/A'] else '')}", 'C')

    pdf.set_xy(51, 67)
    with pdf.rotation(270):
        pdf.cell(12, 4, "SURFACE: 125-250 Ra" if facing == 'RF' else ("SURFACE: 63-125 Ra" if facing == 'RF63-125' else ''), align='C')

    pdf.set_xy(20, 111)
    with pdf.rotation(270):
        pdf.cell(12, 4, f"{size + ' / ' + rtj_r_type}" if str(facing) == 'RTJ' else f"{size}", align='C')
        pdf.cell(10.5, 4, f"{rtj_p_diam}" if str(facing) == 'RTJ' else f"{handle_height}", align='C')
        pdf.cell(9, 4, f"{rtj_thickness}" if str(facing) == 'RTJ' else f"{handle_width}", align='C')
        pdf.cell(8, 4, f"{plate_c_dim}", align='C')
        pdf.cell(11, 4, f"{handle_height}" if str(facing) == 'RTJ' else f"{plate_ext_diam}", align='C')

    # Project data
    pdf.set_xy(118, 222)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{engineering}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{customer}", 'C')

    pdf.set_xy(108, 222)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{project}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{po_number}", 'C')

    # Materials and quantities
    if int(tapping_number) < 4:
        pdf.set_font("Helvetica", "", 6)
        pdf.set_xy(97, 237)
        with pdf.rotation(270):
            y_pos = pdf.get_y()
            x_pos = pdf.get_x()
            pdf.set_font("Helvetica", "", 5)
            pdf.fixed_height_multicell(23.5, 5, screw_material if screw_material else '', 'C')
            pdf.set_xy(x_pos + 23.5, y_pos)
            pdf.fixed_height_multicell(22, 5, notes_jack_screw if notes_jack_screw else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(92.25, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(23, 2.5, str(size_line_flange) + " " + str(rating_line_flange) + "# " + str(type_line_flange) + " " + str(facing), align='C')
        pdf.set_xy(x_pos, y_pos + 2.5)
        pdf.cell(23, 2.5, f"SCH {schedule}", align='C')
        pdf.set_xy(x_pos + 23, y_pos)
        pdf.cell(22, 5, f"{flange_material}", align='C')
        pdf.fixed_height_multicell(55, 5, 'REDUCING FLANGE' if size_line_flange != size_orifice_flange else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(87, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(23, 5, str(size_orifice_flange) + " SCH " + str(schedule), align='C')
        pdf.cell(22, 5, f"{tube_material}", align='C')

    gasket_type = 'SPIRAL GASKETS' if 'SPW' in gasket_material else ('FLAT GASKETS' if 'FLAT' in gasket_material.upper() else '')

    if 'SPW' in gasket_material:
        match = re.search(r'F:([^/)]*)', gasket_material)
        gasket_main_material = match.group(1) if match else ''
        gasket_main_material = (
            '316L+GRAPHITE'
            if gasket_main_material == '316+GRAPHITE'
            else gasket_main_material
        )
    elif 'FLAT' in gasket_material.upper():
        gasket_main_material = 'SYNTHETIC FIBER'
    else:
        gasket_main_material = ''

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(82.5, 238)
    with pdf.rotation(270):
        x_pos = pdf.get_x()
        y_pos = pdf.get_y()
        pdf.fixed_height_multicell(23, 5, f"{gasket_type + ' ' + gasket_main_material}", 'C')
        pdf.set_xy(x_pos + 22.5, y_pos)
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(40, 4, notes_gasket if notes_gasket else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(77, 206)
    with pdf.rotation(270):
        pdf.cell(9, 5, f"{plug_qty}", align='C')
        pdf.cell(23, 5, "", align='C')
        pdf.cell(22.5, 5, f"{plug_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 5, notes_plugs if notes_plugs else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(72, 238)
    with pdf.rotation(270):
        pdf.cell(23, 5, f"{plate_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 5, notes_plate if notes_plate else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(67.5, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(23, 2.5, str(size_orifice_flange) + " " + str(rating_orifice_flange) + "# " + str(type_orifice_flange) + " " + str(facing), align='C')
        pdf.set_xy(x_pos, y_pos + 2.5)
        pdf.cell(23, 2.5, f"SCH {schedule}", align='C')
        pdf.set_xy(x_pos + 23, y_pos)
        pdf.cell(22, 5, f"{flange_material}", align='C')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(62, 237)
    with pdf.rotation(270):
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(23.5, 5, f"{nut_material}", 'C')
        pdf.set_xy(x_pos + 23.5, y_pos)
        pdf.fixed_height_multicell(55, 5, notes_nut if notes_nut else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(57, 237)
    with pdf.rotation(270):
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(23.5, 5, f"{stud_material}", 'C')
        pdf.set_xy(x_pos + 23.5, y_pos)
        pdf.fixed_height_multicell(55, 5, notes_stud if notes_stud else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(52.25, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(23, 5, str(size_orifice_flange) + " SCH " + str(schedule), align='C')
        pdf.cell(22, 5, f"{tube_material}", align='C')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(47.75, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(23, 2.5, str(size_line_flange) + " " + str(rating_line_flange) + "# " + str(type_line_flange) + " " + str(facing), align='C')
        pdf.set_xy(x_pos, y_pos + 2.5)
        pdf.cell(23, 2.5, f"SCH {schedule}", align='C')
        pdf.set_xy(x_pos + 23, y_pos)
        pdf.cell(22, 5, f"{flange_material}", align='C')
        pdf.fixed_height_multicell(55, 5, 'REDUCING FLANGE' if size_line_flange != size_orifice_flange else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    # Drawing information
    write_revisions_horizontal(pdf, results_revisions)
    # pdf.set_xy(21, 177.75)
    # with pdf.rotation(270):
    #     pdf.cell(10, 3, f"{drawing_date}", align='C')

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(31, 256)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order)}-{int(drawing_number.split("-")[-1]):02d}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{int(drawing_number.split("-")[-1]):02d}/{counter:02d}", align='C')

    return io.BytesIO(pdf.output())

def dwg_dim_venturi(num_order: str, item_type: str, tag: str,
                        size: str, schedule: str, rating: str, facing: str,
                        pipe_int_diam: str, bore_diam: str, notes: str, tapping_size: str, tapping_number: str,
                        weight: str, length: str, tube_material: str, cones_material: str,
                        a_venturi: str, d_venturi: str, e_venturi: str, f_venturi: str, g_venturi: str, c_venturi: str, h_venturi: str, t_venturi: str,
                        engineering: str, customer: str, project: str, po_number: str,
                        flange_material: str, venturi_material: str, plug_qty: str, plug_material: str,
                        notes_flange: str, notes_plate: str, notes_plugs: str, notes_jack_screw: str, notes_presure_taps: str, offer_notes: str,
                        drawing_number: str, counter: int) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    query_revisions = ("""SELECT dim_drawing_rev, TO_CHAR(dim_drawing_date, 'dd/mm/yyyy')
                        FROM tags_data.tags_flow
                        WHERE tag = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                        ORDER BY dim_drawing_rev DESC
                        LIMIT 4;""")

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_revisions, (tag, num_order,))
            results_revisions = cursor.fetchall()

    pdf = PDF()
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    # with pdf.rotation(angle=-90, x=52, y=45):
    #     pdf.image(str(get_path("Resources", "Iconos", "Logo Nobg.ico")), x = 52, y = 45, w = 40, h = 30)

    # Equipment tag and principal dimensions
    pdf.set_xy(195.5, 154.5)
    with pdf.rotation(270):
        pdf.cell(20.5, 6, str(tag), align='C')
        pdf.cell(20, 6, "", align='C')
        pdf.cell(10, 6, str(bore_diam), align='C')
        pdf.cell(10, 6, str(pipe_int_diam), align='C')
        pdf.cell(10, 6, str(d_venturi), align='C')
        pdf.cell(10, 6, str(e_venturi), align='C')
        pdf.cell(9.5, 6, str(f_venturi), align='C')
        pdf.cell(10, 6, str(g_venturi), align='C')
        pdf.cell(10, 6, str(c_venturi), align='C')
        pdf.cell(9.5, 6, str(h_venturi), align='C')
        pdf.cell(9.5, 6, str(length), align='C')
        pdf.cell(8.5, 6, str(t_venturi), align='C')

    pdf.set_xy(195.5, 174.5)
    with pdf.rotation(270):
        pdf.cell(20, 3, str(size) + " " + str(rating) + "# WN" + str(facing), align='C')
    
    pdf.set_xy(192.5, 174.5)
    with pdf.rotation(270):
        pdf.cell(20, 3, "SCH " + str(schedule), align='C')

    # Taps size
    pdf.set_xy(84, 49)
    with pdf.rotation(270):
        pdf.cell(10, 4, f"{tapping_size}", align='C')

    pdf.set_xy(57, 49)
    with pdf.rotation(270):
        pdf.cell(10, 4, f"{notes_jack_screw}", align='C')

    # Project data
    pdf.set_xy(93, 222)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{engineering}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{customer}", 'C')

    pdf.set_xy(83, 222)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{project}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{po_number}", 'C')

    # Materials and quantities
    if item_type in ["VWW", "VFW", "VFM"] or (item_type in ["VFC"] and str(offer_notes).upper() == 'CHAPA'):
        pdf.set_font("Helvetica", "", 6)
        pdf.set_xy(72, 238)
        with pdf.rotation(270):
            pdf.cell(22, 4, f"{cones_material}", align='C')
            pdf.set_font("Helvetica", "", 4)

        pdf.set_font("Helvetica", "", 6)
        pdf.set_xy(68, 238)
        with pdf.rotation(270):
            pdf.cell(22, 4, f"{venturi_material}", align='C')
            pdf.set_font("Helvetica", "", 5)
            pdf.fixed_height_multicell(55, 4, notes_plate if notes_plate else '', 'L')

        pdf.set_font("Helvetica", "", 6)
        pdf.set_xy(64, 238)
        with pdf.rotation(270):
            pdf.cell(22, 4, f"{cones_material}", align='C')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(60, 215)
    with pdf.rotation(270):
        if item_type in ["VWW", "VFW", "VFM"] or (item_type in ["VFC"] and str(offer_notes).upper() == 'CHAPA'):
            pdf.cell(23, 4, str(size) + " SCH " + str(schedule), align='C')
        else:
            pdf.cell(23, 4, "", align='C')
        pdf.cell(22, 4, f"{venturi_material}" if item_type in ["VFM", "VWM"] else f"{tube_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 4, notes_plate if notes_plate else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(55, 206.5)
    with pdf.rotation(270):
        pdf.cell(8.5, 4, f"{plug_qty}", align='C')
        pdf.cell(23, 4, str(tapping_size).replace('F',''), align='C')
        pdf.cell(22, 4, f"{plug_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 4, notes_plugs if notes_plugs else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(51, 206.5)
    with pdf.rotation(270):
        pdf.cell(8.5, 4, f"{tapping_number}", align='C')
        pdf.cell(23, 4, f"{tapping_size}", align='C')
        pdf.cell(22, 4, f"{flange_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        rating_tapping = "3000#" if str(rating) in ["150#", "300#", "600#"] else "6000#"
        pdf.fixed_height_multicell(55, 4,  rating_tapping + ((" // " + notes_presure_taps) if notes_presure_taps else ''), 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(47, 206.5)
    with pdf.rotation(270):
        pdf.cell(8.5, 4, '2' if item_type in ["VFM", "VFW", "VFC"] else '0', align='C')
        pdf.cell(23, 4, "", align='C')
        pdf.cell(22, 4, f"{flange_material}" if item_type in ["VFM", "VFW", "VFC"] else '', align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 4, notes_flange if notes_flange else '', 'L')

    # Drawing information
    pdf.set_font("Helvetica", "", 6)
    write_revisions_horizontal(pdf, results_revisions)
    # pdf.set_xy(21, 177.75)
    # with pdf.rotation(270):
    #     pdf.cell(10, 3, f"{drawing_date}", align='C')

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(31, 256)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order)}-{int(drawing_number.split("-")[-1]):02d}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{int(drawing_number.split("-")[-1]):02d}/{counter:02d}", align='C')

    return io.BytesIO(pdf.output())

def dwg_dim_nozzle(num_order: str, item_type: str, tag: str,
                        size: str, schedule: str, rating: str, facing: str,
                        pipe_int_diam: str, bore_diam: str, notes: str, tapping_size: str, tapping_number: str,
                        dim_a: str, dim_d: str, dim_f: str, dim_e: str, length: str, 
                        weight: str, tube_material: str,
                        engineering: str, customer: str, project: str, po_number: str,
                        flange_material: str, nozzle_material: str, plug_qty: str, plug_material: str,
                        notes_flange: str, notes_plate: str, notes_plugs: str,
                        drawing_number: str, counter: int) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    query_revisions = ("""SELECT dim_drawing_rev, TO_CHAR(dim_drawing_date, 'dd/mm/yyyy')
                        FROM tags_data.tags_flow
                        WHERE tag = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                        ORDER BY dim_drawing_rev DESC
                        LIMIT 4;""")

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_revisions, (tag, num_order,))
            results_revisions = cursor.fetchall()

    pdf = PDF()
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    # with pdf.rotation(angle=-90, x=52, y=45):
    #     pdf.image(str(get_path("Resources", "Iconos", "Logo Nobg.ico")), x = 52, y = 45, w = 40, h = 30)

    # Equipment tag and principal dimensions
    pdf.set_xy(195, 156)
    with pdf.rotation(270):
        pdf.cell(22, 5, str(tag), align='C')
        pdf.cell(18, 5, "", align='C')
        pdf.cell(10, 5, str(pipe_int_diam), align='C')
        pdf.cell(10, 5, str(bore_diam), align='C')
        pdf.cell(10, 5, str(dim_a), align='C')
        pdf.cell(10, 5, str(dim_d), align='C')
        pdf.cell(9, 5, str(dim_f), align='C')
        pdf.cell(10, 5, str(dim_e), align='C')
        pdf.cell(10, 5, str(length), align='C')
        pdf.fixed_height_multicell(26, 5, f"{weight + '\n' + ('NACE' if str(notes) not in ['None', 'NO', 'N/A'] else '')}", 'C')

    pdf.set_xy(195, 178)
    with pdf.rotation(270):
        pdf.cell(18, 3, str(size) + " " + str(rating) + " " + str(facing), align='C')
    
    pdf.set_xy(192, 178)
    with pdf.rotation(270):
        pdf.cell(18, 3, "SCH " + str(schedule), align='C')

    # Project data
    pdf.set_xy(98, 222)
    with pdf.rotation(270):
        pdf.cell(38, 5, f"{engineering}", align='C')
        pdf.cell(31, 5, f"{customer}", align='C')

    pdf.set_xy(88, 222)
    with pdf.rotation(270):
        pdf.cell(38, 9, f"{project}", align='C')
        pdf.cell(31, 9, f"{po_number}", align='C')

    # Materials and quantities
    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(72, 238)
    with pdf.rotation(270):
        pdf.cell(22, 4, f"{nozzle_material}", align='C') # pin
        pdf.set_font("Helvetica", "", 4)

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(68, 238)
    with pdf.rotation(270):
        pdf.cell(22, 4, f"{nozzle_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 4, notes_plate if notes_plate else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(64, 238)
    with pdf.rotation(270):
        pdf.cell(22, 4, f"{nozzle_material}", align='C') # backing

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(60, 206.5)
    with pdf.rotation(270):
        pdf.cell(8.5, 4, f"{plug_qty}", align='C')
        pdf.cell(23, 4, f"{plug_material}", align='C')
        pdf.cell(22, 4, f"{plug_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 4, notes_plugs if notes_plugs else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(54.5, 206.5)
    with pdf.rotation(270):
        pdf.cell(8.5, 4, f"{tapping_number}", align='C')
        pdf.cell(23, 4, f"{tapping_size}", align='C')
        pdf.set_font("Helvetica", "", 5)
        # pdf.fixed_height_multicell(55, 4, notes_stud if notes_stud else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(51, 215)
    with pdf.rotation(270):
        pdf.cell(23, 4, "", align='C')
        pdf.cell(22, 4, f"{tube_material}", align='C')
        pdf.set_font("Helvetica", "", 5)

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(47, 206.5)
    with pdf.rotation(270):
        pdf.cell(8.5, 4, '2' if item_type in ["VFM", "VFW"] else '0', align='C')
        pdf.cell(23, 4, "", align='C')
        pdf.cell(22, 4, f"{flange_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 4, notes_flange if notes_flange else '', 'L')

    # Drawing information
    pdf.set_font("Helvetica", "", 6)
    write_revisions_horizontal(pdf, results_revisions)
    # pdf.set_xy(21, 177.75)
    # with pdf.rotation(270):
    #     pdf.cell(10, 3, f"{drawing_date}", align='C')

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(31, 256)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order)}-{int(drawing_number.split("-")[-1]):02d}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{int(drawing_number.split("-")[-1]):02d}/{counter:02d}", align='C')

    return io.BytesIO(pdf.output())



def dwg_dim_thermowell(num_order: str, item_type: str, tag: str,
                    ins_length: str, std_length: str, sensor_element: str, wire_size: str, sheath_stem_diam: str, sheath_stem_material: str, nace: str,
                    root_diam: str, tip_diam: str, bore_diam: str, tip_thk: str, radius_dim: str,
                    engineering: str, customer: str, project: str, po_number: str,
                    insulation: str, elec_conn_case_diam: str, head_case_material: str, head_certification: str, nipple_ext_material: str, plug: str,
                    tw_type: str, size: str, rating: str, facing: str, material_tw: str,
                    drawing_number: str, counter: int) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    query_revisions = ("""SELECT dim_drawing_rev, TO_CHAR(dim_drawing_date, 'dd/mm/yyyy')
                    FROM tags_data.tags_temp
                    WHERE tag = %s AND num_order = %s AND tag_state in ('PURCHASED', 'SUPERADO')
                    ORDER BY dim_drawing_rev DESC
                    LIMIT 4;""")

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_revisions, (tag, num_order,))
            results_revisions = cursor.fetchall()

    query_element_material = ("SELECT materials FROM validation_data.temp_sensor_element WHERE sensor_element = %s")
    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cur:
            cur.execute(query_element_material, (sensor_element,))
            results = cur.fetchall()
            sensor_element_material = results[0][0]

    pdf = PDF()
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    # tag data
    pdf.set_xy(191, 166)
    with pdf.rotation(270):
        pdf.cell(25, 5, f"{tag}", align='C')
        pdf.cell(9, 5, f"{ins_length}", align='C')
        pdf.cell(9, 5, f"{std_length}", align='C')
        pdf.cell(9, 5, f"{sensor_element[-1] if 'T/C' in sensor_element else 'PT100'}" if sensor_element != 'N/A' else ('-' if item_type != 'TW' else ''), align='C')
        pdf.cell(8, 5, f"{wire_size if wire_size != 'N/A' else ('-' if item_type != 'TW' else '')}", align='C')
        pdf.cell(13, 5, f"{'S' if 'Single' in sensor_element else 'D'}" if sensor_element != 'N/A' else ('-' if item_type != 'TW' else ''), align='C')
        pdf.cell(5, 5, f"{sheath_stem_diam if sheath_stem_diam != 'N/A' else ('-' if item_type != 'TW' else '')}", align='C')
        pdf.cell(19, 5, f"{sheath_stem_material if sheath_stem_material != 'N/A' else ('-' if item_type != 'TW' else '')}", align='C')
        pdf.cell(30, 5, f"{nace}" if str(nace) not in ['NO', 'N/A', '', 'None'] else '', align='C')

    if item_type != 'TW':
        pdf.set_xy(191, 120)
        with pdf.rotation(270):
            pdf.cell(10, 3, f"{elec_conn_case_diam.split('x')[1]}", align='C')

    # dimensions data
    pdf.set_font("Helvetica", "", 8)
    pdf.set_xy(90, 102.5)
    with pdf.rotation(270):
        pdf.cell(5, 3, f"{radius_dim}" if radius_dim != 'N/A' else '', align='C')

    pdf.set_xy(81, 78)
    with pdf.rotation(270):
        pdf.cell(5, 3, f"{root_diam}" if root_diam != 'N/A' else '', align='C')

    pdf.set_xy(36, 79)
    with pdf.rotation(270):
        pdf.cell(5, 3, f"{bore_diam}" if bore_diam != 'N/A' else '', align='C')

    pdf.set_xy(18.5, 72.5)
    with pdf.rotation(270):
        pdf.cell(5, 3, f"{tip_thk}" if tip_thk != 'N/A' else '', align='C')

    pdf.set_xy(13, 100)
    with pdf.rotation(270):
        pdf.cell(5, 3, f"{tip_diam}" if tip_diam != 'N/A' else '', align='C')

    # materials data
    pdf.set_font("Helvetica", "", 6)
    if item_type != 'TW':
        pdf.set_xy(77, 215)
        with pdf.rotation(270):
            x_pos = pdf.get_x()
            y_pos = pdf.get_y()
            pdf.fixed_height_multicell(23, 4, ('THERMOCOUPLE TYPE ' + sensor_element[-1]) if 'T/C' in sensor_element else 'PT-100 ' + ('SIMPLE' if 'Single' in sensor_element else 'DOUBLE'), 'C')
            pdf.set_xy(x_pos + 23, y_pos)
            pdf.cell(22, 4, f"{sensor_element_material}", align='C')
            pdf.fixed_height_multicell(25, 4, ((insulation + " / ") if (insulation != 'N/A' and 'PT100' not in sensor_element) else "") +  ('2' if 'T/C Single' in sensor_element else ('4' if 'T/C Double' in sensor_element else sensor_element.split('(')[1].split()[0])) + " wires\nMgO Mineral Sheath", 'L')

        pdf.set_xy(73, 215)
        with pdf.rotation(270):
            pdf.cell(23, 4, f"{tw_type}", align='C')
            pdf.cell(22, 4, f"{material_tw}", align='C')

        pdf.set_xy(68, 215)
        with pdf.rotation(270):
            pdf.cell(23, 4, f"{size} {rating if '0' not in rating else (rating + '#')} {facing if facing != 'N/A' else ''}", align='C')
            pdf.cell(22, 4, f"{material_tw}", align='C')
            pdf.fixed_height_multicell(30, 5, "B16.5 BLIND FLANGE\nRAISED FACE 125÷250 Ra" if facing == 'RF' else ("B16.5 BLIND FLANGE" if facing == 'FF' else ("B16.5 BLIND FLANGE\nRAISED FACE 63 Ra" if facing == 'RTJ' else '')), 'L')

        pdf.set_xy(63, 215)
        with pdf.rotation(270):
            pdf.cell(23, 4, f"{re.search(r'(\d+/\d+")\s*\((.*?)\)', nipple_ext_material).group(1)}NPT", align='C')
            pdf.cell(22, 4, 'A-106' if re.search(r'(\d+/\d+")\s*\((.*?)\)', nipple_ext_material).group(2) == 'CS' else 'SS 316/316L', align='C')

        pdf.set_xy(58, 215)
        with pdf.rotation(270):
            pdf.cell(23, 4, f"{re.search(r'(\d+/\d+")\s*\((.*?)\)', nipple_ext_material).group(1)}NPT x {re.search(r'(\d+/\d+")\s*\((.*?)\)', nipple_ext_material).group(1)}NPT", align='C')
            pdf.cell(22, 4, 'A-105' if re.search(r'(\d+/\d+")\s*\((.*?)\)', nipple_ext_material).group(2) == 'CS' else 'SS 316/316L', align='C')

        pdf.set_xy(47.5, 215)
        with pdf.rotation(270):
            x_pos = pdf.get_x()
            y_pos = pdf.get_y()
            pdf.cell(23, 4, f"{elec_conn_case_diam}", align='C')
            pdf.fixed_height_multicell(22, 4, 'CAST ALUMINUM EPOXY COATED' if 'AL' in head_case_material else ('CARBON STEEL' if 'CS' in head_case_material else head_case_material), 'C')
            pdf.set_xy(x_pos + 23 + 22, y_pos)
            pdf.set_font("Helvetica", "", 5.5)
            pdf.fixed_height_multicell(31, 4, f"{head_certification}" if head_certification != 'N/A' else '', 'L')

    else:
        pdf.set_xy(58, 215)
        with pdf.rotation(270):
            pdf.cell(23, 4, f"{plug.split(" ")[0]} {plug.split(" ")[1]}" if plug is not None and plug not in ['N/A', ""] else "", align='C')
            pdf.cell(22, 4, "STAINLESS STEEL", align='C')

        pdf.set_xy(53, 215)
        with pdf.rotation(270):
            pdf.cell(23, 4, f"{tw_type}", align='C')
            pdf.cell(22, 4, f"{material_tw}", align='C')

        pdf.set_xy(47.75, 215)
        with pdf.rotation(270):
            pdf.cell(23, 4, f"{size} {rating if '0' not in rating else (rating + '#')} {facing if facing != 'N/A' else ''}", align='C')
            pdf.cell(22, 4, f"{material_tw}", align='C')
            pdf.fixed_height_multicell(30, 5, "B16.5 BLIND FLANGE\nRAISED FACE 125÷250 Ra" if facing == 'RF' else ("B16.5 BLIND FLANGE" if facing == 'FF' else ("B16.5 BLIND FLANGE\nRAISED FACE 63 Ra" if facing == 'RTJ' else '')), 'L')

    # Project data
    pdf.set_xy(113, 224)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 5, f"{engineering}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 5, f"{customer}", 'C')

    pdf.set_xy(103, 224)
    with pdf.rotation(270):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(38, 9, f"{project}", 'C')
        pdf.set_xy(x + 38, y)
        pdf.fixed_height_multicell(31, 9, f"{po_number}", 'C')

    # Drawing information
    write_revisions_horizontal(pdf, results_revisions)
    # pdf.set_xy(21, 177.75)
    # with pdf.rotation(270):
    #     pdf.cell(10, 3, f"{drawing_date}", align='C')

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(31, 256)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order)}-{int(drawing_number.split("-")[-1]):02d}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{int(drawing_number.split("-")[-1]):02d}/{counter:02d}", align='C')

    return io.BytesIO(pdf.output())



def dwg_dim_glass_level(num_order: str, tag: str, item_type: str,
                    model_num: str, visibility: str, centers_length: str, body_length: str,
                    proc_conn_type: str, proc_conn_size: str, proc_conn_rating: str, proc_conn_facing: str, proc_conn_material: str, nace: str,
                    body_material: str, cover_material: str, gasket_material: str, nuts_material: str, bolts_material: str,
                    nipple_hex: str, nipple_hex_material: str, valve_type: str, valve_conn: str, valve_material: str,
                    dv_conn: str, dv_size: str, dv_rating: str, dv_facing: str, dv_material: str,
                    nipple_tub: str, nipple_tub_material: str, illuminator: str, illuminator_conn: str,
                    engineering: str, customer: str, project: str, po_number: str,
                    drawing_number: str, counter: int) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    query_revisions = ("""SELECT dim_drawing_rev, TO_CHAR(dim_drawing_date, 'dd/mm/yyyy')
                        FROM tags_data.tags_level
                        WHERE tag = %s AND num_order = %s AND tag_state = 'PURCHASED'
                        ORDER BY dim_drawing_rev DESC
                        LIMIT 4;""")

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_revisions, (tag, num_order,))
            results_revisions = cursor.fetchall()

    query_studs_qty = ("SELECT quantity_torn FROM validation_data.level_torn WHERE code_torn = %s")
    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cur:
            cur.execute(query_studs_qty, (model_num[2:],))
            results = cur.fetchall()
            studs_qty = results[0][0]

    pdf = PDF()
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    final_model = model_num
    body_model = model_num[-4:]

    if illuminator == 'YES':
        final_model += "I"

    if 'MICA' in gasket_material:
        final_model += "M"

    # tag data
    pdf.set_xy(196, 166)
    with pdf.rotation(270):
        pdf.cell(22, 5, f"{tag}", align='C')
        pdf.cell(18, 5, f"{final_model}", align='C')
        pdf.cell(7.5, 5, f"{centers_length}", align='C')
        pdf.cell(7.5, 5, f"{body_length}", align='C')
        pdf.cell(7.5, 5, f"{visibility}", align='C')
        pdf.cell(17.5, 5, f"{proc_conn_size} {proc_conn_rating}# {proc_conn_facing}" if proc_conn_type == 'FLANGED' else f"{proc_conn_size} {proc_conn_rating}", align='C')
        pdf.cell(19, 5, f"{nace}", align='C')

    # materials and dimensions data
    pdf.set_font("Helvetica", "", 6)
    if illuminator == 'YES':
        if 'PLUG' in dv_conn:
            pdf.set_xy(97, 215)
        else:
            pdf.set_xy(107, 215)
        with pdf.rotation(270):
            pdf.cell(23, 2, f"{illuminator_conn}", align='C')

    pdf.set_font("Helvetica", "", 7)
    if 'PLUG' in dv_conn:
        pdf.set_xy(92.5, 215)
        with pdf.rotation(270):
            pdf.cell(23, 5, f"{dv_size} {dv_rating}", align='C')
            pdf.cell(22, 5, f"{dv_material}", align='C')
    else:
        pdf.set_xy(102.5, 215)
        with pdf.rotation(270):
            pdf.cell(23, 5, f"{dv_size} {dv_rating}", align='C')
            pdf.cell(22, 5, f"{dv_material}", align='C')

        pdf.set_xy(97.5, 215)
        with pdf.rotation(270):
            pdf.cell(23, 5, f"{dv_size} {dv_rating}", align='C')
            pdf.cell(22, 5, f"{dv_material}", align='C')

        pdf.set_xy(92.5, 215)
        with pdf.rotation(270):
            pdf.cell(23, 5, f"{dv_size} {dv_rating}", align='C')
            pdf.cell(22, 5, f"{nipple_tub_material}", align='C')

    pdf.set_xy(87.5, 215)
    with pdf.rotation(270):
        pdf.cell(23, 5, f"{proc_conn_size} {proc_conn_rating}# {proc_conn_facing}" if proc_conn_type == 'FLANGED' else f"{proc_conn_size} {proc_conn_rating}", align='C')
        pdf.cell(22, 5, f"{proc_conn_material}", align='C')

    pdf.set_xy(82.5, 215)
    with pdf.rotation(270):
        pdf.cell(23, 5, f"{valve_conn}", align='C')
        pdf.cell(22, 5, f"{valve_material}", align='C')
    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(82.5, 268)
    with pdf.rotation(270):
        pdf.cell(10, 2.5, f"{valve_type}" + "NB" if valve_material == 'A-105' else "NC", align='C')

    pdf.set_font("Helvetica", "", 7)
    pdf.set_xy(77.5, 215)
    with pdf.rotation(270):
        pdf.cell(23, 5, f"{nipple_hex}", align='C')
        pdf.cell(22, 5, f"{nipple_hex_material}", align='C')

    pdf.set_xy(72.5, 206.5)
    with pdf.rotation(270):
        pdf.cell(8.5, 5, f"{int(studs_qty)}", align='C')
        pdf.cell(23, 5, f"", align='C')
        pdf.cell(22, 5, f"{bolts_material}", align='C')

    pdf.set_xy(67.5, 206.5)
    with pdf.rotation(270):
        pdf.cell(8.5, 5, f"{int(studs_qty) * 2}", align='C')
        pdf.cell(23, 5, f"", align='C')
        pdf.cell(22, 5, f"{nuts_material}", align='C')

    pdf.set_xy(62.5, 206.5)
    with pdf.rotation(270):
        pdf.cell(8.5, 5, f"{int(body_model[1]) * (2 if item_type == 'Transparent' else 1)}", align='C')
        pdf.cell(23, 5, f"", align='C')
        pdf.cell(22, 5, "BOROSILICATE", align='C')

    pdf.set_xy(58, 206.5)
    with pdf.rotation(270):
        pdf.cell(8.5, 5, f"{int(body_model[1]) * (4 if item_type == 'Transparent' else 2)}", align='C')
        pdf.cell(23, 5, f"", align='C')
        pdf.cell(22, 5, f"{gasket_material}", align='C')

    pdf.set_xy(53.5, 206.5)
    with pdf.rotation(270):
        pdf.cell(8.5, 5, f"{int(body_model[1]) * (2 if item_type == 'Transparent' else 1)}", align='C')
        pdf.cell(23, 5, f"{model_num}", align='C')
        pdf.cell(22, 5, f"{cover_material}", align='C')

    pdf.set_xy(48, 215)
    with pdf.rotation(270):
        pdf.cell(23, 5, f"{model_num}", align='C')
        pdf.cell(22, 5, f"{body_material}", align='C')

    # Project data
    pdf.set_xy(138, 222)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{engineering}", align='C')
        pdf.cell(31, 6, f"{customer}", align='C')

    pdf.set_xy(128, 222)
    with pdf.rotation(270):
        pdf.cell(37, 10, f"{project}", align='C')
        pdf.cell(31, 10, f"{po_number}", align='C')

    pdf.set_font("Helvetica", "", 6)
    # Drawing information
    write_revisions_horizontal(pdf, results_revisions)
    # pdf.set_xy(21, 177.75)
    # with pdf.rotation(270):
    #     pdf.cell(10, 3, f"{drawing_date}", align='C')

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(31, 256)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order)}-{int(drawing_number.split("-")[-1]):02d}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{int(drawing_number.split("-")[-1]):02d}/{counter:02d}", align='C')

    return io.BytesIO(pdf.output())



# Functions to create OF drawings PDFs
def dwg_of_op_ro_rf(item_type, num_order, count_drawings, connection, element_material, of_drawing, of_drawing_date, of_drawing_rev,
                    handle_height, handle_width, handle_thickness, plate_c_dim, plate_ext_diam, plate_type, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    pdf = PDF()
    pdf.add_font('DejaVuSansCondensed', '', str(get_path("Resources", "Iconos", "DejaVuSansCondensed.ttf")))
    pdf.set_font("DejaVuSansCondensed", size=6)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cur:
            query_revisions = ("""SELECT DISTINCT ON (of_drawing_rev) of_drawing_rev, TO_CHAR(MAX(of_drawing_date), 'dd/mm/yyyy')
                                FROM tags_data.tags_flow
                                WHERE of_drawing = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                                GROUP BY of_drawing_rev
                                ORDER BY of_drawing_rev DESC
                                LIMIT 4;""")

            cur.execute(query_revisions, (of_drawing, num_order,))
            results_revisions = cur.fetchall()

    total_count = 0

    # Equipment tag and principal dimensions
    pdf.set_font("Helvetica", "", 7)
    pdf.set_xy(185, 108)
    with pdf.rotation(270):
        pdf.cell(3, 4, str(handle_thickness), align='C')

    block_size = 20
    item_list = list(item_data)
    total_blocks = math.ceil(len(item_list) / block_size)

    for block_index, start in enumerate(range(0, len(item_list), block_size), start=1):
        if block_index > 1:
            pdf.add_page()
            total_count = 0

        block = item_list[start:start + block_size]

    # Equipment data
        pdf.set_font("DejaVuSansCondensed", size=6.5)
        pdf.set_xy(195.7, 156)
        with pdf.rotation(270):
            for tag, line_size, rating, facing, schedule, element_material, pipe_int_diam, orif_diam, plate_thk, dv_diam, w_diam, cnt, rev in block:
                size_line=line_size
                facing=facing

                z_diam = ''
                m_diam = ''
                if item_type == 'M.RUN':
                    query_mrun_lengths = ("""
                                            SELECT z_diam
                                            FROM validation_data.mrun_lengths
                                            WHERE connection = %s   
                                            """)

                    with Database_Connection(config_database()) as conn:
                        with conn.cursor() as cur:
                            cur.execute(query_mrun_lengths, (size_line,))
                            results_lengths = cur.fetchall()
                            z_diam = results_lengths[0][0]

                if '5-HOLED' in plate_type:
                    m_diam = round((float(pipe_int_diam) + float(orif_diam.replace(',','.').strip().split('x')[1]))/2,0)
                elif '4-HOLED' in plate_type:
                    m_diam = round((float(pipe_int_diam) + float(orif_diam.replace(',','.').strip().split('x')[1]))/(1 + math.sqrt(2)),0)

                y_pos = pdf.get_y()
                x_pos = pdf.get_x()

                str(rev) != "0" and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(rev) + ".png")), x = x_pos - 2, y = y_pos, w = 2, h = 2)
                pdf.cell(22, 5.62, str(tag), align='C')
                pdf.cell(18, 2.8, (str(line_size).split('"/')[1] if '"/' in str(line_size) else str(line_size)) + " " + (str(rating).split("/")[1] if "/" in str(rating) else str(rating)) + "# " + str(facing), align='C')
                pdf.set_xy(x_pos + 22, y_pos + 2.8)
                pdf.cell(18, 2.8, f"{"SCH " + str(schedule)}", align='C')
                pdf.set_xy(x_pos + 22 + 18, y_pos)
                pdf.fixed_height_multicell(18, 5.65, str(element_material), 'C')
                pdf.set_xy(x_pos + 22 + 18 + 18, y_pos)
                pdf.cell(9, 5.62, str(float(pipe_int_diam)), align='C')
                pdf.cell(9, 5.62, str(orif_diam), align='C')
                pdf.cell(9, 5.62, str(plate_thk), align='C')
                pdf.cell(10.5, 5.62, str(dv_diam) if item_type in ['F+P', 'P'] else (str(m_diam) if 'HOLED' in plate_type else ''), align='C')
                pdf.cell(10, 5.62, str(w_diam) if item_type in ['F+P', 'P'] else '', align='C')
                pdf.cell(10, 5.62, str(m_diam) if 'HOLED' in plate_type and  item_type in ['F+P', 'P'] else '', align='C')
                # pdf.cell(31.5, 5.62, str(nace) if (str(nace) not in ['None', 'NO', 'N/A'] and item_type in ['F+P', 'P', 'M.RUN']) else '', align='C')

                pdf.set_xy(x_pos, y_pos + 5.62)

                total_count += int(cnt)

        pdf.set_font("DejaVuSansCondensed", size=6)

        # Plate dimensions
        pdf.set_xy(138, 75)
        with pdf.rotation(270):
            pdf.cell(12, 4, "SURFACE: 125-250 Ra" if facing in ['RF', 'FF'] else ("SURFACE: 63-125 Ra" if facing == 'RF63-125' else ''), align='C')

        pdf.set_xy(52, 28.5)
        with pdf.rotation(270):
            pdf.cell(12, 4, f"{size_line}", align='C')
            pdf.cell(10, 4, f"{handle_height}", align='C')
            pdf.cell(9, 4, f"{handle_width}", align='C')
            pdf.cell(8, 4, f"{plate_c_dim}" if plate_c_dim else "", align='C')
            pdf.cell(11, 4, f"{plate_ext_diam}", align='C')
            pdf.cell(11, 4,
                    str(round(float(orif_diam.replace(',','.')) * 1.5, 1)) if plate_type == 'QUADRANT' else
                    (str(round((float(pipe_int_diam) - float(orif_diam.replace(',','.')))/2 - 0.01 * float(pipe_int_diam), 2)) if plate_type == 'ECC' else
                    (f"{z_diam}" if (str(size_line) == '1/2"' or str(size_line) == '1"' ) else
                    '')), align='C')
            pdf.cell(11, 4, str(round(float(plate_thk) - float(plate_c_dim.replace(',','.').split("=")[1]),1)) if plate_type == 'QUADRANT' else '', align='C')

        if 'ADELANTO' in of_drawing_rev:
            pdf.set_text_color(255, 0, 0)
            pdf.set_font("Helvetica", "B", 15)
            pdf.set_xy(60, 180)
            with pdf.rotation(270):
                pdf.cell(14, 10, "ADELANTO", align='L')
        else:
            pdf.set_font("Helvetica", "", 6)
            write_revisions_horizontal(pdf, results_revisions)

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_xy(34, 166)
        with pdf.rotation(270):
            pdf.cell(14, 10, f"{total_count}", align='C')
            pdf.set_font("Helvetica", "", 7)
            pdf.cell(41, 10, f"{element_material}", align='C')
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(35, 10, f"{connection}", align='C')
            pdf.cell(37, 10, f"{num_order}", align='C')

        pdf.set_font("Helvetica", "", 10)
        pdf.set_xy(22, 265)
        with pdf.rotation(270):
            pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order) + '-' + str(of_drawing).split('-')[1]}", align='C')

        pdf.set_xy(16, 265)
        with pdf.rotation(270):
            pdf.cell(28, 6, f"{of_drawing}/{count_drawings:02d}" + (f" ({block_index}/{total_blocks})" if total_blocks > 1 else ""), align='C')

    return io.BytesIO(pdf.output())

def dwg_of_op_ro_rtj(item_type, num_order, count_drawings, connection, element_material, of_drawing, of_drawing_date, of_drawing_rev,
                    plate_c_dim, rtj_thickness, plate_type, handle_height, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    pdf = PDF()
    pdf.add_font('DejaVuSansCondensed', '', str(get_path("Resources", "Iconos", "DejaVuSansCondensed.ttf")))
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cur:
            query_revisions = ("""SELECT DISTINCT ON (of_drawing_rev) of_drawing_rev, TO_CHAR(MAX(of_drawing_date), 'dd/mm/yyyy')
                                FROM tags_data.tags_flow
                                WHERE of_drawing = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                                GROUP BY of_drawing_rev
                                ORDER BY of_drawing_rev DESC
                                LIMIT 4;""")

            cur.execute(query_revisions, (of_drawing, num_order,))
            results_revisions = cur.fetchall()

    total_count = 0

    block_size = 20
    item_list = list(item_data)
    total_blocks = math.ceil(len(item_list) / block_size)

    # gasket_main_material = gasket_material.split(";")[0].replace("ORTJ Type", "").strip()

    # Equipment data
    for block_index, start in enumerate(range(0, len(item_list), block_size), start=1):
        if block_index > 1:
            pdf.add_page()
            total_count = 0

        block = item_list[start:start + block_size]
        pdf.set_xy(195.7, 156)
        with pdf.rotation(270):
            pdf.set_font("Helvetica", "", 6.5)
            for tag, line_size, rating, facing, schedule, element_material, pipe_int_diam, orif_diam, plate_thk, dv_diam, w_diam, cnt in block:
                y_pos = pdf.get_y()
                x_pos = pdf.get_x()

                m_diam = ''

                if '5-HOLED' in plate_type:
                    m_diam = round((float(pipe_int_diam) + float(orif_diam.replace(',','.').strip().split('x')[1]))/2,0)
                elif '4-HOLED' in plate_type:
                    m_diam = round((float(pipe_int_diam) + float(orif_diam.replace(',','.').strip().split('x')[1]))/(1 + math.sqrt(1)),0)

                size=line_size
                rating=rating
                pdf.cell(23, 5.65, str(tag), align='C')
                pdf.fixed_height_multicell(18.1, 5.65, str(line_size) + " " + str(rating) + "# " + ('RTJ' if 'RTJ' in str(facing) else str(facing)) + "\n" + f"{"SCH " + str(schedule)}", 'C')
                pdf.set_xy(x_pos + 23 + 18.1, y_pos)
                pdf.fixed_height_multicell(17, 5.65, str(element_material), 'C')
                pdf.set_xy(x_pos + 23 + 18.1 + 17, y_pos)
                pdf.cell(9.5, 5.65, str(pipe_int_diam), align='C')
                pdf.cell(14, 5.65, str(orif_diam), align='C')
                pdf.cell(11.25, 5.65, str(plate_thk) if item_type in ['F+P', 'P', 'M.RUN', 'RO'] else '', align='C')
                pdf.cell(11.5, 5.65, str(dv_diam) if item_type in ['F+P', 'P'] else '', align='C')
                pdf.cell(12, 5.65, str(w_diam) if item_type in ['F+P', 'P'] else '', align='C')
                pdf.cell(15, 5.65, (str(m_diam) if 'HOLED' in plate_type else ''), align='C')

                # pdf.ln()
                pdf.set_xy(x_pos, y_pos + 5.65)

                total_count += int(cnt)

        pdf.set_font("Helvetica", "", 7)
        plate_dimensions = str(size) + " " + str(rating)

        query_plate_dimensions = ("""
                                SELECT p_diam, r_number, internal_plate_size, a_dim, c_dim, f_diam, s_diam,
                                bar_diam, l1_length, l2_length, thread,
                                g_dim, dim_0125, k_dim, rest_dim
                                FROM validation_data.flow_rtj_plate_dimensions
                                WHERE plate_size = %s""")

        query_ro_dimensions = ("""
                                SELECT p_diam, r_number,
                                bar_diam, l1_length, l2_length, thread,
                                ro_ext_diam, ro_e_dim, ro_f_dim, ro_x_dim
                                FROM validation_data.flow_rtj_plate_dimensions
                                WHERE plate_size = %s""")

        if item_type in ['F+P', 'P', 'M.RUN'] or (item_type == 'RO' and facing == 'RTJ-M'):
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(query_plate_dimensions, (plate_dimensions,))
                    results_ro = cur.fetchall()
                    print(results_ro)
                    p_diam = results_ro[0][0]
                    r_number = results_ro[0][1]
                    internal_plate_size = results_ro[0][2]
                    a_dim = results_ro[0][3]
                    c_dim = results_ro[0][4]
                    f_diam = results_ro[0][5]
                    s_diam = results_ro[0][6]
                    bar_diam = results_ro[0][7]
                    l1_length = results_ro[0][8]
                    l2_length = results_ro[0][9]
                    thread = results_ro[0][10]
                    g_dim = results_ro[0][11]
                    dim_0125 = results_ro[0][12]
                    k_dim = results_ro[0][13]
                    rest_dim = results_ro[0][14]

            pdf.set_xy(174, 125)
            with pdf.rotation(270):
                pdf.cell(4, 2, f"{c_dim}", align='C')

            pdf.set_xy(168, 136)
            with pdf.rotation(270):
                pdf.cell(4, 2, f"{a_dim}", align='C')

            pdf.set_xy(132, 133)
            with pdf.rotation(270):
                pdf.cell(4, 3, f"{round(float(p_diam) - float(a_dim),2)}", align='C')

            pdf.set_xy(132, 143)
            with pdf.rotation(270):
                pdf.cell(4, 3, f"{round(float(p_diam) + float(a_dim),2)}", align='C')

            if size not in ['1-1/2"', '1-1/4"', '1-1/4"', '1/2"', '1/4"', '1/8"', '2"/1-1/2"', '2"/1"', '2"/3/4"', '3/4"', '3/8"'] and (size+rating) not in ['2"300', '2"600'] and item_type != 'RO':
                pdf.set_xy(42, 77)
                with pdf.rotation(270):
                    pdf.cell(4, 3, f"{internal_plate_size}", align='C')

                pdf.set_xy(132, 123)
                with pdf.rotation(270):
                    pdf.cell(4, 3, f"{f_diam}", align='C')

                pdf.set_xy(95, 92)
                with pdf.rotation(270):
                    pdf.cell(4, 3, f"{dim_0125}", align='C')

                pdf.set_xy(98, 121)
                with pdf.rotation(270):
                    pdf.cell(4, 3, f"{k_dim}", align='C')

                pdf.set_xy(82, 92)
                with pdf.rotation(270):
                    pdf.cell(4, 3, f"{g_dim}", align='C')

                pdf.set_xy(89, 121)
                with pdf.rotation(270):
                    pdf.cell(4, 3, f"{rest_dim}", align='C')

                pdf.set_xy(100, 20)
                with pdf.rotation(270):
                    pdf.cell(4, 3, f"{s_diam}", align='C')

        else:
            with Database_Connection(config_database()) as conn:
                with conn.cursor() as cur:
                    cur.execute(query_ro_dimensions, (plate_dimensions,))
                    results_ro = cur.fetchall()
                    p_diam = results_ro[0][0]
                    r_number = results_ro[0][1]
                    bar_diam = results_ro[0][2]
                    l1_length = results_ro[0][3]
                    l2_length = results_ro[0][4]
                    thread = results_ro[0][5]
                    ro_ext_diam = results_ro[0][6]
                    ro_e_dim = results_ro[0][7]
                    ro_f_dim = results_ro[0][8]
                    ro_x_dim = results_ro[0][9]

            pdf.set_xy(112, 134)
            with pdf.rotation(270):
                pdf.cell(7, 3, f"{ro_ext_diam}", align='C')

            pdf.set_xy(60, 105)
            with pdf.rotation(270):
                pdf.cell(5, 3, f"{ro_e_dim}", align='C')

            pdf.set_xy(33, 134)
            with pdf.rotation(270):
                pdf.cell(7, 3, f"{ro_x_dim}", align='C')

            pdf.set_xy(33, 148)
            with pdf.rotation(270):
                pdf.cell(7, 3, f"{ro_f_dim}", align='C')

        pdf.set_xy(178, 21)
        with pdf.rotation(270):
            pdf.cell(7, 2, f"{handle_height}", align='C')

        pdf.set_xy(170, 67)
        with pdf.rotation(270):
            pdf.cell(7, 2, f"{l2_length}", align='C')

        pdf.set_font('DejaVuSansCondensed','', size=7)
        pdf.set_xy(167, 60)
        with pdf.rotation(270):
            pdf.cell(7, 2, f"{bar_diam}", align='C')

        pdf.set_font("Helvetica", "", 7)
        pdf.set_xy(184, 115)
        with pdf.rotation(270):
            pdf.cell(7, 2, f"{thread}", align='C')

        pdf.set_xy(72, 28)
        with pdf.rotation(270):
            pdf.cell(13, 5, f"{size + ' / ' + r_number}", align='C')
            pdf.cell(10, 5, f"{p_diam}", align='C')
            pdf.cell(8, 5, f"{rtj_thickness}", align='C')
            pdf.cell(8, 5, str(plate_c_dim) if item_type in ['F+P', 'P', 'M.RUN'] else '', align='C')

        pdf.set_font("Helvetica", "", 9)
        pdf.set_xy(33, 166)
        with pdf.rotation(270):
            pdf.cell(14, 7, f"{total_count}", align='C')
            # if item_type in ['RO', 'M.RUN']:
            pdf.cell(41, 7, f"{element_material}", align='C')
            # else:
            #     pdf.fixed_height_multicell(41, 7, gasket_main_material + " +\n" +f"{element_material}", 'C')
            #     pdf.set_xy(89, 166)
            pdf.cell(35, 7, f"{connection}", align='C')
            pdf.cell(37, 7, f"{num_order}", align='C')

        # Drawing information
        if 'ADELANTO' in of_drawing_rev:
            pdf.set_text_color(255, 0, 0)
            pdf.set_font("Helvetica", "B", 15)
            pdf.set_xy(60, 180)
            with pdf.rotation(270):
                pdf.cell(14, 10, "ADELANTO", align='L')
        else:
            pdf.set_font("Helvetica", "", 6)
            write_revisions_horizontal(pdf, results_revisions)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_xy(22, 265)
        with pdf.rotation(270):
            pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order) + '-' + str(of_drawing).split('-')[1]}", align='C')

        pdf.set_xy(16, 265)
        with pdf.rotation(270):
            pdf.cell(28, 6, f"{of_drawing}/{count_drawings:02d}" + (f" ({block_index}/{total_blocks})" if total_blocks > 1 else ""), align='C')

    return io.BytesIO(pdf.output())

def dwg_of_ms_ro(num_order: str, count_drawings,
                    flange_material: str, tube_material: str, plate_material: str,
                    of_drawing: str, item_data) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cur:
            query_revisions = ("""SELECT DISTINCT ON (of_drawing_rev) of_drawing_rev, TO_CHAR(MAX(of_drawing_date), 'dd/mm/yyyy')
                                FROM tags_data.tags_flow
                                WHERE of_drawing = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                                GROUP BY of_drawing_rev
                                ORDER BY of_drawing_rev DESC
                                LIMIT 4;""")

            cur.execute(query_revisions, (of_drawing, num_order,))
            results_revisions = cur.fetchall()

    pdf = PDF()
    pdf.set_font("Helvetica", "", 5.5)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    total_count = 0

    # Equipment tag and principal dimensions
    pdf.set_xy(196, 156)
    with pdf.rotation(270):
        for tag, size, rating, facing, schedule, stages_number, pipe_int_diam, approx_length, notes, cnt in item_data:
            x_pos = pdf.get_x()
            y_pos = pdf.get_y()

            pdf.cell(22, 5.75, str(tag), align='C')
            pdf.fixed_height_multicell(18.1, 5.75, str(size) + " " + str(rating) + "# " + ('RTJ' if 'RTJ' in str(facing) else str(facing)) + "\n" + f"{"SCH " + str(schedule)}", 'C')
            pdf.set_xy(x_pos + 22 + 18.1, y_pos)
            pdf.cell(18, 5.75, str(stages_number), align='C')
            pdf.cell(9, 5.75, str(pipe_int_diam), align='C')
            pdf.cell(18, 5.75, str(approx_length), align='C')
            pdf.cell(11, 5.75, str(notes) if str(notes) not in  ['None', 'NO', 'N/A'] else '', align='C')

            pdf.set_xy(x_pos, y_pos + 5.75)
            
            total_count += int(cnt)

    # Equipment data
    pdf.set_xy(58, 206)
    with pdf.rotation(270):
        pdf.cell(9, 5, str(stages_number), align='C')
        pdf.cell(22, 5, '', align='C')
        pdf.fixed_height_multicell(26, 5, str(plate_material), 'C')
    
    pdf.set_xy(53, 206)
    with pdf.rotation(270):
        pdf.cell(9, 5, str(int(stages_number) - 1), align='C')
        pdf.cell(22, 5, str(size) + " SCH " + str(schedule), align='C')
        pdf.cell(26, 5, str(tube_material), align='C')

    pdf.set_xy(48, 215)
    with pdf.rotation(270):
        pdf.cell(22, 5, str(size) + " " + str(rating) + " WN " + str(facing), align='C')
        pdf.cell(26, 5, str(flange_material), align='C')

    # Drawing information
    pdf.set_font("Helvetica", "", 5.5)
    write_revisions_horizontal(pdf, results_revisions)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_xy(33, 166)
    with pdf.rotation(270):
        pdf.cell(14, 7, f"{total_count}", align='C')

        pdf.cell(41, 7, "", align='C')
        pdf.cell(35, 7, str(size) + " " + str(rating) + " " + str(facing), align='C')
        pdf.cell(37, 7, f"{num_order}", align='C')

    # pdf.set_font("Helvetica", "", 10)
    # pdf.set_xy(33, 256)
    # with pdf.rotation(270):
    #     pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order) + '-' + str(of_drawing).split('-')[1]}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{of_drawing}/{count_drawings:02d}", align='C')

    return io.BytesIO(pdf.output())



def dwg_of_thermowell(tw_type, num_order, count_drawings, connection, material_tw, base_diam, std_length, insertion_length,
                    root_diam, tip_diam, bore_diam, tip_thk, radius_dim,
                    conical_length, straight_length, puntal,
                    of_drawing, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cur:
            query_code = ("""
                    SELECT code_material
                    FROM validation_data.temp_tw_material
                    WHERE tw_material = %s""")

            query_welding_procedure = ("""
                    SELECT first_option
                    FROM validation_data.temp_welding_proc
                    WHERE material = %s""")

            query_revisions = ("""SELECT DISTINCT ON (of_drawing_rev) of_drawing_rev, TO_CHAR(MAX(of_drawing_date), 'dd/mm/yyyy')
                                FROM tags_data.tags_temp
                                WHERE of_drawing = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                                GROUP BY of_drawing_rev
                                ORDER BY of_drawing_rev DESC
                                LIMIT 4;""")

            query_tests = ("""SELECT order_extras FROM public.orders WHERE num_order = %s""")

            cur.execute(query_code, (material_tw,))
            results = cur.fetchall()
            code_material = results[0][0]

            cur.execute(query_welding_procedure, (code_material,))
            results = cur.fetchall()
            welding_procedure = results[0][0]

            cur.execute(query_revisions, (of_drawing, num_order,))
            results_revisions = cur.fetchall()

            cur.execute(query_tests, (num_order,))
            results_tests = cur.fetchall()

            applicable_tests = (results_tests[0][0] or '').replace(',', '\n').replace('Calibración', '')
            if tw_type in ['VORTICRACK', 'Flanged Helical', 'Forged Flanged TW']:
                applicable_tests = applicable_tests.replace('LP\n', '').replace('RX\n', '').replace('Ultrasonidos\n', '')
            applicable_tests = 'PH' + ('(int/ext)' if 'Prueba Hidráulica Externa' in applicable_tests else '') + '\n' + applicable_tests.replace('Prueba Hidráulica Externa\n', '') 

    pdf = PDF()
    pdf.add_font('DejaVuSansCondensed', '', str(get_path("Resources", "Iconos", "DejaVuSansCondensed.ttf")))
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    total_count = 0

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(122, 16)
    pdf.cell(5, 3, str(base_diam), align='C')

    pdf.set_xy(174, 60)
    pdf.cell(5, 3, str(int(std_length) - int(insertion_length)), align='C')

    pdf.set_xy(185, 109)
    pdf.cell(6, 3, str(std_length), align='C')

    pdf.set_xy(174, 127)
    pdf.cell(5, 3, str(insertion_length), align='C')

    pdf.set_xy(102, 84)
    pdf.cell(5, 3, str(radius_dim) if radius_dim != 'N/A' else '', align='C')

    if tw_type in ['VORTICRACK', 'Flanged Helical']:
        pdf.set_xy(164, 147)
        pdf.cell(6, 3, str(straight_length), align='C')

        pdf.set_xy(164, 84)
        pdf.cell(5, 3, str(conical_length), align='C')

    if (tw_type == 'Flanged TW' and int(insertion_length) > 500):
        pdf.set_xy(164, 112)
        pdf.cell(6, 3, str(straight_length), align='C')

        pdf.set_xy(164, 165)
        pdf.cell(5, 3, str(conical_length), align='C')

    if tw_type in ['Flanged TWP']:
        pdf.set_xy(164, 112)
        pdf.cell(6, 3, str(straight_length), align='C')

        pdf.set_xy(164, 165)
        pdf.cell(5, 3, str(conical_length), align='C')

        pdf.set_xy(94, 156)
        pdf.cell(5, 3, str(puntal).split(" X ")[1].split(" ")[0], align='C')

    if tw_type in ['VORTICRACK', 'Flanged Helical']:
        pdf.set_xy(135, 88)
    else:
        pdf.set_xy(103, 98)

    pdf.cell(5, 3, str(root_diam) if root_diam != 'N/A' else '', align='C')

    pdf.set_xy(156, 183)
    pdf.cell(5, 3, str(int(float(tip_thk))) if tip_thk != 'N/A' else '', align='C')

    pdf.set_xy(164, 183)
    pdf.cell(5, 3, str(int(float(tip_thk) + 2)) if tip_thk != 'N/A' else '', align='C')

    pdf.set_xy(105, 191)
    pdf.cell(5, 3, ("7" if float(str(bore_diam).replace(",",".")) else str(bore_diam)) if bore_diam != 'N/A' else '', align='C')

    pdf.set_xy(104, 200)
    pdf.cell(5, 3, str(tip_diam) if tip_diam != 'N/A' else '', align='C')

    if tw_type in ['VORTICRACK', 'Flanged Helical']:
        pdf.set_xy(109, 101)
        pdf.cell(5, 3, str(tip_diam) if tip_diam != 'N/A' else '', align='C')

        pdf.set_xy(82, 170)
        pdf.cell(5, 3, str(tip_diam) if tip_diam != 'N/A' else '', align='C')

        pdf.set_xy(80, 177)
        pdf.cell(5, 3, str(int(tip_diam) + 5) if tip_diam != 'N/A' else '', align='C')
        
        pdf.set_xy(122, 213)
        pdf.cell(5, 3, str(int(tip_diam) + 5) if tip_diam != 'N/A' else '', align='C')

    pdf.set_xy(24, 14.8)
    for tag, rev in item_data:
        x_pos = pdf.get_x()
        y_pos = pdf.get_y()
        int(rev) != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(rev) + ".png")), x = x_pos - 3, y = y_pos, w = 2, h = 2)
        pdf.cell(26, 6.4, str(tag), align='L')
        pdf.set_xy(x_pos, y_pos + 6.4)
        total_count += 1

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_xy(61, 10)
    pdf.set_text_color(255, 0, 0)
    pdf.fixed_height_multicell(15, 19, str(applicable_tests), 'L')

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 10)

    if tw_type in ['Flanged TWP']:
        pdf.set_xy(135, 214)
    else:
        pdf.set_xy(135, 219)
    welding_procedure = '' if tw_type in ['VORTICRACK', 'Forged Flanged TW'] else welding_procedure
    pdf.cell(30.5, 5, str(welding_procedure), align='C')

    if tw_type in ['Flanged TWP']:
        pdf.set_xy(101.5, 219)
        pdf.cell(38.5, 6, str(material_tw), align='C')

    pdf.set_xy(71, 225)
    if tw_type in ['Flanged TWP']:
        pdf.cell(30.5, 6, "ø32xø16", align='C')
    else:
        pdf.cell(30.5, 6, "ø" + str(base_diam) + " mm", align='C')

    pdf.cell(38.5, 6, str(material_tw), align='C')

    pdf.set_xy(71, 231)
    pdf.set_font("DejaVuSansCondensed", size=10)
    pdf.cell(30.5, 6, str(connection), align='C')
    pdf.cell(38.5, 6, str(material_tw), align='C')

    pdf.set_font("Helvetica", "", 7)
    write_revisions_vertical(pdf, results_revisions)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_xy(24, 251)
    pdf.cell(21, 6, str(total_count), align='C')
    pdf.cell(37, 6, str(material_tw), align='C')
    pdf.cell(70, 6, "", align='C')
    pdf.cell(52, 6, str(num_order), align='C')

    pdf.set_xy(164, 265)
    pdf.cell(40, 8, f"{re.sub(r"^P-", "", num_order) + '-' + str(of_drawing).split('-')[1]}", align='C')

    pdf.set_xy(164, 274)
    pdf.cell(40, 3, f"{of_drawing}/{count_drawings:02d}", align='C')

    return io.BytesIO(pdf.output())

def dwg_of_sensor(num_order, count_drawings, sensor_element, sheath_stem_material, sheath_stem_diam,
                insulation, nipple_ext_material, head_case_material, head_certification, elec_conn_case_diam,
                of_sensor_drawing, item_data):
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    pdf = PDF()
    pdf.add_font('DejaVuSansCondensed', '', str(get_path("Resources", "Iconos", "DejaVuSansCondensed.ttf")))
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cur:
            query_revisions = ("""SELECT DISTINCT ON (of_sensor_drawing_rev) of_sensor_drawing_rev, TO_CHAR(MAX(of_sensor_drawing_date), 'dd/mm/yyyy')
                                FROM tags_data.tags_temp
                                WHERE of_sensor_drawing = %s AND num_order LIKE (%s||'%%') AND tag_state in ('PURCHASED', 'SUPERADO')
                                GROUP BY of_sensor_drawing_rev
                                ORDER BY of_sensor_drawing_rev DESC
                                LIMIT 4;""")

            query_tests = ("""SELECT order_extras FROM public.orders WHERE num_order = %s""")

            cur.execute(query_revisions, (of_sensor_drawing, num_order,))
            results_revisions = cur.fetchall()

            cur.execute(query_tests, (num_order,))
            results_tests = cur.fetchall()

            applicable_tests = "Calibracion" if "Calibración" in (results_tests[0][0] or '') else ''

    total_count = 0

    block_size = 25
    item_list = list(item_data)
    total_blocks = math.ceil(len(item_list) / block_size)

    dim_l_total = 0

    for block_index, start in enumerate(range(0, len(item_list), block_size), start=1):
        if block_index > 1:
            pdf.add_page()
            total_count = 0

        block = item_list[start:start + block_size]
        pdf.set_xy(24, 14.8)
        pdf.set_font("Helvetica", "", 10)
        for tag, dim_a, dim_b, dim_l, rev in block:
            x_pos = pdf.get_x()
            y_pos = pdf.get_y()
            int(rev) != 0 and pdf.image(str(get_path("Resources", "Iconos", "Triangle_Rev" + str(rev) + ".png")), x = x_pos - 3, y = y_pos, w = 2, h = 2)
            pdf.cell(36, 6.4, str(tag), align='C')
            pdf.cell(13, 6.4, str(dim_a), align='C')
            pdf.cell(12, 6.4, str(dim_b), align='C')
            pdf.cell(12, 6.4, str(dim_l), align='C')

            pdf.set_xy(x_pos, y_pos + 6.4)
            total_count += 1
            dim_l_total += float(dim_l)

        pdf.cell(36, 6.4, "TOTAL L", align='C')
        pdf.cell(25, 6.4, "", align='C')
        pdf.cell(12, 6.4, str(dim_l_total), align='C')
        dim_l_total = 0

        pdf.set_xy(105, 12)
        pdf.cell(5, 3, "TERMOPAR:" if "T/C" in sensor_element else "TERMORRESISTENCIA", align='L')

        pdf.set_xy(105, 15)
        pdf.cell(5, 3, "AISLADO DE MASA" if str(insulation) == "Ungrounded" else ("A MASA" if str(insulation) == "Grounded" else ""), align='L')

        pdf.set_font("Helvetica", "B", 9)
        pdf.set_xy(100, 20)
        pdf.set_text_color(255, 0, 0)
        pdf.cell(20, 6, str(applicable_tests), align='L')

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 10)

        pdf.set_xy(186, 24)
        pdf.cell(10, 3, f"{elec_conn_case_diam.split('x')[1]}", align='C')

        pdf.set_xy(130, 184)
        pdf.cell(3, 3, str(sheath_stem_diam), align='C')

        pdf.set_font("Helvetica", "", 8)
        pdf.set_xy(71, 201)
        pdf.cell(30.5, 6, str(sensor_element), align='C')
        pdf.cell(29, 6, str(sheath_stem_material), align='C')
        pdf.cell(20.5, 6, "", align='C')
        pdf.cell(15, 6, '2 HILOS' if 'T/C Single' in sensor_element else ('4 HILOS' if 'T/C Double' in sensor_element else ((sensor_element.split('(')[1][0] + ' HILOS') if '(' in sensor_element else '')), align='C')

        pdf.set_xy(71, 207.5)
        pdf.set_font("DejaVuSansCondensed", size=10)
        pdf.cell(30.5, 6, f"{re.search(r'(\d+/\d+")\s*\((.*?)\)', nipple_ext_material).group(1)}NPT", align='C')
        pdf.cell(29, 6, 'A-106' if re.search(r'(\d+/\d+")\s*\((.*?)\)', nipple_ext_material).group(2) == 'CS' else 'SS 316/316L', align='C')

        pdf.set_xy(71, 214)
        pdf.cell(30.5, 6, f"{re.search(r'(\d+/\d+")\s*\((.*?)\)', nipple_ext_material).group(1)}NPT x {re.search(r'(\d+/\d+")\s*\((.*?)\)', nipple_ext_material).group(1)}NPT", align='C')
        pdf.cell(29, 6, 'A-105' if re.search(r'(\d+/\d+")\s*\((.*?)\)', nipple_ext_material).group(2) == 'CS' else 'SS 316/316L', align='C')

        pdf.set_xy(71, 225)
        pdf.cell(60, 6, "", align='C')
        pdf.cell(19.5, 6, "E-H-10/2A" if "T/C" in sensor_element else "E-H-12/2A", align='C')

        pdf.set_font("Helvetica", "", 8)
        pdf.set_xy(71, 231)
        pdf.cell(30.5, 6, str(elec_conn_case_diam), align='C')
        pdf.cell(49.5, 6, "", align='C')
        pdf.fixed_height_multicell(50, 6, f"{head_certification}" if head_certification != 'N/A' else '', 'L')

        pdf.set_font("Helvetica", "", 7)
        write_revisions_vertical(pdf, results_revisions)

        pdf.set_font("Helvetica", "", 12)
        pdf.set_xy(24, 251)
        pdf.cell(21, 6, str(total_count), align='C')
        pdf.cell(37, 6, "", align='C')
        pdf.cell(70, 6, "", align='C')
        pdf.cell(52, 6, str(num_order), align='C')

        pdf.set_xy(164, 265)
        pdf.cell(40, 8, f"{re.sub(r"^P-", "", num_order) + '-' + str(of_sensor_drawing).split('-')[1]}", align='C')

        pdf.set_xy(164, 274)
        pdf.cell(40, 3, f"{of_sensor_drawing}/{count_drawings:02d}" + (f" ({block_index}/{total_blocks})" if total_blocks > 1 else ""), align='C')

    return io.BytesIO(pdf.output())



# Function to create special drawings PDFs
def dwg_dim_flange_plate_riyas(num_order: str, tag: str,
                        size: str, schedule: str, rating: str, facing: str,
                        pipe_int_diam: str, bore_diam: str, thickness: str, dv_diam: str, notes: str, tapping_size:str, tapping_orientation: str, weight: str,
                        o_diam: str, a_diam: str, c_flange: str, y_flange: str, x_diam: str, r_diam: str, d_diam: str, t_flange: str, n_bores: str, diam_bores: str,
                        handle_height: str, handle_width: str, plate_c_dim: str, plate_ext_diam: str,
                        rtj_thickness: str, rtj_r_type: str, rtj_p_diam: str, rtj_e_diam: str, rtj_f_diam: str, plate_type: str,
                        engineering: str, customer: str, project: str, po_number: str,
                        flange_material: str, stud_material: str, nut_material: str, plate_material: str, gasket_material: str, plug_qty: str, plug_material: str, screw_material: str,
                        notes_flange: str, notes_stud: str, notes_nut: str, notes_plate: str, notes_gasket: str, notes_plugs: str, notes_jack_screw: str,
                        drawing_number: str, drawing_date: str, counter: int) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    query_revisions = ("""SELECT dim_drawing_rev, TO_CHAR(dim_drawing_date, 'dd/mm/yyyy')
                        FROM tags_data.tags_flow
                        WHERE tag = %s AND num_order = %s AND tag_state in ('PURCHASED', 'SUPERADO')
                        ORDER BY dim_drawing_rev DESC
                        LIMIT 4;""")

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_revisions, (tag, num_order,))
            results_revisions = cursor.fetchall()

    pdf = PDF()
    pdf.add_font('DejaVuSansCondensed', '', str(get_path("Resources", "Iconos", "DejaVuSansCondensed.ttf")))
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    # with pdf.rotation(angle=-90, x=52, y=45):
    #     pdf.image(str(get_path("Resources", "Iconos", "Logo Nobg.ico")), x = 52, y = 45, w = 40, h = 30)

    # Equipment tag and principal dimensions
    pdf.set_font('DejaVuSansCondensed','', size=6)
    pdf.set_xy(195, 134)
    with pdf.rotation(270):
        pdf.cell(33, 6, str(tag), align='C')
        pdf.cell(23, 6, "", align='C')
        pdf.cell(12, 6, str(pipe_int_diam), align='C')
        pdf.cell(11, 6, str(bore_diam), align='C')
        pdf.cell(11, 6, str(thickness), align='C')
        pdf.cell(11, 6, str(dv_diam) if str(dv_diam) != 'None' else 'N/A', align='C')
        pdf.cell(12, 6, str(round((float(pipe_int_diam) - float(dv_diam.split("=")[1].replace(',', '.'))) / 2, 2)) if str(dv_diam) not in ['None', '', 'N/A'] else 'N/A', align='C')
        pdf.fixed_height_multicell(30, 5, f"{weight + '\n' + ('NACE MR-0175' if str(notes) not in ['None', 'NO', 'N/A'] else '')}", 'C')

    pdf.set_xy(195, 167)
    with pdf.rotation(270):
        pdf.cell(23, 3, str(size) + " " + str(rating) + " WN " + str(facing), align='C')

    pdf.set_xy(192, 167)
    with pdf.rotation(270):
        pdf.cell(23, 3, "SCH " + str(schedule), align='C')

    # Flange dimensions
    pdf.set_xy(45, 16)
    with pdf.rotation(270):
        pdf.cell(7, 4, f"{size + ' / ' + rtj_r_type}" if str(facing) == 'RTJ' else f"{size}", align='C')
        pdf.cell(12, 4, str(o_diam), align='C')
        pdf.cell(12, 4, str(a_diam), align='C')
        pdf.cell(12, 4, str(c_flange), align='C')
        pdf.cell(12, 4, str(y_flange), align='C')
        pdf.cell(12, 4, str(x_diam), align='C')
        pdf.cell(12, 4, str(r_diam), align='C')
        pdf.cell(12, 4, str(d_diam), align='C')
        pdf.cell(7, 4, str(tapping_orientation), align='C')
        pdf.cell(7, 4, str(t_flange), align='C')
        pdf.cell(7, 4, str(n_bores), align='C')
        pdf.cell(14, 4, str(diam_bores), align='C')

    # Plate dimensions
    pdf.set_xy(84, 183)
    with pdf.rotation(270):
        pdf.cell(15, 4, f"{size + ' / ' + rtj_r_type}" if str(facing) == 'RTJ' else f"{size}", align='C')
        pdf.cell(8, 4, f"{rtj_p_diam}" if str(facing) == 'RTJ' else f"{handle_height}", align='C')
        pdf.cell(7, 4, f"{rtj_thickness}" if str(facing) == 'RTJ' else f"{handle_width}", align='C')
        pdf.cell(8, 4, f"{plate_c_dim}" if str(plate_type) == 'SQE' else f"{plate_c_dim}", align='C')
        pdf.cell(14, 4, f"{handle_height}" if str(facing) == 'RTJ' else f"{plate_ext_diam}", align='C')

    # Materials and quantities
    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(40, 65)
    with pdf.rotation(270):
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(30, 4, f"{screw_material}", 'C')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(36, 65)
    with pdf.rotation(270):
        # pdf.cell(8, 4, f"{str(int(plug_qty)*2)}", align='C')
        pdf.cell(30, 4, f"{plug_material}", align='C')

    gasket_type = 'SPIRAL GASKETS' if 'SPW' in gasket_material else ('FLAT GASKETS' if 'FLAT' in gasket_material.upper() else '')

    if 'SPW' in gasket_material:
        match = re.search(r'F:([^/)]*)', gasket_material)
        if match:
            material = match.group(1)
            gasket_main_material = '316L+GRAPHITE' if material == '316+GRAPHITE' else material

    elif 'FLAT' in gasket_material.upper():
        gasket_main_material = 'SYNTHETIC FIBER'

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(31.5, 70)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(20, 4, f"{gasket_type + ' ' + gasket_main_material}", 'C')
        pdf.set_xy(x_pos + 25, y_pos)
        pdf.fixed_height_multicell(40, 4, notes_gasket if notes_gasket else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(27, 65)
    with pdf.rotation(270):
        pdf.cell(30, 4, f"{plate_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 4, notes_plate if notes_plate else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(23, 57)
    with pdf.rotation(270):
        pdf.cell(8, 4, f"{str(int(n_bores)*2)}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(30, 4, f"{nut_material}", 'C')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(19.5, 57)
    with pdf.rotation(270):
        pdf.cell(8, 5, f"{n_bores}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(30, 5, f"{stud_material}", 'C')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(15, 65)
    with pdf.rotation(270):
        pdf.cell(30, 4, f"{flange_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 4, notes_flange if notes_flange else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    # Drawing dates and revision information
    write_revisions_horizontal(pdf, results_revisions)
    # pdf.set_xy(21, 177.75)
    # with pdf.rotation(270):
    #     pdf.cell(10, 3, f"{drawing_date}", align='C')

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(31, 256)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order)}-{int(drawing_number.split("-")[-1]):02d}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{int(drawing_number.split("-")[-1]):02d}/{counter:02d}", align='C')

    return io.BytesIO(pdf.output())

def dwg_dim_mrun_riyas(num_order: str, tag: str,
                    size: str, schedule: str, rating: str, facing: str,
                    pipe_int_diam: str, bore_diam: str, notes: str, tapping_size: str, flange_type: str,
                    weight: str, length: str, tube_material: str,
                    handle_height: str, handle_width: str, plate_c_dim: str, plate_ext_diam: str,
                    rtj_thickness: str, rtj_r_type: str, rtj_p_diam: str, rtj_e_diam: str, rtj_f_diam: str,
                    engineering: str, customer: str, project: str, po_number: str,
                    flange_material: str, stud_material: str, nut_material: str, plate_material: str, gasket_material: str, plug_qty: str, plug_material: str, screw_material: str,
                    notes_flange: str, notes_stud: str, notes_nut: str, notes_plate: str, notes_gasket: str, notes_plugs: str, notes_jack_screw: str,
                    drawing_number: str, drawing_date: str, counter: int) -> io.BytesIO:
    """
    Generates a PDF containing a new content based on the specified value and equipment type.
    """

    query_revisions = ("""SELECT dim_drawing_rev, TO_CHAR(dim_drawing_date, 'dd/mm/yyyy')
                        FROM tags_data.tags_flow
                        WHERE tag = %s AND num_order = %s AND tag_state in ('PURCHASED', 'SUPERADO')
                        ORDER BY dim_drawing_rev DESC
                        LIMIT 4;""")

    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query_revisions, (tag, num_order,))
            results_revisions = cursor.fetchall()

    pdf = PDF()
    pdf.add_font('DejaVuSansCondensed', '', str(get_path("Resources", "Iconos", "DejaVuSansCondensed.ttf")))
    pdf.set_font("Helvetica", "", 6)
    pdf.set_text_color(0, 0, 0)

    pdf.add_page()

    size_orifice_flange = str(size).split('"/')[1] if '"/' in str(size) else size
    rating_orifice_flange = str(rating).split('/')[1] if '/' in str(rating) else rating
    type_orifice_flange = str(flange_type).split('/')[1] if '/' in str(flange_type) else flange_type

    size_line_flange = str(size).split('"/', 1)[0] + '"' if '"/' in str(size) else size
    rating_line_flange = str(rating).split('/')[0]
    type_line_flange = str(flange_type).split('/')[0]

    query_mrun_lengths = ("""
                            SELECT length_1, length_2
                            FROM validation_data.mrun_lengths
                            WHERE connection = %s   
                            """)
    
    with Database_Connection(config_database()) as conn:
        with conn.cursor() as cur:
            cur.execute(query_mrun_lengths, (size,))
            results_lengths = cur.fetchall()
            length_1 = results_lengths[0][0]
            length_2 = results_lengths[0][1]

    # Equipment tag and principal dimensions
    pdf.set_font('DejaVuSansCondensed','', size=6)
    pdf.set_xy(194, 151)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(29, 7, str(tag), align='C')
        pdf.cell(8, 7,  str(length_1), align='C')
        pdf.cell(9, 7, str(length_2), align='C')
        pdf.cell(8, 7, str(length), align='C')
        pdf.cell(9, 7, str(pipe_int_diam), align='C')
        pdf.cell(21, 3.5, str(size_orifice_flange) + " " + str(rating_orifice_flange) + "# " + str(type_orifice_flange) + " " + str(facing), align='C')
        pdf.set_xy(x_pos + 63, y_pos + 3.5)
        pdf.cell(21, 3.5, f"SCH {schedule}", align='C')
        pdf.set_xy(x_pos + 63 + 21, y_pos)
        pdf.cell(21, 3.5, str(size_line_flange) + " " + str(rating_line_flange) + "# " + str(type_line_flange) + " " + str(facing), align='C')
        pdf.set_xy(x_pos + 63 + 21, y_pos + 3.5)
        pdf.cell(21, 3.5, f"SCH {schedule}", align='C')
        pdf.set_xy(x_pos + 63 + 21 + 21, y_pos)
        pdf.cell(10, 7, str(bore_diam), align='C')
        pdf.fixed_height_multicell(20, 5, f"{weight + ' ' + ('NACE' if str(notes) not in ['None', 'NO', 'N/A'] else '')}", 'C')

    pdf.set_xy(20, 111)
    with pdf.rotation(270):
        pdf.cell(12, 4, f"{size + ' / ' + rtj_r_type}" if str(facing) == 'RTJ' else f"{size}", align='C')
        pdf.cell(10.5, 4, f"{rtj_p_diam}" if str(facing) == 'RTJ' else f"{handle_width}", align='C')
        pdf.cell(9, 4, f"{rtj_thickness}" if str(facing) == 'RTJ' else f"{plate_c_dim}", align='C')
        pdf.cell(8, 4, f"{plate_ext_diam}", align='C')

    # Materials and quantities
    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(95, 237)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(23.5, 5, screw_material if screw_material else '', 'C')
        pdf.set_xy(x_pos + 23.5, y_pos)
        pdf.fixed_height_multicell(22, 5, notes_jack_screw if notes_jack_screw else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(90, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(23, 2.5, str(size_line_flange) + " " + str(rating_line_flange) + "# " + str(type_line_flange) + " " + str(facing), align='C')
        pdf.set_xy(x_pos, y_pos + 2.5)
        pdf.cell(23, 2.5, f"SCH {schedule}", align='C')
        pdf.set_xy(x_pos + 23, y_pos)
        pdf.cell(22, 5, f"{flange_material}", align='C')
        pdf.fixed_height_multicell(55, 5, 'REDUCING FLANGE' if size_line_flange != size_orifice_flange else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(85, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(23, 5, str(size_orifice_flange) + " SCH " + str(schedule), align='C')
        pdf.cell(22, 5, f"{tube_material}", align='C')

    gasket_type = 'SPIRAL GASKETS' if 'SPW' in gasket_material else ('FLAT GASKETS' if 'FLAT' in gasket_material.upper() else '')
    gasket_main_material = re.search(r'F:([^/)]*)', gasket_material) if 'SPW' in gasket_material else ('SYNTHETIC FIBER' if 'FLAT' in gasket_material.upper() else '')
    gasket_main_material = '316L+GRAPHITE' if gasket_main_material.group(1) == '316+GRAPHITE' else gasket_main_material.group(1)

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(80, 238)
    with pdf.rotation(270):
        x_pos = pdf.get_x()
        y_pos = pdf.get_y()
        pdf.fixed_height_multicell(23, 5, f"{gasket_type + ' ' + gasket_main_material}", 'C')
        pdf.set_xy(x_pos + 23, y_pos)
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(40, 4, notes_gasket if notes_gasket else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(75, 238)
    with pdf.rotation(270):
        pdf.cell(23, 5, f"{plug_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 5, notes_plugs if notes_plugs else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(70, 238)
    with pdf.rotation(270):
        pdf.cell(23, 5, f"{plate_material}", align='C')
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(55, 5, notes_plate if notes_plate else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(65, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(23, 2.5, str(size_orifice_flange) + " " + str(rating_orifice_flange) + "# " + str(type_orifice_flange) + " " + str(facing), align='C')
        pdf.set_xy(x_pos, y_pos + 2.5)
        pdf.cell(23, 2.5, f"SCH {schedule}", align='C')
        pdf.set_xy(x_pos + 23, y_pos)
        pdf.cell(22, 5, f"{flange_material}", align='C')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(60, 237)
    with pdf.rotation(270):
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(23.5, 5, f"{nut_material}", 'C')
        pdf.set_xy(x_pos + 23.5, y_pos)
        pdf.fixed_height_multicell(55, 5, notes_nut if notes_nut else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(55, 237)
    with pdf.rotation(270):
        pdf.set_font("Helvetica", "", 5)
        pdf.fixed_height_multicell(23.5, 5, f"{stud_material}", 'C')
        pdf.set_xy(x_pos + 23.5, y_pos)
        pdf.fixed_height_multicell(55, 5, notes_stud if notes_stud else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(50, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(23, 5, str(size_orifice_flange) + " SCH " + str(schedule), align='C')
        pdf.cell(22, 5, f"{tube_material}", align='C')

    pdf.set_font("Helvetica", "", 6)
    pdf.set_xy(45.5, 215)
    with pdf.rotation(270):
        y_pos = pdf.get_y()
        x_pos = pdf.get_x()
        pdf.cell(23, 2.5, str(size_line_flange) + " " + str(rating_line_flange) + "# " + str(type_line_flange) + " " + str(facing), align='C')
        pdf.set_xy(x_pos, y_pos + 2.5)
        pdf.cell(23, 2.5, f"SCH {schedule}", align='C')
        pdf.set_xy(x_pos + 23, y_pos)
        pdf.cell(22, 5, f"{flange_material}", align='C')
        pdf.fixed_height_multicell(55, 5, 'REDUCING FLANGE' if size_line_flange != size_orifice_flange else '', 'L')

    pdf.set_font("Helvetica", "", 6)
    # Drawing information
    write_revisions_horizontal(pdf, results_revisions)
    # pdf.set_xy(21, 177.75)
    # with pdf.rotation(270):
    #     pdf.cell(10, 3, f"{drawing_date}", align='C')

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(31, 256)
    with pdf.rotation(270):
        pdf.cell(37, 6, f"{num_order}", align='C')

    pdf.set_xy(22, 265)
    with pdf.rotation(270):
        pdf.cell(28, 5, f"{re.sub(r"^P-", "", num_order)}-{int(drawing_number.split("-")[-1]):02d}", align='C')

    pdf.set_xy(16, 265)
    with pdf.rotation(270):
        pdf.cell(28, 6, f"{int(drawing_number.split("-")[-1]):02d}/{counter:02d}", align='C')

    return io.BytesIO(pdf.output())



def write_revisions_horizontal(pdf, revisions):
    rev_positions = [
    (21, 165.5),
    (18.2, 165.5),
    (15.5, 165.5),
    (12.5, 165.5),
    ]

    revisions = list(reversed(revisions))
    for (x, y), rev in zip(rev_positions, revisions):
        r, date = rev

        pdf.set_xy(x, y)
        with pdf.rotation(270):
            pdf.cell(7, 3, "REV.", align="C")
            pdf.cell(5, 3, str(r), align="C")
            pdf.cell(10.5, 3, str(date), align="C")
            pdf.image(str(get_path("Resources", "Iconos", "Drawing_Signature.png")), x = x + 22.5, y = y, w = 9, h = 3)

def write_revisions_vertical(pdf, revisions):
    rev_positions = [
    (24, 267),
    (24, 271),
    (24, 275),
    (24, 279),
    ]

    revisions = list(reversed(revisions))
    for (x, y), rev in zip(rev_positions, revisions):
        r, date = rev

        pdf.set_xy(x, y)
        pdf.cell(10, 4, "REV.", align="C")
        pdf.cell(7, 4, str(r), align="C")
        pdf.cell(15, 4, str(date), align="C")
        pdf.image(str(get_path("Resources", "Iconos", "Drawing_Signature.png")), x = x + 32, y = y, w = 13, h = 4)

