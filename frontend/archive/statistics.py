from sudoku_generator import SudokuGenerator
from sudoku_solver import BruteForceSolver
import time
TIME_LIMIT = {9: 5, 12: 15, 16: 16, 25: 160}


def add_to_hash_list(hash, key, value):
    if key not in hash:
        hash[key] = [value]
    else:
        hash[key].append(value)


def add_to_hash_int(hash, key):
    if key not in hash:
        hash[key] = 1
    else:
        hash[key] += 1


if __name__ == "__main__":
    print("Starting Statistics Run")
    # board_sizes = [9, 12, 16, 25]
    board_sizes = [9]
    solver1 = BruteForceSolver()
    num_boards = 30
    retry = 10
    board_to_times = {}
    board_to_solve = {}
    board_to_retry = {}
    for board_size in board_sizes:
        print("Running Board Size", board_size)
        generator = SudokuGenerator(board_size)
        for _ in range(num_boards):
            board = generator.generate()
            start_time = time.time()
            tries = 0
            for i in range(retry):
                print("Board", _, "Retry", i)
                temp_start_time = time.time()
                solution = solver1.solve(board, temp_start_time, limit=TIME_LIMIT[board_size])
                tries += 1
                if solution:
                    break
            end_time = time.time()
            duration = end_time - start_time
            add_to_hash_list(board_to_times, board_size, duration)
            board_to_retry[board_size] = tries
            if solution:
                add_to_hash_int(board_to_solve, board_size)
            else:
                print("Failed", solution, ",Tries", tries)
    print(board_to_solve)
    print(board_to_times)
