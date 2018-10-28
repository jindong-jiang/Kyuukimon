import Python_Chemkin_ToolBox as PyChemTB
import os
import subprocess
import shutil
import matplotlib.pyplot as plt
import numpy as np

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


PyChemTB.gererateInputFile(        reactants=[#('CH4',0),
                                             #('CO',0.0),
                                             #('CO2',0.15),
                                             #('H2',0.2),
                                             ('N2',0.7898),
                                             ('NH3',0.02),
                                             ('NO',0.0002),
                                             ('O2',0.06),],     # Reactant (mole fraction)

                                  temperature = 1100, # Temperature(K)
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



PyChemTB.generateChemInput(#3.56e20,0,1.03e4,1.48e10,0,5.95e3,
                           2e10,0,1.03e20,1e15,0,5.95e4,
                           tempFile=os.path.join(currentDir,"ChemInput_OverallReaction.inp"))




fraction_NO_Detail_Reaction,fraction_NH3_Detail_Reaction,residentTimeDetail=getMolesFractions(
                                                "G:\SNCR\SNCR\chem_add_ITL.inp",
                                                os.path.join(currentDir, "test.inp"))
fraction_NO_Overall_Reaction,fraction_NH3_Overall_Reaction,residentTimeOverall=getMolesFractions(
                                                os.path.join(currentDir,"ChemInput_OverallReaction.inp"),
                                                os.path.join(currentDir, "test.inp"))

plt.plot(residentTimeOverall,fraction_NO_Overall_Reaction,'--',
         residentTimeDetail,fraction_NO_Detail_Reaction,'-.',
         residentTimeOverall,fraction_NH3_Overall_Reaction,'v',
         residentTimeDetail,fraction_NH3_Detail_Reaction,'^',
         )
plt.show()
plt.xlabel('ResidentTime',fontsize='large')
plt.ylabel('Fraction out/ Fraction in',fontsize='large')

