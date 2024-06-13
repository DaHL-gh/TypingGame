from moderngl import Context, Texture, Program, Buffer
import pygame as pg
from typing import Hashable

from ..functions import load_program
from ..settings import BASE_DIR


class KWSingleton:
    _instances = {}

    def __new__(cls, key, *args, **kwargs):
        if key not in cls._instances:
            cls._instances[key] = super(KWSingleton, cls).__new__(cls)
            print("created new instance:", key)
        return cls._instances[key]


class TextureManager:
    _instances = {}

    def __new__(cls, ctx: Context, *args, **kwargs):
        if ctx not in cls._instances:
            cls._instances[ctx] = super(TextureManager, cls).__new__(cls)

            cls.ctx = ctx
            cls.textures: dict[str, Texture] = {}

        return cls._instances[ctx]

    def get_texture(self, name: str) -> Texture:
        if name not in self.textures:
            img = pg.image.load(f'{BASE_DIR}\\data\\textures\\{name}')
            data = pg.image.tobytes(img, 'RGBA')

            self.textures[name] = self.ctx.texture(size=img.get_size(), components=4, data=data)

        return self.textures[name]

    def release_texture(self, name) -> None:
        if name in self.textures:
            return self.textures.pop(name).release()
        else:
            print('Warning: tried to release non-existent texture')


class ProgramManager:
    _instances = {}

    def __new__(cls, ctx: Context, *args, **kwargs):
        if ctx not in cls._instances:
            cls._instances[ctx] = super(ProgramManager, cls).__new__(cls)

            cls.ctx = ctx
            cls.programs: dict[str, Program] = {}

        return cls._instances[ctx]

    def get_program(self, name: str) -> Program:
        if name not in self.programs:
            self.programs[name] = load_program(self.ctx, name)

        return self.programs[name]

    def release_program(self, name) -> None:
        if name in self.programs:
            return self.programs.pop(name).release()
        else:
            print('Warning: tried to release non-existent program')


class BufferManager:
    _instances = {}

    def __new__(cls, ctx: Context, *args, **kwargs):
        if ctx not in cls._instances:
            cls._instances[ctx] = super(BufferManager, cls).__new__(cls)

            cls.ctx = ctx
            cls.buffers: dict[str, Buffer] = {}

        return cls._instances[ctx]

    def create_buffer(self, name:str, data):
        self.load_buffer(name, self.ctx.buffer(data))

    def load_buffer(self, name: str, buffer: Buffer):
        if name in self.buffers:
            self.buffers[name].release()
            print(f'Buffer {name} in {self} was replaced')

        self.buffers[name] = buffer

    def get_buffer(self, name: str) -> Buffer:
        return self.buffers[name]

    def release_program(self, name) -> None:
        if name in self.buffers:
            return self.buffers.pop(name).release()
        else:
            print('Warning: tried to release non-existent buffer')
