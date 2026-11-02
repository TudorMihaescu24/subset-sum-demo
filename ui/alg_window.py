import tkinter as tk
from tkinter import ttk

from algorithm import SubsetSum
from ui.theme import (
    CELL_PITCH,
    CELL_RADIUS,
    CELL_SIZE,
    CURRENT_COLOR,
    EMPTY_COLOR,
    FONT,
    LEFT_MARGIN,
    TEXT_COLOR,
    TOP_MARGIN,
    TRUE_COLOR,
    WINDOW_BG,
)

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

        ttk.Label(frame, text=f"S = [{', '.join(map(str, self.S))}]").grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )
        ttk.Label(frame, text=f"T = {self.T}").grid(
            row=1, column=0, sticky="w", pady=(0, 16)
        )

        matrix = ttk.Frame(frame)
        matrix.grid(row=2, column=0)
        self.create_matrix(matrix)

        self.status = ttk.Label(frame, text="")
        self.status.grid(row=3, column=0, pady=(16, 0))

        self.create_timeline(frame)
        self.create_buttons(frame)
        return frame

    def create_timeline(self, parent):
        self.timeline = ttk.Scale(
            parent,
            from_=0,
            to=len(self.history),
            orient="horizontal",
            command=self.on_timeline_move,
        )
        self.timeline.grid(row=4, column=0, sticky="ew", pady=(16, 0))

    def create_buttons(self, parent):
        buttons = ttk.Frame(parent)
        buttons.grid(row=5, column=0, pady=(24, 0))

        self.play_button = ttk.Button(buttons, text="▶", command=self.toggle_play)

        ttk.Button(buttons, text="◄◄", command=self.previous_step).pack(
            side="left", padx=16
        )
        self.play_button.pack(side="left", padx=16)
        ttk.Button(buttons, text="►►", command=self.next_step).pack(
            side="left", padx=16
        )
        ttk.Button(buttons, text="⟳", command=self.restart).pack(
            side="left", padx=16
        )
        ttk.Button(
            buttons, text="Back", style="Accent.TButton", command=self.back
        ).pack(side="left", padx=16)

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
                self.cells[(i, j)] = self.draw_cell(*self.cell_origin(i, j))

        self.update_cell((0, 0), text="T", color=TRUE_COLOR)

    def cell_origin(self, i, j):
        return LEFT_MARGIN + j * CELL_PITCH, TOP_MARGIN + i * CELL_PITCH

    def draw_headers(self):
        center = CELL_SIZE / 2

        for j in range(self.T + 1):
            x, _ = self.cell_origin(0, j)
            self.draw_text(x + center, TOP_MARGIN / 2, str(j))

        for i in range(self.N + 1):
            _, y = self.cell_origin(i, 0)
            text = "-" if i == 0 else str(self.S[i - 1])
            self.draw_text(LEFT_MARGIN - 8, y + center, text, anchor="e")

    def draw_text(self, x, y, text, anchor="center"):
        return self.canvas.create_text(
            x, y, text=text, fill=TEXT_COLOR, font=FONT, anchor=anchor
        )

    def draw_cell(self, x, y):
        s, r = CELL_SIZE, CELL_RADIUS
        points = [
            x + r, y, x + s - r, y, x + s, y, x + s, y + r,
            x + s, y + s - r, x + s, y + s, x + s - r, y + s, x + r, y + s,
            x, y + s, x, y + s - r, x, y + r, x, y,
        ]
        shape = self.canvas.create_polygon(points, smooth=True, fill=EMPTY_COLOR)
        label = self.draw_text(x + s / 2, y + s / 2, "")
        return shape, label

    def update_cell(self, position, text=None, color=None):
        shape, label = self.cells[position]
        if text is not None:
            self.canvas.itemconfigure(label, text=text)
        if color is not None:
            self.canvas.itemconfigure(shape, fill=color)

    def on_timeline_move(self, value):
        position = round(float(value))
        if position == self.position:
            return

        self.stop()
        self.go_to(position)

    def go_to(self, position):
        position = max(0, min(position, len(self.history)))
        if position == self.position:
            return

        self.set_highlight(False)

        while self.position < position:
            i, j, value = self.history[self.position]
            self.update_cell(
                (i, j),
                text=str(int(value)),
                color=TRUE_COLOR if value else EMPTY_COLOR,
            )
            self.position += 1

        while self.position > position:
            self.position -= 1
            i, j, _ = self.history[self.position]
            self.update_cell((i, j), text="", color=EMPTY_COLOR)

        self.set_highlight(True)
        self.timeline.set(position)
        self.update_status()

    def set_highlight(self, active):
        if self.position == 0:
            return

        i, j, value = self.history[self.position - 1]
        if active:
            color = CURRENT_COLOR
        else:
            color = TRUE_COLOR if value else EMPTY_COLOR
        self.update_cell((i, j), color=color)

    def update_status(self):
        if self.position == 0:
            text = "Press ▶ to begin"
        elif self.position == len(self.history):
            subset = self.solver.find_subset()
            if subset is None:
                text = f"No subset sums to {self.T}"
            else:
                text = f"Found: {subset} = {self.T}"
        else:
            i, j, value = self.history[self.position - 1]
            text = f"dp[{i}][{j}] = {int(value)}"

        self.status.configure(text=text)

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

        if self.position == len(self.history):
            self.stop()
        else:
            self.after_id = self.window.after(200, self.play_step)

    def stop(self):
        if self.after_id is not None:
            self.window.after_cancel(self.after_id)
            self.after_id = None
        self.play_button.configure(text="▶")

    def back(self):
        self.stop()
        self.on_back()