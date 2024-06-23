from __future__ import annotations

import moderngl as mgl
import freetype as ft
import numpy as np
import glm

from ..misc.mglmanagers import ProgramManager, BufferManager
from .gui_object import GUIObject
from ...settings import MONITOR_DPI, BASE_DIR


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


class _Char(GUIObject):
    def __init__(self, glyph: Glyph, color: tuple[float, float, float] = (1, 1, 1), **kwargs):
        self._color = color
        self._color_buffer = kwargs['parent'].ctx.buffer(glm.vec3(self._color))

        self._glyph = glyph
        super().__init__(size=self._glyph.size,
                         program=ProgramManager(kwargs['parent'].ctx).get('text_render'), **kwargs)

    def _get_vao(self) -> mgl.VertexArray:
        return self.ctx.vertex_array(self._program,
                                     [
                                         (self._vertices, '2f /v', 'in_position'),
                                         (BufferManager(self.ctx).get('UV'), '2f /v', 'in_texture_cords'),
                                         (self._color_buffer, '3f /i', 'in_color')
                                     ])

    @property
    def glyph(self):
        return self._glyph

    @property
    def color(self) -> tuple[float, float, float]:
        return self._color

    @color.setter
    def color(self, value: tuple[float, float, float]):
        self._color = value
        self._color_buffer.write(glm.vec3(self._color))

    def release(self, keep_texture=False):
        self._color_buffer.release()

        super().release(keep_texture)

