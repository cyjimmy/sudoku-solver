import sys
import traceback
from multiprocessing import Process, Queue

from PySide6.QtCore import QRunnable, Slot, QObject, Signal


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
        self.queue = Queue()

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

    def __helper(self, queue, fn):
        ret = fn()
        queue.put(ret)

    @Slot()
    def run(self):
        try:
            args = [self.queue, self.fn]
            p = Process(target=self.__helper, args=args)
            p.start()
            self.__result, self.__timer = self.queue.get()
            p.join()
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
