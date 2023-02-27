# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'generatepuzzledialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 213)
        Dialog.setMinimumSize(QSize(0, 0))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sudokuSizeSelector = QComboBox(Dialog)
        self.sudokuSizeSelector.setObjectName(u"sudokuSizeSelector")
        font = QFont()
        font.setFamilies([u"P052"])
        font.setPointSize(12)
        self.sudokuSizeSelector.setFont(font)
        self.sudokuSizeSelector.setLayoutDirection(Qt.LeftToRight)
        self.sudokuSizeSelector.setLocale(QLocale(QLocale.English, QLocale.Canada))

        self.verticalLayout.addWidget(self.sudokuSizeSelector)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setLocale(QLocale(QLocale.English, QLocale.Canada))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.sudokuSizeSelector.setPlaceholderText(QCoreApplication.translate("Dialog", u"Select Sudoku Size", None))
    # retranslateUi

