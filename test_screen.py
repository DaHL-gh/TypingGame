import glm
import pygame as pg

from src.interface.layouts.linelayout import LineLayout
from src.interface.misc.animation_manager import Animation
from src.interface.layouts.anchorlayout import AnchorLayout
from src.interface.misc.mglmanagers import ProgramManager
from src.interface.widgets.root import Root


class Test(Root):
    def __init__(self, ctx, id='test'):
        super().__init__(ctx, id)

    def build(self) -> None:
        al = AnchorLayout(parent=self)

        LineLayout(parent=al, size_hint=(1, 1), program=ProgramManager(self.ctx).get('background_fog'), id='backgorund')

        self.root.gui.animation_manager.add(self._get_animation())

    def _get_animation(self) -> Animation:
        return Animation(id='backgorund', func=self._animation_func, start=pg.time.get_ticks())

    def _animation_func(self, start: int, time: int, end: int):
        self.backgorund.vao.program['time'].write(glm.vec1(time / 1000))
        self.backgorund.redraw_request()

