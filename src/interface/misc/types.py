from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from ..widgets.root import Root

    from ..layouts.linelayout import LineLayout
    from ..layouts.anchorlayout import AnchorLayout
    from ..layouts.floatlayout import FloatLayout

    from ..widgets.gui_object import GUIObject
    from ..widgets.text_field import TextField
    from ..widgets.text_line import TextLine
    from ..widgets.slider import Slider

    Parent = TypeVar('Parent', Root,
                     LineLayout, AnchorLayout, FloatLayout)
    Child = TypeVar('Child', LineLayout, AnchorLayout, FloatLayout,
                    GUIObject, TextLine, TextField, Slider)

else:
    GUI = None
    Parent = None
    Child = None
    Root = None
