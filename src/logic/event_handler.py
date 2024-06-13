import pygame as pg
import sys


class EventHandler:
    mouse_data = {1: 'left', 2: 'middle', 3: 'right'}

    def __init__(self, window):
        self.window = window

        # MOUSE
        self.drag_info = None

        self.last_press = {'b_name': '', 'pos': (0, 0), 'time': 0, 'count': 0, 'widget': None}

    def handle_events(self):
        window = self.window
        gui = self.window.gui

        for event in pg.event.get():

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                       WINDOW
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            if event.type == pg.VIDEORESIZE:
                window.size = pg.display.get_window_size()

                window.ctx.viewport = (0, 0) + window.size

                gui.size = window.size

            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                       KEYBOARD
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            elif event.type == pg.KEYDOWN:
                if event.dict['key'] == pg.K_F5:
                    gui.widgets[0].line = f'fps: {window.summ // 100}'

                if event.dict['key'] == pg.K_F4:
                    gui.widgets[0].size = (50, 50)

                if event.dict['key'] == pg.K_w:
                    gui.toggle_bbox()


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                        MOUSE
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.dict['button'] in self.mouse_data:
                    button_name = self.mouse_data[event.dict['button']]

                    current_time = pg.time.get_ticks()

                    if self.last_press['b_name'] == button_name:
                        time_from_last_click = current_time - self.last_press['time']
                        if_click_in_range = any(abs(self.last_press['pos'][i] - event.dict['pos'][i]) < 2 for i in (0, 1))

                        if if_click_in_range and time_from_last_click < 500:
                            self.last_press['count'] += 1
                        else:
                            self.last_press['count'] = 1

                    else:
                        self.last_press['b_name'] = button_name
                        self.last_press['count'] = 1

                    self.last_press['time'] = current_time
                    self.last_press['pos'] = event.dict['pos']
                    self.last_press['widget'] = gui.mouse_down(button_name, event.dict['pos'], self.last_press['count'])

            elif event.type == pg.MOUSEBUTTONUP:
                if event.dict['button'] in self.mouse_data:
                    button_name = self.mouse_data[event.dict['button']]

                    gui.mouse_up(button_name, event.dict['pos'])

                    if self.drag_info is not None and self.drag_info['b_name'] == button_name:
                        self.drag_info = None
                        self.last_press['widget'] = None

            elif event.type == pg.MOUSEMOTION:
                if_click_out_of_range = any(abs(self.last_press['pos'][i] - event.dict['pos'][i]) > 2 for i in (0, 1))

                pressed_buttons = set(self.mouse_data[i + 1] if event.dict['buttons'][i] else '' for i in range(3))

                # DRAGGING
                if self.drag_info is not None and self.drag_info['widget'] is not None:
                    self.drag_info['widget'].mouse_drag(self.drag_info['b_name'], event.dict['pos'], event.dict['rel'])

                elif if_click_out_of_range and self.last_press['b_name'] in pressed_buttons:
                    self.drag_info = {'b_name': self.last_press['b_name'], 'widget': self.last_press['widget']}

