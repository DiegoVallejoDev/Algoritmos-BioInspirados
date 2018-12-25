class Quartic:
    MIN_VALUE = -2.048
    MAX_VALUE = 2.048
    name = "Quartic"

    def __init__(self):
        pass

    def fitness(self, cromosoma):
        z = 0
        n = 1
        for gen in cromosoma:
            z += (n * gen ** 4)
            n += 1
        return z
