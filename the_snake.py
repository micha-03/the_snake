import sys
import random
import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    USEREVENT,
)
from pygame.math import Vector2

FRUIT_COLOR = (255, 0, 0)  # ROJO para la manzana
SNAKE_COLOR = (128, 128, 128)  # GRIS para la serpiente
BACKGROUND_COLOR = (144, 238, 144)  # VERDE para el fondo
FRUIT_SIZE = 20

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Fruits:
    """Fruta del juego. Se posiciona aleatoriamente evitando la serpiente."""

    def __init__(self):
        self.position = Vector2(0, 0)
        self.randomize([])

    def draw(self, screen) -> None:
        rect = pygame.Rect(
            int(self.position.x),
            int(self.position.y),
            FRUIT_SIZE,
            FRUIT_SIZE,
        )
        pygame.draw.rect(screen, FRUIT_COLOR, rect)

    def randomize(self, occupied_positions) -> None:
        while True:
            x = random.randrange(0, SCREEN_WIDTH, FRUIT_SIZE)
            y = random.randrange(0, SCREEN_HEIGHT, FRUIT_SIZE)
            candidate = Vector2(x, y)
            if candidate not in occupied_positions:
                self.position = candidate
                return


class Snake:
    """Serpiente controlada por el jugador."""

    def __init__(self):
        self.body = [Vector2(100, 100), Vector2(80, 100), Vector2(60, 100)]
        self.direction = Vector2(FRUIT_SIZE, 0)
        self.new_block = False

    def draw(self, screen) -> None:
        for segment in self.body:
            x_pos = int(segment.x)
            y_pos = int(segment.y)
            segment_rect = pygame.Rect(x_pos, y_pos, FRUIT_SIZE, FRUIT_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, segment_rect)

    def move(self) -> None:
        if self.direction.length() == 0:
            return

        new_head = self.body[0] + self.direction

        # Wrap around en los bordes
        if new_head.x >= SCREEN_WIDTH:
            new_head.x = 0
        elif new_head.x < 0:
            new_head.x = SCREEN_WIDTH - FRUIT_SIZE
        if new_head.y >= SCREEN_HEIGHT:
            new_head.y = 0
        elif new_head.y < 0:
            new_head.y = SCREEN_HEIGHT - FRUIT_SIZE

        if self.new_block:
            self.body.insert(0, new_head)
            self.new_block = False
        else:
            self.body.insert(0, new_head)
            self.body.pop()


def handle_event(event: pygame.event.Event, snake_obj: Snake) -> None:
    """Procesa eventos y actualiza la dirección o estado."""
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    if event.type == SCREEN_UPDATE:
        snake_obj.move()
    if event.type == KEYDOWN:
        if event.key == K_UP and snake_obj.direction.y <= 0:
            snake_obj.direction = Vector2(0, -FRUIT_SIZE)
        elif event.key == K_DOWN and snake_obj.direction.y >= 0:
            snake_obj.direction = Vector2(0, FRUIT_SIZE)
        elif event.key == K_LEFT and snake_obj.direction.x <= 0:
            snake_obj.direction = Vector2(-FRUIT_SIZE, 0)
        elif event.key == K_RIGHT and snake_obj.direction.x >= 0:
            snake_obj.direction = Vector2(FRUIT_SIZE, 0)


def check_eat(snake_obj: Snake, fruit_obj: Fruits) -> None:
    """Comprueba si la serpiente come la fruta y la reubica."""
    head = snake_obj.body[0]
    head_rect = pygame.Rect(head.x, head.y, FRUIT_SIZE, FRUIT_SIZE)
    fruit_rect = pygame.Rect(fruit_obj.position.x,
                             fruit_obj.position.y, FRUIT_SIZE, FRUIT_SIZE)

    if head_rect.colliderect(fruit_rect):
        snake_obj.new_block = True
        fruit_obj.randomize(snake_obj.body)


def check_self_collision(snake_obj: Snake) -> bool:
    """Verifica si la serpiente choca consigo misma."""
    head = snake_obj.body[0]
    for segment in snake_obj.body[1:]:
        if head == segment:
            return True
    return False


# Inicialización de pygame
pygame.init()
pygame.display.set_caption("Snake Game")

# COLORES DEFINIDOS ARRIBA - ya no necesitamos WHITE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Creación de objetos
fruit = Fruits()
snake = Snake()

SCREEN_UPDATE = USEREVENT + 1
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        handle_event(event, snake)

    # Verificar colisión consigo misma
    if check_self_collision(snake):
        running = False

    # Verificar si come fruta
    check_eat(snake, fruit)

    # Dibujar todo con nuevos colores
    screen.fill(BACKGROUND_COLOR)  # FONDO VERDE
    fruit.draw(screen)  # MANZANA ROJA
    snake.draw(screen)  # SERPIENTE GRIS

    pygame.display.update()
    clock.tick(60)

# Salir del juego
pygame.quit()
