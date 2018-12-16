from evaluationFunction import getMolesFractions
import Python_Chemkin_ToolBox as PyChemTB
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

currentDir = os.path.dirname(__file__)
tempDir = os.path.join(currentDir, 'tempDeNOx')
#[0.27,0.64,0.03,0.001]
for GasCompent in [[0.34,0.23,0.31,0.105],]:
    NO_EndPoint_Detail_Temp=[]
    correctionCoefiencts=0.8
    concentrationList=np.array([0,300e-6,900e-6])*correctionCoefiencts
    NSR=1.5*correctionCoefiencts
    temperatureListX=np.linspace(650+273.15,1000+273.15,5)
    cNO=0.00015
    cO2=0.06

    cNH3=NSR*cNO

        
    for concentrationIter in concentrationList:          
        for temperatureIter in temperatureListX:
            cH2Add=concentrationIter*GasCompent[0]
            cCOAdd=concentrationIter*GasCompent[1]
            cCO2=concentrationIter*GasCompent[2]+0.15
            cCH4Add=concentrationIter*GasCompent[3]
            PyChemTB.gererateInputFile(reactants=[('N2',1-cCOAdd-cCO2-cH2Add-cCH4Add-cNH3-cNO-cO2),('CO',cCOAdd),
                                    ('CO2',cCO2),('H2',cH2Add),('CH4',cCH4Add),
                                    ('NH3',cNH3),('NO',cNO),('O2',cO2)],     # Reactant (mole fraction)
                                    temperature = temperatureIter, # Temperature(K)
                                    pressure = 1 ,   # Pressure (bar)
                                    velocity=75.0,
                                    viscosity=0.0,
                                    reactorDiameter=3.2,
                                    endPosition=45.0,
                                    startPosition=0.0 ,
                                    endTime = 0.05 ,   # End Time (sec)
                                    tempFile="test.inp")                  

        
            fraction_NO_Detail_Reaction_Temp,fraction_NH3_Detail_Reaction_Temp,_=getMolesFractions(
                                                    os.path.join(currentDir,"chem_add_ITL.inp"),
                                                        os.path.join(currentDir, "test.inp"))
                  
    
            NO_EndPoint_Detail_Temp.append(fraction_NO_Detail_Reaction_Temp.iloc[-1]/fraction_NO_Detail_Reaction_Temp.iloc[0])

    NO_EndPoint_Detail_Temp_Np=np.array(NO_EndPoint_Detail_Temp)

    df=pd.DataFrame(data={'temperature':temperatureListX})
    df1=pd.DataFrame(data={'NO_Detail':NO_EndPoint_Detail_Temp_Np})   
    dftoWrite=pd.concat([df,df1],axis=1)       
    dftoWrite.to_csv("DataAnalyse\\YangmeiGas\\simulationData.csv")
    C_NO_Detail=NO_EndPoint_Detail_Temp_Np.reshape(len(concentrationList),len(temperatureListX))
    plt.figure()
    for dataLine in C_NO_Detail:        
        plt.plot(temperatureListX-273.15,dataLine,'-')
    
    data={}
    with pd.ExcelFile(r'DataAnalyse\Additive\data1ResultSynGasSNCR1.xlsx') as xls:
        data['exp_1_900'] = pd.read_excel(xls, '合成气1,900ppm ',usecols=[0, 2])
        data['smlt_1_900']=pd.read_excel(xls, '合成气1,900ppm ',usecols=[3, 5])
        data['exp_1_300'] = pd.read_excel(xls, '合成气1,300ppm',usecols=[0, 2])
        data['smlt_1_300']=pd.read_excel(xls, '合成气1,300ppm',usecols=[4, 6])
        data['exp_1_000'] = pd.read_excel(xls, 'NSR1.5,t0.6s',usecols=[0, 2])
        data['smlt_1_000']=pd.read_excel(xls, 'NSR1.5,t0.6s',usecols=[3, 5])
        
          
        symbol=iter(['s','--','^',':','*','-.'])
        for datatoplot in data:
            plt.plot(data[datatoplot].iloc[:,0],data[datatoplot].iloc[:,1],next(symbol))
        #plt.xlim((550,1100))
        plt.xlabel('Temperature ($^\circ$C)',fontsize="medium")
        plt.ylabel('[NO](out)/[NO](in)',fontsize="medium")
        plt.legend(['Simulation additive#1 900μL/L','Experiment additive#1 900μL/L',
                    'Simulation additive#1 300μL/L','Experiment additive#1 300μL/L',
                    'Simulation additive#1 0μL/L','Experiment additive#1 0μL/L'],fontsize="medium")
        #plt.savefig("DataAnalyse\\Fig\\syngasYang1.png",bbox_inches='tight')
    
    plt.show()