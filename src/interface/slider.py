from __future__ import annotations
import moderngl as mgl

from .mglmanagers import TextureManager
from .gui_object import GUILayout, GUIObject
from .types import Parent, Child
from .constants import *


class Slider(GUILayout):
    def __init__(self,
                 orientation: str = 'horizontal',
                 slider_width: int = 10,
                 bar_width: int = 10,
                 slider_texture: mgl.Texture | None = None,
                 bar_texture: mgl.Texture | None = None,
                 **kwargs):

        super().__init__(**kwargs)

        self._orientation = orientation

        self._bar_width = bar_width
        self._bar = GUIObject(self, texture=bar_texture)

        self._slider_width = slider_width
        self._value = 0
        self._slider = GUIObject(self, texture=slider_texture)

    @property
    def orientation(self):
        return self._orientation

    def _update_layout(self) -> None:
        if self.orientation == 'vertical':
            self._slider.pos = (0, int(self._value * (self.height - self._slider_width)))
            self._slider.size = (self.width, self._slider_width)

            self._bar.pos = (int((self.width - self._bar_width) / 2), int(self._slider_width / 2))
            self._bar.size = (self._bar_width, self.height - self._slider_width)
        else:
            self._slider.pos = (int(self._value * (self.width - self._slider_width)), 0)
            self._slider.size = (self._slider_width, self.height)

            self._bar.size = (self.width - self._slider_width, self._bar_width)
            self._bar.pos = (int(self._slider_width / 2), int((self.height - self._bar_width) / 2))

    def _mouse_down_func(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return self

    def _mouse_drag_func(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        if self.orientation == 'vertical':
            if mouse_pos[1] < self._slider_width / 2:
                self._value = 0.
            elif mouse_pos[1] > self.height - self._slider_width / 2:
                self._value = 1.
            else:
                self._value = (mouse_pos[1] - self._slider_width / 2) / (self.height - self._slider_width)
        else:
            if mouse_pos[0] < self._slider_width / 2:
                self._value = 0.
            elif mouse_pos[0] > self.width - self._slider_width / 2:
                self._value = 1.
            else:
                self._value = (mouse_pos[0] - self._slider_width / 2) / (self.width - self._slider_width)

        self._update_layout()
        self.redraw()

        return self


