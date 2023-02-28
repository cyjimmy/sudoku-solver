import sys
from PySide6 import QtWidgets

import mainwindow
import generatepuzzle
from frontend.sudoku_generator import SudokuGenerator


class MainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class GeneratePuzzleWindow(QtWidgets.QMainWindow, generatepuzzle.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_3.clicked.connect(self.generate_sudoku)

    @staticmethod
    def generate_sudoku():
        generator = SudokuGenerator(25)
        board = generator.generate()
        for row in board:
            print(row)
        print("---------------")


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

gw = GeneratePuzzleWindow()
gw.show()
app.exec()
