from __future__ import annotations

import moderngl as mgl

from .gui_object import GUILayout
from .types import Parent, Child
from .constants import *


class LineLayout(GUILayout):
    def __init__(self, padding=20, spacing=20, orientation='vertical', **kwargs):
        super().__init__(**kwargs)

        self._padding = padding
        self._spacing = spacing
        self._orientation = orientation

    @property
    def orientation(self):
        return self._orientation

    def _update_layout(self) -> None:
        if self.orientation == 'vertical':

            gathered_space = self._padding * 2 + self._spacing * (len(self._widgets) - 1)
            free_size_w_count = 0
            max_min_w = 0
            min_h = 0
            for widget in self._widgets:
                max_min_w = max(max_min_w, widget.min_size[0])
                min_h += widget.min_size[1]
                if widget.size_hints[1] == NONE:
                    free_size_w_count += 1
                else:
                    gathered_space += widget.size[1]

            self.min_size = (max_min_w + self._padding * 2, self._padding * 2 + min_h + self._spacing * (len(self._widgets) - 1))

            x = int((self.size[1] - gathered_space) / free_size_w_count)
            pos_mem = self._padding
            for widget in self._widgets:
                widget.pos = (self._padding, pos_mem)
                if widget.size_hints[1] == NONE:
                    pos_mem += x
                    widget.size = (int(self.size[0] - self._padding * 2), x)
                else:
                    pos_mem += self.size * widget.size_hints[1]
                    widget.size = (int(self.size[0] - self._padding * 2), int(self.size * widget.size_hints[1]))

                pos_mem += self._spacing



    def _mouse_down_func(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return self

    def _mouse_drag_func(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        if button_name == 'left':
            self.pos = tuple(self.pos[i] + rel[i] for i in (0, 1))
        elif button_name == 'right':
            self.size = tuple(self.size[i] + rel[i] for i in (0, 1))

        return self

