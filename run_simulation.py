
import numpy as np
import os
import pygame
import sys
import datetime

from modeling.distributions import ExponentialDist, GamaDist, NormalDist
from simulation.navio import Navio, SPEED_SCALE
from simulation.porto import Porto
from simulation.cais_carregamento import CaisCarregamento
from simulation.cais_pagamento import CaisPagamento


pygame.init()
WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

navios:list[Navio] = []
TOTAL_SHIP_COUNT = 190
TIME_SCALE = 0.1 / SPEED_SCALE
porto = Porto()
cais_carregamento = CaisCarregamento()
cais_pagamento = CaisPagamento()

exp_dist = ExponentialDist(0.0422)
gama_dist = GamaDist(27.6587, 1.3054)
norm_dist = NormalDist(13.96, 4.27)

resumo = []

tempo_gen_navio = pygame.time.get_ticks() / 1000
intervalo_proximo_navio = exp_dist.generate() * TIME_SCALE
tempo_cais1 = gama_dist.generate()
tempo_cais2 = norm_dist.generate()
navios.append(Navio(0, cais_carregamento, tempo_cais1 * TIME_SCALE, cais_pagamento, tempo_cais2 * TIME_SCALE))
cais_carregamento.fila.append(navios[0])
resumo.append([])
resumo.append([tempo_cais1])
resumo.append([tempo_cais2])
print(f'NAVIO 0: TEMPO CAIS CARREGAMENTO: {tempo_cais1} TEMPO CAIS PAGAMENTO: {tempo_cais2}')
print(f'PROXIMO NAVIO EM {intervalo_proximo_navio}')

water_bg = pygame.image.load('./images/bg-water.jpg')
water_bg = pygame.transform.scale(water_bg, (WIDTH,HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    print(navios[len(navios)-1].image_rect.y)
    if len(navios) == TOTAL_SHIP_COUNT and navios[len(navios)-1].image_rect.y <= 0:
        # TODO: aqui salva os dados no arquivo .txt e abre o arquivo
        file = open('./simulation_summary.txt', 'w')
        file.write('RESUMO DA SIMULAÇÃO\n')
        file.write(f'Data: {datetime.datetime.now()}\n\n')
        file.write('Tempo total da simulação: {:.2f} horas\n\n'.format(np.sum(resumo[0])+np.sum(resumo[1:]) // 1))
        file.write('---------------------------------------------------------\n')
        file.write('INTERVALO ENTRE CHEGADAS:\n')
        file.write(f'Média: {np.mean(resumo[0])}\nDesvio padrão: {np.std(resumo[0])}\nMáx.: {np.max(resumo[0])}\nMin.: {np.min(resumo[0])}\n')
        file.write('---------------------------------------------------------\n')
        file.write('TEMPO DE CARREGAMENTO:\n')
        file.write(f'Média: {np.mean(resumo[1])}\nDesvio padrão: {np.std(resumo[1])}\nMáx.: {np.max(resumo[1])}\nMin.: {np.min(resumo[1])}\n')
        file.write('---------------------------------------------------------\n')
        file.write('TEMPO DE PAGAMENTO E SAÍDA:\n')
        file.write(f'Média: {np.mean(resumo[2])}\nDesvio padrão: {np.std(resumo[2])}\nMáx.: {np.max(resumo[2])}\nMin.: {np.min(resumo[2])}\n')
        file.close()
        os.startfile('simulation_summary.txt')
        pygame.quit()
        sys.exit()

    screen.blit(water_bg, (0,0))
    
    if (pygame.time.get_ticks() / 1000) >= tempo_gen_navio + intervalo_proximo_navio and len(navios) < TOTAL_SHIP_COUNT:
        tempo_gen_navio =  pygame.time.get_ticks() / 1000
        tempo_cais1 = gama_dist.generate()
        tempo_cais2 = norm_dist.generate()
        # print(f'NAVIO {len(navios)}: INTERVALO DE CHEGADA: {tempo_gen_navio} TEMPO CAIS CARREGAMENTO: {tempo_cais1} TEMPO CAIS PAGAMENTO: {tempo_cais2}')
        navios.append(Navio(len(navios), cais_carregamento, tempo_cais1 * TIME_SCALE, cais_pagamento, tempo_cais2 * TIME_SCALE))
        cais_carregamento.fila.append(navios[len(navios)-1])
        resumo[0].append(intervalo_proximo_navio/TIME_SCALE)
        resumo[1].append(tempo_cais1)
        resumo[2].append(tempo_cais2)
        intervalo_proximo_navio = exp_dist.generate() * TIME_SCALE
        # print(f'PROXIMO NAVIO EM {intervalo_proximo_navio}')

    cais_carregamento.update()
    cais_pagamento.update()

    cais_carregamento.draw(screen)
    cais_pagamento.draw(screen)
    
    for navio in navios:
        if navio.image_rect.y > 0:
            navio.draw(screen)
    

    pygame.display.update()
    pygame.time.Clock().tick(240)