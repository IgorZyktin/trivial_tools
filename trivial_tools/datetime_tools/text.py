# -*- coding: utf-8 -*-
"""

    Инструменты обработки текстового представления дат

"""
# встроенные модули
import time
from datetime import date, datetime
from typing import Optional, Sequence, List


def parse_date(string: Optional[str], pattern: str = '%Y-%m-%d') -> Optional[date]:
    """
    Обработка даты (при возможности)
    """
    if string:
        return datetime.strptime(string, pattern).date()
    return None


def parse_dates(container: Sequence, pattern: str = '%Y-%m-%d') -> List[date]:
    """
    Распарсить множество дат
    """
    result = []
    for each in container:
        new_date = parse_date(each, pattern)
        if new_date is not None:
            result.append(new_date)
    return sorted(result)


def parse_datetime(string: Optional[str], pattern: str = '%Y-%m-%d %H:%M:%S') -> Optional[date]:
    """
    Обработка даты+время (при возможности)
    """
    if string:
        return datetime.strptime(string, pattern)
    return None


def parse_datetime_ms(string: Optional[str],
                      pattern: str = '%Y-%m-%d %H:%M:%S.%f') -> Optional[date]:
    """
    Обработка даты+время (при возможности)
    """
    return parse_datetime(string, pattern)


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


def datetime_to_text_ms(moment: datetime, format_string: str = "%Y-%m-%d %H:%M:%S.%f") -> str:
    """
    Преобразовать время в виде datetime в текстовую форму
    """
    result = datetime_to_text(moment, format_string)
    return result
