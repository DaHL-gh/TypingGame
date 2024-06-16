from __future__ import annotations
from .types import Child, Parent

import moderngl as mgl
import freetype as ft
import numpy as np
import glm

from .mglmanagers import ProgramManager, BufferManager
from .gui_object import GUIObject, GUILayout
from ..settings import MONITOR_DPI, BASE_DIR
from .constants import *


class Glyph:
    def __init__(self, code: int, face: ft.Face):
        self.symbol = chr(code)
        face.load_char(self.symbol)

        ft_glyph = face.glyph
        self.bitmap = np.array(ft_glyph.bitmap.buffer, dtype='u1')
        self.size = (ft_glyph.bitmap.width, ft_glyph.bitmap.rows)

        bbox = ft_glyph.get_glyph().get_cbox(ft.FT_GLYPH_BBOX_MODES['FT_GLYPH_BBOX_PIXELS'])
        self.offset = (bbox.xMin, bbox.yMin)

        self.horizontal_advance = ft_glyph.linearHoriAdvance >> 16
        self.vertical_advance = ft_glyph.linearVertAdvance >> 16


class Font:
    def __init__(self, name: str, char_size: int):
        self.name = name
        self.char_size = char_size

        self.face = ft.Face(f'{BASE_DIR}/data/fonts/{name}.ttf')
        w = h = char_size << 6
        self.face.set_char_size(width=w, height=h, hres=int(MONITOR_DPI), vres=int(MONITOR_DPI))

        self.loaded_glyphs = {}

    def get_glyph(self, code: int) -> Glyph:
        if code not in self.loaded_glyphs:
            self.loaded_glyphs[code] = Glyph(code, self.face)

        return self.loaded_glyphs[code]


class Char(GUIObject):
    def __init__(self, glyph: Glyph, color: tuple[float, float, float] = (1, 1, 1), **kwargs):
        self._color = color
        self._color_buffer = kwargs['parent'].ctx.buffer(glm.vec3(self._color))

        self.glyph = glyph
        super().__init__(size=self.glyph.size,
                         program=ProgramManager(kwargs['parent'].ctx).get_program('text_render'), **kwargs)

        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)

    def _get_vao(self):
        self._vao = self.ctx.vertex_array(self._program,
                                          [
                                              (self._vertices, '2f /v', 'in_position'),
                                              (BufferManager(self.ctx).get_buffer('UV'), '2f /v', 'in_texture_cords'),
                                              (self._color_buffer, '3f /i', 'in_color')
                                          ])

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: tuple[float, float, float]):
        self._color = value
        self._color_buffer.write(glm.vec3(self._color))


class TextField(GUILayout):
    def __init__(self, font: Font, line: str = '', **kwargs):
        super().__init__(**kwargs)

        self._font = font

        self._pen = (0, 0)
        self.line_height = self._font.char_size * 2
        self.visible_widgets_count = 0

        self._bitmap_textures: dict[str: mgl.Texture] = {}

        self.line = line

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, line: str):
        self._release_widgets(keep_texture=True)

        self._line = line
        for char in line:
            self._add_char(char)

        self.redraw()

    def _add_char(self, char: str):
        glyph = self._font.get_glyph(ord(char))

        if self._pen[0] + glyph.size[0] + glyph.offset[0] > self.size[0]:
            self._pen = (0, self._pen[1] + self.line_height)

        if char not in self._bitmap_textures:
            self._bitmap_textures[char] = self.ctx.texture(size=glyph.size, data=glyph.bitmap, components=1)
            self._bitmap_textures[char].filter = (mgl.NEAREST, mgl.NEAREST)

        pos = (self._pen[0] + glyph.offset[0],
               self._pen[1] - glyph.offset[1] - glyph.size[1])

        self.visible_widgets_count += 1

        self._pen = (self._pen[0] + glyph.horizontal_advance, self._pen[1])

        Char(parent=self, pos=pos, glyph=glyph, texture=self._bitmap_textures[char])

        if char == '\r' or char == '\n':
            self._pen = (0, self._pen[1] + self.line_height)

    def _update_layout(self) -> None:
        self.visible_widgets_count = 0

        self._pen = [0, self.line_height]

        for char in self._widgets:
            if self._pen[0] + char.glyph.size[0] + char.glyph.offset[0] > self.size[0]:

                if self._pen[1] > self.height:
                    break
                self._pen = (0, self._pen[1] + self.line_height)

            char.pos = (self._pen[0] + char.glyph.offset[0],
                        self._pen[1] - char.glyph.offset[1] - char.glyph.size[1])

            self._pen = (self._pen[0] + char.glyph.horizontal_advance, self._pen[1])

            if char.glyph.symbol == '\r' or char.glyph.symbol == '\n':
                self._pen = (0, self._pen[1] + self.line_height)

            self.visible_widgets_count += 1

    def append_line(self, line: str):
        for char in line:
            self._add_char(char)

        self.redraw()

    def redraw(self):
        self.framebuffer.use()
        self.framebuffer.clear()

        i = 0
        for widget in self._widgets:
            widget.draw()

            i += 1
            if i == self.visible_widgets_count:
                break

        self.parent.redraw()

    def remove_last(self):
        if len(self._widgets) > 0:
            x = self._widgets.pop(len(self._widgets) - 1)
            x.release(keep_texture=True)

            self._update_layout()
            self.redraw()

    def _keyboard_press(self, key: int, unicode: str):
        print('press')
        if unicode == '\t':
            self.append_line("    ")
        elif unicode == '\x1b':  # escape
            pass
        elif unicode == '\b':  # backspace
            self.remove_last()
        else:
            self.append_line(unicode)

    def _mouse_down_func(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return self
