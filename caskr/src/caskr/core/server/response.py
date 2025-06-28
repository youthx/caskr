class Response:
    def __init__(self, body='', status='200 OK', headers=None, content_type='text/html', method=None):
        self._body = body.encode('utf-8') if isinstance(body, str) else body 
        self._status = status 
        self._headers = headers or []
        self._headers.append(('Content-Type', content_type))
        self._cookies = []
        self._method = method  # Add method attribute

    def set_cookie(self, key, value, path='/', max_age=None):
        cookie = f"{key}={value}; Path={path}"
        if max_age is not None:
            cookie += f"; Max-Age={max_age}"
        self._cookies.append(cookie)

    def get_headers(self):
        headers = self._headers[:]
        for cookie in self._cookies:
            headers.append(('Set-Cookie', cookie))
        return headers 

    @property 
    def cookies(self):
        return self._cookies

    @property
    def body(self):
        return self._body

    @property
    def status(self):
        return self._status

    @property
    def method(self):
        return self._method

    def __str__(self) -> str:
        # Build the response string
        response = f"HTTP/1.1 {self.status}\r\n"
        for header, value in self.get_headers():
            response += f"{header}: {value}\r\n"
        response += "\r\n"
        response += self.body.decode('utf-8') if isinstance(self.body, bytes) else self.body
        return response