import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
import pygame
from Terminal_Version.Connect4 import Connect4
from agents import RandomAgent, RuleBasedAgent, BFSAgent, AStarAgent, MiniMax
import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 120
RADIUS = SQUARESIZE // 2 - 5
# WIDTH = COLUMN_COUNT * SQUARESIZE
# HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
# SIZE = (WIDTH, HEIGHT)

# MENU_WIDTH = 300
# WIDTH = COLUMN_COUNT * SQUARESIZE + MENU_WIDTH
# SIZE = (WIDTH, HEIGHT)

MENU_WIDTH = 300
WIDTH = COLUMN_COUNT * SQUARESIZE + MENU_WIDTH
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

# The board
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load images
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect 4")
red_img = pygame.image.load("img/red.png")
yellow_img = pygame.image.load("img/yellow.png")
red_img = pygame.transform.scale(red_img, (SQUARESIZE, SQUARESIZE))
yellow_img = pygame.transform.scale(yellow_img, (SQUARESIZE, SQUARESIZE))
font = pygame.font.SysFont("monospace", 55)

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE + SQUARESIZE//2, (r+1)*SQUARESIZE + SQUARESIZE//2), RADIUS)
            
            if board[r][c] == "●":
                screen.blit(red_img, (c*SQUARESIZE, (r+1)*SQUARESIZE))
            elif board[r][c] == "○":
                screen.blit(yellow_img, (c*SQUARESIZE, (r+1)*SQUARESIZE))

    pygame.display.update()

class GameModeMenu:
    def __init__(self, x_offset, options=None):
        if options is None:
            options = []
        self.options = options
        self.selected = 0
        self.x_offset = x_offset
        self.font = pygame.font.SysFont("arial", 24)

        self.restart_button_rect = pygame.Rect(self.x_offset + 20, HEIGHT - 60, 260, 40)
        self.restart_hovered = False

        self.back_button_rect = pygame.Rect(self.x_offset + 20, HEIGHT - 120, 260, 40)
        self.back_hovered = False

        self.mode_button_rect = pygame.Rect(self.x_offset + 20, HEIGHT - 180, 260, 40)
        self.mode_hovered = False



    def draw(self):
        for i, option in enumerate(self.options):
            rect = pygame.Rect(self.x_offset + 20, 40 + i * 40, 20, 20)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            if self.selected == i:
                pygame.draw.circle(screen, (255, 255, 255), rect.center, 8)

            label = self.font.render(option, True, (255, 255, 255))
            screen.blit(label, (self.x_offset + 50, 35 + i * 40))

        # Draw Restart Button
        color = (150, 200, 150) if self.restart_hovered else (100, 180, 100)
        pygame.draw.rect(screen, color, self.restart_button_rect, border_radius=8)
        restart_text = self.font.render("Restart Game", True, (0, 0, 0))
        text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
        screen.blit(restart_text, text_rect)

        # Draw Back Button
        back_color = (200, 150, 150) if self.back_hovered else (180, 100, 100)
        pygame.draw.rect(screen, back_color, self.back_button_rect, border_radius=8)
        back_text = self.font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        screen.blit(back_text, back_text_rect)

        # Draw Options Button
        mode_color = (150, 150, 200) if self.mode_hovered else (100, 100, 180)
        pygame.draw.rect(screen, mode_color, self.mode_button_rect, border_radius=8)
        mode_text = self.font.render("Game Mode", True, (0, 0, 0))
        mode_text_rect = mode_text.get_rect(center=self.mode_button_rect.center)
        screen.blit(mode_text, mode_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.restart_hovered = self.restart_button_rect.collidepoint(event.pos)
            self.back_hovered = self.back_button_rect.collidepoint(event.pos)
            self.mode_hovered = self.mode_button_rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button_rect.collidepoint(event.pos):
                return "restart"
            if self.back_button_rect.collidepoint(event.pos):
                return "back"
            if self.mode_button_rect.collidepoint(event.pos):
                print("Mode button clicked")  # Add this line
                return "mode"

            for i in range(len(self.options)):
                rect = pygame.Rect(self.x_offset + 20, 40 + i * 40, 20, 20)
                if rect.collidepoint(event.pos):
                    self.selected = i
                    return i
        return None

    def get_mode(self):
        return self.selected

def initialize_game_and_agents(selected_mode):
    game = Connect4()
    agent = None
    agent1 = None
    agent2 = None

    if selected_mode == 0:
        agent = RandomAgent(game)
        agent.name = "Random Agent"
    elif selected_mode == 1:
        agent = RuleBasedAgent(game)
        agent.name = "Rule-Based Agent"
    elif selected_mode == 2:
        agent = BFSAgent(game)
        agent.name = "BFS Agent"
    elif selected_mode == 3:
        agent = AStarAgent(game)
        agent.name = "A* Agent"
    elif selected_mode == 4:
        agent = MiniMax(game)
        agent.name = "MiniMax Agent"
    elif selected_mode == 5:
        agent1 = RandomAgent(game)
        agent1.name = "Random Agent"
        agent2 = RuleBasedAgent(game)
        agent2.name = "Rule-Based Agent"
    elif selected_mode == 6:
        agent1 = RuleBasedAgent(game)
        agent1.name = "Rule-Based Agent"
        agent2 = MiniMax(game)
        agent2.name = "MiniMax Agent"

    return game, agent, agent1, agent2

def main_menu():
    title_font = pygame.font.SysFont("monospace", 60)
    menu_font = pygame.font.SysFont("monospace", 40)

    # Define button rectangles
    play_button_rect = pygame.Rect(WIDTH // 2 - 130, 250, 260, 60)
    quit_button_rect = pygame.Rect(WIDTH // 2 - 130, 330, 260, 60)

    play_hovered = False
    quit_hovered = False

    while True:
        screen.fill((0, 0, 0))

        # Draw title
        title_label = title_font.render("Connect 4", True, (255, 255, 255))
        screen.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, 100))

        # Mouse hover detection
        mouse_pos = pygame.mouse.get_pos()
        play_hovered = play_button_rect.collidepoint(mouse_pos)
        quit_hovered = quit_button_rect.collidepoint(mouse_pos)

        # Button colors
        play_color = (150, 200, 150) if play_hovered else (100, 180, 100)
        quit_color = (200, 150, 150) if quit_hovered else (180, 100, 100)

        # Draw buttons
        pygame.draw.rect(screen, play_color, play_button_rect, border_radius=8)
        pygame.draw.rect(screen, quit_color, quit_button_rect, border_radius=8)

        # Draw button text
        play_text = menu_font.render("Play Game", True, (0, 0, 0))
        quit_text = menu_font.render("Quit", True, (0, 0, 0))
        screen.blit(play_text, play_text.get_rect(center=play_button_rect.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button_rect.center))

        pygame.display.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    main(0)  # Start game
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def options_menu():
    options = [
        "Player vs Random Agent",
        "Player vs Rule-Based Agent",
        "Player vs BFS Agent",
        "Player vs A* Agent",
        "Player vs MiniMax Agent",
        "AI vs AI (Random vs Rule-Based Agent)",
        "AI vs AI (Rule-Based vs MiniMax Agent)",
        "Quit"
    ]
    menu = GameModeMenu(COLUMN_COUNT * SQUARESIZE, options)
    while True:
        screen.fill((0, 0, 0))
        menu.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mode_selected = menu.handle_event(event)

            if mode_selected == "back":
                main_menu()
                return  # Back to main menu

            if isinstance(mode_selected, int):
                if mode_selected == 7:
                    pygame.quit()
                    sys.exit()
                main(mode_selected)  # Only here can you start a game with a selected mode
                return

def main(selected_mode):
    # Pass an empty options list since options are not needed in main
    game, agent, agent1, agent2 = initialize_game_and_agents(selected_mode)
    game_over = False
    menu = GameModeMenu(COLUMN_COUNT * SQUARESIZE)

    while True:
        screen.fill((0, 0, 0))
        menu.draw()
        draw_board(game.board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mode_selected = menu.handle_event(event)
            if mode_selected is not None:
                if mode_selected == "restart":
                    game, agent, agent1, agent2 = initialize_game_and_agents(selected_mode)
                    game_over = False
                    break  # break out of the event loop

                if mode_selected == "back":
                    main_menu()
                    return

                if mode_selected == "mode":
                    options_menu()
                    return

                if isinstance(mode_selected, int) and mode_selected == 7:
                    pygame.quit()
                    sys.exit()
                # No need to continue, just break after handling
                break

            # Human player's move
            if not game_over and game.current_player == "●" and event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                if x < COLUMN_COUNT * SQUARESIZE:
                    col = x // SQUARESIZE
                    if col in game.get_available_moves(game.board):
                        game.make_move(col, "●")
                        draw_board(game.board)
                        pygame.display.update() 
                        if game.check_winner("●"):
                            label = font.render("You win!", 1, (255, 0, 0))
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            game_over = True
                        else:
                            game.current_player = "○"

        # AI move
        if not game_over and (selected_mode in [0, 1, 2, 3, 4] and game.current_player == "○"):
            pygame.time.wait(500)
            if agent is not None:
                if selected_mode == 0:  # Random Agent
                    col = agent.random_agent_move(game.board)
                elif selected_mode == 1:  # Rule-Based Agent
                    col = agent.rule_based_agent(game.board)
                elif selected_mode == 2:  # BFS Agent
                    col = agent.bfs_ai_move(game.board, player="○", opponent="●")
                elif selected_mode == 3:  # A* Agent
                    col = agent.best_move()
                elif selected_mode == 4:  # MiniMax Agent
                    col = agent.best_move(game.board)
                ai_name = agent.name
            else:
                raise ValueError("Agent is not initialized for the selected mode.")

            game.make_move(col, "○")
            if game.check_winner("○"):
                label = font.render(f"{ai_name} wins!", 1, (255, 255, 0))
                screen.blit(label, (40, 10))
                pygame.display.update()
                pygame.time.wait(3000)
                game_over = True
            else:
                game.current_player = "●"

        # AI vs AI move (one move per frame)
        elif not game_over and selected_mode in [5, 6]:
            pygame.time.wait(500)
            if game.current_player == "●" and agent1 is not None:
                if selected_mode == 5:
                    col = agent1.random_agent_move(game.board)
                    ai_name = agent1.name
                elif selected_mode == 6:
                    col = agent1.rule_based_agent(game.board)
                    ai_name = agent1.name
            elif game.current_player == "○" and agent2 is not None:
                if selected_mode == 5:
                    col = agent2.rule_based_agent(game.board)
                    ai_name = agent2.name
                elif selected_mode == 6:
                    # agent2.game.board = np.copy(game.board)
                    # col = agent2.best_move()
                    col = agent2.best_move(game.board)
                    ai_name = agent2.name
            else:
                raise ValueError("Agents are not properly initialized for AI vs AI mode.")

            game.make_move(col, game.current_player)

            # Check for a winner
            if game.check_winner(game.current_player):
                label = font.render(f"{ai_name} wins!", 1, (255, 255, 0))
                screen.blit(label, (40, 10))
                pygame.display.update()
                pygame.time.wait(3000)
                game_over = True
            elif game.is_full(game.board):
                label = font.render("Draw!", 1, (255, 255, 255))
                screen.blit(label, (40, 10))
                pygame.display.update()
                pygame.time.wait(3000)
                game_over = True
            else:
                # Switch to the other player
                game.current_player = "●" if game.current_player == "○" else "○"

            draw_board(game.board)

        # Check for draw
        if game.is_full(game.board):
            label = font.render("Draw!", 1, (255, 255, 255))
            screen.blit(label, (40, 10))
            pygame.display.update()
            pygame.time.wait(3000)
            game_over = True

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
