# -*- coding: utf-8 -*-
"""

    Контейнер для хранения среза данных на определённую глубину в прошлое.
    Можно добавлять данные с нерегулярными временными метками и он будет держать
    в себе показатели за необходимое число секунд.

    Предполагается, что данные округляются до целых секунд. Поскольку данные ненормированы,
    минимальное количество элементов должно быть равно числу секунд за которых происходит анализ.
    Технически очень вероятно, что содержимое контейнера постоянно будет включать пустые
    элементы т.к. шаг в секундах между двумя соседними записями может быть больше 1.

    Пример работы с контейнером:
    t = TimeSlice(datetime_index=0, maxlen=14)
    t.push((datetime(2019, 12, 1, 12, 0, 10), 'U'))  # внутри лежит U
    t.push((datetime(2019, 12, 1, 12, 0, 15), 'V'))  # внутри лежит U, V
    t.push((datetime(2019, 12, 1, 12, 0, 20), 'W'))  # внутри лежит U, V, W
    t.push((datetime(2019, 12, 1, 12, 0, 25), 'X'))  # внутри лежит U, V, W, X
    t.push((datetime(2019, 12, 1, 12, 0, 30), 'Y'))  # внутри лежит V, W, X, Y
    t.push((datetime(2019, 12, 1, 12, 0, 35), 'Z'))  # внутри лежит W, X, Y, Z

    Для этого объекта запрещён доступ к элементам т.к. мы никогда не знаем, где находятся
    пустые значения в блоке данных.

"""
# встроенные модули
from typing import Any, Optional

# модули проекта
from trivial_tools.special.special import fail
from trivial_tools.formatters.base import s_type
from trivial_tools.containers.class_carousel import Carousel


class TimeSlice(Carousel):
    """
    Контейнер для хранения среза данных на определённую глубину в прошлое
    """
    __slots__ = ('datetime_index', 'newest', 'minimum_allowed_timestamp')

    def __init__(self, datetime_index: int = 0, maxlen: int = 1, sentinel: Any = object()):
        """
        Создание экземпляра

        :param datetime_index: индекс, по которому находится метка времени в блоке данных
        :param maxlen: ширина среза в секундах, фактически размер окна для анализа
        :param sentinel: элемент для заполнения пустых ячеек (можно добавить свой)
        """
        self.datetime_index = datetime_index
        self.newest: int = 0
        self.minimum_allowed_timestamp: Optional[int] = None
        super().__init__(None, maxlen, sentinel)

    @property
    def delta(self) -> int:
        """
        Разница в секундах между самым новым и самым старым элементом
        При итерировании нас не интересует порядок элементов
        """
        oldest = self.newest

        for element in self:
            element_time = self.get_seconds(element)

            if element_time < oldest:
                oldest = element_time

        difference = self.newest - oldest

        return difference

    def push(self, item: tuple) -> None:
        """
        Добавить элемент в контейнер
        """
        item_timestamp = self.get_seconds(item)

        if item_timestamp <= self.newest:
            return

        super().push(item)

        self.newest = item_timestamp
        self.clear_outdated()

    def update_minimum_allowed_timestamp(self):
        """
        Обновить предельно допустимую границу времени
        """
        index = self._index
        steps_left = len(self._data)

        while True:
            element = self._data[index]

            if element is not self._sentinel:
                element_time = self.get_seconds(element)
                if self.newest - element_time > self.maxlen:
                    self.minimum_allowed_timestamp = element_time

            index += 1
            steps_left -= 1

            if steps_left <= 0:
                break

            if index > len(self._data) - 1:
                index -= len(self._data) - 1

    def clear_outdated(self):
        """
        Стереть устаревшие элементы. Это нетривиальная операция т.к. нам требуется оставить один
        элемент, временная разница с которым будет ПРЕВЫШАТЬ требуемый нам размер. Мы анализируем
        данные в окне шириной не менее чем self.maxlen. Поэтому приходится сначала искать
        допустимую временную метку, а уже потом стирать всё, что дальше этой метки
        """
        self.update_minimum_allowed_timestamp()

        if self.minimum_allowed_timestamp is None:
            # контейнер ещё не до конца заполнен
            return

        for i, element in enumerate(self._data):

            if element is self._sentinel:
                continue

            element_time = self.get_seconds(element)
            if element_time < self.minimum_allowed_timestamp:
                self._data[i] = self._sentinel

    def get_seconds(self, payload: tuple) -> int:
        """
        Выделить число секунд для datetime
        """
        return int(payload[self.datetime_index].replace(microsecond=0).timestamp())

    def __getitem__(self, item):
        """
        Обратиться к элементу по индексу

        Поскольку содержимое внутреннего хранилища представляет собой неоднородный массив,
        не существует простого способа определить какой индекс нам надо использовать
        """
        fail(f"Для типа {s_type(self)} доступ к внутренним элементам не разрешается!",
             reason=NotImplementedError)

    def __setitem__(self, key, value):
        """
        Записать элемент по индексу

        Поскольку содержимое внутреннего хранилища представляет собой неоднородный массив,
        не существует простого способа определить какой индекс нам надо использовать
        """
        fail(f"Для типа {s_type(self)} доступ к внутренним элементам не разрешается!",
             reason=NotImplementedError)

    @property
    def not_filled(self) -> bool:
        """
        Проверка на то, что мы ещё не собрали достаточно данных для анализа
        """
        return self.minimum_allowed_timestamp is None
