import pygame

class CaisPagamento:
    def __init__(self):
        self.navio = None
        self.fila = []
        self.rect = pygame.Rect(1100, 80, 60, 160)  # X, Y, Width, Height
        self.color = (100, 120, 200)  # Branco
        self.font = pygame.font.Font(None, 24)  # Define uma fonte de texto

    def update(self):
        if self.navio == None and len(self.fila) > 0:
            self.navio = self.fila.pop(0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        label = self.font.render("Cais Pagamento", True, (0, 0, 0))
        screen.blit(pygame.transform.rotate(label, 90), (self.rect.x + 40, self.rect.y+10))