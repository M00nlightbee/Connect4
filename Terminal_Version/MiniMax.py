import random
import numpy as np
from Connect4 import Connect4

class MiniMax:
    def __init__(self, game):
        self.game = game
        self.opponent_player = "●"
        self.ai_player = "○"

    def minimax(self, board, depth, alpha, beta, is_maximizing, max_depth=5):
        """Minimax algorithm with Alpha-Beta pruning and Depth Limit."""
        if depth >= max_depth or self.game.check_winner(self.ai_player, board) or self.game.check_winner(self.opponent_player, board) or self.game.is_full(board):
            if self.game.check_winner(self.ai_player, board):
                return 10 - depth
            elif self.game.check_winner(self.opponent_player, board):
                return depth - 10
            elif self.game.is_full(board):
                return 0
            return 0  # Return 0 if max depth is reached and no winner

        if is_maximizing:
            max_eval = float('-inf')
            for col in self.game.get_available_moves(board):
                temp_board = self.game.drop_piece(board, col, self.ai_player)
                if temp_board is not None:
                    eval = self.minimax(temp_board, depth + 1, alpha, beta, False, max_depth)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for col in self.game.get_available_moves(board):
                temp_board = self.game.drop_piece(board, col, self.opponent_player)
                if temp_board is not None:
                    eval = self.minimax(temp_board, depth + 1, alpha, beta, True, max_depth)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
            return min_eval

    def best_move(self):
        """Determine the best move for the AI player using Minimax."""
        best_val = float('-inf')
        best_col = None

        available_moves = self.game.get_available_moves(self.game.board)
        print(f"Available moves for AI: {available_moves}")

        for col in available_moves:
            temp_board = self.game.drop_piece(self.game.board, col, self.ai_player)
            if temp_board is not None:
                move_val = self.minimax(temp_board, 0, float('-inf'), float('inf'), False)
                # print(f"Column: {col}, Move Value: {move_val}")  # Debugging
                if move_val > best_val:
                    best_val = move_val
                    best_col = col

        if best_col is None and available_moves:
            # Default: Choose a random valid column if no best move is found
            best_col = random.choice(available_moves)
            print(f"No optimal move found. Falling back to random column: {best_col}")

        print(f"Best move selected: {best_col}, Score: {best_val}")
        return best_col

    

def play_game():
    game = Connect4()
    agent = MiniMax(game)

    while True:
        game.display_board()

        if game.current_player == "●":
            # Human's turn
            print("Your turn!")
            available_cols = game.get_available_moves(game.board)
            print(f"Available columns: {available_cols}")
            while True:
                try:
                    col = int(input("Enter column (0-6): "))
                    if col in available_cols:
                        game.make_move(col, game.current_player)
                        break
                    else:
                        print("Invalid input. Try Again")
                except (ValueError, IndexError):
                    print("Invalid input. Enter a number between 0 and 6.")
        else:
            # AI's turn
            print("MiniMax AI's move:")
            col = agent.best_move()
            if col is not None:
                print(f"AI chooses column: {col}")
                game.make_move(col, game.current_player)
            else:
                print("MiniMax AI could not make a move!")
                break

        if game.check_winner("○"):
            game.display_board()
            print("MiniMax AI wins!")
            break
        elif game.check_winner("●"):
            game.display_board()
            print("You win!")
            break
        elif game.is_full(game.board):
            game.display_board()
            print("It's a draw!")
            break

        # Switch player
        game.current_player = "○" if game.current_player == "●" else "●"

if __name__ == "__main__":
    play_game()