import tkinter as tk

import theme
from app import App


def main():
    root = tk.Tk()
    root.title("Subset Sum")
    root.geometry("1280x720")
    root.resizable(False, False)

    theme.apply()
    App(root).pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()