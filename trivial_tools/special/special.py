# -*- coding: utf-8 -*-
"""

    Особые инструменты

"""
# встроенные модули
from typing import NoReturn, Optional, Type

# модули проекта
from trivial_tools.formatters.base import decorate


def fail(message: str, reason: Type[Exception] = RuntimeError,
         raise_from: Optional[Exception] = None) -> NoReturn:
    """Выбросить исключение с заданным текстовым сообщением

    :param message: сообщение, которое необходимо передать
    :param reason: исключение, которые необходимо вызвать
    :param raise_from: возбудить исключение из переданного экземпляра
    :return: нет возврата
    """
    if isinstance(reason, (UnicodeDecodeError, UnicodeTranslateError, UnicodeEncodeError)):
        # Unicode ошибки нельзя выбросить просто с одним текстовым сообщением
        raise

    if isinstance(raise_from, Exception):
        # выбрасываем из экземпляра класса исключений
        name = raise_from.__class__.__name__
        instance = type(raise_from)(decorate(f'{name}: {message}'))
        raise instance from raise_from

    # выбрасываем из класса исключений
    name = reason.__name__

    # В настоящий момент (python 3.7) нет способа корректно указать исключения в аннотациях типов.
    # noinspection PyCallingNonCallable
    raise reason(decorate(f'{name}: {message}'))
