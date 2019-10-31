# -*- coding: utf-8 -*-
"""

    Инструменты обработки текстового представления дат

"""
# встроенные модули
import time
from typing import Optional
from datetime import date, datetime


def parse_date(string: Optional[str]) -> Optional[date]:
    """
    Обработка даты (при возможности)
    """
    if string is not None:
        return datetime.strptime(string, '%Y-%m-%d').date()
    return None


def cur_time(format_string: str = '%H:%M:%S') -> str:
    """
    Получить строку с текущим временем в формате %H:%M:%S
    """
    return datetime.now().strftime(format_string)


def cur_time_ms() -> str:
    """
    Получить строку с текущим временем в формате %H:%M:%S.%f
    """
    return cur_time('%H:%M:%S.%f')


def time_to_str(moment: float, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Преобразовать timestamp в текстовую форму.

    :param moment: timestamp в виде float
    :param format_string: формат в котором надо оформить строку
    :return: текстовая форма времени
    """
    result = time.strftime(format_string, datetime.fromtimestamp(moment).timetuple())
    return result


def date_to_text(moment: date, format_string: str = "%Y-%m-%d") -> str:
    """
    Преобразовать время в виде date в текстовую форму
    """
    result = moment.strftime(format_string)
    return result


def datetime_to_text(moment: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Преобразовать время в виде datetime в текстовую форму
    """
    result = moment.strftime(format_string)
    return result
