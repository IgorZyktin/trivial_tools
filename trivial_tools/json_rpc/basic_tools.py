# -*- coding: utf-8 -*-
"""

    Простые инструменты для работы с JSON-RPC

"""
# встроенные модули
from typing import Dict, Any, Union

id_type = Union[int, str, None]


def form_request(*, method: str, id_: id_type = None, **kwargs) -> Dict[str, Any]:
    """
    Собрать запрос к API
    """
    return {"jsonrpc": "2.0", "method": method, "params": {**kwargs}, "id": id_}


def result(output: Any, request_id: id_type = None) -> Dict[str, Any]:
    """
    Успешный результат
    """
    return {"jsonrpc": "2.0", "result": output, "id": request_id}


def error(output: str, request_id: id_type = None) -> Dict[str, Any]:
    """
    Неудачный результат
    """
    return {"jsonrpc": "2.0", "error": output, "id": request_id}
