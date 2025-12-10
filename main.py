# main.py - 程序入口
from UI import FumenExtractorApp

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    app = FumenExtractorApp(root)
    root.mainloop()