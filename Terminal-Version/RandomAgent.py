import random
import numpy as np
from Connect4 import Connect4

class RandomAgent:
    # Instantiate class
    def __init__(self, game):
        self.game = game

    # Define random agent
    def random_agent_move(self, board):
        self.game.board = np.copy(board)  # Sync the board
        return random.choice(self.game.get_available_moves(board))

def play_game():
    game = Connect4()
    random_agent = RandomAgent(game)
    board = np.full((6, 7), " ")
    print("Welcome to Connect 4! You are '●' and the Random Agent is '○'.")

    while True:
        game.display_board()
        available_cols = game.get_available_moves(board)
        print(f"Available columns: {available_cols}")

        if game.current_player == "●":
            # Player move
            while True:
                try:
                    col = int(input("Enter your move (column 0-6): "))
                    if col in available_cols:
                        game.make_move(col, game.current_player)
                        break
                    else:
                        print("Invalid input. Try Again")
                except (ValueError, IndexError):
                    print("Invalid input. Enter a number between 0 and 6.")
        else:
            # Random Agent AI's turn
            print("Random Agent AI's move:")
            col = random_agent.random_agent_move(board)
            if col is not None:
                game.make_move(col, game.current_player)
                board = game.board  # Sync the board
            else:
                print("AI could not make a move!")
                break

        if game.check_winner("○"):
            game.display_board()
            print("Random Agent AI wins!")
            break
        elif game.check_winner("●"):
            game.display_board()
            print("You win!")
            break
        elif game.is_full(board):
            game.display_board()
            print("It's a draw!")
            break

        # Switch player
        game.current_player = "○" if game.current_player == "●" else "●"

# Start the game
if __name__ == "__main__":
    play_game()