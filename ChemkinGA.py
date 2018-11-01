from __future__ import division
from deap import base, creator
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
# un individual, ca veut dire, un variable de vecteur
import random
from deap import tools
import evaluationFunction as evltFun


IND_SIZE = 6

def atribute_initiale():
    return random.random()

toolbox = base.Toolbox()
toolbox.register("attribute",atribute_initiale)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attribute, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    #individual[0]:learnning rate;individual[1] numbers of perceptron
    #if 0<individual[0]<=1 and 0<individual[1]<=1:
    #notes=(individual[0]-0.5)**2+(individual[1]-0.8)**2
    notes=evltFun.difference_Overall_Detail(individual)

    #else:
    #    notes=100000

    return notes,

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

def main():
    pop = toolbox.population(n=5)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 50

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)

    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        #print(offspring)
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            #print(child1,child2)
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring
        print(pop)
        print(fitnesses)


    return pop

if __name__=="__main__":
    xx=main()
    print(xx)
