# SPDX-FileCopyrightText: 2025-present youthx <youthxf@gmail.com>
#
# SPDX-License-Identifier: MIT
import platform
import sys
import time

from caskr.core.component import html, p
from caskr.core.config import CaskrGlobalConf
from caskr.core.router import Router, route, route_get_handler, route_set_handler
from caskr.core.router.routes import _RouteDirectory
from caskr.core.server.basic_server import BasicServerContext, serve_forever
from caskr.core.utils.logger import logger, set_log_level, setup_logger


# The `Caskr` class is a Python class that initializes with a name attribute and a route directory,
# and provides a method to serve a server forever.
class Caskr(object):
    def __init__(self, name: str = "__main__"):
        """
        The function initializes an object with a specified name and sets a route base directory for a
        global configuration.

        @param name The `name` parameter in the `__init__` method is a string parameter with a default value
        of `"__main__"`. It is used to initialize the `name` attribute of the class instance.
        """
        self.name = name
        self.route_directory = _RouteDirectory()
        self.platform = platform

        CaskrGlobalConf.set_route_base_directory(self.route_directory)
    def uptime(self):
        time.time() - self.start_time

    def _route_info(self):
        return html(
            "Caskr Server Info",
            f"""<br>--------------------------<br>
        server-name: {self.name}<br>
        platform-version: {self.platform.python_version()}<br>
        platform: {self.platform.platform()}<br>
        executable: {sys.executable}<br>
        uptime: {self.uptime()}<br>
        --------------------------
        """,
        )

    def serve_forever(self, hostname: str = "localhost", port: int = 8000):
        """
        The `serve_forever` function starts a server with the specified hostname and port using
        BasicServerContext and Router.

        @param hostname The `hostname` parameter in the `serve_forever` method specifies the host on which
        the server will listen for incoming connections. By default, it is set to "localhost", which means
        the server will only accept connections from the local machine. If you want the server to accept
        connections from other devices
        @param port The `port` parameter specifies the port number on which the server will listen for
        incoming connections. In this case, the default port number is set to 8000 if no specific port is
        provided when calling the `serve_forever` method.

        @return The `serve_forever` method is returning the result of calling the `serve_forever` function
        with the arguments `BasicServerContext`, `Router`, `hostname`, and `port`.
        """
        @route("caskr/info", method="GET")
        def _info():
            return self._route_info()

        self.start_time = time.time()

        return serve_forever(Router, BasicServerContext, hostname, port)


__all__ = [
    "Caskr",
    "serve_forever",
    "setup_logger",
    "set_log_level",
    "logger",
    "BasicServerContext",
    "Router",
    "route",
    "route_get_handler",
    "route_set_handler",
    "htmlp",
]
