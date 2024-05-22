import moderngl as mgl
import pygame as pg
import glm

from functions import get_rect_vertices, load_program


class Widget:
    def __init__(self, ctx: mgl.Context, size=(150, 200), pos=(0, 0), color=(1, 1, 1)):
        self.ctx = ctx
        self.size = size
        self.pos = pos
        self.color = self.ctx.buffer(glm.vec3(color))

        self.vertices = self.ctx.buffer(get_rect_vertices(pg.display.get_window_size(), self.size, self.pos))

        self.program = load_program(self.ctx, 'textured_box')

        self.vao = self.ctx.vertex_array(self.program,
                                         [
                                             (self.vertices, '2f /v', 'in_position'),
                                             (self.color, '3f /i', 'in_color')
                                         ])

    def update_vertices(self):
        self.vertices.write(get_rect_vertices(pg.display.get_window_size(), self.size, self.pos))

    def move(self, offset: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(offset) != 2:
            raise ValueError(f'argument len must be 2, not {len(offset)}')

        elif not all(any(isinstance(offset[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.pos = tuple(int(self.pos[i] + offset[i]) for i in (0, 1))
            self.update_vertices()

    def set_pos(self, pos: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(pos) != 2:
            raise ValueError(f'argument len must be 2, not {len(pos)}')

        elif not all(any(isinstance(pos[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.pos = pos
            self.update_vertices()

    def set_color(self, color) -> None:
        self.color.write(glm.vec3(color))

    def set_size(self, size: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(size) != 2:
            raise ValueError(f'argument len must be 2, not {len(size)}')

        elif not all(any(isinstance(size[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.size = size
            self.update_vertices()

    def contains_dot(self, cords: list[int | float, int | float] | tuple[int | float, int | float]) -> bool:
        return all(0 < cords[i] - self.pos[i] < self.size[i] for i in (0, 1))

    def drag(self, mouse_pos):
        self.set_pos(mouse_pos)

    def draw(self, mode=mgl.TRIANGLE_STRIP) -> None:
        self.vao.render(mode)
