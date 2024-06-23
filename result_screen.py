from src.interface.layouts.anchorlayout import AnchorLayout
from src.interface.layouts.linelayout import LineLayout
from src.interface.widgets.root import Root
from src.interface.widgets.text_line import TextLine
from src.interface.widgets.text_render import Font


class Results(Root):
    def __init__(self, ctx):
        super().__init__(ctx, 'results')

    def build(self) -> None:
        title_font = Font(name='Inkfree', char_size=100)
        lower_title_font = Font(name='Inkfree', char_size=50)
        numbers_font = Font(name='CascadiaMono', char_size=30)

        al = AnchorLayout(parent=self)

        result_ll = LineLayout(parent=al, size_hint=(1, 0.8), id='main_ll')

        TextLine(parent=result_ll, font=title_font, line='Результат')
        TextLine(parent=result_ll, font=lower_title_font, line='Нажатия')

        TextLine(parent=result_ll, font=numbers_font, id='keystrokes_line')

        TextLine(parent=result_ll, font=lower_title_font, line='Слова В Минуту')

        TextLine(parent=result_ll, font=numbers_font, id='words_line')

    def set_data(self, keystrokes: tuple[int, int], wpm: float, words: tuple[int, int]):
        self.main_ll.keystrokes_line.line = f'({keystrokes[0]}|{keystrokes[1]}) : {keystrokes[0] + keystrokes[1]}'
        temp = 1
        self.main_ll.keystrokes_line.set_color(i=slice(temp, temp + len(str(keystrokes[0]))), color=(0.1, 0.8, 0.1))
        temp += len(str(keystrokes[0])) + 1
        self.main_ll.keystrokes_line.set_color(i=slice(temp, temp + len(str(keystrokes[1]))), color=(0.8, 0.1, 0.1))

        self.main_ll.words_line.line = f'({words[0]}|{words[1]}) : {wpm}'
        temp = 1
        self.main_ll.words_line.set_color(i=slice(temp, temp + len(str(words[0]))), color=(0.1, 0.8, 0.1))
        temp += len(str(words[0])) + 1
        self.main_ll.words_line.set_color(i=slice(temp, temp + len(str(words[1]))), color=(0.8, 0.1, 0.1))


