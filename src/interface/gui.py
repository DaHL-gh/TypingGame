from __future__ import annotations
from .types import Child, Parent

import numpy as np
import moderngl as mgl

from .mglmanagers import ProgramManager, TextureManager, BufferManager
from .slider import Slider
from .text_render import TextField, Font
from .linelayout import LineLayout
from .ll import LinkedList


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
        self._widgets: LinkedList[Child] = LinkedList()

        self.font = Font(name='CascadiaMono', char_size=20)

        ll = LineLayout(parent=self, orientation='horizontal', size=(200, 200), texture=TextureManager(self.ctx).get_texture('chopper.jpg'))
        ll2 = LineLayout(parent=ll, orientation='horizontal', texture=TextureManager(self.ctx).get_texture('chopper.jpg'))

        TextField(parent=ll, font=self.font)
        Slider(parent=ll2, size=(None, 80), orientation='vertical', slider_width=50)
        Slider(parent=ll2, size=(None, 40))
        Slider(parent=ll2, size=(None, 40))

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def ctx(self):
        return self._ctx

    @property
    def framebuffer(self):
        return self._framebuffer

    def show_bbox(self):
        return self._show_bbox

    @property
    def window_pos(self):
        return 0, 0

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
        for widget in self._widgets:
            if widget.cords_in_rect(mouse_pos):
                return widget.mouse_down(button_name, mouse_pos, count)

    def mouse_up(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        for widget in self._widgets:
            if widget.cords_in_rect(mouse_pos):
                return widget.mouse_up(button_name, mouse_pos)

    def mouse_drag(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        for widget in self._widgets:
            if widget.cords_in_rect(mouse_pos):
                return widget.mouse_drag(button_name, mouse_pos, rel)

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def add(self, widget: Child):
        self._widgets.append(widget)

    def _update_layout(self) -> None:
        self._framebuffer.use()

        for widget in self._widgets:
            widget.size = widget.size

    def _update_framebuffer(self) -> None:
        self._mem_texture.release()
        self._mem_texture = self.ctx.texture(size=self.size, components=4)

        self._framebuffer.release()
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def redraw(self) -> None:
        self._framebuffer.use()
        self._framebuffer.clear()

        for widget in self._widgets:
            widget.draw()

    def draw(self) -> None:
        self.ctx.screen.use()

        self._mem_texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

    def toggle_bbox(self, state=None):
        if state is not None:
            self._show_bbox = state
        else:
            self._show_bbox = not self._show_bbox

        for widget in self._widgets:
            widget.toggle_bbox(self._show_bbox)

        self.redraw()

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def _release_widgets(self) -> None:
        for widget in self._widgets:
            widget.release()

        self._widgets = LinkedList()

    def release(self) -> None:
        self._vertices.release()

        self._vao.release()

        self._mem_texture.release()
        self._framebuffer.release()
        self._release_widgets()
