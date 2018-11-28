import numpy  
import pandas as pd
import os

ChemkinDiretory=r"C:\Program Files\Reaction\chemkin15083_pc"

def gererateInputFile( reactants, temperature, pressure,velocity,viscosity,
                      reactorDiameter,endPosition,startPosition ,endTime,tempFile,
                      Continuations=False, typeContinuation = None, Tlist = [], Plist = [],
                      variableVolume=False, variableVolumeProfile = None,
                      solverTimeStepProfile = None):
    input_stream=("""ENRG   ! Solve Gas Energy Equation""")

    # Solver type definition block

    input_stream+=("""
MOMEN ON   ! Turn on Momentum Equation
PLUG   ! Plug Flow Reactor
RTIME ON   ! Turn on Residence Time Calculation""")

    # Physical property

    input_stream+=("""
!Surface_Temperature   ! Surface Temperature Same as Gas Temperature\n""")

    input_stream+=('PRES {0:g}   ! Pressure (atm)\n'.format(pressure))
    input_stream+=('QLOS 0.0   ! Heat Loss (cal/sec)\n')
    input_stream+=('TEMP {0:g}   ! Temperature (K)'.format(temperature))

   
    # Species property block

    input_stream+=('''
VEL {0:g} ! Axial Velocity (cm/sec)'
VIS {1:g} ! ! Mixture Viscosity (g/cm-sec)'
DIAM {2:g}  ! Diameter (cm)
XEND {3:g}   ! Ending Axial Position (cm)
XSTR {4:g}  ! Starting Axial Position (cm) \n'''.format(velocity,viscosity,reactorDiameter,endPosition,startPosition))

    for reac , conc in reactants:
        input_stream+=('REAC {0} {1:g} ! Reactant Fraction (mole fraction) \n'.format(reac,conc))

    # Solver control block

    input_stream+=("""
ADAP   ! Save Additional Adaptive Points
ASTEPS 20   ! Use Solver Integration Steps
ATLS 1.0E-7   ! Sensitivity Absolute Tolerance
ATOL 1.0E-10   ! Absolute Tolerance
RTLS 1.0E-7   ! Sensitivity Relative Tolerance
RTOL 1.0E-8   ! Relative Tolerance
GFAC 1.0   ! Gas Reaction Rate Multiplier""")

    
    input_stream+=('\nEND')

    with open(tempFile, 'w') as stream:
            stream.write(input_stream)

    return input_stream

def postProcess(resultFile):
    try:
        df=pd.read_csv(resultFile)
        fraction_NO=df[" Mole_fraction_NO_()"]
        fraction_NH3=df[" Mole_fraction_NH3_()"]
        residentTime=df[" Plug_flow_residence_time_(sec)"]
        return fraction_NO,fraction_NH3,residentTime
    except:
        print("No result data exists")

def generateChemInput(A1,B1,E1,A2,B2,E2,tempFile,withAdditive=False,*enhenceFactor):
    if not withAdditive:
        input_stream=("""ELEMENTS O H N C END
SPECIES NH3 NO O2 N2 H2O CO2 END
REACTIONS
NH3+NO+0.25O2=>N2+1.5H2O {0:g}  {1:g}  {2:g}
NH3+1.25O2=>NO+1.5H2O  {3:g} {4:g} {5:g}
END
    """.format(A1,B1,E1,A2,B2,E2) )
        with open(tempFile,'w') as stream:
            stream.write(input_stream)
    else:
        input_stream=("""ELEMENTS O H N C END
SPECIES NH3 NO O2 N2 H2O CO2 CO CH4 H2 END
REACTIONS
NH3+NO+0.25O2+M=>N2+1.5H2O+M {0:g}  {1:g}  {2:g}
CO/{6:g}/ H2/{7:g}/ CH4/{8:g}/
NH3+1.25O2+M=>NO+1.5H2O+M  {3:g} {4:g} {5:g}
CO/{9:g}/ H2/{10:g}/ CH4/{11:g}/
END
    """.format(A1,B1,E1,A2,B2,E2,enhenceFactor[0],enhenceFactor[1],enhenceFactor[2],
    enhenceFactor[3],enhenceFactor[4],enhenceFactor[5]) )
        with open(tempFile,'w') as stream:
            stream.write(input_stream)





fileEnvBat=os.path.join(ChemkinDiretory,r'bin\run_chemkin_env_setup.bat')
fileEnvTherm=os.path.join(ChemkinDiretory,r'data\therm.dat')
fileEnvTran=os.path.join(ChemkinDiretory,r'data\tran.dat')
fileEnvChexe=os.path.join(ChemkinDiretory,r'bin\chem.exe')
fileEnvChdtd=os.path.join(ChemkinDiretory,r'data\chemkindata.dtd')
def generateBatFile(chemicalMecanismInp,ChemkinParametreInp,tempDir,tempFile):


    input_stream=(r"""CALL "{3}"
cd "{2}"

COPY "{4}"
COPY "{5}"
CALL "{6}" -i "{0}" -o test_python.out -d therm.dat

COPY "{7}"
SET CHEMKIN_MODE=Pro
CKReactorPlugFlow -i "{1}" -o chemkin.out
GetSolution
CKSolnTranspose""".format(chemicalMecanismInp,ChemkinParametreInp,tempDir,fileEnvBat,fileEnvTherm,
                          fileEnvTran,fileEnvChexe,fileEnvChdtd))
    with open(os.path.join(tempDir,tempFile),'w') as stream:
        stream.write(input_stream)
