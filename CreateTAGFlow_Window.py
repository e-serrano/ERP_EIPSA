# Form implementation generated from reading ui file 'CreateTAGFlow_Window.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from config import config
import psycopg2


class Ui_CreateTAGFlow_Window(object):
    def setupUi(self, CreateTAGFlow_Window):
        CreateTAGFlow_Window.setObjectName("CreateTAGFlow_Window")
        CreateTAGFlow_Window.resize(1255, 511)
        CreateTAGFlow_Window.setMinimumSize(QtCore.QSize(1255, 515))
        CreateTAGFlow_Window.setMaximumSize(QtCore.QSize(1255, 515))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        CreateTAGFlow_Window.setWindowIcon(icon)
        CreateTAGFlow_Window.setStyleSheet("QWidget {\n"
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
"}")
        self.centralwidget = QtWidgets.QWidget(parent=CreateTAGFlow_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(1235, 450))
        self.frame.setMaximumSize(QtCore.QSize(1235, 450))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.hLayout1 = QtWidgets.QHBoxLayout()
        self.hLayout1.setObjectName("hLayout1")
        self.vLayout1 = QtWidgets.QVBoxLayout()
        self.vLayout1.setSpacing(15)
        self.vLayout1.setObjectName("vLayout1")
        self.label_TAG = QtWidgets.QLabel(parent=self.frame)
        self.label_TAG.setMinimumSize(QtCore.QSize(110, 25))
        self.label_TAG.setMaximumSize(QtCore.QSize(110, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_TAG.setFont(font)
        self.label_TAG.setObjectName("label_TAG")
        self.vLayout1.addWidget(self.label_TAG)
        self.label_NumOffer = QtWidgets.QLabel(parent=self.frame)
        self.label_NumOffer.setMinimumSize(QtCore.QSize(110, 25))
        self.label_NumOffer.setMaximumSize(QtCore.QSize(110, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumOffer.setFont(font)
        self.label_NumOffer.setObjectName("label_NumOffer")
        self.vLayout1.addWidget(self.label_NumOffer)
        self.label_NumOrder = QtWidgets.QLabel(parent=self.frame)
        self.label_NumOrder.setMinimumSize(QtCore.QSize(110, 25))
        self.label_NumOrder.setMaximumSize(QtCore.QSize(110, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_NumOrder.setFont(font)
        self.label_NumOrder.setObjectName("label_NumOrder")
        self.vLayout1.addWidget(self.label_NumOrder)
        self.label_Pos = QtWidgets.QLabel(parent=self.frame)
        self.label_Pos.setMinimumSize(QtCore.QSize(110, 25))
        self.label_Pos.setMaximumSize(QtCore.QSize(110, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Pos.setFont(font)
        self.label_Pos.setObjectName("label_Pos")
        self.vLayout1.addWidget(self.label_Pos)
        self.label_SubPos = QtWidgets.QLabel(parent=self.frame)
        self.label_SubPos.setMinimumSize(QtCore.QSize(110, 25))
        self.label_SubPos.setMaximumSize(QtCore.QSize(110, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_SubPos.setFont(font)
        self.label_SubPos.setObjectName("label_SubPos")
        self.vLayout1.addWidget(self.label_SubPos)
        self.label_Type = QtWidgets.QLabel(parent=self.frame)
        self.label_Type.setMinimumSize(QtCore.QSize(110, 25))
        self.label_Type.setMaximumSize(QtCore.QSize(110, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Type.setFont(font)
        self.label_Type.setObjectName("label_Type")
        self.vLayout1.addWidget(self.label_Type)
        self.label_Linesize = QtWidgets.QLabel(parent=self.frame)
        self.label_Linesize.setMinimumSize(QtCore.QSize(110, 25))
        self.label_Linesize.setMaximumSize(QtCore.QSize(110, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Linesize.setFont(font)
        self.label_Linesize.setObjectName("label_Linesize")
        self.vLayout1.addWidget(self.label_Linesize)
        self.label_Rating = QtWidgets.QLabel(parent=self.frame)
        self.label_Rating.setMinimumSize(QtCore.QSize(110, 25))
        self.label_Rating.setMaximumSize(QtCore.QSize(110, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Rating.setFont(font)
        self.label_Rating.setObjectName("label_Rating")
        self.vLayout1.addWidget(self.label_Rating)
        self.hLayout1.addLayout(self.vLayout1)
        self.vLayout2 = QtWidgets.QVBoxLayout()
        self.vLayout2.setSpacing(15)
        self.vLayout2.setObjectName("vLayout2")
        self.TAG_CreatetagQ = QtWidgets.QLineEdit(parent=self.frame)
        self.TAG_CreatetagQ.setMinimumSize(QtCore.QSize(150, 25))
        self.TAG_CreatetagQ.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.TAG_CreatetagQ.setFont(font)
        self.TAG_CreatetagQ.setObjectName("TAG_CreatetagQ")
        self.vLayout2.addWidget(self.TAG_CreatetagQ)
        self.NumOffer_CreatetagQ = QtWidgets.QLineEdit(parent=self.frame)
        self.NumOffer_CreatetagQ.setMinimumSize(QtCore.QSize(150, 25))
        self.NumOffer_CreatetagQ.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumOffer_CreatetagQ.setFont(font)
        self.NumOffer_CreatetagQ.setObjectName("NumOffer_CreatetagQ")
        self.vLayout2.addWidget(self.NumOffer_CreatetagQ)
        self.NumOrder_CreatetagQ = QtWidgets.QLineEdit(parent=self.frame)
        self.NumOrder_CreatetagQ.setMinimumSize(QtCore.QSize(150, 25))
        self.NumOrder_CreatetagQ.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.NumOrder_CreatetagQ.setFont(font)
        self.NumOrder_CreatetagQ.setObjectName("NumOrder_CreatetagQ")
        self.vLayout2.addWidget(self.NumOrder_CreatetagQ)
        self.Pos_CreatetagQ = QtWidgets.QLineEdit(parent=self.frame)
        self.Pos_CreatetagQ.setMinimumSize(QtCore.QSize(150, 25))
        self.Pos_CreatetagQ.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Pos_CreatetagQ.setFont(font)
        self.Pos_CreatetagQ.setObjectName("Pos_CreatetagQ")
        self.vLayout2.addWidget(self.Pos_CreatetagQ)
        self.Subpos_CreatetagQ = QtWidgets.QLineEdit(parent=self.frame)
        self.Subpos_CreatetagQ.setMinimumSize(QtCore.QSize(150, 25))
        self.Subpos_CreatetagQ.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Subpos_CreatetagQ.setFont(font)
        self.Subpos_CreatetagQ.setObjectName("Subpos_CreatetagQ")
        self.vLayout2.addWidget(self.Subpos_CreatetagQ)
        self.Type_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.Type_CreatetagQ.setMinimumSize(QtCore.QSize(150, 25))
        self.Type_CreatetagQ.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Type_CreatetagQ.setFont(font)
        self.Type_CreatetagQ.setObjectName("Type_CreatetagQ")
        self.vLayout2.addWidget(self.Type_CreatetagQ)
        self.Linesize_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.Linesize_CreatetagQ.setMinimumSize(QtCore.QSize(150, 25))
        self.Linesize_CreatetagQ.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Linesize_CreatetagQ.setFont(font)
        self.Linesize_CreatetagQ.setObjectName("Linesize_CreatetagQ")
        self.vLayout2.addWidget(self.Linesize_CreatetagQ)
        self.Rating_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.Rating_CreatetagQ.setMinimumSize(QtCore.QSize(150, 25))
        self.Rating_CreatetagQ.setMaximumSize(QtCore.QSize(150, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Rating_CreatetagQ.setFont(font)
        self.Rating_CreatetagQ.setObjectName("Rating_CreatetagQ")
        self.vLayout2.addWidget(self.Rating_CreatetagQ)
        self.hLayout1.addLayout(self.vLayout2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hLayout1.addItem(spacerItem)
        self.vLayout3 = QtWidgets.QVBoxLayout()
        self.vLayout3.setSpacing(15)
        self.vLayout3.setObjectName("vLayout3")
        self.label_Facing = QtWidgets.QLabel(parent=self.frame)
        self.label_Facing.setMinimumSize(QtCore.QSize(125, 25))
        self.label_Facing.setMaximumSize(QtCore.QSize(125, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Facing.setFont(font)
        self.label_Facing.setObjectName("label_Facing")
        self.vLayout3.addWidget(self.label_Facing)
        self.label_Sch = QtWidgets.QLabel(parent=self.frame)
        self.label_Sch.setMinimumSize(QtCore.QSize(125, 25))
        self.label_Sch.setMaximumSize(QtCore.QSize(125, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Sch.setFont(font)
        self.label_Sch.setObjectName("label_Sch")
        self.vLayout3.addWidget(self.label_Sch)
        self.label_Flangemat = QtWidgets.QLabel(parent=self.frame)
        self.label_Flangemat.setMinimumSize(QtCore.QSize(125, 25))
        self.label_Flangemat.setMaximumSize(QtCore.QSize(125, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Flangemat.setFont(font)
        self.label_Flangemat.setObjectName("label_Flangemat")
        self.vLayout3.addWidget(self.label_Flangemat)
        self.label_Tapping = QtWidgets.QLabel(parent=self.frame)
        self.label_Tapping.setMinimumSize(QtCore.QSize(125, 25))
        self.label_Tapping.setMaximumSize(QtCore.QSize(125, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Tapping.setFont(font)
        self.label_Tapping.setObjectName("label_Tapping")
        self.vLayout3.addWidget(self.label_Tapping)
        self.label_Platemat = QtWidgets.QLabel(parent=self.frame)
        self.label_Platemat.setMinimumSize(QtCore.QSize(125, 25))
        self.label_Platemat.setMaximumSize(QtCore.QSize(125, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Platemat.setFont(font)
        self.label_Platemat.setObjectName("label_Platemat")
        self.vLayout3.addWidget(self.label_Platemat)
        self.label_Platetype = QtWidgets.QLabel(parent=self.frame)
        self.label_Platetype.setMinimumSize(QtCore.QSize(125, 25))
        self.label_Platetype.setMaximumSize(QtCore.QSize(125, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Platetype.setFont(font)
        self.label_Platetype.setObjectName("label_Platetype")
        self.vLayout3.addWidget(self.label_Platetype)
        self.label_Platethk = QtWidgets.QLabel(parent=self.frame)
        self.label_Platethk.setMinimumSize(QtCore.QSize(125, 25))
        self.label_Platethk.setMaximumSize(QtCore.QSize(125, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Platethk.setFont(font)
        self.label_Platethk.setObjectName("label_Platethk")
        self.vLayout3.addWidget(self.label_Platethk)
        self.label_Platestd = QtWidgets.QLabel(parent=self.frame)
        self.label_Platestd.setMinimumSize(QtCore.QSize(125, 25))
        self.label_Platestd.setMaximumSize(QtCore.QSize(125, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Platestd.setFont(font)
        self.label_Platestd.setObjectName("label_Platestd")
        self.vLayout3.addWidget(self.label_Platestd)
        self.hLayout1.addLayout(self.vLayout3)
        self.vLayout4 = QtWidgets.QVBoxLayout()
        self.vLayout4.setSpacing(15)
        self.vLayout4.setObjectName("vLayout4")
        self.Facing_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.Facing_CreatetagQ.setMinimumSize(QtCore.QSize(200, 25))
        self.Facing_CreatetagQ.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Facing_CreatetagQ.setFont(font)
        self.Facing_CreatetagQ.setObjectName("Facing_CreatetagQ")
        self.vLayout4.addWidget(self.Facing_CreatetagQ)
        self.Sch_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.Sch_CreatetagQ.setMinimumSize(QtCore.QSize(200, 25))
        self.Sch_CreatetagQ.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Sch_CreatetagQ.setFont(font)
        self.Sch_CreatetagQ.setObjectName("Sch_CreatetagQ")
        self.vLayout4.addWidget(self.Sch_CreatetagQ)
        self.Flangemat_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.Flangemat_CreatetagQ.setMinimumSize(QtCore.QSize(200, 25))
        self.Flangemat_CreatetagQ.setMaximumSize(QtCore.QSize(200, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Flangemat_CreatetagQ.setFont(font)
        self.Flangemat_CreatetagQ.setObjectName("Flangemat_CreatetagQ")
        self.vLayout4.addWidget(self.Flangemat_CreatetagQ)
        self.Tapping_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.Tapping_CreatetagQ.setMinimumSize(QtCore.QSize(200, 25))
        self.Tapping_CreatetagQ.setMaximumSize(QtCore.QSize(200, 25))
        self.Tapping_CreatetagQ.setObjectName("Tapping_CreatetagQ")
        self.vLayout4.addWidget(self.Tapping_CreatetagQ)
        self.PlateMat_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.PlateMat_CreatetagQ.setMinimumSize(QtCore.QSize(200, 25))
        self.PlateMat_CreatetagQ.setMaximumSize(QtCore.QSize(200, 25))
        self.PlateMat_CreatetagQ.setObjectName("PlateMat_CreatetagQ")
        self.vLayout4.addWidget(self.PlateMat_CreatetagQ)
        self.PlateType_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.PlateType_CreatetagQ.setMinimumSize(QtCore.QSize(200, 25))
        self.PlateType_CreatetagQ.setMaximumSize(QtCore.QSize(200, 25))
        self.PlateType_CreatetagQ.setObjectName("PlateType_CreatetagQ")
        self.vLayout4.addWidget(self.PlateType_CreatetagQ)
        self.PlateThk_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.PlateThk_CreatetagQ.setMinimumSize(QtCore.QSize(200, 25))
        self.PlateThk_CreatetagQ.setMaximumSize(QtCore.QSize(200, 25))
        self.PlateThk_CreatetagQ.setObjectName("PlateThk_CreatetagQ")
        self.vLayout4.addWidget(self.PlateThk_CreatetagQ)
        self.PlateStd_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.PlateStd_CreatetagQ.setMinimumSize(QtCore.QSize(200, 25))
        self.PlateStd_CreatetagQ.setMaximumSize(QtCore.QSize(200, 25))
        self.PlateStd_CreatetagQ.setObjectName("PlateStd_CreatetagQ")
        self.vLayout4.addWidget(self.PlateStd_CreatetagQ)
        self.hLayout1.addLayout(self.vLayout4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.hLayout1.addItem(spacerItem1)
        self.vLayout5 = QtWidgets.QVBoxLayout()
        self.vLayout5.setContentsMargins(-1, -1, 0, -1)
        self.vLayout5.setSpacing(15)
        self.vLayout5.setObjectName("vLayout5")
        self.label_Gasketmat = QtWidgets.QLabel(parent=self.frame)
        self.label_Gasketmat.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Gasketmat.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Gasketmat.setFont(font)
        self.label_Gasketmat.setObjectName("label_Gasketmat")
        self.vLayout5.addWidget(self.label_Gasketmat)
        self.label_Bnmat = QtWidgets.QLabel(parent=self.frame)
        self.label_Bnmat.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Bnmat.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Bnmat.setFont(font)
        self.label_Bnmat.setObjectName("label_Bnmat")
        self.vLayout5.addWidget(self.label_Bnmat)
        self.label_Nace = QtWidgets.QLabel(parent=self.frame)
        self.label_Nace.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Nace.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Nace.setFont(font)
        self.label_Nace.setObjectName("label_Nace")
        self.vLayout5.addWidget(self.label_Nace)
        self.label_Stagesnum = QtWidgets.QLabel(parent=self.frame)
        self.label_Stagesnum.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Stagesnum.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Stagesnum.setFont(font)
        self.label_Stagesnum.setObjectName("label_Stagesnum")
        self.vLayout5.addWidget(self.label_Stagesnum)
        self.label_Pipespec = QtWidgets.QLabel(parent=self.frame)
        self.label_Pipespec.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Pipespec.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Pipespec.setFont(font)
        self.label_Pipespec.setObjectName("label_Pipespec")
        self.vLayout5.addWidget(self.label_Pipespec)
        self.label_Notes = QtWidgets.QLabel(parent=self.frame)
        self.label_Notes.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Notes.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Notes.setFont(font)
        self.label_Notes.setObjectName("label_Notes")
        self.vLayout5.addWidget(self.label_Notes)
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setText("")
        self.label.setObjectName("label")
        self.vLayout5.addWidget(self.label)
        self.label_Amount = QtWidgets.QLabel(parent=self.frame)
        self.label_Amount.setMinimumSize(QtCore.QSize(115, 25))
        self.label_Amount.setMaximumSize(QtCore.QSize(115, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_Amount.setFont(font)
        self.label_Amount.setObjectName("label_Amount")
        self.vLayout5.addWidget(self.label_Amount)
        self.hLayout1.addLayout(self.vLayout5)
        self.vLayout6 = QtWidgets.QVBoxLayout()
        self.vLayout6.setContentsMargins(-1, -1, 0, -1)
        self.vLayout6.setSpacing(15)
        self.vLayout6.setObjectName("vLayout6")
        self.GasketMat_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.GasketMat_CreatetagQ.setMinimumSize(QtCore.QSize(375, 25))
        self.GasketMat_CreatetagQ.setMaximumSize(QtCore.QSize(375, 25))
        self.GasketMat_CreatetagQ.setObjectName("GasketMat_CreatetagQ")
        self.vLayout6.addWidget(self.GasketMat_CreatetagQ)
        self.BnMat_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.BnMat_CreatetagQ.setMinimumSize(QtCore.QSize(375, 25))
        self.BnMat_CreatetagQ.setMaximumSize(QtCore.QSize(375, 25))
        self.BnMat_CreatetagQ.setObjectName("BnMat_CreatetagQ")
        self.vLayout6.addWidget(self.BnMat_CreatetagQ)
        self.Nace_CreatetagQ = QtWidgets.QComboBox(parent=self.frame)
        self.Nace_CreatetagQ.setMinimumSize(QtCore.QSize(375, 25))
        self.Nace_CreatetagQ.setMaximumSize(QtCore.QSize(375, 25))
        self.Nace_CreatetagQ.setObjectName("Nace_CreatetagQ")
        self.vLayout6.addWidget(self.Nace_CreatetagQ)
        self.StagesNum_CreatetagQ = QtWidgets.QLineEdit(parent=self.frame)
        self.StagesNum_CreatetagQ.setMinimumSize(QtCore.QSize(375, 25))
        self.StagesNum_CreatetagQ.setMaximumSize(QtCore.QSize(375, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.StagesNum_CreatetagQ.setFont(font)
        self.StagesNum_CreatetagQ.setObjectName("StagesNum_CreatetagQ")
        self.vLayout6.addWidget(self.StagesNum_CreatetagQ)
        self.PipeSpec_CreatetagQ = QtWidgets.QLineEdit(parent=self.frame)
        self.PipeSpec_CreatetagQ.setMinimumSize(QtCore.QSize(375, 25))
        self.PipeSpec_CreatetagQ.setMaximumSize(QtCore.QSize(375, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PipeSpec_CreatetagQ.setFont(font)
        self.PipeSpec_CreatetagQ.setObjectName("PipeSpec_CreatetagQ")
        self.vLayout6.addWidget(self.PipeSpec_CreatetagQ)
        self.Notes_CreatetagQ = QtWidgets.QTextEdit(parent=self.frame)
        self.Notes_CreatetagQ.setMinimumSize(QtCore.QSize(375, 65))
        self.Notes_CreatetagQ.setMaximumSize(QtCore.QSize(375, 65))
        self.Notes_CreatetagQ.setObjectName("Notes_CreatetagQ")
        self.vLayout6.addWidget(self.Notes_CreatetagQ)
        self.Amount_CreatetagQ = QtWidgets.QLineEdit(parent=self.frame)
        self.Amount_CreatetagQ.setMinimumSize(QtCore.QSize(375, 25))
        self.Amount_CreatetagQ.setMaximumSize(QtCore.QSize(375, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Amount_CreatetagQ.setFont(font)
        self.Amount_CreatetagQ.setObjectName("Amount_CreatetagQ")
        self.vLayout6.addWidget(self.Amount_CreatetagQ)
        self.hLayout1.addLayout(self.vLayout6)
        self.verticalLayout_5.addLayout(self.hLayout1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_5.addItem(spacerItem2)
        self.hLayout2 = QtWidgets.QHBoxLayout()
        self.hLayout2.setObjectName("hLayout2")
        self.Button_Create = QtWidgets.QPushButton(parent=self.frame)
        self.Button_Create.setMinimumSize(QtCore.QSize(200, 35))
        self.Button_Create.setMaximumSize(QtCore.QSize(200, 35))
        self.Button_Create.setObjectName("Button_Create")
        self.hLayout2.addWidget(self.Button_Create)
        self.Button_Cancel = QtWidgets.QPushButton(parent=self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button_Cancel.sizePolicy().hasHeightForWidth())
        self.Button_Cancel.setSizePolicy(sizePolicy)
        self.Button_Cancel.setMinimumSize(QtCore.QSize(200, 35))
        self.Button_Cancel.setMaximumSize(QtCore.QSize(200, 35))
        self.Button_Cancel.setObjectName("Button_Cancel")
        self.hLayout2.addWidget(self.Button_Cancel)
        self.verticalLayout_5.addLayout(self.hLayout2)
        self.label_error = QtWidgets.QLabel(parent=self.frame)
        self.label_error.setMinimumSize(QtCore.QSize(0, 20))
        self.label_error.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_error.setStyleSheet("color: rgb(255, 0, 0);")
        self.label_error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_error.setFont(font)
        self.label_error.setObjectName("label_error")
        self.verticalLayout_5.addWidget(self.label_error)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        CreateTAGFlow_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=CreateTAGFlow_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1255, 22))
        self.menubar.setObjectName("menubar")
        CreateTAGFlow_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=CreateTAGFlow_Window)
        self.statusbar.setObjectName("statusbar")
        CreateTAGFlow_Window.setStatusBar(self.statusbar)

        list_nace=['Hold','No','Yes']
        self.Nace_CreatetagQ.addItems(list_nace)

        self.retranslateUi(CreateTAGFlow_Window)
        self.Button_Cancel.clicked.connect(CreateTAGFlow_Window.close) # type: ignore
        self.Button_Create.clicked.connect(self.createtagF) # type: ignore
        self.NumOrder_CreatetagQ.returnPressed.connect(self.queryoffernumber)
        QtCore.QMetaObject.connectSlotsByName(CreateTAGFlow_Window)


    def retranslateUi(self, CreateTAGFlow_Window):
        _translate = QtCore.QCoreApplication.translate
        CreateTAGFlow_Window.setWindowTitle(_translate("CreateTAGFlow_Window", "Crear TAG Caudal"))
        self.label_TAG.setText(_translate("CreateTAGFlow_Window", "*TAG:"))
        self.label_NumOffer.setText(_translate("CreateTAGFlow_Window", "*Nº Oferta:"))
        self.label_NumOrder.setText(_translate("CreateTAGFlow_Window", "Nº Pedido:"))
        self.label_Pos.setText(_translate("CreateTAGFlow_Window", "Posición:"))
        self.label_SubPos.setText(_translate("CreateTAGFlow_Window", "Sub-Pos:"))
        self.label_Type.setText(_translate("CreateTAGFlow_Window", "*Tipo:"))
        self.label_Linesize.setText(_translate("CreateTAGFlow_Window", "*Tamaño Línea:"))
        self.label_Rating.setText(_translate("CreateTAGFlow_Window", "*Rating:"))
        self.label_Facing.setText(_translate("CreateTAGFlow_Window", "*Facing:"))
        self.label_Sch.setText(_translate("CreateTAGFlow_Window", "*SCH:"))
        self.label_Flangemat.setText(_translate("CreateTAGFlow_Window", "Mat. Brida:"))
        self.label_Amount.setText(_translate("CreateTAGFlow_Window", "Importe (€):"))
        self.label_Tapping.setText(_translate("CreateTAGFlow_Window", "Tomas Pres. (Nº):"))
        self.label_Platemat.setText(_translate("CreateTAGFlow_Window", "Mat. Placa:"))
        self.label_Platetype.setText(_translate("CreateTAGFlow_Window", "Tipo Placa:"))
        self.label_Platethk.setText(_translate("CreateTAGFlow_Window", "Esp. Placa (mm):"))
        self.label_Platestd.setText(_translate("CreateTAGFlow_Window", "STD Placa:"))
        self.label_Gasketmat.setText(_translate("CreateTAGFlow_Window", "Mat. Junta:"))
        self.label_Bnmat.setText(_translate("CreateTAGFlow_Window", "Mat. Tornillería:"))
        self.label_Nace.setText(_translate("CreateTAGFlow_Window", "NACE:"))
        self.label_Stagesnum.setText(_translate("CreateTAGFlow_Window", "Nº Saltos:"))
        self.label_Pipespec.setText(_translate("CreateTAGFlow_Window", "Espec. Línea:"))
        self.label_Notes.setText(_translate("CreateTAGFlow_Window", "Notas:"))
        self.Button_Create.setText(_translate("CreateTAGFlow_Window", "Crear"))
        self.Button_Cancel.setText(_translate("CreateTAGFlow_Window","Cancelar"))


    def createtagF(self):
        tag=self.TAG_CreatetagQ.text()
        numoffer=self.NumOffer_CreatetagQ.text()
        numorder=self.NumOrder_CreatetagQ.text()
        pos=self.Pos_CreatetagQ.text()
        subpos=self.Subpos_CreatetagQ.text()
        typeF=self.Type_CreatetagQ.currentText()
        linesize=self.Linesize_CreatetagQ.currentText()
        rating=self.Rating_CreatetagQ.currentText()
        facing=self.Facing_CreatetagQ.currentText()
        schedule=self.Sch_CreatetagQ.currentText()
        flagemat=self.Flangemat_CreatetagQ.currentText()
        amount=self.Amount_CreatetagQ.text()
        tapping=self.Tapping_CreatetagQ.currentText()
        platemat=self.PlateMat_CreatetagQ.currentText()
        platetype=self.PlateType_CreatetagQ.currentText()
        platethk=self.PlateThk_CreatetagQ.currentText()
        platestd=self.PlateStd_CreatetagQ.currentText()
        gasketmat=self.GasketMat_CreatetagQ.currentText()
        boltsnutsmat=self.BnMat_CreatetagQ.currentText()
        nace=self.Nace_CreatetagQ.currentText()
        numstages=self.StagesNum_CreatetagQ.text()
        pipespec=self.PipeSpec_CreatetagQ.text()
        notes=self.Notes_CreatetagQ.toPlainText()


        if ((tag=="" or tag==" ") or (typeF=="" or typeF==" ") or (numoffer=="" or numoffer==" ") or (linesize=="" or linesize==" ")
        or (rating=="" or rating==" ") or (facing=="" or facing==" ") or (schedule=="" or schedule==" ")):
            self.label_error.setText('Rellene los campos con * mínimo')
        
        else:
            print('a')


    def queryoffernumber(self):
        numorder=self.NumOrder_CreatetagQ.text()
    #SQL Query for loading existing data in database
        commands_loadofferorder = ("""
                    SELECT "num_order","num_offer"
                    FROM orders
                    WHERE "num_order" = %s
                    """)
        conn = None
        try:
        # read the connection parameters
            params = config()
        # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
        # execution of commands one by one
            cur.execute(commands_loadofferorder,(numorder,))
            results=cur.fetchall()
            match=list(filter(lambda x:numorder in x, results))
        # close communication with the PostgreSQL database server
            cur.close()
        # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        if len(match)==0:
            dlg = QtWidgets.QMessageBox()
            new_icon = QtGui.QIcon()
            new_icon.addPixmap(QtGui.QPixmap("//nas01/DATOS/Comunes/EIPSA-ERP/Iconos/icon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            dlg.setWindowIcon(new_icon)
            dlg.setWindowTitle("Crear Tag")
            dlg.setText("El número de oferta introducido no existe")
            dlg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            dlg.exec()

        else:
            self.NumOffer_CreatetagQ.setText(str(results[0][1]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    CreateTAGFlow_Window = QtWidgets.QMainWindow()
    ui = Ui_CreateTAGFlow_Window()
    ui.setupUi(CreateTAGFlow_Window)
    CreateTAGFlow_Window.show()
    sys.exit(app.exec())
