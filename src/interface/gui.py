from __future__ import annotations
from .types import Child, Parent

import numpy as np
import moderngl as mgl
from structlinks.LinkedList import LinkedList

from .mglmanagers import ProgramManager, TextureManager, BufferManager
from .slider import Slider
from .text_render import TextField, Font
from .layout import LineLayout


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

        # DEBUG
        self._show_bbox = False

        # WIDGETS
        self.widgets: LinkedList[Child] = LinkedList()

        self.font = Font(name='Bitter-VariableFont_wght', char_size=50)

        ll = LineLayout(self, 'vertical', size=(200, 200), padding=20, spacing=50, texture=TextureManager(self.ctx).get_texture('chopper.jpg'))

        f1 = TextField(ll, line='', font=self.font, size=(20, 10), texture=TextureManager(self.ctx).get_texture('chopper.jpg'))
        f2 = TextField(ll, line='', font=self.font, size=(10, 10), texture=TextureManager(self.ctx).get_texture('chopper.jpg'))
        f3 = TextField(ll, line='', font=self.font, size=(10, 10), texture=TextureManager(self.ctx).get_texture('chopper.jpg'))

        s1 = Slider(ll, size=(200, 40))
        s2 = Slider(ll, size=(200, 40))
        s3 = Slider(ll, size=(200, 40))

        ll.add(s1, s2, s3)

        self.widgets.append(ll)

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def ctx(self):
        return self._ctx

    @property
    def framebuffer(self):
        return self._framebuffer

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        self._size = value

        self._update_framebuffer()
        self._update_layout()
        self.redraw()

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

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def redraw(self) -> None:
        self._framebuffer.use()
        self._framebuffer.clear()

        for widget in self.widgets:
            widget.draw()

        self.ctx.screen.use()

    def draw(self) -> None:
        self.ctx.screen.use()

        self._mem_texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

    def toggle_bbox(self, state=None):
        if state is not None:
            self._show_bbox = state
        else:
            self._show_bbox = not self._show_bbox

        for widget in self.widgets:
            widget.toggle_bbox(self._show_bbox)

        self.redraw()

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
