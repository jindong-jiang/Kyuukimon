import numpy as np
import pandas as pd
import os



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

    if variableVolume:
        with open(variableVolumeProfile, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in reader:
                time = float(row[0].split(',')[0]) # (sec)
                vol = float(row[0].split(',')[1]) # (cm3)
                input_stream+=("""
VPRO {0:g} {1:g}   ! Volume (cm3)""".format(time,vol))

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
ATLS 1.0E-6   ! Sensitivity Absolute Tolerance
ATOL 1.0E-10   ! Absolute Tolerance
RTLS 1.0E-7   ! Sensitivity Relative Tolerance
RTOL 1.0E-8   ! Relative Tolerance
GFAC 1.0   ! Gas Reaction Rate Multiplier""")

    if solverTimeStepProfile:
        with open(solverTimeStepProfile, 'rb') as csvfile2:
            timeStepReader = csv.reader(csvfile2, delimiter=' ', quotechar='|')
            for row in timeStepReader:
                time = float(row[0].split(',')[0]) # (sec)
                vol = float(row[0].split(',')[1]) # (sec)
                input_stream+=("""
STPTPRO {0:g} {1:g}           ! Solver Maximum Step Time (sec)""".format(time,vol))

    if Continuations:
        if numpy.array(Tlist).size:
            for i in range(numpy.array(Tlist).shape[0]):
                input_stream+=("""
{0}
{0}
END
TEMP {1:g}""".format(typeContinuation,numpy.array(Tlist)[i]))

        if numpy.array(Plist).size:
            for i in range(numpy.array(Plist).shape[0]):
                input_stream+=("""
{0}
END
PRES {1:g}""".format(typeContinuation,numpy.array(Plist)[i]/1.01325))

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

def generateChemInput(A1,B1,E1,A2,B2,E2,tempFile):
    input_stream=("""ELEMENTS O H N C END
SPECIES NH3 NO O2 N2 H2O END
REACTIONS
NH3+NO+0.25O2=>N2+1.5H2O {0:g}  {1:g}  {2:g}
NH3+1.25O2=>NO+1.5H2O  {3:g} {4:g} {5:g}
END
    """.format(A1,B1,E1,A2,B2,E2) )
    with open(tempFile,'w') as stream:
        stream.write(input_stream)


def generateBatFile(chemicalMecanismInp,ChemkinParametreInp,tempDir,tempFile):
    input_stream=(r"""
CALL "C:\Program Files (x86)\Reaction\chemkin15083_pc\bin\run_chemkin_env_setup.bat"
cd {2}

COPY "C:\Program Files (x86)\Reaction\chemkin15083_pc\data\therm.dat"
COPY "C:\Program Files (x86)\Reaction\chemkin15083_pc\data\tran.dat"
CALL "C:\Program Files (x86)\Reaction\chemkin15083_pc\bin\chem.exe" -i {0} -o test_python.out -d therm.dat

COPY "C:\Program Files (x86)\Reaction\chemkin15083_pc\data\chemkindata.dtd"
SET CHEMKIN_MODE=Pro
CKReactorGenericClosed -i {1} -o chemkin.out
GetSolution
CKSolnTranspose""".format(chemicalMecanismInp,ChemkinParametreInp,tempDir))
    with open(os.path.join(tempDir,tempFile),'w') as stream:
        stream.write(input_stream)
