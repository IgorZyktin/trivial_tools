# -*- coding: utf-8 -*-
"""

    Тесты карусели

"""
# сторонние модули
import pytest

# модули проекта
from trivial_tools.containers.class_carousel import Carousel


def test_creation():
    """
    Проверка создания
    """
    with pytest.raises(ValueError):
        Carousel()

    c = Carousel(maxlen=2)
    assert len(c) == 0
    assert c.maxlen == 2
    assert c.get_contents() == []

    c = Carousel([1, 2, 3])
    assert len(c) == 3
    assert c.maxlen == 3
    assert c.get_contents() == [1, 2, 3]
    assert c.extract() == [1, 2, 3]

    c = Carousel([1, 2, 3], maxlen=2)
    assert len(c) == 2
    assert c.maxlen == 2
    assert c.get_contents() == [2, 3]
    assert c.extract() == [2, 3]


def test_push():
    """
    Проверка добавления элемента
    """
    maxlen = 3
    c = Carousel(maxlen=maxlen, sentinel=None)
    assert c.get_contents() == []

    x = c.push(1)
    assert c.get_contents() == [1]
    assert x is None

    x = c.push(2)
    assert c.get_contents() == [1, 2]
    assert x is None

    x = c.push(3)
    assert c.get_contents() == [1, 2, 3]
    assert x is None

    x = c.push(4)
    assert c.get_contents() == [2, 3, 4]
    assert x == 1

    x = c.push(5)
    assert c.get_contents() == [3, 4, 5]
    assert x == 2

    x = c.push(6)
    assert c.get_contents() == [4, 5, 6]
    assert x == 3


def test_len():
    """
    Проверка измерения длины
    """
    maxlen = 5
    c = Carousel(maxlen=maxlen)
    for i in range(1, 10):
        c.push(i)
        assert len(c) == i if i < maxlen else maxlen
    assert len(c) == maxlen


def test_get_contents():
    """
    Не должно влиять на внутренности
    """
    c = Carousel([1, 2, 3])
    assert c.get_contents() == [1, 2, 3]
    assert c._data == [1, 2, 3]
    assert c._data == c.get_contents()

    c = Carousel([1, 2, 3], maxlen=2)
    assert c.get_contents() == [2, 3]
    assert c._data == [3, 2]
    assert c._data != c.get_contents()


def test_str():
    """
    Проверка текстового представления
    """
    c = Carousel(maxlen=4)
    assert str(c) == 'Carousel([], maxlen=4)'

    c = Carousel([1, 2, 3])
    assert str(c) == 'Carousel([1, 2, 3], maxlen=3)'

    c = Carousel([1, 2, 3], maxlen=2)
    assert str(c) == 'Carousel([2, 3], maxlen=2)'


def test_repr():
    """
    Проверка текстового представления
    """
    c = Carousel(maxlen=4)
    assert repr(c) == 'Carousel([NULL, NULL, NULL, NULL], maxlen=4)'

    c = Carousel([1, 2, 3])
    assert repr(c) == 'Carousel([1, 2, 3], maxlen=3)'

    c = Carousel([1, 2, 3], maxlen=2)
    assert repr(c) == 'Carousel([2, 3], maxlen=2)'


def test_resize():
    """
    Проверка изменения размера
    """
    c = Carousel([1, 2, 3], maxlen=2)
    assert len(c) == 2
    assert c.maxlen == 2
    assert c.get_contents() == [2, 3]

    assert repr(c) == 'Carousel([2, 3], maxlen=2)'
    c.resize(5)
    assert repr(c) == 'Carousel([2, 3, NULL, NULL, NULL], maxlen=5)'

    c.push(4)
    c.push(5)

    assert len(c) == 4
    assert c.maxlen == 5
    assert c.get_contents() == [2, 3, 4, 5]
    assert repr(c) == 'Carousel([2, 3, 4, 5, NULL], maxlen=5)'

    c.push(6)

    assert len(c) == 5
    assert c.maxlen == 5
    assert c.get_contents() == [2, 3, 4, 5, 6]
    assert repr(c) == 'Carousel([2, 3, 4, 5, 6], maxlen=5)'

    c.resize(2)
    assert repr(c) == 'Carousel([5, 6], maxlen=2)'

    assert len(c) == 2
    assert c.maxlen == 2
    assert c.get_contents() == [5, 6]


def test_resize_empty():
    """
    Проверка изменения размера пустой карусели
    """
    c = Carousel(maxlen=2)
    assert c.maxlen == 2
    assert repr(c) == 'Carousel([NULL, NULL], maxlen=2)'

    c.resize(5)
    assert c.maxlen == 5
    assert repr(c) == 'Carousel([NULL, NULL, NULL, NULL, NULL], maxlen=5)'

    c.resize(3)
    assert c.maxlen == 3
    assert repr(c) == 'Carousel([NULL, NULL, NULL], maxlen=3)'


def test_no_resize():
    """
    Проверка изменения размера при том же значении
    """
    c = Carousel(maxlen=2)
    assert c.maxlen == 2
    c.resize(c.maxlen)
    assert c.maxlen == 2


def test_iter():
    """
    Проверка итерирования по карусели
    """
    base = [1, 2, 3]
    c = Carousel(base, maxlen=4)
    for ref, value in zip(base, c):
        assert ref == value

    # убедимся, что не сломали список
    assert base == [1, 2, 3]
