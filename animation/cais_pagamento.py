import pygame

class Cais_pagamento:
    def __init__(self):
        self.rect = pygame.Rect(520, 80, 60, 160)  # X, Y, Width, Height
        self.color = (100, 120, 200)  # Branco
        # self.speed = 1
        self.font = pygame.font.Font(None, 24)  # Define uma fonte de texto

    # def update(self):
    #     self.rect.x += self.speed
    #     if(self.rect.x == 800):
    #         self.rect.x = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        # Cria uma superfície de texto
        label = self.font.render("Cais Pagamento", True, (0, 0, 0))

        # Desenha a superfície de texto na tela
        screen.blit(pygame.transform.rotate(label, 90), (self.rect.x + 60, self.rect.y))