# Not using queue data structure and more like the rule-based agent.

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
    available_moves = get_available_moves(board)  # Get all valid columns

    print("\n--- BFS without Queue Search Process ---")

    for col in available_moves:
        # AI's move
        new_board = [row[:] for row in board]  # Copy the current board state
        move = drop_piece(new_board, col, player)
        if move:
            row, _ = move
            # Check if this move wins the game for the AI
            if check_winner(new_board, player):
                print(f"AI's winning move: Row: {row}, Col: {col}")
                return col

        # Block their human winning move
        new_board = [row[:] for row in board]  # Reset the board copy
        move = drop_piece(new_board, col, opponent)
        if move:
            row, _ = move
            if check_winner(new_board, opponent):
                print(f"AI blocks opponent's winning move: Row: {row}, Column: {col}")
                return col

    # If no immediate winning or blocking move, choose the first available move
    print("No immediate winning or blocking move found. AI will make a move.")
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
                drop_piece(board, col, current_player)
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
    