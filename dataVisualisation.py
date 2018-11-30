import numpy as np
import pandas as  pd
import matplotlib.pyplot as plt
import os
import time

df=pd.read_csv("Convergence.csv",header=0)
listTemperature=[1100,1400,1600]
symbol=[":","-.","--"]
lgd=[]
for num,temperature in enumerate(listTemperature):
    dfToAnalyse=df[abs(df["temperature"]-temperature)<1e-3]
    iterSteps,errorData=dfToAnalyse["iterSteps"],dfToAnalyse["Error"]
    plt.plot(iterSteps,errorData,symbol[num])
    lgd.append(str(temperature)+"K")

currentTime=time.strftime("%Y%m%d_%H%M%S")
plt.legend(lgd)
plt.xlabel('step',fontsize='large')
plt.ylabel('Relative Error',fontsize='large')
plt.title('Convergence of Genetic Algorithm',fontsize='large')
plt.savefig(os.path.join(os.path.dirname(__file__),'ImageResult',currentTime+"_Convergence.png"))
plt.show()

