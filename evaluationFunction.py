import Python_Chemkin_ToolBox as PyChemTB
import os
import subprocess
import shutil
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import csv
import time


currentDir = os.path.dirname(__file__)
tempDir = os.path.join(currentDir, 'tempDeNOx')
ImageResult=os.path.join(currentDir, 'ImageResult')

if os.path.exists(tempDir):
    shutil.rmtree(tempDir)

os.makedirs(tempDir)

def clearDir(pathToClear):
    fileList=os.listdir(pathToClear)
    for fileToClear in fileList:
        abslouteFilePath=os.path.join(pathToClear,fileToClear)
        if os.path.isdir(abslouteFilePath):
            clearDir(abslouteFilePath)
        else:
            os.remove(abslouteFilePath)



def getMolesFractions(machanismInp,expParameterInp):
    if os.path.exists(tempDir):
        clearDir(tempDir)
    else:
        os.makedirs(tempDir)
    PyChemTB.generateBatFile(machanismInp,expParameterInp,tempDir,"DeNOxExp.bat")
    process=subprocess.Popen(os.path.join(tempDir,"DeNOxExp.bat"), cwd=tempDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(stdout)
        print(stderr)
        quit()
    if os.path.exists(os.path.join(tempDir,"CKSoln_solution_no_1.csv")):
        resultFileChemkin=os.path.join(tempDir,"CKSoln_solution_no_1.csv")
    if os.path.exists(os.path.join(tempDir,"CKSoln_solution_no_1_1.csv")):
        resultFileChemkin=os.path.join(tempDir,"CKSoln_solution_no_1_1.csv")
    fraction_NO,fraction_NH3,residentTime=PyChemTB.postProcess(resultFile=resultFileChemkin)
    return fraction_NO,fraction_NH3,residentTime

###########################################
##        research on residence time     ##
###########################################

class sncr4AllResidenceCalculator:
    def __init__(self,temperatureX):
        self.temperatureValue=temperatureX      
        PyChemTB.gererateInputFile(         reactants=[#('CH4',0),
                                                        #('CO',0.0),
                                                        #('CO2',0.15),
                                                        #('H2',0.2),
                                                        ('N2',0.7895),
                                                        ('NH3',0.0003),
                                                        ('NO',0.0002),
                                                        ('O2',0.06),
                                                        ('CO2',0.15)],     # Reactant (mole fraction)

                                            temperature = temperatureX, # Temperature(K)
                                            pressure = 1 ,   # Pressure (bar)
                                            velocity=75.0,
                                            viscosity=0.0,
                                            reactorDiameter=3.2,
                                            endPosition=45.0,
                                            startPosition=0.0 ,
                                            endTime = 0.05 ,   # End Time (sec)
                                            tempFile="testForResiTime.inp")

        fraction_NO_Detail_Reaction,fraction_NH3_Detail_Reaction,residentTimeDetail=getMolesFractions(
                                                        os.path.join(currentDir,"chem_add_ITL.inp"),
                                                            os.path.join(currentDir, "testForResiTime.inp"))

        f_NO_Detail=interp1d(residentTimeDetail.values,fraction_NO_Detail_Reaction.values,kind='linear',fill_value="extrapolate")	
        f_NH3_Detail=interp1d(residentTimeDetail.values,fraction_NH3_Detail_Reaction.values,kind='linear',fill_value="extrapolate")			
        self.comparationListTime = np.linspace(residentTimeDetail.values[0],residentTimeDetail.values[-1],num=20,endpoint=True )
        self.comparationList_NO_Detail = f_NO_Detail(self.comparationListTime)
        self.comparationList_NH3_Detail = f_NH3_Detail(self.comparationListTime)									
													
    def difference_Overall_Detail(self,Coefficient,draw=False):

        PyChemTB.generateChemInput(Coefficient[0],Coefficient[1],Coefficient[2],
                                    Coefficient[3],Coefficient[4],Coefficient[5],
                                    tempFile=os.path.join(currentDir,"ChemInput_OverallReaction.inp"))

        
        fraction_NO_Overall_Reaction,fraction_NH3_Overall_Reaction,residentTimeOverall=getMolesFractions(
                                                        #"G:\SNCR\SNCR\chem_add_ITL.inp",
                                                        os.path.join(currentDir,"ChemInput_OverallReaction.inp"),
                                                        os.path.join(currentDir, "testForResiTime.inp"))
        # print(fraction_NO_Overall_Reaction.ilpoc[])

        
        
        f_NO_Overall=interp1d(residentTimeOverall.values,fraction_NO_Overall_Reaction.values,kind='linear',fill_value="extrapolate")
        f_NH3_Overall=interp1d(residentTimeOverall.values,fraction_NH3_Overall_Reaction.values,kind='linear',fill_value="extrapolate")

        
        self.comparationList_NO_Overall = f_NO_Overall(self.comparationListTime)
        self.comparationList_NH3_Overall = f_NH3_Overall(self.comparationListTime)

        self.diff2_NO = ((self.comparationList_NO_Detail-self.comparationList_NO_Overall)/fraction_NO_Overall_Reaction[0])**2
        self.diff2_NH3 = ((self.comparationList_NH3_Detail-self.comparationList_NH3_Overall)/fraction_NH3_Overall_Reaction[0])**2

        if(draw):
            currentTime = time.strftime("%Y%m%d_%H%M%S")
            plt.figure()
            pic01=plt.plot(self.comparationListTime,self.comparationList_NO_Overall/self.comparationList_NO_Overall[0],'^',
                    self.comparationListTime,self.comparationList_NO_Detail/self.comparationList_NO_Detail[0],'-.',
                    self.comparationListTime,self.comparationList_NH3_Overall/self.comparationList_NH3_Overall[0],'v',
                    self.comparationListTime,self.comparationList_NH3_Detail/self.comparationList_NH3_Detail[0],'--',
                    )
            
            plt.xlabel('ResidentTime',fontsize='large')
            plt.ylabel('Fraction out/ Fraction in',fontsize='large')
            plt.title("De NOx Result with Temperature {0:.2f}K".format(self.temperatureValue))
            plt.legend(["NO: Overall Reaction","NO: Detail Reaction",
            "NH3: Overall Reaction","NH3: Detail Reaction"])
            plt.subplots_adjust(left=0.18, wspace=0.25, hspace=0.25,
                    bottom=0.13, top=0.91)
            plt.savefig(os.path.join(ImageResult,currentTime+'NH3NO.png'))

            plt.figure()
            pic02=plt.plot(self.comparationListTime,self.diff2_NO,'--',
                    self.comparationListTime,self.diff2_NH3,'-.',
                    #residentTimeOverall,fraction_NH3_Overall_Reaction,'v',
                    #residentTimeDetail,fraction_NH3_Detail_Reaction,'^',
                    )
            plt.xlabel('ResidentTime',fontsize='large')
            plt.ylabel('Fraction out/ Fraction in',fontsize='large')
            plt.title("Errors with Temperature {0:.2f}K".format(self.temperatureValue))
            plt.legend(["NO Errors between Overall Reaction Detail Reaction",
            "NH3 Errors between Overall Reaction Detail Reaction"])
            plt.subplots_adjust(left=0.18, wspace=0.25, hspace=0.25,
                    bottom=0.13, top=0.91)
            plt.savefig(os.path.join(ImageResult,currentTime+'Err.png')) 
            
        return (2*self.diff2_NO.mean()+self.diff2_NH3.mean())/3

###################################################
##               For different temperature       ##
###################################################
	

class temperatureListDiffCalculator: 

    def __init__(self,temperatureListX):
        self.temperatureListX=temperatureListX
        self.NH3_AllPoint_Detail_Temp_cmprList=[]
        self.NO_AllPoint_Detail_Temp_cmprList=[]         
        self.NH3_AllPoint_Overall_Temp_cmprList=[]
        self.NO_AllPoint_Overall_Temp_cmprList=[]

        self.NH3_EndPoint_Detail_Temp=[]
        self.NO_EndPoint_Detail_Temp=[]
        self.NH3_EndPoint_Overall=[]
        self.NO_EndPoint_Overall=[] 

        self.resultWithDetailReaction()
        
    def resultWithDetailReaction(self):
        self.NH3_AllPoint_Detail_Temp_cmprList=[]
        self.NO_AllPoint_Detail_Temp_cmprList=[]
        self.NH3_EndPoint_Detail_Temp=[]
        self.NO_EndPoint_Detail_Temp=[]
        
        
        for temperatureIter in self.temperatureListX:
            PyChemTB.gererateInputFile(        reactants=[#('CH4',0),
                                                    #('CO',0.0),
                                                    #('CO2',0.15),
                                                    #('H2',0.2),
                                                    ('N2',0.7895),
                                                    ('NH3',0.0003),
                                                    ('NO',0.0002),
                                                    ('O2',0.06),
                                                    ('CO2',0.15)],     # Reactant (mole fraction)

                                        temperature = temperatureIter, # Temperature(K)
                                        pressure = 1 ,   # Pressure (bar)
                                        velocity=75.0,
                                        viscosity=0.0,
                                        reactorDiameter=3.2,
                                        endPosition=45.0,
                                        startPosition=0.0 ,
                                        endTime = 0.05 ,   # End Time (sec)
                                        tempFile="test.inp")                  

            
            fraction_NO_Detail_Reaction_Temp,fraction_NH3_Detail_Reaction_Temp,residentTimeDetail_Temp=getMolesFractions(
                                                    os.path.join(currentDir,"chem_add_ITL.inp"),
                                                        os.path.join(currentDir, "test.inp"))

            f_NO_Detail=interp1d(residentTimeDetail_Temp.values,fraction_NO_Detail_Reaction_Temp.values,kind='linear',fill_value="extrapolate")	
            f_NH3_Detail=interp1d(residentTimeDetail_Temp.values,fraction_NH3_Detail_Reaction_Temp.values,kind='linear',fill_value="extrapolate")			
            self.comparationListTime = np.linspace(residentTimeDetail_Temp.values[0],residentTimeDetail_Temp.values[-1],num=20,endpoint=True )
            comparationList_NO_Detail_1T = f_NO_Detail(self.comparationListTime)
            comparationList_NH3_Detail_1T = f_NH3_Detail(self.comparationListTime)	
            
            self.NH3_AllPoint_Detail_Temp_cmprList=np.hstack((self.NH3_AllPoint_Detail_Temp_cmprList,comparationList_NH3_Detail_1T))           
            self.NO_AllPoint_Detail_Temp_cmprList=np.hstack((self.NO_AllPoint_Detail_Temp_cmprList,comparationList_NO_Detail_1T))  	
            self.NH3_EndPoint_Detail_Temp.append(fraction_NH3_Detail_Reaction_Temp.iloc[-1])
            self.NO_EndPoint_Detail_Temp.append(fraction_NO_Detail_Reaction_Temp.iloc[-1])
	
    def difference_Overall_Detail_temperature(self,Coeficients,draw=False):
        self.NH3_EndPoint_Overall=[]
        self.NO_EndPoint_Overall=[]  
        self.NH3_AllPoint_Overall_Temp_cmprList=[]
        self.NO_AllPoint_Overall_Temp_cmprList=[]             
    
        for temperatureIter in self.temperatureListX:
            PyChemTB.gererateInputFile(        reactants=[#('CH4',0),
                                                    #('CO',0.0),
                                                    #('CO2',0.15),
                                                    #('H2',0.2),
                                                    ('N2',0.7895),
                                                    ('NH3',0.0003),
                                                    ('NO',0.0002),
                                                    ('O2',0.06),
                                                    ('CO2',0.15)],     # Reactant (mole fraction)

                                        temperature = temperatureIter, # Temperature(K)
                                        pressure = 1 ,   # Pressure (bar)
                                        velocity=75.0,
                                        viscosity=0.0,
                                        reactorDiameter=3.2,
                                        endPosition=45.0,
                                        startPosition=0.0 ,
                                        endTime = 0.05 ,   # End Time (sec)
                                        tempFile="test.inp")
                        

            PyChemTB.generateChemInput(#1.49e19,0,3.6e5,1.2e15,0,3.4e5,
                                Coeficients[0],Coeficients[1],Coeficients[2],Coeficients[3],Coeficients[4],Coeficients[5],
                                tempFile=os.path.join(currentDir,"ChemInput_OverallReaction.inp"))
            
            fraction_NO_Overall_Reaction,fraction_NH3_Overall_Reaction,residentTimeOverall=getMolesFractions(
                                                        #"G:\SNCR\SNCR\chem_add_ITL.inp",
                                                        os.path.join(currentDir,"ChemInput_OverallReaction.inp"),
                                                        os.path.join(currentDir, "test.inp"))
        

            
            f_NO_Overall=interp1d(residentTimeOverall.values,fraction_NO_Overall_Reaction.values,kind='linear',fill_value="extrapolate")	
            f_NH3_Overall=interp1d(residentTimeOverall.values,fraction_NH3_Overall_Reaction.values,kind='linear',fill_value="extrapolate")			
            
            comparationList_NO_Overall_1T = f_NO_Overall(self.comparationListTime)
            comparationList_NH3_Overall_1T = f_NH3_Overall(self.comparationListTime)	
            
            self.NH3_AllPoint_Overall_Temp_cmprList=np.hstack((self.NH3_AllPoint_Overall_Temp_cmprList,comparationList_NH3_Overall_1T))           
            self.NO_AllPoint_Overall_Temp_cmprList=np.hstack((self.NO_AllPoint_Overall_Temp_cmprList,comparationList_NO_Overall_1T))  	
	

            self.NH3_EndPoint_Overall.append(fraction_NH3_Overall_Reaction.iloc[-1])        
            self.NO_EndPoint_Overall.append(fraction_NO_Overall_Reaction.iloc[-1])
        '''
        print("NH3 Detail: {} \n".format(self.NH3_AllPoint_Detail_Temp_cmprList))    
        print("NH3 Overal: {} \n".format(self.NH3_AllPoint_Overall_Temp_cmprList))
        print("NO Detail: {} \n".format(self.NO_AllPoint_Detail_Temp_cmprList))    
        print("NO Overal: {} \n".format(self.NO_AllPoint_Overall_Temp_cmprList))
        print("Temperature list：{} \n".format(self.temperatureListX))
        '''
        diff_NH3=((self.NH3_AllPoint_Detail_Temp_cmprList-self.NH3_AllPoint_Overall_Temp_cmprList)/fraction_NH3_Overall_Reaction.iloc[0])**2
        diff_NO=((self.NO_AllPoint_Detail_Temp_cmprList-self.NO_AllPoint_Overall_Temp_cmprList)/fraction_NO_Overall_Reaction.iloc[0])**2
        if(draw):
            currentTime = time.strftime("%Y%m%d_%H%M%S")
            
            plt.figure()
            plt.plot(self.temperatureListX,self.NH3_EndPoint_Detail_Temp/fraction_NH3_Overall_Reaction.iloc[0],'--',self.temperatureListX,self.NH3_EndPoint_Overall/fraction_NH3_Overall_Reaction.iloc[0],'^')
            plt.xlabel('Temperature',fontsize='large')
            plt.ylabel('Fraction out/ Fraction in',fontsize='large')
            plt.title("Concentration of NH3 at Endpoint of Reactor",fontsize='large')
            plt.legend(["NH3: Detail Reaction","NH3: Overall Reaction"],fontsize='large')
            plt.subplots_adjust(left=0.18, wspace=0.25, hspace=0.25,
                    bottom=0.13, top=0.91)
            plt.savefig(os.path.join(ImageResult,currentTime+'NH3EndPoint.png'))
            plt.figure()
            plt.plot(self.temperatureListX,self.NO_EndPoint_Detail_Temp/fraction_NO_Overall_Reaction.iloc[0],'-.',self.temperatureListX,self.NO_EndPoint_Overall/fraction_NO_Overall_Reaction.iloc[0],'v')
            plt.xlabel('Temperature',fontsize='large')
            plt.ylabel('Fraction out/ Fraction in',fontsize='large')
            plt.title("Concentration of NO at Endpoint of Reactor",fontsize='large')
            plt.legend(["NO: Detail Reaction","NO: Overall Reaction"],fontsize='large')
            plt.subplots_adjust(left=0.18, wspace=0.25, hspace=0.25,
                    bottom=0.13, top=0.91)
            plt.savefig(os.path.join(ImageResult,currentTime+'NOEndPoint.png'))
        return (diff_NH3.mean()+2*diff_NO.mean())/3

###########################################
##         Test the function             ##
###########################################


if __name__=='__main__':
    '''
    #Coeficients=[1e15,0,3e4,1e15,0,3e4]   
    with open('lastBestResult.csv','r') as f:
        reader=csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)    
        for row in reader:
            if len(row)==10:
                temperature2Test=row[1]
                Coeficients=row[3:9]
                calculatorForResTime=sncr4AllResidenceCalculator(temperatureX=temperature2Test)
                val_diff=calculatorForResTime.difference_Overall_Detail(Coefficient=Coeficients,draw=True)
                print(temperature2Test,Coeficients,val_diff,row[9])
    # calculate the result for different operating condition
    '''
    listTemperature=np.linspace(500,1600,20)
    '''
    Coeficients=[40609356.32837867,4.591567103723157,59293.190204797174,
            1.2500592750801196e+48,0.2384295271582183,227638.0184552551]
    '''
    Coeficients=[[40609356.32837867,4.591567103723157,59293.190204797174,
            1.2500592750801196e+48,0.2384295271582183,227638.0184552551],
            [2.1489719679116273,3.6556482376087636,14.912031071151327,
                10.977243831448774,3.883371131587305,26418.321246185045]]
    calculatorTemperature=temperatureListDiffCalculator(listTemperature)
    for coeficient in Coeficients:
        result=calculatorTemperature.difference_Overall_Detail_temperature(coeficient,draw=True)
        print(result)
    
  