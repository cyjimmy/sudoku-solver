import sys

from PySide6.QtCore import QRunnable, Slot, QObject, Signal
import traceback


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.__result = None
        self.__finished_status = None
        self.__timer = None

    @property
    def finished_status(self):
        self.__finished_status = "Status: Failed" if self.result is None else "Status: Solved"
        return self.__finished_status

    @property
    def result(self):
        return self.__result

    @property
    def timer(self):
        return self.__timer

    @Slot()
    def run(self):
        try:
            self.__result, self.__timer = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(self.result)
        finally:
            self.signals.finished.emit()


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)
