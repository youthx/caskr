import inspect
from typing import Callable, List, Literal, Union

from caskr.core.config import CaskrGlobalConf
from caskr.core.router.routes import _RouteHandler, parse_route_params
from caskr.core.utils.logger import logger

_MethodLiteral = Literal["GET", "POST"]
_Method = Union[_MethodLiteral, List[_MethodLiteral]]


def route_get_handler(path: str) -> _RouteHandler | None:
    return CaskrGlobalConf.route_dir.get_handler(path)


def route_set_handler(
    path: str,
    handler: _RouteHandler,
    method: _Method,
    required_cookies: List[str],
) -> None:
    if isinstance(method, str):
        method = [method]
    method = [m.upper() for m in method]
    CaskrGlobalConf.route_dir.set_handler(path, handler, method, required_cookies)


def route(
    path: str,
    method: _Method = "GET",
    cookies: List[str] = [],
) -> Callable:
    def wrapper(func: Callable) -> Callable:
        sig = inspect.signature(func)

        def wrapped_handler(*args, **kwargs):
            # TODO: Check cookies against cookies in future implementation
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
            if typed_params:
                return func(args[0], **typed_params)
            return func()

        route_set_handler(path, wrapped_handler, method, cookies)
        return func

    return wrapper
