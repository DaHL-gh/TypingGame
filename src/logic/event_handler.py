import pygame as pg
import sys

from .mouse import MouseClick, MouseMove, LastPress, DragInfo


class EventHandler:
    def __init__(self, window):
        self.window = window

        # MOUSE
        self.drag_info = DragInfo()
        self.last_press = LastPress()

    def handle_events(self):
        window = self.window
        gui = self.window.gui

        for event in pg.event.get():

            # //////////////////////////////////////////////////////////////////////////////////////////////////////////
            #                                           WINDOW
            # //////////////////////////////////////////////////////////////////////////////////////////////////////////

            if event.type == pg.VIDEORESIZE:
                window.size = pg.display.get_window_size()

                window.ctx.viewport = (0, 0) + window.size

                gui.size = window.size

            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # //////////////////////////////////////////////////////////////////////////////////////////////////////////
            #                                           KEYBOARD
            # //////////////////////////////////////////////////////////////////////////////////////////////////////////

            elif event.type == pg.KEYDOWN:
                if event.dict['key'] == pg.K_F1:
                    gui.toggle_bbox()

                if event.dict['key'] == pg.K_F2:
                    pass

                if self.last_press.widget is not None:
                    self.last_press.widget.keyboard_press(event.dict['key'], event.dict['unicode'])

            # //////////////////////////////////////////////////////////////////////////////////////////////////////////
            #                                            MOUSE
            # //////////////////////////////////////////////////////////////////////////////////////////////////////////

            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_click = MouseClick(event)

                if mouse_click.b_name is None:
                    return

                current_time = pg.time.get_ticks()

                if self.last_press.b_name == mouse_click.b_name:
                    time_from_last_click = current_time - self.last_press.time
                    if_click_in_range = any(abs(self.last_press.pos[i] - mouse_click.pos[i]) < 2 for i in (0, 1))

                    if if_click_in_range and time_from_last_click < 500:
                        self.last_press.count += 1
                    else:
                        self.last_press.count = 1

                else:
                    self.last_press.b_name = mouse_click.b_name
                    self.last_press.count = 1

                self.last_press.time = current_time
                self.last_press.pos = mouse_click.pos

                x = self.last_press.widget

                self.last_press.widget = gui.mouse_down(mouse_click.b_name, mouse_click.pos, self.last_press.count)

                if x != self.last_press.widget:
                    if x is not None:
                        x.out_focus()
                    if self.last_press.widget is not None:
                        self.last_press.widget.in_focus()

                print(self.last_press.widget, x)

            elif event.type == pg.MOUSEBUTTONUP:
                mouse_click = MouseClick(event)

                if mouse_click.b_name is None:
                    return

                gui.mouse_up(mouse_click.b_name, mouse_click.pos)

                # STOP DRAGGING
                if self.drag_info is not None and self.drag_info.b_name == mouse_click.b_name:
                    self.drag_info = None
                    self.last_press.widget = None

            elif event.type == pg.MOUSEMOTION:
                mouse_move = MouseMove(event)

                if_click_out_of_range = any(abs(self.last_press.pos[i] - mouse_move.pos[i]) > 2 for i in (0, 1))

                # DRAGGING
                if self.drag_info is not None and self.drag_info.widget is not None:
                    self.drag_info.widget.mouse_drag(self.drag_info.b_name, mouse_move.pos, mouse_move.rel)

                elif if_click_out_of_range and self.last_press.b_name in mouse_move.buttons:
                    self.drag_info = DragInfo(self.last_press.b_name, self.last_press.widget)
