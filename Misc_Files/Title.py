import shlex
import os

wd = os.getcwd()
path = wd +"\IP_Project"
os.chdir(path)



def Get_2017(c):
    i = 0
    count=0
    for i in c:
        if i == "2017":
            return count
        count += 1
        
def Get_Abstract(c):
    i=0
    count=0
    for i in c:
        if i == "Abstract":
            return count
        count+=1

def Get_Title():
    for file in os.listdir(path):
        if file.startswith("8"):
            f = open(file,"r")
            contents=f.read()
            f.close()
            contents=str(contents)+'\''
            c=shlex.split(contents)    
            start=Get_2017(c)
            end=Get_Abstract(c)
            print"start: "+str(start)
            print"end: "+str(end)
            title=''
            for i in range(start+1,end):
                title=title+" "+c[i]

            print title


Get_Title()

    
