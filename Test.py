import Python_Chemkin_ToolBox as PyChemTB
import os
import subprocess


currentDir = os.path.dirname(__file__)
tempDir = os.path.join(currentDir, 'tempDeNOx')

if not os.path.exists(tempDir):
    os.makedirs(tempDir)


PyChemTB.gererateInputFile(        reactants=[#('CH4',0),
                                             #('CO',0.0),
                                             #('CO2',0.15),
                                             #('H2',0.2),
                                             ('N2',0.3),
                                             ('NH3',0.2),
                                             ('NO',0.2),
                                             ('O2',0.3),],     # Reactant (mole fraction)

                                  temperature = 1100, # Temperature(K)
                                  pressure = 1 ,   # Pressure (bar)
                                  velocity=75.0,
                                  viscosity=0.0,
                                  reactorDiameter=3.2,
                                  endPosition=45.0,
                                  startPosition=0.0 ,
                                  endTime = 0.05 ,   # End Time (sec)
                                  tempFile=os.path.join(tempDir,"test.inp"),
                                  #Continuations = True,             # Continuations
                                  #typeContinuation = 'NEWRUN',      # Type of continuation NEWRUN or CNTN
                                  #Tlist=[1000.,1200.],              # Temperature (K) list of continuations
                                  #Plist=[1.,2.],                   # Pressure (atm) list of continuations

                                  #variableVolume = True,            # Variable volume true / false
                                  #variableVolumeProfile =vproFile,  # File name path for vpro (sec,cm3)

                                  #solverTimeStepProfile = solTimeStepFile # Solver time profile (sec))
                            )

#PyChemTB.postProcess()

PyChemTB.generateChemInput(3.56e20,0,1.03e4,1.48e10,0,5.95e3,
                           tempFile=os.path.join(tempDir,"ChemInput_OverallReaction.inp"))

PyChemTB.generateBatFile('ChemInput_OverallReaction.inp','test.inp',tempDir,"DeNOxExp.bat")
process=subprocess.Popen(os.path.join(tempDir,"DeNOxExp.bat"), cwd=tempDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
