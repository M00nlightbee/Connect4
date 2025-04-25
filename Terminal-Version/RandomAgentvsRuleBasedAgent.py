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

# Define rule based agent
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

# Define random agent
def random_agent(board):
    empty_cells = [(row, col) for row in range(6) for col in range(7) if board[row][col] == " "]
    return random.choice(empty_cells)

def play_game():
    """Plays a game between the random agent and the rule-based agent."""
    board = [[" " for _ in range(7)] for _ in range(6)]
    players = ["●", "○"]
    current_player = 0  # 0 -> Random Agent (●), 1 -> Rule-Based Agent (○)

    print("Game Start!")
    display_board(board)

    while True:
        if current_player == 0:
            move = random_agent(board)
            print("\nRandom Agent (●) moves:", move)
        else:
            move = rule_based_agent(board)
            print("\nRule-Based Agent (○) moves:", move)

        # Make the move
        board[move[0]][move[1]] = players[current_player]

        # Display the board
        display_board(board)

        # Check for a winner or draw
        if check_winner(board, players[current_player]):
            print(f"\nPlayer {players[current_player]} wins!")
            break
        if is_full(board):
            print("\nIt's a draw!")
            break

        # Switch player
        current_player = 1 - current_player

# Start the game
play_game()
