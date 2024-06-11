import glm
import moderngl as mgl
import numpy as np
import pygame as pg
from structlinks.LinkedList import LinkedList

from .mglmanagers import ProgramManager
from ..functions import get_rect_vertices

from abc import ABC, abstractmethod


class GUIObject:
    def __init__(self,
                 ctx: mgl.Context,
                 size: tuple[int, int],
                 pos: tuple[int, int],
                 program: mgl.Program,
                 texture: mgl.Texture | None = None):

        if texture is None:
            texture = ctx.texture(size=size, components=1)

        self._ctx = ctx

        # MGL ATTRIBUTES
        self._texture = texture

        self._vertices = self.ctx.buffer(reserve=32)
        self._uv = self.ctx.buffer(np.array(((0, 0), (0, 1), (1, 0), (1, 1)), dtype='float32'))

        self._program = program

        self._get_vao()

        self._bbox_vao = self.ctx.vertex_array(ProgramManager(self.ctx).get_program('bbox_outline'),
                                          [
                                              (self._vertices, '2f /v', 'in_position'),
                                              (self._uv, '2f /v', 'in_texture_cords')
                                          ])

        # FORM
        self._size = size
        self._pos = pos
        self.update_vertices()

    def _get_vao(self):
        self._vao = self.ctx.vertex_array(self._program,
                                          [
                                              (self._vertices, '2f /v', 'in_position'),
                                              (self._uv, '2f /v', 'in_texture_cords')
                                          ])

# /////////////////////////////////////////////////////PROPERTIES///////////////////////////////////////////////////////

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
    def pos(self, value: tuple[int, int]):
        self._pos = value

        self.update_vertices()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        self._size = value

        self.update_vertices()

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

# ////////////////////////////////////////////////////// SMTNG /////////////////////////////////////////////////////////

    def update_vertices(self):
        self._vertices.write(get_rect_vertices(fb_size=self.ctx.fbo.viewport[2:],
                                               rect_size=self.size,
                                               rect_pos=self.pos))

    def cords_in_rect(self, cords):
        return all(0 < cords[i] - self.pos[i] < self.size[i] for i in (0, 1))

    def move(self, movement):
        self.pos = tuple(self.pos[i] + movement[i] for i in (0, 1))

# ////////////////////////////////////////////////////// MOUSE /////////////////////////////////////////////////////////

    def mouse_down(self, button_name, mouse_pos, count) -> bool:
        return False

    def mouse_up(self, button_name, mouse_pos) -> bool:
        return False

    def mouse_drag(self, button_name, mouse_pos, rel):
        return False

# ///////////////////////////////////////////////////// DISPLAY ////////////////////////////////////////////////////////

    def draw(self) -> None:
        self._texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

        self._bbox_vao.program['w_size'].write(glm.vec2(self.size))
        self._bbox_vao.render(mgl.TRIANGLE_STRIP)

# ///////////////////////////////////////////////////// RELEASE ////////////////////////////////////////////////////////

    def release(self):
        self._vertices.release()
        self._uv.release()

        self._vao.release()


class GUILayout(GUIObject, ABC):
    def __init__(self, ctx: mgl.Context,
                 size: tuple[int, int],
                 pos: tuple[int, int],
                 program: mgl.Program,
                 texture: mgl.Texture | None = None):
        super().__init__(ctx=ctx, size=size, pos=pos, program=program, texture=texture)

        self._mem_texture = self.ctx.texture(size=self.size, components=4)
        self._framebuffer = ctx.framebuffer(self._mem_texture)

        self.widgets = LinkedList()

    def update_framebuffer(self):
        self._mem_texture.release()
        self._mem_texture = self.ctx.texture(size=self.size, components=4)

        self._framebuffer.release()
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

    @abstractmethod
    def update_layout(self):
        pass

    @GUIObject.size.setter
    def size(self, value: tuple[int, int]):

        GUIObject.size.fset(self, value)

        self.update_framebuffer()
        self.update_layout()
        self._redraw()

# ////////////////////////////////////////////////////// MOUSE /////////////////////////////////////////////////////////

    def mouse_down(self, button_name, mouse_pos, count) -> bool:
        mouse_pos = tuple(mouse_pos[i] - self.pos[i] for i in (0, 1))

        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                if widget.mouse_down(button_name, mouse_pos, count):
                    return True

        return False

    def mouse_up(self, button_name, mouse_pos) -> bool:
        mouse_pos = tuple(mouse_pos[i] - self.pos[i] for i in (0, 1))

        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                if widget.mouse_up(button_name, mouse_pos):
                    return True

        return False

    def mouse_drag(self, button_name, mouse_pos, rel):
        mouse_pos = tuple(mouse_pos[i] - self.pos[i] for i in (0, 1))

        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                if widget.mouse_drag(button_name, mouse_pos, rel):
                    return True

        return False

# ///////////////////////////////////////////////////// DISPLAY ////////////////////////////////////////////////////////

    def _redraw(self):
        self._framebuffer.use()
        self._framebuffer.clear()

        for widget in self.widgets:
            widget.draw()

        self.ctx.screen.use()

    def draw(self):
        super().draw()

        self._mem_texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

# ///////////////////////////////////////////////////// RELEASE ////////////////////////////////////////////////////////

    def _release_widgets(self):
        for widget in self.widgets:
            widget.release()

        self.widgets = []

    def release(self):
        super().release()

        self._mem_texture.release()
        self._framebuffer.release()
        self._release_widgets()
