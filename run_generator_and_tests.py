import os
import time
import numpy

import modelagem.tests as tests
from modelagem.gnpcl import GNPCL

def generate_test():
    """Gera um arquivo com números aleatórios com dist. uniforme utilizando o numpy, para testes"""
    with open(f'./txt_files/test.txt', 'w') as file:
        for _ in range(5000000):
            x = numpy.random.uniform()
            file.write(f'{x}\n')

def generate_files():
    """Gera 10 arquivos com 5 MI de números aleatórios com o gerador criado"""
    gen = GNPCL(0)
    for file_no in range(1, 11):
        with open(f'./txt_files/NEWALEO_{file_no}.txt', 'w') as file:
            start_time = time.time()
            # usa o valor do unix timestamp como seed
            gen.new_seed(start_time)
            for _ in range(5000000):
                x = gen.generate()
                file.write(f'{x}\n')
            duration = time.time() - start_time
            print(f'Arquivo {file.name} criado em {duration:.2f} segundos')

def execute_tests():
    """Executa os testes de aleatoriedade nos arquivos gerados"""
    with open('./txt_files/resumo_testes.txt', 'w') as file:
        for file_no in range(10):
            r1 = tests.uniformity_test(f'./txt_files/NEWALEO_{file_no+1}.txt')
            r2 = tests.runs_test(f'./txt_files/NEWALEO_{file_no+1}.txt')
            r3 = tests.interval_test(f'./txt_files/NEWALEO_{file_no+1}.txt')
            r4 = tests.permutation_test(f'./txt_files/NEWALEO_{file_no+1}.txt')
            file.write(f"ARQUIVO NEWALEO_{file_no+1}.txt\n")
            file.write(f"Teste de uniformidade: {'OK' if r1 else 'Nao Passou'}\n")
            file.write(f"Teste das corridas:\n")
            file.write(f"\tCorrida ascendente: {'OK' if r2[0] else 'Nao Passou'}\n")
            file.write(f"\tCorrida descendente: {'OK' if r2[1] else 'Nao Passou'}\n")
            file.write("Teste de intervalos:\n")
            for i in range(len(r3)):
                file.write(f"\tD = {i}: {'OK' if r3[i] else 'Nao Passou'}\n")
            file.write(f"Teste de permutacao: {'OK' if r4 else 'Nao Passou'}\n\n")

if __name__ == '__main__':
    if not os.path.exists("./txt_files"):
        os.makedirs("./txt_files")
    generate_files()
    execute_tests()