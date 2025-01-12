import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Game Hub")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
HIGHLIGHT = (150, 150, 255)

# Fonts
font = pygame.font.Font(None, 50)
title_font = pygame.font.Font(None, 80)

# Game list
games = [
    {"name": "Tic Tac Toe", "file": "tic_tac_toe.py"},
    {"name": "Number Guessing", "file": "number_guessing.py"},
    {"name": "Hand Cricket", "file": "hand_cricket.py"},
    {"name": "Nim Game", "file": "nim_game.py"},
    {"name": "Memory Game", "file": "memory_game.py"},
]

# Draw menu
def draw_menu(selected_index):
    screen.fill(WHITE)

    # Draw title
    title = title_font.render("Arcade Game Hub", True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title, title_rect)

    # Draw game options
    for i, game in enumerate(games):
        color = HIGHLIGHT if i == selected_index else GRAY
        text = font.render(game["name"], True, color)
        text_rect = text.get_rect(center=(WIDTH // 2, 150 + i * 60))
        screen.blit(text, text_rect)

# Main loop
def main_menu():
    selected_index = 0
    clock = pygame.time.Clock()

    while True:
        draw_menu(selected_index)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(games)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(games)
                elif event.key == pygame.K_RETURN:
                    # Launch selected game and wait for it to finish
                    subprocess.run(["python", games[selected_index]["file"]])

        clock.tick(30)

if __name__ == "__main__":
    main_menu()
