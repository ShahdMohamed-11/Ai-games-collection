import tkinter as tk
from gui.menu import MainMenuGUI
from gui.game_screen import GameScreenGUI
from game import Game
from constants import ROWS, COLUMNS, BG_COLOR

class Connect4App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4 - AI Game")
        self.root.configure(bg=BG_COLOR)
        
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.root.geometry(f"{int(screen_w*0.8)}x{int(screen_h*0.8)}")

        self.menu_screen = MainMenuGUI(self.root, self)
        self.game_screen = GameScreenGUI(self.root, self)
        self.current_screen = None

    def show_menu(self):
        if self.current_screen:
            self.current_screen.hide()
        self.current_screen = self.menu_screen
        self.menu_screen.show()

    def start_game(self, rows, cols, depth, ai_func):
        if self.current_screen:
            self.current_screen.hide()
        game = Game(rows, cols, depth, ai_func)
        self.game_screen.set_game(game)
        self.current_screen = self.game_screen
        self.game_screen.show()

    def run(self):
        self.show_menu()
        self.root.mainloop()

# -------------------- Run Application --------------------
if __name__ == "__main__":
    app = Connect4App()
    app.run()