from __future__ import division

try:
    from deap import tools
except:
    import os
    os.system("pip install deap")
    from deap import tools

from deap import base, creator
import numpy as np
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
# un individual, ca veut dire, un variable de vecteur
import random

import evaluationFunction as evltFun


POP_SIZE = 50
CXPB, MUTPB,INDPB, NGEN = 0.5, 0.2, 0.2,100

def atribute_initiale(PMin,Pmax):
    a=random.uniform(0,10)
    b=random.uniform(PMin,Pmax)
    return a*10**b

LimitMinAi,LimitMaxAi=0,50
LimitMinBetai,LimitMaxBetai=0,0
LimitMinEi,LimitMaxEi=0,10
toolbox = base.Toolbox()
toolbox.register("attribute_Ai",atribute_initiale,LimitMinAi,LimitMaxAi)
toolbox.register("attribute_Betai",atribute_initiale,LimitMinBetai,LimitMaxBetai)
toolbox.register("attribute_Ei",atribute_initiale,LimitMinEi,LimitMaxEi)
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attribute_Ai,toolbox.attribute_Betai,toolbox.attribute_Ei), n=2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    # individual[0]:learnning rate;individual[1] numbers of perceptron

    if LimitMinAi<individual[0]<=10*10**LimitMaxAi and LimitMinBetai<individual[1]<=10*10**LimitMaxBetai and \
            LimitMinEi<individual[2]<=10*10**LimitMaxEi and LimitMinAi<individual[3]<=10*10**LimitMaxAi and \
            LimitMinBetai<individual[4]<=10*10**LimitMaxBetai and LimitMinEi<individual[5]<=10*10**LimitMaxEi:
        #notes=((individual[0]-5*10**5)/(5*10**5))**2+((individual[1]-5)/5)**2+((individual[2]-5*10**5)/(5*10**5))**2+ \
             #((5*10**5-individual[3])/(5*10**5))**2+((individual[4]-4)/4)**2+((individual[5]-5*10**5)/(5*10**5))**2
        #notes=evltFun.difference_Overall_Detail(individual)
        listTemperature=np.linspace(500,1800,13)
        notes=evltFun.difference_Overall_Detail_temperature(individual,listTemperature,draw=False)

    else:
        notes=float('Inf')

    return notes,
def mutGaussianModified(individual, mu, sigma, indpb):
    #print("This is the original:{0}".format(individual))
    for i in range(len(individual)):
        if random.uniform(0,1)<indpb:
            individual[i]*=(1+random.gauss(mu,sigma))
    #print("This is the number:{0}".format(individual))
    return individual
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutGaussianModified, mu=0, sigma=1, indpb=INDPB)
toolbox.register("select", tools.selTournament, tournsize=int(0.2*POP_SIZE))
toolbox.register("evaluate", evaluate)

def main():
    pop = toolbox.population(n=POP_SIZE)


    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))

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
        fitnesses = list(map(toolbox.evaluate, invalid_ind))

        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring
        print(pop)
        fitnessesPOP=[]
        for inds in pop:
            fitnessesPOP.append(inds.fitness.values)
        print(fitnessesPOP)

        input_stream=("""step{0} pop: {1} \n step{0} fitnessesPOP {2} \n """.format(g,pop,fitnessesPOP) )
        with open("logFile.txt",'a+') as stream:
            stream.write(input_stream)


    return pop

if __name__=="__main__":
    xx=main()
    print(xx)
