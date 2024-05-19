import moderngl as mgl
import numpy as np
import pygame as pg

from functions import load_program, get_rect_vertices


class GUIObject:
    def __init__(self, ctx: mgl.Context, size: tuple[int, int], pos: tuple[int, int]):
        self._ctx = ctx

        # MGL ATTRIBUTES
        self._texture = ctx.texture((1, 1), components=1)
        self._texture.filter = (mgl.NEAREST, mgl.NEAREST)
        self._framebuffer = self.ctx.framebuffer(self._texture)

        self._vertices = self.ctx.buffer(reserve=32)
        self._uv = self.ctx.buffer(np.array(((0, 0), (0, -1), (1, 0), (1, -1)), dtype='float32'))

        self._program = load_program(self.ctx, 'textured_box')

        self._vao = self.ctx.vertex_array(self._program,
                                          [
                                             (self._vertices, '2f /v', 'in_position'),
                                             (self._uv, '2f /v', 'in_bitmap_cords'),
                                         ])

        # FORM
        self._size = size
        self._pos = pos
        self._vertices.write(get_rect_vertices(pg.display.get_window_size(), self.size, self.pos))

    @property
    def ctx(self):
        return self._ctx

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos: tuple[int, int]):
        self._pos = pos

        self._vertices.write(get_rect_vertices(pg.display.get_window_size(), self.size, self.pos))

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: tuple[int, int]):
        self._size = size

        self._vertices.write(get_rect_vertices(pg.display.get_window_size(), self.size, self.pos))

        self._update_framebuffer()

    def _update_framebuffer(self):
        self._texture.release()
        self._texture = self.ctx.texture(size=self.size, components=4, data=None)

        self._framebuffer.release()
        self._framebuffer = self.ctx.framebuffer(self._texture)

    def contains_dot(self, cords: tuple[int, int]) -> bool:
        return all(0 < cords[i] - self.pos[i] < self.size[i] for i in (0, 1))

    def move(self, offset: tuple[int, int]) -> None:
        self.pos = tuple(int(self.pos[i] + offset[i]) for i in (0, 1))

    def _redraw(self):
        pass

    def draw(self, mode=mgl.TRIANGLE_STRIP) -> None:
        self._texture.use()
        self._vao.render(mode)

    def release(self):
        pass


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

        self._vao.render(mode)

