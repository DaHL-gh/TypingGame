from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .root import Root

    from .linelayout import LineLayout
    from .anchorlayout import AnchorLayout
    from .floatlayout import FloatLayout

    from .gui_object import GUIObject
    from .text_render import TextField
    from .slider import Slider

    Parent = TypeVar('Parent', Root, LineLayout, AnchorLayout, FloatLayout)
    Child = TypeVar('Child', LineLayout, AnchorLayout, FloatLayout, GUIObject, TextField, Slider)

else:
    Parent = None
    Child = None
