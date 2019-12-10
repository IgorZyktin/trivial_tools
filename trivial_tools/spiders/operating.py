# -*- coding: utf-8 -*-
"""

    Обработка данных для пауков

"""
# встроенные модули
import re
from typing import Tuple


def analyze_channels(string: str,
                     pattern=re.compile(r'(\d+)([ABC])(x(.*)?)?')) -> Tuple[int, str, float]:
    """
    Разложить строку каналов на составляющие

    >>> analyze_channels('1Ax0.5')
    (1, 'A', 0.5)

    >>> analyze_channels('35C')
    (35, 'C', 1.0)
    """
    number, phase, _, mul = pattern.search(string).groups()
    result = int(number), phase.upper(), 1.0 if mul is None else float(mul)
    return result
