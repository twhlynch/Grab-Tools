import os

for file in os.listdir("levels"):
    if file.endswith(".level"):
        os.system('python GRAB-Level-Format-main/tools/ConvertToJSON.py'+' levels/'+file+' levels/'+file+'.json')