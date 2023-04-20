import pygame
from pygame import Surface

from simulation.cais_carregamento import CaisCarregamento
from simulation.cais_pagamento import CaisPagamento

# speed_scale: 200x = 3s aprox.

class Navio:
    def __init__(
            self, 
            id: int, 
            cais_carregamento: CaisCarregamento, 
            tempo_carregamento: float, 
            cais_pagamento: CaisPagamento, 
            tempo_pagamento: float
        ):
        self.id = id
        self.estado = "entrando"
        self.speed_scale = 1
        self.speed_horizontal = 5 * self.speed_scale
        self.speed_vertical = 0
        self.image = pygame.image.load("./images/navio_t1_direita.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 3, self.image.get_height() // 3))
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = (0, 590)
        self.image.set_colorkey((255, 255, 255))
        self.cais_carregamento = cais_carregamento
        self.cais_pagamento = cais_pagamento
        self.tempo_total_carregamento = tempo_carregamento
        self.tempo_inicial_carregamento = None
        self.tempo_total_pagamento = tempo_pagamento
        self.tempo_inicial_pagamento = None

    def update_speed(self, new_scale):
        self.tempo_total_carregamento = self.tempo_total_carregamento / (new_scale / self.speed_scale)
        self.tempo_total_pagamento = self.tempo_total_pagamento / (new_scale / self.speed_scale)
        self.speed_scale = new_scale

    def draw(self, screen: Surface):

        self.image_rect.x += self.speed_horizontal
        self.image_rect.y += self.speed_vertical
        screen.blit(self.image, self.image_rect)
        
        # cais carregamento
        if self in self.cais_carregamento.fila:
            if self.image_rect.x > 1000 - self.image.get_width() - ((self.cais_carregamento.fila.index(self)) * self.image.get_width()):
                self.speed_horizontal = 0
            else: self.speed_horizontal = 5 * self.speed_scale
        elif self.image_rect.x < 1000:
            self.speed_horizontal = 5 * self.speed_scale

        if(self.image_rect.x >= 1000 and self.tempo_inicial_carregamento is None and self.estado == "entrando"):
            self.estado = "carregando"
            self.speed_horizontal = 0
            self.tempo_inicial_carregamento = pygame.time.get_ticks() / 1000

        if self.tempo_inicial_carregamento is not None and self.estado == "carregando":
            # print(f'Carregando: Navio {self.id}')
            tempo_atual = pygame.time.get_ticks()/1000
            if tempo_atual - self.tempo_inicial_carregamento >= self.tempo_total_carregamento:
                self.estado = "saindo carregamento"
                self.cais_carregamento.navio = None
                self.image = pygame.transform.rotate(self.image, 90)
                self.speed_vertical = -5 * self.speed_scale
                self.tempo_inicial_carregamento = None
                self.cais_pagamento.fila.append(self)

        # cais pagamento - falta adicionar fila
        if self.estado == "saindo carregamento":
            if self.speed_scale < 6:
                if self in self.cais_pagamento.fila:
                    if self.image_rect.y < 80 + self.image.get_height() + ((self.cais_pagamento.fila.index(self)) * self.image.get_height()):
                        self.speed_vertical = 0
                    else: self.speed_vertical = -5 * self.speed_scale
                elif self.image_rect.y > 80:
                    self.speed_vertical = -5 * self.speed_scale
            else: self.cais_pagamento.fila = []

            if (self.image_rect.y < 80 and self.tempo_inicial_pagamento is None):
                self.estado = "pagando"
                self.speed_vertical = 0
                self.tempo_inicial_pagamento = pygame.time.get_ticks() / 1000

        if self.tempo_inicial_pagamento is not None and self.estado == "pagando":
            # print(f'Pagando: Navio {self.id}')
            tempo_atual = pygame.time.get_ticks() / 1000
            if tempo_atual - self.tempo_inicial_pagamento >= self.tempo_total_pagamento:
                # print(f'Navio {self.id}: entrou')
                self.estado = 'saindo'
                self.speed_vertical = -5 * self.speed_scale
                self.tempo_inicial_pagamento = None
                self.cais_pagamento.navio = None

        # print(f'Navio {self.id}: {self.estado}')
