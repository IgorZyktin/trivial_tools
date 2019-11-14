# -*- coding: utf-8 -*-
"""

    Инструменты обработки JSON файлов

"""
# встроенные модули
import os
import sys
import json
from typing import Dict, Any, Optional

# сторонние модули
from loguru import logger


def json_config_load(filename: str, config_name: str,
                     default_config: Optional[str]) -> Dict[str, Any]:
    """
    Открыть указанный файл и прочитать его содержимое
    """
    path = os.path.join(os.getcwd(), filename)
    try:
        with open(path, mode='r', encoding='utf-8') as file:
            data = json.load(file)

            if config_name in data:
                config_data = data[config_name]

            elif default_config in data:
                config_data = data[default_config]

            else:
                raise KeyError

            return config_data

    except FileNotFoundError:
        logger.critical(f'Не найден файл конфигурации: "{path}"')

    except KeyError:
        logger.critical(f'Не удалось загрузить конфигурацию "{config_name}" из файла: "{path}"')

    sys.exit(1)
