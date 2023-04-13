class GNPCL():
    """
    Gerador de números pseudo-aletórios congruencial linear.
 

    Atributos:
    ----------
    seed : float
        número inicial do gerador
    exp : float
        expoente para geração do módulo
    mod : float
        módulo utilizado para congruência. Preferencialmente o maior inteiro possível
    c : float   
        constante de incremento (padrão: 0)

    Métodos:
    ----------
    new_seed(seed: float)
        define nova seed para o gerador, iniciando um novo ciclo de geração
    generate()
        gera o próximo número do gerador
    """
    def __init__(self, seed: float, exp:float, c: float = 0) -> None:
        self.prev = seed
        self.exp = exp
        self.mod = float(2**exp - 1)
        # valor alternativo:
        # self.a = self.mod**(0.5)
        self.a = float(2**(exp/2))
        self.c = c

    def new_seed(self, seed: float) -> None:
        self.prev = seed

    def generate(self) -> float:
        self.prev = float((self.a * self.prev + self.c) % self.mod)
        return self.prev/self.mod