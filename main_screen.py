from __future__ import annotations

from dataclasses import dataclass
import pygame as pg

from src.interface.misc.mglmanagers import TextureManager
from src.interface.widgets.gui_object import GUIObject
from src.interface.widgets.root import Root
from src.interface.layouts.anchorlayout import AnchorLayout
from src.interface.layouts.linelayout import LineLayout
from src.interface.widgets.text_line import TextLine
from src.interface.widgets.text_input import TextInput, Font
from src.interface.misc.animation_manager import Animation
from src.logic.text_generator import TextGenerator
from src.logic.levenshtein_distance import levenshtein_distance


class MainScreen(Root):
    def __init__(self, ctx):
        super().__init__(ctx, 'main')

        self.correct_presses = 0
        self.wrong_presses = 0
        self.wpm_data = 0
        self.correct_words_count = 0
        self.wrong_words_count = 0

        self.current_word_num = 0
        self.is_game_on = False

    @property
    def is_game_on(self) -> bool:
        return self._is_game_on

    @is_game_on.setter
    def is_game_on(self, value: bool):
        if value and not self._is_game_on:
            self.gui.main.central_ll.input_ll.timer.start()
        self._is_game_on = value

    def build(self) -> None:
        char_size = 30
        font = Font(name='CascadiaMono', char_size=char_size)

        al = AnchorLayout(parent=self)
        # [
        ll = LineLayout(parent=al, size_hint=(0.8, 0.6), padding=20, spacing=40, orientation='vertical',
                        id='central_ll')

        # --[

        def text_view_resize():
            self.reset_game()

        text_view_layout = LineLayout(parent=ll, size=(None, int(char_size * 3)), padding=0, spacing=0,
                                      orientation='vertical', id='text_view_ll', resize_func=text_view_resize)
        # ----[
        PlayingLine(parent=text_view_layout, font=font, id='current_line')
        GeneratedLine(parent=text_view_layout, font=font, id='next_line')
        # ]----

        input_layout = LineLayout(parent=ll, size=(None, int(char_size * 1.5)), padding=0, spacing=0,
                                  orientation='horizontal', id='input_ll')
        # ----[

        def input_validation():
            input_word = self.gui.main.central_ll.input_ll.input_line.line
            current_line = self.gui.main.central_ll.text_view_ll.current_line
            current_word_data = current_line.words_data[self.current_word_num]

            # оценка слова на правильность
            if input_word != '' and input_word.lower() == current_word_data.word:
                color = (0, 1, 0)
                self.correct_words_count += 1
                self.wpm_data += 1
            else:
                color = (1, 0, 0)
                self.correct_words_count += 1
                ld = levenshtein_distance(current_word_data.word, input_word)
                self.wpm_data += ld
                print(ld)
            current_line.set_color(i=slice(current_word_data.start, current_word_data.end), color=color)

            # пропуск строки
            self.current_word_num += 1
            if self.current_word_num == len(current_line.words_data):
                self.skip_line()

            # выделение целевого слова
            current_word_data = current_line.words_data[self.current_word_num]
            current_line.set_color(i=slice(current_word_data.start, current_word_data.end), color=(0.8, 0.8, 0.8))

        def input_key_press():
            self.is_game_on = True

            input_word = self.gui.main.central_ll.input_ll.input_line.line
            current_line = self.gui.main.central_ll.text_view_ll.current_line
            current_word_data = current_line.words_data[self.current_word_num]

            # выделение неправильно вводимого слова
            if not current_word_data.word.startswith(input_word):
                current_line.set_color(i=slice(current_word_data.start, current_word_data.end), color=(0.8, 0, 0))
            else:
                current_line.set_color(i=slice(current_word_data.start, current_word_data.end), color=(0.8, 0.8, 0.8))

        Input(parent=input_layout, size=(None, int(char_size * 1.5)), font=font,
              id='input_line', pressable=True, validate_func=input_validation, keyboard_press_func=input_key_press)

        Timer(parent=input_layout, font=font, line='0:00', size=(int(char_size * 4), int(char_size * 1.5)), id='timer')

        GUIObject(parent=input_layout, size=(int(char_size * 1.5), int(char_size * 1.5)), press_func=self.reset_game,
                  pressable=True, id='reset_button', texture=TextureManager(self.ctx).get('reset_button.png'))
        # ]----

        # ]--
        # ]

    def skip_line(self):
        self.current_word_num = 0
        text_view_ll = self.gui.main.central_ll.text_view_ll

        text_view_ll.current_line.line = text_view_ll.next_line.line
        text_view_ll.next_line.generate(max_width=text_view_ll.width)

    def reset_game(self):
        self.skip_line()
        self.skip_line()

        current_line = self.gui.main.central_ll.text_view_ll.current_line

        if len(current_line.words_data) > 0:
            if self.is_game_on:
                self.gui.animation_manager.pop('timer')
                self.gui.main.central_ll.input_ll.timer.line = '0:00'

            self.gui.main.central_ll.input_ll.input_line.line = self.gui.main.central_ll.input_ll.input_line.placeholder

            self.is_game_on = False

            current_word_data = current_line.words_data[self.current_word_num]
            current_line.set_color(i=slice(current_word_data.start, current_word_data.end), color=(0.8, 0.8, 0.8))

            self.all_presses = 0
            self.wrong_presses = 0
            self.correct_words_count = 0

            self.current_word_num = 0

    def end_game(self):
        self.reset_game()


class Timer(TextLine):
    def __init__(self, font: Font, **kwargs):
        super().__init__(font, **kwargs)

    def _get_animation(self) -> Animation:
        return Animation(id='timer', func=self._animation_func, start=pg.time.get_ticks(), interval=1000, end=60_000)

    def _animation_func(self, start: int, time: int, end: int):
        self.line = f'{(end + start - time) // 60_000}:{(end + start - time) // 1000 % 60}'

        if time == end:
            self.line = '0:00'
            self.root.is_game_on = False
            self.root.gui.results.set_data(keystrokes=(self.root.correct_presses, self.root.wrong_presses),
                                           wpm=self.root.wpm_data,
                                           words=(self.root.correct_words_count, self.root.wrong_words_count))
            self.root.gui.results.use()

    def start(self):
        self.root.gui.animation_manager.add(self._get_animation())


class Input(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _validate(self):
        self.line = ''

    def _keyboard_press(self, key: int, unicode: str) -> None:
        if unicode == '\b':  # BACKSPACE
            self.remove_last()
        elif unicode == '\x1b' or unicode == '\t' or unicode == '\n':  # ESCAPE and TAB and ENTER
            pass
        elif unicode == ' ':
            self.validate()
        else:
            self.line += unicode

            current_line = self.root.central_ll.text_view_ll.current_line
            current_word_data = current_line.words_data[self.root.current_word_num]

            if not current_word_data.word.startswith(self.line):
                self.root.wrong_presses += 1
            else:
                self.root.correct_presses += 1


@dataclass
class _GeneratedWord:
    start: int
    end: int
    word: str


class GeneratedLine(TextLine):
    def __init__(self, font: Font, text_gen_limit: int | None = None, **kwargs):
        super().__init__(font, **kwargs)

        self.text_gen = TextGenerator(limit=text_gen_limit)

    def generate(self, max_width):
        self.width = max_width
        self.line = ''
        while True:
            gen_word = self.text_gen.get()
            word_len = sum(self._font.get_glyph(ord(i)).horizontal_advance for i in gen_word)

            if self._pen[0] + word_len < self.width:
                self.line += gen_word + ' '
            else:
                break


class PlayingLine(TextLine):
    def __init__(self, font: Font, **kwargs):
        super().__init__(font, **kwargs)

        current_word = 0
        self._words_data = []

    @property
    def words_data(self):
        return self._words_data

    @TextLine.line.setter
    def line(self, line: str):
        TextLine.line.fset(self, line)

        self._words_data = []
        end = -1
        while ' ' in self._line[end + 1:]:
            start = end + 1
            end = self._line[start:].index(' ') + start

            self._words_data.append(_GeneratedWord(start, end, self._line[start:end]))
