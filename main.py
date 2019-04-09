import os
from ObdII import*

mypath = ""
for file in os.listdir(os.getcwd()):
    if file.endswith(".csv") or file.endswith(".xlsx"):
        mypath = os.getcwd() + "/" + file

if mypath == "":
    raise FileNotFoundError

esperienza = Obd2Analysis(mypath)
print(esperienza.getConsumoMedioIst())
esperienza.plotConsumo()