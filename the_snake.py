# pylint: disable=E1101
'''Juego Snake clasico.'''
import random
import sys
import pygame

# Configuración del juego
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FRUIT_SIZE = 20
GAME_SPEED = 150

BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 200, 0)
FRUIT_COLOR = (255, 0, 0)
BORDER_COLOR = (0, 0, 0)

SCREEN_UPDATE = pygame.USEREVENT + 1


class Fruit:
    '''Representa la fruta del juego.'''

    def __init__(self):
        '''Inicializa la fruta.'''
        self.position = (0, 0)
        self.randomize([])

    def randomize(self, occupied_positions):
        '''Coloca la fruta en una posición libre.'''
        max_x = SCREEN_WIDTH // FRUIT_SIZE
        max_y = SCREEN_HEIGHT // FRUIT_SIZE
        for _ in range(100):
            x_pos = random.randint(0, max_x - 1) * FRUIT_SIZE
            y_pos = random.randint(0, max_y - 1) * FRUIT_SIZE
            if (x_pos, y_pos) not in occupied_positions:
                self.position = (x_pos, y_pos)
                return
        self.position = (FRUIT_SIZE, FRUIT_SIZE)

    def draw(self, screen):
        '''Dibuja la fruta.'''
        rect = pygame.Rect(self.position[0], self.position[1], FRUIT_SIZE,
                           FRUIT_SIZE)
        pygame.draw.rect(screen, FRUIT_COLOR, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake:
    '''Representa la serpiente.'''

    def __init__(self):
        '''Inicializa la serpiente.'''
        self.body = [(100, 100)]
        self.direction = (FRUIT_SIZE, 0)
        self.grow = False

    def move(self):
        '''Mueve la serpiente.'''
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % SCREEN_WIDTH,
                    (head_y + dy) % SCREEN_HEIGHT)
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def draw(self, screen):
        '''Dibuja la serpiente.'''
        for segment in self.body:
            rect = pygame.Rect(segment[0], segment[1], FRUIT_SIZE, FRUIT_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def check_self_collision(self):
        '''Detecta colisión consigo misma.'''
        return self.body[0] in self.body[1:]


def handle_events(snake):
    '''Gestiona eventos del teclado.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            dx, dy = snake.direction
            if event.key == pygame.K_UP and dy == 0:
                snake.direction = (0, -FRUIT_SIZE)
            elif event.key == pygame.K_DOWN and dy == 0:
                snake.direction = (0, FRUIT_SIZE)
            elif event.key == pygame.K_LEFT and dx == 0:
                snake.direction = (-FRUIT_SIZE, 0)
            elif event.key == pygame.K_RIGHT and dx == 0:
                snake.direction = (FRUIT_SIZE, 0)
        if event.type == SCREEN_UPDATE:
            snake.move()


def main():
    '''Función principal del juego.'''
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    snake = Snake()
    fruit = Fruit()
    pygame.time.set_timer(SCREEN_UPDATE, GAME_SPEED)

    while True:
        handle_events(snake)

        if snake.body[0] == fruit.position:
            snake.grow = True
            fruit.randomize(snake.body)

        if snake.check_self_collision():
            pygame.quit()
            sys.exit()

        screen.fill(BACKGROUND_COLOR)
        fruit.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
