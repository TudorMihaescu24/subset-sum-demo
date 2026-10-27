import tkinter as tk

import theme


class DPTable(tk.Canvas):
    LABEL_WIDTH = 110

    def __init__(self, parent, width, height):
        super().__init__(parent, width=width, height=height,
                         bg=theme.BG, highlightthickness=0)
        self.width = width
        self.height = height
        self.cells = {}
        self.row_labels = {}
        self.marks = []

    def draw(self, numbers, target):
        self.delete("all")
        self.cells.clear()
        self.row_labels.clear()
        self.marks.clear()

        cols = target + 1
        rows = len(numbers) + 2
        self.cw = min(56, (self.width - self.LABEL_WIDTH - 10) // cols)
        self.ch = min(40, (self.height - 10) // rows)
        self.x0 = self.LABEL_WIDTH + (self.width - self.LABEL_WIDTH - self.cw * cols) // 2
        self.y0 = self.ch + (self.height - self.ch * rows) // 2

        size = max(9, min(15, self.cw // 2 - 2, self.ch // 2))
        font = (theme.FONT, -size)
        bold = (theme.FONT, -size, "bold")

        self.create_text(self.x0 - self.LABEL_WIDTH // 2, self.y0 - self.ch // 2,
                         text="i \\ sum", fill=theme.MUTED, font=font)
        for s in range(cols):
            color = theme.CURRENT if s == target else theme.MUTED
            self.create_text(self.x0 + s * self.cw + self.cw // 2, self.y0 - self.ch // 2,
                             text=str(s), fill=color, font=bold)

        for i in range(len(numbers) + 1):
            y = self.y0 + i * self.ch
            name = "-" if i == 0 else f"{i}: {numbers[i - 1]}"
            box = self.create_rectangle(self.x0 - self.LABEL_WIDTH + 4, y + 1, self.x0 - 4,
                                        y + self.ch - 1, fill=theme.BG, outline="")
            text = self.create_text(self.x0 - self.LABEL_WIDTH // 2, y + self.ch // 2,
                                    text=name, fill=theme.TEXT, font=bold)
            self.row_labels[i] = (box, text)

            for s in range(cols):
                x = self.x0 + s * self.cw
                rect = self.create_rectangle(x, y, x + self.cw, y + self.ch,
                                             fill=theme.EMPTY, outline=theme.GRID)
                label = self.create_text(x + self.cw // 2, y + self.ch // 2,
                                         text="", font=font)
                self.cells[(i, s)] = (rect, label)

    def set_cell(self, i, s, value, color=None):
        rect, label = self.cells[(i, s)]
        if color is None:
            color = theme.TRUE if value else theme.FALSE
        self.itemconfig(rect, fill=color)
        self.itemconfig(label, text="T" if value else "F",
                        fill=theme.TEXT if value else theme.MUTED)

    def mark(self, i, s, color):
        x = self.x0 + s * self.cw
        y = self.y0 + i * self.ch
        self.marks.append(self.create_rectangle(x + 2, y + 2, x + self.cw - 2,
                                                y + self.ch - 2, outline=color, width=3))

    def clear_marks(self):
        for item in self.marks:
            self.delete(item)
        self.marks.clear()

    def highlight_row(self, i):
        box, text = self.row_labels[i]
        self.itemconfig(box, fill=theme.CHOSEN_ROW)
        self.itemconfig(text, fill=theme.PATH)