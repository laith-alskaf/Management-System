# -*- coding: utf-8 -*-

"""
وحدة العامل (Worker) لتشغيل المهام الطويلة في خيط منفصل (Thread)
لتجنب تجميد واجهة المستخدم.
"""

from PyQt6.QtCore import QObject, pyqtSignal, QRunnable

class WorkerSignals(QObject):
    """
    تُعرّف الإشارات المتاحة من خيط العامل.

    Supported signals are:
    - finished: لا يوجد بيانات تُرسل.
    - error: `tuple` (نوع الاستثناء, بيانات الاستثناء, traceback).
    - result: `object` بيانات النتيجة من المهمة.
    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

class Worker(QRunnable):
    """
    فئة العامل التي يمكن تشغيلها في خيط منفصل باستخدام QThreadPool.
    """
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        """
        تنفيذ المهمة.
        """
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            # يمكنك تسجيل الخطأ هنا إذا أردت
            # import traceback
            # traceback.print_exc()
            self.signals.error.emit((type(e), e, e.__traceback__))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
