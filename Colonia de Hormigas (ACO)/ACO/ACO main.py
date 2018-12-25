from functions import sphere, quartic, rastrigin, rosenbrock
import ACO
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

generations = 400
sampleEach = 10
runNtimes = 1
x = numpy.linspace(0, generations, sampleEach)  # range: (initial, last, iteration)
functions = [sphere.Sphere(), rastrigin.Rastrigin(), quartic.Quartic(), rosenbrock.Rosenbrock()]
dimensions = [2, 4, 8, 16]


def promedioFuncion(samples):
    prom = []
    for iteracion in range(len(samples[0])):
        x = 0
        for gen in samples:
            x += gen[iteracion]
        prom.append(x / len(samples))
    return prom


def run(problem, dim, printEach=int(generations / 4)):
    print(problem.name, dim, "d")
    aco = ACO.ACO(
     cantidad_individuos=10,      # N
     cantidad_dimensiones=dim,    # n
     cantidad_intervalos=8,       # B
     importancia_feromona=1,      # alpha
     constante_deposito=20,       # Q
     tasa_eveporacion=.9,         # p
     feromona_inicial=0.00001,    # to
     problema=problem,
     generaciones=generations,
     sampleEach=sampleEach,
     printEach=printEach
     )
    aco.run()
    r = []
    for s in aco.samples:
        r.append(s._fitness)

    return r


def main():
    it = 0
    for f in functions:
        plt.ylabel(f.name)
        plt.xlabel("generacion x" + str(sampleEach))
        for d in dimensions:
            sameFuncNtimes = []
            for r in range(runNtimes):
                print(str(r+1)+"a iteracion ", end="")
                sameFuncNtimes.append(run(f, d))
            promedios = promedioFuncion(sameFuncNtimes)
            plt.legend(handles=[
                mpatches.Patch(label='2 dimensiones'),
                mpatches.Patch(color='orange', label='4 dimensiones'),
                mpatches.Patch(color='green',  label='8 dimensiones'),
                mpatches.Patch(color='red',    label='16 dimensiones')
            ])
            plt.plot(promedios, label='Inline label')
            it += 1
        plt.show()


if __name__ == '__main__':
    main()
