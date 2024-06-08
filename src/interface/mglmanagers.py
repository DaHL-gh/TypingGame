from moderngl import Context, Texture, Program
from typing import Hashable

from ..functions import load_program


class KWSingleton:
    _instances = {}

    def __new__(cls, key, *args, **kwargs):
        if key not in cls._instances:
            cls._instances[key] = super(KWSingleton, cls).__new__(cls)
            print("created new instance:", key)
        return cls._instances[key]


class TextureManager(KWSingleton):
    def __init__(self, key: Context):
        self.ctx = key

        self.textures: dict[Hashable, Texture] = {}

    def add_texture(self, key, texture: Texture) -> None:
        self.textures[key] = texture

    def get_texture(self, key) -> Texture:
        if key in self.textures:
            return self.textures[key]
        else:
            raise KeyError(f'No such texture in this context: {self.ctx}')

    def release_texture(self, key) -> None:
        if key in self.textures:
            return self.textures.pop(key).release()
        else:
            print('Warning: tried to release non-existent texture')


class ProgramManager(KWSingleton):
    def __init__(self, key: Context):
        self.ctx = key

        self.programs: dict[str, Program] = {}

    def get_program(self, key: str) -> Program:
        if key not in self.programs:
            self.programs[key] = load_program(self.ctx, key)

        return self.programs[key]

    def release_program(self, key) -> None:
        if key in self.programs:
            return self.programs.pop(key).release()
        else:
            print('Warning: tried to release non-existent program')

