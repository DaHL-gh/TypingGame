from __future__ import annotations

import numpy as np
import moderngl as mgl
from structlinks.LinkedList import LinkedList

from .mglmanagers import ProgramManager, TextureManager, BufferManager
from .text_render import TextField, Font
from .types import Child, Parent


class GUI:
    def __init__(self, window):
        self.window = window
        self._size = window.size

        # MGL ATTRIBUTES

        self._ctx = window.ctx

        BufferManager(self.ctx).create_buffer('UV', np.array(((0, 0), (0, 1), (1, 0), (1, 1)), dtype='float32'))

        self._vertices = self.ctx.buffer(np.array(((-1, -1), (-1, 1), (1, -1), (1, 1)), dtype='float32'))
        self._vao = self.ctx.vertex_array(ProgramManager(window.ctx).get_program('textured_box_reversed'),
                                          [
                                              (self._vertices, '2f /v', 'in_position'),
                                              (BufferManager(self.ctx).get_buffer('UV'), '2f /v', 'in_texture_cords')
                                          ])

        self._mem_texture = self.ctx.texture(size=self.size, components=4)
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

        # WIDGETS
        self.widgets: LinkedList[Child] = LinkedList()

        self.font = Font(name='WillowHead', char_size=100)

        self.frame_counter = TextField(self.ctx, (500, 300), 'tehgfhjhghjhfgjkfxt', self.font,
                                       ProgramManager(self.ctx).get_program('textured_box'),
                                       TextureManager(self.ctx).get_texture('Chopper.jpg'))
        self.widgets.append(self.frame_counter)

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def ctx(self):
        return self._ctx

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        self._size = value

        self._update_framebuffer()
        self._update_layout()
        self._redraw()

    @property
    def width(self):
        return self._size[0]

    @property
    def height(self):
        return self._size[1]

    # //////////////////////////////////////////////////// MOUSE ///////////////////////////////////////////////////////

    def mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                return widget.mouse_down(button_name, mouse_pos, count)

    def mouse_up(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                return widget.mouse_up(button_name, mouse_pos)

    def mouse_drag(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                return widget.mouse_drag(button_name, mouse_pos, rel)

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def _update_layout(self) -> None:
        self._framebuffer.use()

        for widget in self.widgets:
            widget.pos = widget.pos

    def _update_framebuffer(self) -> None:
        self._mem_texture.release()
        self._mem_texture = self.ctx.texture(size=self.size, components=4)

        self._framebuffer.release()
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

    def _redraw(self) -> None:
        self._framebuffer.use()
        self._framebuffer.clear()

        for widget in self.widgets:
            widget.draw()

        self.ctx.screen.use()

    def draw(self) -> None:
        self._mem_texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def _release_widgets(self) -> None:
        for widget in self.widgets:
            widget.release()

        self.widgets = LinkedList()

    def release(self) -> None:
        self._vertices.release()

        self._vao.release()

        self._mem_texture.release()
        self._framebuffer.release()
        self._release_widgets()
