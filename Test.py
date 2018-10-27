import Python_Chemkin_ToolBox as PyChemTB

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

                                  #Continuations = True,             # Continuations
                                  #typeContinuation = 'NEWRUN',      # Type of continuation NEWRUN or CNTN
                                  #Tlist=[1000.,1200.],              # Temperature (K) list of continuations
                                  #Plist=[1.,2.],                   # Pressure (atm) list of continuations

                                  #variableVolume = True,            # Variable volume true / false
                                  #variableVolumeProfile =vproFile,  # File name path for vpro (sec,cm3)

                                  #solverTimeStepProfile = solTimeStepFile # Solver time profile (sec))
                            )

#PyChemTB.postProcess()

PyChemTB.generateChemInput(3.56e49,0,1.03e6,1.48e24,0,5.95e5)
