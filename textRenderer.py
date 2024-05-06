import moderngl as mgl
import numpy as np
import freetype as ft
import glm

from glmanager import GlManager
from functions import get_gl_cords_for_rect


class Glyph:
    def __init__(self, code: int, face: ft.Face):
        face.load_char(chr(code))

        glyph = face.glyph
        self.bitmap = np.array(glyph.bitmap.buffer, dtype='u1')

        glyph_bbox = glyph.get_glyph().get_cbox(ft.FT_GLYPH_BBOX_MODES['FT_GLYPH_BBOX_PIXELS'])
        self.offset = (glyph_bbox.xMin, glyph_bbox.yMin)
        self.glyph_size = (glyph.bitmap.width, glyph.bitmap.rows)

        self.horizontal_advance = glyph.linearHoriAdvance // 2**16


class Char:
    def __init__(self, gl_manager: GlManager, glyph: Glyph):
        self.glyph = glyph

        self.gl_manager = gl_manager

        self.vertices = self.gl_manager.ctx.buffer(np.array([[0 for _ in range(2)] for _ in range(4)], dtype='float32'))
        self.uv = self.gl_manager.ctx.buffer(np.array(((0, 0), (0, 1), (1, 0), (1, 1)), dtype='float32'))
        self.color = self.gl_manager.ctx.buffer(glm.vec3((1, 1, 1)))

        self.texture = self.gl_manager.ctx.texture(size=self.glyph.glyph_size, data=self.glyph.bitmap, components=1)

        self.program = self.gl_manager.shader_program.load('text_render')

        self.vao = self.gl_manager.ctx.vertex_array(self.program,
                                                    [
                                                        (self.vertices, '2f /v', 'in_position'),
                                                        (self.uv, '2f /v', 'in_bitmap_cords'),
                                                        (self.color, '3f /i', 'in_color')
                                                    ])

    def draw(self, mode=mgl.TRIANGLE_STRIP):
        self.texture.use()
        self.vao.render(mode)

    def update_vertices(self, pos):
        self.vertices.write(get_gl_cords_for_rect(w_size=self.gl_manager.ctx.screen.size,
                                                  rect_size=self.glyph.glyph_size,
                                                  rect_pos=pos))

    def release(self):
        self.vertices.release()
        self.uv.release()
        self.color.release()

        self.program.release()
        self.texture.release()
        self.vao.release()


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


class Line:
    def __init__(self, gl_manager: GlManager, font: Font, line: str, pos: tuple):
        self.__gl_manager = gl_manager
        self.__font = font

        self.__line = line
        self.__pos = pos

        self.__chars = []
        self.set_line(self.__line)

    def update_vertices(self):
        x = list(self.__pos)
        for char in self.__chars:
            glyph = char.glyph

            char.update_vertices((x[0] + glyph.offset[0], x[1] - glyph.offset[1] - glyph.glyph_size[1]))

            x[0] += glyph.horizontal_advance

    def set_line(self, line: str):
        for char in self.__chars:
            char.release()

        self.__line = line
        self.__chars = []
        for char in line:
            self.__chars.append(Char(self.__gl_manager, self.__font.get_glyph(ord(char))))

        self.update_vertices()

    def set_pos(self, pos: tuple):
        self.__pos = pos
        self.update_vertices()

    def draw(self, mode=mgl.TRIANGLE_STRIP):
        for char in self.__chars:
            char.draw(mode)

    def release(self):
        for char in self.__chars:
            char.release()
