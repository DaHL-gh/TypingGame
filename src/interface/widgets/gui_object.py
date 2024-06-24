from __future__ import annotations
from ..misc.types import Child, Parent

from typing import Callable
import glm
import moderngl as mgl
from abc import ABC, abstractmethod

from ..misc.mglmanagers import ProgramManager, BufferManager, TextureManager
from ...functions import get_rect_vertices


class GUIObject(ABC):
    def __init__(self,
                 parent: Parent,
                 id: str | None = None,
                 size: tuple[int | None, int | None] = (None, None),
                 min_size: tuple[int | None, int | None] = (None, None),
                 max_size: tuple[int | None, int | None] = (None, None),
                 size_hint: tuple[float | None, float | None] = (None, None),
                 pos: tuple[int, int] = (0, 0),
                 program: mgl.Program | None = None,
                 texture: mgl.Texture | None = None,
                 keyboard_press_func: Callable | None = None,
                 press_func: Callable | None = None,
                 release_func: Callable | None = None,
                 pressable: bool = False,
                 resize_func: Callable | None = None,
                 repos_func: Callable | None = None,
                 in_focus_func: Callable | None = None,
                 out_focus_func: Callable | None = None):

        # TREE RELATED
        self._id = id
        self._parent = parent

        # FORM
        self._resize_func = resize_func
        self._size = tuple(int(size[i]) if size[i] is not None else 1 for i in (0, 1))
        self._min_size = tuple(max(int(min_size[i]), self._size[i]) if min_size[i] is not None else 1 for i in range(2))
        self._max_size = tuple(min(int(max_size[i]), self._size[i]) if min_size[i] is not None else 1 for i in range(2))
        self._base_size = size
        self._size_hint = size_hint

        self._repos_func = repos_func
        self._pos = pos

        # MGL ATTRIBUTES
        if texture is None:
            texture = TextureManager(self.ctx).get('None.png')
        self._texture = texture

        self._vertices = self.ctx.buffer(reserve=32)
        if program is None:
            program = ProgramManager(self.ctx).get('textured_box')
        self._program = program

        self._vao = self._get_vao()
        self._bbox_vao = self.ctx.vertex_array(ProgramManager(self.ctx).get('bbox_outline'),
                                               [
                                                   (self._vertices, '2f /v', 'in_position'),
                                                   (BufferManager(self.ctx).get('UV'), '2f /v',
                                                    'in_texture_cords')
                                               ])
        self._update_vertices()

        # INPUT
        self._keyboard_press_func = keyboard_press_func

        self.pressable = pressable
        self._press_func = press_func
        self._release_func = release_func

        self._is_in_focus = False
        self._in_focus_func = in_focus_func
        self._out_focus_func = out_focus_func

        # DEBUG
        self.show_bbox = self.parent.show_bbox

        # ADD TO PARENT
        self.parent.add(self)

    def _get_vao(self) -> mgl.VertexArray:
        return self.ctx.vertex_array(self._program,
                                     [
                                         (self._vertices, '2f /v', 'in_position'),
                                         (BufferManager(self.ctx).get('UV'), '2f /v', 'in_texture_cords')
                                     ])

    def cords_in_rect(self, cords):
        return all(0 < cords[i] - self.window_pos[i] < self.size[i] for i in (0, 1))

    def move(self, move):
        self.pos = (self.pos[0] + move[0], self.pos[1] + move[1])

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def ctx(self) -> mgl.Context:
        return self.parent.ctx

    @property
    def id(self):
        return self._id

    @property
    def parent(self):
        return self._parent

    @property
    def root(self):
        return self._parent.root

    @property
    def texture(self) -> mgl.Texture:
        return self._texture

    @property
    def program(self) -> mgl.Program:
        return self._program

    @property
    def vao(self) -> mgl.VertexArray:
        return self._vao

    @property
    def is_in_focus(self):
        return self._is_in_focus

    @property
    def show_bbox(self) -> bool:
        return self._show_bbox

    @show_bbox.setter
    def show_bbox(self, value: bool):
        self._show_bbox = value

    @property
    def pos(self) -> tuple[int, int]:
        return self._pos

    @pos.setter
    def pos(self, value: tuple[int, int]):
        if self._pos != value:
            self._pos = value

            if self._repos_func is not None:
                self._repos_func()

        self._update_vertices()

        self.parent.redraw_request()

    @property
    def window_pos(self) -> tuple[int, int]:
        return self.parent.window_pos[0] + self._pos[0], self.parent.window_pos[1] + self._pos[1]

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        if self._size != value:
            self._size = (max(self._min_size[0], value[0]), max(self._min_size[1], value[1]))

            if self._resize_func is not None:
                self._resize_func()

            self._update_vertices()

            self.parent.update_request()

    @property
    def width(self) -> int:
        return self._size[0]

    @width.setter
    def width(self, value: int):
        self.size = (max(self.min_width, value), self.height)

    @property
    def height(self) -> int:
        return self._size[1]

    @height.setter
    def height(self, value: int):
        self.size = (self.width, max(self.min_height, value))

    @property
    def center(self) -> tuple[int, int]:
        return self.center_x, self.center_y

    @property
    def center_x(self) -> int:
        return self.width // 2

    @property
    def center_y(self) -> int:
        return self.height // 2

    @property
    def size_hint(self) -> tuple[float | None, float | None]:
        return self._size_hint

    @property
    def width_hint(self) -> float | None:
        return self.size_hint[0]

    @property
    def height_hint(self) -> float | None:
        return self.size_hint[1]

    @property
    def base_size(self) -> tuple[int | None, int | None]:
        return self._base_size

    @property
    def base_width(self) -> int | None:
        return self._base_size[0]

    @property
    def base_height(self) -> int | None:
        return self._base_size[1]

    @property
    def min_size(self) -> tuple[int, int]:
        return self._min_size

    @property
    def min_width(self) -> int:
        return self._min_size[0]

    @property
    def min_height(self) -> int:
        return self._min_size[1]

    @property
    def max_size(self) -> tuple[int, int]:
        return self._max_size

    @property
    def max_width(self) -> int:
        return self._max_size[0]

    @property
    def max_height(self) -> int:
        return self._max_size[1]

    # /////////////////////////////////////////////////// UPDATE ///////////////////////////////////////////////////////

    def _update_vertices(self):
        self.parent.framebuffer.use()
        self._vertices.write(get_rect_vertices(fb_size=self.ctx.fbo.viewport[2:],
                                               rect_size=self.size,
                                               rect_pos=self.pos))

    # //////////////////////////////////////////////////// INPUT ///////////////////////////////////////////////////////

    def in_focus(self):
        self._is_in_focus = True
        if self._in_focus_func is not None:
            self._in_focus_func()
        self._in_focus()

    def _in_focus(self):
        pass

    def out_focus(self):
        self._is_in_focus = False
        if self._out_focus_func is not None:
            self._out_focus_func()
        self._out_focus()

    def _out_focus(self):
        pass

    def mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        if not self.pressable:
            return

        mouse_pos = (mouse_pos[0] - self.window_pos[0], mouse_pos[1] - self.window_pos[1])
        if self._press_func is not None:
            self._press_func()
        self._mouse_down(button_name, mouse_pos, count)

        return self

    def _mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        return None

    def mouse_up(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        if not self.pressable:
            return

        mouse_pos = (mouse_pos[0] - self.window_pos[0], mouse_pos[1] - self.window_pos[1])
        if self._release_func is not None:
            self._release_func()
        self._mouse_up(button_name, mouse_pos)

        return self

    def _mouse_up(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        return None

    def mouse_drag(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:

        mouse_pos = (mouse_pos[0] - self.window_pos[0], mouse_pos[1] - self.window_pos[1])
        return self._mouse_drag(button_name, mouse_pos, rel)

    def _mouse_drag(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        return None

    def keyboard_press(self, key: int, unicode: str):
        self._keyboard_press(key, unicode)

        if self._keyboard_press_func is not None:
            self._keyboard_press_func()

    def _keyboard_press(self, key: int, unicode: str):
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
        self._bbox_vao.release()
