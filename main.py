import sys
import pygame as pg
import moderngl as mgl
from structlinks.LinkedList import LinkedList

from glmanager import GlManager
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
        self.gl_manager = GlManager(self.ctx)

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
        fps_buffer = LinkedList([100 for _ in range(100)])
        summ = 100 * 100

        while True:
            self.ctx.clear(0.0, 0.0, 0)
            self.handle_events()
            self.gui.draw()
            # self.gui.text_renderer.render_at(f"fps: {summ // 100}", (0, 50))
            self.gui.line.draw()

            summ -= fps_buffer.pop(0)
            x = self.clock.get_fps()
            summ += x
            fps_buffer.append(x)
            self.clock.tick(self.fps)

            pg.display.flip()


if __name__ == '__main__':
    w = Window()
    w.run()
