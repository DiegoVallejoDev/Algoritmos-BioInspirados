import numpy as np


# Particle Swarm Optimization

class Pso:
    def __init__(self):
        pass

    def run(self, problem, dimensions=5, Generations=100, PopSize=100, c1=1.4962, c2=1.4962, w=0.7298, wdamp=1.0,sampleEach=100, printEach=1):
        # Empty Particle Template
        empty_particle = {
            'position': None,
            'velocity': None,
            'fitness': None,
            'best_position': None,
            'best_fitness': None,
        }

        # Extract Problem Info
        fitnessFunction = problem.fitness
        VarMin = problem.MIN_VALUE
        VarMax = problem.MAX_VALUE
        nVar = dimensions
        samples = []

        # Initialize Global Best with none and infinite
        gbest = {'position': None, 'fitness': np.inf}

        # Create Initial Population (Random)
        pop = []
        for i in range(0, PopSize):
            pop.append(empty_particle.copy())
            pop[i]['position'] = np.random.uniform(VarMin, VarMax, nVar)
            pop[i]['velocity'] = np.zeros(nVar)
            pop[i]['fitness'] = fitnessFunction(pop[i]['position'])
            pop[i]['best_position'] = pop[i]['position'].copy()
            pop[i]['best_fitness'] = pop[i]['fitness']

            if pop[i]['best_fitness'] < gbest['fitness']:
                gbest['position'] = pop[i]['best_position'].copy()
                gbest['fitness'] = pop[i]['best_fitness']

        # PSO Loop
        for it in range(0, Generations):
            for i in range(0, PopSize):

                pop[i]['velocity'] = w * pop[i]['velocity'] \
                                     + c1 * np.random.rand(nVar) * (pop[i]['best_position'] - pop[i]['position']) \
                                     + c2 * np.random.rand(nVar) * (gbest['position'] - pop[i]['position'])

                pop[i]['position'] += pop[i]['velocity']
                pop[i]['position'] = np.maximum(pop[i]['position'], VarMin)
                pop[i]['position'] = np.minimum(pop[i]['position'], VarMax)

                pop[i]['fitness'] = fitnessFunction(pop[i]['position'])

                if pop[i]['fitness'] < pop[i]['best_fitness']:
                    pop[i]['best_position'] = pop[i]['position'].copy()
                    pop[i]['best_fitness'] = pop[i]['fitness']

                    if pop[i]['best_fitness'] < gbest['fitness']:
                        gbest['position'] = pop[i]['best_position'].copy()
                        gbest['fitness'] = pop[i]['best_fitness']

            w *= wdamp
            if printEach != 0 and it % printEach == 0:
                print('Iteration {}: Best f = {}'.format(it, gbest['fitness']))
            if sampleEach != 0 and it % sampleEach == 0:
                samples.append(gbest['fitness'])

        return gbest, samples
