import pygame
# from navio import Navio

tempo_pagamento = 0.25
# navio = Navio()
class Cais_carregamento:
    def __init__(self, idnavio = None):
        self.estado = "livre"
        self.navio_id = idnavio
        self.fila = []
        self.rect = pygame.Rect(400, 400, 160, 50)  # X, Y, Width, Height
        self.color = (255, 0, 255)  # Branco
        # self.speed = 1
        self.font = pygame.font.Font(None, 24)  # Define uma fonte de texto

    def update(self):
        if self.estado == "livre" and len(self.fila > 0):
            self.estado = "ocupado"
            navio = self.fila.pop(0)
            navio.tempo_espera = pygame.time.get_ticks() / 1000 - navio.tempo_espera
            navio.tempo_carregamento = pygame.time.get_ticks() / 1000
            self.navios.append(navio)

            # verifica se algum navio já foi carregado
            for navio in self.navios:
                if navio.tempo_pagamento is not None:
                    tempo_atual = pygame.time.get_ticks() / 1000
                    if tempo_atual - navio.tempo_pagamento >= tempo_pagamento:
                        self.navios.remove(navio)
                        self.estado = "livre"

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        # Cria uma superfície de texto
        label = self.font.render("Cais Carregamento", True, (0, 0, 0))
        # Desenha a superfície de texto na tela
        screen.blit(label, (self.rect.x, self.rect.y + 50))
