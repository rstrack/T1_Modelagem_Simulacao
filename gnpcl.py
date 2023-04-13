class Generator():
    def __init__(self, seed: float, exp:float, m: float,c: float = 0) -> None:
        self.prev = seed
        self.exp = exp
        self.m = m
        self.a = float(2**(exp/2))
        self.c = c

    def new_seed(self, seed: float) -> None:
        self.prev = seed

    def generate(self) -> float:
        self.prev = float((self.a * self.prev + self.c) % self.m)
        return self.prev/self.m