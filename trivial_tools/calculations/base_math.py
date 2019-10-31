# -*- coding: utf-8 -*-
"""

    Инструменты простых вычислений

"""
# встроенные модули
import math


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
