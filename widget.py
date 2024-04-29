import glm
import pygame as pg
import numpy as np
import moderngl as mgl
from functions import get_gl_cords_for_rect


class Widget:
    def __init__(self, app, ctx: mgl.Context, size=(150, 200), pos=(0, 0), color=(1, 0, 1)):
        self.app = app
        self.ctx = ctx
        self.size: tuple[int] = size
        self.pos: tuple[int] = pos

        self.vertices = self.ctx.buffer(get_gl_cords_for_rect(self.app.size, self.size, self.pos))
        self.uv = self.ctx.buffer(np.array(((0, 0), (0, 1), (1, 0), (1, 1)), dtype='float32'))
        self.color = self.ctx.buffer(glm.vec3(color))

        self.program = app.program.load('textured_box')

        self.vao = self.ctx.vertex_array(self.program,
                                         [
                                             (self.vertices, '2f /v', 'in_position'),
                                             (self.uv, '2f /v', 'in_texture_cords'),
                                             (self.color, '3f /i', 'in_color')
                                         ])

    def move(self, offset: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(offset) != 2:
            raise ValueError(f'argument len must be 2, not {len(offset)}')

        elif not all(any(isinstance(offset[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.pos = tuple(int(self.pos[i] + offset[i]) for i in (0, 1))
            self.vertices.write(get_gl_cords_for_rect(self.app.size, self.size, self.pos))

    def set_pos(self, pos: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(pos) != 2:
            raise ValueError(f'argument len must be 2, not {len(pos)}')

        elif not all(any(isinstance(pos[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.pos = pos
            self.vertices.write(get_gl_cords_for_rect(self.app.size, self.size, self.pos))

    def set_color(self, color) -> None:
        self.color.write(glm.vec3(color))

    def set_size(self, size: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(size) != 2:
            raise ValueError(f'argument len must be 2, not {len(size)}')

        elif not all(any(isinstance(size[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.size = size
            self.vertices.write(get_gl_cords_for_rect(self.app.size, self.size, self.pos))

    def contains_dot(self, cords: list[int | float, int | float] | tuple[int | float, int | float]) -> bool:
        return all(0 < cords[i] - self.pos[i] < self.size[i] for i in (0, 1))

    def drag(self, mouse_pos):
        self.set_pos(mouse_pos)

    def draw(self) -> None:
        self.vao.render(mgl.TRIANGLE_STRIP)
