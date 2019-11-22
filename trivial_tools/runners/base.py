# -*- coding: utf-8 -*-
"""

    Инструменты запуска

"""
# встроенные модули
import os
import time
from functools import wraps
from typing import Callable, Union, Tuple, Any, Type, Optional

# сторонние модули
from loguru import logger

# модули проекта
from trivial_tools.special.special import fail
from trivial_tools.config_handling import BaseConfig
from trivial_tools.system.envs import get_full_path_from_env, get_env_variable


def repeat_on_exceptions(repeats: int, case: Union[Exception, Tuple[Exception]],
                         delay: float = 1.0, verbose: bool = True) -> Callable:
    """Декоратор, заставляющий функцию повторить операцию при выбросе исключения.

    Инструмент добавлен для возможности повторной отправки HTTP запросов на серверах

    :param verbose: логгировать произошедшие исключения и выводить их на экран
    :param delay: время ожидания между попытками
    :param repeats: сколько раз повторить (0 - повторять бесконечно)
    :param case: при каком исключении вызывать повтор
    :return: возвращает фабрику декораторов
    """

    def decorator(func: Callable) -> Callable:
        """
        Декоратор
        """

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """
            Враппер
            """
            iteration = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                    break
                except case as exc:
                    iteration += 1

                    if verbose:
                        logger.warning(f'Исключение {type(exc)} в функции {func.__name__}'
                                       f' (итерация {iteration})')

                    if repeats and iteration > repeats:
                        fail(exc)

                    time.sleep(delay)

            return result

        return wrapper

    return decorator


def start_working(folder_name: str, config_name: Optional[str], func: Callable,
                  config_type: Type[BaseConfig], env_name: str,
                  config_filename: str = 'config.json', infinite: bool = True) -> None:
    """Стартовать скрипт с выбранными настройками.

    :param folder_name: имя суб-каталога со скриптом. Запуск предполагается из коневого каталога
    :param config_name: принудительный выбор конфигурации для скрипта при запуске из консоли
    :param func: рабочая функция скрпта, которая будет выполнять всю полезную работу
    :param config_type: класс конфигурации для выбранного скрипта
    :param env_name: имя переменной окружения, в которой хранится имя конфигурации по умолчанию
    :param config_filename: имя json файла в котором следует искать кофигурацию
    :param infinite: флаг бесконечного перезапуска скрипта при выбросе исключения
    """
    config = config_type.from_json(
        filename=os.path.join(folder_name, config_filename),
        config_name=config_name,
        default_config=get_env_variable(env_name)
    )

    logger.add(
        sink=get_full_path_from_env(config.db_path, config.logger_filename),
        level=config.logger_level,
        rotation=config.logger_rotation
    )

    separator = '#' * 79

    logger.warning(separator)
    logger.warning(config.start_message)
    logger.info(f'Параметры скрипта:\n{config}')

    while True:
        # noinspection PyBroadException
        try:
            message = func(config)
            logger.warning(message)
        except Exception:
            logger.exception('\nКритический сбой!')

        if not infinite:
            break

    logger.warning(separator)
