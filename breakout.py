import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Ball and Paddle settings
BALL_RADIUS = 10
BALL_COLOR = WHITE
BALL_SPEED_X = 5  # Initial ball speed
BALL_SPEED_Y = -5  # Initial ball speed
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_COLOR = BLUE
PADDLE_SPEED = 8

# Brick settings
BRICK_WIDTH = 70
BRICK_HEIGHT = 30
BRICK_COLOR = RED
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_PADDING = 5

# Create brick grid
bricks = []
for row in range(BRICK_ROWS):
    brick_row = []
    for col in range(BRICK_COLS):
        brick_rect = pygame.Rect(col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING, row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_PADDING, BRICK_WIDTH, BRICK_HEIGHT)
        brick_row.append(brick_rect)
    bricks.append(brick_row)

# Paddle setup
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball setup
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT - 60, BALL_RADIUS, BALL_RADIUS)

# Game state
game_over = False
score = 0

# Font for score and game over text
font = pygame.font.Font(None, 36)

# Draw the ball
def draw_ball():
    pygame.draw.circle(screen, BALL_COLOR, ball.center, BALL_RADIUS)

# Draw the paddle
def draw_paddle():
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)

# Draw the bricks
def draw_bricks():
    for row in bricks:
        for brick in row:
            pygame.draw.rect(screen, BRICK_COLOR, brick)

# Draw score
def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Draw game over screen
def draw_game_over():
    game_over_text = font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 20))
    restart_text = font.render("Press R to Restart", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

# Main game loop
def main():
    global ball, paddle, bricks, score, game_over, BALL_SPEED_X, BALL_SPEED_Y
    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)
        draw_bricks()
        draw_ball()
        draw_paddle()
        draw_score()

        if game_over:
            draw_game_over()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += PADDLE_SPEED

        # Ball movement and collision with walls
        if not game_over:
            ball.x += BALL_SPEED_X
            ball.y += BALL_SPEED_Y

            # Ball collision with walls
            if ball.left <= 0 or ball.right >= WIDTH:
                BALL_SPEED_X = -BALL_SPEED_X
            if ball.top <= 0:
                BALL_SPEED_Y = -BALL_SPEED_Y

            # Ball collision with the paddle
            if ball.colliderect(paddle):
                BALL_SPEED_Y = -BALL_SPEED_Y

            # Ball collision with bricks
            for row in bricks:
                for brick in row:
                    if ball.colliderect(brick):
                        row.remove(brick)
                        score += 10
                        BALL_SPEED_Y = -BALL_SPEED_Y

            # Check for game over (if ball falls below screen)
            if ball.bottom >= HEIGHT:
                game_over = True

        # Check if the player has won (all bricks destroyed)
        if len([brick for row in bricks for brick in row]) == 0:
            game_over = True
            draw_score()  # Show final score
            pygame.display.flip()
            pygame.time.delay(2000)  # Wait for 2 seconds before closing

        # Restart on 'R' key press
        if game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_over = False
                score = 0
                ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT - 60, BALL_RADIUS, BALL_RADIUS)
                bricks = []
                for row in range(BRICK_ROWS):
                    brick_row = []
                    for col in range(BRICK_COLS):
                        brick_rect = pygame.Rect(col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING, row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_PADDING, BRICK_WIDTH, BRICK_HEIGHT)
                        brick_row.append(brick_rect)
                    bricks.append(brick_row)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
