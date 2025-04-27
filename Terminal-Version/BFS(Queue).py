import queue

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

# BFS Agent
def bfs_ai_move(board, player, opponent):
    q = queue.Queue()
    q.put((board, None))  # Start with the current board and no move yet

    visited_states = set()  # To store visited board states
    available_moves = get_available_moves(board)

    # Show all available moves before making a decision
    # print("\nAvailable moves before AI makes a move:")
    # for move in available_moves:
    #     print(f"Row: {move[0]}, Col: {move[1]}")

    print("\n--- BFS with Queue Search Process ---")

    while not q.empty():
        current_board, move = q.get()

        # Convert board to tuple (to store in set)
        current_state = tuple(tuple(row) for row in current_board)
        if current_state in visited_states:
            continue  # Skip if already visited

        visited_states.add(current_state)

        # print("\nEvaluating Board State:")
        # display_board(current_board)

        # Get available moves
        available_moves = get_available_moves(current_board)

        # Check for a winning move
        for move in available_moves:
            row, col = move
            new_board = [r[:] for r in current_board]
            new_board[row][col] = player

            if check_winner(new_board, player):
                print(f"\nAI chooses WINNING move: Row {row}, Col {col}")
                return row, col  # Return immediately if winning move found

            q.put((new_board, (row, col)))  # Add to BFS queue

        # Check for a blocking move
        for move in available_moves:
            row, col = move
            new_board = [r[:] for r in current_board]
            new_board[row][col] = opponent

            if check_winner(new_board, opponent):
                print(f"\nAI chooses BLOCKING move: Row {row}, Col {col}")
                return row, col  # Block opponent if they can win

    # If no winning/blocking move, pick first available move
    print("\nNo winning or blocking move found. AI picks a RANDOM move.")
    return available_moves[0] if available_moves else None

def play_game():
    board = [[" " for _ in range(7)] for _ in range(6)]
    players = ["●", "○"]
    current_player = players[0]

    while True:
        display_board(board)
        
        if current_player == "●":
            # Human player's turn
            while True:
                try:
                    row = int(input("Enter row (0-5): "))
                    col = int(input("Enter col (0-6): "))
                    
                    # Validate if the cell is empty
                    if board[row][col] != " ":
                        print("Cell is already occupied.")
                        continue                    
                    break  # Exit the loop if input is valid
                except (ValueError, IndexError):
                    print("Invalid input. Use numbers between 0-5 for row and 0-6 for column.")
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
            if(current_player):
                print(f"\nBFS with Queue Agent wins! {players[0]}")
            else:
                print(f"\nYou wins! {players[1]}")
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