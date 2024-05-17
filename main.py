import sys
import pygame as pg
import moderngl as mgl
from structlinks.LinkedList import LinkedList

from gui import GUI
from event_handler import EventHandler

class Window:
    def __init__(self, size=(1000, 600)):

        # SETTING PYGAME TO WORK WITH OPENGL
        self.display = pg.display.set_mode(size, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # CREATING CONTEXT
        self.ctx = mgl.create_context()
        self.ctx.enable(mgl.BLEND)

        # WINDOW PARAMETERS
        self.fps = 60
        self.size = size

        # OTHER ATTRIBUTES
        self.clock = pg.time.Clock()
        self.event_handler = EventHandler(self)
        self.gui = GUI(self)

    def draw(self):
        self.gui.draw()

    def run(self):
        fps_buffer = LinkedList([100 for _ in range(100)])
        self.summ = 100 * 100

        while True:
            self.ctx.clear()
            self.event_handler.handle_events()

            self.draw()
            # print(self.summ // 100)

            self.summ -= fps_buffer.pop(0)
            x = self.clock.get_fps()
            self.summ += x
            fps_buffer.append(x)

            pg.display.flip()

            self.clock.tick(self.fps)


if __name__ == '__main__':
    pg.init()

    w = Window()
    w.run()
