import tkinter as tk
from tkinter import ttk

from algorithm import SubsetSum
from util.theme import FONT, WINDOW_BG, TEXT_COLOR
from util.theme import CURRENT_COLOR, TRUE_COLOR, EMPTY_COLOR
from util.theme import CELL_SIZE, CELL_PITCH, LEFT_MARGIN, TOP_MARGIN

SOURCE_COLOR = "#5B8DEF"
PLAY_DELAY = 200


class AlgWindow:
    def __init__(self, master, N, S, T, on_back):
        self.root = master
        self.N = N
        self.S = S
        self.T = T
        self.on_back = on_back

        self.solver = SubsetSum(S, T)
        self.history = list(self.solver.steps())
        self.position = 0
        self.after_id = None
        self.cells = {}

        self.window = self.create_screen()

    def create_screen(self):
        frame = ttk.Frame(self.root, padding=32)

        s_text = ", ".join(map(str, self.S))
        ttk.Label(frame, text=f"S = [{s_text}]").grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )
        ttk.Label(frame, text=f"T = {self.T}").grid(
            row=1, column=0, sticky="w", pady=(0, 16)
        )

        matrix = ttk.Frame(frame)
        matrix.grid(row=2, column=0)
        self.create_matrix(matrix)

        self.status = ttk.Label(frame, text="Press ▶ to begin")
        self.status.grid(row=3, column=0, pady=(16, 0))

        self.timeline = ttk.Scale(
            frame,
            from_=0,
            to=len(self.history),
            orient="horizontal",
            command=self.on_timeline_move,
        )
        self.timeline.grid(row=4, column=0, sticky="ew", pady=(16, 0))

        self.create_buttons(frame)
        return frame

    def create_buttons(self, parent):
        buttons = ttk.Frame(parent)
        buttons.grid(row=5, column=0, pady=(24, 0))

        controls = [
            ("◄◄", self.previous_step),
            ("▶", self.toggle_play),
            ("►►", self.next_step),
            ("⟳", self.restart),
        ]
        for text, command in controls:
            ttk.Button(buttons, text=text, command=command).pack(
                side="left", padx=16
            )

        ttk.Button(
            buttons, text="Back", style="Accent.TButton", command=self.back
        ).pack(side="left", padx=16)

    # Matrix

    def create_matrix(self, parent):
        self.canvas = tk.Canvas(
            parent,
            width=LEFT_MARGIN + (self.T + 1) * CELL_PITCH,
            height=TOP_MARGIN + (self.N + 1) * CELL_PITCH,
            background=WINDOW_BG,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.draw_headers()

        for i in range(self.N + 1):
            for j in range(self.T + 1):
                self.cells[(i, j)] = self.draw_cell(i, j)

        for j in range(self.T + 1):
            self.update_cell(
                (0, j),
                text=self.letter(self.solver.dp[0][j]),
                color=self.color_for((0, j)),
            )

    def cell_origin(self, i, j):
        return LEFT_MARGIN + j * CELL_PITCH, TOP_MARGIN + i * CELL_PITCH

    def draw_headers(self):
        for j in range(self.T + 1):
            x, _ = self.cell_origin(0, j)
            self.draw_text(x + CELL_SIZE / 2, TOP_MARGIN / 2, str(j))

        for i in range(self.N + 1):
            _, y = self.cell_origin(i, 0)
            text = "-" if i == 0 else str(self.S[i - 1])
            self.draw_text(LEFT_MARGIN - 8, y + CELL_SIZE / 2, text, "e")

    def draw_text(self, x, y, text, anchor="center"):
        return self.canvas.create_text(
            x, y, text=text, fill=TEXT_COLOR, font=FONT, anchor=anchor
        )

    def draw_cell(self, i, j):
        x, y = self.cell_origin(i, j)
        shape = self.canvas.create_rectangle(
            x, y, x + CELL_SIZE, y + CELL_SIZE, fill=EMPTY_COLOR, outline=""
        )
        label = self.draw_text(x + CELL_SIZE / 2, y + CELL_SIZE / 2, "")
        return shape, label

    def update_cell(self, cell, text=None, color=None):
        shape, label = self.cells[cell]
        if text is not None:
            self.canvas.itemconfigure(label, text=text)
        if color is not None:
            self.canvas.itemconfigure(shape, fill=color)

    def letter(self, value):
        return "T" if value else "F"

    def color_for(self, cell):
        i, j = cell
        return TRUE_COLOR if self.solver.dp[i][j] else EMPTY_COLOR

    def cell_text(self, cell):
        return f"dp[{cell[0]}][{cell[1]}]"

    # Highlighting

    def clear_highlight(self):
        if self.position == 0:
            return

        i, j, _, leave, take = self.history[self.position - 1]
        for cell in ((i, j), leave, take):
            if cell:
                self.update_cell(cell, color=self.color_for(cell))

    def highlight(self):
        if self.position == 0 or self.position == len(self.history):
            return

        i, j, _, leave, take = self.history[self.position - 1]
        for cell in (leave, take):
            if cell:
                self.update_cell(cell, color=SOURCE_COLOR)
        self.update_cell((i, j), color=CURRENT_COLOR)

    # Timeline

    def go_to(self, position):
        position = max(0, min(position, len(self.history)))
        if position == self.position:
            return

        self.clear_highlight()

        while self.position < position:
            i, j, value, _, _ = self.history[self.position]
            self.update_cell(
                (i, j),
                text=self.letter(value),
                color=self.color_for((i, j)),
            )
            self.position += 1

        while self.position > position:
            self.position -= 1
            i, j, _, _, _ = self.history[self.position]
            self.update_cell((i, j), text="", color=EMPTY_COLOR)

        self.highlight()
        self.timeline.set(position)
        self.update_status()

    def format_formula(self):
        i, j, value, leave, take = self.history[self.position - 1]
        terms = [self.cell_text(cell) for cell in (leave, take) if cell]
        formula = " or ".join(terms)
        return f"{self.cell_text((i, j))} = {formula} = {self.letter(value)}"

    def format_result(self):
        subset = self.solver.find_subset()
        if subset is None:
            return f"No subset sums to {self.T}"
        return f"Found: {subset} = {self.T}"

    def update_status(self):
        if self.position == 0:
            text = "Press ▶ to begin"
        elif self.position == len(self.history):
            text = f"{self.format_formula()}   |   {self.format_result()}"
        else:
            text = self.format_formula()

        self.status.configure(text=text)

    def on_timeline_move(self, value):
        position = round(float(value))
        if position != self.position:
            self.stop()
            self.go_to(position)

    def previous_step(self):
        self.stop()
        self.go_to(self.position - 1)

    def next_step(self):
        self.stop()
        self.go_to(self.position + 1)

    def restart(self):
        self.stop()
        self.go_to(0)

    def toggle_play(self):
        if self.after_id is not None:
            self.stop()
            return

        if self.position == len(self.history):
            self.go_to(0)

        self.play_step()

    def play_step(self):
        self.after_id = None
        self.go_to(self.position + 1)

        if self.position < len(self.history):
            self.after_id = self.window.after(PLAY_DELAY, self.play_step)

    def stop(self):
        if self.after_id is not None:
            self.window.after_cancel(self.after_id)
            self.after_id = None

    def back(self):
        self.stop()
        self.on_back()