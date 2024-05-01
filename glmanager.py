import moderngl as mgl

from vao import VAO
from vbo import VBO
from texture import Texture
from shader_program import ShaderProgram


class GlManager:
    def __init__(self, ctx: mgl.Context):
        self.ctx = ctx
        self.vao = VAO(ctx)
        self.vbo = VBO(ctx)
        self.texture = Texture(ctx)
        self.shader_program = ShaderProgram(ctx)

