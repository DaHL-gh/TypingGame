from __future__ import annotations
from ..misc.types import Child

import dataclasses
from typing import Any
import moderngl as mgl

from .gui_object import GUIObject
from ..layouts.gui_layout import GUILayout


@dataclasses.dataclass
class _Bind:
    cls: Any
    attr_name: str
    min_v: int
    max_v: int


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

        # bar
        self._bar_width = bar_width
        self._bar = GUIObject(parent=self, id='bar', texture=bar_texture)

        # slider
        self._slider_width = slider_width
        self._value = 0
        self._slider = GUIObject(parent=self, id='slider', texture=slider_texture)

        # bind
        self._binds: list[_Bind] = []

    @property
    def orientation(self):
        return self._orientation

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

        for bind in self._binds:
            setattr(bind.cls, bind.attr_name, int(self._value * (bind.max_v - bind.min_v) + bind.min_v))

        self.update_request()

    def add_bind(self, cls_ref, attr_name: str, min_v, max_v) -> None:
        self._binds.append(_Bind(cls_ref, attr_name, min_v, max_v))

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

    def _mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return self

    def _mouse_drag(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        if self.orientation == 'vertical':
            if mouse_pos[1] < self._slider_width / 2:
                self.value = 0.
            elif mouse_pos[1] > self.height - self._slider_width / 2:
                self.value = 1.
            else:
                self.value = (mouse_pos[1] - self._slider_width / 2) / (self.height - self._slider_width)
        else:
            if mouse_pos[0] < self._slider_width / 2:
                self.value = 0.
            elif mouse_pos[0] > self.width - self._slider_width / 2:
                self.value = 1.
            else:
                self.value = (mouse_pos[0] - self._slider_width / 2) / (self.width - self._slider_width)
