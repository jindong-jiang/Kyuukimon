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

def getMolesFractions(machanismInp,expParameterInp):
    if os.path.exists(tempDir):
        shutil.rmtree(tempDir)
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


def difference_Overall_Detail(Coefficient):

    PyChemTB.generateChemInput(#1.49e19,0,3.6e5,1.2e15,0,3.4e5,
                               Coefficient[0],Coefficient[1],Coefficient[2],Coefficient[3],Coefficient[4],Coefficient[5],
                               tempFile=os.path.join(currentDir,"ChemInput_OverallReaction.inp"))




    fraction_NO_Detail_Reaction,fraction_NH3_Detail_Reaction,residentTimeDetail=getMolesFractions(
                                                    "G:\SNCR\SNCR\chem_add_ITL.inp",
                                                    os.path.join(currentDir, "test.inp"))
    fraction_NO_Overall_Reaction,fraction_NH3_Overall_Reaction,residentTimeOverall=getMolesFractions(
                                                     #"G:\SNCR\SNCR\chem_add_ITL.inp",
                                                    os.path.join(currentDir,"ChemInput_OverallReaction.inp"),
                                                    os.path.join(currentDir, "test.inp"))
    # print(fraction_NO_Overall_Reaction.ilpoc[])

    f_NO_Detail=interp1d(residentTimeDetail.values,fraction_NO_Detail_Reaction.values,kind='linear',fill_value="extrapolate")
    f_NH3_Detail=interp1d(residentTimeDetail.values,fraction_NH3_Detail_Reaction.values,kind='linear',fill_value="extrapolate")
    f_NO_Overall=interp1d(residentTimeOverall.values,fraction_NO_Overall_Reaction.values,kind='linear',fill_value="extrapolate")
    f_NH3_Overall=interp1d(residentTimeOverall.values,fraction_NH3_Overall_Reaction.values,kind='linear',fill_value="extrapolate")

    comparationListTime = np.linspace(residentTimeDetail.values[0],residentTimeDetail.values[-1],
                                    num=20,endpoint=True )
    comparationList_NO_Detail = f_NO_Detail(comparationListTime)
    comparationList_NH3_Detail = f_NH3_Detail(comparationListTime)
    comparationList_NO_Overall = f_NO_Overall(comparationListTime)
    comparationList_NH3_Overall = f_NH3_Overall(comparationListTime)

    diff2_NO = ((comparationList_NO_Detail-comparationList_NO_Overall)/fraction_NO_Overall_Reaction[0])**2
    diff2_NH3 = ((comparationList_NH3_Detail-comparationList_NH3_Overall)/fraction_NH3_Overall_Reaction[0])**2
    return (2*diff2_NO.mean()+diff2_NH3.mean())/3
'''
    plt.figure(1)
    plt.plot(residentTimeOverall,fraction_NO_Overall_Reaction/fraction_NO_Overall_Reaction[0],'--',
             residentTimeDetail,fraction_NO_Detail_Reaction/fraction_NO_Detail_Reaction[0],'-.',
             #residentTimeOverall,fraction_NH3_Overall_Reaction,'v',
             #residentTimeDetail,fraction_NH3_Detail_Reaction,'^',
             )
    plt.figure(2)
    plt.plot(comparationListTime,diff2_NO,'--',
             comparationListTime,diff2_NH3,'-.',
             #residentTimeOverall,fraction_NH3_Overall_Reaction,'v',
             #residentTimeDetail,fraction_NH3_Detail_Reaction,'^',
             )
    plt.xlabel('ResidentTime',fontsize='large')
    plt.ylabel('Fraction out/ Fraction in',fontsize='large')
    plt.show()
'''

PyChemTB.gererateInputFile(        reactants=[#('CH4',0),
                                                 #('CO',0.0),
                                                 #('CO2',0.15),
                                                 #('H2',0.2),
                                                 ('N2',0.7895),
                                                 ('NH3',0.0003),
                                                 ('NO',0.0002),
                                                 ('O2',0.06),
                                                 ('CO2',0.15)],     # Reactant (mole fraction)

                                      temperature = 1200, # Temperature(K)
                                      pressure = 1 ,   # Pressure (bar)
                                      velocity=75.0,
                                      viscosity=0.0,
                                      reactorDiameter=3.2,
                                      endPosition=45.0,
                                      startPosition=0.0 ,
                                      endTime = 0.05 ,   # End Time (sec)
                                      tempFile="test.inp",
                                      #Continuations = True,             # Continuations
                                      #typeContinuation = 'NEWRUN',      # Type of continuation NEWRUN or CNTN
                                      #Tlist=[1000.,1200.],              # Temperature (K) list of continuations
                                      #Plist=[1.,2.],                   # Pressure (atm) list of continuations

                                      #variableVolume = True,            # Variable volume true / false
                                      #variableVolumeProfile =vproFile,  # File name path for vpro (sec,cm3)

                                      #solverTimeStepProfile = solTimeStepFile # Solver time profile (sec))
                                )


Coeficients=[1e15,0,3e4,1e15,0,3e4]
val_diff=difference_Overall_Detail(Coefficient=Coeficients)
print(val_diff)
