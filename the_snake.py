"""
Juego Snake clasico
"""
import sys
import random
import pygame

# Configuracion del juego
FRUIT_COLOR = (255, 0, 0)
SNAKE_COLOR = (128, 128, 128)
BACKGROUND_COLOR = (144, 238, 144)
FRUIT_SIZE = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_SPEED = 150
SCREEN_UPDATE = pygame.USEREVENT + 1


class Fruits:
    """Clase para la fruta del juego"""
    def __init__(self):
        self.position = pygame.math.Vector2(0, 0)
        self.randomize([])

    def draw(self, screen):
        """Dibuja la fruta en pantalla"""
        rect = pygame.Rect(
            int(self.position.x),
            int(self.position.y),
            FRUIT_SIZE,
            FRUIT_SIZE,
        )
        pygame.draw.rect(screen, FRUIT_COLOR, rect)

    def randomize(self, occupied_positions):
        """Coloca la fruta en posicion aleatoria"""
        while True:
            x = random.randrange(0, SCREEN_WIDTH, FRUIT_SIZE)
            y = random.randrange(0, SCREEN_HEIGHT, FRUIT_SIZE)
            candidate = pygame.math.Vector2(x, y)
            if candidate not in occupied_positions:
                self.position = candidate
                return


class Snake:
    """Clase para la serpiente del juego"""
    def __init__(self):
        self.body = [
            pygame.math.Vector2(100, 100),
            pygame.math.Vector2(80, 100),
            pygame.math.Vector2(60, 100)
        ]
        self.direction = pygame.math.Vector2(FRUIT_SIZE, 0)
        self.new_block = False

    def draw(self, screen):
        """Dibuja la serpiente en pantalla"""
        for segment in self.body:
            x_pos = int(segment.x)
            y_pos = int(segment.y)
            segment_rect = pygame.Rect(x_pos, y_pos, FRUIT_SIZE, FRUIT_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, segment_rect)

    def move(self):
        """Mueve la serpiente"""
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


def handle_event(event, snake_obj):
    """Maneja los eventos del juego"""
    if event.type == pygame.QUIT:
        pygame.quit()  # pylint: disable=no-member
        sys.exit()
    if event.type == SCREEN_UPDATE:
        snake_obj.move()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP and snake_obj.direction.y <= 0:
            snake_obj.direction = pygame.math.Vector2(0, -FRUIT_SIZE)
        elif event.key == pygame.K_DOWN and snake_obj.direction.y >= 0:
            snake_obj.direction = pygame.math.Vector2(0, FRUIT_SIZE)
        elif event.key == pygame.K_LEFT and snake_obj.direction.x <= 0:
            snake_obj.direction = pygame.math.Vector2(-FRUIT_SIZE, 0)
        elif event.key == pygame.K_RIGHT and snake_obj.direction.x >= 0:
            snake_obj.direction = pygame.math.Vector2(FRUIT_SIZE, 0)


def check_eat(snake_obj, fruit_obj):
    """Verifica si la serpiente come la fruta"""
    head = snake_obj.body[0]
    head_rect = pygame.Rect(head.x, head.y, FRUIT_SIZE, FRUIT_SIZE)
    fruit_rect = pygame.Rect(
        fruit_obj.position.x,
        fruit_obj.position.y,
        FRUIT_SIZE,
        FRUIT_SIZE
    )

    if head_rect.colliderect(fruit_rect):
        snake_obj.new_block = True
        fruit_obj.randomize(snake_obj.body)


def check_self_collision(snake_obj):
    """Verifica colision con si misma"""
    head = snake_obj.body[0]
    for segment in snake_obj.body[1:]:
        if head == segment:
            return True
    return False


def main():
    """Funcion principal del juego"""
    pygame.init()  # pylint: disable=no-member
    pygame.display.set_caption("Snake Game")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    fruit = Fruits()
    snake = Snake()

    pygame.time.set_timer(SCREEN_UPDATE, GAME_SPEED)

    running = True
    while running:
        for event in pygame.event.get():
            handle_event(event, snake)

        if check_self_collision(snake):
            running = False

        check_eat(snake, fruit)
        screen.fill(BACKGROUND_COLOR)
        fruit.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()  # pylint: disable=no-member


if __name__ == "__main__":
    main()
