import pygame as pg
from numpy.random import rand
import glm
from structlinks.LinkedList import LinkedList

import textRenderer
from widget import Widget


class GUI:
    def __init__(self, window):
        self.window = window
        self.gl_manager = window.__gl_manager

        self.font = textRenderer.Font(name='CascadiaMono', char_size=50)
        self.line = textRenderer.Line(self.gl_manager, self.font, 'abcdef', (100, 100))

        self.dragged_widget = None
        self.last_press = dict((key, {'pos': (0, 0), 'time': 0}) for key in ('left', 'right', 'double_left'))

        self.widgets = LinkedList()
        widget = Widget(self.gl_manager, pos=(100, 100), size=(100, 100), color=(0.5, 0.2, 0.6))
        self.widgets.append(widget)

    def process_event(self, event):
        current_time = pg.time.get_ticks()

        if event.type == pg.MOUSEBUTTONDOWN:

            # left button
            if event.dict['button'] == 1:
                # doubleclick
                if (current_time - self.last_press['double_left']['time'] > 500 or
                        any(abs(self.last_press['double_left']['pos'][i] - event.dict['pos'][i]) > 4 for i in (0, 1))):
                    if (current_time - self.last_press['left']['time'] < 500 and
                            all(abs(self.last_press['left']['pos'][i] - event.dict['pos'][i]) < 4 for i in (0, 1))):

                        self.widgets[0].set_color(glm.vec3((rand(1, 3)[0])))
                        self.widgets[0].set_pos(event.dict['pos'])

                        self.last_press['double_left']['pos'] = event.dict['pos']
                        self.last_press['double_left']['time'] = current_time

                self.last_press['left']['pos'] = event.dict['pos']
                self.last_press['left']['time'] = current_time

        if event.type == pg.MOUSEBUTTONUP:

            # left button
            if event.dict['button'] == 1:
                self.dragged_widget = None

        if event.type == pg.MOUSEMOTION:
            # dragging
            if event.dict['buttons'][0] and self.dragged_widget is None and any(abs(self.last_press['left']['pos'][i] - event.dict['pos'][i]) > 4 for i in (0, 1)):
                for i in range(len(self.widgets)):
                    if self.widgets[i].contains_dot(self.last_press['left']['pos']):
                        self.dragged_widget = self.widgets[i]
                        self.widgets.pop(i)
                        self.widgets.insert(0, self.dragged_widget)
                        break

            if self.dragged_widget is not None:
                self.dragged_widget.move(event.dict['rel'])

        if event.type == pg.VIDEORESIZE:
            for widget in self.widgets:
                widget.move((0, 0))

    def draw(self):
        for i in range(len(self.widgets)-1, -1, -1):
            self.widgets[i].draw()
