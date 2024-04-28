import glm
import pygame as pg
import numpy as np
import moderngl as mgl


class Widget:
    def __init__(self, app, ctx: mgl.Context, size=(150, 200), pos=(0, 0), color=(1, 0, 1)):
        self.app = app
        self.ctx = ctx
        self.size: tuple[int] = size
        self.pos: tuple[int] = pos

        self.vertices = self.ctx.buffer(self.__get_vertices())
        self.uv = self.ctx.buffer(np.array(((0, 0), (0, 1), (1, 0), (1, 1)), dtype='float32') )
        self.color = self.ctx.buffer(glm.vec3(color))

        self.program = app.program.load('colored_box')

        self.vao = self.ctx.vertex_array(self.program,
                                         [
                                             (self.vertices, '2f /v', 'in_position'),
                                             (self.uv, '2f /v', 'in_texture_cords'),
                                             (self.color, '3f /i', 'in_color')
                                         ])

    def __get_vertices(self) -> np.ndarray:
        w_size = pg.display.get_window_size()

        i = 0
        n = [[0], [], [], []]
        for y in (0, self.size[1]):
            for x in (0, self.size[0]):
                n[i] = (self.pos[0] + x, w_size[1] - self.pos[1] - y)

                i += 1

        n[2], n[1] = n[1], n[2]

        for i in range(4):
            n[i] = tuple((n[i][j] / w_size[j] - 0.5) * 2 for j in (0, 1))

        return np.array(n, dtype='float32')

    def move(self, offset: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(offset) != 2:
            raise ValueError(f'argument len must be 2, not {len(offset)}')

        elif not all(any(isinstance(offset[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.pos = tuple(int(self.pos[i] + offset[i]) for i in (0, 1))
            self.vertices.write(self.__get_vertices())

    def set_pos(self, pos: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(pos) != 2:
            raise ValueError(f'argument len must be 2, not {len(pos)}')

        elif not all(any(isinstance(pos[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.pos = pos
            self.vertices.write(self.__get_vertices())

    def set_color(self, color) -> None:
        self.color.write(glm.vec3(color))

    def set_size(self, size: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(size) != 2:
            raise ValueError(f'argument len must be 2, not {len(size)}')

        elif not all(any(isinstance(size[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.size = size
            self.vertices.write(self.__get_vertices())

    def is_in(self, cords: list[int | float, int | float] | tuple[int | float, int | float]) -> bool:
        return all(0 < cords[i] - self.pos[i] < self.size[i] for i in (0, 1))

    def drag(self, mouse_pos):
        self.set_pos(mouse_pos)

    def draw(self) -> None:
        self.vao.render(mgl.TRIANGLE_STRIP)
