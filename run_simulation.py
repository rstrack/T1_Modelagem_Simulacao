import pygame
import sys

from modeling.distributions import ExponentialDist, GamaDist, NormalDist
from simulation.navio import Navio
from simulation.porto import Porto
from simulation.cais_carregamento import CaisCarregamento
from simulation.cais_pagamento import CaisPagamento
from util.general_functions import generate_summary, resource_path

HEIGHT = 800
WIDTH = 1200
TOTAL_SHIP_COUNT = 190

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
water_bg = pygame.image.load(resource_path('images/bg-water.jpg'))
water_bg = pygame.transform.scale(water_bg, (WIDTH,HEIGHT))

cais_carregamento = CaisCarregamento()
cais_pagamento = CaisPagamento()
porto = Porto()

exp_dist = ExponentialDist(0.0422)
gama_dist = GamaDist(27.6587, 1.3054)
norm_dist = NormalDist(13.96, 4.27)

navios = []
resumo = []

speed_scale = 5

tempo_gen_navio = pygame.time.get_ticks() / 1000
intervalo_proximo_navio = exp_dist.generate()
tempo_cais1 = gama_dist.generate()
tempo_cais2 = norm_dist.generate()
navios.append(Navio(0, cais_carregamento, tempo_cais1 / speed_scale, cais_pagamento, tempo_cais2 / speed_scale))
cais_carregamento.fila.append(navios[0])
resumo.append([])
resumo.append([tempo_cais1])
resumo.append([tempo_cais2])
print(f'NAVIO 0: TEMPO CAIS CARREGAMENTO: {tempo_cais1} TEMPO CAIS PAGAMENTO: {tempo_cais2}')
print(f'PROXIMO NAVIO EM {intervalo_proximo_navio}')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                speed_scale = 400 if speed_scale == 20 else 20 if speed_scale == 5 else speed_scale
                print(f'Escala: {speed_scale}')

    if len(navios) == TOTAL_SHIP_COUNT and navios[len(navios)-1].image_rect.y <= 0:
        generate_summary(resumo)
        pygame.quit()
        sys.exit()

    screen.blit(water_bg, (0,0))

    font = pygame.font.Font(None, 96)
    label = font.render(f"{speed_scale}x", True, (255, 255, 255))
    screen.blit(label, (10,10))
    
    if (pygame.time.get_ticks() / 1000) >= tempo_gen_navio + intervalo_proximo_navio / speed_scale and len(navios) < TOTAL_SHIP_COUNT:
        tempo_gen_navio =  pygame.time.get_ticks() / 1000
        tempo_cais1 = gama_dist.generate()
        tempo_cais2 = norm_dist.generate()
        print(f'NAVIO {len(navios)}: INTERVALO DE CHEGADA: {tempo_gen_navio} TEMPO CAIS CARREGAMENTO: {tempo_cais1} TEMPO CAIS PAGAMENTO: {tempo_cais2}')
        navios.append(Navio(len(navios), cais_carregamento, tempo_cais1 / speed_scale, cais_pagamento, tempo_cais2 / speed_scale))
        cais_carregamento.fila.append(navios[len(navios)-1])
        resumo[0].append(intervalo_proximo_navio)
        resumo[1].append(tempo_cais1)
        resumo[2].append(tempo_cais2)
        intervalo_proximo_navio = exp_dist.generate()
        # print(f'PROXIMO NAVIO EM {intervalo_proximo_navio}')

    cais_carregamento.update()
    cais_pagamento.update()

    cais_carregamento.draw(screen)
    cais_pagamento.draw(screen)
    
    for navio in navios:
        if navio.image_rect.y > 0:
            navio.update_speed(speed_scale)
            navio.draw(screen)
    

    pygame.display.update()
    pygame.time.Clock().tick(60)

