# -*- coding: utf-8 -*-
"""

    Инструменты запросов

"""
# встроенные модули
from typing import Dict, Any, Optional

# сторонние модули
import requests
from loguru import logger


def make_post(url: str, json: dict) -> Optional[Dict[str, Any]]:
    """
    Выполнить POST запрос и получить данные
    """
    response = requests.post(url, json=json)
    result = response.json()

    if 'error' in result:
        logger.critical('Критический сбой!')
        logger.critical(result)
        result = None
    # else:
    #     result = result.get('result')

    return result
