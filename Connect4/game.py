from ai.alphabeta import alphabeta_decision
from board import Board
from constants import AI_PLAYER, HUMAN_PLAYER


class Game:
    def __init__(self, rows, cols, depth):
        self.board = Board(rows, cols)
        self.depth = depth
        self.game_over = False
        self.winner = None
        self.ai_fours = 0
        self.human_fours = 0

    def ai_move(self):
        if self.game_over:
            return None
        col = alphabeta_decision(self.board, self.depth)
        if col is not None:
            self.board.drop_piece(col, AI_PLAYER)
            self._check_game_end()
        return col

    def human_move(self, col):
        if self.game_over or not self.board.is_valid_column(col):
            return False
        self.board.drop_piece(col, HUMAN_PLAYER)
        self._check_game_end()
        return True

    def _check_game_end(self):
        """Game ends only when board is full. Winner has more 4-in-a-rows."""
        if self.board.is_full():
            self.game_over = True
            self.ai_fours = self.board.count_fours(AI_PLAYER)
            self.human_fours = self.board.count_fours(HUMAN_PLAYER)
            
            if self.ai_fours > self.human_fours:
                self.winner = AI_PLAYER
            elif self.human_fours > self.ai_fours:
                self.winner = HUMAN_PLAYER
            else:
                self.winner = None  # Draw

    def is_game_over(self):
        return self.game_over

    def get_winner(self):
        return self.winner

    def get_scores(self):

        return {
            'ai': self.board.count_fours(AI_PLAYER),
            'human': self.board.count_fours(HUMAN_PLAYER)
        }

    def reset(self):
        self.board = Board(self.board.rows, self.board.cols)
        self.game_over = False
        self.winner = None
        self.ai_fours = 0
        self.human_fours = 0