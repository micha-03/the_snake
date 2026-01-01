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

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Base class for game objects."""

    def __init__(self):
        self.position = (0, 0)
        self.body_color = (255, 255, 255)

    def draw(self, surface):
        """Draw the object on the surface."""
        pass


class Apple(GameObject):
    """Apple object."""

    def __init__(self):
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position([])

    def randomize_position(self, occupied_positions):
        """Place apple in random free cell."""
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in occupied_positions:
                self.position = (x, y)
                return

    def draw(self, surface):
        """Draw the apple on the surface."""
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE,
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Snake object."""

    def __init__(self):
        super().__init__()
        self.positions = [(100, 100)]
        self.direction = RIGHT
        self.body_color = (0, 200, 0)
        self.position = self.positions[0]

    def get_head_position(self):
        """Return the position of the snake's head. """
        return self.positions[0]

    def update_direction(self, new_direction):
        """Update the snake's direction."""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def move(self):
        """Move the snake in the current direction."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        self.positions.pop()
        self.position = new_head

    def grow(self):
        """Grow the snake by adding a new segment."""
        self.positions.append(self.positions[-1])

    def reset(self):
        """Reset the snake to the initial state."""
        self.positions = [(100, 100)]
        self.direction = RIGHT
        self.position = self.positions[0]

    def draw(self, surface):
        """Draw the snake on the surface."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0],
                position[1],
                GRID_SIZE,
                GRID_SIZE,
            )
            pygame.draw.rect(surface, self.body_color, rect)


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
    snake = Snake()
    apple = Apple()

    running = True
    while running:
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()
