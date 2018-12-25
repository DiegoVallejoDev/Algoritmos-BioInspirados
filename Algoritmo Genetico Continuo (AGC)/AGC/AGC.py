import copy
import numpy as np


class Individuo:
    def __init__(self, alelos, cromosoma):
        self._alelos = alelos
        self._cromosoma = cromosoma
        self._fitness = 0


class AGC:
    def __init__(self, cantidad_individuos, alelos, generaciones, p, problema, sampleEach=0, printEach=0):
        self._cantidad_individuos = cantidad_individuos
        self._alelos = alelos
        self._sampleEach = sampleEach
        self.samples = []
        self._generaciones = generaciones
        self._p = p
        self._problema = problema
        self._printEach = printEach
        self._individuos = np.array([])

    def run(self):
        self.crearIndividuos()
        self._mejor_historico = self._individuos[0]
        self.samples.append(self._mejor_historico)
        generacion = 0
        while generacion <= self._generaciones:
            self.evaluaIndividuos()
            self.mejor()
            if (self._sampleEach != 0 and generacion % self._sampleEach == 0):
                self.samples.append(self._mejor_historico)
            hijos = np.array([])
            while len(hijos) < len(self._individuos):
                padre1 = self.ruleta()
                padre2 = self.ruleta()
                while padre1 == padre2:
                    padre2 = self.ruleta()
                h1, h2 = self.cruza(self._individuos[padre1], self._individuos[padre2])
                hijos = np.append(hijos, [h1])
                hijos = np.append(hijos, [h2])
            self.mutacion(hijos)
            self._individuos = np.copy(hijos)
            if (self._printEach != 0 and generacion % self._printEach == 0):
                print("Generación: ", generacion, 'Mejor Histórico: ', self._mejor_historico._cromosoma,
                      -1 * (self._mejor_historico._fitness - self._problema.MAX_VALUE ** 14))
            generacion += 1

    def crearIndividuos(self):
        for i in range(self._cantidad_individuos):
            cromosoma = self._problema.MIN_VALUE + np.random.random(size=self._alelos) * (
                    self._problema.MAX_VALUE - self._problema.MIN_VALUE)
            individuo = Individuo(self._alelos, cromosoma)
            self._individuos = np.append(self._individuos, [individuo])

    def evaluaIndividuos(self):
        for i in self._individuos:
            i._fitness = self._problema.fitness(i._cromosoma)
            i._fitness *= -1
            i._fitness += self._problema.MAX_VALUE ** 14

    def ruleta(self):
        f_sum = np.sum([i._fitness for i in self._individuos])
        r = np.random.randint(f_sum + 1)
        k = 0
        F = self._individuos[k]._fitness
        while F < r and k+1 < len(self._individuos):
            k += 1
            F += abs(self._individuos[k]._fitness)
        return k

    def cruza(self, i1, i2):
        h1 = copy.deepcopy(i1)
        h2 = copy.deepcopy(i2)

        s = self._alelos - 1
        punto_cruza = np.random.randint(s) + 1
        for i in range(punto_cruza, self._alelos):
            h1._cromosoma[i], h2._cromosoma[i] = h2._cromosoma[i], h1._cromosoma[i]
        return h1, h2

    def mutacion(self, hijos):
        for h in hijos:
            for a in range(len(h._cromosoma)):
                if np.random.rand() < self._p:
                    h._cromosoma[a] = self._problema.MIN_VALUE + np.random.random() * (
                            self._problema.MAX_VALUE - self._problema.MIN_VALUE)

    def mejor(self):
        for i in self._individuos:
            if i._fitness > self._mejor_historico._fitness:
                self._mejor_historico = copy.deepcopy(i)
