import glm
import pygame as pg
import freetype as ft
import numpy as np
import moderngl as mgl
from structlinks.LinkedList import LinkedList

from widget import Widget
from numpy.random import rand

face = ft.Face('fonts/CascadiaMono.ttf')
w = h = 600 << 6
face.set_char_size(width=w, height=h, hres=95, vres=95)
face.load_char('@')
glyph = face.glyph

x = np.array(glyph.bitmap.buffer, dtype='u1')

glyph_bbox = glyph.get_glyph().get_cbox(ft.FT_GLYPH_BBOX_MODES['FT_GLYPH_BBOX_PIXELS'])
x_size = (glyph_bbox.xMax - glyph_bbox.xMin, glyph_bbox.yMax - glyph_bbox.yMin)
print(glyph_bbox.xMax, glyph_bbox.xMin, glyph_bbox.yMax, glyph_bbox.yMin)


print(glyph.bitmap.width, glyph.bitmap.rows)


class GUI:
    def __init__(self, window):
        self.window = window

        self.w_ctx: mgl.Context = window.ctx
        self.t = self.w_ctx.texture(size=(glyph.bitmap.width, glyph.bitmap.rows), data=x, components=1)
        self.t.use()

        self.dragged_widget = None
        self.last_press = dict((key, {'pos': (0, 0), 'time': 0}) for key in ('left', 'right', 'double_left'))

        self.widgets = LinkedList()
        widget = Widget(window, window.ctx, pos=(100, 100), size=x_size)
        self.widgets.append(widget)
        # for j in range(0, 900, 100):
        #     for i in range(0, 1800, 100):
        #         widget = Widget(window, window.ctx, pos=(i, j), size=x_size)
        #         self.widgets.append(widget)

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
