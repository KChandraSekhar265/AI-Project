import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand Cricket")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 35)

# Draw text utility
def draw_text(text, size, color, position):
    font = pygame.font.Font(None, size)
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=position)
    screen.blit(rendered_text, text_rect)

# Game loop
def main():
    clock = pygame.time.Clock()
    running = True

    # Game state variables
    player_score = 0
    computer_score = 0
    is_player_batting = True
    is_game_over = False

    # Match variables
    current_ball = None
    computer_choice = None
    result = ""
    innings = 1

    while running:
        screen.fill(WHITE)

        # Draw the title and scores
        draw_text("Hand Cricket", 60, BLACK, (WIDTH // 2, 50))
        draw_text(f"Innings: {'Player Batting' if is_player_batting else 'Player Bowling'}", 40, BLUE, (WIDTH // 2, 150))
        draw_text(f"Player Score: {player_score}", 40, GREEN, (200, 200))
        draw_text(f"Computer Score: {computer_score}", 40, RED, (600, 200))

        # Display game result or round result
        if is_game_over:
            draw_text(result, 50, BLACK, (WIDTH // 2, 350))
            draw_text("Press R to Restart or Q to Quit", 40, BLACK, (WIDTH // 2, 450))
        elif current_ball is not None and computer_choice is not None:
            draw_text(f"You chose: {current_ball}", 40, BLUE, (200, 300))
            draw_text(f"Computer chose: {computer_choice}", 40, RED, (600, 300))

        # Draw buttons for player input
        if not is_game_over:
            button_rects = []
            for i in range(1, 7):
                button_rect = pygame.Rect(100 + (i - 1) * 100, 400, 80, 50)
                button_rects.append((button_rect, i))
                pygame.draw.rect(screen, GRAY, button_rect, border_radius=10)
                draw_text(str(i), 35, BLACK, button_rect.center)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not is_game_over:
                mouse_pos = event.pos
                for button_rect, value in button_rects:
                    if button_rect.collidepoint(mouse_pos):
                        current_ball = value
                        computer_choice = random.randint(1, 6)

                        # Batting logic
                        if is_player_batting:
                            if current_ball == computer_choice:
                                result = f"You are out! Your score: {player_score}"
                                is_player_batting = False
                                innings += 1
                            else:
                                player_score += current_ball

                        # Bowling logic
                        else:
                            if current_ball == computer_choice:
                                result = f"Computer is out! Computer's score: {computer_score}"
                                is_game_over = True
                                if player_score > computer_score:
                                    result += " You win!"
                                elif player_score < computer_score:
                                    result += " Computer wins!"
                                else:
                                    result += " It's a tie!"
                            else:
                                computer_score += computer_choice

                        # End game if computer exceeds player score
                        if not is_player_batting and computer_score > player_score:
                            result = "Computer wins! Computer exceeded your score."
                            is_game_over = True

            if event.type == pygame.KEYDOWN and is_game_over:
                if event.key == pygame.K_r:  # Restart the game
                    player_score = 0
                    computer_score = 0
                    is_player_batting = True
                    is_game_over = False
                    current_ball = None
                    computer_choice = None
                    result = ""
                    innings = 1
                elif event.key == pygame.K_q:  # Quit the game
                    return

        clock.tick(30)

if __name__ == "__main__":
    main()
