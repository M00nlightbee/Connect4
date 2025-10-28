import numpy as np

class Connect4:
    def __init__(self):
        """Initialize a 6x7 Connect 4 board."""
        self.board = np.full((6, 7), " ")
        self.current_player = "●" 

    def display_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * 26)

    def get_available_moves(self, board):
        if board is None:
            board = self.board
        """Return a list of available columns (0-6) that are not full."""
        return [c for c in range(7) if board[0][c] == " "]

    # Make a move on the board
    def make_move(self, col, player):
        for r in range(5, -1, -1):
            if self.board[r, col] == " ":
                self.board[r, col] = player
                return True
        return False  # Column full
    
    # Drop piece into board
    def drop_piece(self, board, col, player):
        new_board = np.copy(board)
        for r in range(5, -1, -1):
            if new_board[r, col] == " ":
                new_board[r, col] = player
                return new_board
        return None  # Column is full

    # Check winning move
    def check_winner(self, player, board=None):
        if board is None:
            board = self.board

        # Check Horizontal
        for row in board:
            if any(list(row[i:i+4]) == [player]*4 for i in range(4)):
                return True

        # Check Vertical
        for c in range(7):
            for r in range(3):
                if all(board[r+i][c] == player for i in range(4)):
                    return True

        # Check Positive diagonal
        for r in range(3):
            for c in range(4):
                if all(board[r+i][c+i] == player for i in range(4)):
                    return True

        # Check Negative diagonal
        for r in range(3):
            for c in range(3, 7):
                if all(board[r+i][c-i] == player for i in range(4)):
                    return True

        return False

    def is_full(self, board):
        if board is None:
            board = self.board
        return all(board[0, c] != " " for c in range(7))