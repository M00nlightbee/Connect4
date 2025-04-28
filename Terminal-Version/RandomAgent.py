import random

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

# Function to get a random move from the Random Agent
def random_agent_move(board):
    """Randomly selects a valid column and drops a piece for the agent."""
    available_cols = get_available_moves(board)
    col = random.choice(available_cols)  # Randomly select a column from available ones
    row, col = drop_piece(board, col, "○")  # Drop the piece in the selected column
    return row, col


def play_game():
    board = [[" " for _ in range(7)] for _ in range(6)]
    print("Welcome to Connect 4! You are '●' and the Rule-Based Agent is '○'.")
    display_board(board)

    while True:
        available_cols = get_available_moves(board)
        print(f"Available columns: {available_cols}")
        # Player move
        while True:
            try:
                col = int(input("Enter your move (column 0-6): "))
                if col in available_cols:
                    drop_piece(board, col, "●")
                    break
                else:
                    print("Invalid input. Try Again")
            except (ValueError, IndexError):
                print("Invalid input. Enter a number between 0 and 6.")

        display_board(board)

        # Check if player wins
        if check_winner(board, "●"):
            print("Congratulations! You win!")
            break

        # Check for a draw
        if is_full(board):
            print("It's a draw!")
            break

        # random Agent move
        row, col = random_agent_move(board)
        # board[row][col] = "○"
        print(f"Random Agent placed '○' at ({row}, {col})")
        display_board(board)

        # Check if the agent wins
        if check_winner(board, "○"):
            print("Random Agent wins! Better luck next time.")
            break

        # Check for a draw
        if is_full(board):
            print("It's a draw!")
            break

# Start the game
if __name__ == "__main__":
    play_game()