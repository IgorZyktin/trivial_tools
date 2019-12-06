# -*- coding: utf-8 -*-
"""

    Тесты кеширующей машины

"""
# встроенные модули
from datetime import datetime
from unittest.mock import patch

# сторонние модули
import pytest

# модули проекта
from trivial_tools.storage.caching_machine import CachingMachine


@pytest.fixture()
def machine_persistent():
    """
    Машина без срока хранения
    """
    return CachingMachine()


@pytest.fixture()
def machine_persistent():
    """
    Машина со сроком хранения 5 секунд
    """
    return CachingMachine(expiration=5)


@pytest.fixture()
def machine_tiny():
    """
    Машина со сроком хранения 5 секунд и всего на 4 элемента
    """
    return CachingMachine(expiration=5, max_items=4)


def test_fill(machine_tiny):
    """
    Проверка заполнения машины
    """
    with patch('storage.caching_instance.datetime') as fake:
        fake.now.return_value = datetime(2019, 10, 31, 18, 6, 0)
        assert machine_tiny.total() == 0

        machine_tiny.set('key_1', 'value')
        assert machine_tiny.total() == 1

        machine_tiny.set('key_1', 'value')
        assert machine_tiny.total() == 1

        machine_tiny.set('key_2', 'value')
        assert machine_tiny.total() == 2

        machine_tiny.set('key_3', 'value')
        assert machine_tiny.total() == 3

        machine_tiny.set('key_4', 'value')
        assert machine_tiny.total() == 4

        machine_tiny.set('key_5', 'value')
        assert machine_tiny.total() == 4

        machine_tiny.restore()
        assert machine_tiny.total() == 0
