def evaluate_window(window, ai_player, human_player):
    """Evaluate 4-cell window."""
    pass

def compute_heuristic(board):
    """Return heuristic score for board."""
    pass


# 4. ai/heuristic.py

# Compute heuristic values for board evaluation.

# evaluate_window(window, ai_player, human_player)

# Input: 4 consecutive cells (window).

# Count how many AI pieces, how many human pieces, and empty spots.

# Assign score:

# High positive if AI is close to winning.

# High negative if human is close to winning.

# Small positive/negative for 2-in-a-row.

# Return numeric score.

# compute_heuristic(board)

# Loop through the entire board.

# Horizontal windows of 4 cells.

# Vertical windows of 4 cells.

# Diagonal windows (both directions).

# For each window, call evaluate_window() → get score.

# Sum all scores → final heuristic for the board.

# Return final score.