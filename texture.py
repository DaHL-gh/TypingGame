import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.textures = {}

    def load_texture(self, path: str) -> mgl.Texture:
        if path not in self.textures:
            texture = pg.image.load(f"textures/{path}")
            texture = pg.transform.flip(texture, flip_y=True, flip_x=False)

            texture = self.ctx.texture(size=texture.get_size(), components=4, data=pg.image.tostring(texture, "RGBA"))

            self.textures[path] = texture

            return texture
        else:
            return self.textures[path]

    def release_all(self) -> None:
        [texture.release_all() for texture in self.textures]
        self.textures = {}