from http.server import BaseHTTPRequestHandler

from caskr import Caskr, html, p, route

caskr = Caskr(__name__)


@route("/")
def main() -> int:
    return html(p("Welcome to caskr!"), p("We hope you like it here :)"))


@route("user/:id", method=["GET"])
def user(request: BaseHTTPRequestHandler, id):
    return html(p(f"id: {id}"))


if __name__ == "__main__":
    with caskr.serve_forever() as server:
        pass
