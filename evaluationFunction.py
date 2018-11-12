import Python_Chemkin_ToolBox as PyChemTB
import os
import subprocess
import shutil
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

currentDir = os.path.dirname(__file__)
tempDir = os.path.join(currentDir, 'tempDeNOx')


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
            plt.figure(1)
            pic01=plt.plot(self.comparationListTime,self.comparationList_NO_Overall/self.comparationList_NO_Overall[0],'^',
                    self.comparationListTime,self.comparationList_NO_Detail/self.comparationList_NO_Detail[0],'-.',
                    self.comparationListTime,self.comparationList_NH3_Overall/self.comparationList_NH3_Overall[0],'v',
                    self.comparationListTime,self.comparationList_NH3_Detail/self.comparationList_NH3_Detail[0],'--',
                    )
            plt.savefig('1.png') 
            plt.figure(2)
            pic02=plt.plot(self.comparationListTime,self.diff2_NO,'--',
                    self.comparationListTime,self.diff2_NH3,'-.',
                    #residentTimeOverall,fraction_NH3_Overall_Reaction,'v',
                    #residentTimeDetail,fraction_NH3_Detail_Reaction,'^',
                    )
            plt.xlabel('ResidentTime',fontsize='large')
            plt.ylabel('Fraction out/ Fraction in',fontsize='large')
            plt.savefig('2.png') 
            plt.show()
        return (2*self.diff2_NO.mean()+self.diff2_NH3.mean())/3

###################################################
##               For different temperature       ##
###################################################
	

class temperatureListDiffCalculator: 

    def __init__(self,temperatureListX):
        self.temperatureListX=temperatureListX
        self.NH3_EndPoint_Detail_Temp=[]
        self.NO_EndPoint_Detail_Temp=[]
        self.NH3_EndPoint_Overall=[]
        self.NO_EndPoint_Overall=[]   
        self.resultWithDetailReaction()
        
    def resultWithDetailReaction(self):
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
            
            self.NH3_EndPoint_Detail_Temp.append(fraction_NH3_Detail_Reaction_Temp.iloc[-1])
            
            self.NO_EndPoint_Detail_Temp.append(fraction_NO_Detail_Reaction_Temp.iloc[-1])       	
	
	
    def difference_Overall_Detail_temperature(self,Coeficients,draw=False):
        self.NH3_EndPoint_Overall=[]
        self.NO_EndPoint_Overall=[]               
    
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
        
            self.NH3_EndPoint_Overall.append(fraction_NH3_Overall_Reaction.iloc[-1])        
            self.NO_EndPoint_Overall.append(fraction_NO_Overall_Reaction.iloc[-1])

            
        diff_NH3=((np.array(self.NH3_EndPoint_Detail_Temp)-np.array(self.NH3_EndPoint_Overall))/fraction_NH3_Overall_Reaction.iloc[0])**2
        diff_NO=((np.array(self.NO_EndPoint_Detail_Temp)-np.array(self.NO_EndPoint_Overall))/fraction_NO_Overall_Reaction.iloc[0])**2
        if(draw):
            plt.figure(1)
            plt.plot(self.temperatureListX,self.NH3_EndPoint_Detail_Temp,'--',self.temperatureListX,self.NH3_EndPoint_Overall,'^')
            plt.savefig('NH3.png')
            plt.figure(2)
            plt.plot(self.temperatureListX,self.NO_EndPoint_Detail_Temp,'-.',self.temperatureListX,self.NO_EndPoint_Overall,'v')
            plt.savefig("NO.png")
        return (diff_NH3.mean()+2*diff_NO.mean())/3

###########################################
##         Test the function             ##
###########################################


if __name__=='__main__':
    #Coeficients=[1e15,0,3e4,1e15,0,3e4]
    Coeficients=[3498.5172111780353, 5.5169879733298846, 51812.46347905936,
     7.107369586702694e+19, 6.111647708933334, 170713.70515855757]

    calculatorForResTime=sncr4AllResidenceCalculator(temperatureX=1200)
    val_diff=calculatorForResTime.difference_Overall_Detail(Coefficient=Coeficients,draw=True)
    print(val_diff)
    # calculate the result for different operating condition
    '''
    listTemperature=np.linspace(500,1800,13)
    calculatorTemperature=temperatureListDiffCalculator(listTemperature)
    result=calculatorTemperature.difference_Overall_Detail_temperature(Coeficients,draw=True)
    print(result)
    '''
  