import tkinter as tk
from tkinter import ttk
import random

class InitWindow:
    def __init__(self, master):
        self.root = master
        self.N = 0
        self.S = []
        self.T = 0
        self.window = self.create_input_screen()

    def create_input_screen(self):
        frame = ttk.Frame(self.root, padding=40)

        ttk.Label(frame, text="S:").grid(row=0, column=0, sticky="w", padx=(0, 16), pady=16)
        self.S_entry = ttk.Entry(frame, width=50)
        self.S_entry.grid(row=0, column=1, pady=10)

        ttk.Label(frame, text="T:").grid(row=1, column=0, sticky="w", padx=(0, 16), pady=16)
        self.T_entry = ttk.Entry(frame, width=50)
        self.T_entry.grid(row=1, column=1, pady=10)

        buttons = ttk.Frame(frame)
        buttons.grid(row=2, column=0, columnspan=2, pady=(32, 0))

        ttk.Button(buttons, text="Random",
                command=self.random).pack(side="left", padx=16)

        ttk.Button(buttons, text="Submit", style="Accent.TButton",
                command=self.submit).pack(side="left", padx=16)

        self.root.bind("<Return>", lambda e: self.submit())
        return frame

    def random(self):
        self.N = random.randint(4, 8)
        self.S = [random.randint(1, 20) for _ in range(self.N)]
        self.T = random.randint(1, 40)

        self.S_entry.delete(0, tk.END)
        self.S_entry.insert(0, " ".join(map(str, self.S)))
        self.T_entry.delete(0, tk.END)
        self.T_entry.insert(0, str(self.T))

    def submit(self):
        return
