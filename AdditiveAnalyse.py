import evaluationFunction as evltFun
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def GatherData():
    speciesAdd='H2'
    listTemperature=np.linspace(800,1400,25)
    listAdd=np.linspace(0,9000e-6,31)
    calculator_Additive=evltFun.Additive_Analyse(temperatureListX=listTemperature,speciesAdd=speciesAdd,ListAdd=listAdd)
    calculator_Additive.analyse_leftshift_Reaction()
    
def func(x,a,b):
    return a*np.log(b*x+1)
    '''
def func(x,a,b):
    return a*x/(b+x)
    '''  

def AnalyseData():
    for speciesAdd in ['H2','CH4','CO']:
        file1=pd.read_csv(speciesAdd+"TemperatureShift.csv",',',header=None)
        cAdd=file1.iloc[0,:].values
        TemperatureShift=file1.iloc[1,:].values
       
        popt,pcov=curve_fit(func,cAdd,TemperatureShift)
        print("a {0:g} b {1:g} ".format(*popt,pcov))
        plt.figure()
        plt.plot(cAdd*1e6,TemperatureShift,'*')
        plt.plot(cAdd*1e6,func(cAdd,*popt),'r.--')

        plt.xlabel("["+speciesAdd+"] (μL/L)")
        plt.ylabel("Temperature Shift ($^\circ$C)")
        plt.legend(["Data Calculated",'Fiting Curve'])
        plt.show()
        


        


if __name__=='__main__':
    AnalyseData()
