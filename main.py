import time

from gnpcl import Generator

EXP = 13
MOD = float(2**EXP - 1)
#a = MOD**(0.5)
a = float(2**(EXP/2))
c = 773

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

for file_no in range(1, 11):
    with open(f'./NEWALEO_{file_no}.txt', 'w') as file:
        start_time = time.time()
        gen = Generator(SEEDS[file_no-1], EXP, MOD, c)
        for i in range(5000000):
            x = gen.generate()
            file.write(f'{x}\n')
        duration = time.time() - start_time
        print(f'Arquivo {file.name} criado em {duration:.2f} segundos')
