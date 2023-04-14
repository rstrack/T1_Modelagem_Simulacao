import time
import numpy

import tests
from gnpcl import GNPCL

EXP = 17
MOD = float(2**EXP - 1)
#a = MOD**(0.5)
a = float(2**(EXP/2))
c = 7

#valores aleatorios iniciais
SEEDS = numpy.random.uniform(size=10)

def generate_test():
    """Gera um arquivo com números aleatórios com dist. uniforme utilizando o numpy, para testes"""
    with open(f'./test.txt', 'w') as file:
        for _ in range(5000000):
            x = numpy.random.uniform()
            file.write(f'{x}\n')

def generate_files():
    """Gera 10 arquivos com 5 MI de números aleatórios com o gerador criado"""
    for file_no in range(1, 11):
        with open(f'./NEWALEO_{file_no}.txt', 'w') as file:
            start_time = time.time()
            gen = GNPCL(SEEDS[file_no-1], EXP, c)
            for _ in range(5000000):
                x = gen.generate()
                file.write(f'{x}\n')
            duration = time.time() - start_time
            print(f'Arquivo {file.name} criado em {duration:.2f} segundos')

def execute_tests():
    """Executa os testes de aleatoriedade nos arquivos gerados"""
    with open('resumo_testes.txt', 'w') as file:
        for file_no in range(10):
            r1 = tests.uniformity_test(f'./NEWALEO_{file_no+1}.txt')
            r2 = tests.runs_test(f'./NEWALEO_{file_no+1}.txt')
            r3 = tests.interval_test(f'./NEWALEO_{file_no+1}.txt')
            r4 = tests.permutation_test(f'./NEWALEO_{file_no+1}.txt')
            file.write(f"ARQUIVO NEWALEO_{file_no+1}.txt\n")
            file.write(f"Teste de uniformidade: {'OK' if r1 else 'Nao Passou'}\n")
            file.write(f"Teste das corridas: {'OK' if r2 else 'Nao Passou'}\n")
            file.write(f"Teste de intervalos: {'OK' if all(map(bool, r3)) else 'Nao Passou'}\n")
            file.write(f"Teste de permutacao: {'OK' if r4 else 'Nao Passou'}\n\n")

if __name__ == '__main__':
    generate_files()
    execute_tests()