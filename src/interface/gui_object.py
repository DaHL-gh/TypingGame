from __future__ import annotations
from .types import Child, Parent

import glm
import moderngl as mgl
from structlinks.LinkedList import LinkedList
from abc import ABC, abstractmethod

from .mglmanagers import ProgramManager, BufferManager
from ..functions import get_rect_vertices


class GUIObject:
    def __init__(self,
                 parent: Parent,
                 size: tuple[int, int],
                 pos: tuple[int, int],
                 program: mgl.Program,
                 texture: mgl.Texture | None = None):

        self.parent = parent
        self._ctx = parent.ctx

        # MGL ATTRIBUTES
        if texture is None:
            texture = self.ctx.texture(size=size, components=1)
        self._texture = texture

        self._vertices = self.ctx.buffer(reserve=32)

        self._program = program

        self._get_vao()
        self._bbox_vao = self.ctx.vertex_array(ProgramManager(self.ctx).get_program('bbox_outline'),
                                               [
                                                   (self._vertices, '2f /v', 'in_position'),
                                                   (BufferManager(self.ctx).get_buffer('UV'), '2f /v',
                                                    'in_texture_cords')
                                               ])

        # FORM
        self._size = size
        self._pos = pos
        self.update_vertices()

        self._show_bbox = False

    def _get_vao(self):
        self._vao = self.ctx.vertex_array(self._program,
                                          [
                                              (self._vertices, '2f /v', 'in_position'),
                                              (BufferManager(self.ctx).get_buffer('UV'), '2f /v', 'in_texture_cords')
                                          ])

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

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

    # //////////////////////////////////////////////////// SMTNG ///////////////////////////////////////////////////////

    def update_vertices(self):
        self._vertices.write(get_rect_vertices(fb_size=self.ctx.fbo.viewport[2:],
                                               rect_size=self.size,
                                               rect_pos=self.pos))

    def cords_in_rect(self, cords):
        return all(0 < cords[i] - self.pos[i] < self.size[i] for i in (0, 1))

    def move(self, movement):
        self.pos = tuple(self.pos[i] + movement[i] for i in (0, 1))

    # //////////////////////////////////////////////////// MOUSE ///////////////////////////////////////////////////////

    def mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return self._mouse_down_func(button_name, mouse_pos, count)

    def _mouse_down_func(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return None

    def mouse_up(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        return self._mouse_up_func(button_name, mouse_pos)

    def _mouse_up_func(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        return None

    def mouse_drag(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        return self._mouse_drag_func(button_name, mouse_pos, rel)

    def _mouse_drag_func(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        return None

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def draw(self) -> None:
        self._texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

        if self._show_bbox:
            self._bbox_vao.program['w_size'].write(glm.vec2(self.size))
            self._bbox_vao.render(mgl.TRIANGLE_STRIP)

    def toggle_bbox(self, state=None):
        if state is not None:
            self._show_bbox = state
        else:
            self._show_bbox = not self._show_bbox

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def release(self, keep_texture=False):
        self._vertices.release()

        if not keep_texture:
            self._texture.release()

        self._vao.release()


class GUILayout(GUIObject, ABC):
    def __init__(self,
                 parent: Parent,
                 size: tuple[int, int],
                 pos: tuple[int, int],
                 program: mgl.Program,
                 texture: mgl.Texture | None = None):
        super().__init__(parent=parent, size=size, pos=pos, program=program, texture=texture)

        self._mem_texture = self.ctx.texture(size=self.size, components=4)
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

        self.widgets: LinkedList[Child] = LinkedList()

    def update_framebuffer(self) -> None:
        self._mem_texture.release()
        self._mem_texture = self.ctx.texture(size=self.size, components=4)

        self._framebuffer.release()
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

    @abstractmethod
    def _update_layout(self) -> None:
        pass

    @GUIObject.size.setter
    def size(self, value: tuple[int, int]):

        GUIObject.size.fset(self, value)

        self.update_framebuffer()
        self._update_layout()
        self._redraw()

    # //////////////////////////////////////////////////// MOUSE ///////////////////////////////////////////////////////

    def mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        mouse_pos = tuple(mouse_pos[i] - self.pos[i] for i in (0, 1))

        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                if widget.mouse_down(button_name, mouse_pos, count) is not None:
                    return widget

        return self._mouse_down_func(button_name, mouse_pos, count)

    def mouse_up(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        mouse_pos = tuple(mouse_pos[i] - self.pos[i] for i in (0, 1))

        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                if widget.mouse_up(button_name, mouse_pos) is not None:
                    return widget

        return self._mouse_up_func(button_name, mouse_pos)

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

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

    def toggle_bbox(self, state=None):
        super().toggle_bbox(state)

        for widget in self.widgets:
            widget.toggle_bbox(self._show_bbox)

        self._redraw()

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def _release_widgets(self, keep_texture=False):
        for widget in self.widgets:
            widget.release(keep_texture)

        self.widgets = LinkedList()

    def release(self, keep_texture=False):
        super().release(keep_texture)

        self._mem_texture.release()
        self._framebuffer.release()
        self._release_widgets(keep_texture)
