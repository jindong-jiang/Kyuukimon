CALL "C:\Program Files\Reaction\chemkin15083_pc\bin\run_chemkin_env_setup.bat"
cd "e:/Kyuukimon_master/Kyuukimon\tempDeNOx"

COPY "C:\Program Files\Reaction\chemkin15083_pc\data\therm.dat"
COPY "C:\Program Files\Reaction\chemkin15083_pc\data\tran.dat"
CALL "C:\Program Files\Reaction\chemkin15083_pc\bin\chem.exe" -i "e:/Kyuukimon_master/Kyuukimon\ChemInput_OverallReaction.inp" -o test_python.out -d therm.dat

COPY "C:\Program Files\Reaction\chemkin15083_pc\data\chemkindata.dtd"
SET CHEMKIN_MODE=Pro
CKReactorPlugFlow -i "e:/Kyuukimon_master/Kyuukimon\test.inp" -o chemkin.out
GetSolution
CKSolnTranspose