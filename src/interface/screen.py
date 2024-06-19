from __future__ import annotations
from .types import Child

import moderngl as mgl
from abc import abstractmethod

from .root import Root


class Screen:
    def __init__(self, ctx: mgl.Context):
        self._ctx = ctx
        self._root = Root(ctx)

    @property
    def ctx(self) -> mgl.Context:
        return self._ctx

    @property
    def root(self) -> Root:
        return self._root

    @abstractmethod
    def build(self) -> None:
        ...

        # al = AnchorLayout(parent=self._root)
        #
        # font = Font(name='Inkfree', char_size=50)
        #
        # ll2 = LineLayout(parent=al, size=(500, 300), texture=TextureManager(self.ctx).get('chopper.jpg'))
        #
        # TextField(parent=ll2, font=font)
        # Slider(parent=ll2)