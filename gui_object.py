import moderngl as mgl
import numpy as np
from functions import load_program


class GUIObject:
    def __init__(self, ctx: mgl.Context, size: tuple[int, int], pos: tuple[int, int]):
        self.ctx = ctx
        self.size = size
        self.pos = pos

        self.vertices = self.ctx.buffer(reserve=32)
        self.uv = self.ctx.buffer(np.array(((0, 0), (0, 1), (1, 0), (1, 1)), dtype='float32'))

        self.texture = self.ctx.texture(size=self.size, components=4)
        self.program = load_program(self.ctx, 'textured_box')

        self.vao = self.ctx.vertex_array(self.program,
                                         [
                                             (self.vertices, '2f /v', 'in_position'),
                                             (self.uv, '2f /v', 'in_bitmap_cords'),
                                         ])

    def move(self, offset: tuple[int, int]) -> None:
        self.pos = tuple(int(self.pos[i] + offset[i]) for i in (0, 1))

    def set_pos(self, pos: tuple[int, int]) -> None:
        self.pos = pos

    def set_size(self, size: tuple[int, int]) -> None:
        self.size = size

    def contains_dot(self, cords: tuple[int, int]) -> bool:
        return all(0 < cords[i] - self.pos[i] < self.size[i] for i in (0, 1))

    def drag(self, mouse_pos: tuple[int, int]) -> None:
        self.set_pos(mouse_pos)

    def draw(self, mode=mgl.TRIANGLE_STRIP) -> None:
        self.vao.render(mode)


class Widget(GUIObject):
    def __init__(self, ctx: mgl.Context, size: tuple[int, int], pos: tuple[int, int]):
        super().__init__(ctx=ctx, size=size, pos=pos)


class Layout(GUIObject):
    def __init__(self, ctx: mgl.Context, size: tuple[int, int], pos: tuple[int, int], rotation='vertical'):
        super().__init__(ctx=ctx, size=size, pos=pos)
        self.rotation = rotation

        self.widgets = []

    def calculate_shapes(self):
        ...

    def add_widget(self, widget: Widget):
        ...

    def draw(self, mode=mgl.TRIANGLE_STRIP):
        for widget in self.widgets:
            widget.draw(mode)

        self.vao.render(mode)

