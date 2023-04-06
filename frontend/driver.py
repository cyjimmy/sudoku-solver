import multiprocessing
import sys
import time
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QDialog, QMessageBox, QGridLayout, QWidget, QScrollArea

import custom_exceptions
import dll
import generatepuzzle
import generatepuzzledialog
import loadedsudokuwindow
import mainwindow
import solver
from grid import Grid, GridSize
from sudoku_solver import BruteForceSolver, SudokuSolver, CSPSolver, CSPMultiProcessHandler
from worker import Worker

Global_Window_DLL = dll.DoublyLinkedList()


TIME_LIMIT = {9: 5, 12: 15, 16: 16, 25: 30, 100: 30}
CSP_TIME_LIMIT = {9: 1, 12: 1, 16: 2, 25: 5, 100: 5}


class MainWindow(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButtonCreatePuzzle.clicked.connect(self.on_click_create)
        self.pushButtonExit.clicked.connect(self.on_click_exit)
        self.actionExit.triggered.connect(self.on_click_exit)

    def on_click_create(self):
        Global_Window_DLL.append(GeneratePuzzleWindow())
        node = Global_Window_DLL.get_node(self)
        node.next.data.show()
        node.data.hide()
        Global_Window_DLL.print()

    def on_click_exit(self):
        node = Global_Window_DLL.get_node(self)
        node.data.close()
        Global_Window_DLL.delete(self)
        Global_Window_DLL.print()
        sys.exit(0)


class GeneratePuzzleWindow(QtWidgets.QMainWindow, generatepuzzle.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.grid_csp = None
        self.grid_brute = None
        self.setupUi(self)
        self.grid = None
        self.pushButtonGeneratePuzzle.clicked.connect(self.on_click_generate)
        self.pushButtonLoadPuzzle.clicked.connect(self.on_click_load)
        self.pushButtonGoBack.clicked.connect(self.on_click_go_back)
        self.incorrect_file_format_dialog = None
        self.generate_puzzle_dialog = None

    def on_click_load(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, caption="Choose a TXT puzzle to load",
                                                         dir="./", filter="Text files (*.txt)")

        """
        # [TODO] Some logic that determines if the file format is correct/data inside the file is correct? If it's not,
        # [TODO] the raised exception is displayed in a dialog box. Set the text of the dialog box by
        """

        if len(filename[0]) != 0:  # make sure user didn't press 'cancel'
            try:
                self.grid = Grid(None)
                self.grid.load(filename[0])
            except custom_exceptions.InvalidFileDataException as e:
                QMessageBox.critical(self, e.__class__.__name__, e.args[0])
            else:
                # print(self.grid.grid_size)
                Global_Window_DLL.append(LoadedSudokuWindow(self.grid))
                node = Global_Window_DLL.get_node(self)
                node.next.data.show()
                node.data.hide()

    def on_click_generate(self):
        self.generate_puzzle_dialog = GeneratePuzzleDialog(self)
        self.generate_puzzle_dialog.exec()

    def on_click_go_back(self):
        node = Global_Window_DLL.get_node(self)
        node.prev.data.show()
        node.data.close()
        Global_Window_DLL.delete(self)


class GeneratePuzzleDialog(generatepuzzledialog.Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        self.grid_csp = None
        self.grid_brute = None
        self.parent = parent
        super().__init__(self.parent)
        self.grid = None
        self.setupUi(self)
        self.sudokuSizeSelector.addItems([grid_size.name for grid_size in GridSize])
        self.buttonBox.accepted.connect(self.on_click_ok)

    def on_click_ok(self):
        grid_size = self.sudokuSizeSelector.currentText()
        self.grid = Grid(GridSize[str(grid_size)])
        try:
            self.grid.generate()
        except KeyError as e:
            QMessageBox.critical(self, e.__class__.__name__, "Can't select Empty Grid Size!!")
        else:
            Global_Window_DLL.append(LoadedSudokuWindow(self.grid))
            node = Global_Window_DLL.get_node(self.parent)
            node.next.data.show()
            node.data.hide()


class LoadedSudokuWindow(QtWidgets.QMainWindow, loadedsudokuwindow.Ui_MainWindow):
    def __init__(self, grid):
        super().__init__()
        self.showMaximized()
        self.grid = grid
        self.setupUi(self)
        self.pushButtonBack.clicked.connect(self.on_click_go_back)
        self.pushButtonExit.clicked.connect(self.on_click_exit)
        self.parent_layout = QGridLayout()
        self.build_grid()
        self.brute_window = None
        self.csp_window = None
        self.brute_worker = None
        self.csp_worker = None
        self.pushButtonBrute.clicked.connect(self.on_click_brute)
        self.pushButtonCSP.clicked.connect(self.on_click_csp)
        self.brute_threadpool = None
        self.csp_threadpool = None
        # print(self.grid)
        # print(self.grid.puzzle)

    def on_click_brute(self):
        if self.grid.grid_size["blocks"] > 25:
            # QMessageBox.information(self, "Brute Force Disabled", "Sorry, for large puzzles like this, Brute force "
            #                                                       "is disabled!")
            pass
        else:
            if self.brute_window:
                self.brute_window.close()
            self.brute_window = SolverWindow(self.grid.clone(), "Brute Force/Heuristic", BruteForceSolver())

            self.brute_window.show()

            self.brute_worker = Worker(self.brute_window.solve)
            self.brute_worker.setAutoDelete(True)
            self.brute_worker.signals.finished.connect(partial(self.grid_solved, self.brute_worker))

            self.brute_threadpool = QThreadPool()
            self.brute_threadpool.setMaxThreadCount(1)
            self.brute_threadpool.start(self.brute_worker)

    def grid_solved(self, worker):
        print(worker.result)
        self.brute_window.update_widget(worker.result, worker.finished_status, worker.timer)

    def grid_solved_csp(self, worker):
        print(worker.result)
        self.csp_window.update_widget(worker.result, worker.finished_status, worker.timer)

    def on_click_csp(self):
        if self.csp_window:
            self.csp_window.close()
        self.csp_window = SolverWindow(self.grid.clone(), "CSP", CSPSolver())

        self.csp_window.show()

        self.csp_worker = Worker(self.csp_window.solve)
        self.csp_worker.setAutoDelete(True)
        self.csp_worker.signals.finished.connect(partial(self.grid_solved_csp, self.csp_worker))

        self.csp_threadpool = QThreadPool()
        self.csp_threadpool.setMaxThreadCount(1)
        self.csp_threadpool.start(self.csp_worker)

    def on_click_go_back(self):
        node = Global_Window_DLL.get_node(self)
        node.prev.data.show()
        node.data.close()
        Global_Window_DLL.delete(self)
        Global_Window_DLL.print()

    def on_click_exit(self):
        if self.brute_window is not None:
            self.brute_window.close()
        if self.csp_window is not None:
            self.csp_window.close()
        node = Global_Window_DLL.get_node(self)
        temp = node
        while temp.prev is not None:
            temp.data.close()
            temp = temp.prev
            Global_Window_DLL.delete(temp.next.data)
        temp.data.close()
        Global_Window_DLL.delete(temp.data)

    def build_grid(self):
        # if len(self.grid.puzzle) > 25:
        #     self.pushButtonBrute.setDisabled(True)

        for block in self.grid.blocks:
            layout = QGridLayout()
            for cell in block.cells:
                layout.addWidget(cell.label_widget, cell.block_row, cell.block_col)
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setSpacing(2)
            self.parent_layout.addLayout(layout, block.row, block.col)

        widget = QWidget()
        widget.setLayout(self.parent_layout)
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        self.verticalLayout.addWidget(scroll)


class SolverWindow(QtWidgets.QMainWindow, solver.Ui_MainWindow):
    def __init__(self, grid, algorithm, sudoku_solver: SudokuSolver):
        super().__init__()
        self.showMaximized()
        self.grid = grid
        self.setupUi(self)
        self.parent_layout = QGridLayout()
        self.labelAlgorithm.setText(algorithm)
        self.labelSolveStatus.setText("Status: Pending")
        self.labelTime.setText("Loading Puzzle....WAIT!!!")
        self.pushButtonExit.clicked.connect(self.on_click_exit)
        self.scroll = None
        self.__build_grid()

        self.solver = sudoku_solver

    def update_widget(self, result, finished_status, timer):
        if isinstance(result, list):
            self.labelSolveStatus.setText(str(finished_status))
            self.labelTime.setText(f"Solved in {round(timer, 6)} sec")
            self.verticalLayout.removeWidget(self.scroll)
            self.grid = self.grid.clone(puzzle=result)
            self.__build_grid()
        else:
            self.labelSolveStatus.setText("Failed to Solve")
            self.labelTime.setText(f"Failed in {round(timer, 6)} sec")

    def solve(self):
        time.sleep(0.5)

        self.labelTime.setText("Background Thread In progress....")
        size = len(self.grid.puzzle)
        start = time.time()
        limit = TIME_LIMIT[size]
        if isinstance(self.solver, CSPSolver):
            limit = CSP_TIME_LIMIT[size]
        for i in range(10):
            if isinstance(self.solver, CSPSolver) and size > 12:
                if i > 1 and size == 25:
                    limit = 30
                if i > 4 and size == 16:
                    limit = 20
                result = CSPMultiProcessHandler().process_pool_handler(self.grid.puzzle, limit)
                print(time.time() - start)
            else:
                result = self.solver.solve(self.grid.puzzle, time.time(), limit=limit)
            print("Finished Try", i, "with time limit", limit)
            if result:
                break
        end = time.time() - start
        if isinstance(result, list):
            print(result)
        return result, end

    def __build_grid(self):
        self.parent_layout = QGridLayout()
        for block in self.grid.blocks:
            layout = QGridLayout()
            for cell in block.cells:
                layout.addWidget(cell.label_widget, cell.block_row, cell.block_col)
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setSpacing(2)
            self.parent_layout.addLayout(layout, block.row, block.col)

        widget = QWidget()
        widget.setLayout(self.parent_layout)
        self.scroll = QScrollArea()
        self.scroll.setWidget(widget)
        self.scroll.setWidgetResizable(True)
        self.verticalLayout.addWidget(self.scroll)

    def on_click_exit(self):
        self.close()


class Driver:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        main_window = MainWindow()
        Global_Window_DLL.append(main_window)
        main_window.show()

        self.app.exec()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    d = Driver()
