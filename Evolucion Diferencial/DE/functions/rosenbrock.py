class Rosenbrock:
    MIN_VALUE = -2.048
    MAX_VALUE = 2.048
    name = "Rosenbrock"

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
                z += (100 * (Y - (X ** 2)) ** 2 + (X - 1) ** 2)
        return z
