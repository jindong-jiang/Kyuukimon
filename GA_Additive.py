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
import csv
import evaluationFunction as evltFun

enhenced_eff_Limit=100
CXPB, MUTPB,INDPB,PRCENTSEL, POP_SIZE,NGEN = 0.5, 0.8, 0.4,0.3,60,200
def attribute_Indv():
    return 10**(enhenced_eff_Limit*random.random())

toolbox = base.Toolbox()

toolbox.register("individual", tools.initRepeat,creator.Individual,attribute_Indv,n=2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
speciesAdd='CO'
listTemperature=np.linspace(1100,1500,5)
listAdd=np.linspace(0,900e-6,4)

calculator_Additive=evltFun.Additive_Optimazition(temperatureListX=listTemperature,speciesAdd=speciesAdd,ListAdd=listAdd)

def evaluate(individual):
    # individual[0]:learnning rate;individual[1] numbers of perceptron

    if 0<individual[0] and 0<individual[1]:
        try:           
            notes=calculator_Additive.difference_Overall_Detail_temperature(individual,draw=False)
        except:
            notes=float('Inf')
            print("This solution is not valide")

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
toolbox.register("select", tools.selTournament, tournsize=int(PRCENTSEL*POP_SIZE))
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
        
        bestIndiv=toolbox.clone(tools.selTournament(offspring,1,len(offspring)))
        print("Step:{0} | BestIndiv:{1} | Relative Error:{2} \n".format([g],bestIndiv[0],list(bestIndiv[0].fitness.values)))
        with open(speciesAdd+"bestresultforM.csv","a+") as csvFile:
            csvWriter=csv.writer(csvFile)
            csvWriter.writerow([g]+bestIndiv[0]+list(bestIndiv[0].fitness.values))
        
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
