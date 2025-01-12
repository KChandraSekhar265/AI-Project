import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nim Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Font
font = pygame.font.Font(None, 40)
input_font = pygame.font.Font(None, 36)

# Function to draw text
def draw_text(text, x, y, color=BLACK):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Function to display game over message
def display_game_over(winner):
    screen.fill(WHITE)
    if winner == "user":
        draw_text("You Win!", WIDTH // 2 - 80, HEIGHT // 2 - 20, GREEN)
    else:
        draw_text("Computer Wins!", WIDTH // 2 - 140, HEIGHT // 2 - 20, RED)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    exit()

# Function to handle computer's turn
def computer_turn(sticks):
    max_pick = max(1, sticks // 2)
    picked_sticks = random.randint(1, max_pick)
    draw_text(f"Computer picks {picked_sticks} stick(s).", WIDTH // 2 - 180, HEIGHT // 2 + 60, RED)
    pygame.display.flip()
    pygame.time.wait(2000)
    return sticks - picked_sticks

# Function to display input box
def get_user_input(prompt, max_pick):
    input_text = ""
    active = True

    while active:
        screen.fill(WHITE)
        draw_text(f"Remaining sticks: {sticks}", WIDTH // 2 - 180, HEIGHT // 2 - 150, BLACK)
        draw_text(prompt, WIDTH // 2 - 180, HEIGHT // 2 - 80)
        draw_text(f"Max you can pick: {max_pick}", WIDTH // 2 - 180, HEIGHT // 2 - 40)
        pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 100, HEIGHT // 2, 200, 40))
        text_surface = input_font.render(input_text, True, BLACK)
        screen.blit(text_surface, (WIDTH // 2 - 90, HEIGHT // 2 + 5))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        value = int(input_text)
                        if 1 <= value <= max_pick:
                            return value
                        else:
                            draw_text("Invalid input, try again.", WIDTH // 2 - 150, HEIGHT // 2 + 100, RED)
                            pygame.display.flip()
                            pygame.time.wait(1500)
                    except ValueError:
                        draw_text("Invalid input, try again.", WIDTH // 2 - 150, HEIGHT // 2 + 100, RED)
                        pygame.display.flip()
                        pygame.time.wait(1500)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

# Main game loop
def main():
    global sticks
    # Initialize the game with random number of sticks
    sticks = random.randint(10, 30)

    while sticks > 1:
        screen.fill(WHITE)

        # Display remaining sticks at the start
        draw_text(f"Starting with {sticks} sticks", WIDTH // 2 - 150, HEIGHT // 2 - 150, GREEN)

        # User's turn
        max_pick = max(1, sticks // 2)
        user_pick = get_user_input("Your turn: Enter sticks to pick", max_pick)
        sticks -= user_pick
        if sticks == 1:
            display_game_over("computer")

        # Computer's turn
        sticks = computer_turn(sticks)
        if sticks == 1:
            display_game_over("user")

        pygame.display.flip()

if __name__ == "__main__":
    main()
