# The `Router` class in the provided Python code handles routing requests, setting and getting
# cookies, and dispatching requests to appropriate handlers.
import traceback
import uuid
from http import cookies
from typing import Optional, TypeVar

from caskr.core.config import CaskrGlobalConf
from caskr.core.server.request import BaseHTTPRequestHandler
from caskr.core.utils.logger import logger


class Router(BaseHTTPRequestHandler):
    """
    Router class for handling HTTP requests, session management, and cookie operations.
    This class extends BaseHTTPRequestHandler to provide routing, session, and cookie management
    for a web application. It supports both authenticated and unauthenticated cookies, manages
    client sessions, and dispatches requests to appropriate route handlers.
    Attributes:
        _cookies (SimpleCookie): Stores cookies to be sent in the response.
        cookie_jar: Global cookie/session storage.
        client_id (Optional[str]): The current client's session ID.
        stored_cookies (dict): Cookies stored for the current client.
    Methods:
        __init__(*args, **kwargs):
            Initializes the Router, setting up cookies and session storage.
        set_cookie(key, value, path='/', max_age=None, httponly=True, secure=False, samesite='Lax', requires_auth=False):
            Sets a cookie for the response. Supports both authenticated (session-based) and unauthenticated cookies.
        set_priority_client(client_id):
            Marks a client as a priority in the cookie jar.
        get_cookie(key, requires_auth=False):
            Retrieves a cookie value, optionally from the authenticated session store.
        get_client_id(init_max_age=3600*24*30):
            Retrieves the current client's session ID from cookies and updates internal state.
        make_client_id(init_max_age=3600*24*30):
            Generates a new session ID for the client, stores it, and sets the session cookie.
        end_headers():
            Sends all cookies in the response headers before ending the HTTP headers.
        do_GET():
            Handles HTTP GET requests by dispatching to the appropriate route handler.
        do_POST():
            Handles HTTP POST requests by dispatching to the appropriate route handler.
        _dispatch(requesting_method):
            Dispatches the request to the correct handler based on the route and method.
            Checks for required cookies and handles errors.
        _send_error(code, message, content_type='text/plain; charset=utf-8'):
            Sends an HTTP error response with the specified code and message.
    """
    def __init__(self, *args, **kwargs):
        self._cookies = cookies.SimpleCookie()
        self.cookie_jar = CaskrGlobalConf.cookie_jar
        self.client_id: Optional[str] = None
        self.stored_cookies: dict = {}
        super().__init__(*args, **kwargs)

    def set_cookie(
        self,
        key: str,
        value: str,
        path: str = "/",
        max_age: Optional[int] = None,
        httponly: bool = True,
        secure: bool = False,
        samesite: str = "Lax",
        requires_auth: bool = False,
    ) -> None:
        try:
            if requires_auth:
                client_id = self.client_id or self.get_client_id()
                if not client_id:
                    client_id = self.make_client_id()
                sessions = self.cookie_jar._store.setdefault("sessions", {})
                sessions.setdefault(client_id, {})[key] = value
            else:
                self._cookies[key] = value
                self._cookies[key]["path"] = path
                if max_age is not None:
                    self._cookies[key]["max-age"] = str(max_age)
                if httponly:
                    self._cookies[key]["httponly"] = ""
                if secure:
                    self._cookies[key]["secure"] = ""
                if samesite:
                    self._cookies[key]["samesite"] = samesite
        except Exception as e:
            logger.error(f"Error setting cookie '{key}': {e}")
            logger.debug(traceback.format_exc())

    def set_priority_client(self, client_id: str) -> None:
        try:
            self.cookie_jar.set_priority_client(client_id)
        except Exception as e:
            logger.error(f"Error setting priority client: {e}")
            logger.debug(traceback.format_exc())

    def get_cookie(self, key: str, requires_auth: bool = False) -> Optional[str]:
        try:
            if requires_auth:
                client_id = self.client_id or self.get_client_id()
                if not client_id:
                    return None
                return (
                    self.cookie_jar._store.get("sessions", {})
                    .get(client_id, {})
                    .get(key)
                )
            cookie_header = self.headers.get("Cookie")
            if not cookie_header:
                return None
            cookie = cookies.SimpleCookie()
            try:
                cookie.load(cookie_header)
            except Exception as e:
                logger.error(f"Failed to parse cookies: {e}")
                logger.debug(traceback.format_exc())
                return None
            morsel = cookie.get(key)
            return morsel.value if morsel else None
        except Exception as e:
            logger.error(f"Error getting cookie '{key}': {e}")
            logger.debug(traceback.format_exc())
            return None

    def get_client_id(self, init_max_age: int = 3600 * 24 * 30) -> Optional[str]:
        try:
            client_id = self.get_cookie("sessionId")
            sessions = self.cookie_jar._store.setdefault("sessions", {})
            if not client_id or client_id not in sessions:
                return None
            self.stored_cookies = sessions.get(client_id, {})
            self.client_id = client_id
            return client_id
        except Exception as e:
            logger.error(f"Error getting client_id: {e}")
            logger.debug(traceback.format_exc())
            return None

    def make_client_id(self, init_max_age: int = 3600 * 24 * 30) -> str:
        try:
            client_id = str(uuid.uuid4())
            sessions = self.cookie_jar._store.setdefault("sessions", {})
            sessions[client_id] = {}
            self.set_cookie("sessionId", client_id, max_age=init_max_age)
            self.client_id = client_id
            return client_id
        except Exception as e:
            logger.error(f"Error making client_id: {e}")
            logger.debug(traceback.format_exc())
            return ""

    def end_headers(self) -> None:
        try:
            for morsel in self._cookies.values():
                logger.info(f"Set-Cookie: {morsel.OutputString()}")
                self.send_header("Set-Cookie", morsel.OutputString())
            super().end_headers()
        except Exception as e:
            logger.error(f"Error ending headers: {e}")
            logger.debug(traceback.format_exc())

    def do_GET(self) -> None:
        try:
            self._dispatch("GET")
        except Exception as e:
            logger.error(f"Error in do_GET: {e}")
            logger.debug(traceback.format_exc())
            self._send_error(500, "Internal Server Error")

    def do_POST(self) -> None:
        try:
            self._dispatch("POST")
        except Exception as e:
            logger.error(f"Error in do_POST: {e}")
            logger.debug(traceback.format_exc())
            self._send_error(500, "Internal Server Error")

    def _dispatch(self, requesting_method: str) -> None:
        self._cookies.clear()
        self.get_client_id()
        try:
            route_result = CaskrGlobalConf.route_dir.get_handler(self.path)
            if route_result:
                func, params, allowed_methods, required_cookies = route_result
                if requesting_method in allowed_methods:
                    missing_cookies = [
                        cookie["name"]
                        for cookie in required_cookies
                        if self.get_cookie(
                            cookie["name"], cookie.get("requires_auth", False)
                        )
                        is None
                    ]
                    if missing_cookies:
                        self._send_error(
                            403,
                            f"Missing required cookie(s): {', '.join(missing_cookies)}",
                            content_type="text/html; charset=utf-8",
                        )
                        return
                    try:
                        response = func(self, **params) if params else func(self)
                        self.send_response(200)
                        self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.end_headers()
                        if response is not None:
                            self.wfile.write(str(response).encode("utf-8"))
                        else:
                            logger.warning(f"Handler for '{self.path}' returned None")
                    except Exception as e:
                        logger.error("Error in handler for '%s': %s", self.path, str(e))
                        logger.debug(traceback.format_exc())
                        self._send_error(500, "Internal Server Error")
                    return
            self._send_error(404, "404 Not Found")
        except Exception as e:
            logger.error(f"Error dispatching route '{self.path}': {e}")
            logger.debug(traceback.format_exc())
            self._send_error(500, "Internal Server Error")

    def _send_error(
        self, code: int, message: str, content_type: str = "text/plain; charset=utf-8"
    ) -> None:
        try:
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            self.wfile.write(message.encode("utf-8"))
        except Exception as e:
            logger.error(f"Error sending error response: {e}")
            logger.debug(traceback.format_exc())


Response = TypeVar("Response", bound=Router)
