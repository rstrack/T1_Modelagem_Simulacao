import numpy as np

CLASS_COUNT = 10
NUM_COUNT = 5000000

def uniformity_test(file_path: str):

    #array que armazena a frequencia de cada classe
    values = np.zeros(CLASS_COUNT, dtype=float)

    with open(file_path, 'r') as f:
        cont = 0
        for line in f.readlines():
            if cont == NUM_COUNT: break
            cont = cont+1
            value = float(line)
            values[int(value*CLASS_COUNT)] = values[int(value*CLASS_COUNT)] + 1

    #frequencia acumulada esperada
    expected_cdf = np.array([1/CLASS_COUNT*i for i in range(1, CLASS_COUNT+1)]) 

    #frequencia acumulada observada
    observed_cdf = np.zeros(CLASS_COUNT, dtype=float) 
    for i in range(CLASS_COUNT):
        observed_cdf[i] = sum(values[0:i+1])/NUM_COUNT

    ks_calc = np.max(np.abs(observed_cdf - expected_cdf))

    ks_5 = 1.36/(np.sqrt(NUM_COUNT))
    print('\n\n')
    print(observed_cdf)
    print(expected_cdf)

    print(f'KS Calculado: {ks_calc}\nKS 5%: {ks_5}')
    if(ks_calc < ks_5):
        print('Aceita H0')
        return True
    else: 
        print('Rejeita H0')
        return False
