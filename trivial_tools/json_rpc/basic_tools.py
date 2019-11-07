# -*- coding: utf-8 -*-
"""

    Простые инструменты для работы с JSON-RPC

"""
# встроенные модули
from typing import Dict, Callable, Optional, Any


def method(container: Dict[str, Callable]) -> Callable:
    """
    Декоратор регистрации методов в JSON-RPC API
    """
    def wrapper(func: Callable) -> Callable:
        """
        Объёртка для создания замыкания для передачи container
        """
        container[func.__name__] = func
        return func
    return wrapper


def form_request(method_name: str, request_id: Optional[int] = None, **kwargs) -> Dict[str, Any]:
    """
    Собрать запрос к API
    """
    request = {
        "jsonrpc": "2.0",
        "method": method_name,
        "params": {**kwargs},
        "id": request_id
    }
    return request


def form_valid_response(result: Any, request_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Собрать ответ из API
    """
    response = {"jsonrpc": "2.0", "result": result, "id": request_id}
    return response
