import tkinter as tk

from app.gui.main_window import EtiquetadorApp


if __name__ == "__main__":
    root = tk.Tk()
    app = EtiquetadorApp(root)
    root.mainloop()
