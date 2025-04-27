# Not using queue data structure and more like the rule-based agent.

def display_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 26)

def check_winner(board, player):
    # Check horizontal
    for row in board:
        if any(list(row[i:i+4]) == [player]*4 for i in range(4)):
            return True

    # Check vertical
    for col in range(7):
        if any(all(board[row+i][col] == player for i in range(4)) for row in range(3)):
            return True

    # Check diagonals
    for row in range(3):
        for col in range(4):
            if all(board[row+i][col+i] == player for i in range(4)) or \
               all(board[row+i][col+3-i] == player for i in range(4)):
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
    available_moves = []
    for col in range(7):  # Iterate over columns instead of rows
        for row in range(5, -1, -1):  # Start from the bottom row
            if board[row][col] == " ":
                available_moves.append((row, col))
                break  # Only the lowest empty row in the column is valid

    print("Available moves before the AI makes a move:")
    for move in available_moves:
        print(f"Row: {move[0]}, Col: {move[1]}")

    for move in available_moves:
        row, col = move
        # Copy the current board state
        new_board = [row[:] for row in board]
        new_board[row][col] = player

        # Check if this move wins the game for the AI
        if check_winner(new_board, player):
            print(f"AI's winning move: Row: {row}, Col: {col}")
            return row, col

        # Check if this move blocks the opponent from winning
        new_board[row][col] = opponent
        if check_winner(new_board, opponent):
            print(f"AI blocks opponent's winning move: Row: {row}, Col: {col}")
            return row, col

    # If no immediate winning or blocking move, choose a move to proceed
    print("No immediate winning or blocking move found. AI will make a move.")
    return available_moves[0]  # Randomly select the first available move

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
                    col = int(input("Enter column (0-6): "))
                    if col not in available_cols:
                        print("Column full or invalid. Try again.")
                        continue
                    break
                except (ValueError, IndexError):
                    print("Invalid input. Enter a number 0-6.")
        else:
            # AI's turn
            print("\nAI is thinking...")
            move = bfs_ai_move(board, current_player, players[0])  # Pass opponent as the human player

            if move:
                row, col = move
            else:
                print("No valid moves available!")
                break

        # Make the move if valid
        if board[row][col] == " ":
            board[row][col] = current_player
        else:
            print("Invalid move! Try again.")
            continue

        # Check for win or draw
        if check_winner(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_full(board):
            display_board(board)
            print("It's a draw!")
            break

        # Switch players
        current_player = "○" if current_player == "●" else "●"

# Start the game
if __name__ == "__main__":
    play_game()
    