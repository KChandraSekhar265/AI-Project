import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Card dimensions (Adjusted for a better fit)
CARD_WIDTH = 120
CARD_HEIGHT = 100
MARGIN = 10
ROWS = 4
COLS = 4
CARD_LIST = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] * 2  # 8 pairs of cards

# Shuffle cards
random.shuffle(CARD_LIST)

# Create a list to hold the card positions
cards = []
for row in range(ROWS):
    for col in range(COLS):
        cards.append(pygame.Rect(col * (CARD_WIDTH + MARGIN) + MARGIN, row * (CARD_HEIGHT + MARGIN) + MARGIN, CARD_WIDTH, CARD_HEIGHT))

# Game state
flipped_cards = []
matched_cards = []
game_over = False
moves_left = 20  # Limit the number of moves the player can make

# Font
font = pygame.font.Font(None, 60)
move_font = pygame.font.Font(None, 30)
end_font = pygame.font.Font(None, 80)

# Function to draw the cards
def draw_cards():
    for i, card in enumerate(cards):
        if i in flipped_cards or i in matched_cards:
            pygame.draw.rect(screen, GREEN, card)  # Draw face-up card
            text = font.render(CARD_LIST[i], True, BLACK)
            screen.blit(text, (card.x + (CARD_WIDTH // 2 - text.get_width() // 2), card.y + (CARD_HEIGHT // 2 - text.get_height() // 2)))
        else:
            pygame.draw.rect(screen, RED, card)  # Draw face-down card

# Function to check for a match
def check_match():
    global flipped_cards
    if len(flipped_cards) == 2:
        idx1, idx2 = flipped_cards
        if CARD_LIST[idx1] == CARD_LIST[idx2]:
            matched_cards.extend([idx1, idx2])
        flipped_cards = []

# Function to display the game over message
def game_over_message():
    text = font.render("Game Over!", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))

# Function to display the remaining moves
def display_moves():
    move_text = move_font.render(f'Moves Left: {moves_left}', True, BLACK)
    screen.blit(move_text, (10, HEIGHT - 40))

# Function to display the win or lose message
def display_result():
    if len(matched_cards) == len(CARD_LIST):  # Player wins if all pairs are matched
        text = end_font.render("You Win!", True, GREEN)
    else:
        text = end_font.render("You Lose!", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 120))

# Main loop
def main():
    global flipped_cards, matched_cards, game_over, moves_left
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)
        draw_cards()
        display_moves()

        # Check if all cards are matched
        if len(matched_cards) == len(CARD_LIST) and moves_left > 0:
            game_over = True
            display_result()

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                for i, card in enumerate(cards):
                    if card.collidepoint(x, y) and i not in flipped_cards and i not in matched_cards:
                        flipped_cards.append(i)

                # Check for match after two cards are flipped
                if len(flipped_cards) == 2:
                    check_match()
                    moves_left -= 1  # Decrease moves after each flip

                # If moves are exhausted, end the game
                if moves_left <= 0:
                    game_over = True
                    display_result()

        pygame.display.flip()
        clock.tick(30)

        # Close the window after the game is over
        if game_over:
            pygame.time.wait(2000)  # Wait for 2 seconds to display "Game Over"
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
