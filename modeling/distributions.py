import time
import numpy as np
from modeling.gnpcl import GNPCL

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
        # Usa a teoria do seguinte artigo para geração do valor:
        # "The Generation of Gamma Variables with Non-Integral Shape Parameter"
        # de R. C. H. Cheng
        # link: https://www.jstor.org/stable/2346871?seq=1#page_scan_tab_contents
        if self.alpha > 1.0:
            ainv = np.sqrt(2.0 * self.alpha - 1.0)
            bbb = self.alpha - np.log(4)
            ccc = self.alpha + ainv
            while True:
                u1 = self.gnpcl.generate()
                if not 1e-7 < u1 < 0.9999999:
                    continue
                u2 = 1.0 - self.gnpcl.generate()
                v = np.log(u1 / (1.0 - u1)) / ainv
                x = self.alpha * np.exp(v)
                z = u1 * u1 * u2
                r = bbb + ccc * v - x
                if r + 1.0 + np.log(4.5) - 4.5 * z >= 0.0 or r >= np.log(z):
                    return x * self.beta
        elif self.alpha == 1.0:
            return -np.log(1.0 - self.gnpcl.generate()) * self.beta
        else:
            while True:
                u = self.gnpcl.generate()
                b = (np.e + self.alpha) / np.e
                p = b * u
                if p <= 1.0:
                    x = p ** (1.0 / self.alpha)
                else:
                    x = -np.log((b - p) / self.alpha)
                u1 = self.gnpcl.generate()
                if p > 1.0:
                    if u1 <= x ** (self.alpha - 1.0):
                        break
                elif u1 <= np.exp(-x):
                    break
            return x * self.beta


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

if __name__ == '__main__':
    exp_dist = ExponentialDist(0.0422)
    gama_dist = GamaDist(27.6587, 1.3054)
    norm_dist = NormalDist(13.96, 4.27)

    with open('./txt_files/exp_teste.txt', 'w') as file:
        for _ in range(1000):
                file.write(f'{exp_dist.generate()}\n')
    with open('./txt_files/norm_teste.txt', 'w') as file:
        for _ in range(1000):
            file.write(f'{norm_dist.generate()}\n')
    with open('./txt_files/gama_teste.txt', 'w') as file:
        for _ in range(1000):
            file.write(f'{gama_dist.generate()}\n')
