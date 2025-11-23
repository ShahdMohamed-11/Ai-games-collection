import tkinter as tk
from gui.base import BaseGUI
from constants import BG_COLOR, ACCENT_COLOR, DEFAULT_DEPTH, MIN_DEPTH, MAX_DEPTH, AI_PLAYER, HUMAN_PLAYER
from ai.alphabeta import alphabeta_decision
from ai.minimax import minimax_decision
from ai.expected_minimax import expected_minimax_decision

ALGORITHMS = {
    "Alpha-Beta": alphabeta_decision,
    "Minimax": minimax_decision,
    "Expected Minimax": expected_minimax_decision
}

class MainMenuGUI(BaseGUI):
    def __init__(self, root, navigator):
        super().__init__(root, navigator)
        self.rows_var = tk.IntVar(value=6)
        self.cols_var = tk.IntVar(value=7)
        self.depth_var = tk.IntVar(value=DEFAULT_DEPTH)
        self.algorithm_var = tk.StringVar(value="Alpha-Beta")

    def build(self):
        container = tk.Frame(self.frame, bg=BG_COLOR)
        container.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(container, text="CONNECT 4", font=('Arial', 60, 'bold'),
                 bg=BG_COLOR, fg='#FFDD00').pack(pady=(0, 20))
        tk.Label(container, text="Dynamic AI Game", font=('Arial', 20),
                 bg=BG_COLOR, fg='#AAAAAA').pack(pady=(0, 50))

        # Board size
        size_frame = tk.Frame(container, bg=ACCENT_COLOR, padx=20, pady=20)
        size_frame.pack(pady=10)
        tk.Label(size_frame, text="Board Size", font=('Arial', 16, 'bold'),
                 bg=ACCENT_COLOR, fg='white').pack(pady=(0,10))
        
        row_frame = tk.Frame(size_frame, bg=ACCENT_COLOR)
        row_frame.pack(pady=5)
        tk.Label(row_frame, text="Rows:", bg=ACCENT_COLOR, fg='white', font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        tk.Spinbox(row_frame, from_=4, to=10, textvariable=self.rows_var, width=5, font=('Arial', 12)).pack(side=tk.LEFT, padx=5)

        col_frame = tk.Frame(size_frame, bg=ACCENT_COLOR)
        col_frame.pack(pady=5)
        tk.Label(col_frame, text="Columns:", bg=ACCENT_COLOR, fg='white', font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
        tk.Spinbox(col_frame, from_=4, to=10, textvariable=self.cols_var, width=5, font=('Arial', 12)).pack(side=tk.LEFT, padx=5)

        # AI depth
        depth_frame = tk.Frame(container, bg=ACCENT_COLOR, padx=20, pady=20)
        depth_frame.pack(pady=10)
        tk.Label(depth_frame, text="AI Depth", font=('Arial', 16, 'bold'),
                 bg=ACCENT_COLOR, fg='white').pack(pady=(0,10))
        tk.Spinbox(depth_frame, from_=1, to=8, textvariable=self.depth_var, width=5, font=('Arial', 14)).pack()

        # Algorithm
        algo_frame = tk.Frame(container, bg=ACCENT_COLOR, padx=20, pady=20)
        algo_frame.pack(pady=10)
        tk.Label(algo_frame, text="Select Algorithm", font=('Arial', 16, 'bold'),
                 bg=ACCENT_COLOR, fg='white').pack(pady=(0,10))
        algo_menu = tk.OptionMenu(algo_frame, self.algorithm_var, *ALGORITHMS.keys())
        algo_menu.config(width=15, font=('Arial', 12, 'bold'), bg='white')
        algo_menu.pack()

        # Start button
        tk.Button(container, text="▶ START GAME", font=('Arial', 24, 'bold'),
                  bg='#4CAF50', fg='white', padx=40, pady=15,
                  command=self._start_game).pack(pady=40)

    def _start_game(self):
        rows = self.rows_var.get()
        cols = self.cols_var.get()
        depth = self.depth_var.get()
        algorithm_name = self.algorithm_var.get()
        self.navigator.start_game(rows, cols, depth, ALGORITHMS[algorithm_name])
