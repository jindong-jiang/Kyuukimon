import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import csv

class plotData:
    def __init__(self,fontTaille):
        self.fontTaille=fontTaille

    def onlyAdditive(self):
        df=pd.read_csv("DataAnalyse\\"+"CSV_4_SNCR\\additive_detail.csv",header=0).drop_duplicates()
        add2=df[abs(df["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-9*(df["Reactant Fraction for CO2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-0.15))<10e-7]
        add1=df[abs(df["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-9*(df["Reactant Fraction for CO2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-0.15))>10e-7]
        df.count()
        add1.count()
        add2.count()
        add2.head()
        add2_0=add2[add2['Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)']==0]
        add2_300=add2[add2['Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)']==8.10e-5]
        add2_900=add2[abs(add2['Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)']-2.43e-4)<10e-7]

        #add1_0=add1[add1['Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)']==0]
        add1_300=add1[abs(add1['Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)']-0.000102)<10e-7]
        add1_900=add1[abs(add1['Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)']-0.000306)<10e-7]
        import matplotlib.pyplot as plt
        from scipy.interpolate import interp1d
        def draw_image(indicator):
            plt.figure()
            #This is to analysis the data of 0ppm
            f=interp1d(add2_0['Temperature C1 PFR PFR (C1)_(C)'],add2_0[indicator],kind='cubic')
            temperature_new=np.linspace(555,1250,num=90,endpoint=True)
            plt.plot(add2_0['Temperature C1 PFR PFR (C1)_(C)'],add2_0[indicator],'*',temperature_new,f(temperature_new),'--')

            #For additive #1 NO
            #This is to analysis the data of 300ppm
            f=interp1d(add1_300['Temperature C1 PFR PFR (C1)_(C)'],add1_300[indicator],kind='cubic')
            temperature_new=np.linspace(555,1250,num=90,endpoint=True)
            plt.plot(add1_300['Temperature C1 PFR PFR (C1)_(C)'],add1_300[indicator],'^',temperature_new,f(temperature_new),'--')
            #This is to analysis the data of 900ppm
            f=interp1d(add1_900['Temperature C1 PFR PFR (C1)_(C)'],add1_900[indicator],kind='cubic')
            temperature_new=np.linspace(555,1250,num=90,endpoint=True)
            plt.plot(add1_900['Temperature C1 PFR PFR (C1)_(C)'],add1_900[indicator],'v',temperature_new,f(temperature_new),'--')

            #For additive #2  NO
            #This is to analysis the data of 300ppm
            f=interp1d(add2_300['Temperature C1 PFR PFR (C1)_(C)'],add2_300[indicator],kind='cubic')
            temperature_new=np.linspace(555,1250,num=90,endpoint=True)
            plt.plot(add2_300['Temperature C1 PFR PFR (C1)_(C)'],add2_300[indicator],'s',temperature_new,f(temperature_new),'--')
            #This is to analysis the data of 900ppm
            f=interp1d(add2_900['Temperature C1 PFR PFR (C1)_(C)'],add2_900[indicator],kind='cubic')
            temperature_new=np.linspace(555,1250,num=90,endpoint=True)
            plt.plot(add2_900['Temperature C1 PFR PFR (C1)_(C)'],add2_900[indicator],'D',temperature_new,f(temperature_new),'--')

            plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
            plt.ylabel(indicator,fontsize='large')
            plt.show()
            plt.legend(['0ppm additive','','300ppm additive#1','','900ppm addtive #1','','300ppm additive#2','','900ppm additive#2',''],fontsize='large')

        draw_image(indicator='Mole fraction NO end point')
        draw_image(indicator='Mole fraction NO2 end point')
        draw_image(indicator='Mole fraction N2O end point')
        draw_image(indicator='Mole fraction NH3 end point')       
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
    def SNCR_AdditiveDetail(self):
        df=pd.read_csv("DataAnalyse\\"+'CSV_4_SNCR\\SNCR_ADDITIVE_Detail.csv',header=0).drop_duplicates()
        df.count()
        add2=df[abs(df["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-9*(df["Reactant Fraction for CO2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-0.15))<10e-7]
        add2[add2["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]==0].count()
        # To check if the data has the right amount
        add1=df[abs(df["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-34.0/31.0*(df["Reactant Fraction for CO2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-0.15))<10e-7]
        #here we can not write 34/31, the python will take this as 1
        #add1[add1["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]==0].count()
        add1.count()
        #This is to analysys the parameter residence time
        symbol=['s','^','o']
        symbol2=[':','--','-']
        i=-1
        j=0
        k=0
        l=0
        fraction_H2=[0.34,0.27]
        Parameter_Study=['ppm NSR=','ppm  ResidTime=']
        Parameter_Study2=[' NSR ',' residence time ']
        Parameter_Value=['str(NSR)','str(45.0/velocity)']
        Parameter_Value2=['','s']
        for addx in [add1,add2]:
            i+=1
            for indicator in ['Mole fraction NO end point','Mole fraction NO2 end point','Mole fraction N2O end point','Mole fraction NH3 end point']:

                for (velocity,NSR) in zip([75.0,50.0,25.0,75,75,75],[1.5,1.5,1.5,1.5,1.8,2]):
                    j=j+1
                    if j%3==1:
                        #plt.figure()
                        lgd=[]
                        k+=1
                        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
                        plt.ylabel(indicator,fontsize='large')
                        plt.title('The Influence of'+Parameter_Study2[k%2] +'with'+' Additive#'+str(i+1),fontsize='large')
                    for concentration in [0e-6,300e-6,900e-6]:
                        l+=1
                        dataSet=addx[(abs(addx['Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)']-concentration*fraction_H2[i])<10e-7) & \
                                    (abs(addx['Axial Velocity C1 Inlet1 PFR (C1)_(cm/sec)']-velocity)<10e-7) &  \
                                    (abs(addx['Reactant Fraction for NH3 C1 Inlet1 PFR (C1)_(mole_fraction)']-0.0002*NSR)<10e-7) ].sort_values(by='Temperature C1 PFR PFR (C1)_(C)')
                        f=interp1d(dataSet['Temperature C1 PFR PFR (C1)_(C)'],dataSet[indicator],kind='cubic')
                        temperature_new=np.linspace(555,1250,num=90,endpoint=True)
                        plt.plot(dataSet['Temperature C1 PFR PFR (C1)_(C)'],dataSet[indicator],symbol[j%3],temperature_new,f(temperature_new),symbol2[l%3])
                        #lgd.append('')
                        lgd.append('additive='+str(concentration*10**6)+Parameter_Study[k%2]+eval(Parameter_Value[k%2])+Parameter_Value2[k%2])
                        lgd.append('')
                    if j%3==0:
                        #plt.legend(lgd,fontsize='xx-small')                        
                        plt.savefig("DataAnalyse\\"+'Fig\\'+indicator+'addx'+str(i)+Parameter_Study2[k%2]+'result.png',bbox_inches='tight')
                        plt.show()
                        plt.close()
    def CH4_Fig(self):
        with open( "DataAnalyse\\"+'CSV_4_SNCR\CH4_New__ADD_ITL.csv','r') as f:
            reader = csv.reader(f)
            temperatures=[]
            CH4s=[]
            NOs=[]
            for row in reader:
            # print(row)
                try:
                    Temperature=float(row[1])
                    CH4=float(row[0])
                    NO=float(row[3])
                    temperatures.append(Temperature)
                    CH4s.append(CH4)
                    NOs.append(NO)
                except:
                    continue
            s=['s','^','*','p','x']
            lgdArry=['0mg/m3 CH4','402mg/m3 CH4','804mg/m3 CH4','1206mg/m3 CH4','1608mg/m3 CH4']
            DataPoint=[]
            jj=-1
            for j in [0,1,2,3,4]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(CH4s)) if CH4s[i]==0.0003*j])
                NO_CH4_jppm = np.array([NOs[i]/0.0002 for i in range(len(CH4s)) if CH4s[i]==0.0003*j])
                f=interp1d(temperature[1:], NO_CH4_jppm[1:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[1],temperature[-1],num=90,endpoint=True)
                ltemp,=plt.plot(temperature,NO_CH4_jppm,s[jj],label=lgdArry[jj],markersize=7)
                DataPoint.append(ltemp)
                plt.plot(temperature_new,f(temperature_new),'--')
        
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
        plt.ylabel('NO out/ NO in',fontsize='large')
        plt.legend(handles=DataPoint,fontsize='large')
        plt.show()
        #plt.savefig('CH4.eps',format="eps")            
    def CO_Fig(self):
        with open( 'DataAnalyse\\'+'CSV_4_SNCR\CO_New__ADD_ITL.csv','r') as f:
            reader = csv.reader(f)
            temperatures=[]
            COs=[]
            NOs=[]
            for row in reader:
            # print(row)
                try:
                    Temperature=float(row[0])
                    CO=float(row[1])
                    NO=float(row[3])+float(row[5])
                    temperatures.append(Temperature)
                    COs.append(CO)
                    NOs.append(NO)
                except:
                    continue
            s=['s','^','*','p','x']
            lgdArry=['0mg/m3 CO','402mg/m3 CO','804mg/m3 CO','1206mg/m3 CO','1608mg/m3 CO']
            jj=-1
            DataPoint=[]
            for j in [0,1,2,3,4]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(COs)) if COs[i]==0.0003*j])
                NO_CO_0ppm = np.array([NOs[i]/0.0002 for i in range(len(COs)) if COs[i]==0.0003*j])
                f=interp1d(temperature[1:], NO_CO_0ppm[1:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[1],temperature[-1],num=90,endpoint=True)
                ltemp,=plt.plot(temperature,NO_CO_0ppm,s[jj],label=lgdArry[jj],markersize=7)
                DataPoint.append(ltemp)
                plt.plot(temperature_new,f(temperature_new),'--')
                
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
        plt.ylabel('NO out/ NO in',fontsize='large')
        plt.legend(handles=DataPoint,fontsize='large')
        plt.show()
    def H2_Fig(self):
        with open( 'DataAnalyse\\'+'CSV_4_SNCR\H2_New__ADD_ITL.csv','r') as f:
            reader = csv.reader(f)
            temperatures=[]
            H2s=[]
            NOs=[]
            for row in reader:
            # print(row)
                try:
                    Temperature=float(row[1])
                    H2=float(row[0])
                    NO=float(row[3])
                    temperatures.append(Temperature)
                    H2s.append(H2)
                    NOs.append(NO)
                except:
                    continue
            s=['s','^','*','p','x']
            lgdArry=['0mg/m3 H2','402mg/m3 H2','804mg/m3 H2','1206mg/m3 H2','1608mg/m3 H2']
            DataPoint=[]
            jj=-1
            for j in [0,1,2,3,4]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(H2s)) if H2s[i]==0.0003*j])
                NO_H2_0ppm = np.array([NOs[i]/0.0002 for i in range(len(H2s)) if H2s[i]==0.0003*j])
                f=interp1d(temperature[1:], NO_H2_0ppm[1:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[1],temperature[-1],num=90,endpoint=True)
                ltemp,=plt.plot(temperature,NO_H2_0ppm,s[jj],label=lgdArry[jj],markersize=7)
                DataPoint.append(ltemp)
                plt.plot(temperature_new,f(temperature_new),'--')
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
        plt.ylabel('[NO]out/[NO]in',fontsize='large')
        plt.legend(handles=DataPoint,fontsize='large')
        plt.show()
    def H2O_Fig(self):
        with open( 'DataAnalyse\\'+'CSV_4_SNCR\H2O_New__ADD_ITL.csv','r') as f:
            reader = csv.reader(f)
            temperatures=[]
            factors=[]
            NOs=[]
            for row in reader:
            # print(row)
                try:
                    Temperature=float(row[1])
                    factor=float(row[0])
                    NO=float(row[3])
                    temperatures.append(Temperature)
                    factors.append(factor)
                    NOs.append(NO)
                except:
                    continue
            s=['s','^','*','p','x','D']
            lgdArry=['0% H2O' ,'2% H2O' ,'4% H2O' ,'6% H2O' ,'8% H2O' ,'10% H2O' ]
            jj=-1
            DataPoint=[]
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if factors[i]==0.02*j])
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if factors[i]==0.02*j])
                f=interp1d(temperature[1:], NO_factor_j[1:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[1],temperature[-1],num=90,endpoint=True)
                ltemp,= plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=6)
                DataPoint.append(ltemp)
                plt.plot( temperature_new,f(temperature_new),'--')
                
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
        plt.ylabel('NO out/ NO in',fontsize='large')
        plt.legend(handles=DataPoint,fontsize='large')
        plt.show()
    def NO_NSR15_Fig(self):
        with open( 'DataAnalyse\\'+r'CSV_4_SNCR\NO_NSR1.5_New__ADD_ITL.csv','r') as f:
            reader = csv.reader(f)
            temperatures=[]
            factors=[]
            NOs=[]
            for row in reader:
            # print(row)
                try:
                    Temperature=float(row[0])
                    factor=float(row[2])
                    NO=float(row[4])
                    temperatures.append(Temperature)
                    factors.append(factor)
                    NOs.append(NO)
                except:
                    continue
            s=['s','^','*','p','x','D']
            jj=-1
            lgdArry=['134mg/m3 NO' ,'509mg/m3 NO' ,'884mg/m3 NO' ,'1259mg/m3 NO' ,'1634mg/m3 NO' ,'2010mg/m3 NO']
            dataPoint=[]
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-0.00028*j-0.0001)/(0.00028*j+0.0001)<10**-3])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/(0.00028*j+0.0001) for i in range(len(factors)) if abs(factors[i]-0.00028*j-0.0001)/(0.00028*j+0.0001)<10**-3])
                f=interp1d(temperature[1:], NO_factor_j[1:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[1],temperature[-1],num=90,endpoint=True)
                ltmp , = plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=6)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),'--')
                
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
        plt.ylabel('NO out/ NO in',fontsize='large')
        plt.legend(handles=dataPoint,fontsize='large')
        plt.show()
    def NSR_Fig(self):
        with open( 'DataAnalyse\\'+r'CSV_4_SNCR\NSR_New__ADD_ITL.csv','r') as f:
            reader = csv.reader(f)
            temperatures=[]
            factors=[]
            NOs=[]
            for row in reader:
                #print(row)
                try:
                    Temperature=float(row[0])
                    factor=float(row[1])
                    NO=float(row[3])
                    temperatures.append(Temperature)
                    factors.append(factor)
                    NOs.append(NO)
                except:
                    continue
            s=['s','^','*','p','x','D']
            jj=-1
            dataPoint=[]
            lgdArry=['NSR=0','NSR=0.6','NSR=1.2','NSR=1.8','NSR=2.4','NSR=3.0']
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-j*0.00012)<10**-5])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if abs(factors[i]-j*0.00012)<10**-5])
                f=interp1d(temperature[0:], NO_factor_j[0:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[0],temperature[-1],num=90,endpoint=True)
                ltmp,=plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=6)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),'--')
                
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
        plt.ylabel('NO out/ NO in',fontsize='large')
        plt.legend(handles=dataPoint,fontsize='large')
        plt.show()
    def O2_Fig(self):
        with open( 'DataAnalyse\\'+'CSV_4_SNCR\O2_NSR1.5_New__ADD_ITL.csv','r') as f:
            reader = csv.reader(f)
            temperatures=[]
            factors=[]
            NOs=[]
            for row in reader:
                #print(row)
                try:
                    Temperature=float(row[0])
                    factor=float(row[1])
                    NO=float(row[3])
                    temperatures.append(Temperature)
                    factors.append(factor)
                    NOs.append(NO)
                except:
                    continue
            s=['s','^','*','p','x','D']
            jj=-1
            lgdArry=['O2 0%' ,'O2 10%','O2 20%','O2 30%','O2 40%','O2 50%']
            dataPoint=[]
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-j*0.1)<10**-5])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if abs(factors[i]-j*0.1)<10**-5])
                f=interp1d(temperature[0:], NO_factor_j[0:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[0],temperature[-1],num=90,endpoint=True)
                ltmp,=plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=7)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),'--')
               
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
        plt.ylabel('NO out/ NO in',fontsize='large')
        plt.legend(handles=dataPoint,fontsize='large')
        plt.show()
    def pressure_Fig(self):
        with open( 'DataAnalyse\\'+'CSV_4_SNCR\Pressure_New__ADD_ITL.csv','r') as f:
            reader = csv.reader(f)
            temperatures=[]
            factors=[]
            NOs=[]
            for row in reader:
                #print(row)
                try:
                    Temperature=float(row[0])
                    factor=float(row[1])
                    NO=float(row[4])
                    temperatures.append(Temperature)
                    factors.append(factor)
                    NOs.append(NO)
                except:
                    continue
            s=['s','^','*','p','x','D']
            jj=-1
            lgdArry=['p=1atm' ,'p=2.5atm','p=4atm','p=5.5atm','p=7atm','p=8.5atm']
            dataPoint=[]
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-j*1.5-1)<10**-5])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if abs(factors[i]-j*1.5-1)<10**-5])
                f=interp1d(temperature[0:], NO_factor_j[0:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[0],temperature[-1],num=90,endpoint=True)
                ltmp,=plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=5)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),'--')
               
                plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
        plt.ylabel('NO out/ NO in',fontsize='large')
        plt.legend(handles=dataPoint,fontsize='large') 
        plt.show()   
    def pressure_NO2_Fig(self):
        with open( 'DataAnalyse\\'+'CSV_4_SNCR\Pressure_New__ADD_ITL.csv','r') as f:
            reader = csv.reader(f)
            temperatures=[]
            factors=[]
            NOs=[]
            for row in reader:
                #print(row)
                try:
                    Temperature=float(row[0])
                    factor=float(row[1])
                    NO=float(row[5])#here NO is present for NO2
                    temperatures.append(Temperature)
                    factors.append(factor)
                    NOs.append(NO)
                except:
                    continue
            s=['s','^','*','p','x','D']
            lgdArry=['p=1.0atm' ,'p=2.5atm','p=4.0atm','p=5.5atm','p=7.0atm','p=8.5atm']
            jj=-1
            dataPoint=[]
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-j*1.5-1)<10**-5])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if abs(factors[i]-j*1.5-1)<10**-5])
                f=interp1d(temperature[0:], NO_factor_j[0:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[0],temperature[-1],num=90,endpoint=True)
                ltmp,=plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=4)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),'--',markersize=1)
                
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
        plt.ylabel('NO2 out/ NO in',fontsize='large')
        plt.legend(handles=dataPoint,fontsize='large')
        plt.show()
    def Residtime_Fig(self):
        with open( 'DataAnalyse\\'+'CSV_4_SNCR\ResidTime_New__ADD_ITL.csv','r') as f:
            reader = csv.reader(f)
            temperatures=[]
            factors=[]
            NOs=[]
            for row in reader:
                #print(row)
                try:
                    Temperature=float(row[1])
                    factor=float(row[0])
                    NO=float(row[4])#here NO is present for NO2
                    temperatures.append(Temperature)
                    factors.append(factor)
                    NOs.append(NO)
                except:
                    continue
            s=['s','^','*','p','x','D']
            jj=-1
            dataPoint=[]
            lgdArry=('residence time 1.8s','residence time 0.9s','residence time 0.6s','residence time 0.45s','residence time 0.36s','residence time 0.3s')
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-j*25-25)<10**-5])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if abs(factors[i]-j*25-25)<10**-5])
                f=interp1d(temperature[0:], NO_factor_j[0:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[0],temperature[-1],num=90,endpoint=True)
                ltmp,=plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=8)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),'--')
                #plt.show()
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize='large')
        plt.ylabel('NO out/ NO in',fontsize='large')
        plt.legend(handles=dataPoint,fontsize='large')
        plt.show()
    def specificTemperatureFig(self):
        for temperatureIter in np.linspace(1100.0,1700.0,7):
            df1=pd.read_csv("DataAnalyse\\OverallForOneT\\{:.1f}KResultOverallCompare.csv".
                            format(temperatureIter))
            plt.figure()
            plt.plot(df1['Time'],df1['NO_Overall']/df1['NO_Overall'].iloc[0],'^',df1['Time'],df1['NO_Detail']/df1['NO_Overall'].iloc[0],'--')
            plt.plot(df1['Time'],df1['NH3_Overall']/df1['NH3_Overall'].iloc[0],'v',df1['Time'],df1['NH3_Detail']/df1['NH3_Overall'].iloc[0],'-.')
            plt.xlabel('ResidentTime',fontsize='large')
            plt.ylabel('[C]out/[C]in',fontsize='large')
            plt.title("De NOx Result with Temperature {0:.2f}K".format(temperatureIter))
            plt.legend(["NO: Overall Reaction","NO: Detail Reaction",
            "NH3: Overall Reaction","NH3: Detail Reaction"])
            plt.savefig("DataAnalyse\\Fig\\{:.0f}K_GA_Result.png".format(temperatureIter),bbox_inches='tight')
            plt.show()
            plt.close()
            plt.figure()
            pic02=plt.plot(df1['Time'],df1['Err_NO'],'--',
                    df1['Time'],df1['Err_NH3'],'-.')
            plt.xlabel('ResidentTime',fontsize='large')
            plt.ylabel('Error',fontsize='large')
            plt.title("Errors with Temperature {0:.2f}K".format(temperatureIter))
            plt.legend(["NO Errors between Overall Reaction Detail Reaction",
            "NH3 Errors between Overall Reaction Detail Reaction"])            
            plt.savefig("DataAnalyse\\Fig\\{:.0f}K_GA_ResultErr.png".format(temperatureIter),bbox_inches='tight') 
            plt.show()
            plt.close()
    def temperatureInterval(self):
        df1=pd.read_csv("DataAnalyse\OverallReactionForAllT\ResultOverallCompareForAllTemperature.csv")     
        temperature=df1['temperature'].dropna()
        timeList=df1['Time'].dropna()
        C_NO_Detail=df1['NO_Detail'].values.reshape(len(temperature),len(timeList))
        C_NH3_Detail=df1['NH3_Detail'].values.reshape(len(temperature),len(timeList))
        C_NO_Overall=df1.NO_Overall.values.reshape(len(temperature),len(timeList))
        C_NH3_Overall=df1.NH3_Overall.values.reshape(len(temperature),len(timeList))
        plt.figure()
        plt.plot(temperature,C_NO_Detail[:,-1]/C_NO_Detail[0],'--',temperature,C_NO_Overall[:,-1]/C_NO_Detail[0],'*')
        plt.plot(temperature,C_NO_Detail[:,-10]/C_NO_Detail[0],'-.',temperature,C_NO_Overall[:,-10]/C_NO_Detail[0],'^')
        plt.plot(temperature,C_NO_Detail[:,-15]/C_NO_Detail[0],':',temperature,C_NO_Overall[:,-15]/C_NO_Detail[0],'v')
        plt.xlabel("temperature(K)")
        plt.ylabel("[NO](in)/[NO](out)")
        plt.legend(["NO:Detail Reaction 0.6s","NO:Overall Reaction 0.6s",
                    "NO:Detail Reaction 0.3s","NO:Overall Reaction 0.3s",
                    "NO:Detail Reaction 0.15s","NO:Overall Reaction 0.15s",])
        plt.savefig("DataAnalyse\\Fig\\temperatureIntervalNO.png",bbox_inches='tight') 
        plt.show()
        plt.close()
        plt.figure()
        plt.plot(temperature,C_NH3_Detail[:,-1]/C_NH3_Detail[0],'--',temperature,C_NH3_Overall[:,-1]/C_NH3_Detail[0],'*')
        plt.plot(temperature,C_NH3_Detail[:,-10]/C_NH3_Detail[0],'-.',temperature,C_NH3_Overall[:,-10]/C_NH3_Detail[0],'^')
        plt.plot(temperature,C_NH3_Detail[:,-15]/C_NH3_Detail[0],':',temperature,C_NH3_Overall[:,-15]/C_NH3_Detail[0],'v')
        plt.xlabel("temperature(K)")
        plt.ylabel("[NH3](in)/[NH3](out)")
        plt.legend(["NH3:Detail Reaction 0.6s","NH3:Overall Reaction 0.6s",
                    "NH3:Detail Reaction 0.3s","NH3:Overall Reaction 0.3s",
                    "NH3:Detail Reaction 0.15s","NH3:Overall Reaction 0.15s",])    
        plt.savefig("DataAnalyse\\Fig\\temperatureIntervalNH3.png",bbox_inches='tight') 
        plt.show()    

if __name__=='__main__':
    figPlotter=plotData('large')
    figPlotter.temperatureInterval()
