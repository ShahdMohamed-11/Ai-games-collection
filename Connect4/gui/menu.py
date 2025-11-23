import tkinter as tk
from gui.base import BaseGUI
from constants import BG_COLOR, ACCENT_COLOR, MIN_DEPTH, MAX_DEPTH, DEFAULT_DEPTH


class MainMenuGUI(BaseGUI):

    
    def __init__(self, root, navigator):
        super().__init__(root, navigator)
        self.selected_depth = None
    
    def build(self):

        container = tk.Frame(self.frame, bg=BG_COLOR)
        container.place(relx=0.5, rely=0.5, anchor='center')
        

        tk.Label(
            container, text="CONNECT 4",
            font=('Arial', 60, 'bold'),
            bg=BG_COLOR, fg='#FFDD00'
        ).pack(pady=(0, 20))
        
        tk.Label(
            container, text="with Alpha-Beta Pruning AI",
            font=('Arial', 20),
            bg=BG_COLOR, fg='#AAAAAA'
        ).pack(pady=(0, 50))
        

        depth_frame = tk.Frame(container, bg=ACCENT_COLOR, padx=40, pady=30)
        depth_frame.pack(pady=20)
        
        tk.Label(
            depth_frame, text="Select AI Difficulty",
            font=('Arial', 18, 'bold'),
            bg=ACCENT_COLOR, fg='white'
        ).pack(pady=(0, 20))
        
        self.selected_depth = tk.IntVar(value=DEFAULT_DEPTH)
        
        btn_frame = tk.Frame(depth_frame, bg=ACCENT_COLOR)
        btn_frame.pack(pady=10)
        
        difficulties = [
            (4, "Medium"),
            (5, "Hard"),
            (6, "Expert")
        ]
        
        for depth, name in difficulties:
            tk.Radiobutton(
                btn_frame,
                text=f"{name}\nDepth {depth}",
                font=('Arial', 14, 'bold'),
                variable=self.selected_depth,
                value=depth,
                bg=ACCENT_COLOR, fg='white',
                selectcolor='#0066CC',
                activebackground=ACCENT_COLOR,
                activeforeground='white',
                indicatoron=0,
                width=10, height=3,
                relief=tk.RAISED, bd=2
            ).pack(side=tk.LEFT, padx=10)
        

        tk.Button(
            container,
            text="▶  START GAME",
            font=('Arial', 24, 'bold'),
            bg='#4CAF50', fg='white',
            padx=40, pady=15,
            command=self._start_game
        ).pack(pady=40)
    
    def _start_game(self):
        depth = self.selected_depth.get()
        self.navigator.start_game(depth)