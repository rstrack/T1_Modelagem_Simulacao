import pygame

class Porto:
    def __init__(self):
        self.rect = pygame.Rect(0, 400, 150, 80)  # X, Y, Width, Height
        self.color = (255, 255, 0)  # Branco
        self.speed = 1
        self.navios = []
        self.font = pygame.font.Font(None, 24)  # Define uma fonte de texto

    # def update(self):
    #     self.rect.x += self.speed
    #     if(self.rect.x == 800):
    #         self.rect.x = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        # Cria uma superfície de texto
        label = self.font.render("Porto", True, (0, 0, 0))
        # Desenha a superfície de texto na tela
        screen.blit(label, (self.rect.x, self.rect.y + 80))
