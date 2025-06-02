# Mini-Max Agent vs ML Agent

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ML import MLAgent

import time
from Connect4 import Connect4
from MiniMax import MiniMax
from ML import MLAgent

def play_game(verbose=True):
    game = Connect4()
    minimax_agent = MiniMax(game)
    ml_agent = MLAgent(game)

    while True:
        if verbose:
            game.display_board()
            available_cols = game.get_available_moves(game.board)
            print(f"Available columns: {available_cols}")

        if game.current_player == "●":
            col = minimax_agent.best_move()
            if verbose:
                print("MiniMax AI's turn")
                print(f"MiniMax AI chooses column: {col}")
        else:
            col = ml_agent.choose_move(game)
            if verbose:
                print("ML Agent's turn")
                print(f"ML Agent chooses column: {col}")

        if col is None:
            return "draw"

        game.make_move(col, game.current_player)

        if game.check_winner("○"):
            return "ml_agent"
        elif game.check_winner("●"):
            return "minimax"
        elif game.is_full(game.board):
            return "draw"

        game.current_player = "○" if game.current_player == "●" else "●"

if __name__ == "__main__":
    start_time = time.time()
    minimax_wins = 0
    ml_agent_wins = 0
    draws = 0
    total_games = 1

    # Initialize the MLAgent
    ml_agent = MLAgent()

    # Explicitly call the load_model function
    ml_agent.load_model()

    # Check if the model is loaded; if not, exit with an error message
    if ml_agent.model is None or ml_agent.scaler is None:
        print("Error: Pre-trained model or scaler not found. Please train the model first.")
        exit(1)  # Exit the program if the model is not loaded

    # Play the games
    for i in range(total_games):
        game_result = play_game()
        if game_result == "minimax":
            minimax_wins += 1
        elif game_result == "ml_agent":
            ml_agent_wins += 1
        else:
            draws += 1

    end_time = time.time()
    duration = end_time - start_time

    print("----ML Agent vs MiniMax Agent----")
    print(f"\nResults after {total_games} games:")
    print(f"MiniMax Agent wins: {minimax_wins}")
    print(f"ML Agent wins: {ml_agent_wins}")
    print(f"Draws: {draws}")
    print(f"Total time taken: {duration:.2f} seconds")