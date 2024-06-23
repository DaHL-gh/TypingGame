from __future__ import annotations
from ..misc.types import Child

import moderngl as mgl
from typing import Callable

from .text_line import TextLine
from .text_render import _Char, Font


class TextInput(TextLine):
    def __init__(self, validate_func: Callable | None = None, placeholder: str = 'ввод', **kwargs):

        self._placeholder = placeholder
        if not 'line' in kwargs or kwargs['line'] == '':
            kwargs['line'] = self.placeholder

        super().__init__(**kwargs)

        glyph = self._font.get_glyph(ord('|'))
        glyph.offset = (0, glyph.offset[1])
        glyph.horizontal_advance = glyph.size[0]
        texture = self.ctx.texture(size=glyph.size, data=glyph.bitmap, components=1)
        self._text_cursor = _Char(parent=self, glyph=glyph, texture=texture)

        self._validate_func = validate_func

        self._widgets = [self._widgets[-1]] + self._widgets[:-1]

    def add(self, widget: Child) -> None:
        super().add(widget)
        if len(self._widgets) > 1:
            self._widgets[-2], self._widgets[-1] = self._widgets[-1], self._widgets[-2]

    @property
    def placeholder(self):
        return self._placeholder

    @TextLine.line.setter
    def line(self, line: str):
        TextLine.line.fset(self, line)

        if len(self._widgets) > 0:
            self._update_char_pos(self._widgets[-1])

    # //////////////////////////////////////////////////// INPUT ///////////////////////////////////////////////////////

    def out_focus(self):
        super().out_focus()
        if self.line == '':
            self.line = self.placeholder
        else:
            self.line = self.line

    def in_focus(self):
        super().in_focus()
        if self.line == self.placeholder:
            self.line = ''
        else:
            self.line = self.line

    def validate(self) -> None:
        if self._validate_func is not None:
            self._validate_func()

        self._validate()

    def _validate(self) -> None:
        pass

    def _keyboard_press(self, key: int, unicode: str) -> None:
        if unicode == '\b':  # BACKSPACE
            self.remove_last()
        elif unicode == '\x1b':  # ESCAPE
            pass
        elif unicode == '\t':  # TAB
            self.line += "    "
        else:
            self.line += unicode

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def set_color(self, i: int | slice, color: tuple[float, float, float]) -> None:
        if isinstance(i, int):
            self._widgets[i].color = color
        elif isinstance(i, slice):
            for w in self._widgets[i]:
                w.color = color

    def _redraw(self):
        for widget in self._widgets[:-1]:
            widget.draw()

        if self.is_in_focus:
            self._text_cursor.draw()

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def remove_last(self) -> None:
        if len(self._widgets) > 1:
            self._line = self._line[:-1]
            x = self._widgets.pop(-2)

            self._pen[0] -= x.glyph.horizontal_advance + self._text_cursor.glyph.horizontal_advance
            self._update_char_pos(self._text_cursor)

            x.release(keep_texture=True)

            self.redraw_request()

    def _release_widgets(self, keep_texture=False):
        if self._widgets:
            for widget in self._widgets[:-2]:
                widget.release(keep_texture)

            self._widgets = [self._widgets[-1]]
            self._widget_ids = {}

    def release(self, keep_texture=False):
        self._text_cursor.release(keep_texture)
        super().release(keep_texture)
