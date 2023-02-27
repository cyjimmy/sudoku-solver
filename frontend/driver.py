import random
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
        # self.pushButton_3.clicked.connect(self.generate_sudoku)
        self.pushButton_3.clicked.connect(self.improved_generate_sudoku)

    @staticmethod
    def improved_generate_sudoku():
        generator = SudokuGenerator(16)
        board = generator.generate()
        for row in board:
            print(row)
        print("---------------")

    @staticmethod
    def generate_sudoku():
        size = 9
        values = set(range(1, size + 1))
        subgrid_row = 3
        subgrid_col = 3
        sudoku_grid = [[0] * size for _ in range(size)]
        valid_board_generated = False
        while not valid_board_generated:
            try:
                for row_index, row in enumerate(sudoku_grid):
                    subgrid_start_row_index = (row_index // subgrid_row) * subgrid_row
                    subgrid_row_indices = range(subgrid_start_row_index, subgrid_start_row_index + subgrid_row)
                    for col_index, col in enumerate(row):
                        subgrid_start_col_index = (col_index // subgrid_col) * subgrid_col
                        subgrid_col_indices = range(subgrid_start_col_index, subgrid_start_col_index + subgrid_col)
                        grid_values = set([sudoku_grid[r][c] for r in subgrid_row_indices for c in subgrid_col_indices])
                        row_values = set(cell for cell in row)
                        col_values = set([r[col_index] for r in sudoku_grid])
                        used_values = grid_values | row_values | col_values
                        unused_values = list(values - used_values)
                        sudoku_grid[row_index][col_index] = random.choice(unused_values)
                valid_board_generated = True
            except IndexError:
                sudoku_grid = [[0] * size for _ in range(size)]
        for row in sudoku_grid:
            for col in row:
                print(col, end="")
            print("")
        print("---------------")


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

gw = GeneratePuzzleWindow()
gw.show()
app.exec()
