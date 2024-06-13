from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .gui import GUI
    from .gui_object import GUIObject, GUILayout
    from .text_render import TextField, Char

    Parent = TypeVar('Parent', GUI, GUILayout, TextField)
    Child = TypeVar('Child', GUIObject, GUILayout, TextField, Char)

else:
    Parent = None
    Child = None
