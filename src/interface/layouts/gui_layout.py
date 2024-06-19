from __future__ import annotations
from ..misc.types import Child

from abc import ABC, abstractmethod
import glm
import moderngl as mgl

from ..widgets.gui_object import GUIObject


class GUILayout(GUIObject, ABC):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self._mem_texture = self.ctx.texture(size=self.size, components=4)
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

        self._widgets = []

        self._needs_redraw = True
        self._needs_update = True

    def add(self, widget: Child):
        self._widgets.append(widget)

        self.update_request()

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def framebuffer(self):
        return self._framebuffer

    @GUIObject.size.setter
    def size(self, value: tuple[int, int]):
        GUIObject.size.fset(self, value)

        self._update_framebuffer()
        self.update_request()

    @GUIObject.pos.setter
    def pos(self, value: tuple[int, int]):
        GUIObject.pos.fset(self, value)

        self.update_request()

    # //////////////////////////////////////////////////// MOUSE ///////////////////////////////////////////////////////

    def mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:

        for widget in self._widgets:
            if widget.cords_in_rect(mouse_pos):
                if widget.mouse_down(button_name, mouse_pos, count) is not None:
                    return widget.mouse_down(button_name, mouse_pos, count)

        return super().mouse_down(button_name, mouse_pos, count)

    def mouse_up(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:

        for widget in self._widgets:
            if widget.cords_in_rect(mouse_pos):
                if widget.mouse_up(button_name, mouse_pos) is not None:
                    return widget.mouse_up(button_name, mouse_pos)

        return super().mouse_up(button_name, mouse_pos)

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def update_request(self):
        self._needs_update = True
        self.parent.redraw_request()

    def redraw_request(self):
        self._needs_redraw = True
        self.parent.redraw_request()

    def _update_framebuffer(self) -> None:
        self._mem_texture.release()
        self._mem_texture = self.ctx.texture(size=self.size, components=4)

        self._framebuffer.release()
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

    def update_layout(self):
        self._update_layout()

        self._needs_update = False

    @abstractmethod
    def _update_layout(self) -> None:
        ...

    def redraw(self):
        if self._needs_update:
            self.update_layout()

        self._framebuffer.use()
        self._framebuffer.clear()

        self._redraw()

        self._needs_redraw = False

    def _redraw(self):
        for widget in self._widgets:
            widget.draw()

    def draw(self):
        if self._needs_redraw or self._needs_update:
            self.redraw()

        self.parent.framebuffer.use()

        self._texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

        self._mem_texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

        if self._show_bbox:
            self._bbox_vao.program['w_size'].write(glm.vec2(self.size))
            self._bbox_vao.render(mgl.TRIANGLE_STRIP)

    def toggle_bbox(self, state=None):
        super().toggle_bbox(state)

        for widget in self._widgets:
            widget.toggle_bbox(self._show_bbox)

        self.redraw_request()

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def _release_widgets(self, keep_texture=False):
        for widget in self._widgets:
            widget.release(keep_texture)

        self._widgets = []

    def release(self, keep_texture=False):
        super().release(keep_texture)

        self._mem_texture.release()
        self._framebuffer.release()
        self._release_widgets(keep_texture)
