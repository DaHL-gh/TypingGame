from __future__ import annotations
from .types import Child

import moderngl as mgl

from .root import Root

class GUI:
    def __init__(self, ctx: mgl.Context, size: tuple[int, int]):
        self._ctx = ctx
        self._size = size

        self._root_widget = Root(self.ctx)

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def ctx(self) -> mgl.Context:
        return self._ctx

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        self._size = value
        self._root_widget.size = value

    @property
    def width(self) -> int:
        return self._size[0]

    @property
    def height(self) -> int:
        return self._size[1]

    # //////////////////////////////////////////////////// MOUSE ///////////////////////////////////////////////////////

    def mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return self._root_widget.mouse_down(button_name, mouse_pos, count)

    def mouse_up(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        return self._root_widget.mouse_up(button_name, mouse_pos)

    def mouse_drag(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        return self._root_widget.mouse_drag(button_name, mouse_pos, rel)

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def draw(self) -> None:
        self._root_widget.draw()

    def toggle_bbox(self, state=None) -> None:
        self._root_widget.toggle_bbox(state)

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def release(self) -> None:
        self._root_widget.release()
