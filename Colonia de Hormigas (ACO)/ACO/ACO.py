import copy
import numpy as np


class Individuo:
    def __init__(self, c_dimensiones, c_intervalos, solucion):
        self._c_dimensiones = c_dimensiones
        self._c_intervalos = c_intervalos
        self._solucion = solucion
        self._fitness = 10 ** 10
        self._probabilidades = np.ones(self._c_dimensiones * self._c_intervalos) * 1 / self._c_intervalos
        self._feromona_local = np.zeros(self._c_dimensiones * self._c_intervalos)


class ACO:
    def __init__(self,
                 cantidad_individuos,   # N
                 cantidad_dimensiones,  # n
                 cantidad_intervalos,   # B
                 importancia_feromona,  # alpha
                 constante_deposito,    # Q
                 tasa_eveporacion,      # p
                 feromona_inicial,      # to
                 problema,
                 generaciones,
                 sampleEach=100,
                 printEach=100
                 ):
        self._cantidad_individuos = cantidad_individuos
        self._cantidad_dimensiones = cantidad_dimensiones
        self._cantidad_intervalos = cantidad_intervalos
        self._importancia_feromona = importancia_feromona
        self._constante_deposito = constante_deposito
        self._tasa_eveporacion = tasa_eveporacion
        self._feromona_inicial = feromona_inicial
        self._problema = problema
        self._generaciones = generaciones
        self._rango = self._problema.MAX_VALUE - self._problema.MIN_VALUE
        self._feromona = np.ones(self._cantidad_dimensiones * self._cantidad_intervalos) * self._feromona_inicial
        self._individuos = []
        self._tamano_intervalo = self._rango / self._cantidad_intervalos
        self._L = np.ones(self._cantidad_individuos) * (10 ** 10)
        self._mejor_historico = 0
        self._sampleEach = sampleEach
        self.samples = []
        self._printEach = printEach

    def run(self):
        self.crearIndividuos()
        self._mejor_historico = copy.deepcopy(self._individuos[0])
        generacion = 0
        while generacion <= self._generaciones:
            hormiga_idx = 0
            for hormiga in self._individuos:
                for dimension in range(self._cantidad_dimensiones):
                    for intervalo in range(self._cantidad_intervalos):
                        indice = dimension * self._cantidad_intervalos + intervalo
                        suma_feromona = np.sum(self._feromona[dimension * self._cantidad_intervalos: (
                                                                                                             dimension + 1) * self._cantidad_intervalos] ** self._importancia_feromona)
                        hormiga._probabilidades[indice] = self._feromona[
                                                              indice] ** self._importancia_feromona / suma_feromona
                    intervalo_seleccionado = self.ruleta(hormiga._probabilidades[
                                                         dimension * self._cantidad_intervalos: (
                                                                                                        dimension + 1) * self._cantidad_intervalos])
                    hormiga._solucion[dimension] = np.random.random() * (self._tamano_intervalo) + (
                            self._tamano_intervalo * intervalo_seleccionado) + self._problema.MIN_VALUE
                hormiga._fitness = self._problema.fitness(hormiga._solucion)
                self._L[hormiga_idx] = copy.deepcopy(hormiga._fitness)
                if self._L[hormiga_idx] < self._mejor_historico._fitness:
                    self._mejor_historico = copy.deepcopy(hormiga)
                hormiga_idx += 1
            for dimension in range(self._cantidad_dimensiones):
                for intervalo in range(self._cantidad_intervalos):
                    hormiga_idx = 0
                    indice = dimension * self._cantidad_intervalos + intervalo
                    suma_feromona_local = 0
                    for hormiga in self._individuos:
                        if (
                                self._tamano_intervalo * intervalo + self._problema.MIN_VALUE <= hormiga._solucion[
                            dimension] < self._tamano_intervalo * (intervalo + 1) + self._problema.MIN_VALUE):
                            hormiga._feromona_local[indice] = hormiga._feromona_local[
                                                                  indice] + self._constante_deposito / self._L[
                                                                  hormiga_idx]
                        # else:
                        #    hormiga._feromona_local[indice] = 0
                        suma_feromona_local += hormiga._feromona_local[indice]
                        hormiga_idx += 1
                    self._feromona[indice] = (1 - self._tasa_eveporacion) * self._feromona[indice] + suma_feromona_local
            if (self._printEach != 0 and generacion % self._printEach == 0):
                print('Generación: ', generacion,
                      'Mejor: ', self._mejor_historico._solucion,
                      'f: ', self._mejor_historico._fitness)
            if (self._sampleEach != 0 and generacion % self._sampleEach == 0):
                self.samples.append(self._mejor_historico)
            generacion += 1

    def crearIndividuos(self):
        for i in range(self._cantidad_individuos):
            solucion = np.random.random(size=self._cantidad_dimensiones) * self._rango + self._problema.MIN_VALUE
            individuo = Individuo(self._cantidad_dimensiones, self._cantidad_intervalos, solucion)
            self._individuos.append(individuo)

    def mostrarIndividuos(self):
        for i in self._individuos:
            print(i.solucion)

    def ruleta(self, valores):
        suma = np.sum(valores)
        r = np.random.random()
        k = 0
        F = valores[k] / suma
        while F < r:
            k += 1
            F += valores[k] / suma
        return k  # regresa el intervalo en el cual se debe generar un número
