import moderngl as mgl
import pygame as pg
import numpy as np
import freetype as ft
import glm

from glmanager import GlManager
from functions import get_rect_vertices, convert_vec2


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
    def __init__(self, gl_manager: GlManager, glyph: Glyph, program: mgl.Program, texture: mgl.Texture):
        self.gl_manager = gl_manager
        self.glyph = glyph

        self.vertices = self.gl_manager.ctx.buffer(reserve=32)
        self.uv = self.gl_manager.ctx.buffer(np.array(((0, 0), (0, 1), (1, 0), (1, 1)), dtype='float32'))
        self.color = self.gl_manager.ctx.buffer(glm.vec3((1, 1, 1)))

        self.texture = texture
        self.program = program

        self.vao = self.gl_manager.ctx.vertex_array(self.program,
                                                    [
                                                        (self.vertices, '2f /v', 'in_position'),
                                                        (self.uv, '2f /v', 'in_bitmap_cords'),
                                                        (self.color, '3f /i', 'in_color')
                                                    ])

    def update_vertices(self, pos):
        self.vertices.write(get_rect_vertices(w_size=pg.display.get_window_size(),
                                              rect_size=self.glyph.glyph_size,
                                              rect_pos=pos))

    def draw(self, mode=mgl.TRIANGLE_STRIP):
        self.texture.use()
        self.vao.render(mode)

    def release(self):
        self.vertices.release()
        self.uv.release()
        self.color.release()

        self.vao.release()


class Renderer:
    def __init__(self, gl_manager: GlManager, font: Font, line: str, pos: tuple[int, int], left_limit: int = 100):
        self.gl_manager = gl_manager
        self.font = font
        self.line = line
        self.pos = pos

        self.max_vertical_advance = 0
        self.left_limit = left_limit
        self.pen = [0, 0]

        self.textures = {}
        self.program = self.gl_manager.shader_program.load('text_render')
        self.program['w_pos'].write(convert_vec2(pg.display.get_window_size(), self.pos))

        self.chars = []
        self.set_line(line)

    def set_line(self, line: str):
        for char in self.chars:
            char.release()
        self.chars = []

        self.line = line
        for char in line:
            glyph = self.font.get_glyph(ord(char))

            if char not in self.textures:
                self.textures[char] = self.gl_manager.ctx.texture(size=glyph.glyph_size, data=glyph.bitmap,
                                                                  components=1)

            self.chars.append(Char(self.gl_manager, glyph, self.program, self.textures[char]))

            if glyph.vertical_advance > self.max_vertical_advance:
                self.max_vertical_advance = glyph.vertical_advance

        self.update_vertices()

    def update_vertices(self):
        self.pen = [0, 0]

        for char in self.chars:
            if self.left_limit is not None and self.pen[0] + char.glyph.glyph_size[0] > self.left_limit:
                self.pen[1] += self.max_vertical_advance
                print(self.font.face.max_advance_height)
                self.pen[0] = 0

            pos = (self.pen[0] + char.glyph.offset[0],
                   self.pen[1] - char.glyph.offset[1] - char.glyph.glyph_size[1])

            char.update_vertices(pos)

            self.pen[0] += char.glyph.horizontal_advance

    def set_pos(self, pos: tuple[int, int]):
        self.pos = pos

    def draw(self, mode=mgl.TRIANGLE_STRIP):
        self.program['w_pos'].write(convert_vec2(pg.display.get_window_size(), self.pos))
        for char in self.chars:
            char.draw(mode)

    def release(self):
        self.program.release()

        for t in self.textures.values():
            t.release()

        for char in self.chars:
            char.release()
