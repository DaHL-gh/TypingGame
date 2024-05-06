import moderngl as mgl

from functions import get_norm_cords_for_rect
from glmanager import GlManager


class GUIObject:
    def __init__(self, gl_manager, size=(150, 200), pos=(0, 0), color=(1, 1, 1)):
        self.gl_manager: GlManager = gl_manager
        self.size: tuple[int] = size
        self.pos: tuple[int] = pos

    def move(self, offset: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(offset) != 2:
            raise ValueError(f'argument len must be 2, not {len(offset)}')

        elif not all(any(isinstance(offset[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.pos = tuple(int(self.pos[i] + offset[i]) for i in (0, 1))

    def set_pos(self, pos: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(pos) != 2:
            raise ValueError(f'argument len must be 2, not {len(pos)}')

        elif not all(any(isinstance(pos[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.pos = pos

    def set_size(self, size: list[int | float, int | float] | tuple[int | float, int | float]) -> None:
        if len(size) != 2:
            raise ValueError(f'argument len must be 2, not {len(size)}')

        elif not all(any(isinstance(size[i], cls) for cls in (int, float)) for i in (0, 1)):
            raise ValueError('argument should contain int or float values')

        else:
            self.size = size

    def contains_dot(self, cords: list[int | float, int | float] | tuple[int | float, int | float]) -> bool:
        return all(0 < cords[i] - self.pos[i] < self.size[i] for i in (0, 1))

    def drag(self, mouse_pos):
        self.set_pos(mouse_pos)

    def draw(self, mode=mgl.TRIANGLE_STRIP) -> None:
        self.vao.render(mode)