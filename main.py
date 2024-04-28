import sys
import pygame as pg
import moderngl as mgl
from shader_program import ShaderProgram
from GUI import GUI


class Window:
    def __init__(self, size=(1600, 900)):
        pg.init()

        self.fps = 144
        self.clock = pg.time.Clock()
        self.size = size
        self.display = pg.display.set_mode(size, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        self.ctx = mgl.create_context()
        self.ctx.enable(mgl.BLEND)
        self.program = ShaderProgram(self.ctx)
        self.gui = GUI(self)

    def handle_events(self):
        for event in pg.event.get():
            self.gui.process_event(event)
            self.process_event(event)

    def process_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.VIDEORESIZE:
            self.size = pg.display.get_window_size()

    def run(self):
        while True:
            self.ctx.clear(0.0, 0.0, 0)
            self.handle_events()
            self.gui.draw()
            self.clock.tick(self.fps)
            pg.display.flip()


if __name__ == '__main__':
    w = Window()
    w.run()
