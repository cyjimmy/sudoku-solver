class SudokuSolver:
    def solve(self, board: list):
        raise NotImplemented


class CSPSolver(SudokuSolver):
    def solve(self, board: list):
        return False


class BruteForceSolver(SudokuSolver):
    def solve(self, board):
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
                if self.solve(board):
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
