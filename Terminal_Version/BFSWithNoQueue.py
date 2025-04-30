import random
import numpy as np
from Connect4 import Connect4

class BFSNoQueue:
    def __init__(self, game):
        self.game = game

    def bfs_ai_move(self, board, player, opponent):
        available_moves = self.game.get_available_moves(board)  # Get all valid columns

        print("\n--- BFS without Queue Search Process ---")

        for col in available_moves:
            # AI's move
            new_board = np.copy(board) 
            new_board = self.game.drop_piece(new_board, col, player)
            if new_board is not None:
                if self.game.check_winner(player, board=new_board):
                    print(f"BFS without queue AI's winning move at column: {col}")
                    return col

            # Block the opponent move
            new_board = np.copy(board)
            new_board = self.game.drop_piece(new_board, col, opponent)
            if new_board is not None:
                if self.game.check_winner(opponent, board=new_board):
                    print(f"BFS without queue AI blocks opponent's winning move at column: {col}")
                    return col

        # No immediate win or block — pick the first available move
        print("No immediate winning or blocking move found. BFS without queue AI picks a RANDOM move.")
        return random.choice(available_moves) if available_moves else None 

def play_game():
    game = Connect4()
    bfs_no_queue = BFSNoQueue(game)

    print("Welcome to Connect 4! You are '●' and the BFS without queue Agent is '○'.")

    while True:
        game.display_board()
        available_cols = game.get_available_moves(game.board)
        print(f"Available columns: {available_cols}")

        if game.current_player == "●":
            # Human player's move
            while True:
                try:
                    col = int(input("Enter your move (column 0-6): "))
                    if col in available_cols:
                        game.make_move(col, game.current_player)
                        break
                    else:
                        print("Invalid move. Column is full or invalid number.")
                except (ValueError, IndexError):
                    print("Invalid input. Enter a number between 0 and 6.")
        else:
            # AI's move
            print("BFS without queue AI's move:")
            col = bfs_no_queue.bfs_ai_move(game.board, player="○", opponent="●")
            if col is not None:
                game.make_move(col, game.current_player)
            else:
                print("BFS without queue AI could not make a move!")
                break

        # Check for a win or draw
        if game.check_winner("○"):
            game.display_board()
            print("BFS without queue Agent wins!")
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
