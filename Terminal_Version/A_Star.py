import numpy as np
import heapq
import random
from Connect4 import Connect4

class AStarAgent:
    # Instantiate class
    def __init__(self, game):
        self.game = game
        self.opponent_player = "●"
        self.ai_player = "○"

    def evaluate_board(self, board):
        """Heuristic function: Assigns a score to the board state."""
        if self.game.check_winner(self.ai_player, board):
            return 100
        if self.game.check_winner(self.opponent_player, board):
            return -100
        score = 0

        # Center position
        if board[0, 3] == self.ai_player:
            score += 50
        
        # Corners positions
        corners = [0, 6]
        for col in corners:
            if board[0, col] == self.ai_player:
                score += 20



        return score

    def a_star_search(self):
        open_list = []
        heapq.heappush(open_list, (0, 0, None, tuple(map(tuple, self.game.board))))
        best_move = None
        best_score = float('-inf')

        while open_list:
            f, g, move, state = heapq.heappop(open_list)
            board_state = np.array(state)

            valid_moves = [c for c in range(7) if board_state[0][c] == " "]
            for col in valid_moves:
                # AI's move
                new_state = self.game.drop_piece(board_state, col, self.ai_player)
                if new_state is None:
                    continue  # Invalid move

                # Check if this move results in a win for the AI
                if self.game.check_winner(self.ai_player, new_state):
                    return col  # Immediate win

                # Block opponent's winning move
                opponent_state = self.game.drop_piece(board_state, col, self.opponent_player)
                if opponent_state is not None and self.game.check_winner(self.opponent_player, opponent_state):
                    return col  # Block human's winning move

                # Evaluate the board state
                h = self.evaluate_board(new_state)
                # A* cost function: f(n) = g(n) + h(n)
                f_new = g + 1 + h

                if h > best_score:
                    best_score = h
                    best_move = col

                heapq.heappush(open_list, (f_new, g + 1, col, tuple(map(tuple, new_state))))

        available_moves = self.game.get_available_moves(board_state)
        return best_move if best_move is not None else (random.choice(available_moves) if available_moves else None)

    def best_move(self):
        move = self.a_star_search()
        print(f"AI selects column: {move}")
        return move


def play_game():
    game = Connect4()
    agent = AStarAgent(game)

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
            print("AI's move:")
            col = agent.best_move()
            if col is not None:
                game.make_move(col, game.current_player)
            else:
                print("AI could not make a move!")
                break

        if game.check_winner("○"):
            game.display_board()
            print("AI wins!")
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
