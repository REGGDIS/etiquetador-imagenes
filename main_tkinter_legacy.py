import tkinter as tk

from app.gui.legacy.tkinter_window import EtiquetadorApp


if __name__ == "__main__":
    root = tk.Tk()
    app = EtiquetadorApp(root)
    root.mainloop()
