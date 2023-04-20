import sys

import pygame

from simulacao.navio import Navio, SPEED_SCALE
from simulacao.porto import Porto
from simulacao.cais_carregamento import Cais_carregamento
from simulacao.cais_pagamento import Cais_pagamento

from modelagem.distributions import ExponentialDist, GamaDist, NormalDist

pygame.init()
WIDTH = 1200
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

navios:list[Navio] = []
TOTAL_SHIP_COUNT = 190
TIME_SCALE = SPEED_SCALE * 0.1
porto = Porto()
cais_carregamento = Cais_carregamento()
cais_pagamento = Cais_pagamento()

exp_dist = ExponentialDist(0.0422)
gama_dist = GamaDist(27.6587, 1.3054)
norm_dist = NormalDist(13.96, 4.27)

resumo = []

tempo_gen_navio = pygame.time.get_ticks() / 1000
intervalo_proximo_navio = exp_dist.generate() * TIME_SCALE
tempo_cais1 = gama_dist.generate() * TIME_SCALE
tempo_cais2 = norm_dist.generate() * TIME_SCALE
navios.append(Navio(0, cais_carregamento, tempo_cais1, cais_pagamento, tempo_cais2))
cais_carregamento.fila.append(navios[0])
resumo.append([0, tempo_cais1, tempo_cais2])
print(f'NAVIO 0: TEMPO CAIS CARREGAMENTO: {tempo_cais1} TEMPO CAIS PAGAMENTO: {tempo_cais2}')
print(f'PROXIMO NAVIO EM {intervalo_proximo_navio}')

water_bg = pygame.image.load('./images/bg-water.jpg')
water_bg = pygame.transform.scale(water_bg, (WIDTH,HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    if len(navios) == TOTAL_SHIP_COUNT and navios[len(navios)-1].tempo_total_carregamento + navios[len(navios)-1].tempo_total_pagamento:
        pygame.quit()
        sys.exit()

    screen.blit(water_bg, (0,0))
    # screen.fill((255, 255, 255))
    
    if (pygame.time.get_ticks() / 1000) >= tempo_gen_navio + intervalo_proximo_navio:
        tempo_gen_navio =  pygame.time.get_ticks() / 1000
        tempo_cais1 = gama_dist.generate() * TIME_SCALE
        tempo_cais2 = norm_dist.generate() * TIME_SCALE
        print(f'NAVIO {len(navios)}: INTERVALO DE CHEGADA: {tempo_gen_navio} TEMPO CAIS CARREGAMENTO: {tempo_cais1} TEMPO CAIS PAGAMENTO: {tempo_cais2}')
        navios.append(Navio(len(navios), cais_carregamento, tempo_cais1, cais_pagamento, tempo_cais2))
        cais_carregamento.fila.append(navios[len(navios)-1])
        resumo.append([intervalo_proximo_navio, tempo_cais1, tempo_cais2])
        intervalo_proximo_navio = exp_dist.generate() * TIME_SCALE
        print(f'PROXIMO NAVIO EM {intervalo_proximo_navio}')

    cais_carregamento.update()
    cais_pagamento.update()
    
    for navio in navios:
        if 0 < navio.image_rect.x or navio.image_rect.x < WIDTH or 0 < navio.image_rect.x or navio.image_rect.x < HEIGHT:
            navio.draw(screen)

    cais_carregamento.draw(screen)
    cais_pagamento.draw(screen)

    pygame.display.update()
    pygame.time.Clock().tick(240)