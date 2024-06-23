import numpy as np


def levenshtein_distance(word1: str, word2: str, insertion_cost: float = 1,
                         deletion_cost: float = 1, substitution_cost: float = 1):
    m = len(word1)
    n = len(word2)

    dp = np.zeros((m + 1, n + 1))

    dp[0] = np.arange(n + 1) * insertion_cost
    dp[:, 0] = np.arange(m + 1) * deletion_cost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i, j] = dp[i - 1, j - 1]
            else:
                dp[i, j] = min(dp[i - 1, j] * deletion_cost,
                               dp[i, j - 1] * insertion_cost,
                               dp[i - 1, j - 1] * substitution_cost)

    return dp[m, n] / max(m, n)