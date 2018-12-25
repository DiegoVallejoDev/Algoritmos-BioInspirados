class Sphere:
    MIN_VALUE = -2.048
    MAX_VALUE = 2.048
    name = "Sphere"

    def __init__(self):
        pass

    def fitness(self, cromosoma):
        z = 0
        for alelo in cromosoma:
            z += alelo ** 2
        return z
