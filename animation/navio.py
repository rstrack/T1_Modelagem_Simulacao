import pygame
# from cais_carregamento import Cais_carregamento

tempo_carregamento = 0.5
tempo_pagamento = 0.4
# cais = Cais_carregamento()

class Navio:
    def __init__(self, id):
        self.id = id
        # self.chegada = chegada
        # self.carga = carga
        # self.pagamento = pagamento
        self.estado = "saindo" # tvlz seja necessario para controle de fila
        self.posicao = (0, 290)
        self.speed_horizontal = 5
        self.speed_vertical = 0
        self.image = pygame.image.load("./images/navio_t1_direita.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 4, self.image.get_height() // 4))
        self.image_rect = self.image.get_rect()
        self.image_rect.topleft = self.posicao
        self.image.set_colorkey((255, 255, 255))
        self.tempo_espera = 0
        # self.tempo_criacao = pygame.time.get_ticks() / 1000
        # self.tempo_criacao = datetime.datetime.now()
        self.tempo_carregamento = None
        self.tempo_pagamento = None


    def draw(self, screen):

        self.image_rect.x += self.speed_horizontal
        self.image_rect.y += self.speed_vertical
        screen.blit(self.image, self.image_rect)

        if(self.image_rect.x == 370 and self.tempo_carregamento is None and self.estado == "saindo"):
            self.estado = "esperando"
            self.speed_horizontal = 0
            self.tempo_carregamento = pygame.time.get_ticks() / 1000

        if self.tempo_carregamento is not None:
            tempo_atual = pygame.time.get_ticks()/1000
            if tempo_atual - self.tempo_carregamento >= tempo_carregamento:  # passaram 3 segundos
                self.image = pygame.image.load("./images/navio_t1_cima.png")
                self.image = pygame.transform.scale(self.image,
                                                    (self.image.get_width() // 4, self.image.get_height() // 4))
                self.speed_vertical = -5
                self.tempo_carregamento = None  # reseta o tempo de início do carregamento

        # print(self.image_rect.y)
        if (self.image_rect.y == 80 and self.tempo_pagamento is None):
            self.speed_vertical = 0
            self.tempo_pagamento = pygame.time.get_ticks() / 1000

        if self.tempo_pagamento is not None:
            tempo_atual = pygame.time.get_ticks() / 1000
            if tempo_atual - self.tempo_pagamento >= tempo_pagamento:
                self.image = pygame.image.load("./images/navio_t1_cima.png")
                self.image = pygame.transform.scale(self.image,
                                                    (self.image.get_width() // 2.5, self.image.get_height() // 2.5))
                self.speed_vertical = -5
                self.tempo_carregamento = None  # reseta o tempo de início do carregamento
