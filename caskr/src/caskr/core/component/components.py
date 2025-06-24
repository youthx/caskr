
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


def p(
    *__content: str | _DOMComponent, **kwargs: Unpack[_ComponentAttributes]
) -> _DOMComponent:
    return _component("p", __content, {}, kwargs)
