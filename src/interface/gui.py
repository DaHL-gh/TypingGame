import pygame as pg
import moderngl as mgl
import glm
from structlinks.LinkedList import LinkedList
from numpy.random import rand

from .mglmanagers import ProgramManager, TextureManager
from ..functions import load_program
from .text_render import TextField, Font
from .gui_object import GUILayout


class GUI(GUILayout):

    def __init__(self, window):
        # WINDOW
        super().__init__(window.ctx, window.size, (0, 0)
                         , ProgramManager(window.ctx).get_program('textured_box_reversed'))

        self.window = window

        # WIDGETS
        self.font = Font(name='WillowHead', char_size=100)

        self.widgets = LinkedList()
        self.frame_counter = TextField(self.ctx, (500, 300), 'tehgfhjhghjhfgjkfxt', self.font,
                                       ProgramManager(self.ctx).get_program('textured_box'),
                                       TextureManager(self.ctx).get_texture('Chopper.jpg'))
        self.widgets.append(self.frame_counter)

    def update_layout(self):
        self._framebuffer.use()

        for widget in self.widgets:
            widget.pos = widget.pos

        self.ctx.screen.use()
