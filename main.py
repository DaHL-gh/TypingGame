import pygame as pg
import moderngl as mgl
from structlinks.LinkedList import LinkedList

from logo_screen import Logo
from main_screen import MainScreen
from result_screen import Results
from src.interface.gui import GUI
from src.logic.event_handler import EventHandler
from src.settings import W_SIZE, FPS


class Window:
    def __init__(self, size=(1000, 600), fps=60):
        # SETTING PYGAME TO WORK WITH OPENGL
        self.display = pg.display.set_mode(size, flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # CREATING CONTEXT
        self.ctx = mgl.create_context()
        self.ctx.enable(mgl.BLEND)

        # WINDOW PARAMETERS
        self.out_of_focus_fps = 1
        self.base_fps = fps
        self.fps = self.base_fps
        self.size = size

        # CLOCK
        self.clock = pg.time.Clock()

        # EVENT HANDLER
        self.event_handler = EventHandler(self)

        # GUI
        self.gui = GUI(self.ctx)

        Logo(self.ctx).use()
        MainScreen(self.ctx)
        Results(self.ctx)

        self.gui.build()

    def run(self):
        fps_buffer_size = 10
        fps_buffer = LinkedList([0 for _ in range(fps_buffer_size)])
        self.summ = 0

        while True:
            self.ctx.clear()

            self.event_handler.handle_events()
            self.gui.animation_manager.update(pg.time.get_ticks())
            self.gui.draw()

            self.summ -= fps_buffer.pop(0)
            x = self.clock.get_fps() / fps_buffer_size
            self.summ += x
            fps_buffer.append(x)

            pg.display.flip()

            self.clock.tick(self.fps)


def main():
    pg.init()

    w = Window(W_SIZE, FPS)
    w.run()


if __name__ == '__main__':
    main()
