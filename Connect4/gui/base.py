import tkinter as tk
from constants import BG_COLOR


class BaseGUI:
 
    
    def __init__(self, root, navigator):
        self.root = root
        self.navigator = navigator
        self.frame = None
    
    def show(self):
        self.clear()
        self.frame = tk.Frame(self.root, bg=BG_COLOR)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.build()
    
    def build(self):
        raise NotImplementedError
    
    def clear(self):
        if self.frame:
            self.frame.destroy()
            self.frame = None
    
    def hide(self):
        self.clear()