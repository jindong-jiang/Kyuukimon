import Python_Chemkin_ToolBox as PyChemTB
'''
PyChemTB.gererateInputFile(        reactants=[('CH4',0),
                                             ('CO',0.0),
                                             ('CO2',0.15),
                                             ('H2',0.0),
                                             ('N2',0.7898),
                                             ('NH3',0.0),
                                             ('NO',0.0002),
                                             ('O2',0.6),],     # Reactant (mole fraction)

                                  temperature = 700, # Temperature(K)
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
'''
PyChemTB.postProcess()
