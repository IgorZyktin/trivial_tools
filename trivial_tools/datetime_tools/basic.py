# -*- coding: utf-8 -*-
"""

    Инструменты вычисления времени и дат

"""
# модули проекта
import calendar


def days_in_month(year: int, month: int) -> int:
    """
    Получить число дней в месяце

    >>> days_in_month(2016, 1)
    31

    >>> days_in_month(2019, 4)
    30
    """
    _, length = calendar.monthrange(year, month)
    return length


def hours_in_month(year: int, month: int) -> int:
    """
    Получить число часов в месяце

    >>> hours_in_month(2016, 1)
    744

    >>> hours_in_month(2019, 4)
    720
    """
    result = days_in_month(year, month) * 24
    return result
