import random

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

# Rule based Agent
def rule_based_agent(board):
    # Rule 1: Check win move
    for col in get_available_moves(board):
        temp_board = [row[:] for row in board]
        row, _ = drop_piece(temp_board, col, "○")
        if check_winner(temp_board, "○"):
            return drop_piece(board, col, "○")

    # Rule 2: Check block move
    for col in get_available_moves(board):
        temp_board = [row[:] for row in board]
        row, _ = drop_piece(temp_board, col, "●")
        if check_winner(temp_board, "●"):
            return drop_piece(board, col, "○")

    # Rule 3: Take center column
    if board[0][3] == " ":
        return drop_piece(board, 3, "○")

    # Rule 4: Take corners
    corners = [0, 6]
    random.shuffle(corners)
    for col in corners:
        if board[0][col] == " ":
            return drop_piece(board, col, "○")

    # Rule 5: Default to random move
    col = random.choice(get_available_moves(board))
    return drop_piece(board, col, "○")

def play_game():
    board = [[" " for _ in range(7)] for _ in range(6)]
    print("Welcome to Connect 4! You are '●' and the Rule-Based Agent is '○'.")
    display_board(board)

    while True:
        # Player move
        while True:
            try:
                col = int(input("Enter your move (column 0-6): "))
                if col in get_available_moves(board):
                    drop_piece(board, col, "●")
                    break
                print("Column full or invalid. Try again.")
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

        # Rule-Based Agent move
        row, col = rule_based_agent(board)
        print(f"Rule-Based Agent placed '○' at ({row}, {col})")
        display_board(board)

        # Check if the agent wins
        if check_winner(board, "○"):
            print("Rule-Based Agent wins! Better luck next time.")
            break

        # Check for a draw
        if is_full(board):
            print("It's a draw!")
            break

# Start the game
if __name__ == "__main__":
    play_game()
