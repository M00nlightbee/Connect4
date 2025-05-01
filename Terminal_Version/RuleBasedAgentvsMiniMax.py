# Smart (Rule-based) agent vs mini-max agent. 

import time
import random
import numpy as np
from Connect4 import Connect4
from RuleBasedAgent import RuleBasedAgent
from MiniMax import MiniMax

def play_game(verbose=False):
    game = Connect4()
    minimax_agent = MiniMax(game)
    rule_based = RuleBasedAgent(game)

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
            col = rule_based.rule_based_agent(game.board)
            if verbose:
                print("Rule Based AI's turn")
                print(f"Rule Based AI chooses column: {col}")

        if col is None:
            return "draw"

        game.make_move(col, game.current_player)

        if game.check_winner("○"):
            return "rule_based"
        elif game.check_winner("●"):
            return "minimax"
        elif game.is_full(game.board):
            return "draw"

        game.current_player = "○" if game.current_player == "●" else "●"

if __name__ == "__main__":
    start_time = time.time()
    minimax_wins = 0
    rule_based_wins = 0
    draws = 0
    total_games = 100

    for i in range(total_games):
        game_result = play_game()
        if game_result == "minimax":
            minimax_wins += 1
        elif game_result == "rule_based":
            rule_based_wins += 1
        else:
            draws += 1
        if (i + 1) % 50 == 0:
            print(f"Completed {i + 1} games...")

    end_time = time.time()
    duration = end_time - start_time

    print("----Smart (Rule-based) agent vs mini-max agent----")
    print(f"\nResults after {total_games} games:")
    print(f"MiniMax Agent wins: {minimax_wins}")
    print(f"Rule-Based Agent wins: {rule_based_wins}")
    print(f"Draws: {draws}")
    print(f"Total time taken: {duration:.2f} seconds")