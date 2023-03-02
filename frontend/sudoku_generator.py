import math
import random


class SudokuGenerator:
    SUDOKU_FOLDER = "./sudoku_files/"

    def __init__(self, size):
        self._size = size
        self._block_rows = math.floor(size ** 0.5)
        self._block_cols = size // self._block_rows
        self._board = [[0] * size for _ in range(size)]
        self._values = range(1, size + 1)
        self._empty = 0.75

    def generate(self):
        if self._size <= 12:
            self._fill_diagonal_block()
            self._fill_cell(0, 0)
        else:
            self._generate_from_file()
        self._remove_cell_values()
        return self._board

    def _fill_diagonal_block(self):
        diagonal_block_count = self._size // self._block_cols
        for block in range(diagonal_block_count):
            start_row = block * self._block_rows
            start_col = block * self._block_cols
            values = list(self._values)
            random.shuffle(values)
            for row in range(start_row, start_row + self._block_rows):
                for col in range(start_col, start_col + self._block_cols):
                    self._board[row][col] = values.pop(0)

    def _fill_cell(self, row, col):
        if col == self._size:
            row += 1
            col = 0
        if row == self._size:
            return True
        if self._board[row][col] != 0:
            if self._fill_cell(row, col + 1):
                return True
        else:
            for value in random.sample(self._values, self._size):
                if self._check_cell_valid(row, col, value):
                    self._board[row][col] = value
                    if self._fill_cell(row, col + 1):
                        return True
                    self._board[row][col] = 0
        return False

    def _check_cell_valid(self, row, col, value):
        for r in self._board:
            if r[col] == value:
                return False
        for c in self._board[row]:
            if c == value:
                return False
        block_row_index = (row // self._block_rows) * self._block_rows
        block_col_index = (col // self._block_cols) * self._block_cols
        for r in range(block_row_index, block_row_index + self._block_rows):
            for c in range(block_col_index, block_col_index + self._block_cols):
                if self._board[r][c] == value:
                    return False
        return True

    def _generate_from_file(self):
        file_number = random.choice([1, 2, 3])
        file = f'{self.SUDOKU_FOLDER}{self._size}-{file_number}.txt'
        with open(file) as input_file:
            rows = input_file.readlines()
            for index, row in enumerate(rows):
                self._board[index] = [int(value) for value in row.split()]

    def _remove_cell_values(self):
        total_cell = self._size ** 2
        filled_cell = math.floor(total_cell * (1 - self._empty))
        board = [[0] * self._size for _ in range(self._size)]
        random_index = random.sample(range(total_cell), filled_cell)
        for index in random_index:
            row = index // self._size
            col = index % self._size
            board[row][col] = self._board[row][col]
        self._board = board


if __name__ == "__main__":
    puzzle_generator = SudokuGenerator(9)
    print(puzzle_generator.generate())
