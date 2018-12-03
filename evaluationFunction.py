import Python_Chemkin_ToolBox as PyChemTB
import os
import subprocess
import shutil
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import csv
import time
import pandas as pd


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
        self.timeListNumber=20
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
            self.comparationListTime = np.linspace(residentTimeDetail_Temp.values[0],residentTimeDetail_Temp.values[-1],num=self.timeListNumber,endpoint=True )
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
            plt.xlabel('Temperature/K',fontsize='large')
            plt.ylabel('Fraction out/ Fraction in',fontsize='large')
            plt.title("Concentration of NH3 at Endpoint of Reactor",fontsize='large')
            plt.legend(["NH3: Detail Reaction","NH3: Overall Reaction"],fontsize='large')
            plt.subplots_adjust(left=0.18, wspace=0.25, hspace=0.25,
                    bottom=0.13, top=0.91)
            plt.savefig(os.path.join(ImageResult,currentTime+'NH3EndPoint.png'))
            plt.figure()
            plt.plot(self.temperatureListX,self.NO_EndPoint_Detail_Temp/fraction_NO_Overall_Reaction.iloc[0],'-.',self.temperatureListX,self.NO_EndPoint_Overall/fraction_NO_Overall_Reaction.iloc[0],'v')
            plt.xlabel('Temperature/K',fontsize='large')
            plt.ylabel('Fraction out/ Fraction in',fontsize='large')
            plt.title("Concentration of NO at Endpoint of Reactor",fontsize='large')
            plt.legend(["NO: Detail Reaction","NO: Overall Reaction"],fontsize='large')
            plt.subplots_adjust(left=0.18, wspace=0.25, hspace=0.25,
                    bottom=0.13, top=0.91)
            plt.savefig(os.path.join(ImageResult,currentTime+'NOEndPoint.png'))
            #----------3D Plot---------------#
            fig = plt.figure()
            ax3d = Axes3D(fig)

            C_NO_Detail=self.NO_AllPoint_Detail_Temp_cmprList.reshape(-1,self.timeListNumber)/fraction_NO_Overall_Reaction.iloc[0]
            time3DIndex,temperature3DIndex=np.meshgrid(self.comparationListTime,self.temperatureListX)
            ax3d.plot_surface(time3DIndex,temperature3DIndex, C_NO_Detail, rstride=1, cstride=1, cmap=plt.cm.spring,alpha=0.8)

            C_NO_Overall=self.NO_AllPoint_Overall_Temp_cmprList.reshape(-1,self.timeListNumber)/fraction_NO_Overall_Reaction.iloc[0]
            
            ax3d.scatter( time3DIndex,temperature3DIndex, C_NO_Overall, c='b',marker='*')            
            ax3d.set_xlabel('Residence Time/s')
            ax3d.set_ylabel('Temperature/K')
            ax3d.set_zlabel('NO out/NO in') 
            plt.show()

            fig = plt.figure()
            ax3d = Axes3D(fig)
            C_NH3_Detail=self.NH3_AllPoint_Detail_Temp_cmprList.reshape(-1,self.timeListNumber)/fraction_NH3_Overall_Reaction.iloc[0]
            time3DIndex,temperature3DIndex=np.meshgrid(self.comparationListTime,self.temperatureListX)
            ax3d.plot_surface(time3DIndex,temperature3DIndex, C_NH3_Detail, rstride=1, cstride=1, cmap=plt.cm.spring,alpha=0.8)

            C_NH3_Overall=self.NH3_AllPoint_Overall_Temp_cmprList.reshape(-1,self.timeListNumber)/fraction_NH3_Overall_Reaction.iloc[0]
            
            ax3d.scatter( time3DIndex,temperature3DIndex, C_NH3_Overall, c='b',marker='*')            
            ax3d.set_xlabel('Residence Time/s')
            ax3d.set_ylabel('Temperature/K')
            ax3d.set_zlabel('NH3 out/NH3 in') 
            plt.show()


            
        return (diff_NH3.mean()+2*diff_NO.mean())/3

###################################################
##               with the additive               ##
###################################################

class Additive_Optimazition:    

    def __init__(self,temperatureListX,speciesAdd,ListAdd):
        self.temperatureListX=temperatureListX
        self.speciesAdd=speciesAdd
        self.listAdd=ListAdd        
        self.NH3_AllPoint_Detail_Temp_cmprList=[]
        self.NO_AllPoint_Detail_Temp_cmprList=[]         
        self.NH3_AllPoint_Overall_Temp_cmprList=[]
        self.NO_AllPoint_Overall_Temp_cmprList=[]
        self.timeListNumber=20
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
        
        for IterAddConctrt in self.listAdd:            
            for temperatureIter in self.temperatureListX:
                PyChemTB.gererateInputFile( reactants=[('N2',0.7895-IterAddConctrt),(self.speciesAdd,IterAddConctrt),
                                            ('NH3',0.0003),
                                            ('NO',0.0002),('O2',0.06),('CO2',0.15)],     # Reactant (mole fraction)

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
                self.comparationListTime = np.linspace(residentTimeDetail_Temp.values[0],residentTimeDetail_Temp.values[-1],num=self.timeListNumber,endpoint=True )
                comparationList_NO_Detail_1T = f_NO_Detail(self.comparationListTime)
                comparationList_NH3_Detail_1T = f_NH3_Detail(self.comparationListTime)	
                
                self.NH3_AllPoint_Detail_Temp_cmprList=np.hstack((self.NH3_AllPoint_Detail_Temp_cmprList,comparationList_NH3_Detail_1T))           
                self.NO_AllPoint_Detail_Temp_cmprList=np.hstack((self.NO_AllPoint_Detail_Temp_cmprList,comparationList_NO_Detail_1T))  	
                self.NH3_EndPoint_Detail_Temp.append(fraction_NH3_Detail_Reaction_Temp.iloc[-1])
                self.NO_EndPoint_Detail_Temp.append(fraction_NO_Detail_Reaction_Temp.iloc[-1])
        
    def difference_Overall_Detail_temperature(self,CoeficientsForM,draw=False):
        self.NH3_EndPoint_Overall=[]
        self.NO_EndPoint_Overall=[]  
        self.NH3_AllPoint_Overall_Temp_cmprList=[]
        self.NO_AllPoint_Overall_Temp_cmprList=[]             
    

        for IterAddConctrt in self.listAdd:
            for temperatureIter in self.temperatureListX:
                PyChemTB.gererateInputFile( reactants=[('N2',0.7895-IterAddConctrt),(self.speciesAdd,IterAddConctrt),
                                            ('NH3',0.0003),
                                            ('NO',0.0002),('O2',0.06),('CO2',0.15)],     # Reactant (mole fraction)

                                            temperature = temperatureIter, # Temperature(K)
                                            pressure = 1 ,   # Pressure (bar)
                                            velocity=75.0,
                                            viscosity=0.0,
                                            reactorDiameter=3.2,
                                            endPosition=45.0,
                                            startPosition=0.0 ,
                                            endTime = 0.05 ,   # End Time (sec)
                                            tempFile="test.inp")                     

                if  temperatureIter<1200:
                    Coeficients=[40609356.32837867,4.591567103723157,59293.190204797174,
                                1.2500592750801196e+48,0.2384295271582183,227638.0184552551]
                if  temperatureIter>=1200:
                    Coeficients=[2.1489719679116273,3.6556482376087636,14.912031071151327,
                                10.977243831448774,3.883371131587305,26418.321246185045]
                
                PyChemTB.generateChemInput(#1.49e19,0,3.6e5,1.2e15,0,3.4e5,
                        Coeficients[0],Coeficients[1],Coeficients[2],Coeficients[3],Coeficients[4],Coeficients[5],
                        tempFile=os.path.join(currentDir,"ChemInput_OverallReaction.inp"),
                        withAdditive=True,speciesAdd=self.speciesAdd,enhenceFactor=CoeficientsForM)

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
            plt.xlabel('Temperature/K',fontsize='large')
            plt.ylabel('Fraction out/ Fraction in',fontsize='large')
            plt.title("Concentration of NH3 at Endpoint of Reactor",fontsize='large')
            plt.legend(["NH3: Detail Reaction","NH3: Overall Reaction"],fontsize='large')
            plt.subplots_adjust(left=0.18, wspace=0.25, hspace=0.25,
                    bottom=0.13, top=0.91)
            plt.savefig(os.path.join(ImageResult,currentTime+'NH3EndPoint.png'))
            plt.figure()
            plt.plot(self.temperatureListX,self.NO_EndPoint_Detail_Temp/fraction_NO_Overall_Reaction.iloc[0],'-.',self.temperatureListX,self.NO_EndPoint_Overall/fraction_NO_Overall_Reaction.iloc[0],'v')
            plt.xlabel('Temperature/K',fontsize='large')
            plt.ylabel('Fraction out/ Fraction in',fontsize='large')
            plt.title("Concentration of NO at Endpoint of Reactor",fontsize='large')
            plt.legend(["NO: Detail Reaction","NO: Overall Reaction"],fontsize='large')
            plt.subplots_adjust(left=0.18, wspace=0.25, hspace=0.25,
                    bottom=0.13, top=0.91)
            plt.savefig(os.path.join(ImageResult,currentTime+'NOEndPoint.png'))
           

            
        return (diff_NH3.mean()+2*diff_NO.mean())/3

###################################################
##         For the additive methode Classic      ##
###################################################

class Additive_Analyse:    

    def __init__(self,temperatureListX,speciesAdd,ListAdd):
        self.temperatureListX=temperatureListX
        self.speciesAdd=speciesAdd
        self.listAdd=ListAdd     
        self.NH3_EndPoint_Detail_Temp=[]
        self.NO_EndPoint_Detail_Temp=[]
        self.NH3_EndPoint_Overall=[]
        self.NO_EndPoint_Overall=[] 

        self.resultWithDetailReaction()
        
    def resultWithDetailReaction(self):
        
        self.NH3_EndPoint_Detail_Temp=[]
        self.NO_EndPoint_Detail_Temp=[]
        
        for IterAddConctrt in self.listAdd:            
            for temperatureIter in self.temperatureListX:
                PyChemTB.gererateInputFile( reactants=[('N2',0.7895-IterAddConctrt),(self.speciesAdd,IterAddConctrt),
                                            ('NH3',0.0003),
                                            ('NO',0.0002),('O2',0.06),('CO2',0.15)],     # Reactant (mole fraction)

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
                
                
                self.NH3_EndPoint_Detail_Temp.append(fraction_NH3_Detail_Reaction_Temp.iloc[-1]/fraction_NH3_Detail_Reaction_Temp.iloc[0])
                self.NO_EndPoint_Detail_Temp.append(fraction_NO_Detail_Reaction_Temp.iloc[-1]/fraction_NO_Detail_Reaction_Temp.iloc[0])
                with open(self.speciesAdd+"logFile.txt",'a+') as stream:
                    stream.write("Additive:{0:g} ,temperture:{1:g} | Fraction EndPoint {2:g}  Fraction StartPoint {3:g}  \n".format(
                               IterAddConctrt,temperatureIter, fraction_NO_Detail_Reaction_Temp.iloc[-1],fraction_NO_Detail_Reaction_Temp.iloc[0]))
        self.NH3_EndPoint_Detail_Temp_Np=np.array(self.NH3_EndPoint_Detail_Temp)
        self.NO_EndPoint_Detail_Temp_Np=np.array(self.NO_EndPoint_Detail_Temp)
        self.C_NO_Detail=self.NO_EndPoint_Detail_Temp_Np.reshape(len(self.listAdd),len(self.temperatureListX))

    def analyse_leftshift_Reaction(self):
        currentTime = time.strftime("%Y%m%d_%H%M%S")        
        BestTemperatures=self.temperatureListX[self.C_NO_Detail.argmin(axis=1)]
        BestC=self.C_NO_Detail[np.arange(len(self.C_NO_Detail)),self.C_NO_Detail.argmin(axis=1)]
        plt.figure()
        TemperatureShift=-BestTemperatures+BestTemperatures[0]
        plt.plot(self.listAdd,TemperatureShift)
        plt.xlabel("C(NO)")
        plt.ylabel("Tempeture Shift ($^\circ$C)")
        plt.savefig(os.path.join(ImageResult,self.speciesAdd+currentTime+'TempetureShift.png'))
        plt.show()
        
        plt.figure()
        symbol=['.','*','o','v','^','<','>',',','1','2','3','4','s','p']
        for ithAdd in np.arange(len(self.C_NO_Detail)):            
            plt.plot(self.temperatureListX,self.C_NO_Detail[ithAdd],symbol[ithAdd%14])
        plt.ylabel("NO(out)/NO(in)")
        plt.xlabel("Temperature ($^\circ$C)")
        plt.savefig(os.path.join(ImageResult,self.speciesAdd+currentTime+'DeNOx.png'))
        plt.show()
        with open(self.speciesAdd+"TemperatureShift.csv","a+") as csvFile:
            csvWriter=csv.writer(csvFile)
            csvWriter.writerow(self.listAdd)
            csvWriter.writerow(TemperatureShift)

    def Detail_Overall_withAdd(self,coeficientAddDict,funEmploye=1,draw=False):
        self.NH3_EndPoint_Overall=[]
        self.NO_EndPoint_Overall=[]   
        coefAdd=coeficientAddDict[self.speciesAdd]
        
        for IterAddConctrt in self.listAdd:
            for temperatureIter in self.temperatureListX:
                if funEmploye==1:
                    temperatureShift=coefAdd[0]*np.log(coefAdd[1]*IterAddConctrt+1)
                else:
                    temperatureShift=coefAdd[0]*IterAddConctrt/(coefAdd[1]+IterAddConctrt)
                temperatureIter+=temperatureShift
                PyChemTB.gererateInputFile( reactants=[('N2',0.7895-IterAddConctrt),(self.speciesAdd,IterAddConctrt),
                                            ('NH3',0.0003),
                                            ('NO',0.0002),('O2',0.06),('CO2',0.15)],     # Reactant (mole fraction)

                                            temperature = temperatureIter, # Temperature(K)
                                            pressure = 1 ,   # Pressure (bar)
                                            velocity=75.0,
                                            viscosity=0.0,
                                            reactorDiameter=3.2,
                                            endPosition=45.0,
                                            startPosition=0.0 ,
                                            endTime = 0.05 ,   # End Time (sec)
                                            tempFile="test.inp")                     

                if  temperatureIter<1200:
                    Coeficients=[40609356.32837867,4.591567103723157,59293.190204797174,
                                1.2500592750801196e+48,0.2384295271582183,227638.0184552551]
                if  temperatureIter>=1200:
                    Coeficients=[2.1489719679116273,3.6556482376087636,14.912031071151327,
                                10.977243831448774,3.883371131587305,26418.321246185045]
                
                PyChemTB.generateChemInput(#1.49e19,0,3.6e5,1.2e15,0,3.4e5,
                        Coeficients[0],Coeficients[1],Coeficients[2],Coeficients[3],Coeficients[4],Coeficients[5],
                        tempFile=os.path.join(currentDir,"ChemInput_OverallReaction.inp"))

                fraction_NO_Overall_Reaction,fraction_NH3_Overall_Reaction,residentTimeOverall=getMolesFractions(
                                                #"G:\SNCR\SNCR\chem_add_ITL.inp",
                                                os.path.join(currentDir,"ChemInput_OverallReaction.inp"),
                                                os.path.join(currentDir, "test.inp"))
                
                with open(self.speciesAdd+"{0:g}logFile.txt".format(funEmploye),'a+') as stream:
                    stream.write("Additive:{0:g} ,temperture:{1:g} | Fraction EndPoint {2:g}  Fraction StartPoint {3:g}  \n".format(
                               IterAddConctrt,temperatureIter, fraction_NO_Overall_Reaction.iloc[-1],fraction_NO_Overall_Reaction.iloc[0]))
                self.NH3_EndPoint_Overall.append(fraction_NH3_Overall_Reaction.iloc[-1]/fraction_NH3_Overall_Reaction.iloc[0])        
                self.NO_EndPoint_Overall.append(fraction_NO_Overall_Reaction.iloc[-1]/fraction_NO_Overall_Reaction.iloc[0])
        self.NO_EndPoint_Overall_Temp_Np=np.array(self.NO_EndPoint_Overall)
        self.C_NO_overall=self.NO_EndPoint_Overall_Temp_Np.reshape(len(self.listAdd),len(self.temperatureListX))
        d={self.speciesAdd+'Overall':self.NO_EndPoint_Overall_Temp_Np,self.speciesAdd+'Detail':self.NO_EndPoint_Detail_Temp_Np}
        df=pd.DataFrame(data=d)
        df1=pd.DataFrame(data={"temperatureListX":self.temperatureListX})
        df2=pd.DataFrame(data={self.speciesAdd+"listAdd":self.listAdd})
        dfForAdditive=pd.concat([df,df1,df2], ignore_index=True, axis=1)
        dfForAdditive.to_csv(self.speciesAdd+"ResultAdditiveCompare{0:g}.csv".format(funEmploye))
        if(draw):            
            currentTime = time.strftime("%Y%m%d_%H%M%S")    
            plt.figure()
            symbolOverall=['o','v','^','<','>']
            symbolDetail=['.-','--',':','.--','-']
            for ithAdd in np.arange(len(self.C_NO_Detail)):            
                plt.plot(self.temperatureListX,self.C_NO_Detail[ithAdd],symbolDetail[ithAdd%14])
                plt.plot(self.temperatureListX,self.C_NO_overall[ithAdd],symbolOverall[ithAdd%14])
            plt.ylabel("[NO](out)/[NO](in)")
            plt.xlabel("Temperature ($^\circ$C)")
            plt.savefig(os.path.join(ImageResult,self.speciesAdd+currentTime+'DeNOx.png'))
            plt.show()
    
           

           


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
            1.2500592750801196e+48,0.2384295271582183,227638.0184552551],
            [2.1489719679116273,3.6556482376087636,14.912031071151327,
            10.977243831448774,3.883371131587305,26418.321246185045],
            [24605131153138.434,0.5423493881224208,0.5484230644458539,
            865665.0299722904,3.380599012341277,26111.172189728528],
            [5768579274.510609,0.6620741397171189,1422.3511582152546,
            77603.57418676408,3.4672772057643466,43389.17261664884]
    '''
    Coeficients=[[16084827.893287595,2.587810040194352,23799.73019602423,
            1.2551668605210685e+19,1.3311990757391372,91991.52518245796]]
    calculatorTemperature=temperatureListDiffCalculator(listTemperature)
    for coeficient in Coeficients:
        result=calculatorTemperature.difference_Overall_Detail_temperature(coeficient,draw=True)
        print(result)
    
  