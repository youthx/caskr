import logging
import queue
import socket
import threading
from http.server import BaseHTTPRequestHandler

logger = logging.getLogger("caskr@root")



# The `_RequestHandler` class is a subclass of `BaseHTTPRequestHandler` in Python that handles GET
# requests and logs messages
class _RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logger.info("%s - - %s", self.client_address[0], format % args)

    def do_GET(self):
        # self.log(f"Received GET request: {self.path}")

        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Hello, world!")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
