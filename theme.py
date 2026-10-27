import tkinter.font as tkfont
from tkinter import ttk

import sv_ttk

FONT = "JetBrains Mono"

BG = "#1c1c1c"
GRID = "#3a3a3a"
EMPTY = "#262626"
TRUE = "#1f4d2e"
FALSE = "#2e2e2e"
TEXT = "#e6e6e6"
MUTED = "#8a8a8a"
ERROR = "#ff99a4"

CURRENT = "#f0c040"
SKIP = "#58a6ff"
TAKE = "#d2a8ff"
PATH = "#3fb950"
CHOSEN_ROW = "#2a3d2f"


def apply():
    sv_ttk.set_theme("dark")
    for name in tkfont.names():
        tkfont.nametofont(name).configure(family=FONT)
    ttk.Style().configure(".", font=(FONT, 11))