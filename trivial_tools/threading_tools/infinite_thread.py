# -*- coding: utf-8 -*-
"""

    Тред с бесконечным выполнением коллбэка

"""
# встроенные модули
from threading import Thread, current_thread

# сторонние модули
from loguru import logger


class InfiniteThread(Thread):
    """
    Тред, способный выдерживать исключения в рабочей функции
    """
    def run(self) -> None:
        """
        Аналогичный стандартному исполнитель, только в бесконечном цикле
        """
        while True:
            # noinspection PyBroadException
            try:
                self._target(*self._args, **self._kwargs)
            except Exception:
                logger.exception(f'Критический сбой в треде {current_thread()}!')
