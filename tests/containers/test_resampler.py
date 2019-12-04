# -*- coding: utf-8 -*-
"""

    Тесты ресемплировщика

"""
# встроенные модули
from datetime import datetime

# модули проекта
from containers.class_resampler import Resampler


def test_creation():
    """
    Проверка создания
    """
    r = Resampler()
    assert r.max_gap == 30
    assert r.datetime_index == 0


def test_str():
    """
    Проверка текстового представления
    """
    r = Resampler()
    assert str(r) == 'Resampler[None]'

    r = Resampler(40, 0)
    list(r.iter_push((datetime(2019, 12, 1, 12, 0, 0), 'A')))
    assert str(r) == 'Resampler[2019-12-01 12:00:00]'


def test_repr():
    """
    Проверка текстового представления
    """
    r = Resampler()
    assert repr(r) == 'Resampler(max_gap=30, datetime_index=0, placeholder=None)'

    r = Resampler(40, 4)
    assert repr(r) == 'Resampler(max_gap=40, datetime_index=4, placeholder=None)'

    r = Resampler(40, 4, 'Fail!')
    assert repr(r) == "Resampler(max_gap=40, datetime_index=4, placeholder='Fail!')"


def test_iter_push():
    """
    Должен выдавать генератор с набором заполнителей
    """
    r = Resampler()

    package = [
        (datetime(2019, 12, 1, 12, 0, 0), 'A'),
        (datetime(2019, 12, 1, 12, 0, 5), 'B'),
        (datetime(2019, 12, 1, 12, 0, 10), 'C'),
        (datetime(2019, 12, 1, 12, 0, 15), 'D'),
        (datetime(2019, 12, 1, 12, 0, 20), 'E')
    ]

    ref = 0
    for payload in package:
        for each in r.iter_push(payload):
            assert each[0].second == ref
            ref += 1


def test_same_time():
    """
    Проверка получения нескольких значений с одной меткой времени
    """
    r = Resampler()
    list(r.iter_push((datetime(2019, 12, 1, 12, 0, 0), 'A')))
    list(r.iter_push((datetime(2019, 12, 1, 12, 0, 0), 'B')))
    list(r.iter_push((datetime(2019, 12, 1, 12, 0, 0), 'C')))
    list(r.iter_push((datetime(2019, 12, 1, 12, 0, 0), 'D')))
    assert r.previous == [datetime(2019, 12, 1, 12, 0, 0), 'D']


def test_wrong_time():
    """
    Проверка получения значения с неправильным временем
    """
    r = Resampler()

    list(r.iter_push((datetime(2019, 12, 1, 12, 0, 9), 'A')))
    list(r.iter_push((datetime(2019, 12, 1, 12, 0, 0), 'B')))
    list(r.iter_push((datetime(2019, 12, 1, 12, 0, 15), 'C')))

    gen = r.iter_push((datetime(2019, 12, 1, 12, 0, 17), 'D'))

    assert next(gen) == [datetime(2019, 12, 1, 12, 0, 15), 'C']
    assert next(gen) == [datetime(2019, 12, 1, 12, 0, 16), 'C']


def test_empty_payload():
    """
    Проверить отсутствие срабатывания при подаче пустого значения
    """
    r = Resampler()
    list(r.iter_push(()))
    assert r.previous is None


def test_long_gap():
    """
    Проверить заполнение при слишком больших паузах
    """
    r = Resampler(max_gap=4, placeholder='null')

    package = [
        (datetime(2019, 12, 1, 12, 0, 0), 'A'),
        (datetime(2019, 12, 1, 12, 0, 4), 'B'),
        (datetime(2019, 12, 1, 12, 0, 8), 'C'),
        (datetime(2019, 12, 1, 12, 0, 15), 'D'),
        (datetime(2019, 12, 1, 12, 0, 19), 'E')
    ]

    ref = iter(['A', 'A', 'A', 'A',
                'B', 'B', 'B', 'B',
                'C',
                'null', 'null', 'null', 'null', 'null', 'null',
                'D', 'D', 'D', 'D'
                ])

    for payload in package:
        for each in r.iter_push(payload):
            assert next(ref) == each[-1]


def test_push():
    """
    Проверка алгоритма добавления без итераций
    """
    r = Resampler(max_gap=4, placeholder='null')
    assert r.push((datetime(2019, 12, 1, 12, 0, 0), 'A')) == []

    item_1 = r.push((datetime(2019, 12, 1, 12, 0, 4), 'B'))
    assert item_1 == [
        [datetime(2019, 12, 1, 12, 0, 0), 'A'],
        [datetime(2019, 12, 1, 12, 0, 1), 'A'],
        [datetime(2019, 12, 1, 12, 0, 2), 'A'],
        [datetime(2019, 12, 1, 12, 0, 3), 'A']
    ]

    r.clear()
    assert r.push((datetime(2019, 12, 1, 12, 0, 0), 'A')) == []
    for each_x, each_y in zip(item_1, r.iter_push((datetime(2019, 12, 1, 12, 0, 4), 'B'))):
        assert each_x == each_y
