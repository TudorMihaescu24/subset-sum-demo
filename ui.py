import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

import sv_ttk
from ui.init_window import InitWindow
from ui.alg_window import AlgWindow
from ui.theme import FONT_FAMILY, FONT

def apply_font():
    for name in tkfont.names():
        tkfont.nametofont(name).configure(family=FONT_FAMILY)
    ttk.Style().configure(".", font=FONT)

WIDTH = 1280
HEIGHT = 720

class DemoUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Subset Sum Demo")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")

        sv_ttk.set_theme("dark")
        apply_font()

        self.current = None
        self.alg_window = None
        self.init_window = InitWindow(self.root, self.start_algorithm)

        self.show_init()

    def show(self, frame):
        if self.current is not None:
            self.current.place_forget()
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.current = frame

    def show_init(self):
        self.root.bind("<Return>", lambda e: self.init_window.submit())
        self.show(self.init_window.window)

        if self.alg_window is not None:
            self.alg_window.window.destroy()
            self.alg_window = None

    def start_algorithm(self, N, S, T):
        self.root.unbind("<Return>")
        self.alg_window = AlgWindow(self.root, N, S, T, self.show_init)
        self.show(self.alg_window.window)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    DemoUI().run()

