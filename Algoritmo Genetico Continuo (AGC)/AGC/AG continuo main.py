from functions import sphere, quartic, rastrigin, rosenbrock
import AGC
import numpy
import matplotlib.pyplot as plt

generations = 4000
sampleEach = 100
runNtimes = 4
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
    print(problem.name, dim)
    ag = AGC.AGC(
        cantidad_individuos=32,
        alelos=dim,
        generaciones=generations,
        p=0.02,
        problema=problem,
        sampleEach=sampleEach,
        printEach=printEach
    )
    ag.run()
    r = []
    for s in ag.samples:
        r.append(-1 * (s._fitness - problem.MAX_VALUE ** dim))

    return r


def main():
    it = 0
    for f in functions:
        plt.ylabel(f.name + " " + str(it))
        plt.xlabel("generacion x" + str(sampleEach))
        for d in dimensions:
            sameFuncNtimes = []
            for r in range(runNtimes):
                sameFuncNtimes.append(run(f, d))
            promedios = promedioFuncion(sameFuncNtimes)
            plt.plot(promedios)
            it += 1
        plt.show()


if __name__ == '__main__':
    main()
