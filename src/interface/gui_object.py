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
                 size: tuple[int | None, int | None] = (None, None),
                 min_size: tuple[int | None, int | None] = (None, None),
                 size_hint: tuple[float | None, float | None] = (None, None),
                 pos: tuple[int, int] = (0, 0),
                 program: mgl.Program | None = None,
                 texture: mgl.Texture | None = None):

        self.parent = parent

        # FORM
        self._size = tuple(int(size[i]) if size[i] is not None else 1 for i in (0, 1))
        self._min_size = tuple(max(int(min_size[i]), self._size[i]) if min_size[i] is not None else 1 for i in (0, 1))
        self._base_size = size
        self._size_hint = size_hint

        self._pos = pos

        # MGL ATTRIBUTES
        if texture is None:
            texture = self.ctx.texture(size=self.size, components=1)
        self._texture = texture

        self._vertices = self.ctx.buffer(reserve=32)
        if program is None:
            program = ProgramManager(self.ctx).get_program('textured_box')
        self._program = program

        self._get_vao()
        self._bbox_vao = self.ctx.vertex_array(ProgramManager(self.ctx).get_program('bbox_outline'),
                                               [
                                                   (self._vertices, '2f /v', 'in_position'),
                                                   (BufferManager(self.ctx).get_buffer('UV'), '2f /v',
                                                    'in_texture_cords')
                                               ])

        self._update_vertices()

        self.show_bbox = self.parent.show_bbox

        self.parent.add(self)

    def _get_vao(self):
        self._vao = self.ctx.vertex_array(self._program,
                                          [
                                              (self._vertices, '2f /v', 'in_position'),
                                              (BufferManager(self.ctx).get_buffer('UV'), '2f /v', 'in_texture_cords')
                                          ])

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def ctx(self):
        return self.parent.ctx

    @property
    def texture(self):
        return self._texture

    @property
    def program(self):
        return self._program

    @property
    def show_bbox(self):
        return self._show_bbox

    @show_bbox.setter
    def show_bbox(self, value: bool):
        self._show_bbox = value

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value: tuple[int, int]):
        self._pos = value

        self._update_vertices()

    @property
    def window_pos(self):
        return self.parent.window_pos[0] + self._pos[0], self.parent.window_pos[1] + self._pos[1]

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        self._size = (max(self._min_size[0], value[0]), max(self._min_size[1], value[1]))

        self._update_vertices()

    @property
    def width(self):
        return self._size[0]

    @width.setter
    def width(self, value: int):
        self.size = (max(self.min_width, value), self.height)

    @property
    def height(self):
        return self._size[1]

    @height.setter
    def height(self, value: int):
        self.size = (self.width, max(self.min_height, value))

    @property
    def size_hint(self):
        return self._size_hint

    @property
    def width_hint(self):
        return self.size_hint[0]

    @property
    def height_hint(self):
        return self.size_hint[1]

    @property
    def base_size(self):
        return self._base_size

    @property
    def base_width(self):
        return self._base_size[0]

    @property
    def base_height(self):
        return self._base_size[1]

    @property
    def min_size(self):
        return self._min_size

    @property
    def min_width(self):
        return self._min_size[0]

    @property
    def min_height(self):
        return self._min_size[1]

    # //////////////////////////////////////////////////// SMTNG ///////////////////////////////////////////////////////

    def _update_vertices(self):
        self.parent.framebuffer.use()
        self._vertices.write(get_rect_vertices(fb_size=self.ctx.fbo.viewport[2:],
                                               rect_size=self.size,
                                               rect_pos=self.pos))

    def cords_in_rect(self, cords):
        return all(0 < cords[i] - self.window_pos[i] < self.size[i] for i in (0, 1))

    def move(self, move):
        self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])

    # //////////////////////////////////////////////////// MOUSE ///////////////////////////////////////////////////////

    def mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        mouse_pos = (mouse_pos[0] - self.window_pos[0], mouse_pos[1] - self.window_pos[1])
        return self._mouse_down_func(button_name, mouse_pos, count)

    def _mouse_down_func(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return None

    def mouse_up(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        mouse_pos = (mouse_pos[0] - self.window_pos[0], mouse_pos[1] - self.window_pos[1])
        return self._mouse_up_func(button_name, mouse_pos)

    def _mouse_up_func(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        return None

    def mouse_drag(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        mouse_pos = (mouse_pos[0] - self.window_pos[0], mouse_pos[1] - self.window_pos[1])
        return self._mouse_drag_func(button_name, mouse_pos, rel)

    def _mouse_drag_func(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        return None

    def keyboard_press(self, key: int, unicode: str):
        return  self._keyboard_press(key, unicode)

    def _keyboard_press(self, key: int, unicode: str):
        return  None

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
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self._mem_texture = self.ctx.texture(size=self.size, components=4)
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

        self._widgets: list[Child] = []

    def _update_framebuffer(self) -> None:
        self._mem_texture.release()
        self._mem_texture = self.ctx.texture(size=self.size, components=4)

        self._framebuffer.release()
        self._framebuffer = self.ctx.framebuffer(self._mem_texture)

    @abstractmethod
    def _update_layout(self) -> None:
        pass

    def add(self, widget: Child):
        self._widgets.append(widget)

    @property
    def framebuffer(self):
        return self._framebuffer

    @GUIObject.size.setter
    def size(self, value: tuple[int, int]):
        GUIObject.size.fset(self, value)

        self._update_framebuffer()
        self._update_layout()
        self.redraw()

    @GUIObject.pos.setter
    def pos(self, value: tuple[int, int]):
        GUIObject.pos.fset(self, value)

        self.parent.redraw()

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

    def redraw(self):
        self._framebuffer.use()
        self._framebuffer.clear()

        for widget in self._widgets:
            widget.draw()

        self.parent.redraw()

    def draw(self):
        super().draw()

        self._mem_texture.use()
        self._vao.render(mgl.TRIANGLE_STRIP)

        if self._show_bbox:
            self._bbox_vao.program['w_size'].write(glm.vec2(self.size))
            self._bbox_vao.render(mgl.TRIANGLE_STRIP)

    def toggle_bbox(self, state=None):
        super().toggle_bbox(state)

        for widget in self._widgets:
            widget.toggle_bbox(self._show_bbox)

        self.redraw()

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def _release_widgets(self, keep_texture=False):
        for widget in self._widgets:
            widget.release(keep_texture)

        self._widgets = LinkedList()

    def release(self, keep_texture=False):
        super().release(keep_texture)

        self._mem_texture.release()
        self._framebuffer.release()
        self._release_widgets(keep_texture)
