from PSO import Pso
from functions import sphere, quartic, rastrigin, rosenbrock
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

generations = 4000
runNtimes = 4
sampleEach = 100
x = numpy.linspace(0, generations)  # range: (initial, last, iteration=?)
functions = [sphere.Sphere(), rastrigin.Rastrigin(), quartic.Quartic(), rosenbrock.Rosenbrock()]
dimensions = [2, 4, 8, 16]
swarm = Pso()


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
    best, samples = swarm.run(
        problem,
        dimensions=dim,
        Generations=generations,
        PopSize=50,
        c1=1.5,
        c2=2,
        w=1,
        wdamp=0.995,
        sampleEach=sampleEach,
        printEach=printEach
    )

    return samples


def main():
    it = 0
    for f in functions:
        plt.ylabel(f.name)
        plt.xlabel("generacion x" + str(sampleEach))
        for d in dimensions:
            sameFuncNtimes = []
            for r in range(runNtimes):
                print(str(r + 1) + "a iteracion ", end="")
                sameFuncNtimes.append(run(f, d))
            promedios = promedioFuncion(sameFuncNtimes)
            plt.legend(handles=[
                mpatches.Patch(label='2 dimensiones'),
                mpatches.Patch(color='orange', label='4 dimensiones'),
                mpatches.Patch(color='green', label='8 dimensiones'),
                mpatches.Patch(color='red', label='16 dimensiones')
            ])
            plt.plot(promedios, label='Inline label')
            it += 1
        plt.show()


if __name__ == '__main__':
    main()
