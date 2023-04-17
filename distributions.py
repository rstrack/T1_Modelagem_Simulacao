import time
import numpy as np
from gnpcl import GNPCL

class ExponentialDist:
    def __init__(self, param_lambda) -> None:
        self.gnpcl = GNPCL(time.time())
        self.param_lambda = param_lambda

    def generate(self):
        return (- 1/self.param_lambda) * np.log(self.gnpcl.generate())


class GamaDist:
    def __init__(self, alpha, beta) -> None:
        self.gnpcl = GNPCL(time.time())
        self.alpha = alpha
        self.beta = beta

    def generate(self):
        return (-1/self.alpha) * np.log(1 - self.gnpcl.generate()) / self.beta


class NormalDist:
    def __init__(self, mean, std_dev) -> None:
        self.gnpcl = GNPCL(time.time())
        self.mean = mean
        self.std_dev = std_dev
        self.z1 = None
        self.z2 = None

    def generate(self):
        if self.z2 == None:
            r1 = self.gnpcl.generate()
            r2 = self.gnpcl.generate()
            ret = np.sqrt(-2 * np.log(r1)) * np.cos(2 * np.pi * r2)
            self.z2 = np.sqrt(-2 * np.log(r1)) * np.sin(2 * np.pi * r2)
            return self.std_dev*ret + self.mean
        if self.z1 == None:
            ret = self.z2
            self.z2 = None
            return self.std_dev*ret + self.mean
        return 'error'


if __name__ == '__main__':
    exp_dist = ExponentialDist(0.1)
    norm_dist = NormalDist(13.96, 4.27)
    gama_dist = GamaDist(27.6587, 1.3)

    with open('./exp_teste.txt', 'w') as file:
        for _ in range(1000):
            file.write(f'{exp_dist.generate()}\n')
    with open('./norm_teste.txt', 'w') as file:
        for _ in range(1000):
            file.write(f'{norm_dist.generate()}\n')
    with open('./gama_teste.txt', 'w') as file:
        for _ in range(1000):
            file.write(f'{gama_dist.generate()}\n')