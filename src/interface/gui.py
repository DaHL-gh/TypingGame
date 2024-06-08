import pygame as pg
import moderngl as mgl
import glm
from structlinks.LinkedList import LinkedList
from numpy.random import rand

from ..functions import load_program
from .text_render import TextField, Font


class GUI:
    mouse_data = {1: 'left', 2: 'middle', 3: 'right'}

    def __init__(self, window):
        # WINDOW
        self.window = window
        self.ctx = window.ctx

        # MOUSE
        self.drag_info = None
        self.last_press = dict((key, dict((key, {'pos': (0, 0), 'time': 0}) for key in ('single', 'double')))
                               for key in self.mouse_data.values())

        self.last_press = {'b_name': '', 'pos': (0, 0), 'time': 0, 'count': 0}

        # WIDGETS
        self.font = Font(name='WillowHead', char_size=100)
        self.widget_program = load_program(self.ctx, 'textured_box')

        self.widgets = LinkedList()
        self.frame_counter = TextField(self.ctx, (1000, 300), 'text', self.font, self.widget_program)
        self.widgets.append(self.frame_counter)

        # widget = Widget(self.ctx, pos=(500, 300), size=(200, 200), color=(0.5, 0, 1))
        # self.widgets.append(widget)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                        MOUSE
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def mouse_down(self, button_name, mouse_pos):
        current_time = pg.time.get_ticks()

        if self.last_press['b_name'] == button_name:
            time_from_last_click = current_time - self.last_press['time']
            if_click_in_range = any(abs(self.last_press['pos'][i] - mouse_pos[i]) < 2 for i in (0, 1))

            if if_click_in_range and time_from_last_click < 500:
                self.last_press['count'] += 1
            else:
                self.last_press['count'] = 1

        else:
            self.last_press['b_name'] = button_name
            self.last_press['count'] = 1

        self.last_press['time'] = current_time
        self.last_press['pos'] = mouse_pos

        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                widget.mouse_down(button_name, mouse_pos, self.last_press['count'])

    def mouse_up(self, button_name, mouse_pos):
        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                widget.mouse_up(button_name, mouse_pos)

        if self.drag_info is not None and self.drag_info['b_name'] == button_name:
            self.drag_info = None

    def mouse_motion(self, pressed_buttons, mouse_pos, rel):
        if_click_out_of_range = any(abs(self.last_press['pos'][i] - mouse_pos[i]) > 2 for i in (0, 1))

        pressed_buttons = set(self.mouse_data[i + 1] if pressed_buttons[i] else '' for i in range(3))

        # DRAGGING
        if self.drag_info is not None:
            self.drag_info['widget'].mouse_drag(self.drag_info['b_name'], mouse_pos, rel)

        elif if_click_out_of_range and self.last_press['b_name'] in pressed_buttons:
            for i in range(len(self.widgets)):
                w = self.widgets[i]
                if w.cords_in_rect(self.last_press['pos']):
                    self.drag_info = {'b_name': self.last_press['b_name'], 'widget': w}
                    self.widgets.pop(i)
                    self.widgets.insert(0, w)

                    w.mouse_drag(self.last_press['b_name'], mouse_pos, rel)

                    break



# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                       WIDGETS
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def add_widget(self, widget):
        pass

    def draw(self):
        for i in range(len(self.widgets) - 1, -1, -1):
            self.widgets[i].draw()
