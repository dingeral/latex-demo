import pygame
import numpy as np# Define constants
width, height = 640, 480
cell_size = 10
rows, cols = height // cell_size, width // cell_size
paddle_width, paddle_height = 10, 60
paddle_speed = 5
bg_color = pygame.Color('black')
fg_color = pygame.Color('white')
font_size = 36
font_color = pygame.Color('red')

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong and Game of Life')

# Define Paddle class
class Paddle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = paddle_width
        self.height = paddle_height
        self.speed = paddle_speed
    
    def move_up(self):
        if self.y >= self.speed:
            self.y -= self.speed
    
    def move_down(self):
        if self.y <= height - self.height - self.speed:
            self.y += self.speed
    
    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, fg_color, rect)

# Define Game of Life class
class GameOfLife():
    def __init__(self):
        self.grid = np.zeros((rows, cols))
        self.grid[5:9, 5:9] = [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
    
    def update(self):
        # Compute the number of living neighbors for each cell
        neighbors = np.zeros((rows, cols))
        neighbors[1:rows-1, 1:cols-1] = self.grid[:rows-2, :cols-2] + self.grid[:rows-2, 1:cols-1] + \
                                         self.grid[:rows-2, 2:] + \
                                         self.grid[1:rows-1, :cols-2] + self.grid[1:rows-1, 2:] + \
                                         self.grid[2:, :cols-2] + self.grid[2:, 1:cols-1] + self.grid[2:, 2:]
        
        # Apply the rules of the Game of Life to update the grid
        self.grid[neighbors < 2] = 0
        self.grid[np.logical_and(neighbors >= 2, neighbors <= 3)] = 1
        self.grid[neighbors > 3] = 0
        self.grid[np.logical_and(self.grid == 0, neighbors == 3)] = 1
    
    def draw(self, surface):
        for row in range(rows):
            for col in range(cols):
                if self.grid[row, col] == 1:
                    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(surface, fg_color, rect)

# Initialize the Paddle and Game of Life objects
paddle = Paddle(width - paddle_width - 10, height // 2 - paddle_height // 2)
game_of_life = GameOfLife()

# Define the main game loop
clock = pygame.time.Clock()
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle.move_up()
            elif event.key == pygame.K_DOWN:
                paddle.move_down()
    
    # Update and draw the game objects
    game_of_life.update()
    screen.fill(bg_color)
    paddle.draw(screen)
    game_of_life.draw(screen)
    
    # Check for collisions
    ball_rect = pygame.Rect(0, 0, cell_size, cell_size)
    ball_rect.center = (paddle.x - cell_size, paddle.y + paddle_height // 2)
    if game_of_life.grid[ball_rect.center[1] // cell_size, ball_rect.center[0] // cell_size] == 1:
        # Game over
        font = pygame.font.SysFont(None, font_size)
        text = font.render('Game Over!', True, font_color)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        exit()
    
    # Update the display and wait for the next frame
    pygame.display.flip()
    clock.tick(60)
