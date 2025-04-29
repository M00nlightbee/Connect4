import random
import numpy as np
import queue
from Connect4 import Connect4

# BFS Agent
class BFSAgent:
    def __init__(self, game):
        self.game = game
        self.visited_states = set()

    def bfs_ai_move(self, board, player, opponent):
        q = queue.Queue()
        q.put((board, None))

        self.visited_states.clear()  # Reset visited states for each move
        available_moves = self.game.get_available_moves(board)  # Get all valid columns

        print("\n--- BFS with Queue Search Process ---")

        while not q.empty():
            current_board, move = q.get()

            # Convert board to tuple (to store in set)
            current_state = tuple(tuple(row) for row in current_board)
            if current_state in self.visited_states:
                continue  # Skip if already visited

            self.visited_states.add(current_state)

            # Get available moves
            available_moves = self.game.get_available_moves(current_board)

            # Check for a winning move
            for col in available_moves:        
                new_board = np.copy(current_board) 
                new_board = self.game.drop_piece(new_board, col, player)
                if new_board is not None:
                    if self.game.check_winner(player, board=new_board):
                        print(f"BFS with Queue AI's winning move at column: {col}")
                        return col
                    q.put((new_board, col))  # Add to BFS queue

            # Check for a blocking move
            for col in available_moves:
                new_board = np.copy(current_board)
                new_board = self.game.drop_piece(new_board, col, opponent)
                if new_board is not None:
                    if self.game.check_winner(opponent, board=new_board):
                        print(f"\nBFS with Queue AI blocks opponent's winning move at column: {col}")
                        return col

        # If no winning/blocking move, pick the first available move
        print(f"\nNo winning or blocking move found. \nBFS with Queue AI picks a RANDOM move at column: {col}\n")
        return random.choice(available_moves) if available_moves else None

def play_game():
    game = Connect4()
    bfs_queue = BFSAgent(game)

    print("Welcome to Connect 4! You are '●' and the BFS with queue Agent is '○'.")

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
            print("BFS with queue AI's move:")
            col = bfs_queue.bfs_ai_move(game.board, player="○", opponent="●")
            if col is not None:
                game.make_move(col, game.current_player)
            else:
                print("BFS with queue AI could not make a move!")
                break

        # Check for a win or draw
        if game.check_winner("○"):
            game.display_board()
            print("BFS with queue Agent wins!")
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

# Start the game
if __name__ == "__main__":
    play_game()