import moderngl as mgl
import numpy as np
import pygame as pg

from ..functions import load_program, get_rect_vertices


class GUIObject:
    def __init__(self,
                 ctx: mgl.Context,
                 size: tuple[int, int],
                 pos: tuple[int, int],
                 texture: mgl.Texture,
                 program: mgl.Program):
        self._ctx = ctx

        # MGL ATTRIBUTES
        self._texture = texture

        self._vertices = self.ctx.buffer(reserve=32)
        self._uv = self.ctx.buffer(np.array(((0, 0), (0, 1), (1, 0), (1, 1)), dtype='float32'))

        self._program = program

        self._vao = self.ctx.vertex_array(self._program,
                                          [
                                              (self._vertices, '2f /v', 'in_position'),
                                              (self._uv, '2f /v', 'in_texture_cords'),
                                          ])

        # FORM
        self._size = size
        self._pos = pos
        self.update_vertices()

    @property
    def ctx(self):
        return self._ctx

    @property
    def texture(self):
        return self._texture

    @property
    def program(self):
        return self._program

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos: tuple[int, int]):
        self._pos = pos

        self.update_vertices()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: tuple[int, int]):
        self._size = size

        self.update_vertices()

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    def update_vertices(self):
        self._vertices.write(get_rect_vertices(fb_size=self.ctx.fbo.viewport[2:],
                                               rect_size=self.size,
                                               rect_pos=self.pos))

    def cords_in_rect(self, cords):
        return all(0 < cords[i] - self.pos[i] < self.size[i] for i in (0, 1))

    def move(self, movement):
        self.pos = tuple(self.pos[i] + movement[i] for i in (0, 1))

    def mouse_down(self, button_name, mouse_pos):
        pass

    def mouse_up(self, button_name, mouse_pos):
        pass

    def mouse_double(self, button_name, mouse_pos):
        pass

    def draw(self) -> None:
        self._texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

    def release(self):
        self._vertices.release()
        self._uv.release()

        self._vao.release()


class GUILayout(GUIObject):
    def __init__(self, ctx: mgl.Context,
                 size: tuple[int, int],
                 pos: tuple[int, int],
                 texture: mgl.Texture,
                 program: mgl.Program):
        super().__init__(ctx=ctx, size=size, pos=pos, texture=texture, program=program)

        self._background = GUIObject(self.ctx, self.size, (0, 0), self.texture, self.program)

        self._mem_texture = self.ctx.texture(size=self.size, components=4)
        self._framebuffer = ctx.framebuffer(self._mem_texture)

        self.widgets = []

    def update_framebuffer(self):
        self._mem_texture.release()
        self._mem_texture = self.ctx.texture(size=self.size, components=4)

        self._framebuffer.release()
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

    def update_layout(self):
        pass

    def _redraw(self):
        self._framebuffer.use()
        self._framebuffer.clear()

        self._background.draw()

        for widget in self.widgets:
            widget.draw()

        self.ctx.screen.use()

    def draw(self):
        self._mem_texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

    def _release_widgets(self):
        for widget in self.widgets:
            widget.release()

        self.widgets = []

    def release(self):
        super().release()

        self._mem_texture.release()
        self._framebuffer.release()

        self._background.release()
        self._release_widgets()
