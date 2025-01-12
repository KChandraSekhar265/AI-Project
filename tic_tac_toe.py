import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe with AI")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (50, 50, 50)

# Board variables
CELL_SIZE = WIDTH // 3
board = [["" for _ in range(3)] for _ in range(3)]
player = "X"

# Draw board
def draw_board():
    screen.fill(WHITE)
    for x in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT), 5)
        pygame.draw.line(screen, LINE_COLOR, (0, x * CELL_SIZE), (WIDTH, x * CELL_SIZE), 5)

# Draw marks
def draw_marks():
    font = pygame.font.Font(None, 120)
    for row in range(3):
        for col in range(3):
            if board[row][col] != "":
                mark = font.render(board[row][col], True, BLACK)
                x, y = col * CELL_SIZE + CELL_SIZE // 3, row * CELL_SIZE + CELL_SIZE // 3
                screen.blit(mark, (x, y))

# Display winner or draw message
def display_message(message):
    font = pygame.font.Font(None, 80)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(WHITE)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Pause for 2 seconds
    pygame.quit()
    sys.exit()

# Check for a winner
def check_winner():
    # Rows, Columns, and Diagonals
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != "":
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

# Check if the board is full (draw)
def is_draw():
    for row in board:
        if "" in row:
            return False
    return True

# Minimax Algorithm for AI
def minimax(board, is_maximizing):
    winner = check_winner()
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = "O"
                    score = minimax(board, False)
                    board[row][col] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = "X"
                    score = minimax(board, True)
                    board[row][col] = ""
                    best_score = min(score, best_score)
        return best_score

# AI Move
def ai_move():
    best_score = -float('inf')
    best_move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                board[row][col] = "O"
                score = minimax(board, False)
                board[row][col] = ""
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        board[best_move[0]][best_move[1]] = "O"

# Main game loop
def main():
    global player
    running = True
    while running:
        draw_board()
        draw_marks()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and player == "X":
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE

                if board[row][col] == "":
                    board[row][col] = player
                    winner = check_winner()
                    if winner:
                        display_message(f"{winner} Wins!")
                    elif is_draw():
                        display_message("It's a Draw!")
                    else:
                        player = "O"
                        ai_move()
                        winner = check_winner()
                        if winner:
                            display_message(f"{winner} Wins!")
                        elif is_draw():
                            display_message("It's a Draw!")
                        player = "X"

if __name__ == "__main__":
    main()
