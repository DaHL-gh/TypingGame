import numpy as np


def convert_vertices(vertices: tuple[tuple[int]], w_size: tuple[int]) -> np.ndarray:
    i = j = 0
    arr = []
    while i != len(vertices):
        arr.append([])
        while j != len(vertices):
            arr.append((int((vertices[i][j][0] / w_size[0] - 0.5) * 2),
                      int((vertices[i][j][1] / w_size[1] - 0.5) * 2)))
            j += 1
        i += 1

    return np.array(arr, dtype='float32')


def get_gl_cords_for_rect(w_size, rect_size, rect_pos) -> np.ndarray:
    arr = np.array([[0 for _ in range(2)] for _ in range(4)], dtype='float32')

    i = 0
    for x in (0, rect_size[0]):
        for y in (0, rect_size[1]):
            arr[i][0] = ((rect_pos[0] + x) / w_size[0] - 0.5) * 2
            arr[i][1] = ((w_size[1] - rect_pos[1] - y) / w_size[1] - 0.5) * 2
            i += 1

    return arr

