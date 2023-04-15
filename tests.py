import numpy as np
import math

CLASS_COUNT = 10
NUM_COUNT = 5000000

def uniformity_test(file_path: str):
    #array que armazena a frequencia de cada classe
    values = np.zeros(CLASS_COUNT, dtype=float)

    with open(file_path, 'r') as f:
        cont = 0
        for line in f.readlines():
            if cont == NUM_COUNT: break
            cont += 1
            value = float(line)
            values[int(value*CLASS_COUNT)] += 1

    #frequencia acumulada esperada
    expected_cdf = np.array([1/CLASS_COUNT*i for i in range(1, CLASS_COUNT+1)]) 

    #frequencia acumulada observada
    observed_cdf = np.zeros(CLASS_COUNT, dtype=float) 
    for i in range(CLASS_COUNT):
        observed_cdf[i] = sum(values[0:i+1])/NUM_COUNT

    ks_calc = np.max(np.abs(observed_cdf - expected_cdf))
    ks_5 = 1.36/(np.sqrt(NUM_COUNT))
    print('\n')
    print(f'TESTE DE UNIFORMIDADE: KS Calculado: {ks_calc}\nKS 5%: {ks_5}')
    if(ks_calc < ks_5):
        print('Aceita H0')
        return True
    else: 
        print('Rejeita H0')
        return False


def runs_test(file_path: str):
    asc_run_value = 1
    desc_run_value = 1
    asc_runs = list()
    desc_runs = list()
    prev_asc_val = None
    prev_desc_val = None

    with open(file_path, 'r') as f:
        for line in f.readlines():
            if prev_asc_val is not None:
                #teste ascendente
                if float(line) > prev_asc_val or asc_run_value == 0:
                    asc_run_value += 1
                else:
                    asc_runs.append(asc_run_value)
                    asc_run_value = 0
                #teste descendente
                if float(line) < prev_desc_val or desc_run_value == 0:
                    desc_run_value += 1
                else:
                    desc_runs.append(desc_run_value)
                    desc_run_value = 0
            prev_asc_val = float(line)
            prev_desc_val = float(line)

    asc_class_count = np.max(asc_runs)
    desc_class_count = np.max(desc_runs)
    asc_expected = [i/math.factorial(i+1)for i in range(asc_class_count)]
    asc_expected_cdf = np.array([(asc_expected[i] if i == 0 else sum(asc_expected[:i+1])) for i in range(asc_class_count)])
    asc_observed_cdf = np.zeros(asc_class_count)
    for i in range(asc_class_count):
        asc_observed_cdf[i] = asc_runs.count(i)/len(asc_runs) if i == 0 else asc_runs.count(i)/len(asc_runs) + asc_observed_cdf[i-1]
            
    desc_expected = [i/math.factorial(i+1)for i in range(desc_class_count)]
    desc_expected_cdf = np.array([(desc_expected[i] if i == 0 else sum(desc_expected[:i+1])) for i in range(desc_class_count)])
    desc_observed_cdf = np.zeros(desc_class_count)
    for i in range(desc_class_count):
        desc_observed_cdf[i] = desc_runs.count(i)/len(desc_runs) if i == 0 else desc_runs.count(i)/len(desc_runs) + desc_observed_cdf[i-1]        
            
    asc_ks_calc = np.max(np.abs(asc_observed_cdf - asc_expected_cdf))
    asc_ks_5 = 1.36/(np.sqrt(len(asc_runs)))
    desc_ks_calc = np.max(np.abs(desc_observed_cdf - desc_expected_cdf))
    desc_ks_5 = 1.36/(np.sqrt(len(desc_runs)))
    print(f'CORRIDA ASCENDENTE: KS Calculado: {asc_ks_calc}\nKS 5%: {asc_ks_5}')
    print(f'CORRIDA DESCENDENTE: KS Calculado: {desc_ks_calc}\nKS 5%: {desc_ks_5}')

    if(asc_ks_calc < asc_ks_5 and desc_ks_calc < desc_ks_5):
        print('Aceita H0')
        return True
    else: 
        print('Rejeita H0')
        if asc_ks_calc > asc_ks_5: print('Falha na corrida ascendente')
        if desc_ks_calc > desc_ks_5: print('Falha na corrida descendente')
        return False
    

def interval_test(file_path: str):
    """
    Realiza os testes para n = [0,9] um de cada vez
    """
    with open(file_path, 'r') as f:
        values = [float(line) for line in f.readlines()]
    results = [False]*10
    for d in range(10):
        interval_len = 1
        intervals = []
        for value in values:
            trunc_value = int(value*10)
            if d != trunc_value:
                interval_len += 1
            else:
                intervals.append(interval_len)
                interval_len = 0
        class_count = np.max(intervals)+1
        expected = np.array([(0.9**k)*0.1 for k in range(class_count)])
        expected_cdf = np.array([(expected[k] if k == 0 else sum(expected[:k+1])) for k in range(class_count)])
        observed_cdf = np.zeros(class_count)
        for i in range(class_count):
            observed_cdf[i] = intervals.count(i)/len(intervals) if i == 0 else intervals.count(i)/len(intervals) + observed_cdf[i-1]
        
        ks_calc = np.max(np.abs(observed_cdf - expected_cdf))
        ks_5 = 1.36/np.sqrt(len(intervals))
        print(f'TESTE DE INTERVALO n = {d}: KS Calculado: {ks_calc} | KS 5%: {ks_5}')
        if(ks_calc < ks_5):
            print('Aceita H0')
            results[d] = True
        else: 
            print('Rejeita H0')
    return results


def permutation_test(file_path: str):
    fo_count = [0] * 6
    with open(file_path, 'r') as f:
        values = [float(line) for line in f.readlines()]

    values = values[:-(len(values)%3)]
    
    for i in range(len(values)):
        if ((i+1) % 3) == 0:
            fo_count[order_func(values[i-2], values[i-1], values[i])] += 1
    group_count = sum(fo_count)
    expected_cdf = np.array([(1/6)*i for i in range(1,7)])
    observed_cdf = np.array([sum(fo_count[:i+1])/group_count for i in range(6)])
    ks_calc = np.max(np.abs(observed_cdf - expected_cdf))
    ks_5 = 1.36/np.sqrt(group_count)
    print(f'TESTE DE PERMUTAÇÃO: KS Calculado: {ks_calc} | KS 5%: {ks_5}')
    if(ks_calc < ks_5):
        print('Aceita H0')
        return True
    else: 
        print('Rejeita H0')
        return False


def order_func(v1:float, v2:float, v3:float):
    if v1 < v2 and v2 < v3:
        return 0
    elif v1 < v3 and v3 < v2:
        return 1
    elif v2 < v1 and v1 < v3:
        return 2
    elif v2 < v3 and v3 < v1:
        return 3
    elif v3 < v1 and v1 < v2:
        return 4
    elif v3 < v2 and v2 < v1:
        return 5
    else: return 'error'