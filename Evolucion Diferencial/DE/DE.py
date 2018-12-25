import numpy as np


def de(problem, dimensions, mut=0.8, crossp=0.7, popsize=20, generations=1000, sampleEach=100, printEach=1):
    samples = []
    pop = np.random.rand(popsize, dimensions)
    limiteInferior, limiteSuperior = problem.MIN_VALUE, problem.MAX_VALUE
    diff = np.fabs(limiteInferior - limiteSuperior)
    pop_denorm = limiteInferior + pop * diff
    fitness = np.asarray([problem.fitness(ind) for ind in pop_denorm])
    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]
    for i in range(generations):
        for j in range(popsize):
            individuos = [ind for ind in range(popsize) if ind != j]
            a, b, c = pop[np.random.choice(individuos, 3, replace=False)]
            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            J = limiteInferior + trial * diff
            f = problem.fitness(J)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = J
        if printEach !=0 and i % printEach == 0:
            print("Generacion ", i, best, fitness[best_idx])
        if sampleEach != 0 and i % sampleEach == 0:
            samples.append(fitness[best_idx])
    return samples
