from s import html, p 

page = html(
    p("Hello world!", _class="text"),
)

print(page)
