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

            add_config = {}
            base_config = data['base']

            if config_name in data:
                add_config = data[config_name]

            elif default_config in data:
                add_config = data[default_config]

            if add_config:
                resulting_config = {**base_config, **add_config}
            else:
                resulting_config = base_config

            return resulting_config

    except FileNotFoundError:
        logger.critical(f'Не найден файл конфигурации: "{path}"')

    except KeyError:
        logger.critical(f'Не удалось загрузить конфигурацию "{config_name}" из файла: "{path}"')

    sys.exit(1)
