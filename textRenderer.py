import freetype as ft
import numpy as np
import moderngl as mgl


class Font:
    def __init__(self, ctx: mgl.Context, name: str, char_size: int):
        self.ctx = ctx
        self.name = name
        self.char_size = char_size

        self.face = ft.Face(f'fonts/{name}.ttf')
        w = h = char_size << 6
        self.face.set_char_size(width=w, height=h, hres=95, vres=95)

        self.loaded_chars = {}

    def get_char(self, code: int):
        if code not in self.loaded_chars:
            self.loaded_chars[code] = Char(self.ctx, code, self.face)

        return self.loaded_chars[code]


class Char:
    def __init__(self, ctx: mgl.Context, code: int, face: ft.Face):
        face.load_char(chr(code))

        glyph = face.glyph
        self.bitmap = np.array(glyph.bitmap.buffer, dtype='u1')

        glyph_bbox = glyph.get_glyph().get_cbox(ft.FT_GLYPH_BBOX_MODES['FT_GLYPH_BBOX_PIXELS'])
        self.bbox_size = (glyph_bbox.xMax - glyph_bbox.xMin, glyph_bbox.yMax - glyph_bbox.yMin)
        self.glyph_size = (glyph.bitmap.width, glyph.bitmap.rows)

        self.texture = ctx.texture(size=self.glyph_size, data=self.bitmap, components=1)


class Renderer:
    def __init__(self, ctx: mgl.Context, font_name: str):
        self.font = Font(ctx, font_name, 50)
        self.target_ctx = ctx

    def render_at(self, line: str, pos):
        for char in line:
            glyph = self.font.get_char(ord(char))
