from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from ..widgets.root import Root

    from ..layouts.linelayout import LineLayout
    from ..layouts.anchorlayout import AnchorLayout
    from ..layouts.floatlayout import FloatLayout

    from ..widgets.gui_object import GUIObject
    from ..widgets.text_render import TextField
    from ..widgets.slider import Slider

    Parent = TypeVar('Parent', Root, LineLayout, AnchorLayout, FloatLayout)
    Child = TypeVar('Child', LineLayout, AnchorLayout, FloatLayout, GUIObject, TextField, Slider)

else:
    Parent = None
    Child = None
