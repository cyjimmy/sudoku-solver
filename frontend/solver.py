# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'solver.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(500, 500))
        font = QFont()
        font.setFamilies([u"P052"])
        font.setPointSize(12)
        MainWindow.setFont(font)
        icon = QIcon(QIcon.fromTheme(u"edit-find"))
        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.Canada))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelSolveStatus = QLabel(self.centralwidget)
        self.labelSolveStatus.setObjectName(u"labelSolveStatus")
        self.labelSolveStatus.setFrameShape(QFrame.StyledPanel)
        self.labelSolveStatus.setFrameShadow(QFrame.Plain)
        self.labelSolveStatus.setWordWrap(True)

        self.horizontalLayout.addWidget(self.labelSolveStatus)

        self.labelAlgorithm = QLabel(self.centralwidget)
        self.labelAlgorithm.setObjectName(u"labelAlgorithm")
        self.labelAlgorithm.setFrameShape(QFrame.StyledPanel)
        self.labelAlgorithm.setWordWrap(True)

        self.horizontalLayout.addWidget(self.labelAlgorithm)

        self.labelTime = QLabel(self.centralwidget)
        self.labelTime.setObjectName(u"labelTime")
        self.labelTime.setFrameShape(QFrame.StyledPanel)
        self.labelTime.setWordWrap(True)

        self.horizontalLayout.addWidget(self.labelTime)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.pushButtonExit = QPushButton(self.centralwidget)
        self.pushButtonExit.setObjectName(u"pushButtonExit")
        self.pushButtonExit.setFont(font)
        self.pushButtonExit.setLayoutDirection(Qt.LeftToRight)
        icon1 = QIcon(QIcon.fromTheme(u"application-exit"))
        self.pushButtonExit.setIcon(icon1)

        self.verticalLayout.addWidget(self.pushButtonExit)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 28))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Solver", None))
        self.labelSolveStatus.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.labelAlgorithm.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.labelTime.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButtonExit.setText(QCoreApplication.translate("MainWindow", u"EXIT", None))
    # retranslateUi


class BruteForceSolver:
    def solveSudoku(self, board):
        """
        Solves the Sudoku puzzle using backtracking algorithm.

        Parameters:
        board (list): 9x9 Sudoku grid with missing numbers represented as 0.

        Returns:
        bool: True if puzzle is solved, False if not solvable.
        """
        # Find the next empty cell
        row, col = self.findEmptyCell(board)

        # If no empty cell is found, the puzzle is solved
        if row == -1 and col == -1:
            return board
            # return True

        # Try filling the empty cell with numbers 1 to 9
        for num in range(1, len(board[0]) + 1):
            # Check if the number is valid for the empty cell
            if self.isValid(board, row, col, num):
                # Fill the empty cell with the valid number
                board[row][col] = num

                # Recursively try solving the rest of the puzzle
                if self.solveSudoku(board):
                    return board
                    # return True

                # If the puzzle cannot be solved with the current number,
                # backtrack by resetting the empty cell to 0
                board[row][col] = 0

        # If none of the numbers 1 to 9 can solve the puzzle, return False
        return False

    def findEmptyCell(self, board):
        """
        Finds the next empty cell in the Sudoku puzzle.

        Parameters:
        board (list): 9x9 Sudoku grid with missing numbers represented as 0.

        Returns:
        tuple: Row and column indices of the next empty cell. (-1, -1) if no empty cell is found.
        """
        for row in range(len(board[0])):
            for col in range(len(board[0])):
                if board[row][col] == 0:
                    return row, col
        return -1, -1

    def isValid(self, board, row, col, num):
        """
        Checks if the given number is valid for the given cell.

        Parameters:
        board (list): 9x9 Sudoku grid with missing numbers represented as 0.
        row (int): Row index of the cell.
        col (int): Column index of the cell.
        num (int): Number to be checked.

        Returns:
        bool: True if number is valid for the cell, False otherwise.
        """
        # Check row for same number
        for i in range(len(board[0])):
            if board[row][i] == num:
                return False

        # Check column for same number
        for i in range(len(board[0])):
            if board[i][col] == num:
                return False

        # Check 3x3 sub-grid for same number
        subgridRow = (row // 3) * 3
        subgridCol = (col // 3) * 3
        for i in range(subgridRow, subgridRow + 3):
            for j in range(subgridCol, subgridCol + 3):
                if board[i][j] == num:
                    return False

        # Number is valid for the cell
        return True