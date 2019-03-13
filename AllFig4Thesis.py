import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import csv
from scipy.optimize import curve_fit
 

class plotData:
    def __init__(self,fontTaille):
        self.fontTaille=fontTaille
        self.axissize="medium"
        self.lgdsize="medium"
        self.mkrSize=5
        
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
            plt.plot(temperature_new,f(temperature_new)/(200e-6),'o--',markersize=self.mkrSize)

            #For additive #1 NO
            #This is to analysis the data of 300ppm
            f=interp1d(add1_300['Temperature C1 PFR PFR (C1)_(C)'],add1_300[indicator],kind='cubic')
            temperature_new=np.linspace(555,1250,num=90,endpoint=True)
            plt.plot(temperature_new,f(temperature_new)/(200e-6),'*--',markersize=self.mkrSize)
            #This is to analysis the data of 900ppm
            f=interp1d(add1_900['Temperature C1 PFR PFR (C1)_(C)'],add1_900[indicator],kind='cubic')
            temperature_new=np.linspace(555,1250,num=90,endpoint=True)
            plt.plot(temperature_new,f(temperature_new)/(200e-6),'P--',markersize=self.mkrSize)

            #For additive #2  NO
            #This is to analysis the data of 300ppm
            f=interp1d(add2_300['Temperature C1 PFR PFR (C1)_(C)'],add2_300[indicator],kind='cubic')
            temperature_new=np.linspace(555,1250,num=90,endpoint=True)
            plt.plot(temperature_new,f(temperature_new)/(200e-6),'d--',markersize=self.mkrSize)
            #This is to analysis the data of 900ppm
            f=interp1d(add2_900['Temperature C1 PFR PFR (C1)_(C)'],add2_900[indicator],kind='cubic')
            temperature_new=np.linspace(555,1250,num=90,endpoint=True)
            plt.plot(temperature_new,f(temperature_new)/(200e-6),'<--',markersize=self.mkrSize)
            species=indicator.split(" ")[2]
            plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
            plt.ylabel("["+species+"](out)/[NO](in)",fontsize=self.axissize)            
            plt.legend(['0μL/L additive','300μL/L additive#1','900μL/L addtive #1','300μL/L additive#2','900μL/L additive#2'],fontsize=self.lgdsize)
            plt.savefig("DataAnalyse\\Fig\\"+indicator.replace(" ","")+".png",bbox_inches='tight')   
            plt.close()
        draw_image(indicator='Mole fraction NO end point')
        draw_image(indicator='Mole fraction NO2 end point')
        draw_image(indicator='Mole fraction N2O end point')
        draw_image(indicator='Mole fraction NH3 end point')       
    def Additive_NSR0(self):
        df=pd.read_csv('DataAnalyse\CSV_4_SNCR\SNCR_NSR=0_T100.csv',header=0).drop_duplicates()
        df.count()
        add2=df[abs(df["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-9.0*(df["Reactant Fraction for CO2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-0.15))<10e-6]
        add2.count()
        add1=df[abs(df["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-34.0/31.0*(df["Reactant Fraction for CO2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-0.15))<10e-7]
        #here we can not write 34/31, the python will take this as 1
        #add1[add1["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]==0].count()
        add1.count()
        h2_add1=np.linspace(0.000102,0.002754,num=14).tolist()
        h2_add1.insert(0,0)# the first time I used h2_add1=h2_add1.inset, but it doesn t work, the result is not in the return value of insert
        h2_add1=np.asarray(h2_add1[0:14:2])[[0,1,2,4,6]]
        h2_add2=np.linspace(0.27*3e-4,0.27*8.1e-3,num=14).tolist()
        h2_add2.insert(0,0)# the first time I used h2_add1=h2_add1.inset, but it doesn t work, the result is not in the return value of insert
        #h2_add2=np.asarray(h2_add2[1:14:3])
        h2_add2=np.asarray([0,0.000081,0.000243,0.000405,0.000567,0.000729,0.000891,0.001053,0.001215,0.001377,0.001539,0.001701,0.001863, \
                            0.002025,0.002187][0:14:2])[[0,1,2,4,6]]
        h2_percentage=[0.34,0.27]
        symbol=['s','^','o','*','v','d','p']
        k=0
        for i in [0,1]:
            addx=[add1,add2][i]
            h2_addx=[h2_add1,h2_add2][i]
            addx['Mole_Fraction_NOx']=addx['Mole fraction NO2 end point']+addx['Mole fraction NO end point']+addx['Mole fraction N2O end point']
            for indicator in ['Mole fraction NO end point','Mole fraction NO2 end point','Mole fraction N2O end point','Mole_Fraction_NOx']:
                plt.figure()
                plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
                try:
                    ylbl="["+indicator.split(" ")[2]+"](out)/[NO](in)"
                except:
                    ylbl="["+indicator.split("_")[2]+"](out)/[NO](in)"
                plt.ylabel(ylbl,fontsize=self.axissize)
                lgd=[]
                for h2 in h2_addx:
                    
                    k=k+1
                    dataSet=addx[abs(addx['Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)']-h2)<10e-6]
                    f=interp1d(dataSet['Temperature C1 PFR PFR (C1)_(C)'],dataSet[indicator],kind='slinear')
                    temperature_new=np.linspace(100,1240,num=90,endpoint=True)
                    plt.plot(temperature_new,f(temperature_new)/(200e-6),symbol[k%7]+'--',markersize=self.mkrSize-2)
                    lgd.append('Addtive#'+str(i+1)+':'+"{:.0f}μL/L".format(h2/h2_percentage[i]*1e6))                    
                plt.legend(lgd,fontsize=self.lgdsize)
                if indicator=='Mole_Fraction_NOx':
                    plt.ylim(ymin=0.95)
                #plt.yticks(range(0,1.1,0.2))
                plt.savefig("DataAnalyse\\Fig\\"+ylbl.replace("/","")+".png",bbox_inches='tight')
        df2=pd.read_csv(r'DataAnalyse\CSV_4_SNCR\NSR_New__ADD_ITL.csv',header=0)
        df2['Mole Fraction NOx']=df2['Mole fraction NO2 end point']+df2['Mole fraction NO end point']+df2['Mole fraction N2O end point']
        symbol=['s','^','o','*','v','d','1']
        l=0
        for indicator in ['Mole fraction NO end point','Mole fraction NO2 end point','Mole fraction N2O end point','Mole Fraction NOx']:
            plt.figure()
            plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
            try:
                ylbl="["+indicator.split(" ")[2]+"](out)/[NO](in)"
            except:
                ylbl="["+indicator.split("_")[2]+"](out)/[NO](in)"
            plt.ylabel(ylbl,fontsize=self.axissize)
            lgd=[]
            for j in np.array([0,1,2,3,4]):
                l+=1
                dataSet=df2[abs(df2['Reactant Fraction for NH3 C1 Inlet1 PFR (C1)_(mole_fraction)']-0.00012*j)<10e-7].drop_duplicates()
                f=interp1d(dataSet['Temperature C1 PFR PFR (C1)_(C)'],dataSet[indicator],kind='cubic')
                temperature_new=np.linspace(550,1250,num=90,endpoint=True)
                plt.plot(temperature_new,f(temperature_new)/(200e-6),symbol[l%6]+'--',markersize=self.mkrSize-2)
                lgd.append('NSR='+"{:.1f}".format(j*0.00012/0.0002)+":"+"NH3:"+str(j*0.00012*1e6)+"μL/L")                
            plt.legend(lgd,fontsize=self.axissize)
            
            plt.savefig("DataAnalyse\\Fig\\"+ylbl.replace("/","_")+".png",bbox_inches='tight')
            plt.close()
    def Additive_NSR_different(self):
        df=pd.read_csv('DataAnalyse\\CSV_4_SNCR\\NSR=06_1_12_Additive.csv',header=0).drop_duplicates()
        df['Mole Fraction NOx']=df['Mole fraction NO2 end point']+df['Mole fraction NO end point']+df['Mole fraction N2O end point']
        df.count()
        add2=df[abs(df["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-9.0*(df["Reactant Fraction for CO2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-0.15))<10e-7]
        add2.count()
        add1=df[abs(df["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-34.0/31.0*(df["Reactant Fraction for CO2 C1 Inlet1 PFR (C1)_(mole_fraction)"]-0.15))<10e-7]
        #here we can not write 34/31, the python will take this as 1
        #add1[add1["Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)"]==0].count()
        
        symbol=['p','^','X','*','v','s','P','o']
        for i in [1,2]:
            addx=[add1,add2][i-1]
            H2_Initial=[0.000408,0.000324][i-1]
            for NSR in [0.6,1,1.2]:
                for indicator in ['Mole fraction NO end point','Mole fraction NO2 end point','Mole fraction N2O end point','Mole fraction NH3 end point','Mole Fraction NOx']:
                    plt.figure()
                    plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
                    try:
                        ylbl="["+indicator.split(" ")[2]+"](out)/[NO](in)"
                    except:
                        ylbl="["+indicator.split("_")[2]+"](out)/[NO](in)"
                    plt.ylabel(ylbl,fontsize=self.axissize)
                    
                    #plt.title('NSR='+str(NSR))
                    lgd=[]
                    for j in [0,1,2,4,7]:
                        dataSet=addx[(addx['Reactant Fraction for NH3 C1 Inlet1 PFR (C1)_(mole_fraction)']==NSR*0.0002) & (abs(addx['Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)']-H2_Initial*j)<10e-7)]
                        f=interp1d(dataSet['Temperature C1 PFR PFR (C1)_(C)'],dataSet[indicator],kind='cubic')
                        temperature_new=np.linspace(100,1240,num=90,endpoint=True)
                        plt.plot(temperature_new,f(temperature_new)/(200e-6),symbol[j]+'--',markersize=4)
                        lgd.append('Addtive#'+str(i)+'='+str(0.0012*j))                        
                    plt.legend(lgd,fontsize=self.lgdsize)
                    plt.savefig('DataAnalyse\\Fig\\NSR'+str(NSR)+ylbl.replace("/","_")+".png",bbox_inches='tight')
                    plt.close()
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
            plt.plot(df_experiment['Temperature_K']-273.15--correct[iC],df_experiment['NO']*10**(-6)/initialCncntrtn[iC], next(symbol),temperature_new,f(temperature_new)/initialCncntrtn[iC],s[iC],markersize=self.mkrSize)
            iC=iC+1
        df_CO=pd.read_csv("DataAnalyse\\"+"CSV_4_SNCR\\LiDe-longYangMeiPapersTestify\CO.csv",header=0).drop_duplicates()
        df_CO.head()
        df1=pd.read_csv("DataAnalyse\\"+"""CSV_4_SNCR\\LiDe-longYangMeiPapersTestify\\testify_LiDeLong.csv""",header=0).drop_duplicates()
        df_CO_Simulation=df1[abs(df1['Reactant Fraction for CO C1 Inlet1 PFR (C1)_(mole_fraction)']-0.0009)<10e-6].sort_values(by='Temperature C1 PFR PFR (C1)_(C)')
        df_CO_experiment=pd.read_csv("DataAnalyse\\"+"CSV_4_SNCR\\LiDe-longYangMeiPapersTestify\CO.csv",header=0).drop_duplicates()
        f=interp1d(df_CO_Simulation['Temperature C1 PFR PFR (C1)_(C)'],df_CO_Simulation['Mole fraction NO end point'],kind='cubic')
        temperature_new=np.linspace(555,1245,num=90,endpoint=True)
        plt.plot(df_CO_experiment['temperature'],df_CO_experiment['NOout/Noin']/100,'*',temperature_new,f(temperature_new)/0.0002,markersize=self.mkrSize)

        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize )
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(['Experiment Result of CH4','Simulation Result of CH4','Experiment Result of H2','Simulation Result of H2','Experiment Result of CO','Simulation Result of CO'],
                    fontsize=self.lgdsize)
        #plt.title('DeNOx Result with different Additives')
        plt.savefig("DataAnalyse\\Fig\\verifyCaoQingxi1.png",bbox_inches='tight')

        df=pd.read_csv("DataAnalyse\\"+"CaoQingXi_Verifier\caoqingxi_300_900.csv",header=0)
        df.head()
        s=['*','^']
        i=0
        for concenration in [0.0003,0.0009]:
            plt.figure()
            plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
            plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
            #plt.title('DeNOx Result of SNCR with '+str(int(concenration*1e6*1.34))+"mg/m3"+" additive",fontsize='large')
            for species in ['CH4','CO']:
                i=i+1
                curve=df[df['Reactant Fraction for '+species+' C1 Inlet1 PFR (C1)_(mole_fraction)']==concenration]
                f=interp1d(curve['Temperature C1 PFR PFR (C1)_(C)'],curve['Mole fraction NO end point'],kind='slinear')
                temperature_new=np.linspace(555,1250,num=90,endpoint=True)
                plt.plot(temperature_new,f(temperature_new)/0.0003)

                df_exp=pd.read_csv("DataAnalyse\\"+"CaoQingXi_Verifier\\"+str(int(concenration*1e6))+"ppm"+species+'.csv',header=0)
                plt.plot(df_exp['x'],df_exp['y'],s[i%2])
            plt.legend(['CH4 Simulation','CH4 Experiment','CO Simulation','CO Experiment'],fontsize=self.lgdsize)
            plt.savefig("DataAnalyse\\Fig\\verifyCaoQingxi{:.0f}mg.png".format(concenration*1e6*1.34),bbox_inches='tight')
        plt.close()
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
                        plt.figure()
                        lgd=[]
                        k+=1
                        ylbl="["+indicator.split(" ")[2]+"](out)/[NO](in)"
                        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
                        plt.ylabel(ylbl,fontsize=self.axissize)
                        #plt.title('The Influence of'+Parameter_Study2[k%2] +'with'+' Additive#'+str(i+1),fontsize='large')
                    for concentration in [0e-6,300e-6,900e-6]:
                        l+=1
                        dataSet=addx[(abs(addx['Reactant Fraction for H2 C1 Inlet1 PFR (C1)_(mole_fraction)']-concentration*fraction_H2[i])<10e-7) & \
                                    (abs(addx['Axial Velocity C1 Inlet1 PFR (C1)_(cm/sec)']-velocity)<10e-7) &  \
                                    (abs(addx['Reactant Fraction for NH3 C1 Inlet1 PFR (C1)_(mole_fraction)']-0.0002*NSR)<10e-7) ].sort_values(by='Temperature C1 PFR PFR (C1)_(C)')
                        f=interp1d(dataSet['Temperature C1 PFR PFR (C1)_(C)'],dataSet[indicator],kind='cubic')
                        temperature_new=np.linspace(555,1250,num=90,endpoint=True)
                        plt.plot(dataSet['Temperature C1 PFR PFR (C1)_(C)'],dataSet[indicator]/(200e-6),symbol[j%3],temperature_new,f(temperature_new)/(200e-6),symbol2[l%3],markersize=self.mkrSize)
                        #lgd.append('')
                        #lgd.append('additive='+str(concentration*10**6)+Parameter_Study[k%2]+eval(Parameter_Value[k%2])+Parameter_Value2[k%2])
                        #lgd.append('')
                    if j%3==0:
                        #plt.legend(lgd,fontsize='xx-small')                        
                        plt.savefig("DataAnalyse\\"+'Fig\\'+indicator+'addx'+str(i)+Parameter_Study2[k%2]+'result.png',bbox_inches='tight')
                        #plt.show()
                        plt.close()
    def CH4_Fig(self):
        plt.figure()
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
            s=['s','^','*','p','X']
            lgdArry=['0mg/m3 CH4','402mg/m3 CH4','804mg/m3 CH4','1206mg/m3 CH4','1608mg/m3 CH4']
            DataPoint=[]
            jj=-1
            for j in [0,1,2,3,4]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(CH4s)) if CH4s[i]==0.0003*j])
                NO_CH4_jppm = np.array([NOs[i]/0.0002 for i in range(len(CH4s)) if CH4s[i]==0.0003*j])
                f=interp1d(temperature[1:], NO_CH4_jppm[1:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[1],temperature[-1],num=90,endpoint=True)
                ltemp,=plt.plot(temperature,NO_CH4_jppm,s[jj],label=lgdArry[jj],markersize=self.mkrSize)
                DataPoint.append(ltemp)
                plt.plot(temperature_new,f(temperature_new),'--')
        
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(handles=DataPoint,fontsize=self.lgdsize)
        #plt.show()
        plt.savefig("DataAnalyse\\Fig\\CH4.png",bbox_inches='tight')            
    def CO_Fig(self):
        plt.figure()
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
            s=['s','^','*','p','X']
            lgdArry=['0mg/m3 CO','402mg/m3 CO','804mg/m3 CO','1206mg/m3 CO','1608mg/m3 CO']
            jj=-1
            DataPoint=[]
            for j in [0,1,2,3,4]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(COs)) if COs[i]==0.0003*j])
                NO_CO_0ppm = np.array([NOs[i]/0.0002 for i in range(len(COs)) if COs[i]==0.0003*j])
                f=interp1d(temperature[1:], NO_CO_0ppm[1:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[1],temperature[-1],num=90,endpoint=True)
                ltemp,=plt.plot(temperature,NO_CO_0ppm,s[jj],label=lgdArry[jj],markersize=self.mkrSize)
                DataPoint.append(ltemp)
                plt.plot(temperature_new,f(temperature_new),'--')
                
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(handles=DataPoint,fontsize=self.lgdsize)
        #plt.show()
        plt.savefig("DataAnalyse\\Fig\\CO.png",bbox_inches='tight') 
    def H2_Fig(self):
        plt.figure()
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
            s=['s','^','*','p','X']
            lgdArry=['0mg/m3 H2','402mg/m3 H2','804mg/m3 H2','1206mg/m3 H2','1608mg/m3 H2']
            DataPoint=[]
            jj=-1
            for j in [0,1,2,3,4]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(H2s)) if H2s[i]==0.0003*j])
                NO_H2_0ppm = np.array([NOs[i]/0.0002 for i in range(len(H2s)) if H2s[i]==0.0003*j])
                f=interp1d(temperature[1:], NO_H2_0ppm[1:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[1],temperature[-1],num=90,endpoint=True)
                ltemp,=plt.plot(temperature,NO_H2_0ppm,s[jj],label=lgdArry[jj],markersize=self.mkrSize)
                DataPoint.append(ltemp)
                plt.plot(temperature_new,f(temperature_new),'--')
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(handles=DataPoint,fontsize=self.lgdsize)
        #plt.show()
        plt.savefig("DataAnalyse\\Fig\\H2.png",bbox_inches='tight') 
    def H2O_Fig(self):
        plt.figure()
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
            s=['s','^','*','p','X','D']
            lgdArry=['0% H2O' ,'2% H2O' ,'4% H2O' ,'6% H2O' ,'8% H2O' ,'10% H2O' ]
            jj=-1
            DataPoint=[]
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if factors[i]==0.02*j])
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if factors[i]==0.02*j])
                f=interp1d(temperature[1:], NO_factor_j[1:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[1],temperature[-1],num=90,endpoint=True)
                ltemp,= plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=self.mkrSize)
                DataPoint.append(ltemp)
                plt.plot( temperature_new,f(temperature_new),'--')
                
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(handles=DataPoint,fontsize=self.lgdsize)
        #plt.show()
        plt.savefig("DataAnalyse\\Fig\\H2O.png",bbox_inches='tight') 
    def NO_NSR15_Fig(self):
        plt.figure()
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
            s=['s','^','*','p','X','D']
            jj=-1
            lgdArry=['134mg/m3 NO' ,'509mg/m3 NO' ,'884mg/m3 NO' ,'1259mg/m3 NO' ,'1634mg/m3 NO' ,'2010mg/m3 NO']
            dataPoint=[]
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-0.00028*j-0.0001)/(0.00028*j+0.0001)<10**-3])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/(0.00028*j+0.0001) for i in range(len(factors)) if abs(factors[i]-0.00028*j-0.0001)/(0.00028*j+0.0001)<10**-3])
                f=interp1d(temperature[1:], NO_factor_j[1:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[1],temperature[-1],num=90,endpoint=True)
                ltmp , = plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=self.mkrSize)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),'--')
                
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(handles=dataPoint,fontsize=self.lgdsize)
        #plt.show()
        plt.savefig("DataAnalyse\\Fig\\NO_NSR1.5.png",bbox_inches='tight') 
    def NSR_Fig(self):
        plt.figure()
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
            s=['s','^','*','p','X','D']
            jj=-1
            dataPoint=[]
            lgdArry=['NSR=0','NSR=0.6','NSR=1.2','NSR=1.8','NSR=2.4','NSR=3.0']
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-j*0.00012)<10**-5])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if abs(factors[i]-j*0.00012)<10**-5])
                f=interp1d(temperature[0:], NO_factor_j[0:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[0],temperature[-1],num=90,endpoint=True)
                ltmp,=plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=self.mkrSize)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),'--')
                
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(handles=dataPoint,fontsize=self.lgdsize)
        #plt.show()
        plt.savefig("DataAnalyse\\Fig\\NSR.png",bbox_inches='tight') 
    def O2_Fig(self):
        plt.figure()
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
            s=['s','^','*','p','X','D']
            jj=-1
            lgdArry=['O2 0%' ,'O2 10%','O2 20%','O2 30%','O2 40%','O2 50%']
            dataPoint=[]
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-j*0.1)<10**-5])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if abs(factors[i]-j*0.1)<10**-5])
                f=interp1d(temperature[0:], NO_factor_j[0:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[0],temperature[-1],num=90,endpoint=True)
                ltmp,=plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=self.mkrSize)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),'--')
               
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(handles=dataPoint,fontsize=self.lgdsize)
        #plt.show()
        plt.savefig("DataAnalyse\\Fig\\O2.png",bbox_inches='tight') 
    def pressure_Fig(self):
        plt.figure()
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
            s=['s','^','*','p','X','D']
            jj=-1
            lgdArry=['p=1atm' ,'p=2.5atm','p=4atm','p=5.5atm','p=7atm','p=8.5atm']
            dataPoint=[]
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-j*1.5-1)<10**-5])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if abs(factors[i]-j*1.5-1)<10**-5])
                f=interp1d(temperature[0:], NO_factor_j[0:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[0],temperature[-1],num=90,endpoint=True)
                ltmp,=plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=self.mkrSize)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),'--')
               
                plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(handles=dataPoint,fontsize=self.lgdsize)
        #plt.show()
        plt.savefig("DataAnalyse\\Fig\\pressureNO.png",bbox_inches='tight')   
    def pressure_NO2_Fig(self):
        plt.figure()
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
            s=['s','^','*','p','X','D']
            lgdArry=['p=1.0atm' ,'p=2.5atm','p=4.0atm','p=5.5atm','p=7.0atm','p=8.5atm']
            jj=-1
            dataPoint=[]
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-j*1.5-1)<10**-5])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if abs(factors[i]-j*1.5-1)<10**-5])
                f=interp1d(temperature[0:], NO_factor_j[0:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[0],temperature[-1],num=90,endpoint=True)
                ltmp,=plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=5)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),':',markersize=1)
                
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO2](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(handles=dataPoint,fontsize=self.lgdsize)
        #plt.show()
        plt.savefig("DataAnalyse\\Fig\\pressureNO2.png",bbox_inches='tight') 
    def Residtime_Fig(self):
        plt.figure()
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
            s=['s','^','*','p','X','D']
            jj=-1
            dataPoint=[]
            lgdArry=('residence time 1.8s','residence time 0.9s','residence time 0.6s','residence time 0.45s','residence time 0.36s','residence time 0.3s')
            for j in [0,1,2,3,4,5]:
                jj=jj+1
                temperature= np.array( [temperatures[i] for i in range(len(factors)) if abs(factors[i]-j*25-25)<10**-5])# the data can not be the value exacte,the range is necessary
                NO_factor_j = np.array([NOs[i]/0.0002 for i in range(len(factors)) if abs(factors[i]-j*25-25)<10**-5])
                f=interp1d(temperature[0:], NO_factor_j[0:],kind='cubic')# the 2 minimum values can not be the same

                temperature_new=np.linspace(temperature[0],temperature[-1],num=90,endpoint=True)
                ltmp,=plt.plot(temperature,NO_factor_j,s[jj],label=lgdArry[jj],markersize=self.mkrSize)
                dataPoint.append(ltmp)
                plt.plot(temperature_new,f(temperature_new),'--')
                #plt.show()
            # plt.hold(True)
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(handles=dataPoint,fontsize=self.lgdsize)
        #plt.show()
        plt.savefig("DataAnalyse\\Fig\\resTime.png",bbox_inches='tight') 
    def specificTemperatureFig(self):
        for temperatureIter in np.linspace(1100.0,1700.0,7):
            df1=pd.read_csv("DataAnalyse\\OverallForOneT\\{:.1f}KResultOverallCompare.csv".
                            format(temperatureIter))
            plt.figure()
            plt.plot(df1['Time'],df1['NO_Overall']/df1['NO_Overall'].iloc[0],'^',df1['Time'],df1['NO_Detail']/df1['NO_Overall'].iloc[0],'--')
            plt.plot(df1['Time'],df1['NH3_Overall']/df1['NH3_Overall'].iloc[0],'v',df1['Time'],df1['NH3_Detail']/df1['NH3_Overall'].iloc[0],'-.')
            plt.xlabel('ResidenceTime(s)',fontsize=self.axissize)
            plt.ylabel('[C](out)/[C](in)',fontsize=self.axissize)
            #plt.title("De NOx Result with Temperature {0:.2f}K".format(temperatureIter))
            plt.legend(["NO: Overall Reaction","NO: Detail Reaction",
            "NH3: Overall Reaction","NH3: Detail Reaction"],fontsize=self.lgdsize)
            plt.savefig("DataAnalyse\\Fig\\{:.0f}K_GA_Result.png".format(temperatureIter-273.15),bbox_inches='tight')
            #plt.show()
            plt.close()
            plt.figure()
            pic02=plt.plot(df1['Time'],df1['Err_NO'],'--',
                    df1['Time'],df1['Err_NH3'],'-.')
            plt.xlabel('ResidenceTime(s)',fontsize=self.axissize)
            plt.ylabel('Error',fontsize=self.axissize)
            plt.gca().yaxis.get_major_formatter().set_powerlimits((0,1)) 
            #plt.title("Errors with Temperature {0:.2f}K".format(temperatureIter))
            plt.legend(["NO Errors between Overall Reaction Detail Reaction",
            "NH3 Errors between Overall Reaction Detail Reaction"],fontsize=self.lgdsize)            
            plt.savefig("DataAnalyse\\Fig\\{:.0f}C_GA_ResultErr.png".format(temperatureIter-273.15),bbox_inches='tight') 
            #plt.show()
            plt.close()
    def temperatureInterval(self):
        df1=pd.read_csv("DataAnalyse\OverallReactionForAllT\ResultOverallCompareForAllTemperature.csv")     
        temperature=df1['temperature'].dropna()-273
        timeList=df1['Time'].dropna()
        C_NO_Detail=df1['NO_Detail'].values.reshape(len(temperature),len(timeList))
        C_NH3_Detail=df1['NH3_Detail'].values.reshape(len(temperature),len(timeList))
        C_NO_Overall=df1.NO_Overall.values.reshape(len(temperature),len(timeList))
        C_NH3_Overall=df1.NH3_Overall.values.reshape(len(temperature),len(timeList))
        plt.figure()
        plt.plot(temperature,C_NO_Detail[:,-1]/C_NO_Detail[0],'--',temperature,C_NO_Overall[:,-1]/C_NO_Detail[0],'*')
        plt.plot(temperature,C_NO_Detail[:,-10]/C_NO_Detail[0],'-.',temperature,C_NO_Overall[:,-10]/C_NO_Detail[0],'^')
        plt.plot(temperature,C_NO_Detail[:,-15]/C_NO_Detail[0],':',temperature,C_NO_Overall[:,-15]/C_NO_Detail[0],'v')
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel("[NO](in)/[NO](out)",fontsize=self.axissize)
        plt.legend(["NO:Detail Reaction 0.6s","NO:Overall Reaction 0.6s",
                    "NO:Detail Reaction 0.3s","NO:Overall Reaction 0.3s",
                    "NO:Detail Reaction 0.15s","NO:Overall Reaction 0.15s",],fontsize=self.lgdsize)
        plt.savefig("DataAnalyse\\Fig\\temperatureIntervalNO.png",bbox_inches='tight') 
        #plt.show()
        plt.close()
        plt.figure()
        plt.plot(temperature,C_NH3_Detail[:,-1]/C_NH3_Detail[0],'--',temperature,C_NH3_Overall[:,-1]/C_NH3_Detail[0],'*')
        plt.plot(temperature,C_NH3_Detail[:,-10]/C_NH3_Detail[0],'-.',temperature,C_NH3_Overall[:,-10]/C_NH3_Detail[0],'^')
        plt.plot(temperature,C_NH3_Detail[:,-15]/C_NH3_Detail[0],':',temperature,C_NH3_Overall[:,-15]/C_NH3_Detail[0],'v')
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel("[NH3](in)/[NH3](out)",fontsize=self.axissize)
        plt.legend(["NH3:Detail Reaction 0.6s","NH3:Overall Reaction 0.6s",
                    "NH3:Detail Reaction 0.3s","NH3:Overall Reaction 0.3s",
                    "NH3:Detail Reaction 0.15s","NH3:Overall Reaction 0.15s",],fontsize=self.lgdsize)    
        plt.savefig("DataAnalyse\\Fig\\temperatureIntervalNH3.png",bbox_inches='tight') 
        #plt.show()    
    def Additive_Overall_Fig(self):
        species=['CH4','CO','H2']
        methodeNum=[1,2]
        for speciesX in species:
            for iM in methodeNum:    
                df1=pd.read_csv('DataAnalyse\\Additive\\'+speciesX+'ResultAdditiveCompare'+str(iM)+'.csv')
                temperature=df1['temperatureListX'].dropna()-273
                SpicieslistAdd=df1[speciesX+'listAdd'].dropna()
                C_Detail=df1[speciesX+'Detail'].values.reshape(len(SpicieslistAdd),len(temperature))
                C_Overall=df1[speciesX+'Overall'].values.reshape(len(SpicieslistAdd),len(temperature))
                plt.figure()
                symbol=['*','^','v']
                lgd=[]
                for i in np.arange(3):
                    plt.plot(temperature,C_Detail[i,:]/C_Detail[i,0],'--',temperature,C_Overall[i,:]/C_Overall[i,0],symbol[i])
                    lgd.append("NO:Detail Reaction "+speciesX+" {:.0f}μL/L".format(SpicieslistAdd[i]*1e6))
                    lgd.append("NO:Overall Reaction "+speciesX+" {:.0f}μL/L".format(SpicieslistAdd[i]*1e6))
                plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
                plt.ylabel("[NO](in)/[NO](out)",fontsize=self.axissize)
                plt.ylim(0,2.2)
                plt.legend(lgd,fontsize=self.lgdsize)
                plt.savefig("DataAnalyse\\Fig\\AdditiveOverall"+speciesX+"Methode"+str(iM)+".png",bbox_inches='tight')
    def AdditiveTemperatureShift(self):
        def func(x,a,b):
            return a*np.log(b*x+1)
    
        def func1(x,a,b):
            return a*x/(b+x)            

        def AnalyseData(funEmployelist):
            for speciesAdd in ['H2','CH4','CO']:
                              
                file1=pd.read_csv(speciesAdd+"TemperatureShift.csv",',',header=None)
                cAdd=file1.iloc[0,:].values
                TemperatureShift=file1.iloc[1,:].values
                plt.figure()
                plt.plot(cAdd*1e6,TemperatureShift,'*')
                s=iter(["r--","b.--"])
                for funEmploye in funEmployelist:  
                    popt,pcov=curve_fit(funEmploye,cAdd,TemperatureShift)
                    print("a {0:g} b {1:g} ".format(*popt,pcov))                                 
                    plt.plot(cAdd*1e6,funEmploye(cAdd,*popt),next(s))
                plt.xlabel("["+speciesAdd+"](μL/L)",fontsize=self.axissize)
                plt.ylabel("Temperature Shift ($^\circ$C)",fontsize=self.axissize)
                plt.legend(["Data Calculated",'Fiting Curve 1','Fiting Curve 2'],fontsize=self.lgdsize)                
                plt.savefig("DataAnalyse\\Fig\\AdditiveOverall"+speciesAdd+"Methode.png",bbox_inches='tight')
        funEmployeList=[func1,func]
        AnalyseData(funEmployeList)
    def GA_Convergence_Fig(self):
        df=pd.read_csv("DataAnalyse\\OverallForOneT\\Convergence.csv",header=0)
        listTemperature=[1100,1400,1600]
        symbol=[":","-.","--"]
        lgd=[]
        plt.figure()
        for num,temperature in enumerate(listTemperature):
            dfToAnalyse=df[abs(df["temperature"]-temperature)<1e-3]
            iterSteps,errorData=dfToAnalyse["iterSteps"],dfToAnalyse["Error"]
            plt.plot(iterSteps,errorData,symbol[num])
            lgd.append(str(temperature-273.15)+"$^\circ$C")

        
        plt.legend(lgd,fontsize=self.lgdsize)
        plt.xlabel('Step',fontsize=self.axissize)
        plt.ylabel('Relative Error',fontsize=self.axissize)
        #plt.title('Convergence of Genetic Algorithm',fontsize='large')
        plt.savefig("DataAnalyse\\Fig\\GA_Convergence.png",bbox_inches='tight')
        #plt.show()
    def SynGasExp(self):
        plt.figure()
        data={}
        with pd.ExcelFile(r'DataAnalyse\Additive\data2ResultSynGasSNCR2.xlsx') as xls:
            data['df_1_600'] = pd.read_excel(xls, '合成气1,600ppm',usecols=[0, 2])
            data['df_1_1200'] = pd.read_excel(xls, '合成气1,1200ppm',usecols=[0, 2])
            data['CO1H21']=pd.read_excel(xls,'CO1H21',usecols=[0,2])
            data['H21CH41']=pd.read_excel(xls,'H21CH41',usecols=[0,2])
            data['H23CH41']=pd.read_excel(xls,'H23CH41',usecols=[0,2])
        symbol=iter(['--',':','*','^','v'])
        for datatoplot in data:
            plt.plot(data[datatoplot].iloc[:,0],data[datatoplot].iloc[:,1],next(symbol))
        #plt.xlim((550,1100))
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(['Simulation additive#1 600μL/L','Simulation additive#1 1200μL/L',
                    'Experiment CO 300μL/L H2 300μL/L','Experiment H2 300μL/L CH4 300μL/L','Experiment H2 900μL/L CH4 300μL/L'],fontsize=self.lgdsize)
        plt.savefig("DataAnalyse\\Fig\\syngasQing1.png",bbox_inches='tight')
        plt.figure()
        data={}
        with pd.ExcelFile(r'DataAnalyse\Additive\data2ResultSynGasSNCR2.xlsx') as xls:
            data['df_2_600'] = pd.read_excel(xls, '合成气2,600ppm',usecols=[0, 2])
            data['df_2_1200'] = pd.read_excel(xls, '合成气2,1200ppm',usecols=[0, 2])
            data['CO1H21']=pd.read_excel(xls,'CO1H21',usecols=[0,2])
            data['CO3H21']=pd.read_excel(xls,'CO3H21',usecols=[0,2])
            
        symbol=iter(['--',':','*','^','v'])
        for datatoplot in data:
            plt.plot(data[datatoplot].iloc[:,0],data[datatoplot].iloc[:,1],next(symbol))
        #plt.xlim((550,1100))
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.legend(['Simulation additive#2 600μL/L','Simulation additive#2 1200μL/L',
                    'Experiment CO 300μL/L H2 300μL/L','Experiment CO 900μL/L H2 300μL/L'],fontsize=self.lgdsize)
        plt.savefig("DataAnalyse\\Fig\\syngasQing2.png",bbox_inches='tight')

        plt.figure()
        data={}
        with pd.ExcelFile(r'DataAnalyse\Additive\data1ResultSynGasSNCR1.xlsx') as xls:
            #data['exp_1_900'] = pd.read_excel(xls, '合成气1,900ppm ',usecols=[0, 2])
            #data['smlt_1_900']=pd.read_excel(xls, '合成气1,900ppm ',usecols=[3, 5])
            data['exp_1_300'] = pd.read_excel(xls, '合成气1,300ppm',usecols=[0, 2])
            data['smlt_1_300']=pd.read_excel(xls, '合成气1,300ppm',usecols=[4, 6])
            data['exp_1_000'] = pd.read_excel(xls, 'NSR1.5,t0.6s',usecols=[0, 2])
            data['smlt_1_000']=pd.read_excel(xls, 'NSR1.5,t0.6s',usecols=[3, 5])
        
          
        symbol=iter(['s','--','^',':','*','-.'])
        for datatoplot in data:
            plt.plot(data[datatoplot].iloc[:,0],data[datatoplot].iloc[:,1],next(symbol))
        #plt.xlim((550,1100))
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        #'Simulation additive#1 900μL/L','Experiment additive#1 900μL/L',
        plt.legend(['Simulation additive#1 300μL/L','Experiment additive#1 300μL/L',
                    'Simulation additive#1 0μL/L','Experiment additive#1 0μL/L'],fontsize=self.lgdsize)
        plt.savefig("DataAnalyse\\Fig\\syngasYang1.png",bbox_inches='tight')
        data={}
        with pd.ExcelFile(r"DataAnalyse\Additive\data1ResultSynGasSNCR1.xlsx") as xls:
            #data['exp_2_900']=pd.read_excel(xls,'合成气2,900ppm',usecols=[0,2])
            #data['smlt_2_900']=pd.read_excel(xls,'合成气2,900ppm',usecols=[3,5])
            data['exp_2_300']=pd.read_excel(xls,'合成气2,300ppm',usecols=[0,2])
            data['smlt_2_300']=pd.read_excel(xls,'合成气2,300ppm',usecols=[3,5])
            data['exp_1_000'] = pd.read_excel(xls, 'NSR1.5,t0.6s',usecols=[0, 2])
            data['smlt_1_000']=pd.read_excel(xls, 'NSR1.5,t0.6s',usecols=[3, 5])
        
        plt.figure()
        symbol=iter(["*",'--','s',':','^',"-."])
        for key in data:
            plt.plot(data[key].iloc[:,0],data[key].iloc[:,1],next(symbol))
        #plt.xlim((550,1100))
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        #'Simulation additive#2 900μL/L','Experiment additive#2 900μL/L',
        plt.legend(['Simulation additive#2 300μL/L','Experiment additive#2 300μL/L',
                    'Simulation additive#2 0μL/L',  'Experiment additive#2 0μL/L'],fontsize=self.lgdsize)
        plt.savefig("DataAnalyse\\Fig\\syngasYang2.png",bbox_inches='tight')
    def NSRRensidenceTimeExp(self):
        def myplot(name,maxData):
            
            xls_file=pd.read_csv(r'DataAnalyse\\DataNSRResTime\\'+name+r'Exp.csv',header=0)
            plt.plot(xls_file.x,xls_file.Curve1/maxData,'s')
            xls_file=pd.read_csv(r'DataAnalyse\\DataNSRResTime\\'+name+r'Simulation.csv',header=0)
            plt.plot(xls_file.x,xls_file.Curve1/maxData,'--')
            plt.legend(["Experiment Data","Simulation Curve"],fontsize=self.lgdsize)
        plt.figure()    
        myplot("NSR",268)
        plt.xlabel("NSR")
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.savefig("DataAnalyse\\Fig\\NSRExp.png",bbox_inches='tight')
        plt.figure()  
        myplot("residenceTime",100)
        plt.xlabel("Residence Time(s)")
        plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
        plt.savefig("DataAnalyse\\Fig\\residenceTimeExp.png",bbox_inches='tight')      
    def YangMeiGasCorrection(self):
        df=pd.read_csv("DataAnalyse\\YangmeiGas\\simulationData1.csv")        
        NO_EndPoint_Detail_Temp_Np=df['NO_Detail'].values
        temperatureListX=df['temperature'].dropna()
        plt.figure()
        C_NO_Detail=NO_EndPoint_Detail_Temp_Np.reshape(-1,len(temperatureListX))
        symbol3=iter(['--',':','-.'])
        for dataLine in C_NO_Detail:        
            plt.plot(temperatureListX-273.15,dataLine,next(symbol3))
        data={}
        with pd.ExcelFile(r'DataAnalyse\Additive\data1ResultSynGasSNCR1.xlsx') as xls:
            data['exp_1_000'] = pd.read_excel(xls, 'NSR1.5,t0.6s',usecols=[0, 2])
            data['exp_1_300'] = pd.read_excel(xls, '合成气1,300ppm',usecols=[0, 2])
            data['exp_1_900'] = pd.read_excel(xls, '合成气1,900ppm ',usecols=[0, 2])
            #data['smlt_1_900']=pd.read_excel(xls, '合成气1,900ppm ',usecols=[3, 5])
            
            #data['smlt_1_300']=pd.read_excel(xls, '合成气1,300ppm',usecols=[4, 6])
            
            #data['smlt_1_000']=pd.read_excel(xls, 'NSR1.5,t0.6s',usecols=[3, 5])           
            symbol=iter(['s','^','*'])
            for datatoplot in data:
                plt.plot(data[datatoplot].iloc[:,0],data[datatoplot].iloc[:,1],next(symbol))
            #plt.xlim((550,1100))
            plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
            plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
            plt.legend(['Simulation additive#1 0μL/L','Simulation additive#1 300μL/L','Simulation additive#1 900μL/L',
                        'Experiment additive#1 0μL/L','Experiment additive#1 300μL/L','Experiment additive#1 900μL/L'],
                        fontsize=self.lgdsize)
            plt.savefig("DataAnalyse\\Fig\\syngasYang1c.png",bbox_inches='tight')

        df=pd.read_csv("DataAnalyse\\YangmeiGas\\simulationData2.csv")        
        NO_EndPoint_Detail_Temp_Np=df['NO_Detail'].values
        temperatureListX=df['temperature'].dropna()
        plt.figure()
        C_NO_Detail=NO_EndPoint_Detail_Temp_Np.reshape(-1,len(temperatureListX))
        symbol3=iter(['--',':','-.'])
        for dataLine in C_NO_Detail:        
            plt.plot(temperatureListX-273.15,dataLine,next(symbol3),)
        data={}
        with pd.ExcelFile(r"DataAnalyse\Additive\data1ResultSynGasSNCR1.xlsx") as xls:
            data['exp_1_000'] = pd.read_excel(xls, 'NSR1.5,t0.6s',usecols=[0, 2])
            # data['smlt_2_900']=pd.read_excel(xls,'合成气2,900ppm',usecols=[3,5])
            data['exp_2_300']=pd.read_excel(xls,'合成气2,300ppm',usecols=[0,2])
            #data['smlt_2_300']=pd.read_excel(xls,'合成气2,300ppm',usecols=[3,5])            
            #data['smlt_1_000']=pd.read_excel(xls, 'NSR1.5,t0.6s',usecols=[3, 5])  
            data['exp_2_900']=pd.read_excel(xls,'合成气2,900ppm',usecols=[0,2])  
            symbol=iter(["*",'s','^'])
            for key in data:
                plt.plot(data[key].iloc[:,0],data[key].iloc[:,1],next(symbol))
            #plt.xlim((550,1100))
            plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
            plt.ylabel('[NO](out)/[NO](in)',fontsize=self.axissize)
            plt.legend(['Simulation additive#2 0μL/L','Simulation additive#2 300μL/L','Simulation additive#2 900μL/L',
                        'Experiment additive#2 0μL/L','Experiment additive#2 300μL/L','Experiment additive#2 900μL/L'],fontsize=self.lgdsize)
            plt.savefig("DataAnalyse\\Fig\\syngasYang2c.png",bbox_inches='tight')   

    def temperatureIntervalTestPaperCoef(self):
        df1=pd.read_csv("DataAnalyse\OverallReactionForAllT\ResultOverallCompareForAllTemperatureNewData.csv")     
        temperature=df1['temperature'].dropna()-273
        timeList=df1['Time'].dropna()
        C_NO_Detail=df1['NO_Detail'].values.reshape(len(temperature),len(timeList))
        C_NH3_Detail=df1['NH3_Detail'].values.reshape(len(temperature),len(timeList))
        C_NO_Overall=df1.NO_Overall.values.reshape(len(temperature),len(timeList))
        C_NH3_Overall=df1.NH3_Overall.values.reshape(len(temperature),len(timeList))
        plt.figure()
        plt.plot(temperature,C_NO_Detail[:,-1]/C_NO_Detail[0],'--',temperature,C_NO_Overall[:,-1]/C_NO_Detail[0],'*')
        plt.plot(temperature,C_NO_Detail[:,-10]/C_NO_Detail[0],'-.',temperature,C_NO_Overall[:,-10]/C_NO_Detail[0],'^')
        plt.plot(temperature,C_NO_Detail[:,-15]/C_NO_Detail[0],':',temperature,C_NO_Overall[:,-15]/C_NO_Detail[0],'v')
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel("[NO](in)/[NO](out)",fontsize=self.axissize)
        plt.legend(["NO:Detail Reaction 0.6s","NO:Overall Reaction 0.6s",
                    "NO:Detail Reaction 0.3s","NO:Overall Reaction 0.3s",
                    "NO:Detail Reaction 0.15s","NO:Overall Reaction 0.15s",],fontsize=self.lgdsize)
        plt.savefig("DataAnalyse\\Fig\\temperatureIntervalNONew.png",bbox_inches='tight') 
        #plt.show()
        plt.close()
        plt.figure()
        plt.plot(temperature,C_NH3_Detail[:,-1]/C_NH3_Detail[0],'--',temperature,C_NH3_Overall[:,-1]/C_NH3_Detail[0],'*')
        plt.plot(temperature,C_NH3_Detail[:,-10]/C_NH3_Detail[0],'-.',temperature,C_NH3_Overall[:,-10]/C_NH3_Detail[0],'^')
        plt.plot(temperature,C_NH3_Detail[:,-15]/C_NH3_Detail[0],':',temperature,C_NH3_Overall[:,-15]/C_NH3_Detail[0],'v')
        plt.xlabel('Temperature ($^\circ$C)',fontsize=self.axissize)
        plt.ylabel("[NH3](in)/[NH3](out)",fontsize=self.axissize)
        plt.legend(["NH3:Detail Reaction 0.6s","NH3:Overall Reaction 0.6s",
                    "NH3:Detail Reaction 0.3s","NH3:Overall Reaction 0.3s",
                    "NH3:Detail Reaction 0.15s","NH3:Overall Reaction 0.15s",],fontsize=self.lgdsize)    
        plt.savefig("DataAnalyse\\Fig\\temperatureIntervalNH3New.png",bbox_inches='tight') 
        #plt.show()    
    



if __name__=='__main__':
    figPlotter=plotData('large')
    
    '''
    figPlotter.verifyCaoQingXi()
    
   
    figPlotter.CH4_Fig()
    figPlotter.CO_Fig()
    figPlotter.H2_Fig()
    figPlotter.H2O_Fig()
    figPlotter.NO_NSR15_Fig()
    figPlotter.NSR_Fig()
    figPlotter.O2_Fig()
    figPlotter.pressure_Fig()
    figPlotter.pressure_NO2_Fig()
    figPlotter.Residtime_Fig()
    
    figPlotter.Additive_NSR0()    
    figPlotter.Additive_NSR_different()
    figPlotter.onlyAdditive()
    figPlotter.SNCR_AdditiveDetail()

    figPlotter.GA_Convergence_Fig()
    figPlotter.specificTemperatureFig()
    
    figPlotter.Additive_Overall_Fig()
    figPlotter.AdditiveTemperatureShift()
   
    figPlotter.SynGasExp()
 
    figPlotter.NSRRensidenceTimeExp()
    figPlotter.YangMeiGasCorrection()
    
    figPlotter.temperatureIntervalTestPaperCoef()
    '''
    figPlotter.temperatureInterval()
    
    
    
    
