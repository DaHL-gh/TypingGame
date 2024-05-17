from __future__ import annotations

import glm
import moderngl as mgl
import pygame as pg
import numpy as np
import freetype as ft

from functions import get_rect_vertices, convert_vec2, load_program, get_part_of_frame_buffer


class Glyph:
    def __init__(self, code: int, face: ft.Face):
        face.load_char(chr(code))

        glyph = face.glyph
        self.bitmap = np.array(glyph.bitmap.buffer, dtype='u1')
        self.glyph_size = (glyph.bitmap.width, glyph.bitmap.rows)

        glyph_bbox = glyph.get_glyph().get_cbox(ft.FT_GLYPH_BBOX_MODES['FT_GLYPH_BBOX_PIXELS'])
        self.offset = (glyph_bbox.xMin, glyph_bbox.yMin)

        self.horizontal_advance = glyph.linearHoriAdvance // 2 ** 16
        self.vertical_advance = glyph.linearVertAdvance // 2 ** 16


class Font:
    def __init__(self, name: str, char_size: int):
        self.name = name
        self.char_size = char_size

        self.face = ft.Face(f'fonts/{name}.ttf')
        w = h = char_size << 6
        self.face.set_char_size(width=w, height=h, hres=95, vres=95)

        self.loaded_glyphs = {}

    def get_glyph(self, code: int) -> Glyph:
        if code not in self.loaded_glyphs:
            self.loaded_glyphs[code] = Glyph(code, self.face)

        return self.loaded_glyphs[code]


class Char:
    def __init__(self, ctx: mgl.Context, glyph: Glyph, program: mgl.Program, bitmap_texture: mgl.Texture, pos=(0, 0)):
        self.ctx = ctx
        self.glyph = glyph

        self.vertices = self.ctx.buffer(reserve=32)
        self.pos = pos
        self.uv = self.ctx.buffer(np.array(((0, 0), (0, 1), (1, 0), (1, 1)), dtype='float32'))

        self.bitmap_texture = bitmap_texture

        self.program = program

        self.vao = self.ctx.vertex_array(self.program,
                                         [
                                             (self.vertices, '2f /v', 'in_position'),
                                             (self.uv, '2f /v', 'in_bitmap_cords'),
                                         ])

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos: tuple[int, int]):
        self._pos = pos
        self.vertices.write(get_rect_vertices(fb_size=self.ctx.fbo.size,
                                              rect_size=self.glyph.glyph_size,
                                              rect_pos=pos))

    def draw(self, mode=mgl.TRIANGLE_STRIP):
        self.bitmap_texture.use()
        self.vao.render(mode)

    def release(self):
        self.vertices.release()
        self.uv.release()

        self.vao.release()


class Renderer:
    def __init__(self, ctx: mgl.Context, font: Font, line: str, pos: tuple[int, int], size: tuple[int, int]):
        self.ctx = ctx
        self.font = font

        self.max_vertical_advance = 0
        self.pen = [0, 0]
        self.texture = ctx.texture((1, 1), components=1)
        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)

        self.chars = []
        self.bitmap_textures = {}

        self.program = load_program(self.ctx, 'text_render')

        self.vertices = self.ctx.buffer(reserve=32)
        self.framebuffer = self.ctx.framebuffer(self.texture)

        self.size = size
        self.pos = pos
        self.line = line

        self.uv = self.ctx.buffer(np.array(((0, 1), (0, 0), (1, 1), (1, 0)), dtype='float32'))

        self.vao = self.ctx.vertex_array(self.program,
                                         [
                                             (self.vertices, '2f /v', 'in_position'),
                                             (self.uv, '2f /v', 'in_bitmap_cords'),
                                         ])

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, line: str):
        self._release_chars()

        self._line = line
        for char in line:
            glyph = self.font.get_glyph(ord(char))

            if glyph.vertical_advance > self.max_vertical_advance:
                self.max_vertical_advance = glyph.vertical_advance

            if char not in self.bitmap_textures:
                self.bitmap_textures[char] = self.ctx.texture(size=glyph.glyph_size, data=glyph.bitmap, components=1)
                self.bitmap_textures[char].filter = (mgl.NEAREST, mgl.NEAREST)

            self.chars.append(Char(self.ctx, glyph, self.program, self.bitmap_textures[char]))

        self._update_char_pos()

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos: tuple[int, int]):
        self._pos = pos

        self.vertices.write(get_rect_vertices(pg.display.get_window_size(), self.size, self.pos))

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: tuple[int, int]):
        self._size = size

        self._update_framebuffer()

    def _update_framebuffer(self):
        self.framebuffer.release()
        self.framebuffer = self.ctx.framebuffer(self.ctx.texture(size=self.size, components=4))

        self._update_char_pos()

    def _update_char_pos(self):
        self.framebuffer.use()

        self.pen = [0, self.max_vertical_advance]

        for char in self.chars:
            if self.pen[0] + char.glyph.glyph_size[0] > self.size[0]:
                self.pen[0] = 0
                self.pen[1] += self.max_vertical_advance

            char.pos = (self.pen[0] + char.glyph.offset[0],
                        self.pen[1] - char.glyph.offset[1] - char.glyph.glyph_size[1])

            self.pen[0] += char.glyph.horizontal_advance

        self._update_texture()

        self.ctx.screen.use()

    def _update_texture(self):
        self.framebuffer.clear(0)

        for char in self.chars:
            char.draw(mgl.TRIANGLE_STRIP)

        self.texture.release()
        self.texture = self.ctx.texture(size=self.size, components=4, data=self.framebuffer.read(components=4))

    def draw(self, mode=mgl.TRIANGLE_STRIP):

        self.texture.use()
        self.vao.render(mode)

    def _release_chars(self):
        for char in self.chars:
            char.release()
        self.chars = []

    def release(self):
        self.program.release()

        for bitmap in self.bitmap_textures.values():
            bitmap.release()

        self._release_chars()

    def contains_dot(self, cords: list[int | float, int | float] | tuple[int | float, int | float]) -> bool:
        return all(0 < cords[i] - self.pos[i] < self.size[i] for i in (0, 1))

    def drag(self, mouse_pos):
        self.pos = mouse_pos

    def move(self, offset: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        self.pos = tuple(int(self.pos[i] + offset[i]) for i in (0, 1))

    def update_vertices(self):
        self.pos = self.pos