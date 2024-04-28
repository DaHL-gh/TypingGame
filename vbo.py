import moderngl as mgl


class VBO:
    def __init__(self, ctx: mgl.Context) -> None:
        self.ctx = ctx
        self.vertex_buffers = {}

    def load(self, name: str, data: dict) -> dict:
        for item in data.items():

            if name in self.vertex_buffers:
                self.vertex_buffers[name][item[0]] = self.ctx.buffer(item[1])
            else:
                self.vertex_buffers[name] = {item[0]: self.ctx.buffer(item[1])}

        return self.vertex_buffers[name]

    def release(self, name: str) -> None:
        self.vertex_buffers[name].release_all()
        self.vertex_buffers.pop(name)

    def release_all(self) -> None:
        [buffer.release_all() for buffer in self.vertex_buffers]
        self.vertex_buffers = {}
