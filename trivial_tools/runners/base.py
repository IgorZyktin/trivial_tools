# -*- coding: utf-8 -*-
"""

    Инструменты запуска

"""
# встроенные модули
import time
from functools import wraps
from typing import Callable, Union, Tuple, Any

# сторонние модули
from loguru import logger

# модули проекта
from trivial_tools.special.special import fail


def repeat_on_exceptions(repeats: int, case: Union[Exception, Tuple[Exception]],
                         delay: float = 1.0, verbose: bool = True) -> Callable:
    """Декоратор, заставляющий функцию повторить операцию при выбросе исключения.

    Инструмент добавлен для возможности повторной отправки HTTP запросов на серверах

    :param delay: время ожидания между попытками
    :param repeats: сколько раз повторить (0 - повторять бесконечно)
    :param case: при каком исключении вызывать повтор
    :return: возвращает фабрику декораторов
    """
    def decorator(func: Callable) -> Callable:
        """
        Декоратор
        """
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """
            Враппер
            """
            iteration = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                    break
                except case as exc:
                    iteration += 1

                    if verbose:
                        logger.warning(f'Исключение {type(exc)} в функции {func.__name__}'
                                        f' (итерация {iteration})')

                    if repeats and iteration > repeats:
                        fail(exc)

                    time.sleep(delay)

            return result
        return wrapper
    return decorator
