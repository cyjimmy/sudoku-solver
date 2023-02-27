# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(520, 637)
        MainWindow.setMinimumSize(QSize(500, 500))
        font = QFont()
        font.setFamilies([u"P052"])
        MainWindow.setFont(font)
        icon = QIcon()
        iconThemeName = u"system-run"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(3.000000000000000)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        icon1 = QIcon()
        iconThemeName = u"application-exit"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.actionExit.setIcon(icon1)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Nimbus Roman"])
        font1.setPointSize(30)
        font1.setBold(False)
        self.label.setFont(font1)
        self.label.setMouseTracking(True)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setFrameShape(QFrame.StyledPanel)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.pushButtonCreatePuzzle = QPushButton(self.centralwidget)
        self.pushButtonCreatePuzzle.setObjectName(u"pushButtonCreatePuzzle")
        font2 = QFont()
        font2.setFamilies([u"P052"])
        font2.setPointSize(15)
        self.pushButtonCreatePuzzle.setFont(font2)
        self.pushButtonCreatePuzzle.setLayoutDirection(Qt.LeftToRight)
        self.pushButtonCreatePuzzle.setAutoFillBackground(False)
        self.pushButtonCreatePuzzle.setLocale(QLocale(QLocale.English, QLocale.Canada))
        icon2 = QIcon()
        iconThemeName = u"applications-office"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButtonCreatePuzzle.setIcon(icon2)

        self.verticalLayout.addWidget(self.pushButtonCreatePuzzle)

        self.pushButtonExit = QPushButton(self.centralwidget)
        self.pushButtonExit.setObjectName(u"pushButtonExit")
        self.pushButtonExit.setFont(font2)
        self.pushButtonExit.setIcon(icon1)

        self.verticalLayout.addWidget(self.pushButtonExit)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 520, 24))
        font3 = QFont()
        font3.setFamilies([u"P052"])
        font3.setPointSize(10)
        self.menubar.setFont(font3)
        self.menuMain = QMenu(self.menubar)
        self.menuMain.setObjectName(u"menuMain")
        font4 = QFont()
        font4.setFamilies([u"P052"])
        font4.setPointSize(10)
        font4.setBold(False)
        self.menuMain.setFont(font4)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMain.menuAction())
        self.menuMain.addAction(self.actionExit)
        self.menuMain.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sudoku Solver", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sudoku Solver", None))
        self.pushButtonCreatePuzzle.setText(QCoreApplication.translate("MainWindow", u"Create Puzzle", None))
        self.pushButtonExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.menuMain.setTitle(QCoreApplication.translate("MainWindow", u"Main", None))
    # retranslateUi

