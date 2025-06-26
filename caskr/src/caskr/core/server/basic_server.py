from http.server import HTTPServer

from caskr.core.utils import env, logger

from .request import _RequestHandler


# The `BasicServerContext` class is a custom context manager for an HTTP server that can be used with
# the `with` statement.
class BasicServerContext(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.log("Shutting down HTTP server..")
        self.shutdown()
        self.server_close()


def serve_forever(
    request_handler: _RequestHandler,
    server_context: type[HTTPServer] = BasicServerContext,
    host: str = "localhost",
    port: int = 8000,
) -> HTTPServer:
    env.set("caskr_httpserver_host", host)
    env.set("caskr_httpserver_port", port)

    context = server_context((host, port), request_handler)
    logger.log("Serving on http://{}:{}".format(host, port))

    # context.log("Serving HTTP forever...")  # log before running
    context.serve_forever(1)

    return context
