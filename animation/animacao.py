import sys
from random import random

import pygame
import pandas as pd
import datetime
from navio import Navio
from porto import Porto
from cais_carregamento import Cais_carregamento
from cais_pagamento import Cais_pagamento

# df = pd.read_csv('dados.csv', sep=',')

pygame.init()
largura = 800
altura = 600
screen = pygame.display.set_mode((largura, altura))

navios = []
tempo_intervalo = 2
# tempo_carregamento = 0.5
# tempo_pagamento = 0.4
navios_count = 190

porto = Porto()
cais_carregamento = Cais_carregamento()
cais_pagamento = Cais_pagamento()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # porto.update()
    screen.fill((255, 255, 255)) # MALDITA COISA TEM Q FICAR ANTES PQPPPPPPPPP

    # tempo para criar navio
    tempo_atual = pygame.time.get_ticks() / 1000
    tempo_proximo_navio = tempo_intervalo

    #Gostaria de usar so esse para instanciar o navio adicionar na fila
    #e ja fazer o desenho
    if len(navios) < navios_count:
        # if tempo_atual >= tempo_proximo_navio:
        navios.append(Navio(len(navios)))
            # print("ATUAL"+str(tempo_atual))
            # print("PROXIMO"+str(tempo_proximo_navio))
            # print(navios[len(navios)-1].id)
            # print("dentro:" + str(navios[len(navios)-1].id))
            # navios[len(navios)-1].draw(screen)
            # tempo_proximo_navio += tempo_intervalo

    #desse jeito desenha certo mas fica instanciando navios.
    flag = 0
    for navio in navios:
        if tempo_atual >= tempo_proximo_navio and flag != navios_count:
            print("ATUAL"+str(tempo_atual))
            print("PROXIMO"+str(tempo_proximo_navio))
            print("dentro:"+str(navio.id))
            navio.draw(screen)
            cais_carregamento.update()
            tempo_proximo_navio += tempo_intervalo
    #     print("fora"+str(navio.id))

    porto.draw(screen)
    cais_carregamento.draw(screen)
    cais_pagamento.draw(screen)

    # pygame.display.flip()
    pygame.display.update()
    pygame.time.Clock().tick(30)
    # pygame.time.delay(10)

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#     # Atualiza a posição dos navios e do cais
#     for navio in navios:
#         navio.draw(screen)
#     Cais_carregamento.draw(screen)
#
#     # Atualiza o estado do cais e dos navios
#     Cais_carregamento.update()
#     for navio in navios:
#         if navio.estado == "saindo":
#             navios.remove(navio)
#
#     # Adiciona novos navios a cada intervalo de tempo
#     if random.random() < 0.02:
#         navios.append(Navio())
#
#     pygame.display.flip()