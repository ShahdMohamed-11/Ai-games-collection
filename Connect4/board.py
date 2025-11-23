import copy
from constants import EMPTY, AI_PLAYER, HUMAN_PLAYER


class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]

    def drop_piece(self, col, player):
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == EMPTY:
                self.grid[row][col] = player
                return row
        return -1

    def is_valid_column(self, col):
        return 0 <= col < self.cols and self.grid[0][col] == EMPTY

    def get_valid_moves(self):
        return [col for col in range(self.cols) if self.is_valid_column(col)]

    def count_fours(self, player):
        
        count = 0
        
        # horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if all(self.grid[row][col + i] == player for i in range(4)):
                    count += 1
        
        # vertical
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if all(self.grid[row + i][col] == player for i in range(4)):
                    count += 1
        
        # diagonal /
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if all(self.grid[row - i][col + i] == player for i in range(4)):
                    count += 1
        
        # diagonal \
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if all(self.grid[row + i][col + i] == player for i in range(4)):
                    count += 1
        
        return count

    def check_winner(self, player):
        """Check if player has at least one 4-in-a-row (used during game for AI)."""
        return self.count_fours(player) > 0

    def is_full(self):
        return all(self.grid[0][col] != EMPTY for col in range(self.cols))

    def copy(self):
        new_board = Board(self.rows, self.cols)
        new_board.grid = copy.deepcopy(self.grid)
        return new_board