import tkinter as tk
from tkinter import messagebox
from gui.base import BaseGUI
from game import Game
from constants import (
    ROWS, COLUMNS, AI_PLAYER, HUMAN_PLAYER,
    BG_COLOR, DARK_BG, BOARD_COLOR, COLORS
)


class GameScreenGUI(BaseGUI):
    """Game screen where the actual gameplay happens."""
    
    def __init__(self, root, navigator):
        super().__init__(root, navigator)
        self.game = None
        self.canvas = None
        self.col_buttons = []
        self.status = None
        self.score_label = None
        self.btn_frame = None
    
    def set_game(self, game):
        self.game = game
    
    def build(self):
        # Configure grid
        self.frame.rowconfigure(0, weight=0)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=0)
        self.frame.rowconfigure(3, weight=0)
        self.frame.columnconfigure(0, weight=1)
        
        self._build_top_bar()
        self._build_canvas()
        self._build_column_buttons()
        self._build_status_bar()
    
    def _build_top_bar(self):
        top_bar = tk.Frame(self.frame, bg=DARK_BG)
        top_bar.grid(row=0, column=0, sticky='ew')
        
        tk.Label(
            top_bar, text="CONNECT 4",
            font=('Arial', 22, 'bold'),
            bg=DARK_BG, fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(
            top_bar, text=f"AI Depth: {self.game.depth}",
            font=('Arial', 12),
            bg=DARK_BG, fg='#AAAAAA'
        ).pack(side=tk.LEFT, padx=20)
        
        # Score display
        self.score_label = tk.Label(
            top_bar, text="AI: 0  |  You: 0",
            font=('Arial', 14, 'bold'),
            bg=DARK_BG, fg='#00FF00'
        )
        self.score_label.pack(side=tk.LEFT, padx=40)
        
        tk.Button(
            top_bar, text="⚙ Menu",
            font=('Arial', 12, 'bold'),
            bg='#555555', fg='white',
            command=self.navigator.show_menu
        ).pack(side=tk.RIGHT, padx=20, pady=10)
    
    def _build_canvas(self):
        self.canvas = tk.Canvas(self.frame, bg=BOARD_COLOR, highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky='nsew')
        self.canvas.bind('<Configure>', self._on_resize)
    
    def _build_column_buttons(self):
        self.btn_frame = tk.Frame(self.frame, bg=BG_COLOR, height=70)
        self.btn_frame.grid(row=2, column=0, sticky='ew')
        self.btn_frame.grid_propagate(False)
        
        self.col_buttons = []
        for col in range(COLUMNS):
            btn = tk.Button(
                self.btn_frame, text="▼",
                font=('Arial', 20, 'bold'),
                bg='#4CAF50', fg='white',
                relief=tk.RAISED, bd=3,
                command=lambda c=col: self._make_move(c)
            )
            self.col_buttons.append(btn)
    
    def _build_status_bar(self):
        status_frame = tk.Frame(self.frame, bg=BG_COLOR)
        status_frame.grid(row=3, column=0, pady=15)
        
        self.status = tk.Label(
            status_frame, text="Your turn (Yellow) - Fill the board!",
            font=('Arial', 20, 'bold'),
            bg=BG_COLOR, fg='#FFDD00'
        )
        self.status.pack(side=tk.LEFT, padx=20)
        
        tk.Button(
            status_frame, text="🔄 Restart",
            font=('Arial', 12, 'bold'),
            bg='#FF9800', fg='white',
            command=self._restart_game
        ).pack(side=tk.LEFT, padx=20)
    
    def _on_resize(self, event):
        self._draw_board()
        self._align_buttons()
    
    def _align_buttons(self):
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw < 10 or ch < 10:
            return
        
        cell = min(cw // COLUMNS, ch // ROWS)
        total_w = cell * COLUMNS
        offset_x = (cw - total_w) // 2
        
        for col, btn in enumerate(self.col_buttons):
            btn.place(x=offset_x + col * cell, width=cell, y=0, height=70)
    
    def _draw_board(self):
        self.canvas.delete("all")
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw < 10 or ch < 10:
            return
        
        cell = min(cw // COLUMNS, ch // ROWS)
        radius = int(cell * 0.42)
        total_w = cell * COLUMNS
        total_h = cell * ROWS
        ox = (cw - total_w) // 2
        oy = (ch - total_h) // 2
        
        # Background
        self.canvas.create_rectangle(0, 0, cw, ch, fill=BG_COLOR)
        self.canvas.create_rectangle(
            ox, oy, ox + total_w, oy + total_h,
            fill=BOARD_COLOR, outline='#004499', width=4
        )
        
        # Grid lines
        for col in range(COLUMNS + 1):
            x = ox + col * cell
            self.canvas.create_line(x, oy, x, oy + total_h, fill='#004499', width=2)
        for row in range(ROWS + 1):
            y = oy + row * cell
            self.canvas.create_line(ox, y, ox + total_w, y, fill='#004499', width=2)
        
        # Pieces
        for row in range(ROWS):
            for col in range(COLUMNS):
                x = ox + col * cell + cell // 2
                y = oy + row * cell + cell // 2
                color = COLORS[self.game.board.grid[row][col]]
                
                # Shadow
                self.canvas.create_oval(
                    x - radius + 4, y - radius + 4,
                    x + radius + 4, y + radius + 4,
                    fill='#004499'
                )
                # Piece
                self.canvas.create_oval(
                    x - radius, y - radius,
                    x + radius, y + radius,
                    fill=color, outline='#222', width=2
                )
    
    def _update_score(self):
        scores = self.game.get_scores()
        self.score_label.config(
            text=f"AI: {scores['ai']}  |  You: {scores['human']}"
        )
    
    def _make_move(self, col):
        if self.game.is_game_over():
            return
        if not self.game.board.is_valid_column(col):
            return
        
        # Human move
        self.game.human_move(col)
        self._draw_board()
        self._update_score()
        self.root.update()
        
        if self.game.is_game_over():
            self._show_game_over()
            return
        
        # AI move
        self.status.config(text="AI thinking...", fg='#FF4444')
        self.root.update()
        
        self.game.ai_move()
        self._draw_board()
        self._update_score()
        
        if self.game.is_game_over():
            self._show_game_over()
        else:
            self.status.config(text="Your turn (Yellow)", fg='#FFDD00')
    
    def _show_game_over(self):
        ai_score = self.game.ai_fours
        human_score = self.game.human_fours
        winner = self.game.get_winner()
        
        if winner == AI_PLAYER:
            msg = f"AI Wins!\nAI: {ai_score} vs You: {human_score}"
            color = '#FF4444'
        elif winner == HUMAN_PLAYER:
            msg = f"You Win!\nYou: {human_score} vs AI: {ai_score}"
            color = '#FFDD00'
        else:
            msg = f"Draw!\nBoth: {ai_score}"
            color = '#FFFFFF'
        
        self.status.config(text=msg.split('\n')[0], fg=color)
        messagebox.showinfo("Game Over", msg)
    
    def _restart_game(self):
        self.game.reset()
        self.status.config(text="Your turn (Yellow) - Fill the board!", fg='#FFDD00')
        self._update_score()
        self._draw_board()