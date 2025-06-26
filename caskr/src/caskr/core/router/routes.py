from typing import Callable, Dict, Optional, Tuple, Union, Literal, List

from caskr.core.utils.logger import logger

_RouteHandler = Union[Callable, Tuple[Callable, Optional[Dict]]]


def parse_route_params(path: str, pattern: str) -> Optional[dict]:
    path_parts = path.strip("/").split("/")
    pattern_parts = pattern.strip("/").split("/")

    if len(path_parts) != len(pattern_parts):
        return None

    params = {}
    for p_part, pat_part in zip(path_parts, pattern_parts):
        if pat_part.startswith(":"):
            param_name = pat_part[1:]
            params[param_name] = p_part
        elif p_part != pat_part:
            return None  # Static part mismatch

    return params


class _RouteDirectory:
    def __init__(self):
        self._routes: Dict[str, Callable] = {}
        self._cookies: Dict[str, List[str]] = {}
        self._methods: Dict[str, List[str]] = {}

    @property
    def routes(self) -> Dict[str, Callable]:
        return self._routes
        
    def get_handler(self, path: str) -> Optional[Tuple[Callable, Optional[Dict], List[str]]]:
        # Direct match
        if path in self._routes:
            handler = self._routes[path]
            return (handler, None, self._methods.get(path, []), self._cookies.get(path, []))

        # Pattern match with params
        for pattern, handler in self._routes.items():
            params = parse_route_params(path, pattern)
            if params is not None:
                return (handler, params, self._methods.get(pattern, []), self._cookies.get(pattern, []))

        return None

    def set_handler(self, path: str, handler: _RouteHandler, method, cookies) -> None:
        self._routes[path] = handler
        self._methods[path] = method
        self._cookies[path] = cookies or []

    def _normalize_handler(self, handler: _RouteHandler) -> Tuple[Callable, Optional[Dict]]:
        if isinstance(handler, tuple):
            return handler
        return handler, None

    def __str__(self):
        return str(self._routes)
