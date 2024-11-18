# Form implementation generated from reading ui file 'TimerWindow_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import os

basedir = r"\\nas01\DATOS\Comunes\EIPSA-ERP"


class Ui_TimerWindow(QtWidgets.QMainWindow):
    """
    UI class for the Timer window.
    """
    def __init__(self, username):
        """
        Initializes the Ui_TimerWindow with the specified username.

        Args:
            username (str): username associated with the window.
        """
        super().__init__()
        self.username = username
        self.setupUi(self)

    def setupUi(self, TimerWindow):
        """
        Sets up the user interface for the TimerWindow.

        Args:
            TimerWindow (QtWidgets.QMainWindow): The main window for the UI setup.
        """
        TimerWindow.setObjectName("TimerWindow")
        TimerWindow.resize(300, 336)
        TimerWindow.setMinimumSize(QtCore.QSize(1000, 700))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.abspath(os.path.join(basedir, "Resources/Iconos/icon.ico"))), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        TimerWindow.setWindowIcon(icon)
        if self.username == 'm.gil':
            TimerWindow.setStyleSheet("QWidget {\n"
    "background-color: #121212; color: rgb(255, 255, 255)\n"
    "}\n"
    "\n"
    ".QFrame {\n"
    "    border: 2px solid white;\n"
    "}\n"
    "\n"
    "QPushButton {\n"
    "background-color: #33bdef;\n"
    "  border: 1px solid transparent;\n"
    "  border-radius: 3px;\n"
    "  color: #fff;\n"
    "  font-family: -apple-system,system-ui,\"Segoe UI\",\"Liberation Sans\",sans-serif;\n"
    "  font-size: 15px;\n"
    "  font-weight: 800;\n"
    "  line-height: 1.15385;\n"
    "  margin: 0;\n"
    "  outline: none;\n"
    "  padding: 8px .8em;\n"
    "  text-align: center;\n"
    "  text-decoration: none;\n"
    "  vertical-align: baseline;\n"
    "  white-space: nowrap;\n"
    "}\n"
    "\n"
    "QPushButton:hover {\n"
    "    background-color: #019ad2;\n"
    "    border-color: rgb(0, 0, 0);\n"
    "}\n"
    "\n"
    "QPushButton:pressed {\n"
    "    background-color: rgb(1, 140, 190);\n"
    "    border-color: rgb(255, 255, 255);\n"
    "}"
    )
        else:
            TimerWindow.setStyleSheet("QWidget {\n"
    "background-color: rgb(255, 255, 255);\n"
    "}\n"
    "\n"
    ".QFrame {\n"
    "    border: 2px solid black;\n"
    "}\n"
    "\n"
    "QPushButton {\n"
    "background-color: #33bdef;\n"
    "  border: 1px solid transparent;\n"
    "  border-radius: 3px;\n"
    "  color: #fff;\n"
    "  font-family: -apple-system,system-ui,\"Segoe UI\",\"Liberation Sans\",sans-serif;\n"
    "  font-size: 15px;\n"
    "  font-weight: 800;\n"
    "  line-height: 1.15385;\n"
    "  margin: 0;\n"
    "  outline: none;\n"
    "  padding: 8px .8em;\n"
    "  text-align: center;\n"
    "  text-decoration: none;\n"
    "  vertical-align: baseline;\n"
    "  white-space: nowrap;\n"
    "}\n"
    "\n"
    "QPushButton:hover {\n"
    "    background-color: #019ad2;\n"
    "    border-color: rgb(0, 0, 0);\n"
    "}\n"
    "\n"
    "QPushButton:pressed {\n"
    "    background-color: rgb(1, 140, 190);\n"
    "    border-color: rgb(255, 255, 255);\n"
    "}"
    )
        self.centralwidget = QtWidgets.QWidget(parent=TimerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem3, 0, 0, 1, 1)
        self.button = QtWidgets.QPushButton(parent=self.frame)
        self.button.setMinimumSize(QtCore.QSize(100, 35))
        self.button.setMaximumSize(QtCore.QSize(100, 35))
        self.button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button.setObjectName("button")
        self.gridLayout_2.addWidget(self.button, 1, 0, 1, 1)
        self.start_button = QtWidgets.QPushButton(parent=self.frame)
        self.start_button.setMinimumSize(QtCore.QSize(100, 35))
        self.start_button.setMaximumSize(QtCore.QSize(100, 35))
        self.start_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.start_button.setObjectName("start_button")
        self.gridLayout_2.addWidget(self.start_button, 1, 1, 1, 1)
        self.pause_button = QtWidgets.QPushButton(parent=self.frame)
        self.pause_button.setMinimumSize(QtCore.QSize(100, 35))
        self.pause_button.setMaximumSize(QtCore.QSize(100, 35))
        self.pause_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.pause_button.setObjectName("pause_button")
        self.gridLayout_2.addWidget(self.pause_button, 1, 2, 1, 1)
        self.reset_button = QtWidgets.QPushButton(parent=self.frame)
        self.reset_button.setMinimumSize(QtCore.QSize(100, 35))
        self.reset_button.setMaximumSize(QtCore.QSize(100, 35))
        self.reset_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.reset_button.setObjectName("reset_button")
        self.gridLayout_2.addWidget(self.reset_button, 1, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_2.addItem(spacerItem2, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setMinimumSize(QtCore.QSize(250, 35))
        # self.label.setMaximumSize(QtCore.QSize(250, 35))
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.label.setObjectName("label")
        font_id = QtGui.QFontDatabase.addApplicationFont(os.path.abspath(os.path.join(basedir, "Resources/Iconos/DS-DIGI.ttf")))
        if font_id != -1:
            font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QtGui.QFont(font_family, 350)
        else:
            font = QtGui.QFont("arial", 150)
        font.setBold(True)
        self.label.setFont(font)
        if self.username == 'm.gil':
            self.label.setStyleSheet("color: white")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 4)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Cancel.setEnabled(True)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(100, 35))
        self.Button_Cancel.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.gridLayout_2.addWidget(self.Button_Cancel, 4, 3, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        TimerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=TimerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 22))
        self.menubar.setObjectName("menubar")
        TimerWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=TimerWindow)
        self.statusbar.setObjectName("statusbar")
        TimerWindow.setStatusBar(self.statusbar)
        TimerWindow.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint, False)

        self.count = 0
        self.start = False

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.retranslateUi(TimerWindow)
        QtCore.QMetaObject.connectSlotsByName(TimerWindow)

        self.Button_Cancel.clicked.connect(TimerWindow.close) # type: ignore
        self.button.clicked.connect(self.get_seconds)
        self.start_button.clicked.connect(self.start_action)
        self.pause_button.clicked.connect(self.pause_action)
        self.reset_button.clicked.connect(self.reset_action)

# Function to translate and updates the text of various UI elements
    def retranslateUi(self, TimerWindow):
        """
        Translates and updates the text of various UI elements.
        """
        _translate = QtCore.QCoreApplication.translate
        TimerWindow.setWindowTitle(_translate("TimerWindow", "Temporizador"))
        self.start_button.setText(_translate("TimerWindow", "Start"))
        self.pause_button.setText(_translate("TimerWindow", "Pause"))
        self.reset_button.setText(_translate("TimerWindow", "Reset"))
        self.Button_Cancel.setText(_translate("TimerWindow", "Cancelar"))
        self.button.setText(_translate("TimerWindow", "SET"))
        self.label.setText(_translate("TimerWindow", "TIMER"))

# method called by timer
    def showTime(self):
        """
        Updates the countdown timer display. 
        """
	# checking if flag is true
        if self.start:
		# incrementing the counter
            self.count -= 1

		# timer is completed
            if self.count == 0:
			# making flag false
                self.start = False
                self.label.setText("FIN")

        if self.start:
    # getting text from count
            minutes = self.count // 60
            seconds = self.count % 60
            time_text = f"{minutes:02}:{seconds:02}"
            self.label.setText(time_text)

# method called by the push button
    def get_seconds(self):
        """
        Prompts the user to input the number of minutes for the countdown timer.
        The input is then converted into seconds, and the timer label is updated accordingly.
        """
	# making flag false
        self.start = False

	# getting seconds and flag
        minutes, done = QtWidgets.QInputDialog.getInt(self, 'Minutos', 'Introduce los minutos:')

	# if flag is true
        if done:
            self.count = minutes * 60
            self.label.setText(self.secs_to_minsec(minutes))

    def start_action(self):
        """
        Starts the countdown timer if the time is set. 
        """
        self.start = True

        if self.count == 0:
            self.start = False

    def pause_action(self):
        """
        Pauses the countdown timer by setting the `start` flag to False.
        """
        self.start = False

    def reset_action(self):
        """
        Resets the countdown timer to zero, stops it, and updates the display to show "TIMER".
        """
        self.start = False
        self.count = 0
        self.label.setText("TIMER")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def secs_to_minsec(self, minutes: int):
        """
        Converts a given number of minutes into MM:SS format and returns the formatted time string.

        Args:
            minutes (integer): Minutes to be converted
        """
        seconds = minutes * 60
        mins = seconds // 60
        secs = seconds % 60
        minsec = f'{mins:02}:{secs:02}'
        return minsec



# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     QueryDoc_Window = Ui_TimerWindow()
#     QueryDoc_Window.show()
#     sys.exit(app.exec())
