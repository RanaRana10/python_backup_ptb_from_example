import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_COLOR = (23, 145, 135)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)

# Board
board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Function to draw the board
def draw_board():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_symbols():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + 15, row * SQUARE_SIZE + 15),
                                 ((col + 1) * SQUARE_SIZE - 15, (row + 1) * SQUARE_SIZE - 15), 5)
                pygame.draw.line(screen, RED, ((col + 1) * SQUARE_SIZE - 15, row * SQUARE_SIZE + 15),
                                 (col * SQUARE_SIZE + 15, (row + 1) * SQUARE_SIZE - 15), 5)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 15, 5)

def check_winner():
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] != " ":
            return board[row][0]

    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]

    return None

def is_board_full():
    for row in board:
        if " " in row:
            return False
    return True

def draw_status(winner):
    font = pygame.font.Font(None, 48)
    if winner is None:
        status_text = "Tie!"
    else:
        status_text = f"Player {winner} wins!"
    text = font.render(status_text, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()

def reset_board():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = " "
    screen.fill(WHITE)
    draw_board()

def click_square(row, col):
    if board[row][col] == " ":
        if current_player == "X":
            board[row][col] = "X"
        else:
            board[row][col] = "O"
        draw_symbols()
        pygame.display.update()
        return True
    return False

draw_board()
current_player = "X"
game_over = False

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if click_square(clicked_row, clicked_col):
                winner = check_winner()
                if winner is not None or is_board_full():
                    draw_status(winner)
                    game_over = True
                    pygame.time.wait(2000)  # Wait for 2 seconds before starting new game
                    reset_board()
                    game_over = False
                    current_player = "X"
                else:
                    current_player = "O" if current_player == "X" else "X"

    pygame.display.update()
