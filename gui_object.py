import moderngl as mgl
import numpy as np
import pygame as pg

from functions import load_program, get_rect_vertices


class GUIObject:
    def __init__(self, ctx: mgl.Context, size: tuple[int, int], pos: tuple[int, int]):
        self.ctx = ctx

        # MGL ATTRIBUTES
        self.texture = ctx.texture((1, 1), components=1)
        self.texture.filter = (mgl.NEAREST, mgl.NEAREST)
        self.framebuffer = self.ctx.framebuffer(self.texture)

        self.vertices = self.ctx.buffer(reserve=32)
        self.uv = self.ctx.buffer(np.array(((0, 0), (0, -1), (1, 0), (1, -1)), dtype='float32'))

        self.program = load_program(self.ctx, 'text_render')

        self.vao = self.ctx.vertex_array(self.program,
                                         [
                                             (self.vertices, '2f /v', 'in_position'),
                                             (self.uv, '2f /v', 'in_bitmap_cords'),
                                         ])

        # PROPERTIES
        self.size = size
        self.pos = pos

    def move(self, offset: tuple[int, int]) -> None:
        self.pos = tuple(int(self.pos[i] + offset[i]) for i in (0, 1))

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

    def contains_dot(self, cords: tuple[int, int]) -> bool:
        return all(0 < cords[i] - self.pos[i] < self.size[i] for i in (0, 1))

    def draw(self, mode=mgl.TRIANGLE_STRIP) -> None:
        self.texture.use()
        self.vao.render(mode)


class Widget(GUIObject):
    def __init__(self, ctx: mgl.Context, size: tuple[int, int], pos: tuple[int, int]):
        super().__init__(ctx=ctx, size=size, pos=pos)


class Layout(GUIObject):
    def __init__(self, ctx: mgl.Context, size: tuple[int, int], pos: tuple[int, int], rotation='vertical'):
        super().__init__(ctx=ctx, size=size, pos=pos)
        self.rotation = rotation

        self.widgets = []

    def calculate_shapes(self):
        ...

    def add_widget(self, widget: Widget):
        ...

    def draw(self, mode=mgl.TRIANGLE_STRIP):
        for widget in self.widgets:
            widget.draw(mode)

        self.vao.render(mode)

