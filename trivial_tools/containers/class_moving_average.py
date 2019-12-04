# -*- coding: utf-8 -*-
"""

    Контейнер для вычисления скользящего среднего.
    В него можно постоянно можно добавлять элементы и быстро получать среднее

    Пример работы с контейнером:
    m = MovingAverage(maxlen=4)  # среднее равно 0
    m.push(1)   # среднее равно 1
    m.push(3)   # среднее равно 2
    m.push(5)   # среднее равно 3
    m.push(6)   # среднее равно 3,75
    m.push(8)   # среднее равно 5,5
    m.push(41)  # среднее равно 15
    m.push(9)   # среднее равно 16

"""
# встроенные модули
from typing import Union

# модули проекта
from containers.class_carousel import Carousel


class MovingAverage(Carousel):
    """
    Контейнер для вычисления скользящего среднего.
    В него можно постоянно можно добавлять элементы и быстро получать среднее
    """
    __slots__ = ('_sum', '_avg')

    def __init__(self, *args, **kwargs):
        """
        Создание экземпляра
        """
        self._sum = 0.0
        self._avg = 0.0
        super().__init__(*args, **kwargs)

    def push(self, value: Union[int, float]) -> None:
        """
        Добавить элемент в контейнер

        Мы выталкиваем предыдущий элемент и меняем сумму соответствующим образом. Причина
        для такого выполнения - избежать необходимости итерироваться по коллекции при
        попытке вычислить среднее значение

        :param value: новое число, которое соответствует сдвигу окна среднего на один элемент
        """
        old_value = super().push(float(value))

        if old_value is not self._sentinel:
            self._sum -= old_value

        self._sum += value
        self._avg = self._sum / len(self)

    def restore(self) -> None:
        """
        Сбросить параметры
        """
        self._sum = 0.0
        self._avg = 0.0
        super().restore()

    @property
    def sum(self) -> float:
        """
        Сумма всех элементов
        """
        return self._sum

    @property
    def avg(self) -> float:
        """
        Среднее всех элементов
        """
        return self._avg
