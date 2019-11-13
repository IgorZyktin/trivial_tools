# -*- coding: utf-8 -*-
"""

    Инструменты простых вычислений

"""
# встроенные модули
import math
from typing import Union


def math_round(number: float, decimals: int = 0) -> float:
    """Округлить математическиим (не банковским) способом.

    Работает обычным математическим образом, в отличие от встроенной функции round(),
    которая использует банковское округление.

    :param number: число, которое требуется округлить
    :param decimals: сколько разрядов после запятой оставить
    :return: округлённое число с плавающей запятой

    >>> math_round(2.735, 2)
    2.74
    >>> round(2.735, 2)
    2.73
    """
    if math.isnan(number):
        return math.nan

    exp = number * 10 ** decimals
    if abs(exp) - abs(math.floor(exp)) < 0.5:
        return math.floor(exp) / 10 ** decimals
    return math.ceil(exp) / 10 ** decimals


def sep_digits(number: Union[int, float, str], precision: int = 2) -> str:
    """
    Вывести число с разделением на разряды

    >>> sep_digits('12345678')
    '12345678'

    >>> sep_digits(12345678)
    '12 345 678'

    >>> sep_digits(1234.5678)
    '1 234.57'

    >>> sep_digits(1234.5678, precision=4)
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
