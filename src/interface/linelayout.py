from __future__ import annotations

from .gui_object import GUILayout
from .types import Parent, Child


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
        min_width = min_height = 0

        if self.orientation == 'vertical':

            gathered_space = (self._padding * 2 +
                              self._spacing * (len(self._widgets) - 1) +
                              sum(self.fixed_sizes) +
                              sum(self.th_sizes) * self.height)

            if self.free_size_w_count != 0:
                filling_widget_size = int((self.width - gathered_space) / self.free_size_w_count)
            else:
                filling_widget_size = 0

            height_mem = self._padding
            for widget in self._widgets:

                if widget.base_width is not None:
                    w_w = widget.base_width
                elif widget.width_hint is not None:
                    w_w = int(widget.width_hint * self.width)
                else:
                    w_w = int(self.width - self._padding * 2)

                widget.pos = (self._padding + (self.width - self._padding * 2 - w_w) / 2, height_mem)

                if widget.base_height is not None:
                    w_h = widget.base_height
                elif widget.height_hint is not None:
                    w_h = int(widget.height_hint * self.height)
                else:
                    w_h = filling_widget_size

                widget.size = (w_w, w_h)

                min_width = max(min_width, widget.min_width)
                min_height += widget.min_height
                height_mem += self._spacing + w_h

            min_width += self._padding * 2
            min_height += self._padding * 2 + self._spacing * (len(self._widgets) - 1)

        else:
            gathered_space = (self._padding * 2 +
                              self._spacing * (len(self._widgets) - 1) +
                              sum(self.fixed_sizes) +
                              sum(self.th_sizes) * self.width)

            if self.free_size_w_count != 0:
                filling_widget_size = int((self.width - gathered_space) / self.free_size_w_count)
            else:
                filling_widget_size = 0

            width_mem = self._padding
            for widget in self._widgets:

                if widget.base_height is not None:
                    w_h = widget.base_height
                elif widget.height_hint is not None:
                    w_h = int(widget.height_hint * self.height)
                else:
                    w_h = int(self.height - self._padding * 2)

                widget.pos = (width_mem, self._padding + (self.height - self._padding * 2 - w_h) / 2)

                if widget.base_width is not None:
                    w_w = widget.base_width
                elif widget.height_hint is not None:
                    w_w = int(widget.width_hint * self.width)
                else:
                    w_w = filling_widget_size

                widget.size = (w_w, w_h)

                min_height = max(min_height, widget.min_height)
                min_width += widget.min_width
                width_mem += self._spacing + w_w

            min_height += self._padding * 2
            min_width += self._padding * 2 + self._spacing * (len(self._widgets) - 1)
        self._min_size = (min_width, min_height)

    def add(self, widget: Child):
        if self.orientation == 'vertical':
            if widget.base_height is not None:
                self.fixed_sizes.append(widget.height)
            elif widget.height_hint is not None:
                self.th_sizes.append(widget.height_hint)
            else:
                self.free_size_w_count += 1

        else:
            if widget.base_width is not None:
                self.fixed_sizes.append(widget.width)
            elif widget.width_hint is not None:
                self.th_sizes.append(widget.width_hint)
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

