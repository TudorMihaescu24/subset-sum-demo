class SubsetSum:
    def __init__(self, numbers, target):
        self.numbers = numbers
        self.target = target
        self.n = len(numbers)
        self.dp = [[None] * (target + 1) for _ in range(self.n + 1)]

        self.dp[0][0] = True
        for s in range(1, target + 1):
            self.dp[0][s] = False

    def fill(self):
        for i in range(1, self.n + 1):
            a = self.numbers[i - 1]
            for s in range(self.target + 1):
                skip = self.dp[i - 1][s]
                take = self.dp[i - 1][s - a] if s >= a else None
                self.dp[i][s] = skip or bool(take)
                yield i, s, skip, take

    def solvable(self):
        return self.dp[self.n][self.target]

    def backtrack(self):
        i, s = self.n, self.target
        while i > 0:
            a = self.numbers[i - 1]
            taken = not self.dp[i - 1][s]
            yield i, s, taken
            if taken:
                s -= a
            i -= 1
        yield 0, s, False


def parse_input(numbers_text, target_text):
    numbers = [int(x) for x in numbers_text.replace(",", " ").split()]
    target = int(target_text.strip())

    if not numbers:
        raise ValueError("Enter at least one number.")
    if target < 0 or any(x < 0 for x in numbers):
        raise ValueError("Only non-negative numbers are supported.")
    return numbers, target