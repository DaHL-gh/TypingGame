from __future__ import annotations
from .types import Child, Parent

import moderngl as mgl
import freetype as ft
import numpy as np
import glm

from .mglmanagers import ProgramManager, BufferManager
from .gui_object import GUIObject, GUILayout
from ..settings import MONITOR_DPI, BASE_DIR


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
    def __init__(self,
                 parent: Parent,
                 glyph: Glyph,
                 texture: mgl.Texture,
                 pos: tuple[int, int] = (0, 0),
                 color: tuple[float, float, float] = (1, 1, 1)):
        self._color = color
        self._color_buffer = parent.ctx.buffer(glm.vec3(self._color))

        self.glyph = glyph
        super().__init__(parent, self.glyph.size, pos, ProgramManager(parent.ctx).get_program('text_render'), texture)
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
    def __init__(self,
                 parent: Parent,
                 size: tuple[int, int],
                 line: str,
                 font: Font,
                 program: mgl.Program,
                 texture: mgl.Texture | None = None,
                 pos: tuple[int, int] = (0, 0)):

        super().__init__(parent=parent, size=size, pos=pos, program=program, texture=texture)

        self._pen = (0, 0)
        self.max_vertical_advance = 0

        self._font = font

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
            glyph = self._font.get_glyph(ord(char))

            if glyph.vertical_advance > self.max_vertical_advance:
                self.max_vertical_advance = glyph.vertical_advance

            if char not in self._bitmap_textures:
                self._bitmap_textures[char] = self.ctx.texture(size=glyph.size, data=glyph.bitmap, components=1)
                self._bitmap_textures[char].filter = (mgl.NEAREST, mgl.NEAREST)

            self.widgets.append(Char(self, glyph, self._bitmap_textures[char]))

        self._update_layout()
        self._redraw()

    def _update_layout(self):
        self._framebuffer.use()

        self._pen = [0, self.max_vertical_advance]

        for char in self.widgets:
            if self._pen[0] + char.glyph.size[0] > self.size[0]:
                self._pen[0] = 0
                self._pen[1] += self.max_vertical_advance

            char.pos = (self._pen[0] + char.glyph.offset[0],
                        self._pen[1] - char.glyph.offset[1] - char.glyph.size[1])

            self._pen[0] += char.glyph.horizontal_advance

        self.ctx.screen.use()

    def _mouse_down_func(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return self

    def _mouse_drag_func(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        if button_name == 'left':
            self.pos = tuple(self.pos[i] + rel[i] for i in (0, 1))
        elif button_name == 'right':
            self.size = tuple(self.size[i] + rel[i] for i in (0, 1))

        return self

    def release(self, keep_texture=False):
        super().release(keep_texture)

        for x in self._bitmap_textures.values():
            x.release(keep_texture)
