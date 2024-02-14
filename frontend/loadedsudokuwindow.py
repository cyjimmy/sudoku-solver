# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loadedsudokuwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(975, 637)
        MainWindow.setMinimumSize(QSize(500, 500))
        font = QFont()
        font.setFamilies([u"P052"])
        MainWindow.setFont(font)
        icon = QIcon()
        iconThemeName = u"package-x-generic"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.Canada))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonBrute = QPushButton(self.centralwidget)
        self.pushButtonBrute.setObjectName(u"pushButtonBrute")
        font1 = QFont()
        font1.setFamilies([u"P052"])
        font1.setPointSize(12)
        self.pushButtonBrute.setFont(font1)
        self.pushButtonBrute.setLayoutDirection(Qt.LeftToRight)
        icon1 = QIcon()
        iconThemeName = u"system-run"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButtonBrute.setIcon(icon1)

        self.horizontalLayout.addWidget(self.pushButtonBrute)

        self.pushButtonCSP = QPushButton(self.centralwidget)
        self.pushButtonCSP.setObjectName(u"pushButtonCSP")
        self.pushButtonCSP.setFont(font1)
        self.pushButtonCSP.setLayoutDirection(Qt.LeftToRight)
        self.pushButtonCSP.setIcon(icon1)

        self.horizontalLayout.addWidget(self.pushButtonCSP)

        self.pushButtonBack = QPushButton(self.centralwidget)
        self.pushButtonBack.setObjectName(u"pushButtonBack")
        self.pushButtonBack.setFont(font1)
        self.pushButtonBack.setLayoutDirection(Qt.LeftToRight)
        icon2 = QIcon()
        iconThemeName = u"go-previous"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButtonBack.setIcon(icon2)

        self.horizontalLayout.addWidget(self.pushButtonBack)

        self.pushButtonExit = QPushButton(self.centralwidget)
        self.pushButtonExit.setObjectName(u"pushButtonExit")
        self.pushButtonExit.setFont(font1)
        self.pushButtonExit.setLayoutDirection(Qt.LeftToRight)
        icon3 = QIcon()
        iconThemeName = u"application-exit"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButtonExit.setIcon(icon3)

        self.horizontalLayout.addWidget(self.pushButtonExit)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 975, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Loaded Sudoku Puzzle", None))
        self.pushButtonBrute.setText(QCoreApplication.translate("MainWindow", u"Solve (Brute/Heuristic)", None))
        self.pushButtonCSP.setText(QCoreApplication.translate("MainWindow", u"Solve (CSP)", None))
        self.pushButtonBack.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.pushButtonExit.setText(QCoreApplication.translate("MainWindow", u"EXIT", None))
    # retranslateUi

