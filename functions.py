import numpy as np


def convert_vec2(w_size: tuple[int, int], vec2: tuple[int, int]) -> np.ndarray:

    arr = (vec2[0] * 2 / w_size[0] - 1,
           1 - vec2[1] * 2 / w_size[1])

    return np.array(arr, dtype='float32')


def get_rect_vertices(w_size, rect_size, rect_pos) -> np.ndarray:
    arr = np.array([[0 for _ in range(2)] for _ in range(4)], dtype='float32')

    i = 0
    for x in (0, rect_size[0]):
        for y in (0, rect_size[1]):
            arr[i][0] = (rect_pos[0] + x) * 2 / w_size[0] - 1
            arr[i][1] = 1 - (rect_pos[1] + y) * 2 / w_size[1]
            i += 1

    return arr

