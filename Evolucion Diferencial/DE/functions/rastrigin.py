import numpy as np


class Rastrigin:
    MIN_VALUE = -2.048
    MAX_VALUE = 2.048
    name = "Rastrigin"

    def __init__(self):
        pass

    def fitness(self, cromosoma):
        z = 0
        X = 0
        Y = 0
        for i in range(len(cromosoma)):
            if i < (len(cromosoma) - 1):
                X = cromosoma[i]
                Y = cromosoma[i + 1]
                z += (10 * 2 + (X ** 2 + Y ** 2 - (10 * np.cos(2 * np.pi * (X + Y)))))
        return z
