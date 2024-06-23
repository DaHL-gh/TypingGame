from src.interface.layouts.anchorlayout import AnchorLayout
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

        char_size = 100
        font = Font(name='Inkfree', char_size=char_size)

        TextLine(parent=al, line='TypingGame', font=font, id='textfield')
