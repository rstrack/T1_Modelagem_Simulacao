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
SEEDS = [
    123,
    126540,
    1,
    97845461,
    145616,
    4561651,
    564897,
    7978942649,
    564156321,
    465631163
]

def generate_test():
    """Gera um arquivo com números aleatórios com dist. uniforme utilizando o numpy, para testes"""
    with open(f'./test.txt', 'w') as file:
        rand = numpy.random
        for i in range(5000000):
            x = rand.uniform()
            file.write(f'{x}\n')

def generate_files():
    """Gera 10 arquivos com 5 MI de números aleatórios com o gerador criado"""
    for file_no in range(1, 11):
        with open(f'./NEWALEO_{file_no}.txt', 'w') as file:
            start_time = time.time()
            gen = GNPCL(SEEDS[file_no-1], EXP, MOD, c)
            for i in range(5000000):
                x = gen.generate()
                file.write(f'{x}\n')
            duration = time.time() - start_time
            print(f'Arquivo {file.name} criado em {duration:.2f} segundos')

def execute_tests():
    """Executa os testes de aleatoriedade nos arquivos gerados"""
    for file_no in range(10):
        # tests.uniformity_test(f'./NEWALEO_{file_no+1}.txt')
        # tests.runs_test(f'./NEWALEO_{file_no+1}.txt')
        tests.interval_test(f'./NEWALEO_{file_no+1}.txt')

if __name__ == '__main__':
    #generate_files()
    execute_tests()