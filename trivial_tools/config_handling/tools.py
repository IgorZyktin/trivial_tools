# -*- coding: utf-8 -*-
"""

    Примитивные инструменты для обработки конфигов

"""
# встроенные модули
import sys
from typing import Optional

# модули проекта
from trivial_tools.config_handling import BaseConfig
from trivial_tools.system.envs import get_env_variable


def get_config_name() -> Optional[str]:
    """
    Примитивный способ получить имя конфигурации из аргументов запуска
    """
    config_name = None
    if len(sys.argv) >= 3 and sys.argv[1] == '--config':
        config_name = sys.argv[2]
    return config_name


def get_config(config_filename: str = 'config.json',
               env_name: str = 'ENCOST_APP_CONFIG') -> BaseConfig:
    """
    Получить экземпляр конфига
    """
    config = BaseConfig.from_json(
        filename=config_filename,
        config_name=get_config_name(),
        default_config=get_env_variable(env_name)
    )
    return config
