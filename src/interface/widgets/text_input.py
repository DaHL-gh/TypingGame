from __future__ import annotations
from ..misc.types import Child

import moderngl as mgl

from .text_line import TextLine
from .text_render import _Char, Font


class TextInput(TextLine):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def line(self) -> str:
        return self._line

    @line.setter
    def line(self, line: str):
        self._pen = [0, self.line_height]
        self._release_widgets(keep_texture=True)

        self._line = line
        for symbol in line:
            self._add_char(symbol)

        self._min_size = (self._pen[0], int(self.line_height + self.char_size / 2))
        self._base_size = self.min_size
        self.size = self._min_size

    def _add_char(self, symbol: str) -> None:
        glyph = self._font.get_glyph(ord(symbol))

        if symbol not in self._bitmap_textures:
            self._bitmap_textures[symbol] = self.ctx.texture(size=glyph.size, data=glyph.bitmap, components=1)

        char = _Char(parent=self, glyph=glyph, texture=self._bitmap_textures[symbol])
        self._update_char_pos(char)

        self.redraw_request()

    # /////////////////////////////////////////////////// UPDATE ///////////////////////////////////////////////////////

    def _update_layout(self) -> None:
        self._pen = [0, self.line_height]

        for char in self._widgets:
            self._update_char_pos(char)

    def _update_char_pos(self, char: _Char):
        char.pos = (self._pen[0] + char.glyph.offset[0],
                    self._pen[1] - char.glyph.offset[1] - char.glyph.size[1])

        self._pen[0] += char.glyph.horizontal_advance

    # //////////////////////////////////////////////////// INPUT ///////////////////////////////////////////////////////

    def _mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return self

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

    def _redraw(self) -> None:
        for widget in self._widgets:
            widget.draw()

    def set_color(self, i: int | slice, color: tuple[float, float, float]) -> None:
        if isinstance(i, int):
            self._widgets[i].color = color
        elif isinstance(i, slice):
            for w in self._widgets[i]:
                w.color = color

    def remove_last(self) -> None:
        if len(self._widgets) > 0:
            self._line = self._line[:-1]
            x = self._widgets.pop()
            self._pen[0] -= x.glyph.horizontal_advance
            self.size = (self._pen[0], int(self.line_height + self.char_size / 2))

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def release(self, keep_texture=False):
        if not keep_texture:
            for texture in self._bitmap_textures.values():
                texture.release()

        super().release(keep_texture)
