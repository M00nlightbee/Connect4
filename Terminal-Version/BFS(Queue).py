import queue

def display_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 26)

def check_winner(board, player):
    # Check Horizontal
    for row in board:
        if any(list(row[i:i+4]) == [player]*4 for i in range(4)):
            return True

    # Check Vertical
    for c in range(7):
        for r in range(3):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    # Check Positive diagonal
    for r in range(3):
        for c in range(4):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True

    # Check Negative diagonal
    for r in range(3):
        for c in range(3, 7):
            if all(board[r+i][c-i] == player for i in range(4)):
                return True
    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def get_available_moves(board):
    """Return a list of available columns (0-6) that are not full."""
    return [col for col in range(7) if board[0][col] == " "]  # Top row empty means column not full

def drop_piece(board, col, player):
    """Drop a piece into the lowest available row in the specified column."""
    for row in range(5, -1, -1):  # Start from the bottom row
        if board[row][col] == " ":
            board[row][col] = player
            return row, col
    return None  # Column is full

# BFS Agent
def bfs_ai_move(board, player, opponent):
    q = queue.Queue()
    q.put((board, None))  # Start with the current board and no move yet

    visited_states = set()  # To store visited board states
    available_moves = get_available_moves(board)

    print("\n--- BFS with Queue Search Process ---")

    while not q.empty():
        current_board, move = q.get()

        # Convert board to tuple (to store in set)
        current_state = tuple(tuple(row) for row in current_board)
        if current_state in visited_states:
            continue  # Skip if already visited

        visited_states.add(current_state)

        # Get available moves
        available_moves = get_available_moves(current_board)

        # Check for a winning move
        for col in available_moves:
            new_board = [r[:] for r in current_board]
            drop_result = drop_piece(new_board, col, player)
            if drop_result:
                row, col = drop_result  # Unpack the result
                if check_winner(new_board, player):
                    print(f"\nBFS with Queue chooses WINNING move: Row ({row}), Column ({col})")
                    return col  # Return the column of the winning move

            q.put((new_board, col))  # Add to BFS queue

        # Check for a blocking move
        for col in available_moves:
            new_board = [r[:] for r in current_board]
            drop_result = drop_piece(new_board, col, opponent)
            if drop_result:
                row, col = drop_result  # Unpack the result
                if check_winner(new_board, opponent):
                    print(f"\nBFS with Queue chooses BLOCKING move: Row ({row}), Column ({col})")
                    return col  # Return the column of the blocking move

    # If no winning/blocking move, pick the first available move
    print("\nNo winning or blocking move found. BFS with Queue AI picks a RANDOM move.")
    return available_moves[0] if available_moves else None

def play_game():
    board = [[" " for _ in range(7)] for _ in range(6)]
    players = ["●", "○"]
    current_player = players[0]

    while True:
        display_board(board)        
        if current_player == "●":
            available_cols = get_available_moves(board)
            # Human player's turn
            while True:
                try:
                    col = int(input("Enter your move (column 0-6): "))
                    if col in available_cols:
                        drop_piece(board, col, current_player)
                        break
                    else:
                        print("Invalid input. Try Again")
                except (ValueError, IndexError):
                    print("Invalid input. Enter a number between 0 and 6.")
        else:
            # AI's turn
            print("\nAI is thinking...")
            col = bfs_ai_move(board, current_player, players[0])  # Pass opponent as the human player

            if col is not None:
                drop_piece(board, col, current_player)  # Apply the move on the actual board
            else:
                print("No valid moves available!")
                break

        if check_winner(board, current_player):
            display_board(board)
            if current_player == "●":
                print(f"You Win! {current_player}")
            else:
                print(f"AI Wins! {current_player}")
            break
        elif is_full(board):
            display_board(board)
            print("It's a draw!")
            break
        # Switch players
        current_player = "○" if current_player == "●" else "●"

# Start the game
if __name__ == "__main__":
    play_game()