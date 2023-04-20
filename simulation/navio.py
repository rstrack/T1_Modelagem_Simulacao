import pygame
from pygame import Surface

SPEED_SCALE = 0.5

class Navio:
    def __init__(self, id, cais_carregamento, tempo_carregamento, cais_pagamento, tempo_pagamento):
        self.id = id
        self.estado = "saindo"
        self.posicao = (0, 390)
        self.speed_horizontal = 5 / SPEED_SCALE
        self.speed_vertical = 0
        self.image = pygame.image.load("./images/navio_t1_direita.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 3, self.image.get_height() // 3))
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = self.posicao
        self.image.set_colorkey((255, 255, 255))
        self.cais_carregamento = cais_carregamento
        self.cais_pagamento = cais_pagamento
        self.tempo_total_carregamento = tempo_carregamento
        self.tempo_inicial_carregamento = None
        self.tempo_total_pagamento = tempo_pagamento
        self.tempo_inicial_pagamento = None

    def draw(self, screen: Surface):

        self.image_rect.x += self.speed_horizontal
        self.image_rect.y += self.speed_vertical
        screen.blit(self.image, self.image_rect)
        
        # cais carregamento

        if self in self.cais_carregamento.fila:
            # print(f'Navio {self.id} : {self.image_rect.x}')
            if self.image_rect.x > 1000 - self.image.get_width() - ((self.cais_carregamento.fila.index(self)) * self.image.get_width()):
                self.speed_horizontal = 0
            else: self.speed_horizontal = 5 / SPEED_SCALE
        elif self.image_rect.x < 1000:
            self.speed_horizontal = 5 / SPEED_SCALE

        if(self.image_rect.x == 1000 and self.tempo_inicial_carregamento is None and self.estado == "saindo"):
            self.estado = "esperando"
            self.speed_horizontal = 0
            self.tempo_inicial_carregamento = pygame.time.get_ticks() / 1000

        if self.tempo_inicial_carregamento is not None:
            tempo_atual = pygame.time.get_ticks()/1000
            if tempo_atual - self.tempo_inicial_carregamento >= self.tempo_total_carregamento:
                self.cais_carregamento.navio = None
                self.image = pygame.transform.rotate(self.image, 90)
                self.speed_vertical = -5 / SPEED_SCALE
                self.tempo_inicial_carregamento = None

        # cais pagamento - falta adicionar fila

        if (self.image_rect.y == 80 and self.tempo_inicial_pagamento is None):
            self.speed_vertical = 0
            self.tempo_inicial_pagamento = pygame.time.get_ticks() / 1000

        if self.tempo_inicial_pagamento is not None:
            tempo_atual = pygame.time.get_ticks() / 1000
            if tempo_atual - self.tempo_inicial_pagamento >= self.tempo_total_pagamento:
                self.speed_vertical = -5 / SPEED_SCALE
                self.tempo_inicial_pagamento = None
