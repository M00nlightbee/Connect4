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

# Define rule based agent
def rule_based_agent(board):
    # Rule 1: Check win move
    for col in get_available_moves(board):
        new_board = [row[:] for row in board]
        row, _ = drop_piece(new_board, col, "○")
        if check_winner(new_board, "○"):
            return drop_piece(board, col, "○")

    # Rule 2: Check block move
    for col in get_available_moves(board):
        new_board = [row[:] for row in board]
        row, _ = drop_piece(new_board, col, "●")
        if check_winner(new_board, "●"):
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

# Define random agent
def random_agent_move(board):
    """Randomly selects a valid column and drops a piece for the agent."""
    available_cols = get_available_moves(board)
    col = random.choice(available_cols)  # Randomly select a column from available ones
    row, col = drop_piece(board, col, "○")  # Drop the piece in the selected column
    return row, col

def play_game():
    """Plays a game between the random agent and the rule-based agent."""
    board = [[" " for _ in range(7)] for _ in range(6)]
    players = ["●", "○"]
    current_player = 0  # 0 -> Random Agent (●), 1 -> Rule-Based Agent (○)

    print("Game Start!")
    display_board(board)

    while True:
        if current_player == 0:
            move = random_agent_move(board)
            print("\nRandom Agent (●) moves:", move)
        else:
            move = rule_based_agent(board)
            print("\nRule-Based Agent (○) moves:", move)

        # Make the move
        board[move[0]][move[1]] = players[current_player]

        # Display the board
        display_board(board)

        if check_winner(board, players[current_player]):
            if(players[0] == players[current_player]):
                print(f"\nRandom Agent wins! {players[0]}")
            else:
                print(f"\nRule-Based Agent wins! {players[1]}")
            break

        if is_full(board):
            print("\nIt's a draw!")
            break

        # Switch player
        current_player = 1 - current_player

# Start the game
if __name__ == "__main__":
    play_game()
