import numpy as np
import pandas as pd



def gererateInputFile( reactants, temperature, pressure,velocity,viscosity,
                      reactorDiameter,endPosition,startPosition ,endTime,
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

    input_stream+=('PRES {0:g}   ! Pressure (atm)\n'.format(pressure/1.01325))
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
XSTR {4:g}  ! Starting Axial Position (cm)'''.format(velocity,viscosity,reactorDiameter,endPosition,startPosition))

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

    with open("test.inp", 'w') as stream:
            stream.write(input_stream)

    return input_stream

def postProcess():
    df=pd.read_csv(r'C:\Users\dell\Desktop\PythonChemkin\CKSoln_solution_no_1_1.csv')

    fraction_NO=df[" Mole_fraction_NO_()"]
    fraction_NH3=df[" Mole_fraction_NH3_()"]
    print(fraction_NO,fraction_NH3)

def generateChemInput():


