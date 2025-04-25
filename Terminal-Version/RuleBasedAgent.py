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

def get_available_moves(board):
    return [(row, col) for row in range(6) for col in range(7) if board[row][col] == " "]

def rule_based_agent(board):
    # Rule 1 Check win move
    for row, col in get_available_moves(board):
        board[row][col] = "○"
        if check_winner(board, "○"):
            return row, col
        board[row][col] = " "

    # Rule 2 Check block move
    for row, col in get_available_moves(board):
        board[row][col] = "●"
        if check_winner(board, "●"):
            board[row][col] = "○"
            return row, col
        board[row][col] = " "

    # Rule 3 take center space
    if board[2][3] == " ":
        return 2, 3
    
    # Rule 4 take corners
    corners = [(0, 0), (0, 6), (5, 0), (5, 6)]
    random.shuffle(corners)
    for row, col in corners:
        if board[row][col] == " ":
            return row, col
        
    # Rule 5
    return random.choice(get_available_moves(board))

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

        # Rule-Based Agent move
        row, col = rule_based_agent(board)
        board[row][col] = "○"
        print(f"Agent placed '○' at ({row}, {col})")
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
play_game()
