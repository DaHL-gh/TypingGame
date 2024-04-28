import moderngl as mgl


class VAO:
    def __init__(self, ctx: mgl.Context) -> None:
        self.ctx = ctx
        self.vertex_arrays = {}

    def create(self, file_name: str, vbos: dict, shader_name: str, shader_program: mgl.Program) -> dict:
        vao_name = file_name + "/" + shader_name

        for item in vbos.items():
            vbo_name = item[0]
            vbo_data = item[1]

            if vao_name in self.vertex_arrays:
                self.vertex_arrays[vao_name][vbo_name] = self.ctx.vertex_array(shader_program, [(vbo_data, "3f 2f 3f", "in_position", "in_texture_cords", "in_normal")])
            else:
                self.vertex_arrays[vao_name] = {vbo_name: self.ctx.vertex_array(shader_program, [(vbo_data, "3f 2f 3f", "in_position", "in_texture_cords", "in_normal")])}

        return self.vertex_arrays[vao_name]

    def release(self, id: str) -> None:
        self.vertex_arrays[id].release_all()
        self.vertex_arrays.pop(id)

    def release_all(self):
        [vao.release_all() for vao in self.vertex_arrays]
        self.vertex_arrays = {}