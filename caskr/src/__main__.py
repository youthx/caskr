from caskr import Caskr, html, p, route, Response

caskr = Caskr(__name__)


@route("/")
def main(request: Response) -> int:
    return html(p("Welcome to caskr!"), p("We hope you like it here :)"))

@route("/register")
def register(request: Response) -> int:
    if request.cookie_jar.priority_client:
        return html(p("You are already registered!"))
    
    id = request.make_client_id()
    request.set_priority_client(id)
    return html(p(f"Your client ID is {id}"))


@route("/login/:id", method=["GET"])
def user(request: Response, id: str):
    if request.cookie_jar.priority_client:
        return html(p(f"Your already logged in as {request.cookie_jar.priority_client}"))
    
    if id == request.get_client_id():
        return html(p(f"Welcome back, {id}!"))
    
    return html(p("Client not found, please login @ localhost:8000/register"))



if __name__ == "__main__":
    with caskr.serve_forever() as server:
        pass
