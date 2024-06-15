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

        self.fixed_sizes = []
        self.th_sizes = []
        self.free_size_w_count = 0

    @property
    def orientation(self):
        return self._orientation

    def _update_layout(self) -> None:
        if self.orientation == 'vertical':

            gathered_space = (self._padding * 2 +
                              self._spacing * (len(self._widgets) - 1) +
                              sum(self.fixed_sizes) +
                              sum(self.th_sizes) * self.height)

            filling_widget_size = (self.height - gathered_space) / self.free_size_w_count

            height_mem = self._padding
            for widget in self._widgets:

                if widget.base_width is not None:
                    widget.width = widget.base_width
                elif widget.width_hint is not None:
                    widget.width = int(widget.width_hint * self.width)
                else:
                    widget.width = self.width - self._padding * 2

                widget.pos = (self._padding + (self.width - self._padding * 2 - widget.width) / 2, height_mem)

                if widget.base_height is not None:
                    height_mem += widget.base_height
                    widget.height = widget.base_height
                elif widget.height_hint is not None:
                    height_mem += widget.height_hint * self.height
                    widget.height = int(widget.height_hint * self.height)
                else:
                    height_mem += filling_widget_size
                    widget.height = filling_widget_size

                height_mem += self._spacing

    def add(self, widget: Child):
        if self.orientation == 'vertical':
            if widget.base_height is not None:
                self.fixed_sizes.append(widget.height)
            elif widget.height_hint is not None:
                self.th_sizes.append(widget.height_hint)
            else:
                self.free_size_w_count += 1

        super().add(widget)

    def _mouse_down_func(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return self

    def _mouse_drag_func(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        if button_name == 'left':
            self.pos = tuple(self.pos[i] + rel[i] for i in (0, 1))
        elif button_name == 'right':
            self.size = tuple(self.size[i] + rel[i] for i in (0, 1))

        return self

