
import os
import platform

OS=platform.system()

wd=os.getcwd()
if OS == "Windows": 
    directory=wd+"\IP_Project"
else:
    directory=wd+"/IP_Project"

if not os.path.exists(directory):
    os.makedirs(directory)
#directory=wd
for file in os.listdir(directory):
    if file.endswith(".txt"):
        #print(os.path.join(directory, file))
        print(os.path.splitext(file)[0])
        #print file
    else:
        print "No .txt file exists\n"
