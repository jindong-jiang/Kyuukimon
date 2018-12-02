import evaluationFunction as evltFun
import numpy as np
speciesAdd='CH4'
listTemperature=np.linspace(800,1400,25)
listAdd=np.linspace(0,9000e-6,31)
calculator_Additive=evltFun.Additive_Analyse(temperatureListX=listTemperature,speciesAdd=speciesAdd,ListAdd=listAdd)
calculator_Additive.analyse_leftshift_Reaction()