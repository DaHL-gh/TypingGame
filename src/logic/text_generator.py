import pandas as pd
from random import randint


class TextGenerator:
    words_data = pd.read_csv('words_data.csv', sep=',')

    def __init__(self, limit: int | None = None):
        self._prefix_sum = None

        if limit is None:
            self.limit = len(self.words_data)
        else:
            self.limit = limit

        self._words = self.words_data['Лемма'][:self.limit]

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value: int | None):
        if value is None:
            self._limit = len(self.words_data)
        else:
            self._limit = value

        self._calc_prefix_sum()
        self._words = self.words_data['Лемма'][:value]

    def _calc_prefix_sum(self) -> None:
        weights = self.words_data['Частота (ipm)']
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


if __name__ == '__main__':
    txt_gen = TextGenerator()

    for _ in range(200):
        print(txt_gen.get(), end=' ')
