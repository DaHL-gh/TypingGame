from __future__ import annotations
from ..misc.types import Child

import moderngl as mgl

from ..layouts.gui_layout import GUILayout
from .text_render import _Char, Font


class TextField(GUILayout):
    def __init__(self, font: Font, line='', **kwargs):
        super().__init__(**kwargs)

        self._font = font

        self._pen = (0, 0)
        self.visible_widgets_count = 0

        self.char_size = self._font.char_size
        self.line_height = self.char_size

        self._bitmap_textures: dict[str: mgl.Texture] = {}

        self.line = line

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def line(self) -> str:
        return self._line

    @line.setter
    def line(self, line: str):
        self._release_widgets(keep_texture=True)

        self._line = line
        for symbol in line:
            self._add_char(symbol)

    def _add_char(self, symbol: str) -> None:
        glyph = self._font.get_glyph(ord(symbol))

        if self._pen[0] + glyph.size[0] + glyph.offset[0] > self.size[0]:
            self._pen = (0, self._pen[1] + self.line_height)

        if symbol not in self._bitmap_textures:
            self._bitmap_textures[symbol] = self.ctx.texture(size=glyph.size, data=glyph.bitmap, components=1)

        char = _Char(parent=self, glyph=glyph, texture=self._bitmap_textures[symbol])
        self._update_char_pos(char)

        self.visible_widgets_count += 1
        self.redraw_request()

    # /////////////////////////////////////////////////// UPDATE ///////////////////////////////////////////////////////

    def _update_layout(self) -> None:
        self.visible_widgets_count = 0

        self._pen = [0, self.line_height]

        for char in self._widgets:
            if self._pen[0] + char.glyph.size[0] + char.glyph.offset[0] > self.size[0]:

                if self._pen[1] > self.height:
                    break
                self._pen = (0, self._pen[1] + self.line_height)

            self._update_char_pos(char)

            self.visible_widgets_count += 1

    def _update_char_pos(self, char: _Char):
        char.pos = (self._pen[0] + char.glyph.offset[0],
                    self._pen[1] - char.glyph.offset[1] - char.glyph.size[1])

        self._pen = (self._pen[0] + char.glyph.horizontal_advance, self._pen[1])

        if char.glyph.symbol == '\r' or char.glyph.symbol == '\n':
            self._pen = (0, self._pen[1] + self.line_height)

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def _redraw(self) -> None:
        i = 0
        for widget in self._widgets:
            widget.draw()

            i += 1
            if i == self.visible_widgets_count:
                break

    def set_color(self, i: int | slice, color: tuple[float, float, float]) -> None:
        if isinstance(i, int):
            self._widgets[i].color = color
        elif isinstance(i, slice):
            for w in self._widgets[i]:
                w.color = color

    def remove_last(self) -> None:
        if len(self._widgets) > 0:
            self.line = self.line[:-1]

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

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def release(self, keep_texture=False):
        if not keep_texture:
            for texture in self._bitmap_textures.values():
                texture.release()

        super().release(keep_texture)
