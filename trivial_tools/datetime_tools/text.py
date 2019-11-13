# -*- coding: utf-8 -*-
"""

    Инструменты обработки текстового представления дат

"""
# встроенные модули
import time
from datetime import date, datetime
from typing import Optional, Sequence, List, Union

# модули проекта
from trivial_tools.calculations.base_math import math_round


def parse_date(string: Optional[str]) -> Optional[date]:
    """
    Обработка даты (при возможности)
    """
    if string is not None:
        return datetime.strptime(string, '%Y-%m-%d').date()
    return None


def parse_dates(container: Sequence) -> List[date]:
    """
    Распарсить множество дат
    """
    result = []
    for each in container:
        new_date = parse_date(each)
        if new_date is not None:
            result.append(new_date)
    return sorted(result)


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


def datetime_to_text_ms(moment: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Преобразовать время в виде datetime в текстовую форму
    """
    result = datetime_to_text(moment, format_string)
    return result


def sep(number: Union[int, float, str], precision: int = 2) -> str:
    """
    Вывести число с разделением на разряды

    >>> sep('12345678')
    '12345678'

    >>> sep(12345678)
    '12 345 678'

    >>> sep(1234.5678)
    '1 234.57'

    >>> sep(1234.5678, precision=4)
    '1 234.5678'
    """
    if isinstance(number, int):
        result = '{:,}'.format(number).replace(',', ' ')

    elif isinstance(number, float):
        result = '{:,}'.format(math_round(number, precision)).replace(',', ' ')
        if '.' in result:
            tail = result.rsplit('.')[-1]
            result += '0' * (precision - len(tail))

    else:
        result = str(number)

    return result
