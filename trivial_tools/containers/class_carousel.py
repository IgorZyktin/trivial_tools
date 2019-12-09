# -*- coding: utf-8 -*-
"""

    Контейнер с бегущим индексом, в который постоянно можно добавлять элементы

    На базе этого контейнера предполагается собирать структуры для вычисления динамических
    характеристик непрерывного потока входных данных в реальном времени.
    Например вычисление скользящего среднего.

    Пример работы с контейнером:
    c = Carousel(maxlen=3)  # внутреннее хранилище: [NULL, NULL, NULL]
    c.push(1)               # внутреннее хранилище: [   1, NULL, NULL]
    c.push(2)               # внутреннее хранилище: [   1,    2, NULL]
    c.push(3)               # внутреннее хранилище: [   1,    2,    3]
    c.push(4)               # внутреннее хранилище: [   4,    2,    3]
    c.push(5)               # внутреннее хранилище: [   4,    5,    3]
    c.push(6)               # внутреннее хранилище: [   4,    5,    6]
    c.push(7)               # внутреннее хранилище: [   7,    5,    6]
    c.push(8)               # внутреннее хранилище: [   7,    8,    6]
    c.get_contents() --> [6, 7, 8]

    Почему не deque или другое подобие связного списка - очень медленно.
    Предполагается, что данная реализация будет работать намного быстрее
    и меньше загружать процессор при работе.

"""
# встроенные модули
from typing import Any, Optional, Sequence, List, Generator, Union

# модули проекта
from trivial_tools.special.special import fail
from trivial_tools.formatters.base import s_type


class Carousel:
    """
    Контейнер с бегущим индексом на базе списка.
    Нужен для обработки непрерывного входного потока данных
    """
    __slots__ = ('_sentinel', '_data', '_len', '_index', 'maxlen')

    def __init__(self, source: Optional[Sequence] = None,
                 maxlen: int = 0, sentinel: Any = object()):
        """
        Создание экземпляра. Можно задать базовую коллекцию, размер и объект для пустых слотов

        :param source:
        :param maxlen:
        :param sentinel:
        """
        self._sentinel = sentinel
        self._data = []
        self._len = 0
        self._index = 0

        if source:
            # есть коллекция-прототип из которой можно взять данные
            if maxlen:
                self.maxlen = maxlen
            else:
                self.maxlen = len(source)
            self.restore()
            self.populate(source)

        elif maxlen:
            # создаём пустую карусель
            self.maxlen = maxlen
            self.restore()

        else:
            fail(
                f'Для создания экземпляра {s_type(self)} необходимо либо '
                '\nуказать длину и/или дать коллекцию из которой будет собран экземпляр.',
                reason=ValueError
            )

    def __str__(self) -> str:
        """
        Текстовый вид
        """
        contents = [str(x) for x in self._internals() if x is not self._sentinel]
        string = ', '.join(contents)
        result = f'{s_type(self)}([{string}], maxlen={self.maxlen})'
        return result

    def __repr__(self) -> str:
        """
        Текстовый вид
        """
        contents = [str(x) if x is not self._sentinel else 'NULL' for x in self._internals()]
        string = ', '.join(contents)
        result = f'{s_type(self)}([{string}], maxlen={self.maxlen})'
        return result

    def populate(self, source: Sequence[Any]) -> None:
        """
        Наполнить хранилище предоставленными данными

        :param source: некоторая коллекция, элементы которой надо последовательно переложить
        """
        self._index = 0
        for value in source:
            self.push(value)

    def __len__(self) -> int:
        """
        Длина показывает сколько ячеек у нас заполнено
        """
        return self._len

    def increment(self) -> int:
        """
        Увеличить индекс на единицу и вернуть его значение
        """
        if self._index < self.maxlen - 1:
            self._index += 1
        else:
            self._index = 0
        return self._index

    def push(self, element: Any) -> Any:
        """
        Добавить элемент в карусель

        Мы замещаем элемент, выталкивая его из списка и возвращаем его. Его значение потом может
        быть использовано на вызывающей стороне

        :param element: Новый элемент любого типа
        :return: Старый элемент, который был вытолкнут при добавлении (может оказаться sentinel!)
        """
        old_value = self._data[self._index]
        self._data[self._index] = element
        self.increment()

        self._len += 1
        if self._len > self.maxlen:
            self._len = self.maxlen

        return old_value

    def resize(self, new_maxlen: int) -> None:
        """
        Изменить размер карусели

        :param new_maxlen: новая предельная длина для внутреннего хранилища
        """
        if new_maxlen == self.maxlen:
            return

        old_data = self.get_contents()
        self.maxlen = new_maxlen
        self.restore()
        self.populate(old_data)

    def get_contents(self) -> List[Any]:
        """
        Получить копию внутреннего хранилища
        """
        result = [x for x in self._internals() if x is not self._sentinel]
        return result

    def extract(self) -> List[Any]:
        """
        Получить копию внутреннего хранилища и очистить его
        """
        result = self.get_contents()
        self.restore()
        return result

    def restore(self) -> None:
        """
        Сбросить индекс и длину, заполнить
        внутреннее хранилище пустыми объектами
        """
        self._len = 0
        self._index = 0
        self._data = [self._sentinel for _ in range(self.maxlen)]

    def _internals(self) -> Generator[Any, None, None]:
        """
        Проитерироваться по элементам внутреннего хранилища (включая пустые элементы!)
        """
        if len(self) == self.maxlen:
            yield from self._data[self._index:]
            yield from self._data[:self._index]
        else:
            yield from self._data

    def __iter__(self) -> Any:
        """
        Проитерироваться по элементам внутреннего хранилища (без пустых элементов)
        Сохраняет порядок вставки элементов
        """
        for element in self._internals():
            if element is not self._sentinel:
                yield element

    def __getitem__(self, item: Union[int, slice]) -> Any:
        """
        Обратиться к элементу по индексу.
        Обеспечивается обычный доступ к внутреннему хранилищу, просто со смещением индекса

        :param item: ключ индексации
        :return: содержимое внутреннего хранилища
        """
        if isinstance(item, int):
            result = self._data[self._index + item]

            if result is self._sentinel:
                fail(f'В экземпляре {s_type(self)} нет элемента с индексом {item!r}',
                     reason=IndexError)

            return result

        if isinstance(item, slice):
            start = item.start + self._index if item.start else None
            stop = item.stop + self._index if item.stop else None
            step = item.step + self._index if item.step else None
            result = self._data[slice(start, stop, step)]

            if any(x is self._sentinel for x in result):
                fail(f'Часть среза {item!r} экземпляра {s_type(self)} содержит '
                     'непроинициализированные значения ', reason=IndexError)

            return result

        fail(
            f"Тип {s_type(self)} поддерживает работу только с индексами int и slice!",
            reason=IndexError
        )

    def __setitem__(self, key: Union[int, slice], value: Any) -> None:
        """
        Записать элемент по индексу.
        Обеспечивается обычный доступ к внутреннему хранилищу, просто со смещением индекса

        :param key: ключ индексации
        :param value: данные для записи (любой тип)
        """
        if isinstance(key, int):
            self._data[self._index + key] = value
            return

        if isinstance(key, slice):
            start = key.start + self._index if key.start else None
            stop = key.stop + self._index if key.stop else None
            step = key.step + self._index if key.step else None
            self._data[slice(start, stop, step)] = value
            return

        fail(
            f"Тип {s_type(self)} поддерживает работу только с индексами int и slice!",
            reason=IndexError
        )
