import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Guessing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 35)

# Initialize game variables
def reset_game():
    return random.randint(1, 100), 7, "", ""

def draw_text(text, size, color, position):
    font = pygame.font.Font(None, size)
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=position)
    screen.blit(rendered_text, text_rect)

def main():
    number, attempts_left, message, input_text = reset_game()
    running = True

    while running:
        screen.fill(WHITE)

        # Display game info
        draw_text("Number Guessing Game", 60, BLACK, (WIDTH // 2, 50))
        draw_text(f"Attempts Left: {attempts_left}", 40, BLUE, (WIDTH // 2, 120))
        draw_text("Enter your guess (1-100):", 40, BLACK, (WIDTH // 2, 200))

        # Display the input text and message
        input_rect = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
        pygame.draw.rect(screen, GRAY, input_rect, border_radius=5)
        draw_text(input_text, 40, BLACK, (WIDTH // 2, 275))
        draw_text(message, 35, RED if attempts_left == 0 else GREEN, (WIDTH // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check the guess
                    if input_text.isdigit():
                        guess = int(input_text)
                        if guess == number:
                            message = "Correct! You guessed the number!"
                            attempts_left = 0
                        elif guess < number:
                            message = "Too low! Try again."
                            attempts_left -= 1
                        elif guess > number:
                            message = "Too high! Try again."
                            attempts_left -= 1
                    else:
                        message = "Enter a valid number!"

                    input_text = ""  # Clear input text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove last character
                elif len(input_text) < 3 and event.unicode.isdigit():
                    input_text += event.unicode  # Append digit to input text

        # Check for end of game
        if attempts_left == 0:
            screen.fill(WHITE)
            if message.startswith("Correct"):
                draw_text("You Win!", 60, GREEN, (WIDTH // 2, 200))
            else:
                draw_text(f"Game Over! The number was {number}.", 40, RED, (WIDTH // 2, 200))

            draw_text("Press R to Replay or Q to Quit", 40, BLACK, (WIDTH // 2, 300))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            number, attempts_left, message, input_text = reset_game()
                            waiting = False
                        elif event.key == pygame.K_q:
                            return  # Exit to main menu

if __name__ == "__main__":
    main()
