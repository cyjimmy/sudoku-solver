import enum
from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QFrame
from typing import List

from custom_exceptions import InvalidFileDataException
# from frontend.sudoku_generator import SudokuGenerator
from sudoku_generator import SudokuGenerator

@dataclass
class GridSize(enum.Enum):
    __order__ = "NINE TWELVE SIXTEEN TWENTY_FIVE HUNDRED"
    NINE = {"blocks": 9, "block_rows": 3, "block_cols": 3}
    TWELVE = {"blocks": 12, "block_rows": 3, "block_cols": 4}
    SIXTEEN = {"blocks": 16, "block_rows": 4, "block_cols": 4}
    TWENTY_FIVE = {"blocks": 25, "block_rows": 5, "block_cols": 5}
    HUNDRED = {"blocks": 100, "block_rows": 10, "block_cols": 10}


class Cell:
    def __init__(self, row, col, block_row, block_col, value):
        self.value = value
        self.row = row
        self.col = col
        self.block_row = block_row
        self.block_col = block_col
        self.label_widget = QLabel(str(self.value))
        self.label_widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        if self.value is None:
            self.label_widget.setStyleSheet("background-color:#F5F5F5;")
        else:
            self.label_widget.setStyleSheet("background-color:#989898;")
        self.label_widget.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.label_widget.wordWrap()

    def __str__(self):
        result = f"Cell(Value={self.value}, Row={self.row}, Column={self.col})\n"
        return result


class Block:
    cells: List[Cell]

    def __init__(self, grid_size, block_num):
        self.block_num = block_num
        self.cells = []
        self.grid_size = grid_size
        self.row = int(block_num / (self.grid_size["block_rows"]))
        self.col = block_num % (self.grid_size["block_rows"])

    def __str__(self):
        result = f"Block(Row={self.row}, Column={self.col})\n"
        for cell in self.cells:
            result += cell.__str__()
        return result

    def generate(self, puzzle):
        for i in range(self.row * self.grid_size["block_rows"],
                       self.row * self.grid_size["block_rows"] + self.grid_size["block_rows"]):
            for j in range(self.col * self.grid_size["block_cols"],
                           self.col * self.grid_size["block_cols"] + self.grid_size["block_cols"]):
                # [TODO] Put generate puzzle logic here and assign values to cells
                self.cells.append(Cell(row=i,
                                       col=j,
                                       block_row=i - (self.row * self.grid_size["block_rows"]),
                                       block_col=j - (self.col * self.grid_size["block_cols"]),
                                       value=puzzle[i][j] if puzzle[i][j] != 0 else ""))

    def load(self, filename):
        # [TODO] Do something with the file, read it, and extract value for each cell
        for i in range(self.row * self.grid_size["block_rows"],
                       self.row * self.grid_size["block_rows"] + self.grid_size["block_rows"]):
            for j in range(self.col * self.grid_size["block_cols"],
                           self.col * self.grid_size["block_cols"] + self.grid_size["block_cols"]):
                # [TODO] Put load puzzle logic here and assign values to cells
                self.cells.append(Cell(row=i,
                                       col=j,
                                       block_row=i - (self.row * self.grid_size["block_rows"]),
                                       block_col=j - (self.col * self.grid_size["block_cols"]),
                                       value=(i, j)))


class Grid:
    blocks: List[Block]
    puzzle: list
    grid_size: GridSize

    def __init__(self, grid_size, puzzle=None):
        self.blocks = []
        self.grid_size = grid_size
        if puzzle is None:
            puzzle_generator = SudokuGenerator(self.grid_size.value["blocks"])
            self.puzzle = puzzle_generator.generate()
        else:
            self.puzzle = puzzle

    def __str__(self):
        result = "Grid\n"
        for block in self.blocks:
            result += block.__str__() + "\n"
        return result

    def clone(self, puzzle=None):
        if puzzle is None:
            puzzle = self.puzzle

        if self.grid_size is None:
            raise ValueError("Error - Grid Size is none can't copy this grid")
        new_grid = Grid(self.grid_size, puzzle)
        new_grid.generate()
        return new_grid

    def generate(self):
        for i in range(0, self.grid_size.value["blocks"]):
            block = Block(self.grid_size.value, i)
            block.generate(self.puzzle)
            self.blocks.append(block)

        # for block in self.blocks:
        #     print(f"Block {block.block_num}: {block.row}, {block.col}")
        #     for cell in block.cells:
        #         print(f"{cell.row}, {cell.col}")

    def load(self, filename):
        # [TODO] Do something with the file such that we can get the gridSize. For ex: 9, 12, 25, 100
        # based on this number, we can find the relevant enum
        n = 25  # set as constant for now until there's file handling logic

        for gs in GridSize:
            if gs.value["blocks"] == n:
                self.grid_size = gs.value
                break

        if self.grid_size is None:
            raise InvalidFileDataException(filename)
        else:
            for i in range(0, self.grid_size["blocks"]):
                block = Block(self.grid_size, i)
                block.load(filename)
                self.blocks.append(block)

            # for block in self.blocks:
            #     print(f"Block {block.block_num}: {block.row}, {block.col}")
            #     for cell in block.cells:
            #         print(f"{cell.row}, {cell.col}")
