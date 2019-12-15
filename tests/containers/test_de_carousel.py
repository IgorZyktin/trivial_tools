# -*- coding: utf-8 -*-
"""

    Тесты двусторонней карусели

"""
# сторонние модули
import pytest

# модули проекта
from trivial_tools.containers.class_de_carousel import DeCarousel


def test_creation():
    """
    Проверка создания
    """
    with pytest.raises(ValueError):
        DeCarousel()

    d = DeCarousel(window=2)
    assert d.window == 2
    assert len(d) == 0
    assert d.get_contents() == []
    assert d.extract() == []

    d = DeCarousel([1, 2, 3])
    assert len(d) == 3
    assert d.window == 3
    assert d.get_contents() == [1, 2, 3]
    assert d.extract() == [1, 2, 3]
    assert d.extract() == []

    d = DeCarousel([1, 2, 3], window=2)
    assert len(d) == 2
    assert d.window == 2
    assert d.get_contents() == [2, 3]
    assert d.extract() == [2, 3]
    assert d.extract() == []


def test_push():
    """
    Проверка добавления элемента
    """
    maxlen = 3
    d = DeCarousel(window=maxlen, sentinel=None)
    assert d.get_contents() == []

    x = d.push(1)
    assert d.get_contents() == [1]
    assert x is None

    x = d.push(2)
    assert d.get_contents() == [1, 2]
    assert x is None

    x = d.push(3)
    assert d.get_contents() == [1, 2, 3]
    assert x is None

    x = d.push(4)
    assert d.get_contents() == [2, 3, 4]
    assert x == 1

    x = d.push(5)
    assert d.get_contents() == [3, 4, 5]
    assert x == 2

    x = d.push(6)
    assert d.get_contents() == [4, 5, 6]
    assert x == 3


def test_len():
    """
    Проверка измерения длины
    """
    maxlen = 5
    d = DeCarousel(window=maxlen)
    for i in range(1, 10):
        d.push(i)
        assert len(d) == i if i < maxlen else maxlen
    assert len(d) == maxlen


def test_get_contents():
    """
    Не должно влиять на внутренности
    """
    d = DeCarousel([1, 2, 3])
    assert d.get_contents() == [1, 2, 3]
    assert d._data == [1, 2, 3]
    assert d._data == d.get_contents()

    d = DeCarousel([1, 2, 3], window=2)
    assert d.get_contents() == [2, 3]
    assert d._data == [3, 2]
    assert d._data != d.get_contents()


def test_str():
    """
    Проверка текстового представления
    """
    d = DeCarousel(window=4)
    assert str(d) == 'DeCarousel([], window=4)'

    d = DeCarousel([1, 2, 3])
    assert str(d) == 'DeCarousel([1, 2, 3], window=3)'

    d = DeCarousel([1, 2, 3], window=2)
    assert str(d) == 'DeCarousel([2, 3], window=2)'


def test_str_long():
    """
    Проверка текстового представления
    """
    d = DeCarousel(window=40)
    assert str(d) == 'DeCarousel([], window=40)'

    d = DeCarousel(range(100), window=40)
    assert str(d) == 'DeCarousel([60, 61, 62, ..., 97, 98, 99], len=40, window=40)'


def test_repr_long():
    """
    Проверка текстового представления
    """
    d = DeCarousel(window=40)
    assert repr(d) == 'DeCarousel([NULL], window=40)'

    d = DeCarousel(range(100), window=40)
    assert repr(d) == 'DeCarousel([60, 61, 62, ..., 97, 98, 99], len=40, window=40)'


def test_append():
    """
    Проверка добавления элемента
    """
    d = DeCarousel(window=4)
    assert len(d) == 0

    d.append(1)
    assert d.get_contents() == [1]
    assert d.left == 1
    assert d.right == 1

    d.append(2)
    assert d.get_contents() == [1, 2]
    assert d.left == 1
    assert d.right == 2

    d.append(3)
    assert d.get_contents() == [1, 2, 3]
    assert d.left == 1
    assert d.right == 3

    d.append(4)
    assert d.get_contents() == [1, 2, 3, 4]
    assert d.left == 1
    assert d.right == 4

    d.append(5)
    assert d.get_contents() == [2, 3, 4, 5]
    assert d.left == 2
    assert d.right == 5

    d.append(6)
    assert d.get_contents() == [3, 4, 5, 6]
    assert d.left == 3
    assert d.right == 6

    d.append(7)
    assert d.get_contents() == [4, 5, 6, 7]
    assert d.left == 4
    assert d.right == 7

    d.append(8)
    assert d.get_contents() == [5, 6, 7, 8]
    assert d.left == 5
    assert d.right == 8

    d.append(9)
    assert d.get_contents() == [6, 7, 8, 9]
    assert d.left == 6
    assert d.right == 9


def test_appendleft():
    """
    Проверка добавления элемента
    """
    d = DeCarousel(window=4)
    assert len(d) == 0

    with pytest.raises(NotImplementedError):
        d.appendleft(1)


def test_pop():
    """
    Проверка извлечения элемента
    """
    d = DeCarousel([1, 2, 3, 4, 5, 6, 7, 8, 9], window=4)
    assert d.get_contents() == [6, 7, 8, 9]
    assert d.left == 6
    assert d.right == 9

    x = d.pop()
    assert x == 9
    assert d.left == 6
    assert d.right == 8

    x = d.pop()
    assert x == 8
    assert d.left == 6
    assert d.right == 7

    x = d.pop()
    assert x == 7
    assert d.left == 6
    assert d.right == 6

    x = d.pop()
    assert x == 6
    assert d.left is None
    assert d.right is None


# def test_resize():
#     """
#     Проверка изменения размера
#     """
#     c = Carousel([1, 2, 3], window=2)
#     assert len(c) == 2
#     assert c.window == 2
#     assert c.get_contents() == [2, 3]
#
#     assert repr(c) == 'Carousel([2, 3], window=2)'
#     c.resize(5)
#     assert repr(c) == 'Carousel([2, 3, NULL, NULL, NULL], window=5)'
#
#     c.push(4)
#     c.push(5)
#
#     assert len(c) == 4
#     assert c.window == 5
#     assert c.get_contents() == [2, 3, 4, 5]
#     assert repr(c) == 'Carousel([2, 3, 4, 5, NULL], window=5)'
#
#     c.push(6)
#
#     assert len(c) == 5
#     assert c.window == 5
#     assert c.get_contents() == [2, 3, 4, 5, 6]
#     assert repr(c) == 'Carousel([2, 3, 4, 5, 6], window=5)'
#
#     c.resize(2)
#     assert repr(c) == 'Carousel([5, 6], window=2)'
#
#     assert len(c) == 2
#     assert c.window == 2
#     assert c.get_contents() == [5, 6]
#
#
# def test_resize_empty():
#     """
#     Проверка изменения размера пустой карусели
#     """
#     c = Carousel(window=2)
#     assert c.window == 2
#     assert repr(c) == 'Carousel([NULL, NULL], window=2)'
#
#     c.resize(5)
#     assert c.window == 5
#     assert repr(c) == 'Carousel([NULL, NULL, NULL, NULL, NULL], window=5)'
#
#     c.resize(3)
#     assert c.window == 3
#     assert repr(c) == 'Carousel([NULL, NULL, NULL], window=3)'
#
#
# def test_no_resize():
#     """
#     Проверка изменения размера при том же значении
#     """
#     c = Carousel(window=2)
#     assert c.window == 2
#     c.resize(c.window)
#     assert c.window == 2


def test_iter():
    """
    Проверка итерирования по карусели
    """
    base = [1, 2, 3]
    d = DeCarousel(base, window=4)
    for ref, value in zip(base, d):
        assert ref == value

    # убедимся, что не сломали список
    assert base == [1, 2, 3]


# def test_getitem_int():
#     """
#     Проверка обращения к элементу (целое как индекс)
#     """
#     c = Carousel(window=4)
#
#     with pytest.raises(IndexError):
#         assert c[0]
#
#     with pytest.raises(IndexError):
#         # noinspection PyTypeChecker
#         assert c['test']
#
#     c.push(1)
#     assert c[0] == 1
#     assert c[-1] == 1
#
#     with pytest.raises(IndexError):
#         assert c[2]
#
#     c.push(2)
#     assert c[0] == 1
#     assert c[1] == 2
#     assert c[-1] == 2
#     assert c[-2] == 1
#
#     c.push(3)
#     assert c[0] == 1
#     assert c[1] == 2
#     assert c[2] == 3
#     assert c[-1] == 3
#     assert c[-2] == 2
#     assert c[-3] == 1
#
#     c.push(4)
#     assert c[0] == 1
#     assert c[1] == 2
#     assert c[2] == 3
#     assert c[3] == 4
#     assert c[-1] == 4
#     assert c[-2] == 3
#     assert c[-3] == 2
#     assert c[-4] == 1
#
#     c.push(5)
#     assert c[0] == 2
#     assert c[1] == 3
#     assert c[2] == 4
#     assert c[3] == 5
#     assert c[-1] == 5
#     assert c[-2] == 4
#     assert c[-3] == 3
#     assert c[-4] == 2
#
#     c.push(6)
#     assert c[0] == 3
#     assert c[1] == 4
#     assert c[2] == 5
#     assert c[3] == 6
#     assert c[-1] == 6
#     assert c[-2] == 5
#     assert c[-3] == 4
#     assert c[-4] == 3
#
#     c.push(7)
#     assert c[0] == 4
#     assert c[1] == 5
#     assert c[2] == 6
#     assert c[3] == 7
#     assert c[-1] == 7
#     assert c[-2] == 6
#     assert c[-3] == 5
#     assert c[-4] == 4
#
#     c.push(8)
#     assert c[0] == 5
#     assert c[1] == 6
#     assert c[2] == 7
#     assert c[3] == 8
#     assert c[-1] == 8
#     assert c[-2] == 7
#     assert c[-3] == 6
#     assert c[-4] == 5
#
#
# def test_getitem_slice():
#     """
#     Проверка обращения к элементу (срез как индекс)
#     """
#     c = Carousel(window=4)
#
#     assert c[:] == []
#
#     for i in range(1, 9):
#         c.push(i)
#
#     assert c[0] == 5
#     assert c[1] == 6
#     assert c[2] == 7
#     assert c[3] == 8
#
#     assert c[:] == [5, 6, 7, 8]
#
#     assert c[:4] == [5, 6, 7, 8]
#     assert c[:3] == [5, 6, 7]
#     assert c[:2] == [5, 6]
#     assert c[:1] == [5]
#
#     assert c[1:] == [6, 7, 8]
#     assert c[2:] == [7, 8]
#     assert c[3:] == [8]
#     assert c[4:] == []
#
#     c.push(9)
#
#     assert c[:] == [6, 7, 8, 9]
#
#     assert c[:4] == [6, 7, 8, 9]
#     assert c[:3] == [6, 7, 8]
#     assert c[:2] == [6, 7]
#     assert c[:1] == [6]
#
#     assert c[1:] == [7, 8, 9]
#     assert c[2:] == [8, 9]
#     assert c[3:] == [9]
#     assert c[4:] == []
#
#     c.push(10)
#
#     assert c[:] == [7, 8, 9, 10]
#
#     assert c[1:] == [8, 9, 10]
#     assert c[2:] == [9, 10]
#     assert c[3:] == [10]
#     assert c[4:] == []
#
#     assert c[0:3:2] == [7, 9]
#
#
# def test_setitem_int():
#     """
#     Проверка подмены элемента
#     """
#     c = Carousel(window=3)
#
#     with pytest.raises(IndexError):
#         c[0] = 1
#
#     c.push(1)
#     c.push(2)
#     c.push(3)
#     c.push(4)
#     c.push(5)
#     c.push(6)
#
#     assert c[0] == 4
#     assert c[1] == 5
#     assert c[2] == 6
#
#     assert c[-1] == 6
#     assert c[-2] == 5
#     assert c[-3] == 4
#
#     assert c[:] == [4, 5, 6]
#
#     c[0] = 9
#     assert c[0] == 9
#     assert c[1] == 5
#     assert c[2] == 6
#
#     c[1] = 7
#     assert c[0] == 9
#     assert c[1] == 7
#     assert c[2] == 6
#
#     c[2] = 4
#     assert c[0] == 9
#     assert c[1] == 7
#     assert c[2] == 4
#
#     c[-1] = 78
#     assert c[0] == 9
#     assert c[1] == 7
#     assert c[2] == 78
#
#     with pytest.raises(IndexError):
#         c[75] = 6
#
#
# def test_setitem_slice():
#     """
#     Проверка подмены элемента
#     """
#     c = Carousel(window=4)
#
#     with pytest.raises(IndexError):
#         c[:] = [9, 8, 7, 6]
#
#
# def test_is_sentinel():
#     """
#     Проверка выдачи пустого элемента
#     """
#     c = Carousel(window=2)
#
#     with pytest.raises(IndexError):
#         _ = c[0]
