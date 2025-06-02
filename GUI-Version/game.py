import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
import pygame
from Terminal_Version.Connect4 import Connect4
from agents import RandomAgent, RuleBasedAgent, BFSAgent, AStarAgent, MiniMax

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = SQUARESIZE // 2 - 5
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

MENU_WIDTH = 300
WIDTH = COLUMN_COUNT * SQUARESIZE + MENU_WIDTH
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
    def __init__(self, x_offset):
        self.options = [
            "Player vs Random Agent",
            "Player vs Rule-Based Agent",
            "Player vs BFS Agent",
            "Player vs A* Agent",
            "Player vs MiniMax Agent",
            "AI vs AI (Random vs Rule-Based Agent)",
            "AI vs AI (Rule-Based vs MiniMax Agent)",
            "Quit"
        ]
        self.selected = 0
        self.x_offset = x_offset
        self.font = pygame.font.SysFont("arial", 24)

        self.restart_button_rect = pygame.Rect(self.x_offset + 20, HEIGHT - 60, 260, 40)
        self.restart_hovered = False

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

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.restart_hovered = self.restart_button_rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button_rect.collidepoint(event.pos):
                return "restart"

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


def main():
    default_mode = 0  # You can set any mode here, e.g., 0 = Player vs RandomAgent
    game, agent, agent1, agent2 = initialize_game_and_agents(default_mode)
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

            # Restart Button Clicked
            if mode_selected == "restart":
                selected_mode = menu.get_mode()
                game, agent, agent1, agent2 = initialize_game_and_agents(selected_mode)
                game_over = False
                continue

            # Menu Option Selected
            if isinstance(mode_selected, int):
                if mode_selected == 7:
                    pygame.quit()
                    sys.exit()
                game, agent, agent1, agent2 = initialize_game_and_agents(mode_selected)
                game_over = False
                continue

            # Human player's move
            if not game_over and game.current_player == "●" and event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                if x < COLUMN_COUNT * SQUARESIZE:
                    col = x // SQUARESIZE
                    if col in game.get_available_moves(game.board):
                        game.make_move(col, "●")
                        if game.check_winner("●"):
                            label = font.render("You win!", 1, (255, 0, 0))
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            game_over = True
                        else:
                            game.current_player = "○"

        # AI move
        if not game_over and game.current_player == "○":
            pygame.time.wait(500)
            selected_mode = menu.get_mode()

            if selected_mode in [0, 1, 2, 3, 4]:
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
                        col = agent.best_move()
                    ai_name = agent.name
                else:
                    raise ValueError("Agent is not initialized for the selected mode.")
            elif selected_mode in [5, 6]:
                while not game_over:
                    pygame.time.wait(500)

                    if game.current_player == "●" and agent1 is not None:
                        if selected_mode == 5:
                            col = agent1.random_agent_move(game.board)
                        elif selected_mode == 6:
                            col = agent1.rule_based_agent(game.board)
                        ai_name = agent1.name
                    elif game.current_player == "○" and agent2 is not None:
                        if selected_mode == 5:
                            col = agent2.rule_based_agent(game.board)
                        elif selected_mode == 6:
                            col = agent2.best_move()
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
            else:
                col = random.choice(game.get_available_moves(game.board))
                ai_name = "Random"

            game.make_move(col, "○")
            if game.check_winner("○"):
                label = font.render(f"{ai_name} wins!", 1, (255, 255, 0))
                screen.blit(label, (40, 10))
                pygame.display.update()
                pygame.time.wait(3000)
                game_over = True
            else:
                game.current_player = "●"

        # Check for draw
        if game.is_full(game.board):
            label = font.render("Draw!", 1, (255, 255, 255))
            screen.blit(label, (40, 10))
            pygame.display.update()
            pygame.time.wait(3000)
            game_over = True

        pygame.display.update()

if __name__ == "__main__":
    main()
