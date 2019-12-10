# -*- coding: utf-8 -*-
"""

    Тесты ресемплировщика

"""
# встроенные модули
from datetime import datetime

# сторонние модули
import pytest

# модули проекта
from trivial_tools.containers.class_time_slice import TimeSlice


@pytest.fixture()
def var_a():
    return datetime(2019, 12, 1, 12, 0, 0), 'A'


@pytest.fixture()
def var_b():
    return datetime(2019, 12, 1, 12, 0, 1), 'B'


@pytest.fixture()
def var_c():
    return datetime(2019, 12, 1, 12, 0, 2), 'C'


@pytest.fixture()
def var_d():
    return datetime(2019, 12, 1, 12, 0, 3), 'D'


@pytest.fixture()
def var_e():
    return datetime(2019, 12, 1, 12, 0, 4), 'E'


@pytest.fixture()
def var_f():
    return datetime(2019, 12, 1, 12, 0, 5), 'F'


@pytest.fixture()
def var_u():
    return datetime(2019, 12, 1, 12, 0, 10), 'U'


@pytest.fixture()
def var_v():
    return datetime(2019, 12, 1, 12, 0, 15), 'V'


@pytest.fixture()
def var_w():
    return datetime(2019, 12, 1, 12, 0, 20), 'W'


@pytest.fixture()
def var_x():
    return datetime(2019, 12, 1, 12, 0, 25), 'X'


@pytest.fixture()
def var_y():
    return datetime(2019, 12, 1, 12, 0, 30), 'Y'


@pytest.fixture()
def var_z():
    return datetime(2019, 12, 1, 12, 0, 35), 'Z'


def test_creation():
    """
    Проверка создания
    """
    t = TimeSlice()
    assert t.maxlen == 1
    assert t.datetime_index == 0


def test_str():
    """
    Проверка текстового представления
    """
    t = TimeSlice()
    assert str(t) == 'TimeSlice([], maxlen=1)'

    t = TimeSlice(1, 40)
    assert str(t) == 'TimeSlice([], maxlen=40)'


def test_repr():
    """
    Проверка текстового представления
    """
    t = TimeSlice()
    assert repr(t) == 'TimeSlice([NULL], maxlen=1)'

    t = TimeSlice(4, 40)
    assert repr(t) == 'TimeSlice([NULL, NULL, NULL, ..., NULL, NULL, NULL], maxlen=40)'

    t = TimeSlice(4, 40, 'Fail!')
    assert repr(t) == 'TimeSlice([NULL, NULL, NULL, ..., NULL, NULL, NULL], maxlen=40)'


def test_push_dense(var_a, var_b, var_c, var_d, var_e, var_f):
    """
    Проверка алгоритма добавления
    """
    t = TimeSlice(maxlen=4)

    t.push(var_a)
    assert t.newest == int(var_a[0].timestamp())

    t.push(var_b)
    assert t.newest == int(var_b[0].timestamp())

    t.push(var_c)
    assert t.newest == int(var_c[0].timestamp())

    t.push(var_d)
    assert t.newest == int(var_d[0].timestamp())

    t.push(var_e)
    assert t.newest == int(var_e[0].timestamp())

    t.push(var_f)
    assert t.newest == int(var_f[0].timestamp())

    assert t.get_contents() == [var_c, var_d, var_e, var_f]
    assert len(t) == 4


def test_push_sparse(var_u, var_v, var_w, var_x, var_y, var_z):
    """
    Проверка алгоритма добавления
    """
    t = TimeSlice(maxlen=14)
    assert t.get_oldest() is None

    t.push(var_u)
    assert t.get_contents() == [var_u]
    assert t.delta == 0
    assert t.get_oldest() == var_u

    t.push(var_v)
    assert t.get_contents() == [var_u, var_v]
    assert t.delta == 5
    assert t.get_oldest() == var_u

    t.push(var_w)
    assert t.get_contents() == [var_u, var_v, var_w]
    assert t.delta == 10
    assert t.get_oldest() == var_u

    t.push(var_x)
    assert t.get_contents() == [var_u, var_v, var_w, var_x]
    assert t.delta == 15
    assert t.get_oldest() == var_u

    t.push(var_y)
    assert t.get_contents() == [var_v, var_w, var_x, var_y]
    assert t.delta == 15
    assert t.get_oldest() == var_v

    t.push(var_z)
    assert t.get_contents() == [var_w, var_x, var_y, var_z]
    assert t.delta == 15
    assert t.get_oldest() == var_w


def test_not_filled(var_u, var_v, var_w, var_x, var_y, var_z):
    """
    Проверка на заполненность
    """
    t = TimeSlice(maxlen=14)

    t.push(var_u)
    assert t.not_filled

    t.push(var_v)
    assert t.not_filled

    t.push(var_w)
    assert t.not_filled

    t.push(var_x)
    assert t.not_filled

    t.push(var_y)
    assert not t.not_filled

    t.push(var_z)
    assert not t.not_filled


def test_getitem(var_u):
    """
    Проверка на доступ к элементам
    """
    t = TimeSlice(maxlen=14)
    t.push(var_u)

    with pytest.raises(NotImplementedError):
        t[0] = 9

    with pytest.raises(NotImplementedError):
        _ = t[0]


def test_same_time(var_a, var_b, var_c, var_d):
    """
    Проверка вставки элементов с одним временем или устаревшим временем
    """
    t = TimeSlice(maxlen=14)

    t.push(var_a)
    assert len(t) == 1

    t.push(var_b)
    assert len(t) == 2

    t.push(var_a)
    assert len(t) == 2

    t.push(var_b)
    assert len(t) == 2
