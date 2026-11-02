import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

from ui.init_window import InitWindow


import sv_ttk


FONT_FAMILY = "JetBrains Mono"

def apply_font(family):
    for name in tkfont.names():
        tkfont.nametofont(name).configure(family=family)
    ttk.Style().configure(".", font=(family, 11))

WIDTH = 1280
HEIGHT = 720

class DemoUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Subset Sum Demo")
        self.root.geometry("1280x720")
        self.init_window = InitWindow(self.root)

        sv_ttk.set_theme("dark")
        apply_font(FONT_FAMILY)

        self.show(self.init_window.window)

    def show(self, frame):
        for f in (self.init_window.window,):
            f.place_forget()
        frame.place(relx=0.5, rely=0.5, anchor="center")

    def run(self):
        self.root.mainloop()



if __name__ == "__main__":
    DemoUI().run()

