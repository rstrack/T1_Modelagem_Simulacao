import pygame
from pygame import Surface

class CaisCarregamento:
    def __init__(self):
        self.navio = None
        self.fila = []
        self.rect = pygame.Rect(1000, 700, 160, 50)
        self.color = (128, 128, 128)
        self.font = pygame.font.Font(None, 24)

    def update(self):
        if self.navio == None and len(self.fila) > 0:
            self.navio = self.fila.pop(0)

    def draw(self, screen: Surface):
        pygame.draw.rect(screen, self.color, self.rect)
        label = self.font.render("Cais Carregamento", True, (0, 0, 0))
        screen.blit(label, (self.rect.x+2, self.rect.y + 30))
