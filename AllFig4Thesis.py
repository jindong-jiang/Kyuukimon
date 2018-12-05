import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d



class plotData:
    def __init__(self,fontTaille):
        self.fontTaille=fontTaille

    def verifyCaoQingXi(self):        
        symbol=iter(['^','s'])
        s=['-.','--']
        titleJ=iter([' with the Additive CH4',' with the Additive H2'])
        initialCncntrtn=[0.0005,0.00023]
        correct=[0,0]
        iC=0
        for filename1, filename2 in zip(['CaoQingXi_With_CH4.csv','CaoQingXi_With_H2.csv' ],['E_CH4.csv','E_H2.csv']):

            #plt.figure()
            df=pd.read_csv("DataAnalyse"+'\\CaoQingXi_Verifier\\'+filename1,header=0)
            df_experiment=pd.read_csv("DataAnalyse\\"+'CaoQingXi_Verifier\\'+filename2 ,header=0)
            df_experiment.head()

            f=interp1d(df['Temperature C1 PFR PFR (C1)_(C)'],df['Mole fraction NO end point'],kind='cubic')
            temperature_new=np.linspace(555,1245,num=90,endpoint=True)
            plt.plot(df_experiment['Temperature_K']-273.15--correct[iC],df_experiment['NO']*10**(-6)/initialCncntrtn[iC], next(symbol),temperature_new,f(temperature_new)/initialCncntrtn[iC],s[iC],markersize=8)
            iC=iC+1
        df_CO=pd.read_csv("DataAnalyse\\"+"CSV_4_SNCR\\LiDe-longYangMeiPapersTestify\CO.csv",header=0).drop_duplicates()
        df_CO.head()
        df1=pd.read_csv("DataAnalyse\\"+"""CSV_4_SNCR\\LiDe-longYangMeiPapersTestify\\testify_LiDeLong.csv""",header=0).drop_duplicates()
        df_CO_Simulation=df1[abs(df1['Reactant Fraction for CO C1 Inlet1 PFR (C1)_(mole_fraction)']-0.0009)<10e-6].sort_values(by='Temperature C1 PFR PFR (C1)_(C)')
        df_CO_experiment=pd.read_csv("DataAnalyse\\"+"CSV_4_SNCR\\LiDe-longYangMeiPapersTestify\CO.csv",header=0).drop_duplicates()
        f=interp1d(df_CO_Simulation['Temperature C1 PFR PFR (C1)_(C)'],df_CO_Simulation['Mole fraction NO end point'],kind='cubic')
        temperature_new=np.linspace(555,1245,num=90,endpoint=True)
        plt.plot(df_CO_experiment['temperature'],df_CO_experiment['NOout/Noin']/100,'*',temperature_new,f(temperature_new)/0.0002,markersize=8)

        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
        plt.ylabel('NO out/NO in',fontsize='large')
        plt.legend(['Experiment Result of CH4','Simulation Result of CH4','Experiment Result of H2','Simulation Result of H2','Experiment Result of CO','Simulation Result of CO'])
        plt.title('DeNOx Result with different Additives')
        plt.show()

        df=pd.read_csv("DataAnalyse\\"+"CaoQingXi_Verifier\caoqingxi_300_900.csv",header=0)
        df.head()
        s=['*','^']
        i=0
        for concenration in [0.0003,0.0009]:
            plt.figure()
            plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
            plt.ylabel('NO out/ NO in',fontsize='large')
            plt.title('DeNOx Result of SNCR with '+str(int(concenration*1e6*1.34))+"mg/m3"+" additive",fontsize='large')
            for species in ['CH4','CO']:
                i=i+1
                curve=df[df['Reactant Fraction for '+species+' C1 Inlet1 PFR (C1)_(mole_fraction)']==concenration]
                f=interp1d(curve['Temperature C1 PFR PFR (C1)_(C)'],curve['Mole fraction NO end point'],kind='slinear')
                temperature_new=np.linspace(555,1250,num=90,endpoint=True)
                plt.plot(temperature_new,f(temperature_new)/0.0003)

                df_exp=pd.read_csv("DataAnalyse\\"+"CaoQingXi_Verifier\\"+str(int(concenration*1e6))+"ppm"+species+'.csv',header=0)
                plt.plot(df_exp['x'],df_exp['y'],s[i%2])
            plt.legend(['CH4 Simulation','CH4 Experiment','CO Simulation','CO Experiment'])
        plt.show()

if __name__=='__main__':
    figPlotter=plotData('large')
    figPlotter.verifyCaoQingXi()
