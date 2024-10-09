import pandas as pd
from random import randint

from ..settings import BASE_DIR


class TextGenerator:

    def __init__(self, limit: int | None = None, language='russian'):
        self._prefix_sum = None

        self._language = language
        self._words_df = self._get_words_df(language)

        if limit is None:
            self.limit = len(self._words_df)
        else:
            self.limit = limit

        self._words = self._words_df['word'][:self.limit]

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value: str):
        self._language = value

        self._get_words_df(value)

    @staticmethod
    def _get_words_df(language):
        try:
            return pd.read_csv(f'{BASE_DIR}/data/words_data/{language}.csv', sep=';')
        except FileNotFoundError:
            raise NameError(f'No such words data for language name: {language}')

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value: int | None):
        if value is None:
            self._limit = len(self._words_df)
        else:
            self._limit = value

        self._calc_prefix_sum()
        self._words = self._words_df['word'][:value]

    def _calc_prefix_sum(self) -> None:
        weights = self._words_df['count']
        self._prefix_sum = [0 for _ in range(self.limit)]

        temp = 0
        i = 0
        while i != self.limit:
            temp += weights[i]
            self._prefix_sum[i] = temp
            i += 1

    @staticmethod
    def _binary_search(value: float, lst: list):
        left_i = 0
        right_i = len(lst) - 1

        while left_i < right_i:
            probe = (right_i + left_i) // 2

            if lst[probe] < value:
                left_i = probe + 1
            elif lst[probe] > value:
                right_i = probe - 1
            else:
                return probe

        if left_i != right_i:
            return probe
        else:
            return left_i if lst[left_i] >= value else left_i + 1

    def get(self) -> str:
        rand_int = randint(int(self._prefix_sum[0]), int(self._prefix_sum[-1]))

        return self._words[self._binary_search(rand_int, self._prefix_sum)]
