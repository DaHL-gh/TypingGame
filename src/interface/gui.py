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
        self.dragged_widget = None
        self.last_press = dict((key, dict((key, {'pos': (0, 0), 'time': 0}) for key in ('single', 'double')))
                               for key in self.mouse_data.values())

        # WIDGETS
        self.font = Font(name='WillowHead', char_size=100)
        self.widget_program = load_program(self.ctx, 'textured_box')

        self.widgets = LinkedList()
        x = ('''W or L''')
        self.frame_counter = TextField(self.ctx, (1000, 300), 'text', self.font, self.widget_program)
        self.widgets.append(self.frame_counter)

        # widget = Widget(self.ctx, pos=(500, 300), size=(200, 200), color=(0.5, 0, 1))
        # self.widgets.append(widget)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                        MOUSE
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def mouse_down(self, button_name, mouse_pos):
        current_time = pg.time.get_ticks()

        time_from_last_doubleclick = current_time - self.last_press[button_name]['double']['time']
        if_doubleclick_out_of_range = any(
            abs(self.last_press[button_name]['double']['pos'][i] - mouse_pos[i]) > 2 for i in (0, 1))

        time_from_last_click = current_time - self.last_press[button_name]['single']['time']
        if_click_in_range = any(
            abs(self.last_press[button_name]['single']['pos'][i] - mouse_pos[i]) < 2 for i in (0, 1))

        # SINGLE CLICK
        self.last_press[button_name]['single']['pos'] = mouse_pos
        self.last_press[button_name]['single']['time'] = current_time

        # DOUBLE CLICK
        if if_doubleclick_out_of_range or time_from_last_doubleclick > 500:
            if if_click_in_range and time_from_last_click < 500:
                self.mouse_doubleclick(button_name, mouse_pos)

                self.last_press[button_name]['double']['pos'] = mouse_pos
                self.last_press[button_name]['double']['time'] = current_time

                return

        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                widget.mouse_down(button_name, mouse_pos)

    def mouse_up(self, button_name, mouse_pos):
        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                widget.mouse_up(button_name, mouse_pos)

        self.dragged_widget = None

    def mouse_doubleclick(self, button_name, mouse_pos):
        for widget in self.widgets:
            if widget.cords_in_rect(mouse_pos):
                widget.mouse_double(button_name, mouse_pos)

    def mouse_motion(self, pressed_buttons, mouse_pos, movement):
        if_click_out_of_range = any(abs(self.last_press['left']['single']['pos'][i] - mouse_pos[i]) > 2 for i in (0, 1))

        # DRAGGING
        if pressed_buttons[0] and self.dragged_widget is None and if_click_out_of_range:
            for i in range(len(self.widgets)):
                if self.widgets[i].cords_in_rect(self.last_press['left']['single']['pos']):
                    self.dragged_widget = self.widgets[i]
                    self.widgets.pop(i)
                    self.widgets.insert(0, self.dragged_widget)
                    break

        if self.dragged_widget is not None:
            self.dragged_widget.move(movement)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#                                                       WIDGETS
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    def draw(self):
        for i in range(len(self.widgets) - 1, -1, -1):
            self.widgets[i].draw()
