import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)  # Extra space for score and next piece
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Colors for each shape
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 0.5  # Time in seconds between automatic falls

    def new_piece(self):
        # Choose a random shape
        shape = random.randint(0, len(SHAPES) - 1)
        # Starting position (centered at top)
        x = GRID_WIDTH // 2 - len(SHAPES[shape][0]) // 2
        y = 0
        return {'shape': shape, 'x': x, 'y': y, 'rotation': 0}

    def rotate_piece(self, piece):
        # Get the shape matrix
        shape_matrix = SHAPES[piece['shape']]
        # Rotate the matrix 90 degrees clockwise
        rotated = list(zip(*shape_matrix[::-1]))
        return rotated

    def valid_move(self, piece, x, y, rotation=0):
        shape_matrix = SHAPES[piece['shape']]
        if rotation:
            shape_matrix = self.rotate_piece(piece)

        for i in range(len(shape_matrix)):
            for j in range(len(shape_matrix[0])):
                if shape_matrix[i][j]:
                    if (x + j < 0 or x + j >= GRID_WIDTH or
                        y + i >= GRID_HEIGHT or
                        (y + i >= 0 and self.grid[y + i][x + j])):
                        return False
        return True

    def merge_piece(self):
        shape_matrix = SHAPES[self.current_piece['shape']]
        if self.current_piece['rotation']:
            shape_matrix = self.rotate_piece(self.current_piece)

        for i in range(len(shape_matrix)):
            for j in range(len(shape_matrix[0])):
                if shape_matrix[i][j]:
                    if 0 <= self.current_piece['y'] + i < GRID_HEIGHT and 0 <= self.current_piece['x'] + j < GRID_WIDTH:
                        self.grid[self.current_piece['y'] + i][self.current_piece['x'] + j] = self.current_piece['shape'] + 1

    def clear_lines(self):
        lines_to_clear = []
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                lines_to_clear.append(i)

        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])

        # Update score
        cleared = len(lines_to_clear)
        if cleared > 0:
            self.lines_cleared += cleared
            self.score += [0, 100, 300, 500, 800][cleared] * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(0.05, 0.5 - (self.level - 1) * 0.05)

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, GRAY,
                               (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, SHAPE_COLORS[self.grid[y][x] - 1],
                                   (x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2))

    def draw_piece(self, piece, x_offset=0, y_offset=0):
        shape_matrix = SHAPES[piece['shape']]
        if piece['rotation']:
            shape_matrix = self.rotate_piece(piece)

        for i in range(len(shape_matrix)):
            for j in range(len(shape_matrix[0])):
                if shape_matrix[i][j]:
                    pygame.draw.rect(self.screen, SHAPE_COLORS[piece['shape']],
                                   ((piece['x'] + j + x_offset) * BLOCK_SIZE + 1,
                                    (piece['y'] + i + y_offset) * BLOCK_SIZE + 1,
                                    BLOCK_SIZE - 2, BLOCK_SIZE - 2))

    def draw_next_piece(self):
        # Draw "Next Piece" text
        font = pygame.font.Font(None, 36)
        text = font.render("Next:", True, WHITE)
        self.screen.blit(text, (GRID_WIDTH * BLOCK_SIZE + 10, 10))

        # Draw the next piece preview
        self.draw_piece(self.next_piece, GRID_WIDTH + 1, 2)

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        lines_text = font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 100))
        self.screen.blit(level_text, (GRID_WIDTH * BLOCK_SIZE + 10, 140))
        self.screen.blit(lines_text, (GRID_WIDTH * BLOCK_SIZE + 10, 180))

    def run(self):
        while not self.game_over:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, self.current_piece['x'] - 1, self.current_piece['y']):
                            self.current_piece['x'] -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, self.current_piece['x'] + 1, self.current_piece['y']):
                            self.current_piece['x'] += 1
                    elif event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                            self.current_piece['y'] += 1
                    elif event.key == pygame.K_UP:
                        new_rotation = (self.current_piece['rotation'] + 1) % 2
                        if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'], new_rotation):
                            self.current_piece['rotation'] = new_rotation
                    elif event.key == pygame.K_SPACE:
                        # Hard drop
                        while self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                            self.current_piece['y'] += 1
                        self.merge_piece()
                        self.clear_lines()
                        self.current_piece = self.next_piece
                        self.next_piece = self.new_piece()
                        if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
                            self.game_over = True

            # Handle automatic falling
            self.fall_time += self.clock.get_rawtime()
            if self.fall_time >= self.fall_speed * 1000:
                if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                    self.current_piece['y'] += 1
                else:
                    self.merge_piece()
                    self.clear_lines()
                    self.current_piece = self.next_piece
                    self.next_piece = self.new_piece()
                    if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
                        self.game_over = True
                self.fall_time = 0

            # Draw everything
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_piece(self.current_piece)
            self.draw_next_piece()
            self.draw_score()
            pygame.display.flip()
            self.clock.tick(60)

        # Game over screen
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("GAME OVER", True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                        SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

if __name__ == "__main__":
    game = Tetris()
    game.run()
    pygame.quit() 