import tkinter as tk
from tkinter import ttk

import theme
from solver import SubsetSum, parse_input
from table import DPTable

MAX_TARGET = 60
MAX_NUMBERS = 14


class App(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.problem = None
        self.steps = None
        self.chosen = []
        self.timer = None

        self.create_controls()
        self.table = DPTable(self, width=1240, height=430)
        self.table.pack(padx=20, pady=5)
        self.create_status()

        root.bind("<Return>", lambda e: self.load())
        root.bind("<space>", lambda e: self.step())

    def create_controls(self):
        top = ttk.Frame(self, padding=(20, 15, 20, 5))
        top.pack(fill="x")

        ttk.Label(top, text="Subset Sum", font=(theme.FONT, 16, "bold")).grid(
            row=0, column=0, columnspan=9, sticky="w", pady=(0, 10))

        ttk.Label(top, text="Numbers:").grid(row=1, column=0, padx=(0, 8))
        self.numbers_entry = ttk.Entry(top, width=28)
        self.numbers_entry.grid(row=1, column=1, padx=(0, 20))
        self.numbers_entry.insert(0, "3, 34, 4, 12, 5, 2")

        ttk.Label(top, text="Target:").grid(row=1, column=2, padx=(0, 8))
        self.target_entry = ttk.Entry(top, width=8)
        self.target_entry.grid(row=1, column=3, padx=(0, 20))
        self.target_entry.insert(0, "9")

        ttk.Button(top, text="Load", style="Accent.TButton", command=self.load).grid(row=1, column=4, padx=4)
        ttk.Button(top, text="Step", command=self.step).grid(row=1, column=5, padx=4)
        self.play_button = ttk.Button(top, text="Play", command=self.toggle_play)
        self.play_button.grid(row=1, column=6, padx=4)
        ttk.Button(top, text="Finish", command=self.finish).grid(row=1, column=7, padx=4)
        ttk.Button(top, text="Reset", command=self.reset).grid(row=1, column=8, padx=4)

        bar = ttk.Frame(top)
        bar.grid(row=2, column=0, columnspan=9, sticky="w", pady=(10, 0))
        ttk.Label(bar, text="Speed:").pack(side="left", padx=(0, 8))
        self.speed = tk.DoubleVar(value=0.6)
        ttk.Scale(bar, from_=0, to=1, variable=self.speed, length=250).pack(side="left")

        for color, text in [(theme.CURRENT, "current"), (theme.SKIP, "skip"),
                            (theme.TAKE, "take"), (theme.PATH, "solution")]:
            box = tk.Canvas(bar, width=14, height=14, bg=theme.BG, highlightthickness=0)
            box.create_rectangle(1, 1, 13, 13, outline=color, width=3)
            box.pack(side="left", padx=(24, 4))
            ttk.Label(bar, text=text).pack(side="left")

    def create_status(self):
        bottom = ttk.Frame(self, padding=(20, 0, 20, 10))
        bottom.pack(fill="x")
        self.info = ttk.Label(bottom, wraplength=1220)
        self.info.pack(anchor="w")
        self.result = ttk.Label(bottom, font=(theme.FONT, 13, "bold"))
        self.result.pack(anchor="w", pady=(4, 0))
        self.info.config(text="Enter numbers and a target, then press Load.")

    def load(self):
        self.stop()
        try:
            numbers, target = parse_input(self.numbers_entry.get(), self.target_entry.get())
        except ValueError as e:
            message = str(e) if "invalid literal" not in str(e) else "Use integers only."
            self.set_result(message, ok=False)
            return

        if target > MAX_TARGET or len(numbers) > MAX_NUMBERS:
            self.set_result(f"Keep target <= {MAX_TARGET} and at most {MAX_NUMBERS} numbers.", ok=False)
            return

        self.problem = SubsetSum(numbers, target)
        self.steps = self.run()
        self.chosen = []

        self.table.draw(numbers, target)
        for s in range(target + 1):
            self.table.set_cell(0, s, self.problem.dp[0][s])

        self.set_result("", ok=True)
        self.info.config(text="Row 0: with no numbers only sum 0 is reachable. Press Step or Play.")

    def run(self):
        p = self.problem
        for i, s, skip, take in p.fill():
            self.show_fill(i, s, skip, take)
            yield

        if not p.solvable():
            self.set_result(f"No subset of {p.numbers} adds up to {p.target}.", ok=False)
            return

        self.set_result("A subset exists. Backtracking to find it...", ok=True)
        yield

        for i, s, taken in p.backtrack():
            self.show_backtrack(i, s, taken)
            yield

        subset = " + ".join(map(str, reversed(self.chosen))) or "empty set"
        self.set_result(f"Solution: {subset} = {p.target}", ok=True)

    def show_fill(self, i, s, skip, take):
        a = self.problem.numbers[i - 1]
        value = self.problem.dp[i][s]

        self.table.clear_marks()
        self.table.mark(i - 1, s, theme.SKIP)
        if take is None:
            text = f"dp[{i}][{s}]: {a} > {s}, can't take it, copy from above = {tf(value)}"
        else:
            self.table.mark(i - 1, s - a, theme.TAKE)
            text = (f"dp[{i}][{s}]: skip {a} -> dp[{i-1}][{s}] = {tf(skip)}, "
                    f"take {a} -> dp[{i-1}][{s-a}] = {tf(take)}, so {tf(value)}")
        self.table.set_cell(i, s, value)
        self.table.mark(i, s, theme.CURRENT)
        self.info.config(text=text)

    def show_backtrack(self, i, s, taken):
        self.table.clear_marks()
        self.table.set_cell(i, s, True, theme.PATH)

        if i == 0:
            self.info.config(text="Reached dp[0][0], done.")
            return

        a = self.problem.numbers[i - 1]
        if taken:
            self.chosen.append(a)
            self.table.highlight_row(i)
            self.table.mark(i - 1, s - a, theme.TAKE)
            self.info.config(text=f"dp[{i-1}][{s}] is F, so {a} must be in the subset.")
        else:
            self.table.mark(i - 1, s, theme.SKIP)
            self.info.config(text=f"dp[{i-1}][{s}] is already T, so {a} isn't needed.")
        self.table.mark(i, s, theme.CURRENT)

    def step(self):
        if self.steps is None:
            return False
        try:
            next(self.steps)
            return True
        except StopIteration:
            self.steps = None
            self.stop()
            return False

    def toggle_play(self):
        if self.timer:
            self.stop()
        elif self.steps:
            self.play_button.config(text="Pause")
            self.tick()

    def tick(self):
        if self.step():
            delay = int(1000 * (1 - self.speed.get()) ** 2) + 15
            self.timer = self.root.after(delay, self.tick)

    def stop(self):
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None
        self.play_button.config(text="Play")

    def finish(self):
        self.stop()
        while self.step():
            pass

    def reset(self):
        self.stop()
        self.steps = None
        self.problem = None
        self.table.delete("all")
        self.set_result("", ok=True)
        self.info.config(text="Enter numbers and a target, then press Load.")

    def set_result(self, text, ok):
        self.result.config(text=text, foreground=theme.PATH if ok else theme.ERROR)


def tf(value):
    return "T" if value else "F"