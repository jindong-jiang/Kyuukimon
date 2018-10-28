import subprocess
import os

# tempDir=r'C:\Users\dell\Desktop\PythonChemkin\tempDir'





scriptFile = os.path.join(r'C:\Users\dell\Desktop\PythonChemkin', 'ChemkinTest.bat')
process = subprocess.Popen( scriptFile, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print(stdout)
    print(stderr)
    quit()


