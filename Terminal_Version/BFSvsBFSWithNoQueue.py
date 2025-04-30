from Connect4 import Connect4
from BFSWithNoQueue import BFSNoQueue
from BFS import BFSAgent


def play_game():
    game = Connect4()
    bfs_without_Queue = BFSNoQueue(game)
    bfs = BFSAgent(game)

    while True:
        game.display_board()
        available_cols = game.get_available_moves(game.board)
        print(f"Available columns: {available_cols}")

        if game.current_player == "●":
            # BFS without Queue AI's turn
            print("BFS without Queue Agent turn!")
            col = bfs_without_Queue.bfs_ai_move(game.board, player="○", opponent="●")
            if col is not None:
                game.make_move(col, game.current_player)
            else:
                print("BFS without Queue could not make a move!")
                break           
        else:
            # BFS Agent AI's turn
            print("BFS Agent move:")
            col = bfs.bfs_ai_move(game.board, player="○", opponent="●")
            if col is not None:
                game.make_move(col, game.current_player)
            else:
                print("BFS Agent could not make a move!")
                break

        if game.check_winner("○"):
            game.display_board()
            print("BFS Agent wins!")
            break
        elif game.check_winner("●"):
            game.display_board()
            print("BFS without Queue Agent AI wins!")
            break
        elif game.is_full(game.board):
            game.display_board()
            print("It's a draw!")
            break

        # Switch player
        game.current_player = "○" if game.current_player == "●" else "●"

# Start the game
if __name__ == "__main__":
    play_game()

