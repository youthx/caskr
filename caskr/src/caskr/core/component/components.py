from typing import Unpack

from .basecomponent import _component, _ComponentAttributes, _DOMComponent


def html(
    *__content: str | _DOMComponent,
    manifest: str | None = None,
    version: str | None = None,
    xmlns: str | None = None,
    **kwargs: Unpack[_ComponentAttributes],
) -> _DOMComponent:
    return _component(
        "html",
        __content,
        {"manifest": manifest, "version": version, "xmlns": xmlns},
        kwargs,
    )


def head(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("head", __content, {}, kwargs)


def body(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("body", __content, {}, kwargs)


def div(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("div", __content, {}, kwargs)


def span(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("span", __content, {}, kwargs)


def p(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("p", __content, {}, kwargs)


def h1(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("h1", __content, {}, kwargs)


def h2(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("h2", __content, {}, kwargs)


def h3(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("h3", __content, {}, kwargs)


def h4(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("h4", __content, {}, kwargs)


def h5(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("h5", __content, {}, kwargs)


def h6(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("h6", __content, {}, kwargs)


def ul(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("ul", __content, {}, kwargs)


def ol(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("ol", __content, {}, kwargs)


def li(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("li", __content, {}, kwargs)


def a(
    *__content: str | _DOMComponent,
    href: str | None = None,
    target: str | None = None,
    rel: str | None = None,
    **kwargs: Unpack[_ComponentAttributes],
) -> _DOMComponent:
    return _component(
        "a",
        __content,
        {"href": href, "target": target, "rel": rel},
        kwargs,
    )


def img(
    *,
    src: str,
    alt: str | None = None,
    width: str | int | None = None,
    height: str | int | None = None,
    **kwargs: Unpack[_ComponentAttributes],
) -> _DOMComponent:
    return _component(
        "img",
        (),
        {"src": src, "alt": alt, "width": width, "height": height},
        kwargs,
    )


def br(**kwargs: Unpack[_ComponentAttributes]) -> _DOMComponent:
    return _component("br", (), {}, kwargs)


def hr(**kwargs: Unpack[_ComponentAttributes]) -> _DOMComponent:
    return _component("hr", (), {}, kwargs)


def strong(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("strong", __content, {}, kwargs)


def em(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("em", __content, {}, kwargs)


def code(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("code", __content, {}, kwargs)


def pre(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("pre", __content, {}, kwargs)


def table(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("table", __content, {}, kwargs)


def thead(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("thead", __content, {}, kwargs)


def tbody(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("tbody", __content, {}, kwargs)


def tr(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("tr", __content, {}, kwargs)


def th(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("th", __content, {}, kwargs)


def td(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("td", __content, {}, kwargs)
