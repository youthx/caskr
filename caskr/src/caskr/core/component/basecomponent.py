from typing import NotRequired, TypedDict, Any

NEWLINE = "\n"

class _Component(object):
    
    def __init__(self, context: str) -> None:
        self._context = str(context)
    
    def __str__(self) -> str:
        return self._context
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._context!r})"
    
    __text__ = __str__ 
    
class _DOMComponent(_Component):
    
    def __init__(self, context: str | _Component) -> None:
        super().__init__(str(context))
        self.compiler_ready = False 
    
        
class _ComponentAttributes(TypedDict):
    
    # --- Allowed Class Attribute Names ---
    _class: NotRequired[str]
    className: NotRequired[str]
    cls: NotRequired[str]
    # -------------------------------------
    
def _component(
    name: str,
    text: tuple[str | _Component],
    data: dict[str, Any],
    kwargs: _ComponentAttributes,
) -> _DOMComponent:
    attributes: dict[str, str | None] = {**kwargs, **data}

    cls = kwargs.get("_class") or kwargs.get("className") or kwargs.get("cls")
    if cls:
        attributes["class"] = cls
        for k in ("_class", "className", "cls"):
            if kwargs.get(k):
                kwargs.pop(k)
                attributes.pop(k)

    for k, v in kwargs.items():
        if isinstance(v, bool):
            attributes[k] = "true" if v else "false"

    for k, v in (kwargs.get("data") or {}).items():
        attributes[f"data-{k}"] = v

    attr_lines = []

    for k, v in attributes.items():
        if v is None:
            continue

        k = k.replace("_", "-")

        if v:
            attr_lines.append(f"{k}={v!r}")
        else:
            attr_lines.append(f"{k}")

    attrs = "".join(" " + str(a) for a in attr_lines)

    return _DOMComponent(
        f"<{name}{attrs}>{NEWLINE.join([str(i) for i in text])}</{name}>"
    )
 