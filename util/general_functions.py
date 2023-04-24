import os
import sys
import numpy as np
from datetime import datetime


def resource_path(relative_path: str):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def generate_summary(summary: list[float]):
    file = open(resource_path('./simulation_summary.txt'), 'w')
    file.write('RESUMO DA SIMULAÇÃO\n')
    file.write(f'Data: {datetime.now()}\n\n')
    file.write('Tempo total da simulação: {:.2f} horas\n\n'.format(np.sum(summary[0])+np.sum(summary[1:]) // 1))
    file.write('---------------------------------------------------------\n')
    file.write('INTERVALO ENTRE CHEGADAS:\n')
    file.write(f'Média: {np.mean(summary[0])}\nDesvio padrão: {np.std(summary[0])}\nMáx.: {np.max(summary[0])}\nMin.: {np.min(summary[0])}\n')
    file.write('---------------------------------------------------------\n')
    file.write('TEMPO DE CARREGAMENTO:\n')
    file.write(f'Média: {np.mean(summary[1])}\nDesvio padrão: {np.std(summary[1])}\nMáx.: {np.max(summary[1])}\nMin.: {np.min(summary[1])}\n')
    file.write('---------------------------------------------------------\n')
    file.write('TEMPO DE PAGAMENTO E SAÍDA:\n')
    file.write(f'Média: {np.mean(summary[2])}\nDesvio padrão: {np.std(summary[2])}\nMáx.: {np.max(summary[2])}\nMin.: {np.min(summary[2])}\n')
    file.close()
    os.startfile(resource_path('simulation_summary.txt'))