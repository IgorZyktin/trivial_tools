# -*- coding: utf-8 -*-
"""

    Двусторонная карусель.
    В работе подобна deque, но не меняет размера при добавлении и извлечении элементов.

"""
# встроенные модули
from typing import Any, Optional, Collection, Generator, List

# модули проекта
from trivial_tools.special.special import fail
from trivial_tools.formatters.base import s_type
from trivial_tools.containers.class_carousel import Carousel


class DeCarousel(Carousel):
    """
    Двусторонная карусель.
    В работе подобна deque, но не меняет размера при добавлении и извлечении элементов.
    """
    __slots__ = ('_head', '_tail')

    def __init__(self, source: Optional[Collection] = None,
                 window: int = 0, sentinel: Any = object()):
        """
        Создание экземпляра. Можно задать базовую коллекцию, размер и объект для пустых слотов

        :param source: исходная коллекция элементов, на базе которой надо собрать экземпляр
        :param window: максимальное количество элементов (ширина окна вычисления)
        :param sentinel: элемент для заполнения пустых ячеек (можно добавить свой)
        """
        self._head = -1
        self._tail = -1
        super().__init__(source, window, sentinel)

    def __contains__(self, item: Any) -> bool:
        """
        Проверка наличия элемента
        """
        return item in self._data

    def push(self, element: Any) -> Any:
        """
        Добавить элемент в карусель

        Мы замещаем элемент, выталкивая его из списка и возвращаем его. Его значение потом может
        быть использовано на вызывающей стороне

        :param element: Новый элемент любого типа
        :return: Старый элемент, который был вытолкнут при добавлении (может оказаться sentinel!)
        """
        if self._head == self._tail == -1:
            # первая вставка элемента
            old_value = self._data[self._index]
            self._data[self._index] = element

            self._index = self._step_right(self._index)
            self._head = self._step_right(self._head)
            self._tail = self._step_right(self._tail)

        else:
            # обычная конфигурация
            old_value = self._data[self._index]
            self._data[self._index] = element

            if self._index == self._head:
                # затираем голову
                self._head = self._step_right(self._head)

            self._index = self._step_right(self._index)
            self._tail = self._step_right(self._tail)

        if self._head < self._tail:
            self._len = self._tail - self._head + 1

        elif self._head > self._tail:
            self._len = self._tail - self._head + 1 + self.window

        elif self._head == -1 and self._tail == -1:
            self._len = 0

        elif self._head == self._tail:
            self._len = 1

        return old_value

    def _step_right(self, index: int) -> int:
        """
        Шагнуть вправо
        """
        if index < self.window - 1:
            index += 1
        else:
            index = 0
        return index

    def _step_left(self, index: int) -> int:
        """
        Шагнуть влево
        """
        if index > 0:
            index -= 1
        else:
            index = self.window - 1
        return index

    @property
    def left(self) -> Optional[Any]:
        """
        Крайний элемент слева
        """
        if len(self):
            return self._data[self._head]
        return None

    @property
    def right(self) -> Optional[Any]:
        """
        Крайний элемент справа
        """
        if len(self):
            return self._data[self._tail]
        return None

    # def resize(self, new_window: int) -> None:
    #     """
    #     Изменить размер карусели
    #
    #     :param new_window: новая предельная длина для внутреннего хранилища
    #     """
    #     if new_window == self.window:
    #         return
    #
    #     old_data = self.get_contents()
    #     self.window = new_window
    #     self.restore()
    #     self.populate(old_data)

    def restore(self) -> None:
        """
        Сбросить индекс и длину, заполнить
        внутреннее хранилище пустыми объектами
        """
        self._len = 0
        self._index = 0
        self._head = -1
        self._tail = -1
        self._data = [self._sentinel for _ in range(self.window)]

    def _internals(self) -> Generator[Any, None, None]:
        """
        Проитерироваться по элементам внутреннего хранилища (включая пустые элементы!)
        """
        i = self._head
        while True:
            if i == self._tail:
                break
            yield self._data[i]
            i = self._step_right(i)
        yield self._data[self._tail]

    def append(self, item: Any) -> None:
        """
        Добавить элемент справа
        """
        self.push(item)
        return None

    def pop(self) -> Any:
        """
        Извлечь элемент справа
        """
        if len(self) == 0:
            fail(f'Попытка извлечь элемент из пустой коллекции: {self}', reason=IndexError)

        value = self._data[self._tail]
        self._data[self._tail] = self._sentinel
        self._tail = self._step_left(self._tail)
        self._index = self._step_left(self._index)
        self._len -= 1
        return value

    def appendleft(self, item: Any) -> None:
        """
        Добавить элемент слева
        """
        raise NotImplementedError

    def popleft(self) -> Any:
        """
        Извлечь элемент слева
        """
        if len(self) == 0:
            fail(f'Попытка извлечь элемент из пустой коллекции: {self}', reason=IndexError)

        value = self._data[self._head]
        self._data[self._head] = self._sentinel
        self._head = self._step_right(self._head)
        self._len -= 1
        return value


    # def __getitem__(self, item: Union[int, slice]) -> Any:
    #     """
    #     Обратиться к элементу по индексу.
    #     Обеспечивается обычный доступ к внутреннему хранилищу, просто со смещением индекса
    #
    #     :param item: ключ индексации
    #     :return: содержимое внутреннего хранилища
    #     """
    #     if isinstance(item, int):
    #         if not self._len:
    #             fail(f'Попытка получить элемент из пустого объекта {s_type(self)}',
    #                  reason=IndexError)
    #
    #         result = self._data[self.get_real_index(item)]
    #
    #         if result is self._sentinel:
    #             fail(f'В экземпляре {s_type(self)} нет элемента с индексом {item!r}',
    #                  reason=IndexError)
    #
    #         return result
    #
    #     if isinstance(item, slice):
    #         return self.get_contents()[item]
    #
    #     fail(f"Тип {s_type(self)} поддерживает работу только с индексами int и slice!",
    #          reason=IndexError)
    #
    # def __setitem__(self, key: Union[int, slice], value: Any) -> None:
    #     """
    #     Записать элемент по индексу.
    #     Обеспечивается обычный доступ к внутреннему хранилищу, просто со смещением индекса
    #
    #     :param key: ключ индексации, только int
    #     :param value: данные для записи (любой тип)
    #     """
    #     if not isinstance(key, int):
    #         fail(f"Тип {s_type(self)} поддерживает работу только с индексами типа int!",
    #              reason=IndexError)
    #
    #     if not self._len:
    #         fail(f'Попытка присвоить элемент по индексу {key} в пустой объект {s_type(self)}',
    #              reason=IndexError)
    #
    #     self._data[self.get_real_index(key)] = value
    #     return
    #
    # def get_real_index(self, key: int) -> int:
    #     """
    #     Настояшее положение ячеек, с учётом их сдвига
    #     """
    #     index = self._index + key
    #     if index > self._len - 1:
    #         index -= self._len
    #     return index
