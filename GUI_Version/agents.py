import random
import numpy as np
import queue
import heapq
from connect4 import Connect4

class RandomAgent:
    # Instantiate class
    def __init__(self, game):
        self.game = game

    # Define random agent
    def random_agent_move(self, board):
        self.game.board = np.copy(board)  # Sync the board
        return random.choice(self.game.get_available_moves(board))
    

class RuleBasedAgent:
    # Instantiate class
    def __init__(self, game):
        self.game = game

    # Define rule based agent
    def rule_based_agent(self, board):
        self.game.board = np.copy(board)  # Sync the board

        # Rule 1: Win if possible
        for col in self.game.get_available_moves(board):
            new_board = self.game.drop_piece(self.game.board, col, "○")
            if new_board is not None and self.game.check_winner("○", board=new_board):
                return col  # Return the column to move

        # Rule 2: Block opponent win
        for col in self.game.get_available_moves(board):
            new_board = self.game.drop_piece(self.game.board, col, "●")
            if new_board is not None and self.game.check_winner("●", board=new_board):           
                return col  # Return the column to block the opponent's win

        # # Rule 3: Take center
        if self.game.board[0, 3] == " ":
            return 3

        # # Rule 4: Take corners
        corners = [0, 6]
        random.shuffle(corners)
        for col in corners:
            if self.game.board[0, col] == " ":
                return col

        # Rule 5: Random move
        return random.choice(self.game.get_available_moves(board))
    
class BFSAgent:
    def __init__(self, game):
        self.game = game
        self.visited_states = set()

    def bfs_ai_move(self, board, player, opponent):
        q = queue.Queue()
        q.put((board, None))

        self.visited_states.clear()  # Reset visited states for each move
        available_moves = self.game.get_available_moves(board)  # Get all valid columns

        print("\n--- BFS with Queue Search Process ---")

        while not q.empty():
            current_board, move = q.get()

            # Convert board to tuple to store in set(row and col)
            current_state = tuple(tuple(row) for row in current_board)
            if current_state in self.visited_states:
                continue  # Skip if already visited

            self.visited_states.add(current_state)

            # Get available moves
            available_moves = self.game.get_available_moves(current_board)

            # Check for a winning move
            for col in available_moves:        
                new_board = np.copy(current_board) 
                new_board = self.game.drop_piece(new_board, col, player)
                if new_board is not None:
                    if self.game.check_winner(player, board=new_board):
                        print(f"BFS with Queue AI's winning move at column: {col}")
                        return col
                    q.put((new_board, col))  # Add to BFS queue

            # Check for a blocking move
            for col in available_moves:
                new_board = np.copy(current_board)
                new_board = self.game.drop_piece(new_board, col, opponent)
                if new_board is not None:
                    if self.game.check_winner(opponent, board=new_board):
                        print(f"\nBFS with Queue AI blocks opponent's winning move at column: {col}")
                        return col

        # If no winning/blocking move, pick the first available move
        print(f"\nNo winning or blocking move found. \nBFS with Queue AI picks a RANDOM move at column: {col}\n")
        return random.choice(available_moves) if available_moves else None
    
class AStarAgent:
    # Instantiate class
    def __init__(self, game):
        self.game = game
        self.opponent_player = "●"
        self.ai_player = "○"

    def evaluate_board(self, board):
        """Evaluate the board state for A* search."""
        score = 0
        # Center column preference
        center_col = board[:, 3]
        score += np.count_nonzero(center_col == self.ai_player) * 3
        for row in range(6):
            for col in range(7 - 3):
                window = board[row, col:col+4]
                if np.count_nonzero(window == self.ai_player) == 3 and np.count_nonzero(window == " ") == 1:
                    score += 50
                elif np.count_nonzero(window == self.ai_player) == 2 and np.count_nonzero(window == " ") == 2:
                    score += 10
                # Penalize opponent
                if np.count_nonzero(window == self.opponent_player) == 3 and np.count_nonzero(window == " ") == 1:
                    score -= 40
        return score

    def a_star_search(self):
        open_list = []
        heapq.heappush(open_list, (0, 0, None, tuple(map(tuple, self.game.board))))
        best_move = None
        best_score = float('-inf')

        while open_list:
            f, g, move, state = heapq.heappop(open_list)
            board_state = np.array(state)

            valid_moves = [c for c in range(7) if board_state[0][c] == " "]
            for col in valid_moves:
                # AI's move
                new_state = self.game.drop_piece(board_state, col, self.ai_player)
                if new_state is None:
                    continue  # Invalid move

                # Check if this move results in a win for the AI
                if self.game.check_winner(self.ai_player, new_state):
                    return col  # Immediate win

                # Block opponent's winning move
                opponent_state = self.game.drop_piece(board_state, col, self.opponent_player)
                if opponent_state is not None and self.game.check_winner(self.opponent_player, opponent_state):
                    return col  # Block human's winning move

                # Evaluate the board state
                h = self.evaluate_board(new_state)
                # A* cost function: f(n) = g(n) + h(n)
                f_new = g + 1 + h

                if h > best_score:
                    best_score = h
                    best_move = col

                heapq.heappush(open_list, (f_new, g + 1, col, tuple(map(tuple, new_state))))

        available_moves = self.game.get_available_moves(board_state)
        return best_move if best_move is not None else (random.choice(available_moves) if available_moves else None)

    def best_move(self):
        move = self.a_star_search()
        print(f"AI selects column: {move}")
        return move
    
class MiniMax:
    def __init__(self, game):
        self.game = game
        self.opponent_player = "●"
        self.ai_player = "○"

    def chebyshev_distance_heuristic(self, board):
        """Evaluate the board using Chebyshev distance heuristic."""
        score = 0

        # Define directions for horizontal, vertical, and diagonal checks
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == self.ai_player:
                    # Evaluate AI's potential winning move
                    for dr, dc in directions:
                        count = 0
                        for i in range(4):  # Check up to 4 cells in the direction
                            r, c = row + dr * i, col + dc * i
                            if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == self.ai_player:
                                count += 1
                            else:
                                break
                        score += count ** 2 
                elif board[row][col] == self.opponent_player:
                    # Evaluate opponent's potential winning move
                    for dr, dc in directions:
                        count = 0
                        for i in range(4):  # Check up to 4 cells in the direction
                            r, c = row + dr * i, col + dc * i
                            if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == self.opponent_player:
                                count += 1
                            else:
                                break
                        score -= count ** 2
        # Blocking opponent's winning moves
        if self.game.check_winner(self.opponent_player, board):
            score -=1000

        return score

    def minimax(self, board, depth, alpha, beta, is_maximizing, max_depth=3):
        """Minimax algorithm with Alpha-Beta pruning and Chebyshev Distance Heuristic."""
        if depth >= max_depth or self.game.check_winner(self.ai_player, board) or self.game.check_winner(self.opponent_player, board) or self.game.is_full(board):
            if self.game.check_winner(self.ai_player, board):
                return 10 - depth
            elif self.game.check_winner(self.opponent_player, board):
                return depth - 10
            elif self.game.is_full(board):
                return 0
            return self.chebyshev_distance_heuristic(board)

        if is_maximizing:
            max_eval = float('-inf')
            for col in self.game.get_available_moves(board):
                temp_board = self.game.drop_piece(board, col, self.ai_player)
                if temp_board is not None:
                    eval = self.minimax(temp_board, depth + 1, alpha, beta, False, max_depth)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for col in self.game.get_available_moves(board):
                temp_board = self.game.drop_piece(board, col, self.opponent_player)
                if temp_board is not None:
                    eval = self.minimax(temp_board, depth + 1, alpha, beta, True, max_depth)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha cut-off
            return min_eval

    def best_move_minmax(self, board=None):
        """Determine the best move for the AI player using Minimax."""
        if board is None:
            board = self.game.board
        best_val = float('-inf')
        best_col = None

        available_moves = self.game.get_available_moves(board)

        # Check for immediate winning or blocking moves
        for col in available_moves:
            temp_board = self.game.drop_piece(board, col, self.ai_player)
            if temp_board is not None and self.game.check_winner(self.ai_player, temp_board):
                return col
            temp_board = self.game.drop_piece(board, col, self.opponent_player)
            if temp_board is not None and self.game.check_winner(self.opponent_player, temp_board):
                return col

        # Other moves
        for col in available_moves:
            temp_board = self.game.drop_piece(board, col, self.ai_player)
            if temp_board is not None:
                move_val = self.minimax(temp_board, 0, float('-inf'), float('inf'), False)
                if move_val > best_val:
                    best_val = move_val
                    best_col = col

        if best_col is None and available_moves:
            best_col = random.choice(available_moves)

        return best_col