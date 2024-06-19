from __future__ import annotations
from ..misc.types import Child

import numpy as np
import moderngl as mgl

from ..misc.mglmanagers import ProgramManager, BufferManager


class Root:
    def __init__(self, ctx):
        self._size = (1, 1)

        # MGL ATTRIBUTES
        self._ctx = ctx

        BufferManager(self.ctx).create('UV', np.array(((0, 0), (0, 1), (1, 0), (1, 1)), dtype='float32'))

        self._vertices = self.ctx.buffer(np.array(((-1, 1), (-1, -1), (1, 1), (1, -1)), dtype='float32'))
        self._vao = self.ctx.vertex_array(ProgramManager(self.ctx).get('textured_box'),
                                          [
                                              (self._vertices, '2f /v', 'in_position'),
                                              (BufferManager(self.ctx).get('UV'), '2f /v', 'in_texture_cords')
                                          ])

        self._mem_texture = self.ctx.texture(size=self.size, components=4)
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

        # DEBUG
        self._show_bbox = True

        self._needs_redraw = True
        self._needs_update = True

        # WIDGET
        self._widget: Child | None = None

    # //////////////////////////////////////////////////// WIDGETS /////////////////////////////////////////////////////

    def add(self, widget: Child) -> None:
        if self._widget is not None:
            self._widget.release()

        self._widget = widget
        self.update_request()

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def ctx(self) -> mgl.Context:
        return self._ctx

    @property
    def framebuffer(self) -> mgl.Framebuffer:
        return self._framebuffer

    @property
    def show_bbox(self) -> bool:
        return self._show_bbox

    @property
    def window_pos(self) -> tuple[int, int]:
        return 0, 0

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        self._size = value

        self._update_framebuffer()

        self.update_layout()

    @property
    def width(self) -> int:
        return self._size[0]

    @property
    def height(self) -> int:
        return self._size[1]

    # //////////////////////////////////////////////////// MOUSE ///////////////////////////////////////////////////////

    def mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        if self._widget is not None:
            return self._widget.mouse_down(button_name, mouse_pos, count)

    def mouse_up(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        if self._widget is not None:
            return self._widget.mouse_up(button_name, mouse_pos)

    def mouse_drag(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        if self._widget is not None:
            return self._widget.mouse_drag(button_name, mouse_pos, rel)

    # /////////////////////////////////////////////////// UPDATE ///////////////////////////////////////////////////////

    def update_layout(self) -> None:
        if self._widget is None:
            return

        self._widget.pos = (0, 0)
        self._widget.size = self.size

        self._needs_update = False

    def _update_framebuffer(self) -> None:
        self._mem_texture.release()
        self._mem_texture = self.ctx.texture(size=self.size, components=4)

        self._framebuffer.release()
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

    def update_request(self) -> None:
        self._needs_update = True
        self.redraw_request()

    def redraw_request(self) -> None:
        self._needs_redraw = True

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def redraw(self) -> None:
        if self._needs_update:
            self.update_layout()

        self._framebuffer.use()
        self._framebuffer.clear()

        self._widget.draw()

        self._needs_redraw = False

    def draw(self) -> None:
        if self._widget is None:
            return

        if self._needs_redraw or self._needs_update:
            self.redraw()

        self.ctx.screen.use()
        self._mem_texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

    def toggle_bbox(self, state=None) -> None:
        if state is not None:
            self._show_bbox = state
        else:
            self._show_bbox = not self._show_bbox

        if self._widget is None:
            return

        self._widget.toggle_bbox(self._show_bbox)

        self.redraw_request()

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def release(self) -> None:
        self._vertices.release()

        self._vao.release()

        self._mem_texture.release()
        self._framebuffer.release()

        self._widget.release()
        self._widget = None
