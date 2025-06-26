from caskr.core.config import CaskrGlobalConf
from caskr.core.server.request import BaseHTTPRequestHandler
from caskr.core.utils.logger import logger


class Router(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self._dispatch("GET")
    
    def do_POST(self):
        self._dispatch("POST")
            
    def _dispatch(self, requesting_method: str):
        route_result = CaskrGlobalConf.route_dir.get_handler(self.path)

        if route_result:
            func = route_result[0]
            params = route_result[1]
            allowed_methods = route_result[2]
            required_cookies = route_result[3]
            if requesting_method in allowed_methods:
                # Validate required cookies
                client_cookies = self.headers.get("Cookie", "")
                cookie_dict = {
                    pair.split("=")[0].strip(): pair.split("=")[1].strip()
                    for pair in client_cookies.split(";") if "=" in pair
                }

                for cookie_name in required_cookies:
                    if cookie_name not in cookie_dict:
                        self.send_response(403)
                        self.end_headers()
                        self.wfile.write(
                            f"Missing required cookie: {cookie_name}".encode()
                        )
                        return

                try:
                    if params:
                        response = func(self, **params)
                    else:
                        response = func(self)

                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(str(response).encode())
                    return

                except Exception as e:
                    logger.error("Error in handler for '%s': %s", self.path, str(e))
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b"Internal Server Error")
                    return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"404 Not Found")
