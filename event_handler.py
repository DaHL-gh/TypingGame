import pygame as pg
import sys


class EventHandler:
    def __init__(self, window):
        self.window = window

    def handle_events(self):
        window = self.window
        gui = self.window.gui

        for event in pg.event.get():

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                       WINDOW
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            if event.type == pg.VIDEORESIZE:
                window.size = pg.display.get_window_size()

                for widget in gui.widgets:
                    widget.update_vertices()

            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                       KEYBOARD
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            elif event.type == pg.KEYDOWN:
                if event.dict['key'] == pg.K_F5:
                    gui.frame_counter.line = f'fps: {window.summ // 100}'

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                        MOUSE
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.dict['button'] in gui.mouse_data:
                    button_name = gui.mouse_data[event.dict['button']]

                    gui.mouse_down(button_name, pg.mouse.get_pos())

            elif event.type == pg.MOUSEBUTTONUP:
                if event.dict['button'] in gui.mouse_data:
                    button_name = gui.mouse_data[event.dict['button']]

                    gui.mouse_up(button_name, pg.mouse.get_pos())

            elif event.type == pg.MOUSEMOTION:
                gui.mouse_motion(event.dict['buttons'], event.dict['pos'], event.dict['rel'])
