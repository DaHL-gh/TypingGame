import glm
import pygame as pg

from src.interface.layouts.anchorlayout import AnchorLayout
from src.interface.layouts.linelayout import LineLayout
from src.interface.misc.animation_manager import Animation
from src.interface.misc.mglmanagers import ProgramManager
from src.interface.widgets.root import Root
from src.interface.widgets.text_line import TextLine
from src.interface.widgets.text_render import Font


class Logo(Root):
    def __init__(self, ctx):
        super().__init__(ctx, 'logo')

    def build(self) -> None:
        def on_press():
            self.gui.main.use()

        al = AnchorLayout(parent=self, pressable=True, press_func=on_press)

        LineLayout(parent=al, size_hint=(1, 1), program=ProgramManager(self.ctx).get('background_fog'), id='backgorund')

        char_size = 100
        font = Font(name='Inkfree', char_size=char_size)

        TextLine(parent=al, line='TypingGame', font=font, id='textfield')
