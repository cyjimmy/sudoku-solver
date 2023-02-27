import random
import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox

import dll
import generatepuzzle
import generatepuzzledialog
import mainwindow

Global_Window_DLL = dll.DoublyLinkedList()


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

    @staticmethod
    def on_click_exit():
        sys.exit(0)


class GeneratePuzzleWindow(QtWidgets.QMainWindow, generatepuzzle.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButtonGeneratePuzzle.clicked.connect(self.on_click_generate)
        self.pushButtonLoadPuzzle.clicked.connect(self.on_click_load)
        self.pushButtonGoBack.clicked.connect(self.on_click_go_back)
        self.incorrect_file_format_dialog = None
        self.generate_puzzle_dialog = None

    def on_click_load(self):
        filename = QtWidgets.QFileDialog.getOpenFileNames(self, caption="Choose a TXT puzzle to load",
                                                          dir="./", filter="Text files (*.txt)")
        print(filename)

        """
        # [TODO] Some logic that determines if the file format is correct/data inside the file is correct? If it's not,
        # [TODO] the raised exception is displayed in a dialog box. Set the text of the dialog box by
        """

        raise_exception = random.random()
        message = f"The data inside the file {filename[0]} is invalid. Please provide valid data."
        if len(filename[0]) != 0:  # make sure user didn't press 'cancel'
            if raise_exception >= 0.5:  # this is random for now. No logic here!
                QMessageBox.critical(self, "IncorrectFileFormatException", message)

    def on_click_generate(self):
        self.generate_puzzle_dialog = GeneratePuzzleDialog(self)
        self.generate_puzzle_dialog.exec()

    def on_click_go_back(self):
        node = Global_Window_DLL.get_node(self)
        node.prev.data.show()
        node.data.hide()


class GeneratePuzzleDialog(generatepuzzledialog.Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.sudokuSizeSelector.addItems(["1", "2", "3", "4"])
        self.buttonBox.accepted.connect(self.on_click_ok)

    def on_click_ok(self):
        print("hi")


class Driver:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        main_window = MainWindow()
        Global_Window_DLL.append(main_window)
        main_window.show()

        self.app.exec()


d = Driver()
