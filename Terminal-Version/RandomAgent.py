import random

def display_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 26)

def check_winner(board, player):
    # Check horizontal
    for row in board:
        if any(row[i:i+4] == [player]*4 for i in range(len(row) - 3)):
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

# Function to get a random move from the Random Agent
def random_agent_move(board):
    empty_cells = [(row, col) for row in range(6) for col in range(7) if board[row][col] == " "]
    return random.choice(empty_cells)


def play_game():
    board = [[" " for _ in range(7)] for _ in range(6)]
    print("Welcome to Connect 4! You are '●' and the Rule-Based Agent is '○'.")
    display_board(board)

    while True:
        # Player move
        while True:
            try:
                row, col = map(int, input("Enter your move (row and column, separated by space, e.g., '0 1'): ").split())
                if board[row][col] == " ":
                    board[row][col] = "●"
                    break
                print("Cell already taken. Try again.")
            except (ValueError, IndexError):
                print("Invalid input. Use numbers between 0-5 for row and 0-6 for column.")

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
        board[row][col] = "○"
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
play_game()