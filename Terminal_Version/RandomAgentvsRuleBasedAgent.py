import random
import numpy as np
from Connect4 import Connect4
from RandomAgent import RandomAgent
from RuleBasedAgent import RuleBasedAgent

def play_game():
    game = Connect4()
    random_agent = RandomAgent(game)
    rule_based = RuleBasedAgent(game)
    board = np.full((6, 7), " ")

    while True:
        game.display_board()
        available_cols = game.get_available_moves(board)
        print(f"Available columns: {available_cols}")

        if game.current_player == "●":
            # Random Agent AI's turn
            print("Random Agent turn!")
            col = random_agent.random_agent_move(board)
            if col is not None:
                game.make_move(col, game.current_player)
                board = game.board  # Sync the board
            else:
                print("AI could not make a move!")
                break           
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
            print("Rule Based AI wins!")
            break
        elif game.check_winner("●"):
            game.display_board()
            print("Random Agent AI wins!")
            break
        elif game.is_full(board):
            game.display_board()
            print("It's a draw!")
            break

        # Switch player
        game.current_player = "○" if game.current_player == "●" else "●"

if __name__ == "__main__":
    play_game()
