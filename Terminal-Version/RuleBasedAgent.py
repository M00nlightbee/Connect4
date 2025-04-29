import random
import numpy as np
from Connect4 import Connect4

class RuleBasedAgent:
    # Instantiate class
    def __init__(self, game):
        self.game = game

    # Define rule based agent
    def rule_based_agent(self, board):
        # game = Connect4()
        self.game.board = np.copy(board)  # Sync the board

        # Rule 1: Win if possible
        for col in self.game.get_available_moves(board):
            new_board = self.game.drop_piece(self.game.board, col, "○")
            if new_board is not None and self.game.check_winner("○", board=new_board):
                return col  # Return the column to move

        # Rule 2: Block opponent win
        for col in self.game.get_available_moves(board):
            new_board = self.game.drop_piece(self.game.board, col, "●")
            if new_board is not None and self.game.check_winner("●", board=new_board):           
                return col  # Return the column to block the opponent's win

        # Rule 3: Take center
        # if game.board[0, 3] == " ":
        #     return 3

        # Rule 4: Take corners
        # corners = [0, 6]
        # random.shuffle(corners)
        # for col in corners:
        #     if game.board[0, col] == " ":
        #         return col

        # Rule 5: Random move
        return random.choice(self.game.get_available_moves(board))

def play_game():
    game = Connect4()
    rule_based = RuleBasedAgent(game)
    board = np.full((6, 7), " ")
    print("Welcome to Connect 4! You are '●' and the Rule-Based Agent is '○'.")

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
            # Rule Based AI's turn
            print("Rule Based AI's move:")
            col = rule_based.rule_based_agent(board)
            if col is not None:
                game.make_move(col, game.current_player)
                board = game.board  # Sync the board
            else:
                print("AI could not make a move!")
                break

        if game.check_winner("○"):
            game.display_board()
            print("Rule Based Agent AI wins!")
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
