import numpy as np
import pygame as pg
import moderngl as mgl


def convert_vec2(w_size: tuple[int, int], vec2: tuple[int, int]) -> np.ndarray:

    arr = (vec2[0] * 2 / w_size[0] - 1,
           1 - vec2[1] * 2 / w_size[1])

    return np.array(arr, dtype='float32')


def get_rect_vertices(fb_size, rect_size, rect_pos) -> np.ndarray:
    arr = np.array([[0 for _ in range(2)] for _ in range(4)], dtype='float32')

    i = 0
    for x in (0, rect_size[0]):
        for y in (0, rect_size[1]):
            arr[i][0] = (rect_pos[0] + x) * 2 / fb_size[0] - 1
            arr[i][1] = 1 - (rect_pos[1] + y) * 2 / fb_size[1]
            i += 1

    return arr


def load_program(ctx: mgl.Context, shader_name: str) -> mgl.Program:
    with open(f"shaders/{shader_name}.vert") as file:
        vertex_shader = file.read()

    with open(f"shaders/{shader_name}.frag") as file:
        fragment_shader = file.read()

    program = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

    return program


def get_part_of_frame_buffer(ctx: mgl.Context, pos: tuple[int, int], size: tuple[int, int]
                             , components=4, frame_buffer: int | mgl.Framebuffer = 0) -> mgl.Texture:
    if isinstance(frame_buffer, int):
        frame_buffer = ctx.detect_framebuffer(frame_buffer)

    frame_data = np.frombuffer(frame_buffer.read(components=components), dtype='u1')
    w_shape = pg.display.get_window_size()

    if frame_data.size != w_shape[0] * w_shape[1] * components:
        print('get_part_of_screen: uncorrect framebuffer size')
        return ctx.texture(size=size, components=components, data=None)

    frame_data = frame_data.reshape(w_shape[1], w_shape[0] * components)

    cut_data = frame_data[w_shape[1] - (pos[1] + size[1]): w_shape[1] - pos[1],
                          pos[0] * components: (pos[0] + size[0]) * components]

    return ctx.texture(size=size, components=components, data=np.squeeze(cut_data).tobytes())

