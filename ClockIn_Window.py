from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6 import QtCore, QtGui, QtWidgets
from datetime import *
from config import config
import psycopg2
import os

basedir = r"\\erp-eipsa-datos\Comunes\EIPSA-ERP"


class ImageCalendarWidget(QtWidgets.QCalendarWidget):
    """
    A custom calendar widget that displays worker-specific tasks and work times.

    Attributes:
        worker_id (int): The ID of the worker for whom the calendar is displaying data.
        task_dates (list): A list of dates that correspond to task entries.
        week_data (dict): Data on weekly work times for comparison with the expected work hours.
    """
    def __init__(self, worker_id, parent=None):
        """
        Initializes the ImageCalendarWidget.

        Args:
            worker_id (int): The ID of the worker whose data will be displayed.
            parent (QWidget, optional): The parent widget, if any.
        """
        super().__init__(parent)
        self.task_dates = []
        self.week_data = {} 
        self.worker_id = worker_id
        self.currentPageChanged.connect(self.updateWeekNumber)

    def set_task_dates(self, dates):
        """
        Sets the task dates for the worker.

        Args:
            dates (list): A list of dates representing tasks for the worker.
        """
        self.task_dates = dates
        self.updateCells()

    def paintCell(self, painter, rect, date):
        """
        Customizes the rendering of a calendar cell.

        Args:
            painter (QPainter): The painter object used to draw on the calendar.
            rect (QRect): The rectangle area of the cell being painted.
            date (QDate): The date represented by the current cell.
        """
        super().paintCell(painter, rect, date)

        if date.toPython() in self.task_dates:
            commands_dates = ("""
                        SELECT notes,
                            CASE
                                WHEN '00:00:00' IN (time_3, time_4) AND (notes IS NULL OR TRIM(notes) = '') AND EXTRACT(DOW FROM "workday") != 5 THEN (time_2 - time_1) - interval '1 hour'
                                WHEN (notes IS NULL OR TRIM(notes) = '') AND EXTRACT(DOW FROM "workday") != 5 THEN (time_4 - time_1) - interval '1 hour'
                                ELSE (time_2 - time_1)
                            END AS total_time
                        FROM clock_in_times
                        WHERE "workday" = %s AND "worker_id" = %s
                        """)
            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands
                data=(date.toPython(),self.worker_id,)
                cur.execute(commands_dates, data)
                results=cur.fetchall()

                type_day = results[0][0]
                time_result = str(timedelta(seconds=results[0][1].seconds))

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

            text = ("" + "\n" + '' if type_day in ['FESTIVO','AUSENTE'] else "" + "\n" + str(time_result)) +"\n" + type_day
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)
            painter.setPen(QtCore.Qt.GlobalColor.black)

            x = rect.x() + (rect.width() - 20) / 2
            y = rect.y() + rect.height() - 55

            text_rect = QtCore.QRectF(x, y, rect.width(), rect.height())
            painter.drawText(text_rect, text)

            week_number = str(date.weekNumber()[0])

            if str(week_number) in list(self.week_data.keys()):
                seconds_to_work = float(self.week_data[week_number][1]* 8 * 3600)
                time_to_work = timedelta(seconds=seconds_to_work)
                days = time_to_work.days
                hours, remainder = divmod(time_to_work.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_to_work = "{:02}:{:02}:{:02}".format((days * 24) + hours, minutes, seconds)

                seconds_working = self.week_data[week_number][0]
                time_working = timedelta(seconds=seconds_working)
                days = time_working.days
                hours, remainder = divmod(time_working.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_working = "{:02}:{:02}:{:02}".format((days * 24) + hours, minutes, seconds)

                extra_time = int(seconds_working - seconds_to_work)
                hours, remainder = divmod(extra_time, 3600)
                minutes, seconds = divmod(remainder, 60)
                extra_time = "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

                text = f'{time_to_work}\n{time_working}\nExtra: {extra_time}'

                y = rect.y() + rect.height() - 55

                text_rect = QtCore.QRectF(100, y, rect.width(), rect.height())
                painter.drawText(text_rect, text)


    def updateWeekNumber(self):
        """
        Updates the data related to the weeks in the currently displayed month.
        """
        current_month = self.monthShown()
        current_year = self.yearShown()

        # Obtaining dates for current month
        first_day_of_month = QtCore.QDate(current_year, current_month, 1)
        last_day_of_month = first_day_of_month.addMonths(1).addDays(-1)

        # Obtaining weeks for dates range
        weeks_in_month = []
        current_date = first_day_of_month
        while current_date <= last_day_of_month:
            week_number = current_date.weekNumber()
            if week_number not in weeks_in_month:
                weeks_in_month.append(week_number)
            current_date = current_date.addDays(7)

        week_data = {}

        for week_number in weeks_in_month:
            week = str(week_number[0])
            year = str(week_number[1])

            commands = ("""
                        SELECT  
                        EXTRACT(YEAR FROM workday) AS year,
                        EXTRACT(WEEK FROM workday) AS week,
                        SUM(
                            CASE
                                WHEN '00:00:00' IN (time_3, time_4) AND (notes IS NULL OR TRIM(notes) = '') AND EXTRACT(DOW FROM "workday") != 5 THEN EXTRACT(EPOCH FROM (time_2 - time_1 - interval '1 hour'))
                                WHEN (notes IS NULL OR TRIM(notes) = '') AND EXTRACT(DOW FROM "workday") != 5 THEN EXTRACT(EPOCH FROM (time_4 - time_1 - interval '1 hour'))
                                ELSE EXTRACT(EPOCH FROM (time_2 - time_1))
                            END
                        ) AS total_time,
                        SUM(
                            CASE
                                WHEN notes IS NULL OR TRIM(notes) = '' THEN 1
                                ELSE 0
                            END
                        ) AS days_without_notes
                    FROM clock_in_times
                    WHERE (EXTRACT(YEAR FROM workday) = %s AND EXTRACT(WEEK FROM workday) = %s AND worker_id = %s)
                    GROUP BY year, week
                        """)
            conn = None
            try:
            # read the connection parameters
                params = config()
            # connect to the PostgreSQL server
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
            # execution of commands
                data=(year, week, self.worker_id)
                cur.execute(commands, data)
                results=cur.fetchall()

                if len(results) != 0 :
                    days_working = int(results[0][3])
                    total_seconds = float(results[0][2])
                    total_time_timedelta = timedelta(seconds=total_seconds)

                    days = total_time_timedelta.days
                    hours, remainder = divmod(total_time_timedelta.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    formatted_time = "{:02}:{:02}:{:02}".format((days * 24) + hours, minutes, seconds)

                    week_data[week] = [total_seconds, days_working]

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

        self.week_data = week_data


class MyCalendarApp(QMainWindow):
    """
    UI class for the ClockIn Calendar window.
    """
    def __init__(self, username):
        """
        Initializes the MyCalendarApp with the specified username.

        Args:
            username (str): username associated with the window.
        """
        super().__init__()
        self.username = username
        self.setupUi(self)

    def setupUi(self, Calendar_window):
        """
        Sets up the user interface for the Calendar_window.

        Args:
            Calendar_window (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        Calendar_window.setObjectName("Calendar_window")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Calendar_window.setWindowIcon(icon)

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        commands_userlogin = ("""
                        SELECT worker_id
                        FROM users_data.registration
                        WHERE username = %s
                        """)
        conn = None
        try:
            # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands one by one
            cur.execute(commands_userlogin,(self.username,))
            results = cur.fetchall()
            self.worker_id = results[0][0]
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

        self.Calendar = ImageCalendarWidget(self.worker_id, self)
        self.Calendar.setEnabled(True)
        self.Calendar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.Calendar.setStyleSheet("QCalendarWidget QWidget{\n"
"background-color: rgb(3, 174, 236);\n"
"}\n"
"\n"
"QCalendarWidget QTableView{\n"
"    background-color: white;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton {\n"
"    color: white;\n"
"    font-size:20px;\n"
"    icon-size:30px 30px;\n"
"    background-color:rgb(3, 174, 236);\n"
"}\n"
"\n"
"QCalendarWidget QToolButton::hover {\n"
"    background-color : #019ad2;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton::pressed {\n"
"    background-color: rgb(1, 140, 190);\n"
"    border: 3px solid;\n"
"    border-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QCalendarWidget QSpinBox{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: 2px solid;\n"
"    border-color: rgb(3,174, 236);\n"
"}\n"
"\n"
"QCalendarWidget QAbstractItemView:enabled{\n"
"    selection-background-color: rgb(3, 174, 236);\n"
"    selection-color: white;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth {\n"
"    qproperty-icon: url(//ERP-EIPSA-DATOS/DATOS/Comunes/EIPSA-ERP/Resources/Iconos/back_arrow.png);\n"
"}\n"
"#qt_calendar_nextmonth {\n"
"    qproperty-icon: url(//ERP-EIPSA-DATOS/DATOS/Comunes/EIPSA-ERP/Resources/Iconos/forward_arrow.png);\n"
"\n"
"}")
        self.Calendar.setSelectedDate(QtCore.QDate.currentDate())
        self.Calendar.setGridVisible(True)
        self.Calendar.setNavigationBarVisible(True)
        self.Calendar.setDateEditEnabled(True)
        self.Calendar.setObjectName("Calendar")
        self.Calendar.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.layout.addWidget(self.Calendar)

        self.setCentralWidget(self.central_widget)

        self.retranslateUi(Calendar_window)

        data = self.load_data(self.worker_id)

        dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in data]

        self.Calendar.set_task_dates(dates)

        self.Calendar.activated.connect(self.show_selected_date)


# Function to translate and updates the text of various UI elements
    def retranslateUi(self, Calendar_window):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        Calendar_window.setWindowTitle(_translate("Calendar_window", "Calendario Fichajes"))


    def load_data(self, personal_id):
        """
        Loads clock-in dates for a specific worker based on their ID.

        Args:
            personal_id (str): The ID of the worker whose clock-in dates are being retrieved.

        Returns:
            list: A list of clock-in dates for the worker in 'yyyy-MM-dd' format.

        Raises:
            psycopg2.DatabaseError: If an error occurs while querying the PostgreSQL database.
        """
        commands = ("""
                        SELECT TO_CHAR("workday",'yyyy-MM-dd')
                        FROM clock_in_times
                        WHERE "worker_id" = %s
                        """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            data=(personal_id,)
            cur.execute(commands, data)
            results=cur.fetchall()

            dates_clockin = [x[0] for x in results]
    # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()

            return dates_clockin
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


    def show_selected_date(self):
        """
        Displays the clock-in times for the selected date from the calendar.

        Raises:
            psycopg2.DatabaseError: If an error occurs while querying the PostgreSQL database.
        """
        selected_date = self.Calendar.selectedDate().toString("yyyy-MM-dd")
        returned = self.get_times_date(self.worker_id, selected_date)

        if returned:
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("ERP EIPSA")
            final_text=''

            for item in returned:
                day_type = item[0] if item[0] != '' else 'LABORAL'
                mark_1 = item[1]
                mark_2 = item[2]
                mark_3 = item[3]
                mark_4 = item[4]

                final_text += "<br><br>" + f"Fichaje 1: {mark_1}<br>" + f"Fichaje 2: {mark_2}<br>" + f"Fichaje 3: {mark_3}<br>" + f"Fichaje 4: {mark_4}<br>"

            dlg.setText(f"<html><body>Fichajes para la fecha {self.Calendar.selectedDate().toString('dd-MM-yyyy')} ({day_type}){final_text}</body></html>")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            dlg.exec()
            del dlg, new_icon

    def get_times_date(self, id, date):
        """
        Retrieves the clock-in times for a worker on a specific date.

        Args:
            id (str): The worker's ID.
            date (str): The specific date for which clock-in times are being retrieved.

        Returns:
            list: A list containing the notes and four clock-in times for the specified date.

        Raises:
            psycopg2.DatabaseError: If an error occurs while querying the PostgreSQL database.
        """
        commands = ("""
                        SELECT TRIM(notes), time_1, time_2, time_3, time_4
                        FROM clock_in_times
                        WHERE ("worker_id" = %s
                        AND
                        workday = %s)
                        """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands
            data=(id, date,)
            cur.execute(commands, data)
            results=cur.fetchall()

    # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()

            return results

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


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Calendar_window = MyCalendarApp('j.martinez')
#     Calendar_window.showMaximized()
#     sys.exit(app.exec())
