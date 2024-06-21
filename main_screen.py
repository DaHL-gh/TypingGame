from src.interface.widgets.root import Root
from src.interface.layouts.anchorlayout import AnchorLayout
from src.interface.layouts.linelayout import LineLayout
from src.interface.widgets.slider import Slider
from src.interface.widgets.text_input import TextInput, Font, TextLine


class MainScreen(Root):
    def __init__(self, ctx):
        super().__init__(ctx, 'main')

    def build(self) -> None:
        font = Font(name='RobotoMono-Regular', char_size=50)

        al = AnchorLayout(parent=self, id='al')

        ll = LineLayout(parent=al, padding=10, spacing=20, orientation='vertical', id='main_line')

        text_view_layout = LineLayout(parent=ll, padding=20, spacing=20, orientation='vertical', id='text_view')
        text_line = TextLine(parent=text_view_layout, line='text_line', font=font)
        text_line2 = TextLine(parent=text_view_layout, line='text_line2', font=font)

        def on_press():
            self.gui.main.use()

        input_layout = LineLayout(parent=ll, spacing=10, orientation='vertical', id='input')
        TextInput(parent=input_layout, line='Play', font=font, id='textfield', pressable=True, press_func=on_press)


class Logo(Root):
    def __init__(self, ctx):
        super().__init__(ctx, 'logo')

    def build(self) -> None:
        al = AnchorLayout(parent=self)

        font = Font(name='RobotoMono-Regular', char_size=50)

        def on_press():
            self.gui.main.use()

        TextInput(parent=al, line='TypingGame', font=font, id='textfield', pressable=True, press_func=on_press)
