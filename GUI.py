import glm
import pygame as pg
import freetype as ft
import numpy as np
import moderngl as mgl

from widget import Widget
from numpy.random import rand

face = ft.Face('Inkfree.ttf')
w, h = (v for v in (500, 500))
face.set_char_size(w, h)
face.load_char('к')
glyph = face.glyph

x = np.array(glyph.bitmap.buffer)
x = x.astype('u1')
print(glyph.bitmap.width, glyph.bitmap.rows)


class GUI:
    def __init__(self, window):
        self.window = window

        self.w_ctx: mgl.Context = window.ctx
        self.t = self.w_ctx.texture(size=(glyph.bitmap.width, glyph.bitmap.rows), data=x, components=1)
        self.t.use()

        self.dragged_widget = None
        self.last_press = dict((key, {'pos': (0, 0), 'time': 0}) for key in ('left', 'right', 'double_left'))

        self.widget = Widget(window, window.ctx, size=(480, 640))
        self.widget_2 = Widget(window, window.ctx, size=(10, 10), pos=(100, 10, 0), color=(0, 1, 0))

        self.widgets = [self.widget, self.widget_2]

    def process_event(self, event):
        current_time = pg.time.get_ticks()

        if event.type == pg.MOUSEBUTTONDOWN:

            # left button
            if event.dict['button'] == 1:
                # doubleclick
                if current_time - self.last_press['double_left']['time'] > 500 or any(
                        abs(self.last_press['double_left']['pos'][i] - event.dict['pos'][i]) > 4 for i in (0, 1)):
                    if current_time - self.last_press['left']['time'] < 500 and all(
                            abs(self.last_press['left']['pos'][i] - event.dict['pos'][i]) < 4 for i in (0, 1)):

                        self.widget.set_color(glm.vec3((rand(1, 3)[0])))
                        self.widget.set_pos(event.dict['pos'])

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
                for x in reversed(self.widgets):
                    if x.is_in(self.last_press['left']['pos']):
                        self.dragged_widget = x
                        i = self.widgets.index(x)
                        self.widgets[i], self.widgets[-1] = self.widgets[-1], self.widgets[i]
                        break

            if self.dragged_widget is not None:
                self.dragged_widget.move(event.dict['rel'])

        if event.type == pg.VIDEORESIZE:
            for widget in self.widgets:
                widget.move((0, 0))

    def draw(self):
        for widget in self.widgets:
            widget.draw()
