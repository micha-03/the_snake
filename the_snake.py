"""
Juego Snake clasico
"""
import sys
import subprocess
import random

# Verificar e instalar pygame si es necesario
try:
    import pygame
    from pygame import USEREVENT, QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT
    from pygame.math import Vector2
except ImportError:
    print("Pygame no encontrado. Instalando...")
    try:
        # Instalacion silenciosa de pygame
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "pygame"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import pygame
        from pygame import USEREVENT, QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, 
        from pygame import K_RIGHT
        from pygame.math import Vector2
        print("Pygame instalado exitosamente")
    except (subprocess.CalledProcessError, ImportError) as e:
        print(f"Error al instalar pygame: {e}")
        sys.exit(1)

# Configuracion del juego
FRUIT_COLOR = (255, 0, 0)
SNAKE_COLOR = (128, 128, 128)
BACKGROUND_COLOR = (144, 238, 144)
FRUIT_SIZE = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_SPEED = 150
SCREEN_UPDATE = USEREVENT + 1


class Fruits:
    """Clase para la fruta del juego"""

    def __init__(self):
        self.position = Vector2(0, 0)
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
        max_x = SCREEN_WIDTH // FRUIT_SIZE
        max_y = SCREEN_HEIGHT // FRUIT_SIZE

        for _ in range(100):  # Intentar maximo 100 veces
            x_pos = random.randint(0, max_x - 1) * FRUIT_SIZE
            y_pos = random.randint(0, max_y - 1) * FRUIT_SIZE
            candidate = Vector2(x_pos, y_pos)
            if candidate not in occupied_positions:
                self.position = candidate
                return
        # Fallback si no encuentra posicion libre
        self.position = Vector2(FRUIT_SIZE, FRUIT_SIZE)


class Snake:
    """Clase para la serpiente del juego"""

    def __init__(self):
        self.body = [
            Vector2(100, 100),
            Vector2(80, 100),
            Vector2(60, 100)
        ]
        self.direction = Vector2(FRUIT_SIZE, 0)
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

        if self.new_block:
            new_body = [self.body[0] + self.direction] + self.body
            self.body = new_body
            self.new_block = False
        else:
            new_body = [self.body[0] + self.direction] + self.body[:-1]
            self.body = new_body

        # Ajustar posicion si se sale de la pantalla
        head = self.body[0]
        if head.x >= SCREEN_WIDTH:
            head.x = 0
        elif head.x < 0:
            head.x = SCREEN_WIDTH - FRUIT_SIZE
        if head.y >= SCREEN_HEIGHT:
            head.y = 0
        elif head.y < 0:
            head.y = SCREEN_HEIGHT - FRUIT_SIZE


def handle_event(event, snake_obj):
    """Maneja los eventos del juego"""
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    if event.type == SCREEN_UPDATE:
        snake_obj.move()
    if event.type == KEYDOWN:
        if event.key == K_UP and snake_obj.direction.y == 0:
            snake_obj.direction = Vector2(0, -FRUIT_SIZE)
        elif event.key == K_DOWN and snake_obj.direction.y == 0:
            snake_obj.direction = Vector2(0, FRUIT_SIZE)
        elif event.key == K_LEFT and snake_obj.direction.x == 0:
            snake_obj.direction = Vector2(-FRUIT_SIZE, 0)
        elif event.key == K_RIGHT and snake_obj.direction.x == 0:
            snake_obj.direction = Vector2(FRUIT_SIZE, 0)


def check_eat(snake_obj, fruit_obj):
    """Verifica si la serpiente come la fruta"""
    head = snake_obj.body[0]
    if head == fruit_obj.position:
        snake_obj.new_block = True
        fruit_obj.randomize(snake_obj.body)
        return True
    return False


def check_self_collision(snake_obj):
    """Verifica colision con si misma"""
    head = snake_obj.body[0]
    return any(head == segment for segment in snake_obj.body[1:])


def main():
    """Funcion principal del juego"""
    # Inicializar pygame
    pygame.init()

    # Crear ventana
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    # Crear objetos del juego
    clock = pygame.time.Clock()
    fruit = Fruits()
    snake = Snake()

    # Configurar timer para actualizacion del juego
    pygame.time.set_timer(SCREEN_UPDATE, GAME_SPEED)

    # Bucle principal del juego
    running = True
    while running:
        # Manejar eventos
        for event in pygame.event.get():
            handle_event(event, snake)

        # Verificar colisiones
        if check_self_collision(snake):
            running = False

        # Verificar si come fruta
        check_eat(snake, fruit)

        # Dibujar todo
        screen.fill(BACKGROUND_COLOR)
        fruit.draw(screen)
        snake.draw(screen)
        pygame.display.update()

        # Controlar FPS
        clock.tick(60)

    # Salir del juego
    pygame.quit()


if __name__ == "__main__":
    main()
