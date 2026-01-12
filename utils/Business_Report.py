from PySide6 import QtWidgets
from PDF_Styles import CustomPDF_A3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from io import BytesIO
import numpy as np
from Excel_Export_Templates import future_projects, order_reports
from config_keys import DATA_PATH
from config import config, get_path
from utils.Database_Manager import Database_Connection
from utils.Show_Message import MessageHelper
from datetime import *


def report_offers():
    start_date, end_date = get_date_range()

    if start_date and end_date:
        query_graph_commercial_1 = ("""
                        SELECT offers.num_offer, offers.state, offers.responsible,
                        COALESCE(offers.offer_amount, 0::money) AS offer_amount, COALESCE(orders.order_amount, 0::money) AS order_amount, orders.num_order
                        FROM offers
                        LEFT JOIN orders ON offers.num_offer = orders.num_offer
                        WHERE EXTRACT(YEAR FROM offers.register_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                        """)

        query_graph_commercial_2 = ("""
                            SELECT num_offer, state, responsible, 'offers' AS source_table
                            FROM offers
                            WHERE EXTRACT(YEAR FROM offers.register_date) = EXTRACT(YEAR FROM CURRENT_DATE)
                            """)

        query_graph_calculation_1 = ("""
                        SELECT offers.num_offer, offers.state, offers.responsible_calculations,
                        COALESCE(offers.offer_amount, 0::money) AS offer_amount, COALESCE(orders.order_amount, 0::money) AS order_amount
                        FROM offers
                        LEFT JOIN orders ON offers.num_offer = orders.num_offer
                        WHERE EXTRACT(YEAR FROM offers.register_date) = EXTRACT(YEAR FROM CURRENT_DATE) AND (offers.responsible_calculations NOT IN ('N/A', '') AND offers.responsible_calculations IS NOT NULL)
                        """)

        query_graph_calculation_2 = ("""
                            SELECT num_offer, state, responsible_calculations, 'offers' AS source_table
                            FROM offers
                            WHERE EXTRACT(YEAR FROM offers.register_date) = EXTRACT(YEAR FROM CURRENT_DATE) AND (offers.responsible_calculations NOT IN ('N/A', '') AND offers.responsible_calculations IS NOT NULL)
                            """)

        query_last_weekly_summary = ("""
                            SELECT num_offer, state, responsible, responsible_calculations, client, final_client,
                            TO_CHAR(recep_date, 'DD/MM/YYYY') as recep_date, TO_CHAR(presentation_date, 'DD/MM/YYYY') as presentation_date, TO_CHAR(limit_date, 'DD/MM/YYYY') as limit_date,
                            probability, '' as priority, material, items_number, offer_amount, actions, 'offers' AS source_table
                            FROM offers
                            WHERE register_date >= %s AND register_date <= %s
                            """)

        query_active_summary = ("""
                            SELECT num_offer, state, responsible, responsible_calculations, client, final_client,
                            TO_CHAR(recep_date, 'DD/MM/YYYY'), TO_CHAR(presentation_date, 'DD/MM/YYYY'), TO_CHAR(limit_date, 'DD/MM/YYYY'),
                            probability, '' as priority, material, items_number, offer_amount, actions
                            FROM offers
                            WHERE num_offer NOT LIKE '%B-%' AND state IN ('Registrada', 'En Estudio', 'Presentada')
                            ORDER BY state
                            """)

        query_active_budgetary_summary = ("""
                            SELECT num_offer, state, responsible, responsible_calculations, client, final_client,
                            TO_CHAR(recep_date, 'DD/MM/YYYY'), TO_CHAR(presentation_date, 'DD/MM/YYYY'), TO_CHAR(limit_date, 'DD/MM/YYYY'),
                            probability, '' as priority, material, items_number, offer_amount, actions
                            FROM offers
                            WHERE (num_offer LIKE '%B-%') AND (EXTRACT(YEAR FROM offers.register_date) = EXTRACT(YEAR FROM CURRENT_DATE))
                            ORDER BY state
                            """)

        with Database_Connection(config()) as conn:
            with conn.cursor() as cur:

                cur.execute(query_graph_commercial_1)
                results_graph_commercial_1 = cur.fetchall()
                df_graph_commercial_1 = pd.DataFrame(results_graph_commercial_1, columns=['Nº Oferta', 'Estado', 'Responsable', 'Importe Oferta', 'Importe Pedido', 'Nº Pedido'])

                df_graph_commercial_1['Importe Oferta'] = df_graph_commercial_1['Importe Oferta']\
                                            .str.replace('€', '', regex=False) \
                                            .str.replace('.', '', regex=False) \
                                            .str.replace(',', '.', regex=False) \
                                            .astype(float)

                df_graph_commercial_1['Importe Pedido'] = df_graph_commercial_1['Importe Pedido']\
                                            .str.replace('€', '', regex=False) \
                                            .str.replace('.', '', regex=False) \
                                            .str.replace(',', '.', regex=False) \
                                            .astype(float)

                df_graph_commercial_1['Importe Final'] = df_graph_commercial_1.apply(lambda row: row['Importe Pedido'] if row['Estado'] == 'Adjudicada' else row['Importe Oferta'], axis=1)

                cur.execute(query_graph_commercial_2)
                results_graph_commercial_2 = cur.fetchall()
                df_graph_commercial_2 = pd.DataFrame(results_graph_commercial_2, columns=['Nº Oferta', 'Estado', 'Responsable', 'Tabla'])

                cur.execute(query_graph_calculation_1)
                results_graph_calculation_1 = cur.fetchall()
                df_graph_calculation_1 = pd.DataFrame(results_graph_calculation_1, columns=['Nº Oferta', 'Estado', 'Responsable', 'Importe Oferta', 'Importe Pedido'])

                df_graph_calculation_1['Importe Oferta'] = df_graph_calculation_1['Importe Oferta']\
                                            .str.replace('€', '', regex=False) \
                                            .str.replace('.', '', regex=False) \
                                            .str.replace(',', '.', regex=False) \
                                            .astype(float)

                df_graph_calculation_1['Importe Pedido'] = df_graph_calculation_1['Importe Pedido']\
                                            .str.replace('€', '', regex=False) \
                                            .str.replace('.', '', regex=False) \
                                            .str.replace(',', '.', regex=False) \
                                            .astype(float)

                df_graph_calculation_1['Importe Final'] = df_graph_calculation_1.apply(lambda row: row['Importe Pedido'] if row['Estado'] == 'Adjudicada' else row['Importe Oferta'], axis=1)

                cur.execute(query_graph_calculation_2)
                results_graph_calculation_2 = cur.fetchall()
                df_graph_calculation_2 = pd.DataFrame(results_graph_calculation_2, columns=['Nº Oferta', 'Estado', 'Responsable', 'Tabla'])

                df_graph_orders_1 = df_graph_commercial_1.dropna(subset=['Nº Pedido'])

                cur.execute(query_last_weekly_summary, (start_date, end_date))
                results_weekly = cur.fetchall()
                df_weekly = pd.DataFrame(results_weekly,
                columns=['Nº Oferta', 'Estado', 'Responsable', 'Cálculos', 'Cliente', 'Cl. Final',
                'Fecha Rec.', 'Fecha Pres.', 'Fecha Vto.',
                'Prob.', 'Prior.', 'Material', 'Nº Eqs.', 'Importe', 'Acciones', 'Tabla']
                )

                df_weekly['Importe Euros'] = df_weekly['Importe']\
                                            .str.replace('€', '', regex=False) \
                                            .str.replace('.', '', regex=False) \
                                            .str.replace(',', '.', regex=False) \
                                            .astype(float)

                cur.execute(query_active_summary)
                results_active = cur.fetchall()
                df_active = pd.DataFrame(results_active, columns=['Nº Oferta', 'Estado', 'Responsable', 'Cálculos', 'Cliente', 'Cl. Final',
                'Fecha Rec.', 'Fecha Pres.', 'Fecha Vto.',
                'Prob.', 'Prior.', 'Material', 'Nº Eqs.', 'Importe', 'Acciones']
                )

                df_active['Importe Euros'] = df_active['Importe']\
                                            .str.replace('€', '', regex=False) \
                                            .str.replace('.', '', regex=False) \
                                            .str.replace(',', '.', regex=False) \
                                            .astype(float)
                
                cur.execute(query_active_budgetary_summary)
                results_active_budgetary = cur.fetchall()
                df_active_budgetary = pd.DataFrame(results_active_budgetary, columns=['Nº Oferta', 'Estado', 'Responsable', 'Cálculos', 'Cliente', 'Cl. Final',
                'Fecha Rec.', 'Fecha Pres.', 'Fecha Vto.',
                'Prob.', 'Prior.', 'Material', 'Nº Eqs.', 'Importe', 'Acciones']
                )

                df_active_budgetary['Importe Euros'] = df_active_budgetary['Importe']\
                                            .str.replace('€', '', regex=False) \
                                            .str.replace('.', '', regex=False) \
                                            .str.replace(',', '.', regex=False) \
                                            .astype(float)

        pdf = generate_report_offers(start_date, end_date,
                                    df_graph_commercial_1, df_graph_commercial_2, df_graph_calculation_1, df_graph_calculation_2, df_graph_orders_1,
                                    df_weekly, df_active, df_active_budgetary)

        output_path, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Guardar PDF", "", "Archivos PDF (*.pdf)")
        if output_path:
            if not output_path.lower().endswith(".pdf"):
                output_path += ".pdf"
            pdf.output(output_path)

def report_orders():
    query_orders = (r"""
                SELECT p.num_order, o.responsible, o.client, o.final_client, o.material, p.items_number, p.order_date, p.expected_date,
                p.material_available, p.recep_date_workshop, p.porc_workshop, p.expected_date_workshop, p.porc_assembly, p.expected_date_assembly, p.percent_sent_workshop,
                COALESCE(
                    CAST(
                        NULLIF(
                            REGEXP_REPLACE(o.delivery_time, '.*?(\d+)[^\d]+(\d+).*', '\2'), -- take second number
                            ''
                        ) AS INTEGER
                    ),
                    0
                ) AS deliv_time_num,
                p.porc_deliveries, p.last_date_deliveries, p.regularisation, p.notes, p.notes_technical, p.order_amount, p.closed,
                pt.variable, p.total_charged
                FROM orders as p
                LEFT JOIN offers as o ON p.num_offer = o.num_offer
                LEFT JOIN product_type as pt ON o.material = pt.material
                WHERE p.total_charged <> 'OK' OR p.total_charged IS NULL""")

    query_docs = ("""
                SELECT 
                num_order,
                COUNT(num_doc_eipsa) AS total_docs,
                SUM(CASE WHEN state IS NULL OR state = '' THEN 1 ELSE 0 END) AS count_no_sent,
                SUM(CASE WHEN state = 'Enviado' THEN 1 ELSE 0 END) AS count_sent,
                SUM(CASE WHEN state LIKE 'Com%' THEN 1 ELSE 0 END) AS count_comment,
                SUM(CASE WHEN state LIKE 'Eli%' THEN 1 ELSE 0 END) AS count_deleted,
                SUM(CASE WHEN state LIKE 'Ap%' THEN 1 ELSE 0 END) AS count_approved,
                COALESCE(
                    TO_CHAR(MIN(CASE WHEN doc_type_id IN (1, 16) THEN TO_DATE(date_first_rev, 'DD/MM/YYYY') END), 'DD/MM/YYYY'),
                    ''
                ) AS min_date_sent_drawings,
                COALESCE(
                    TO_CHAR(MAX(CASE WHEN state = 'Aprobado' AND doc_type_id IN (1, 16) THEN TO_DATE(state_date, 'DD/MM/YYYY') END), 'DD/MM/YYYY'),
                    ''
                ) AS max_date_approved_drawings,
                COALESCE(
                    TO_CHAR(MIN(CASE WHEN doc_type_id = 6 THEN TO_DATE(date_first_rev, 'DD/MM/YYYY') END), 'DD/MM/YYYY'),
                    ''
                ) AS min_date_sent_dossier,
                COALESCE(
                    TO_CHAR(MAX(CASE WHEN state = 'Aprobado' AND doc_type_id = 6 THEN TO_DATE(state_date, 'DD/MM/YYYY') END), 'DD/MM/YYYY'),
                    ''
                ) AS max_date_approved_dossier
            FROM documentation
            GROUP BY num_order
            """)

    query_tags_fab = ("""
            SELECT num_order, MAX(date_final_fab) AS max_date_fab FROM (
            SELECT num_order, final_verif_dim_date AS date_final_fab FROM tags_data.tags_flow

            UNION ALL

            SELECT num_order, final_verif_dim_date AS date_final_fab FROM tags_data.tags_temp

            UNION ALL

            SELECT num_order, final_verif_dim_date AS date_final_fab FROM tags_data.tags_level

            UNION ALL

            SELECT num_order, final_verif_dim_date AS date_final_fab FROM tags_data.tags_others
            ) AS combined
            GROUP BY num_order
            HAVING COUNT(*) = COUNT(date_final_fab)
            """)

    query_tags_count = ("""
            SELECT num_order, COUNT(num_order) AS items_order, COUNT(final_verif_dim_date) AS items_verified FROM (
            SELECT num_order, final_verif_dim_date FROM tags_data.tags_flow WHERE dim_drawing IS NOT NULL

            UNION ALL

            SELECT num_order, final_verif_dim_date FROM tags_data.tags_temp WHERE dim_drawing IS NOT NULL

            UNION ALL

            SELECT num_order, final_verif_dim_date FROM tags_data.tags_level WHERE dim_drawing IS NOT NULL

            UNION ALL

            SELECT num_order, final_verif_dim_date FROM tags_data.tags_others WHERE dim_drawing IS NOT NULL
            ) AS combined
            GROUP BY num_order
            """)

    query_tags_fact = ("""
        SELECT 
            num_order,
            SUM(amount_fact * COALESCE(percent_invoiced, 0) / 100.0) AS total_fact,
            SUM(amount_fact) as total_order_fact
        FROM (
            SELECT num_order, amount_fact::numeric, percent_invoiced FROM tags_data.tags_flow
            UNION ALL
            SELECT num_order, amount_fact::numeric, percent_invoiced FROM tags_data.tags_temp
            UNION ALL
            SELECT num_order, amount_fact::numeric, percent_invoiced FROM tags_data.tags_level
            UNION ALL
            SELECT num_order, amount_fact::numeric, percent_invoiced FROM tags_data.tags_others
        ) AS combined
        GROUP BY num_order
    """)

    query_tags_charged = ("""
            SELECT combined.num_order, SUM(combined.percent_amount_fact) AS total_charged
            FROM (
                SELECT t.num_order, (t.amount_fact::numeric * COALESCE(t.percent_invoiced, 0) / 100.0) AS percent_amount_fact
                FROM tags_data.tags_flow AS t
                LEFT JOIN purch_fact.invoice_header AS i
                ON t.invoice_number = i.num_invoice
                WHERE t.invoice_number IS NOT NULL and i.pay_date IS NOT NULL

                UNION ALL

                SELECT t.num_order, (t.amount_fact::numeric * COALESCE(t.percent_invoiced, 0) / 100.0) AS percent_amount_fact
                FROM tags_data.tags_temp AS t
                LEFT JOIN purch_fact.invoice_header AS i
                ON t.invoice_number = i.num_invoice
                WHERE t.invoice_number IS NOT NULL and i.pay_date IS NOT NULL

                UNION ALL

                SELECT t.num_order, (t.amount_fact::numeric * COALESCE(t.percent_invoiced, 0) / 100.0) AS percent_amount_fact
                FROM tags_data.tags_level AS t
                LEFT JOIN purch_fact.invoice_header AS i
                ON t.invoice_number = i.num_invoice
                WHERE t.invoice_number IS NOT NULL and i.pay_date IS NOT NULL

                UNION ALL

                SELECT t.num_order, (t.amount_fact::numeric * COALESCE(t.percent_invoiced, 0) / 100.0) AS percent_amount_fact
                FROM tags_data.tags_others AS t
                LEFT JOIN purch_fact.invoice_header AS i
                ON t.invoice_number = i.num_invoice
                WHERE t.invoice_number IS NOT NULL and i.pay_date IS NOT NULL
            ) AS combined
            GROUP BY combined.num_order
            """)

    query_ppi = ("""
            SELECT orders.num_order, TO_CHAR(ppi.verif_ppi_date, 'DD/MM/YYYY') as verif_ppi_date
            FROM orders
            LEFT JOIN verification.ppi_verification AS ppi ON orders.num_order = ppi.num_order
            """)

    final_query_1 = (f"""
        SELECT *
        FROM (
            SELECT query1."num_order", query1."responsible", query1."client", query1."final_client", query1."material", query1."items_number",
                TO_CHAR(query1."order_date", 'DD/MM/YYYY') AS order_date,
                TO_CHAR(query1."expected_date", 'DD/MM/YYYY') AS expected_date,
                query3."total_docs", query3."count_no_sent", query3."count_sent", query3."count_comment", query3."count_deleted", query3."count_approved",
                query3."min_date_sent_drawings",
                query3."max_date_approved_drawings",
                query1."recep_date_workshop", query1."percent_sent_workshop",
                CASE 
                    WHEN query3."max_date_approved_drawings" IS NULL OR query3."max_date_approved_drawings" = '' THEN
                        TO_CHAR(query1."expected_date", 'DD/MM/YYYY')
                    ELSE 
                        TO_CHAR((
                            WITH fechas_validas AS (
                                SELECT d::date
                                FROM generate_series(
                                    TO_DATE(query3."max_date_approved_drawings", 'DD/MM/YYYY'),
                                    TO_DATE(query3."max_date_approved_drawings", 'DD/MM/YYYY') + INTERVAL '1 year',
                                    INTERVAL '1 day'
                                ) AS d
                                WHERE EXTRACT(MONTH FROM d) <> 8  -- excluir agosto
                                ORDER BY d
                            )
                            SELECT d
                            FROM fechas_validas
                            OFFSET GREATEST(COALESCE(query1."deliv_time_num", 0) * 7 - 1, 0)
                            LIMIT 1
                        ), 'DD/MM/YYYY')
                END AS new_contractual_date,
                query1."material_available", 
                query1."porc_workshop", query1."expected_date_workshop", query1."porc_assembly", query1."expected_date_assembly",
                (query5.items_verified::numeric / NULLIF(query5.items_order::numeric, 0) * 100)::numeric(10,0) AS percent_items_verified,
                TO_CHAR(query4."max_date_fab", 'DD/MM/YYYY') AS max_date_verif,
                query3."min_date_sent_dossier",
                query3."max_date_approved_dossier",
                query1."porc_deliveries", query1."last_date_deliveries",
                (query6.total_fact::numeric / NULLIF(query6.total_order_fact::numeric, 0) * 100)::numeric(10,2) AS fact_percent,
                (query7.total_charged::numeric / NULLIF(query6.total_order_fact::numeric, 0) * 100)::numeric(10,2) AS charged_percent,
                query1."regularisation", query1."notes", query1."notes_technical",
                '' as pending_to_charged,
                query1."order_amount",
                query1."variable", query8."verif_ppi_date", query1."total_charged", NULLIF(query6."total_fact"::numeric, 0), NULLIF(query7."total_charged"::numeric, 0)
            FROM ({query_orders}) AS query1
            LEFT JOIN ({query_docs}) AS query3 ON query1."num_order" = query3."num_order"
            LEFT JOIN ({query_tags_fab}) AS query4 ON query1."num_order" = query4."num_order"
            LEFT JOIN ({query_tags_count}) AS query5 ON query1."num_order" = query5."num_order"
            LEFT JOIN ({query_tags_fact}) AS query6 ON query1."num_order" = query6."num_order"
            LEFT JOIN ({query_tags_charged}) AS query7 ON query1."num_order" = query7."num_order"
            LEFT JOIN ({query_ppi}) AS query8 ON query1."num_order" = query8."num_order"
        ) AS final
        
        ORDER BY final."num_order" ASC
    """)

    columns_1 = ['PEDIDO', 'RESPONSABLE', 'CLIENTE', 'CLIENTE FINAL', 'MATERIAL', 'Nº EQUIPOS',
                'FECHA PO', 'FECHA CONT.',
                'DOCS TOTALES', 'DOCS NO ENV.', 'DOCS ENV.', 'DOCS COM.', 'DOCS ELIM.', 'DOCS AP.', 
                'FECHA ENV PLANOS', 'FECHA AP PLANOS',
                'FECHA ENV FAB.', '% ENV FAB',
                'NUEVA FECHA CONT.',
                'MAT. DISP.', '% FAB', 'PREV. FAB', '% MONT','PREV. MONT.',
                '% VERIF.',
                'FECHA FINAL VERIF.',
                'FECHA ENV DOSSIER', 'FECHA AP DOSSIER',
                '% ENV.', 'FECHA ENVÍO',
                '% FACT.',
                '% COBRADO',
                'ORDENES CAMBIO', 'NOTAS', 'NOTAS TÉCNICAS',
                'PTE. COBRAR', 'IMPORTE',
                'VARIABLE', 'PPI', 'NOTAS FACT_COB', 'TOTAL FACT', 'TOTAL COB']

    columns_2 = ['VARIABLE', 'Nº PEDIDOS', 'IMPORTE TOTAL', '% FACT.', '% COBRADO', 'PTE FACTURAR']

    with Database_Connection(config()) as conn:
        with conn.cursor() as cur:
            cur.execute(final_query_1)
            results_1 = cur.fetchall()

        df_orders = pd.DataFrame(results_1, columns=columns_1)
        cols= ['DOCS TOTALES', 'DOCS NO ENV.', 'DOCS ENV.', 'DOCS COM.', 'DOCS ELIM.', 'DOCS AP.']
        df_orders[cols] = df_orders[cols].fillna('N/A')
        df_orders = df_orders.fillna('')
        df_orders.replace('None', '')

        df_orders['IMPORTE'] = (
            df_orders['IMPORTE']
            .str.replace('€', '', regex=False)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )

        df_orders['IMPORTE'] = df_orders['IMPORTE'].astype(float)

        df_orders['% ENV.'] = df_orders.apply(lambda row: 100 if 'R' in row['PEDIDO'] else row['% ENV.'],axis=1)
        df_orders['FECHA ENVÍO'] = df_orders.apply(lambda row: row['FECHA CONT.'] if 'R' in row['PEDIDO'] else row['FECHA ENVÍO'], axis=1)

        df_orders['% VERIF.'] = df_orders.apply(lambda row: row['Nº EQUIPOS'] if row['% VERIF.']== '' else row['% VERIF.'], axis=1)
        df_orders['FECHA FINAL VERIF.'] = df_orders.apply(lambda row: row['PPI'] if row['FECHA FINAL VERIF.'] == '' else row['FECHA FINAL VERIF.'], axis=1)

        df_orders['% FACT.'] = df_orders.apply(lambda row: (float(row['NOTAS FACT_COB'].split(" / ")[0].replace(',','.')) if ("/" in row['NOTAS FACT_COB']) else row['% FACT.']), axis=1)
        df_orders['% COBRADO'] = df_orders.apply(lambda row: (float(row['NOTAS FACT_COB'].split(" / ")[1].replace(',','.')) if ("/" in row['NOTAS FACT_COB']) else row['% COBRADO']), axis=1)

        df_orders['PTE. COBRAR'] = df_orders.apply(
                                    lambda row: (
                                        (float(row['IMPORTE']) * (100 - float(row['% COBRADO'])) / 100) if "/" in row['NOTAS FACT_COB'] and row['% FACT.'] not in ['','0',0] else
                                        ((float(row['IMPORTE']) * float(row['% FACT.']) / 100) if row['% COBRADO'] in ['','0',0] and row['% FACT.'] not in ['','0',0] else
                                        (float(row['TOTAL FACT'] or 0) - float(row['TOTAL COB'] or 0)))),
                                    axis=1)

        df_orders=df_orders[df_orders['% COBRADO'] != 100]

        df_orders_P = df_orders[(df_orders['PEDIDO'].str.startswith('P-')) & (~df_orders['PEDIDO'].str.startswith('PA')) & (~df_orders['PEDIDO'].str.endswith('R')) & (df_orders['% ENV.'] != 100)]

        cols_PA = ['PEDIDO', 'RESPONSABLE', 'CLIENTE', 'CLIENTE FINAL', 'MATERIAL', 'Nº EQUIPOS',
                'FECHA PO', 'FECHA CONT.', '% MONT','PREV. MONT.', '% VERIF.', 'FECHA FINAL VERIF.',
                '% ENV.', 'FECHA ENVÍO', '% FACT.', '% COBRADO', 'NOTAS', 'NOTAS TÉCNICAS', 'PTE. COBRAR', 'IMPORTE']

        cols_sent = ['PEDIDO', 'RESPONSABLE', 'CLIENTE', 'CLIENTE FINAL', 'MATERIAL', 'Nº EQUIPOS',
                'FECHA PO', 'FECHA CONT.', '% ENV.', 'FECHA ENVÍO',
                '% FACT.', '% COBRADO', 'NOTAS', 'NOTAS TÉCNICAS', 'PTE. COBRAR', 'IMPORTE']

        cols_R = ['PEDIDO', 'RESPONSABLE', 'CLIENTE', 'CLIENTE FINAL', 'MATERIAL', 'Nº EQUIPOS',
                'FECHA PO', 'FECHA CONT.', '% ENV.', 'FECHA ENVÍO',
                '% FACT.', '% COBRADO', 'NOTAS', 'NOTAS TÉCNICAS', 'PTE. COBRAR', 'IMPORTE']

        df_orders_PA = df_orders[df_orders['PEDIDO'].str.startswith('PA') & (df_orders['% ENV.'] != 100)][cols_PA]
        df_orders_sent = df_orders[(df_orders['% ENV.'] == 100) & (~df_orders['PEDIDO'].str.endswith('R'))][cols_sent]
        df_orders_R = df_orders[df_orders['PEDIDO'].str.endswith('R')][cols_R]

        df_orders_summary = df_orders.copy()

        df_orders_summary['% FACT.'] = pd.to_numeric(df_orders_summary['% FACT.'], errors='coerce').fillna(0)
        df_orders_summary['% COBRADO'] = pd.to_numeric(df_orders_summary['% COBRADO'], errors='coerce').fillna(0)

        df_orders_summary['IMPORTE FACTURADO'] = df_orders_summary['IMPORTE'] * (df_orders_summary['% FACT.'] / 100)
        df_orders_summary['IMPORTE COBRADO'] = df_orders_summary['IMPORTE'] * (df_orders_summary['% COBRADO'] / 100)

        summary = df_orders_summary.groupby('VARIABLE').agg(
            **{
                'Nº PEDIDOS': ('PEDIDO', 'count'),
                'IMPORTE TOTAL': ('IMPORTE', 'sum'),
                'IMPORTE FACTURADO': ('IMPORTE FACTURADO', 'sum'),
                'IMPORTE COBRADO': ('IMPORTE COBRADO', 'sum'),
            }
        ).reset_index()

        summary['% FACT.'] = (summary['IMPORTE FACTURADO'] / summary['IMPORTE TOTAL'] * 100).round(2)
        summary['% COBRADO'] = (summary['IMPORTE COBRADO'] / summary['IMPORTE TOTAL'] * 100).round(2)
        summary['PTE FACTURAR'] = (summary['IMPORTE TOTAL'] - summary['IMPORTE FACTURADO']).round(2)

        df_orders_summary = summary[columns_2]

        df_wallet = pd.read_excel(DATA_PATH / r'Ana\CP\informe_estructurado.xlsx')

        order_reports(df_orders_P, df_orders_PA, df_orders_sent, df_orders_R, df_orders_summary, df_wallet)

def report_projects():
    query_projects = (f"""
                    SELECT * FROM future_projects
                    """)
    
    columns = ["ID", "Award Date - Quarter", "End User", "Contractor", "Project Name", 
                "Scope", "Country", "Contract Value (MM€)", "EIPSA Portion (MM€)",
                "Contract Duration (months)", "Stage", "Award Date", "GO (%)", "GET (%)", "EIPSA Products", "Actions", "Contacto EPC", "Datos Contacto"]
    
    with Database_Connection(config()) as conn:
        with conn.cursor() as cur:
            cur.execute(query_projects)
            results = cur.fetchall()

        df = pd.DataFrame(results, columns=columns)
        df = df.fillna('')
        df.replace('None', '')

        final_df = df.iloc[:, 1:]

    future_projects(final_df)

def generate_report_offers(start_date, end_date, df_graph_commercial_1, df_graph_commercial_2, df_graph_calculation_1, df_graph_calculation_2, df_graph_orders_1, df_weekly, df_active, df_active_budgetary):
    pdf = CustomPDF_A3('P')

    pdf.add_font('DejaVuSansCondensed', '', str(get_path("Resources", "Iconos", "DejaVuSansCondensed.ttf")))
    pdf.add_font('DejaVuSansCondensed-Bold', '', str(get_path("Resources", "Iconos", "DejaVuSansCondensed-Bold.ttf")))

    pdf.set_auto_page_break(auto=True)
    pdf.set_margins(0.5, 0.5)

    pdf.set_fill_color(3, 174, 236)

    pdf.add_page()

    pdf.image(str(get_path("Resources", "Iconos", "Eipsa Logo Blanco.png")), 1, 0.8, 7, 2)
    pdf.ln(3)

    pdf.set_font('Helvetica', 'B', size=6)
    y_position = 0.5
    pdf.set_xy(12.55, y_position)
    pdf.fixed_height_multicell(3.5, 0.6, 'TOTAL IMPORTE REGISTRADO ' + str(datetime.today().year), fill=True)
    pdf.set_xy(16.05, y_position)
    pdf.cell(0.4, 0.6,'')
    pdf.fixed_height_multicell(4, 0.6, 'TOTAL IMPORTE OFERTADO ' + str(datetime.today().year), fill=True)
    pdf.set_xy(20.45, y_position)
    pdf.cell(0.4, 0.6,'')
    pdf.fixed_height_multicell(4, 0.6, 'TOTAL IMPORTE BUDGETARY ' + str(datetime.today().year), fill=True)
    pdf.set_xy(24.85, y_position)
    pdf.cell(0.4, 0.6, '')
    pdf.fixed_height_multicell(4, 0.6, 'TOTAL IMPORTE ADJUDICADO ' + str(datetime.today().year), fill=True)

    received_amount = df_graph_commercial_1['Importe Oferta'].sum()
    offered_amount = df_graph_commercial_1[~df_graph_commercial_1['Nº Oferta'].str.contains('B-', na=False)]['Importe Oferta'].sum()
    budgetary_amount = df_graph_commercial_1[df_graph_commercial_1['Nº Oferta'].str.contains('B-', na=False)]['Importe Oferta'].sum()
    order_amount = df_graph_commercial_1[df_graph_commercial_1['Estado'] == 'Adjudicada']['Importe Final'].sum()

    pdf.set_font('DejaVuSansCondensed-Bold','', size=6)
    y_position = 1.1
    pdf.set_xy(12.55, y_position)
    pdf.fixed_height_multicell(3.5, 0.3, euro_format(received_amount), fill=False)
    pdf.set_xy(16.05, y_position)
    pdf.cell(0.4, 0.6,'')
    pdf.fixed_height_multicell(4, 0.3, euro_format(offered_amount) + " / " + f"{(offered_amount/received_amount):.1%}", fill=False)
    pdf.set_xy(20.45, y_position)
    pdf.cell(0.4, 0.3, '')
    pdf.fixed_height_multicell(4, 0.3, euro_format(budgetary_amount) + " / " + f"{(budgetary_amount/received_amount):.1%}", fill=False)
    pdf.set_xy(24.85, y_position)
    pdf.cell(0.4, 0.3, '')
    pdf.fixed_height_multicell(4, 0.3, euro_format(order_amount) + " / " + f"{(order_amount/offered_amount):.1%}", fill=False)

    pdf.set_font('Helvetica', 'B', size=6)
    y_position = 1.6
    pdf.set_xy(12.55, y_position)
    pdf.fixed_height_multicell(3.5, 0.6, 'TOTAL OFERTAS REGISTRADAS ' + str(datetime.today().year), fill=True)
    pdf.set_xy(16.05, y_position)
    pdf.cell(0.4, 0.6, '')
    pdf.fixed_height_multicell(4, 0.6, 'TOTAL OFERTAS REALIZADAS ' + str(datetime.today().year), fill=True)
    pdf.set_xy(20.45, y_position)
    pdf.cell(0.4, 0.6, '')
    pdf.fixed_height_multicell(4, 0.6, 'TOTAL BUDGETARIES\n' + str(datetime.today().year), fill=True)
    pdf.set_xy(24.85, y_position)
    pdf.cell(0.4, 0.6, '')
    pdf.fixed_height_multicell(4, 0.6, 'TOTAL OFERTAS ADJUDICADAS ' + str(datetime.today().year), fill=True)
    pdf.set_xy(26.4, y_position)

    received_count = df_graph_commercial_2.shape[0]
    offered_count = df_graph_commercial_2[~df_graph_commercial_2['Nº Oferta'].str.contains('B-', na=False)].shape[0]
    budgetary_count = df_graph_commercial_2[df_graph_commercial_2['Nº Oferta'].str.contains('B-', na=False)].shape[0]
    order_count = df_graph_commercial_2[df_graph_commercial_2['Estado'] == 'Adjudicada'].shape[0]

    pdf.set_font('DejaVuSansCondensed-Bold','', size=6)
    y_position = 2.2
    pdf.set_xy(12.55, y_position)
    pdf.fixed_height_multicell(3.5, 0.3, str(received_count), fill=False)
    pdf.set_xy(16.05, y_position)
    pdf.cell(0.4, 0.3, '')
    pdf.fixed_height_multicell(4, 0.3, str(offered_count) + " / " + f"{(offered_count/received_count):.1%}", fill=False)
    pdf.set_xy(20.45, y_position)
    pdf.cell(0.4, 0.3, '')
    pdf.fixed_height_multicell(4, 0.3, str(budgetary_count) + " / " + f"{(budgetary_count/received_count):.1%}", fill=False)
    pdf.set_xy(24.85, y_position)
    pdf.cell(0.4, 0.3, '')
    pdf.fixed_height_multicell(4, 0.3, str(order_count) + " / " + f"{(order_count/offered_count):.1%}", fill=False)

    df_graph_commercial_1 = df_graph_commercial_1[df_graph_commercial_1['Estado'] != 'Budgetary']
    img_graph_1, img_graph_2 = graphs_commercial_report(df_graph_commercial_1, df_graph_commercial_2)
    img_graph_3, img_graph_4 = graphs_calculation_report(df_graph_calculation_1, df_graph_calculation_2)
    img_graph_5, img_graph_6 = graphs_orders_report(df_graph_orders_1)

    y_position = 3
    pdf.image(img_graph_1, x=0.5, y=y_position, w=8.5, h=4.5)
    pdf.image(img_graph_3, x=10.6, y=y_position, w=8.5, h=4.5)
    pdf.image(img_graph_5, x=20.7, y=y_position, w=8.5, h=4.5)
    pdf.ln(5)

    y_position = pdf.get_y()
    pdf.image(img_graph_2, x=0.5, y=y_position, w=8.5, h=4.5)
    pdf.image(img_graph_4, x=10.6, y=y_position, w=8.5, h=4.5)
    pdf.image(img_graph_6, x=20.7, y=y_position, w=8.5, h=4.5)
    pdf.ln(5)

    pdf.set_fill_color(255, 255, 64)
    pdf.set_font('Helvetica', 'B', size=7)
    pdf.cell(19.75, 0.5, 'RESUMEN SEMANAL', fill=True)
    pdf.cell(3, 0.5, (start_date.strftime('%d/%m/%Y')), fill=True, align='C')
    pdf.cell(3, 0.5, '-', fill=True, align='C')
    pdf.cell(3, 0.5, (end_date.strftime('%d/%m/%Y')), fill=True, align='C')
    pdf.ln(0.5)

    pdf.set_fill_color(3, 174, 236)
    pdf.cell(3, 0.5, 'REGISTRADAS:')
    pdf.cell(3, 0.5, str(df_weekly.shape[0]), align='L')
    pdf.cell(1.5, 0.5, '')
    pdf.cell(3, 0.5, 'EN ESTUDIO:')
    pdf.cell(3, 0.5, str(df_weekly[df_weekly['Estado'] == 'En Estudio'].shape[0]), align='L')
    pdf.cell(1.5, 0.5, '')
    pdf.cell(3, 0.5, 'REALIZADAS:')
    pdf.cell(3, 0.5, str(df_weekly[~df_weekly['Estado'].isin(['Registrada', 'En Estudio'])].shape[0]), align='L')
    pdf.cell(1.5, 0.5, '')
    pdf.cell(3, 0.5, 'ADJUDICADAS:')
    pdf.cell(3, 0.5, str(df_weekly[df_weekly['Estado'] == 'Adjudicada'].shape[0]), align='L')
    pdf.ln(0.5)

    pdf.cell(1.5, 0.3, 'OFERTA', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'ESTADO', fill=True, border=1, align='C')
    pdf.cell(2, 0.3, 'RESP.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'CALC.', fill=True, border=1, align='C')
    pdf.cell(3, 0.3, 'CLIENTE', fill=True, border=1, align='C')
    pdf.cell(3.5, 0.3, 'CLIENTE FINAL', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. REC.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. PRES.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. VTO.', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'PROB.', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'PRIOR.', fill=True, border=1, align='C')
    pdf.cell(2.75, 0.3, 'MATERIAL', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'Nº EQ.', fill=True, border=1, align='C')
    pdf.cell(2.2, 0.3, 'IMPORTE', fill=True, border=1, align='C')
    pdf.cell(3.25, 0.3, 'ACCIONES', fill=True, border=1, align='C')
    pdf.ln()

    pdf.set_font('DejaVuSansCondensed', size=6)
    df_weekly.sort_values(by=['Nº Oferta'], inplace=True)
    for _, row in df_weekly.iterrows():
        # getting the required height of the row
        line_h = pdf.font_size * 1.5
        h_client = pdf.get_multicell_height(2.75, line_h, '' if row['Cliente'] is None else str(row['Cliente']))
        h_clfinal = pdf.get_multicell_height(3.25, line_h, '' if row['Cl. Final'] is None else str(row['Cl. Final']))
        h_material = pdf.get_multicell_height(2.5, line_h, '' if row['Material'] is None else str(row['Material']))
        h_actions = pdf.get_multicell_height(3, line_h, '' if row['Acciones'] is None else str(row['Acciones']))

        row_height = max(h_client, h_clfinal, h_material, h_actions, line_h)

        # Setting values for table
        pdf.cell(1.5, row_height, '' if row['Nº Oferta'] is None else str(row['Nº Oferta']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Estado'] is None else str(row['Estado']), border=1, align='C')
        pdf.cell(2, row_height, '' if row['Responsable'] is None else str(row['Responsable']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Cálculos'] is None else str(row['Cálculos']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3, row_height, '' if row['Cliente'] is None else str(row['Cliente']), border=1)
        pdf.set_xy(x + 3, y)

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3.5, row_height, '' if row['Cl. Final'] is None else str(row['Cl. Final']), border=1)
        pdf.set_xy(x + 3.5, y)

        pdf.cell(1.5, row_height, '' if row['Fecha Rec.'] is None else str(row['Fecha Rec.']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Fecha Pres.'] is None else str(row['Fecha Pres.']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Fecha Vto.'] is None else str(row['Fecha Vto.']), border=1, align='C')
        pdf.cell(1, row_height, '' if row['Prob.'] is None else str(row['Prob.']), border=1, align='C')
        pdf.cell(1, row_height, '' if row['Prior.'] is None else str(row['Prior.']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(2.75, row_height, '' if row['Material'] is None else str(row['Material']), border=1)
        pdf.set_xy(x + 2.75, y)

        pdf.cell(1, row_height, '' if row['Nº Eqs.'] is None else str(row['Nº Eqs.']), border=1, align='C')
        pdf.cell(2.2, row_height, '' if row['Importe'] is None else str(row['Importe']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3.25, row_height, '' if row['Acciones'] is None else str(row['Acciones']), border=1)
        pdf.set_xy(x + 2.5, y)

        pdf.ln(row_height)

    pdf.set_font('DejaVuSansCondensed-Bold', size=7)
    pdf.cell(22, 0.3, '')
    pdf.cell(4.25, 0.3, 'TOTAL:', align='R')
    pdf.cell(2.5, 0.3, euro_format(df_weekly['Importe Euros'].sum()), align='C')
    pdf.ln(0.5)

    pdf.set_fill_color(255, 255, 64)
    pdf.cell(28.75, 0.5, 'OFERTAS EN ACTIVO', fill=True)
    pdf.ln(0.5)

    pdf.set_fill_color(3, 174, 236)

    df_registered = df_active[df_active['Estado'] == 'Registrada'].sort_values(by=['Nº Oferta'])
    if df_registered.shape[0] > 0:
        pdf.cell(3, 0.5, 'REGISTRADAS:')
        pdf.cell(3, 0.5, str(df_registered.shape[0]), align='L')
        pdf.ln(0.5)

        pdf.cell(1.5, 0.3, 'OFERTA', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'ESTADO', fill=True, border=1, align='C')
        pdf.cell(2, 0.3, 'RESP.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'CALC.', fill=True, border=1, align='C')
        pdf.cell(3, 0.3, 'CLIENTE', fill=True, border=1, align='C')
        pdf.cell(3.5, 0.3, 'CLIENTE FINAL', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. REC.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. PRES.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. VTO.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PROB.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PRIOR.', fill=True, border=1, align='C')
        pdf.cell(2.75, 0.3, 'MATERIAL', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'Nº EQ.', fill=True, border=1, align='C')
        pdf.cell(2.2, 0.3, 'IMPORTE', fill=True, border=1, align='C')
        pdf.cell(3.25, 0.3, 'ACCIONES', fill=True, border=1, align='C')
        pdf.ln()

        pdf.set_font('DejaVuSansCondensed', size=6)
        for _, row in df_registered.iterrows():
            # getting the required height of the row
            line_h = pdf.font_size * 1.5
            h_client = pdf.get_multicell_height(2.75, line_h, '' if row['Cliente'] is None else str(row['Cliente']))
            h_clfinal = pdf.get_multicell_height(3.25, line_h, '' if row['Cl. Final'] is None else str(row['Cl. Final']))
            h_material = pdf.get_multicell_height(2.5, line_h, '' if row['Material'] is None else str(row['Material']))
            h_actions = pdf.get_multicell_height(3, line_h, '' if row['Acciones'] is None else str(row['Acciones']))

            row_height = max(h_client, h_clfinal, h_material, h_actions, line_h)

            # Setting values for table
            pdf.cell(1.5, row_height, '' if row['Nº Oferta'] is None else str(row['Nº Oferta']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Estado'] is None else str(row['Estado']), border=1, align='C')
            pdf.cell(2, row_height, '' if row['Responsable'] is None else str(row['Responsable']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Cálculos'] is None else str(row['Cálculos']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3, row_height, '' if row['Cliente'] is None else str(row['Cliente']), border=1)
            pdf.set_xy(x + 3, y)

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.5, row_height, '' if row['Cl. Final'] is None else str(row['Cl. Final']), border=1)
            pdf.set_xy(x + 3.5, y)

            pdf.cell(1.5, row_height, '' if row['Fecha Rec.'] is None else str(row['Fecha Rec.']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Fecha Pres.'] is None else str(row['Fecha Pres.']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Fecha Vto.'] is None else str(row['Fecha Vto.']), border=1, align='C')
            pdf.cell(1, row_height, '' if row['Prob.'] is None else str(row['Prob.']), border=1, align='C')
            pdf.cell(1, row_height, '' if row['Prior.'] is None else str(row['Prior.']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(2.75, row_height, '' if row['Material'] is None else str(row['Material']), border=1)
            pdf.set_xy(x + 2.75, y)

            pdf.cell(1, row_height, '' if row['Nº Eqs.'] is None else str(int(row['Nº Eqs.'])), border=1, align='C')
            pdf.cell(2.2, row_height, '' if row['Importe'] is None else str(row['Importe']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.25, row_height, '' if row['Acciones'] is None else str(row['Acciones']), border=1)
            pdf.set_xy(x + 2.5, y)

            pdf.ln(row_height)

        pdf.set_font('DejaVuSansCondensed-Bold', size=7)
        pdf.cell(20.75, 0.3, '')
        pdf.cell(5, 0.3, 'TOTAL:', align='R')
        pdf.cell(3, 0.3, euro_format(df_registered['Importe Euros'].sum()), align='C')
        pdf.ln()

    df_study = df_active[df_active['Estado'] == 'En Estudio'].sort_values(by=['Nº Oferta'])
    if df_study.shape[0] > 0:
        df_study['Fecha Vto.'] = pd.to_datetime(df_study['Fecha Vto.'], format='%d/%m/%Y', errors='coerce')
        df_study['days_diff'] = (pd.Timestamp.today() - df_study['Fecha Vto.']).dt.days
        df_study['Fecha Vto.'] = df_study['Fecha Vto.'].dt.strftime('%d/%m/%Y')

        pdf.set_font('Helvetica', 'B', size=7)
        pdf.cell(3, 0.5, 'EN ESTUDIO:')
        pdf.cell(3, 0.5, str(df_study.shape[0]), align='L')
        pdf.ln(0.5)

        pdf.cell(1.5, 0.3, 'OFERTA', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'ESTADO', fill=True, border=1, align='C')
        pdf.cell(2, 0.3, 'RESP.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'CALC.', fill=True, border=1, align='C')
        pdf.cell(3, 0.3, 'CLIENTE', fill=True, border=1, align='C')
        pdf.cell(3.5, 0.3, 'CLIENTE FINAL', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. REC.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. PRES.', fill=True, border=1, align='C')
        pdf.cell(1.5, 0.3, 'F. VTO.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PROB.', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'PRIOR.', fill=True, border=1, align='C')
        pdf.cell(2.75, 0.3, 'MATERIAL', fill=True, border=1, align='C')
        pdf.cell(1, 0.3, 'Nº EQ.', fill=True, border=1, align='C')
        pdf.cell(2.2, 0.3, 'IMPORTE', fill=True, border=1, align='C')
        pdf.cell(3.25, 0.3, 'ACCIONES', fill=True, border=1, align='C')
        pdf.ln()

        pdf.set_fill_color(255, 105, 105)
        pdf.set_font('DejaVuSansCondensed', size=6)
        for _, row in df_study.iterrows():
            # getting the required height of the row
            line_h = pdf.font_size * 1.5
            h_client = pdf.get_multicell_height(2.75, line_h, '' if row['Cliente'] is None else str(row['Cliente']))
            h_clfinal = pdf.get_multicell_height(3.25, line_h, '' if row['Cl. Final'] is None else str(row['Cl. Final']))
            h_material = pdf.get_multicell_height(2.5, line_h, '' if row['Material'] is None else str(row['Material']))
            h_actions = pdf.get_multicell_height(3, line_h, '' if row['Acciones'] is None else str(row['Acciones']))

            row_height = max(h_client, h_clfinal, h_material, h_actions, line_h)

            # Setting values for table
            pdf.cell(1.5, row_height, '' if row['Nº Oferta'] is None else str(row['Nº Oferta']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Estado'] is None else str(row['Estado']), border=1, align='C')
            pdf.cell(2, row_height, '' if row['Responsable'] is None else str(row['Responsable']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Cálculos'] is None else str(row['Cálculos']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3, row_height, '' if row['Cliente'] is None else str(row['Cliente']), border=1)
            pdf.set_xy(x + 3, y)

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.5, row_height, '' if row['Cl. Final'] is None else str(row['Cl. Final']), border=1)
            pdf.set_xy(x + 3.5, y)

            pdf.cell(1.5, row_height, '' if row['Fecha Rec.'] is None else str(row['Fecha Rec.']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Fecha Pres.'] is None else str(row['Fecha Pres.']), border=1, align='C')
            pdf.cell(1.5, row_height, '' if row['Fecha Vto.'] is None else str(row['Fecha Vto.']), border=1, align='C', fill=True if row['days_diff'] > 0 else False)
            pdf.cell(1, row_height, '' if row['Prob.'] is None else str(row['Prob.']), border=1, align='C')
            pdf.cell(1, row_height, '' if row['Prior.'] is None else str(row['Prior.']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(2.75, row_height, '' if row['Material'] is None else str(row['Material']), border=1)
            pdf.set_xy(x + 2.75, y)

            pdf.cell(1, row_height, '' if row['Nº Eqs.'] is None else str(int(row['Nº Eqs.'])), border=1, align='C')
            pdf.cell(2.2, row_height, '' if row['Importe'] is None else str(row['Importe']), border=1, align='C')

            x = pdf.get_x()
            y = pdf.get_y()
            pdf.fixed_height_multicell(3.25, row_height, '' if row['Acciones'] is None else str(row['Acciones']), border=1)
            pdf.set_xy(x + 2.5, y)

            pdf.ln(row_height)

        pdf.set_font('DejaVuSansCondensed-Bold', size=7)
        pdf.cell(20.75, 0.3, '')
        pdf.cell(5, 0.3, 'TOTAL:', align='R')
        pdf.cell(3, 0.3, euro_format(df_study['Importe Euros'].sum()), align='C')
        pdf.ln()

    df_presented = df_active[df_active['Estado'] == 'Presentada'].sort_values(by=['Fecha Pres.'])

    df_presented['Fecha Pres.'] = pd.to_datetime(df_presented['Fecha Pres.'], format='%d/%m/%Y', errors='coerce')
    df_presented.sort_values(by=['Nº Oferta'], inplace=True)

    df_presented['days_diff'] = (pd.Timestamp.today() - df_presented['Fecha Pres.']).dt.days

    df_less_30 = df_presented[df_presented['days_diff'] <= 30].copy()
    df_more_30 = df_presented[df_presented['days_diff'] > 30].copy()

    df_less_30['Fecha Pres.'] = df_less_30['Fecha Pres.'].dt.strftime('%d/%m/%Y')
    df_more_30['Fecha Pres.'] = df_more_30['Fecha Pres.'].dt.strftime('%d/%m/%Y')

    pdf.set_fill_color(3, 174, 236)
    pdf.set_font('Helvetica', 'B', size=7)
    pdf.cell(3, 0.5, 'PRESENTADAS:')
    pdf.ln(0.5)

    df_presented['Fecha Pres.'] = pd.to_datetime(df_presented['Fecha Pres.'], errors='coerce', dayfirst=True)

    pdf.cell(1.5, 0.3, 'OFERTA', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'ESTADO', fill=True, border=1, align='C')
    pdf.cell(2, 0.3, 'RESP.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'CALC.', fill=True, border=1, align='C')
    pdf.cell(3, 0.3, 'CLIENTE', fill=True, border=1, align='C')
    pdf.cell(3.5, 0.3, 'CLIENTE FINAL', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. REC.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. PRES.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. VTO.', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'PROB.', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'PRIOR.', fill=True, border=1, align='C')
    pdf.cell(2.75, 0.3, 'MATERIAL', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'Nº EQ.', fill=True, border=1, align='C')
    pdf.cell(2.2, 0.3, 'IMPORTE', fill=True, border=1, align='C')
    pdf.cell(3.25, 0.3, 'ACCIONES', fill=True, border=1, align='C')
    pdf.ln()

    pdf.set_font('DejaVuSansCondensed', size=6)
    for _, row in df_less_30.iterrows():
        # getting the required height of the row
        line_h = pdf.font_size * 1.5
        h_client = pdf.get_multicell_height(2.75, line_h, '' if row['Cliente'] is None else str(row['Cliente']))
        h_clfinal = pdf.get_multicell_height(3.25, line_h, '' if row['Cl. Final'] is None else str(row['Cl. Final']))
        h_material = pdf.get_multicell_height(2.5, line_h, '' if row['Material'] is None else str(row['Material']))
        h_actions = pdf.get_multicell_height(3, line_h, '' if row['Acciones'] is None else str(row['Acciones']))

        row_height = max(h_client, h_clfinal, h_material, h_actions, line_h)

        # Setting values for table
        pdf.cell(1.5, row_height, '' if row['Nº Oferta'] is None else str(row['Nº Oferta']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Estado'] is None else str(row['Estado']), border=1, align='C')
        pdf.cell(2, row_height, '' if row['Responsable'] is None else str(row['Responsable']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Cálculos'] is None else str(row['Cálculos']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3, row_height, '' if row['Cliente'] is None else str(row['Cliente']), border=1)
        pdf.set_xy(x + 3, y)

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3.5, row_height, '' if row['Cl. Final'] is None else str(row['Cl. Final']), border=1)
        pdf.set_xy(x + 3.5, y)

        pdf.cell(1.5, row_height, '' if row['Fecha Rec.'] is None else str(row['Fecha Rec.']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Fecha Pres.'] is None else str(row['Fecha Pres.']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Fecha Vto.'] is None else str(row['Fecha Vto.']), border=1, align='C')
        pdf.cell(1, row_height, '' if row['Prob.'] is None else str(row['Prob.']), border=1, align='C')
        pdf.cell(1, row_height, '' if row['Prior.'] is None else str(row['Prior.']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(2.75, row_height, '' if row['Material'] is None else str(row['Material']), border=1)
        pdf.set_xy(x + 2.75, y)

        pdf.cell(1, row_height, '' if row['Nº Eqs.'] is None else str(int(row['Nº Eqs.'])), border=1, align='C')
        pdf.cell(2.2, row_height, '' if row['Importe'] is None else str(row['Importe']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3.25, row_height, '' if row['Acciones'] is None else str(row['Acciones']), border=1)
        pdf.set_xy(x + 2.5, y)

        pdf.ln(row_height)

    pdf.set_fill_color(3, 174, 236)
    pdf.set_font('DejaVuSansCondensed-Bold', size=7)
    pdf.cell(20.75, 0.3, '')
    pdf.cell(5, 0.3, 'TOTAL:', align='R')
    pdf.cell(3, 0.3, euro_format(df_less_30['Importe Euros'].sum()), align='C')
    pdf.ln()

    pdf.cell(1.5, 0.3, 'OFERTA', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'ESTADO', fill=True, border=1, align='C')
    pdf.cell(2, 0.3, 'RESP.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'CALC.', fill=True, border=1, align='C')
    pdf.cell(3, 0.3, 'CLIENTE', fill=True, border=1, align='C')
    pdf.cell(3.5, 0.3, 'CLIENTE FINAL', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. REC.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. PRES.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. VTO.', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'PROB.', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'PRIOR.', fill=True, border=1, align='C')
    pdf.cell(2.75, 0.3, 'MATERIAL', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'Nº EQ.', fill=True, border=1, align='C')
    pdf.cell(2.2, 0.3, 'IMPORTE', fill=True, border=1, align='C')
    pdf.cell(3.25, 0.3, 'ACCIONES', fill=True, border=1, align='C')
    pdf.ln()

    pdf.set_fill_color(255, 105, 105)
    pdf.set_font('DejaVuSansCondensed', size=6)
    for _, row in df_more_30.iterrows():
        # getting the required height of the row
        line_h = pdf.font_size * 1.5
        h_client = pdf.get_multicell_height(2.75, line_h, '' if row['Cliente'] is None else str(row['Cliente']))
        h_clfinal = pdf.get_multicell_height(3.25, line_h, '' if row['Cl. Final'] is None else str(row['Cl. Final']))
        h_material = pdf.get_multicell_height(2.5, line_h, '' if row['Material'] is None else str(row['Material']))
        h_actions = pdf.get_multicell_height(3, line_h, '' if row['Acciones'] is None else str(row['Acciones']))

        row_height = max(h_client, h_clfinal, h_material, h_actions, line_h)

        # Setting values for table
        pdf.cell(1.5, row_height, '' if row['Nº Oferta'] is None else str(row['Nº Oferta']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Estado'] is None else str(row['Estado']), border=1, align='C')
        pdf.cell(2, row_height, '' if row['Responsable'] is None else str(row['Responsable']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Cálculos'] is None else str(row['Cálculos']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3, row_height, '' if row['Cliente'] is None else str(row['Cliente']), border=1)
        pdf.set_xy(x + 3, y)

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3.5, row_height, '' if row['Cl. Final'] is None else str(row['Cl. Final']), border=1)
        pdf.set_xy(x + 3.5, y)

        pdf.cell(1.5, row_height, '' if row['Fecha Rec.'] is None else str(row['Fecha Rec.']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Fecha Pres.'] is None else str(row['Fecha Pres.']), border=1, align='C', fill=True)
        pdf.cell(1.5, row_height, '' if row['Fecha Vto.'] is None else str(row['Fecha Vto.']), border=1, align='C')
        pdf.cell(1, row_height, '' if row['Prob.'] is None else str(row['Prob.']), border=1, align='C')
        pdf.cell(1, row_height, '' if row['Prior.'] is None else str(row['Prior.']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(2.75, row_height, '' if row['Material'] is None else str(row['Material']), border=1)
        pdf.set_xy(x + 2.75, y)

        pdf.cell(1, row_height, '' if row['Nº Eqs.'] is None else str(int(row['Nº Eqs.'])), border=1, align='C')
        pdf.cell(2.2, row_height, '' if row['Importe'] is None else str(row['Importe']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3.25, row_height, '' if row['Acciones'] is None else str(row['Acciones']), border=1)
        pdf.set_xy(x + 2.5, y)

        pdf.ln(row_height)

    pdf.set_fill_color(3, 174, 236)
    pdf.set_font('DejaVuSansCondensed-Bold', size=7)
    pdf.cell(20.75, 0.3, '')
    pdf.cell(5, 0.3, 'TOTAL:', align='R')
    pdf.cell(3, 0.3, euro_format(df_more_30['Importe Euros'].sum()), align='C')
    pdf.ln()

    df_active_budgetary.sort_values(by=['Nº Oferta'], inplace=True)

    pdf.set_font('Helvetica', 'B', size=7)
    pdf.cell(3, 0.5, 'BUDGETARIES (' + str(datetime.now().year) + '):')
    pdf.cell(3, 0.5, str(df_active_budgetary.shape[0]), align='L')
    pdf.ln(0.5)

    pdf.cell(1.5, 0.3, 'OFERTA', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'ESTADO', fill=True, border=1, align='C')
    pdf.cell(2, 0.3, 'RESP.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'CALC.', fill=True, border=1, align='C')
    pdf.cell(3, 0.3, 'CLIENTE', fill=True, border=1, align='C')
    pdf.cell(3.5, 0.3, 'CLIENTE FINAL', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. REC.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. PRES.', fill=True, border=1, align='C')
    pdf.cell(1.5, 0.3, 'F. VTO.', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'PROB.', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'PRIOR.', fill=True, border=1, align='C')
    pdf.cell(2.75, 0.3, 'MATERIAL', fill=True, border=1, align='C')
    pdf.cell(1, 0.3, 'Nº EQ.', fill=True, border=1, align='C')
    pdf.cell(2.2, 0.3, 'IMPORTE', fill=True, border=1, align='C')
    pdf.cell(3.25, 0.3, 'ACCIONES', fill=True, border=1, align='C')
    pdf.ln()

    pdf.set_fill_color(255, 105, 105)
    pdf.set_font('DejaVuSansCondensed', size=6)
    for _, row in df_active_budgetary.iterrows():
        # getting the required height of the row
        line_h = pdf.font_size * 1.5
        h_client = pdf.get_multicell_height(2.75, line_h, '' if row['Cliente'] is None else str(row['Cliente']))
        h_clfinal = pdf.get_multicell_height(3.25, line_h, '' if row['Cl. Final'] is None else str(row['Cl. Final']))
        h_material = pdf.get_multicell_height(2.5, line_h, '' if row['Material'] is None else str(row['Material']))
        h_actions = pdf.get_multicell_height(3, line_h, '' if row['Acciones'] is None else str(row['Acciones']))

        row_height = max(h_client, h_clfinal, h_material, h_actions, line_h)

        # Setting values for table
        pdf.cell(1.5, row_height, '' if row['Nº Oferta'] is None else str(row['Nº Oferta']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Estado'] is None else str(row['Estado']), border=1, align='C')
        pdf.cell(2, row_height, '' if row['Responsable'] is None else str(row['Responsable']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Cálculos'] is None else str(row['Cálculos']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3, row_height, '' if row['Cliente'] is None else str(row['Cliente']), border=1)
        pdf.set_xy(x + 3, y)

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3.5, row_height, '' if row['Cl. Final'] is None else str(row['Cl. Final']), border=1)
        pdf.set_xy(x + 3.5, y)

        pdf.cell(1.5, row_height, '' if row['Fecha Rec.'] is None else str(row['Fecha Rec.']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Fecha Pres.'] is None else str(row['Fecha Pres.']), border=1, align='C')
        pdf.cell(1.5, row_height, '' if row['Fecha Vto.'] is None else str(row['Fecha Vto.']), border=1, align='C')
        pdf.cell(1, row_height, '' if row['Prob.'] is None else str(row['Prob.']), border=1, align='C')
        pdf.cell(1, row_height, '' if row['Prior.'] is None else str(row['Prior.']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(2.75, row_height, '' if row['Material'] is None else str(row['Material']), border=1)
        pdf.set_xy(x + 2.75, y)

        pdf.cell(1, row_height, '' if row['Nº Eqs.'] is None else str(int(row['Nº Eqs.'])), border=1, align='C')
        pdf.cell(2.2, row_height, '' if row['Importe'] is None else str(row['Importe']), border=1, align='C')

        x = pdf.get_x()
        y = pdf.get_y()
        pdf.fixed_height_multicell(3.25, row_height, '' if row['Acciones'] is None else str(row['Acciones']), border=1)
        pdf.set_xy(x + 2.5, y)

        pdf.ln(row_height)

    pdf.set_font('DejaVuSansCondensed-Bold', size=7)
    pdf.cell(20.75, 0.3, '')
    pdf.cell(5, 0.3, 'TOTAL:', align='R')
    pdf.cell(3, 0.3, euro_format(df_active_budgetary['Importe Euros'].sum()), align='C')
    pdf.ln()

    pdf.set_fill_color(3, 174, 236)

    return pdf

def euro_format(valor):
    return f"{valor:,.2f} €".replace(',', 'X').replace('.', ',').replace('X', '.')

def euro_format_axis(x, pos):
    if x >= 1_000_000:
        return f'{x/1_000_000:.1f}M€'.replace('.', ',')
    elif x >= 1_000:
        return f'{x/1_000:.0f}k€'.replace('.', ',')
    else:
        return f'{x:.0f}€'

def get_date_range():
    """
    Shows input dialogs to enter dates and convert to correct format
    """
    start_date_str, ok1 = QtWidgets.QInputDialog.getText(None, "Fecha inicial", "Introduce la fecha inicial (DD/MM/YYYY):")
    if not ok1 or not start_date_str:
        return None, None

    end_date_str, ok2 = QtWidgets.QInputDialog.getText(None, "Fecha final", "Introduce la fecha final (DD/MM/YYYY):")
    if not ok2 or not end_date_str:
        return None, None

    # Validate and convert date to format yyyy-mm-dd
    try:
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y").date()
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y").date()
    except ValueError:
        MessageHelper.show_message("Formato de fecha inválido. Usa DD/MM/YYYY.", "warning")
        return None, None

    return start_date, end_date

def graphs_commercial_report(df_graph_commercial_1, df_graph_commercial_2):
    final_state_mapping = {
        "Registrada": ["Adjudicada", "Declinada", "No Ofertada", "Perdida", "Presentada", "Registrada", "En Estudio"],
        "No Ofertada": ["No Ofertada", "Declinada", "En Estudio"],
        "Ofertada": ["Adjudicada", "Perdida", "Presentada"],
        "No PO": ["Perdida", "Presentada"],
        "PO": ["Adjudicada"]
    }

    state_colors = {
        "Registrada": "#9467bd",
        "No Ofertada": "#ff7f0e",
        "Ofertada": "#ffe70eda",
        "No PO": "#d62728",
        "PO": "#2ca02c",
    }

    pivot_table_commercial_1 = df_graph_commercial_1.pivot_table(index='Responsable', columns='Estado', values='Importe Final', aggfunc='sum', fill_value=0)

    pivot_table_commercial_1.columns = pivot_table_commercial_1.columns.str.strip()
    categories = pivot_table_commercial_1.index.tolist()
    final_states = list(final_state_mapping.keys())
    final_values = np.zeros((len(categories), len(final_states)))

    for col_list in final_state_mapping.values():
        for col in col_list:
            if col not in pivot_table_commercial_1.columns:
                pivot_table_commercial_1[col] = 0

    # Calcular los valores finales por estado
    for j, final_state in enumerate(final_states):
        original_list = final_state_mapping[final_state]
        final_values[:, j] = pivot_table_commercial_1[original_list].sum(axis=1)

    x = np.arange(len(categories))           # Categories position
    width = 0.8 / len(final_states)               # Bar width

    fig, ax = plt.subplots(figsize=(8,5))

    for i, state in enumerate(final_states):
        color = state_colors.get(state, "#119efc")
        ax.bar(x + i*width, final_values[:, i], width=width, label=state, color=color)

    ax.set_xticks(x + width*(len(final_states)-1)/2)  # Center ticks
    ax.set_xticklabels(categories)

    ax.yaxis.set_major_formatter(FuncFormatter(euro_format_axis))
    ax.set_ylabel("Importe")
    ax.set_title("Importes por responsable y estado")
    ax.legend()

    img_graph_1 = BytesIO()
    plt.savefig(img_graph_1, format='PNG', bbox_inches='tight')
    plt.close()
    img_graph_1.seek(0)

    pivot_table_commercial_2 = df_graph_commercial_2.pivot_table(index='Responsable', columns='Estado', values='Nº Oferta', aggfunc='count', fill_value=0)

    pivot_table_commercial_2.columns = pivot_table_commercial_2.columns.str.strip()
    categories = pivot_table_commercial_2.index.tolist()
    final_states = list(final_state_mapping.keys())
    final_values = np.zeros((len(categories), len(final_states)))

    for col_list in final_state_mapping.values():
        for col in col_list:
            if col not in pivot_table_commercial_2.columns:
                pivot_table_commercial_2[col] = 0

    # Calcular los valores finales por estado
    for j, final_state in enumerate(final_states):
        original_list = final_state_mapping[final_state]
        final_values[:, j] = pivot_table_commercial_2[original_list].sum(axis=1)

    x = np.arange(len(categories))           # Categories position
    width = 0.8 / len(final_states)               # Bar width

    fig, ax = plt.subplots(figsize=(8,5))

    for i, state in enumerate(final_states):
        color = state_colors.get(state, "#119efc")
        ax.bar(x + i*width, final_values[:, i], width=width, label=state, color=color)

    ax.set_xticks(x + width*(len(final_states)-1)/2)  # Center ticks
    ax.set_xticklabels(categories)

    ax.set_ylabel("Recuento")
    ax.set_title("Recuento de ofertas por estado")
    ax.legend()

    img_graph_2 = BytesIO()
    plt.savefig(img_graph_2, format='PNG', bbox_inches='tight')
    plt.close()
    img_graph_2.seek(0)

    return [img_graph_1, img_graph_2]

def graphs_calculation_report(df_graph_calculation_1, df_graph_calculation_2):
    final_state_mapping = {
        "Ofertada": ["Adjudicada", "Perdida", "Presentada", "No Ofertada", "Declinada"],
        "No PO": ["Perdida", "Presentada", "No Ofertada", "Declinada"],
        "PO": ["Adjudicada"]
    }

    state_colors = {
        "Ofertada": "#ffe70eda",
        "No PO": "#d62728",
        "PO": "#2ca02c",
    }

    pivot_table_calculation_1 = df_graph_calculation_1.pivot_table(index='Responsable', columns='Estado', values='Importe Final', aggfunc='sum', fill_value=0)

    categories = pivot_table_calculation_1.index.tolist()
    final_states = list(final_state_mapping.keys())
    final_values = np.zeros((len(categories), len(final_states)))

    for state in state_colors.keys():
        if state not in pivot_table_calculation_1.columns:
            pivot_table_calculation_1[state] = 0

    for j, final_state in enumerate(final_states):
        original_list = final_state_mapping[final_state]
        # Filter columns in pivot only
        existing_columns = [col for col in original_list if col in pivot_table_calculation_1.columns]
        if existing_columns:
            final_values[:, j] = pivot_table_calculation_1[existing_columns].sum(axis=1)
        else:
            final_values[:, j] = 0

    x = np.arange(len(categories))           # Categories position
    width = 0.8 / len(final_states)               # Bar width

    fig, ax = plt.subplots(figsize=(8,5))

    for i, state in enumerate(final_states):
        color = state_colors.get(state, "#119efc")
        ax.bar(x + i*width, final_values[:, i], width=width, label=state, color=color)

    ax.set_xticks(x + width*(len(final_states)-1)/2)  # Center ticks
    ax.set_xticklabels(categories)

    ax.yaxis.set_major_formatter(FuncFormatter(euro_format_axis))
    ax.set_ylabel("Importe")
    ax.set_title("Importes por responsable y estado")
    ax.legend()

    img_graph_3 = BytesIO()
    plt.savefig(img_graph_3, format='PNG', bbox_inches='tight')
    plt.close()
    img_graph_3.seek(0)

    pivot_table_calculation_2 = df_graph_calculation_2.pivot_table(index='Responsable', columns='Estado', values='Nº Oferta', aggfunc='count', fill_value=0)

    categories = pivot_table_calculation_2.index.tolist()
    final_states = list(final_state_mapping.keys())
    final_values = np.zeros((len(categories), len(final_states)))

    for state in state_colors.keys():
        if state not in pivot_table_calculation_2.columns:
            pivot_table_calculation_2[state] = 0

    for j, final_state in enumerate(final_states):
        original_list = final_state_mapping[final_state]
        # Filter columns in pivot only
        existing_columns = [col for col in original_list if col in pivot_table_calculation_2.columns]
        if existing_columns:
            final_values[:, j] = pivot_table_calculation_2[existing_columns].sum(axis=1)
        else:
            final_values[:, j] = 0

    fig, ax = plt.subplots(figsize=(8,5))

    for i, state in enumerate(final_states):
        color = state_colors.get(state, "#119efc")
        ax.bar(x + i*width, final_values[:, i], width=width, label=state, color=color)

    ax.set_xticks(x + width*(len(final_states)-1)/2)  # Center ticks
    ax.set_xticklabels(categories)

    ax.set_ylabel("Recuento")
    ax.set_title("Recuento de ofertas por estado")
    ax.legend()

    img_graph_4 = BytesIO()
    plt.savefig(img_graph_4, format='PNG', bbox_inches='tight')
    plt.close()
    img_graph_4.seek(0)

    return [img_graph_3, img_graph_4]

def graphs_orders_report(df_graph_orders_1):
    df_p = df_graph_orders_1[df_graph_orders_1['Nº Pedido'].str.startswith('P-')]
    df_pa = df_graph_orders_1[df_graph_orders_1['Nº Pedido'].str.startswith('PA-')]

    sum_amount = pd.Series({
        'P': df_p['Importe Pedido'].sum(),
        'PA': df_pa['Importe Pedido'].sum()
    })

    count = pd.Series({
        'P': df_p.shape[0],
        'PA': df_pa.shape[0]
    })

    fig, ax = plt.subplots(figsize=(8,5))
    sum_amount.plot(kind='bar', color=['green', 'yellow'])
    ax.yaxis.set_major_formatter(FuncFormatter(euro_format_axis))
    ax.set_xticklabels(sum_amount.index, rotation=0)
    ax.set_title('Suma de Importe por Tipo de Pedido')
    ax.set_ylabel('Suma Importe')
    ax.set_xlabel('Tipo Pedido')

    img_graph_5 = BytesIO()
    plt.savefig(img_graph_5, format='PNG', bbox_inches='tight')
    plt.close()
    img_graph_5.seek(0)

    fig, ax = plt.subplots(figsize=(8,5))
    count.plot(kind='bar', color=['green', 'yellow'])
    ax.set_xticklabels(count.index, rotation=0)
    ax.set_title('Recuento por Tipo de Pedido')
    ax.set_ylabel('Recuento')
    ax.set_xlabel('Tipo Pedido')

    img_graph_6 = BytesIO()
    plt.savefig(img_graph_6, format='PNG', bbox_inches='tight')
    plt.close()
    img_graph_6.seek(0)

    return [img_graph_5, img_graph_6]

