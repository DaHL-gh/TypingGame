from __future__ import annotations
from dataclasses import dataclass
from ..interface.misc.types import Child

mouse_data: dict[int, str] = {1: 'left', 2: 'middle', 3: 'right'}


@dataclass
class MouseClick:
    pos: tuple[int, int]
    b_name: str

    def __init__(self, event):
        self.pos = event.dict['pos']

        b_num = event.dict['button']
        self.b_name = mouse_data[b_num] if b_num in mouse_data else None


@dataclass
class MouseMove:
    pos: tuple[int, int]
    rel: tuple[int, int]
    buttons: set[str]
    type: int

    def __init__(self, event):
        self.pos = event.dict['pos']
        self.rel = event.dict['rel']
        self.buttons = set(mouse_data[i + 1] if event.dict['buttons'][i] else '' for i in range(len(mouse_data)))
        if '' in self.buttons:
            self.buttons.remove('')
        self.type = event.type


@dataclass
class LastPress:
    pos: tuple[int, int] = (0, 0)
    time: int = 0
    count: int = 0
    b_name: str = ''
    widget: Child | None = None


@dataclass
class DragInfo:
    b_name: str = ''
    widget: Child | None = None
