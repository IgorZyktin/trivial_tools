# -*- coding: utf-8 -*-
"""

    Работа с распечаткой из pandas

"""
# сторонние модули
import pandas as pd


def pandas_output(*args, max_rows: int = -1, max_columns: int = 100):
    """
    Распечатать с настройками контекста
    """
    with pd.option_context(
            'display.max_rows', max_rows,
            'display.max_columns', max_columns,
            'display.expand_frame_repr', False
    ):
        print(*args)
