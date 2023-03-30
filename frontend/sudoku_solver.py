import math
import random
import time
from collections import deque, Counter

from frontend.sudoku_generator import SudokuGenerator


class Cell:
    def __init__(self, row, col, grid):
        self.row = row
        self.col = col
        self.grid = grid

    def __str__(self):
        return f'({self.row}, {self.col})'


SOLVE_TIME_LIMIT = 15


class SudokuSolver:
    def solve(self, board: list, start_time, limit=SOLVE_TIME_LIMIT):
        raise NotImplemented


class CSPSolver(SudokuSolver):
    def __init__(self):
        self._board = []
        self._size = 0
        self._empty_cells = set()
        self._domains = {}
        self._empty_cells_in_rows = {}
        self._empty_cells_in_cols = {}
        self._empty_cells_in_grids = {}
        self._related_cells = {}
        self._assignment = {}
        self._start_time = None

    def solve(self, board: list, start_time, limit=SOLVE_TIME_LIMIT):
        """
        Solve function
        - entry point of this solve algorithm
        - call setup functions and the backtracking search function
        """
        self._reset()
        self._start_time = time.time()
        self._board = board
        self._size = len(self._board)
        self._find_empty_cells()
        self._find_related_cells()
        self._get_initial_domains()
        return self._fill_cell()

    def _find_empty_cells(self):
        self._empty_cells_in_rows = {row: set() for row in range(self._size)}
        self._empty_cells_in_cols = {col: set() for col in range(self._size)}
        self._empty_cells_in_grids = {grid: set() for grid in range(self._size)}
        subgrid_row = math.floor(self._size ** 0.5)
        subgrid_col = self._size // subgrid_row
        for row in range(self._size):
            for col in range(self._size):
                if self._board[row][col] == 0:
                    grid_index = col // subgrid_col + row // subgrid_row * (self._size // subgrid_col)
                    cell = Cell(row, col, grid_index)
                    self._empty_cells.add(cell)
                    self._empty_cells_in_rows[row].add(cell)
                    self._empty_cells_in_cols[col].add(cell)
                    self._empty_cells_in_grids[grid_index].add(cell)
                    self._assignment[cell] = 0

    def _get_initial_domains(self):
        """
        Initial pruning
        - initial assignment of each empty cell's domain
        - call function _ac_3 to further reduce initial domains
        """
        for cell in self._empty_cells:
            row = cell.row
            col = cell.col
            self._domains[cell] = set(range(1, self._size + 1)) - set(self._board[row]) - \
                                  set([row[col] for row in self._board]) - set(self._get_subgrid(row, col))
        for cell in self._empty_cells:
            self._ac_3(cell)

    def _fill_cell(self):
        """
        Backtrack search
        - recursive backtracking
        """
        if time.time() - self._start_time > SOLVE_TIME_LIMIT:
            return False
        if len(self._empty_cells) == 0:
            return self._board
        cell = self._mrv()
        self._empty_cells.remove(cell)
        original_domains = {cell: domain.copy() for cell, domain in self._domains.items()}
        for value in self._arrange_value(cell):
            self._assignment[cell] = value
            self._domains[cell] = set()
            if self._ac_3(cell):
                if self._fill_cell():
                    self._board[cell.row][cell.col] = value
                    return self._board
            self._assignment[cell] = 0
            self._domains = original_domains
        self._empty_cells.add(cell)
        return False

    def _get_subgrid(self, row, col):
        subgrid_row = math.floor(self._size ** 0.5)
        subgrid_col = self._size // subgrid_row
        row_start = (row // subgrid_row) * subgrid_row
        col_start = (col // subgrid_col) * subgrid_col
        return [self._board[i][j] for i in range(row_start, row_start + subgrid_row) for j in
                range(col_start, col_start + subgrid_col)]

    def _mrv(self):
        """
        MRV
        - selecting cell with the least legal values
        - call function _degree_heuristic if there is a tie
        """
        mrv = set()
        min_domain_size = self._size
        for cell in self._empty_cells:
            domain_size = len(self._domains[cell])
            if domain_size == min_domain_size:
                mrv.add(cell)
            elif domain_size < min_domain_size:
                min_domain_size = domain_size
                mrv = {cell}
        if len(mrv) == 1:
            selected = next(iter(mrv))
            return selected

        return self._degree_heuristic(mrv)

    def _degree_heuristic(self, mrv):
        """
        Degree heuristic
        - used as tiebreaker for selecting cell, called by function mrv
        - check which cell has more unassigned related cells (the highest degree)
        """
        highest_degree = 0
        selected_cell = next(iter(mrv))
        for cell in mrv:
            degree = 0
            for related_cell in self._related_cells[cell]:
                if self._assignment[related_cell] == 0:
                    degree += 1
            if degree > highest_degree:
                highest_degree = degree
                selected_cell = cell
        return selected_cell

    def _arrange_value(self, cell):
        """
        Least constraining heuristic
        - check the domain of param cell's neighbor (row, col, grid)
        - count appearances of each domain value and arrange them in ascending order
        """
        domains = self._domains[cell]
        if len(domains) == 1:
            return domains

        domain_count = Counter()
        domain_count.update(self._domains[cell])
        for empty_cell in self._empty_cells:
            if empty_cell in self._related_cells[cell]:
                domain_count.update(self._domains[empty_cell])
        sorted_domains = sorted(domain_count.keys(), key=lambda key: domain_count[key])
        domains = [domain for domain in sorted_domains if domain in self._domains[cell]]
        return domains

    def _ac_3(self, cell):
        """
        AC-3 algorithm
        - called after each cell assignment
        - inference with MAC
        """
        arcs = deque()
        for empty_cell in self._empty_cells:
            if empty_cell in self._related_cells[cell]:
                arcs.append((empty_cell, cell))
        while arcs:
            arc = arcs.popleft()
            cell_i = arc[0]
            cell_j = arc[1]
            if self._revise(cell_i, cell_j):
                if not self._domains[cell_i]:
                    return False
                for empty_cell in self._empty_cells:
                    if empty_cell != cell_i and empty_cell != cell_j and empty_cell in self._related_cells[cell_i]:
                        arcs.append((empty_cell, cell_i))
        return True

    def _revise(self, cell_i, cell_j):
        """
        part of ac-3, revise domains base on constraints
        """
        i_domains = self._domains[cell_i]
        j_domains = self._domains[cell_j]
        domain_changed = False
        if len(j_domains) == 1 and len(i_domains) == 1:
            i_domain = next(iter(i_domains))
            if i_domain in j_domains:
                i_domains.clear()
                domain_changed = True
        elif not j_domains:
            j_assignment = self._assignment[cell_j]
            if j_assignment in i_domains:
                i_domains.remove(j_assignment)
                domain_changed = True
        unique_candidate_updated = self._update_unique_candidate(cell_i)
        return domain_changed or unique_candidate_updated

    def _update_unique_candidate(self, cell):
        """
        Sudoku technique
        - check if cell is a unique candidate which has a domain value that is unique to neighbor cells
        - if the cell has a unique domain values which mean it is the only cell that can hold that value
        """
        i_domains = self._domains[cell]
        domain_changed = False
        related_list = [self._empty_cells_in_grids[cell.grid],
                        self._empty_cells_in_rows[cell.row],
                        self._empty_cells_in_cols[cell.col]]
        for related in related_list:
            if len(i_domains) <= 1:
                return domain_changed

            related_domains = set()
            related_cells = related - {cell}
            for related_cell in related_cells:
                related_domains.update(self._domains[related_cell])
            if related_domains:
                unique_domains = i_domains - related_domains
                if unique_domains:
                    self._domains[cell] = unique_domains
                    domain_changed = True

    def _find_related_cells(self):
        self._related_cells = {cell: set() for cell in self._empty_cells}
        for cell in self._empty_cells:
            self._related_cells[cell] = (self._empty_cells_in_rows[cell.row] | self._empty_cells_in_cols[cell.col] |
                                         self._empty_cells_in_grids[cell.grid])
            self._related_cells[cell].remove(cell)

    def _reset(self):
        self._board = []
        self._size = 0
        self._empty_cells = set()
        self._domains = {}
        self._empty_cells_in_rows = {}
        self._empty_cells_in_cols = {}
        self._empty_cells_in_grids = {}
        self._related_cells = {}
        self._assignment = {}
        self._start_time = None


class BruteForceSolver(SudokuSolver):
    def solve(self, board, start_time, limit=SOLVE_TIME_LIMIT):
        if time.time() - start_time > limit:
            return False
        n = len(board)
        empty = self.find_empty(board)
        if not empty:
            return board
            # return True
        row, col = empty
        for num in self.get_choices(board, row, col):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve(board, start_time):
                    return board
                    # return True
                board[row][col] = 0
        return False

    def fill_naked_single(self, board):
        changed = False
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 0:
                    choices = self.get_choices(board, row, col)
                    print(choices)
                    if len(choices) == 1:
                        board[row][col] = choices[0]
                        changed = True
                        print(row, col, choices)
        return changed

    def find_empty(self, board):
        n = len(board)
        min_choices = n + 1
        min_row, min_col = None, None
        for row in range(n):
            for col in range(n):
                if board[row][col] == 0:
                    choices = self.get_choices(board, row, col)
                    num_choices = len(choices)
                    # if num_choices == 0:
                    #     return None
                    if num_choices < min_choices:
                        min_choices = num_choices
                        min_row, min_col = row, col
        if min_row is None and min_col is None:
            return None
        return min_row, min_col

    def get_choices(self, board, row, col):
        n = len(board)
        choices = set(range(1, n + 1)) - set(self.get_row(board, row)) - set(self.get_col(board, col)) - set(
            self.get_subgrid(board, row, col))
        choices = list(choices)
        random.shuffle(choices)
        return choices

    def get_row(self, board, row):
        return board[row]

    def get_col(self, board, col):
        return [board[row][col] for row in range(len(board))]

    def is_valid(self, board, row, col, num):
        n = len(board)
        # Check row and column
        for i in range(n):
            if board[row][i] == num or board[i][col] == num:
                return False
        # Check subgrid
        subgrid_size = int(n ** 0.5)
        row_start = (row // subgrid_size) * subgrid_size
        col_start = (col // subgrid_size) * subgrid_size
        for i in range(row_start, row_start + subgrid_size):
            for j in range(col_start, col_start + subgrid_size):
                if board[i][j] == num:
                    return False
        return True

    def get_subgrid(self, board, row, col):
        size = len(board)
        subgrid_row = math.floor(size ** 0.5)
        subgrid_col = size // subgrid_row
        row_start = (row // subgrid_row) * subgrid_row
        col_start = (col // subgrid_col) * subgrid_col
        return [board[i][j] for i in range(row_start, row_start + subgrid_row) for j in
                range(col_start, col_start + subgrid_col)]


def print_board(board):
    for row in board:
        for num in row:
            print(num, end=" ")
        print()


size_25_puzzle = [[0, 15, 0, 2, 1, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 14, 24, 0, 11, 0, 23, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 12, 0, 2, 0, 0],
                    [0, 0, 7, 10, 0, 0, 0, 22, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 8, 9, 0, 0, 0, 0, 0],
                    [12, 0, 0, 0, 0, 0, 6, 0, 0, 0, 14, 0, 21, 24, 0, 1, 0, 0, 0, 0, 0, 0, 8, 0, 23],
                    [0, 0, 0, 0, 0, 16, 0, 0, 9, 0, 0, 0, 13, 18, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 15, 0, 25, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 3, 0, 7, 0, 0],
                    [0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 13, 0, 10, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 23, 0, 0, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 20, 0, 0, 0, 6, 0, 0],
                    [0, 9, 24, 25, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 12, 0],
                    [0, 0, 0, 3, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0],
                    [0, 0, 0, 11, 0, 20, 1, 0, 18, 3, 0, 0, 0, 7, 0, 24, 13, 25, 0, 0, 0, 2, 0, 0, 0],
                    [0, 0, 0, 18, 0, 2, 0, 0, 15, 6, 0, 10, 1, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 6, 23, 11, 0, 0, 0, 18, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 12],
                    [23, 0, 0, 16, 0, 10, 0, 0, 0, 14, 0, 0, 0, 0, 15, 20, 4, 0, 18, 21, 0, 0, 0, 0, 3],
                    [0, 0, 0, 0, 3, 0, 0, 0, 0, 16, 23, 0, 0, 0, 0, 0, 0, 18, 13, 15, 22, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 24, 14, 0, 0, 15, 0],
                    [0, 0, 11, 13, 0, 21, 23, 0, 0, 18, 0, 0, 12, 22, 24, 0, 0, 6, 1, 0, 0, 0, 0, 0, 20],
                    [0, 5, 0, 0, 9, 0, 0, 0, 17, 0, 0, 0, 20, 0, 21, 14, 3, 11, 10, 0, 0, 0, 0, 0, 0],
                    [3, 22, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 20, 0, 0, 0, 0, 0],
                    [17, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 16, 0, 0, 0, 0, 22, 0, 0, 0, 6, 0, 20, 3, 7],
                    [14, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 12, 0, 0, 0, 21, 0, 0, 0, 0],
                    [8, 0, 0, 0, 7, 13, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 1, 0, 12, 11, 0, 2],
                    [0, 16, 0, 0, 0, 0, 0, 10, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 23, 5, 0]]

if __name__ == "__main__":
    solver1 = BruteForceSolver()
    solver2 = CSPSolver()
    attempts = 100
    for solver in [solver2]:
        success = 0
        total_time = 0
        for n in range(attempts):
            generator = SudokuGenerator(16)
            puzzle = generator.generate()
            current_time = time.time()
            solution = solver.solve(puzzle, current_time)
            if solution:
                time_elapsed = time.time() - current_time
                total_time += time_elapsed
                success += 1
                # print_board(solution)
                print("Success")
            else:
                print("FAIL!!!")

        print(f"Success rate: {success / attempts}")
        if success:
            print(f"Average time: {total_time / success}")
