import moderngl as mgl


class ShaderProgram:
    def __init__(self, ctx: mgl.Context):
        self.ctx = ctx
        self.programs = {}

    def load(self, shader_name: str) -> mgl.Program:
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()

        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        # self.programs[shader_name] = program

        return program

    def release_all(self) -> None:
        [program.release_all() for program in self.programs]
        self.programs = {}