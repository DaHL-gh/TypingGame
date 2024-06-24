from __future__ import annotations

import glm
import numpy as np
import moderngl as mgl
import pygame as pg

from .misc.mglmanagers import BufferManager
from .misc.types import Child, Root
from .misc.animation_manager import AnimationManager, Animation



class GUI:
    _size: tuple[int, int]
    _roots: dict[str, Root]
    _current_root: Root | None
    _instances = {}

    def __new__(cls, ctx: mgl.Context, *args, **kwargs):
        if ctx not in cls._instances:
            cls._instances[ctx] = super(GUI, cls).__new__(cls)

            cls._ctx = ctx
            cls._animation_manager = AnimationManager()

            cls._size = ctx.screen.size
            cls._current_root = None
            cls._roots = {}

            cls.init(cls._instances[ctx])

        return cls._instances[ctx]

    def init(self):
        # Buffers
        BufferManager(self.ctx).create('UV', np.array(((0, 0), (0, 1), (1, 0), (1, 1)), dtype='float32'))

        # Animations
        def _back_anim_func(start: int, time: int, end: int):
            if self._current_root is None:
                return

            self.current_root.backgorund.vao.program['time'].write(glm.vec1(time / 1000))
            self.current_root.backgorund.redraw_request()

        self.animation_manager.add(Animation(id='backgorund', func=_back_anim_func,
                                             start=pg.time.get_ticks(), interval=30))

    def build(self):
        for root in self._roots.values():
            root.build()

    def set_root(self, root_id: str) -> None:
        self._current_root = self._roots[root_id]

    def add(self, root: Root) -> None:
        if root.id in self._roots:
            raise NameError(f'Root with id: {root.id} already exist in this GUI class')

        root.size = self.size

        self._roots[root.id] = root

    def __getattr__(self, item):
        if item not in self._roots:
            raise NameError(f'No item: {item} in roots:{self._roots.items()} of {self}')
        return self._roots[item]

    # ////////////////////////////////////////////////// PROPERTIES ////////////////////////////////////////////////////

    @property
    def ctx(self) -> mgl.Context:
        return self._ctx

    @property
    def animation_manager(self) -> AnimationManager:
        return self._animation_manager

    @property
    def current_root(self):
        return self._current_root

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @size.setter
    def size(self, value: tuple[int, int]):
        self._size = value
        if self._current_root is not None:
            self._current_root.size = value

    @property
    def width(self) -> int:
        return self._size[0]

    @property
    def height(self) -> int:
        return self._size[1]

    # //////////////////////////////////////////////////// MOUSE ///////////////////////////////////////////////////////

    def mouse_down(self, button_name: str, mouse_pos: tuple[int, int], count: int) -> Child | None:
        if self._current_root is not None:
            return self._current_root.mouse_down(button_name, mouse_pos, count)

    def mouse_up(self, button_name: str, mouse_pos: tuple[int, int]) -> Child | None:
        if self._current_root is not None:
            return self._current_root.mouse_up(button_name, mouse_pos)

    def mouse_drag(self, button_name: str, mouse_pos: tuple[int, int], rel: tuple[int, int]) -> Child | None:
        if self._current_root is not None:
            return self._current_root.mouse_drag(button_name, mouse_pos, rel)

    # /////////////////////////////////////////////////// DISPLAY //////////////////////////////////////////////////////

    def draw(self) -> None:
        if self._current_root is not None:
            self._current_root.draw()

    def toggle_bbox(self, state=None) -> None:
        if self._current_root is not None:
            self._current_root.toggle_bbox(state)

    # /////////////////////////////////////////////////// RELEASE //////////////////////////////////////////////////////

    def release(self) -> None:
        if self._current_root is not None:
            self._current_root.release()
