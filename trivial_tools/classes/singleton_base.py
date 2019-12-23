# -*- coding: utf-8 -*-
"""

    Метакласс для реализации паттерна одиночка

"""
# модули проекта
from trivial_tools.special.special import fail
from trivial_tools.formatters.base import s_type


class Singleton(type):
    """
    Метакласс для реализации паттерна одиночка
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Вызов может быть от различных классов!
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def get_instance(mcs, required_cls):
        """
        Обращение от потомка за экземпляром себя
        """
        if isinstance(required_cls, type):
            if required_cls in mcs._instances:
                return mcs._instances[required_cls]
        else:
            if type(required_cls) in mcs._instances:
                return mcs._instances[type(required_cls)]

        fail(f'Метакласс {mcs} не содержит экземпляров {s_type(required_cls)}!', reason=KeyError)