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
    
def func1(x,a,b):
    return a*x/(b+x)
      

def AnalyseData(funEmploye):
    for speciesAdd in ['H2','CH4','CO']:
        file1=pd.read_csv(speciesAdd+"TemperatureShift.csv",',',header=None)
        cAdd=file1.iloc[0,:].values
        TemperatureShift=file1.iloc[1,:].values
       
        popt,pcov=curve_fit(funEmploye,cAdd,TemperatureShift)
        print("a {0:g} b {1:g} ".format(*popt,pcov))
        plt.figure()
        plt.plot(cAdd*1e6,TemperatureShift,'*')
        plt.plot(cAdd*1e6,funEmploye(cAdd,*popt),'r.--')

        plt.xlabel("["+speciesAdd+"] (μL/L)")
        plt.ylabel("Temperature Shift ($^\circ$C)")
        plt.legend(["Data Calculated",'Fiting Curve'])
        plt.show()
        
def TestAdditive(funEmployeNumber):
    for speciesAdd in ['H2','CH4','CO']:
        listTemperature=np.linspace(800,1400,25)
        #listAdd=np.linspace(0,900e-6,4)
        listAdd=np.array([0,300e-6,900e-6])
        if funEmployeNumber==1:
            dictAdd={'H2':(58.0651,32038.1),'CH4':(15.4262,1.54889e8),'CO':(55.4224,6941.1)}
        else:
            dictAdd={'H2':(338.85,0.00067158),'CH4':(219.285,0.000187777),'CO':(253.087,0.0012789)}
        calculator_Additive=evltFun.Additive_Analyse(temperatureListX=listTemperature,speciesAdd=speciesAdd,ListAdd=listAdd)
        calculator_Additive.Detail_Overall_withAdd(dictAdd,funEmploye=funEmployeNumber,draw=True)

        


if __name__=='__main__':
    for i in [1,2]:
        TestAdditive(i)
