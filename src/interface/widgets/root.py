from __future__ import annotations
from ..misc.types import Child

from abc import abstractmethod, ABC
import numpy as np
import moderngl as mgl

from ..gui import GUI
from ..misc.mglmanagers import ProgramManager, BufferManager


class Root(ABC):
    def __init__(self, ctx, id):
        self._id = id
        self._size = (1, 1)

        # MGL ATTRIBUTES
        self._ctx = ctx

        self._vertices = self.ctx.buffer(np.array(((-1, 1), (-1, -1), (1, 1), (1, -1)), dtype='float32'))
        self._vao = self.ctx.vertex_array(ProgramManager(self.ctx).get('textured_box'),
                                          [
                                              (self._vertices, '2f /v', 'in_position'),
                                              (BufferManager(self.ctx).get('UV'), '2f /v', 'in_texture_cords')
                                          ])

        self._mem_texture = self.ctx.texture(size=self.size, components=4)
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

        # DEBUG
        self._show_bbox = False

        self._needs_redraw = True
        self._needs_update = True

        # WIDGET
        self._widget: Child | None = None

        self.gui = GUI(ctx)
        self.gui.add(self)

    # //////////////////////////////////////////////////// WIDGETS /////////////////////////////////////////////////////

    def add(self, widget: Child) -> None:
        if self._widget is not None:
            self._widget.release()

        self._widget = widget
        self.update_request()

    def use(self):
        self.size = self.gui.size
        self.gui.set_root(self.id)

    @abstractmethod
    def build(self) -> None:
        pass

    def __getattr__(self, item):
        return getattr(self._widget, item)

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def ctx(self) -> mgl.Context:
        return self._ctx

    @property
    def id(self):
        return self._id

    @property
    def root(self):
        return self

    @property
    def framebuffer(self) -> mgl.Framebuffer:
        return self._framebuffer

    @property
    def widget(self):
        return self._widget

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

        self.update_request()

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

    def update_layout(self):
        if self._widget is None:
            return

        if self._needs_update:
            self._widget.pos = (0, 0)
            self._widget.size = self.size

            self._needs_update = False

    def _update_framebuffer(self) -> None:
        self._mem_texture.release()
        self._mem_texture = self.ctx.texture(size=self.size, components=4)
        self._mem_texture.filter = (mgl.NEAREST, mgl.NEAREST)

        self._framebuffer.release()
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

    def update_request(self) -> None:
        if not self._needs_update:
            self._needs_update = True
            self.redraw_request()

    def redraw_request(self) -> None:
        if not self._needs_redraw:
            self._needs_redraw = True

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def redraw(self) -> None:
        if self._needs_redraw:
            self._framebuffer.use()
            self._framebuffer.clear()

            self._widget.draw()

            self._needs_redraw = False

    def draw(self) -> None:
        if self._widget is None:
            return

        self.update_layout()
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
