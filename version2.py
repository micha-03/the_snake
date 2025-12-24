# pylint: disable=no-member,no-name-in-module

"""Juego Snake"""

import random
import sys
from typing import Optional, Tuple

import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

# Configuración de pantalla y rejilla
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FRUIT_SIZE = 20
GAME_SPEED = 10

# Colores
BACKGROUND_COLOR = (144, 238, 144)
SNAKE_COLOR = (128, 128, 128)
FRUIT_COLOR = (255, 0, 0)
BORDER_COLOR = (0, 0, 0)

# Inicialización de pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Direcciones
UP: Tuple[int, int] = (0, -FRUIT_SIZE)
DOWN: Tuple[int, int] = (0, FRUIT_SIZE)
LEFT: Tuple[int, int] = (-FRUIT_SIZE, 0)
RIGHT: Tuple[int, int] = (FRUIT_SIZE, 0)


class Fruit:
    """Representa la fruta del juego."""

    def __init__(self, snake_positions=None):
        """Inicializa la fruta evitando la serpiente."""
        self.position: Tuple[int, int] = (0, 0)
        self.randomize(snake_positions or [])

    def draw(self):
        """Dibuja la fruta."""
        rect = pygame.Rect(self.position, (FRUIT_SIZE, FRUIT_SIZE))
        pygame.draw.rect(screen, FRUIT_COLOR, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize(self, snake_positions):
        """Ubica la fruta en una posición válida."""
        max_x = SCREEN_WIDTH // FRUIT_SIZE
        max_y = SCREEN_HEIGHT // FRUIT_SIZE

        positions = [
            (x * FRUIT_SIZE, y * FRUIT_SIZE)
            for x in range(max_x)
            for y in range(max_y)
            if (x * FRUIT_SIZE, y * FRUIT_SIZE) not in snake_positions
        ]

        self.position = random.choice(positions) if positions else (0, 0)


class Snake:
    """Representa la serpiente."""

    def __init__(self):
        """Inicializa la serpiente."""
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None
        self.new_block: bool = False
        self.positions: list[Tuple[int, int]] = []
        self.reset()

    def reset(self):
        """Reinicia la serpiente."""
        start_x = (SCREEN_WIDTH // 2 // FRUIT_SIZE) * FRUIT_SIZE
        start_y = (SCREEN_HEIGHT // 2 // FRUIT_SIZE) * FRUIT_SIZE
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.new_block = False

    def move(self, fruit: Fruit):
        """Mueve la serpiente y gestiona colisiones."""
        if isinstance(self.next_direction, tuple):
            dx, dy = self.next_direction
            cdx, cdy = self.direction
            if dx + cdx != 0 or dy + cdy != 0:
                self.direction = self.next_direction
            self.next_direction = None

        head_x, head_y = self.positions[-1]
        dx, dy = self.direction
        new_head = ((head_x + dx) % SCREEN_WIDTH, (head_y + dy) % SCREEN_HEIGHT)

        self.positions.append(new_head)

        if new_head == fruit.position:
            self.new_block = True
            fruit.randomize(self.positions)
        elif not self.new_block:
            self.positions.pop(0)
        else:
            self.new_block = False

        if new_head in self.positions[:-1]:
            self.reset()

    def draw(self):
        """Dibuja la serpiente."""
        for pos in self.positions:
            rect = pygame.Rect(pos, (FRUIT_SIZE, FRUIT_SIZE))
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(snake: Snake):
    """Procesa eventos de teclado."""
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                snake.next_direction = UP
            elif event.key == K_DOWN:
                snake.next_direction = DOWN
            elif event.key == K_LEFT:
                snake.next_direction = LEFT
            elif event.key == K_RIGHT:
                snake.next_direction = RIGHT


def main():
    """Función principal del juego."""
    snake = Snake()
    fruit = Fruit(snake.positions)

    while True:
        clock.tick(GAME_SPEED)
        handle_keys(snake)
        snake.move(fruit)

        screen.fill(BACKGROUND_COLOR)
        fruit.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
