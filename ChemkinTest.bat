CALL "C:\Program Files (x86)\Reaction\chemkin15083_pc\bin\run_chemkin_env_setup.bat"
cd C:\Users\dell\Desktop\PythonChemkin
COPY "G:\SNCR\SNCR\chem_add_ITL.inp" "C:\Users\dell\Desktop\PythonChemkin"
COPY "C:\Program Files (x86)\Reaction\chemkin15083_pc\data\therm.dat" "C:\Users\dell\Desktop\PythonChemkin"
COPY "C:\Program Files (x86)\Reaction\chemkin15083_pc\data\tran.dat" "C:\Users\dell\Desktop\PythonChemkin"
CALL "C:\Program Files (x86)\Reaction\chemkin15083_pc\bin\chem.exe" -i chem_add_ITL.inp -o test_python.out -d therm.dat 

COPY "C:\Program Files (x86)\Reaction\chemkin15083_pc\data\chemkindata.dtd"
SET CHEMKIN_MODE=Pro
CKReactorGenericClosed -i test.inp -o chemkin.out
GetSolution
CKSolnTranspose

