# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)
from PySide6.QtGui import (QAction, QIcon)
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import (QMenu, QMenuBar, QSizePolicy, QSplitter, QStatusBar,
    QToolBar, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 600)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)

        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        icon1 = QIcon(QIcon.fromTheme(u"application-exit"))
        self.actionQuit.setIcon(icon1)
        self.actionZoom_In = QAction(MainWindow)
        self.actionZoom_In.setObjectName(u"actionZoom_In")
        icon3 = QIcon()
        iconThemeName = u"zoom-in"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile("//nas01/DATOS/Comunes/EIPSA-ERP/Recursos/pdfviewer/images/zoom-in.svgz", QSize(), QIcon.Normal, QIcon.Off)

        self.actionZoom_In.setIcon(icon3)
        self.actionZoom_Out = QAction(MainWindow)
        self.actionZoom_Out.setObjectName(u"actionZoom_Out")
        icon4 = QIcon()
        iconThemeName = u"zoom-out"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile("//nas01/DATOS/Comunes/EIPSA-ERP/Recursos/pdfviewer/images/zoom-out.svgz", QSize(), QIcon.Normal, QIcon.Off)

        self.actionZoom_Out.setIcon(icon4)
        self.actionPrevious_Page = QAction(MainWindow)
        self.actionPrevious_Page.setObjectName(u"actionPrevious_Page")
        icon5 = QIcon()
        iconThemeName = u"go-previous-view-page"
        if QIcon.hasThemeIcon(iconThemeName):
            icon5 = QIcon.fromTheme(iconThemeName)
        else:
            icon5.addFile("//nas01/DATOS/Comunes/EIPSA-ERP/Recursos/pdfviewer/images/go-previous-view-page.svgz", QSize(), QIcon.Normal, QIcon.Off)

        self.actionPrevious_Page.setIcon(icon5)
        self.actionNext_Page = QAction(MainWindow)
        self.actionNext_Page.setObjectName(u"actionNext_Page")
        icon6 = QIcon()
        iconThemeName = u"go-next-view-page"
        if QIcon.hasThemeIcon(iconThemeName):
            icon6 = QIcon.fromTheme(iconThemeName)
        else:
            icon6.addFile("//nas01/DATOS/Comunes/EIPSA-ERP/Recursos/pdfviewer/images/go-next-view-page.svgz", QSize(), QIcon.Normal, QIcon.Off)

        self.actionNext_Page.setIcon(icon6)
        self.actionContinuous = QAction(MainWindow)
        self.actionContinuous.setObjectName(u"actionContinuous")
        self.actionContinuous.setCheckable(True)
        self.actionBack = QAction(MainWindow)
        self.actionBack.setObjectName(u"actionBack")
        self.actionBack.setEnabled(False)
        icon7 = QIcon()
        icon7.addFile("//nas01/DATOS/Comunes/EIPSA-ERP/Recursos/pdfviewer/images/go-previous-view.svgz", QSize(), QIcon.Normal, QIcon.Off)
        self.actionBack.setIcon(icon7)
        self.actionForward = QAction(MainWindow)
        self.actionForward.setObjectName(u"actionForward")
        self.actionForward.setEnabled(False)
        icon8 = QIcon()
        icon8.addFile("//nas01/DATOS/Comunes/EIPSA-ERP/Recursos/pdfviewer/images/go-next-view.svgz", QSize(), QIcon.Normal, QIcon.Off)
        self.actionForward.setIcon(icon8)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.centralWidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.widget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.pdfView = QPdfView(self.splitter)
        self.pdfView.setObjectName(u"pdfView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(10)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pdfView.sizePolicy().hasHeightForWidth())
        self.pdfView.setSizePolicy(sizePolicy1)
        self.splitter.addWidget(self.pdfView)

        self.verticalLayout_2.addWidget(self.splitter)

        self.verticalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 700, 23))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menuBar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QToolBar(MainWindow)
        self.mainToolBar.setObjectName(u"mainToolBar")
        self.mainToolBar.setMovable(False)
        self.mainToolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionQuit)
        self.menuView.addAction(self.actionZoom_In)
        self.menuView.addAction(self.actionZoom_Out)
        self.menuView.addAction(self.actionPrevious_Page)
        self.menuView.addAction(self.actionNext_Page)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionContinuous)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionZoom_Out)
        self.mainToolBar.addAction(self.actionZoom_In)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionBack)
        self.mainToolBar.addAction(self.actionForward)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PDF Viewer", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionZoom_In.setText(QCoreApplication.translate("MainWindow", u"Zoom In", None))
#if QT_CONFIG(shortcut)
        self.actionZoom_In.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl++", None))
#endif // QT_CONFIG(shortcut)
        self.actionZoom_Out.setText(QCoreApplication.translate("MainWindow", u"Zoom Out", None))
#if QT_CONFIG(shortcut)
        self.actionZoom_Out.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+-", None))
#endif // QT_CONFIG(shortcut)
        self.actionPrevious_Page.setText(QCoreApplication.translate("MainWindow", u"Previous Page", None))
#if QT_CONFIG(shortcut)
        self.actionPrevious_Page.setShortcut(QCoreApplication.translate("MainWindow", u"PgUp", None))
#endif // QT_CONFIG(shortcut)
        self.actionNext_Page.setText(QCoreApplication.translate("MainWindow", u"Next Page", None))
#if QT_CONFIG(shortcut)
        self.actionNext_Page.setShortcut(QCoreApplication.translate("MainWindow", u"PgDown", None))
#endif // QT_CONFIG(shortcut)
        self.actionContinuous.setText(QCoreApplication.translate("MainWindow", u"Continuous", None))
        self.actionBack.setText(QCoreApplication.translate("MainWindow", u"Back", None))
#if QT_CONFIG(tooltip)
        self.actionBack.setToolTip(QCoreApplication.translate("MainWindow", u"back to previous view", None))
#endif // QT_CONFIG(tooltip)
        self.actionForward.setText(QCoreApplication.translate("MainWindow", u"Forward", None))
#if QT_CONFIG(tooltip)
        self.actionForward.setToolTip(QCoreApplication.translate("MainWindow", u"forward to next view", None))
#endif // QT_CONFIG(tooltip)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

