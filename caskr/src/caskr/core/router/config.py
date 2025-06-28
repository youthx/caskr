import inspect
from typing import Callable, List, Literal, Optional, TypedDict, Union

from caskr.core.config import CaskrGlobalConf
from caskr.core.router.routes import _RouteHandler
from caskr.core.utils.logger import logger

_MethodLiteral = Literal["GET", "POST"]
_Method = Union[_MethodLiteral, List[_MethodLiteral]]


class Cookie(TypedDict, total=False):
    """Represents an HTTP cookie with optional attributes."""

    name: str
    value: str
    domain: Optional[str]
    path: Optional[str]
    expires: Optional[str]
    max_age: Optional[int]
    secure: Optional[bool]
    http_only: Optional[bool]
    same_site: Optional[str]


def route_get_handler(path: str) -> Optional[_RouteHandler]:
    """
    Retrieve the route handler for a given path.

    Args:
        path (str): The URL path to look up.

    Returns:
        Optional[_RouteHandler]: The handler if found, else None.
    """
    return CaskrGlobalConf.route_dir.get_handler(path)


def route_set_handler(path: str, handler: _RouteHandler, method: _Method) -> None:
    """
    Register a handler for a specific path and HTTP method(s).

    Args:
        path (str): The URL path to associate with the handler.
        handler (_RouteHandler): The handler function.
        method (_Method): HTTP method(s) (e.g., "GET", "POST").
    """
    if isinstance(method, str):
        method = [method]
    method = [m.upper() for m in method]
    CaskrGlobalConf.route_dir.set_handler(path, handler, method)


def route(
    path: str,
    method: _Method = "GET",
    required_cookies: Optional[List[Cookie]] = None,
) -> Callable:
    """
    Decorator to register a function as a route handler for a specific HTTP path and method(s).

    Args:
        path (str): The URL path to associate with the route handler.
        method (_Method, optional): HTTP method(s) (e.g., "GET", "POST"). Defaults to "GET".
        required_cookies (Optional[List[Cookie]], optional): List of required cookies. Defaults to None.

    Returns:
        Callable: A decorator that registers the target function as a route handler.
    """
    if required_cookies is None:
        required_cookies = []

    def wrapper(func: Callable) -> Callable:
        sig = inspect.signature(func)

        def wrapped_handler(*args, **kwargs):
            # Validate and convert parameters according to function signature
            typed_params = {}
            for name, param in sig.parameters.items():
                if name in kwargs:
                    raw_value = kwargs[name]
                    if param.annotation is not inspect.Parameter.empty:
                        try:
                            typed_params[name] = param.annotation(raw_value)
                        except Exception as e:
                            logger.error(
                                "Failed to convert param '%s' to %s. Error: %s",
                                name,
                                param.annotation,
                                e,
                            )
                            return f"400 Invalid parameter: {name}"
                    else:
                        typed_params[name] = raw_value
            try:
                if typed_params:
                    result = func(args[0], **typed_params)
                else:
                    result = func(args[0])
            except Exception as e:
                logger.error("Handler execution failed: %s", e)
                return "500 Internal Server Error"
            return result

        route_set_handler(path, wrapped_handler, method)
        return func

    return wrapper
