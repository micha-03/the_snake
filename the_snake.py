# pylint: disable=E1101
"""Snake game"""

import random
import sys

import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BOARD_BACKGROUND_COLOR = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Will be initialized in main
screen = None
clock = None


class GameObject:
    """Base class for game objects."""

    def __init__(self, position, body_color):
        """Initialize game object."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Draw object on screen."""
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 1)


class Apple(GameObject):
    """Apple object."""

    def __init__(self):
        """Initialize apple."""
        super().__init__((0, 0), (255, 0, 0))
        self.randomize_position([])

    def randomize_position(self, occupied_positions):
        """Place apple in random free cell."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in occupied_positions:
                self.position = (x, y)
                return


class Snake(GameObject):
    """Snake object."""

    def __init__(self):
        """Initialize snake."""
        self.positions = [(100, 100)]
        self.direction = RIGHT
        super().__init__(self.positions[0], (0, 200, 0))

    def get_head_position(self):
        """Return snake head position."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Update movement direction."""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def move(self):
        """Move snake."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        self.positions.pop()
        self.position = new_head

    def reset(self):
        """Reset snake to initial state."""
        self.positions = [(100, 100)]
        self.direction = RIGHT
        self.position = self.positions[0]

    def draw(self, surface):
        """Draw snake."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0],
                position[1],
                GRID_SIZE,
                GRID_SIZE,
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)


def handle_keys(snake):
    """Handle keyboard input."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Main game loop."""
    global screen, clock

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.flip()
        clock.tick(10)


if __name__ == '__main__':
    main()
