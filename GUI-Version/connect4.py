import random

ROW_COUNT = 6
COL_COUNT = 7


def create_board():
    return [[" " for _ in range(COL_COUNT)] for _ in range(ROW_COUNT)]

def is_valid_location(board, col):
    return board[0][col] == " "

def get_next_open_row(board, col):
    for r in reversed(range(ROW_COUNT)):
        if board[r][col] == " ":
            return r

def check_winner(board, player):
    # Horizontal
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT - 3):
            if all(board[r][c+i] == player for i in range(4)):
                return True
    # Vertical
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True
    # Diagonal / and \
    for r in range(ROW_COUNT - 3):
        for c in range(COL_COUNT - 3):
            if all(board[r+i][c+i] == player for i in range(4)) or all(board[r+3-i][c+i] == player for i in range(4)):
                return True
    return False

def rule_based_agent(board):
    for col in range(COL_COUNT):
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            board[row][col] = "O"
            if check_winner(board, "O"):
                return row, col
            board[row][col] = " "
    for col in range(COL_COUNT):
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            board[row][col] = "X"
            if check_winner(board, "X"):
                board[row][col] = "O"
                return row, col
            board[row][col] = " "
    if is_valid_location(board, 3):
        return get_next_open_row(board, 3), 3
    for col in [0, 6, 1, 5, 2, 4]:
        if is_valid_location(board, col):
            return get_next_open_row(board, col), col
    available = [col for col in range(COL_COUNT) if is_valid_location(board, col)]
    col = random.choice(available)
    return get_next_open_row(board, col), col

# --- Pygame Version ---
# import pygame

# SQUARESIZE = 100
# RADIUS = int(SQUARESIZE / 2 - 5)

# BLUE = (0, 0, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# YELLOW = (255, 255, 0)
# WHITE = (255,255,255)

# pygame.init()
# width = COL_COUNT * SQUARESIZE
# height = (ROW_COUNT + 1) * SQUARESIZE
# size = (width, height)
# screen = pygame.display.set_mode(size)
# font = pygame.font.SysFont("monospace", 45)

# fontTitle = pygame.font.SysFont("monospace", 35)
# title = fontTitle.render("Welcome to Connect 4!.", True, WHITE)
# screen.blit(title, (20, 20))

# def draw_board(board):
#     for c in range(COL_COUNT):
#         for r in range(ROW_COUNT):
#             pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
#             color = BLACK
#             if board[r][c] == "X":
#                 color = RED
#             elif board[r][c] == "O":
#                 color = YELLOW
#             pygame.draw.circle(screen, color, (int(c*SQUARESIZE + SQUARESIZE/2), int((r+1)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
#     pygame.display.update()

# def play_pygame():
#     board = create_board()
#     game_over = False
#     turn = 0
#     draw_board(board)

#     while not game_over:
#         for event in pygame.event.get():
#             # if event.type == pygame.QUIT:
#             #     sys.exit()

#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 return

#             if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
#                 if turn == 0:
#                     x = event.pos[0] // SQUARESIZE
#                     if is_valid_location(board, x):
#                         row = get_next_open_row(board, x)
#                         board[row][x] = "X"
#                         if check_winner(board, "X"):
#                             label = font.render("You win!", 1, RED)
#                             screen.blit(label, (40, 10))
#                             game_over = True
#                         turn = 1
#                         draw_board(board)
#         if turn == 1 and not game_over:
#             pygame.time.wait(500)
#             row, col = rule_based_agent(board)
#             board[row][col] = "O"
#             if check_winner(board, "O"):
#                 label = font.render("Rule Based Agent wins!", 1, YELLOW)
#                 screen.blit(label, (20, 10))
#                 game_over = True
#             turn = 0
#             draw_board(board)

#         if game_over:
#             pygame.display.update()
#             pygame.time.wait(5000)
#             # return play_pygame()

# # Uncomment to run the pygame version
# play_pygame()


# --- Tkinter Version ---
import tkinter as tk
from tkinter import messagebox

# def play_tkinter():
#     window = tk.Tk()
#     window.title("Connect 4")

#     board = [[" " for _ in range(7)] for _ in range(6)]
#     buttons = [[None for _ in range(7)] for _ in range(6)]

#     def update_gui():
#         for r in range(6):
#             for c in range(7):
#                 val = board[r][c]
#                 color = "white"
#                 if val == "X":
#                     color = "red"
#                 elif val == "O":
#                     color = "yellow"
#                 buttons[r][c].config(bg=color)

#     def restart_game():
#         nonlocal board
#         # board = [[" " for _ in range(7)] for _ in range(6)]
#         board = create_board()
#         update_gui()

#     def on_click(c):
#         for r in reversed(range(6)):
#             if board[r][c] == " ":
#                 board[r][c] = "X"
#                 update_gui()
#                 if check_winner(board, "X"):
#                     messagebox.showinfo("Game Over", "You win!")
#                     # window.quit()
#                     return
#                 row, col = rule_based_agent(board)
#                 board[row][col] = "O"
#                 update_gui()
#                 if check_winner(board, "O"):
#                     messagebox.showinfo("Game Over", "Agent wins!")
#                     # window.quit()
#                 return

#     for r in range(6):
#         for c in range(7):
#             btn = tk.Button(window, text="", width=6, height=3, command=lambda c=c: on_click(c))
#             btn.grid(row=r, column=c)
#             buttons[r][c] = btn

#     restart_btn = tk.Button(window, text="Restart", command=restart_game)
#     restart_btn.grid(row=6, column=0, columnspan=7, sticky="ew")

#     window.mainloop()

def play_tkinter():
    window = tk.Tk()
    window.title("Connect 4")

    canvas_width = 700
    canvas_height = 700
    cell_size = 100
    radius = 45

    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='blue')
    canvas.pack()

    board = [[" " for _ in range(7)] for _ in range(6)]

    def draw_board():
        canvas.delete("all")
        for r in range(6):
            for c in range(7):
                x0 = c * cell_size + 5
                y0 = (r+1) * cell_size + 5
                x1 = x0 + radius * 2
                y1 = y0 + radius * 2
                color = 'black'
                if board[r][c] == 'X':
                    color = 'red'
                elif board[r][c] == 'O':
                    color = 'yellow'
                canvas.create_oval(x0, y0, x1, y1, fill=color, outline='')

    def on_click(event):
        nonlocal turn, game_over
        if game_over:
            return
        col = event.x // cell_size
        if col < 0 or col >= 7:
            return
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            board[row][col] = 'X'
            draw_board()
            if check_winner(board, 'X'):
                messagebox.showinfo("Game Over", "You win!")
                game_over = True
                return
            row, col = rule_based_agent(board)
            board[row][col] = 'O'
            draw_board()
            if check_winner(board, 'O'):
                messagebox.showinfo("Game Over", "Agent wins!")
                game_over = True

    def restart():
        nonlocal board, game_over
        board = [[" " for _ in range(7)] for _ in range(6)]
        game_over = False
        draw_board()

    canvas.bind("<Button-1>", on_click)
    restart_btn = tk.Button(window, text="Restart", command=restart)
    restart_btn.pack(fill='x')

    game_over = False
    turn = 0
    draw_board()
    window.mainloop()

# Uncomment to run the tkinter version
play_tkinter()
