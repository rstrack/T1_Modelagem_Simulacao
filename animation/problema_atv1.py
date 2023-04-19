import pygame
import random
import time

# Define as constantes do jogo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHIP_COUNT = 190
SHIP_SPEED = 5
LOADING_TIME = 60
PAYMENT_TIME = 30
ARRIVAL_INTERVAL = 60

# Define as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Inicializa o pygame
pygame.init()

# Cria a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define o título da janela
pygame.display.set_caption("Simulação de Navios Cargueiros Petroleiros")

# Define as fontes do jogo
font = pygame.font.SysFont(None, 24)

# Define as variáveis do jogo
ships = []
loading_docks = [False, False]
payment_docks = [False, False]
last_arrival_time = 0
total_waiting_time = 0
total_loading_time = 0
total_payment_time = 0
total_time = 0


# Define as classes do jogo
class Ship:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.loading_time = 0
        self.payment_time = 0
        self.loading_dock = None
        self.payment_dock = None
        self.waiting_time = 0
        self.loaded = False
        self.paid = False

    def update(self):
        if self.loading_time > 0:
            self.loading_time -= 1
        elif not self.loaded and self.loading_dock is not None:
            self.loaded = True
            loading_docks[self.loading_dock] = False
            self.loading_dock = None
            global total_loading_time
            total_loading_time += LOADING_TIME

        if self.payment_time > 0:
            self.payment_time -= 1
        elif self.loaded and not self.paid and self.payment_dock is not None:
            self.paid = True
            payment_docks[self.payment_dock] = False
            self.payment_dock = None
            global total_payment_time
            total_payment_time += PAYMENT_TIME

    def draw(self):
        if not self.loaded and not self.paid:
            color = WHITE
        elif self.loaded and not self.paid:
            color = (255, 255, 0)
        elif self.loaded and self.paid:
            color = (0, 255, 0)
        else:
            color = BLACK

        # pygame.draw.circle(screen, color, (int(self.waiting_time * SHIP_SPEED), 50), 5)
        pygame.draw.circle(screen, color, (min(int(self.waiting_time * SHIP_SPEED), SCREEN_WIDTH - 5), 50), 5)

    def set_loading_dock(self, dock):
        self.loading_dock = dock
        self.loading_time = LOADING_TIME

    def set_payment_dock(self, dock):
        self.payment_dock = dock
        self.payment_time = PAYMENT_TIME


# Define as funções do jogo
def spawn_ship():
    global last_arrival_time
    global ships
    global total_waiting_time
    ships.append(Ship(last_arrival_time))
    last_arrival_time = time.time()


def find_loading_dock():
    global loading_docks
    for i in range(len(loading_docks)):
        if not loading_docks[i]:
            loading_docks[i] = True
            return i
    return None


def find_payment_dock():
    global payment_docks
    for i in range(len(payment_docks)):
        if not payment_docks[i]:
            payment_docks[i] = True
            return i
    return None


# Loop principal do jogo
running = True
clock = pygame.time.Clock()

while running:
    # Eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Verifica se é hora de criar um novo navio
    if time.time() - last_arrival_time >= ARRIVAL_INTERVAL and len(ships) < SHIP_COUNT:
        spawn_ship()

    # Atualiza a lógica do jogo para cada navio
    for ship in ships:
        # Verifica se o navio está esperando para carregar
        if not ship.loaded and not ship.loading_dock:
            loading_dock = find_loading_dock()
            if loading_dock is not None:
                ship.set_loading_dock(loading_dock)
            else:
                ship.waiting_time += 1
                total_waiting_time += 1

        # Verifica se o navio está esperando para pagar
        if ship.loaded and not ship.paid and not ship.payment_dock:
            payment_dock = find_payment_dock()
            if payment_dock is not None:
                ship.set_payment_dock(payment_dock)
            else:
                ship.waiting_time += 1
                total_waiting_time += 1

        # Atualiza o navio
        ship.update()

    # Limpa a tela
    screen.fill(BLACK)

    # Desenha os objetos na tela
    for ship in ships:
        ship.draw()

    # Exibe as estatísticas do jogo na tela
    total_time += 1
    if total_time % 60 == 0:
        avg_waiting_time = total_waiting_time / len(ships)
        avg_loading_time = total_loading_time / SHIP_COUNT
        avg_payment_time = total_payment_time / SHIP_COUNT
        stats = f"Tempo médio de espera: {avg_waiting_time:.2f}s | Tempo médio de carregamento: {avg_loading_time:.2f}s | Tempo médio de pagamento: {avg_payment_time:.2f}s"
        text = font.render(stats, True, WHITE)
        screen.blit(text, (10, 10))

    # Atualiza a tela
    pygame.display.update()
    pygame.display.flip()

    # Controla a velocidade do jogo
    clock.tick(60)

# Encerra o pygame
pygame.quit()

# # Loop principal do jogo
# running = True
# clock = pygame.time.Clock()
#
# while running:
#     # Eventos do jogo
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # Verifica se é hora de criar um novo navio
#     if time.time() - last_arrival_time >= ARRIVAL_INTERVAL and len(ships) < SHIP_COUNT:
#         spawn_ship()
#
#     # Atualiza a lógica do jogo para cada navio
#     for ship in ships:
#         # Verifica se o navio está esperando para carregar
#         if not ship.loaded and not ship.loading_dock:
#             loading_dock = find_loading_dock()
#             if loading_dock is not None:
#                 ship.set_loading_dock(loading_dock)
#             else:
#                 ship.waiting_time += 1
#                 total_waiting_time += 1
#
#         # Verifica se o navio está esperando para pagar
#         if ship.loaded and not ship.paid and not ship.payment_dock:
#             payment_dock = find_payment_dock()
#             if payment_dock is not None:
#                 ship.set_payment_dock(payment_dock)
#             else:
#                 ship.waiting_time += 1
#                 total_waiting_time += 1
#
#         # Atualiza o navio
#         ship.update()
#
#     # Limpa a tela
#     screen.fill(BLACK)
#
#     # Desenha os objetos na tela
#     for ship in ships:
#         ship.draw()
#
#     # Exibe as estatísticas do jogo na tela
#     total_time += 1
#     if total_time % 60 == 0:
#         avg_waiting_time = total_waiting_time / len(ships)
#         avg_loading_time = total_loading_time / SHIP_COUNT
#         avg_payment_time = total_payment_time / SHIP_COUNT
#         stats = f"Tempo médio de espera: {avg_waiting_time:.2f}s | Tempo médio de carregamento: {avg_loading_time:.2f}s | Tempo médio de pagamento: {avg_payment_time:.2f}s"
#         text = font.render(stats, True, WHITE)
#         screen.blit(text, (10, 10))
#
#     # Atualiza a tela
#     pygame.display.update()
#
#     # Limita a taxa de atualização do jogo
#     clock.tick(60)
#
# # Encerra o pygame
# pygame.quit()

