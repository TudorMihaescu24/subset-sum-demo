class SubsetSum:
    def __init__(self, S, T):
        self.S = S
        self.T = T
        self.dp = [[False] * (T + 1) for _ in range(len(S) + 1)]
        self.dp[0][0] = True

    def steps(self):
        for i in range(1, len(self.S) + 1):
            for j in range(self.T + 1):
                yield i, j, self.compute_step(i, j)

    def compute_step(self, i, j):
      num = self.S[i - 1]
      leave = self.dp[i - 1][j]
      take = j >= num and self.dp[i - 1][j - num]
      self.dp[i][j] = leave or take
      return self.dp[i][j]

    def solve(self):
        for _ in self.steps():
            pass
        return self.dp[-1][self.target]

    def find_subset(self):
        if not self.dp[-1][self.target]:
            return None

        subset = []
        j = self.target
        for i in range(len(self.numbers), 0, -1):
            if not self.dp[i - 1][j]:
                number = self.numbers[i - 1]
                subset.append(number)
                j -= number

        subset.reverse()
        return subset