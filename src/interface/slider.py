from __future__ import annotations
import moderngl as mgl

from .mglmanagers import TextureManager
from .gui_object import GUILayout, GUIObject
from .types import Parent, Child
from .constants import *


class Slider(GUILayout):
    def __init__(self,
                 parent: Parent,
                 bar_width: int = 10,
                 slider_width: int = 10,
                 size: tuple[int, int] = (1, 1),
                 pos: tuple[int, int] = (0, 0),
                 min_size: tuple[int, int] = None,
                 size_hints: tuple[float | int, float | int] = (NONE, NONE),
                 program: mgl.Program | None = None,
                 texture: mgl.Texture | None = None,
                 slider_texture: mgl.Texture | None = None,
                 bar_texture: mgl.Texture | None = None):

        super().__init__(parent=parent, size=size, pos=pos, min_size=min_size,
                         size_hints=size_hints, program=program, texture=texture)

        self.slider_width = slider_width
        self.slider_pos = slider_width / 2
        self.slider = GUIObject(self, texture=slider_texture)

        self.bar_width = bar_width
        self.bar = GUIObject(self, texture=bar_texture)

        self._widgets.append(self.bar)
        self._widgets.append(self.slider)

    def _update_layout(self) -> None:
        self.slider.pos = (int(self.slider_pos - self.slider_width / 2), 0)
        self.slider.size = (self.slider_width, self.height)

        self.bar.pos = (int(self.slider_width / 2), int((self.height - self.bar_width) / 2))
        self.bar.size = (self.width - self.slider_width, self.bar_width)

    def _mouse_down_func(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return self

    def _mouse_drag_func(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        if self.slider_width / 2 < mouse_pos[0] < self.width - self.slider_width / 2:
            self.slider_pos = mouse_pos[0]

        self._update_layout()
        self.redraw()

        return self


