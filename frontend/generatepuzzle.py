# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'generatepuzzle.ui'
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 500)
        MainWindow.setMinimumSize(QSize(500, 500))
        font = QFont()
        font.setFamilies([u"P052"])
        MainWindow.setFont(font)
        icon = QIcon()
        iconThemeName = u"address-book-new"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.Canada))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButtonLoadPuzzle = QPushButton(self.centralwidget)
        self.pushButtonLoadPuzzle.setObjectName(u"pushButtonLoadPuzzle")
        font1 = QFont()
        font1.setFamilies([u"P052"])
        font1.setPointSize(15)
        self.pushButtonLoadPuzzle.setFont(font1)
        icon1 = QIcon()
        iconThemeName = u"insert-object"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButtonLoadPuzzle.setIcon(icon1)
        self.pushButtonLoadPuzzle.setAutoDefault(False)
        self.pushButtonLoadPuzzle.setFlat(False)

        self.verticalLayout.addWidget(self.pushButtonLoadPuzzle)

        self.pushButtonGeneratePuzzle = QPushButton(self.centralwidget)
        self.pushButtonGeneratePuzzle.setObjectName(u"pushButtonGeneratePuzzle")
        self.pushButtonGeneratePuzzle.setFont(font1)
        icon2 = QIcon()
        iconThemeName = u"utilities-system-monitor"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButtonGeneratePuzzle.setIcon(icon2)
        self.pushButtonGeneratePuzzle.setAutoDefault(False)
        self.pushButtonGeneratePuzzle.setFlat(False)

        self.verticalLayout.addWidget(self.pushButtonGeneratePuzzle)

        self.pushButtonGoBack = QPushButton(self.centralwidget)
        self.pushButtonGoBack.setObjectName(u"pushButtonGoBack")
        self.pushButtonGoBack.setFont(font1)
        icon3 = QIcon()
        iconThemeName = u"go-previous"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.pushButtonGoBack.setIcon(icon3)
        self.pushButtonGoBack.setAutoDefault(False)
        self.pushButtonGoBack.setFlat(False)

        self.verticalLayout.addWidget(self.pushButtonGoBack)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 500, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.pushButtonLoadPuzzle.setDefault(False)
        self.pushButtonGeneratePuzzle.setDefault(False)
        self.pushButtonGoBack.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sudoku Solver: generate puzzle", None))
        self.pushButtonLoadPuzzle.setText(QCoreApplication.translate("MainWindow", u"Load Puzzle", None))
        self.pushButtonGeneratePuzzle.setText(QCoreApplication.translate("MainWindow", u"Generate Puzzle", None))
        self.pushButtonGoBack.setText(QCoreApplication.translate("MainWindow", u"Back", None))
    # retranslateUi

