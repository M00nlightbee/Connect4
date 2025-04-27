import numpy as np
import heapq
import random

class Connect4:
    def __init__(self):
        """Initialize a 6x7 Connect 4 board."""
        self.board = np.full((6, 7), " ")
        self.current_player = "●"  # Human starts first

    def display_board(self):
        """Display the current board."""
        for row in self.board:
            print(" | ".join(row))
            print("-" * 26)

    def get_available_moves(self):
        """Return a list of available columns (0-6) that are not full."""
        return [c for c in range(7) if self.board[0][c] == " "]  # Top row empty means column not full

    def make_move(self, col, player):
        """Place the player's mark in the lowest available row in the column."""
        for r in range(5, -1, -1):
            if self.board[r, col] == " ":
                self.board[r, col] = player
                return True
        return False  # Column full

    def check_winner(self, player, board=None):
        """Check if the given player has won."""
        if board is None:
            board = self.board

        # Horizontal
        for row in board:
            if any(list(row[i:i+4]) == [player]*4 for i in range(4)):
                return True

        # Vertical
        for c in range(7):
            for r in range(3):
                if all(board[r+i][c] == player for i in range(4)):
                    return True

        # Positive diagonal
        for r in range(3):
            for c in range(4):
                if all(board[r+i][c+i] == player for i in range(4)):
                    return True

        # Negative diagonal
        for r in range(3):
            for c in range(3, 7):
                if all(board[r+i][c-i] == player for i in range(4)):
                    return True

        return False

    def is_full(self):
        """Check if the board is full."""
        return all(self.board[0, c] != " " for c in range(7))

    def drop_piece(self, board, col, player):
        """Simulate dropping a piece in a column and return new board state."""
        new_board = np.copy(board)
        for r in range(5, -1, -1):
            if new_board[r, col] == " ":
                new_board[r, col] = player
                return new_board
        return None  # Column is full


class AStarAgent:
    def __init__(self, game):
        self.game = game
        self.human_player = "●"
        self.ai_player = "○"

    def evaluate_board(self, board):
        """Simple heuristic to value board positions."""
        if self.game.check_winner(self.ai_player, board):
            return 100
        if self.game.check_winner(self.human_player, board):
            return -100
        score = 0

        center_array = [board[r][3] for r in range(6)]
        center_count = center_array.count(self.ai_player)
        score += center_count * 3  # Prefer center column

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

                # Check if human's move results in a win
                human_state = self.game.drop_piece(board_state, col, self.human_player)
                if human_state is not None and self.game.check_winner(self.human_player, human_state):
                    return col  # Block human's winning move

                # Evaluate the board state
                score = self.evaluate_board(new_state)
                if score > best_score:
                    best_score = score
                    best_move = col

                heapq.heappush(open_list, (g + 1 - score, g + 1, col, tuple(map(tuple, new_state))))

        return best_move if best_move is not None else random.choice(self.game.get_available_moves())

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
            available_cols = game.get_available_moves()
            print(f"Available columns: {available_cols}")
            while True:
                try:
                    col = int(input("Enter column (0-6): "))
                    if col not in available_cols:
                        print("Column full or invalid. Try again.")
                        continue
                    break
                except (ValueError, IndexError):
                    print("Invalid input. Enter a number 0-6.")
            game.make_move(col, game.current_player)
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
        elif game.is_full():
            game.display_board()
            print("It's a draw!")
            break

        # Switch player
        game.current_player = "○" if game.current_player == "●" else "●"

if __name__ == "__main__":
    play_game()
