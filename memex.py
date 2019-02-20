import click
import subprocess
import sys
import os

pids = []
spids = []

volurl = "https://github.com/volatilityfoundation/volatility.git"
limeurl = "https://github.com/504ensicsLabs/LiME.git"

profileName = "TEST-PROFILE"

def main():
    #filename = sys.argv[1]
    #p = subprocess.Popen("./" + filename + " & echo $!", stdout=subprocess.PIPE)
    makeProfile()
    #print(str(os.path.isdir("/volatility")))
    
def getInfo(pid): #gets information about a process

    #elapsed time
    #ps -p <PID> -o etime
    print("PROCESS ID = " + str(pid))
    p = subprocess.Popen(["ps", "-p", str(pid), "-o", "etime"], stdout=subprocess.PIPE)
    print("ELAPSED TIME" + " = " + str(p.communicate()).split(' ')[7][0:8])

    #resouce usage
    #ps -p <PID> -o %cpu,%mem
    p = subprocess.Popen(["ps", "-p", str(pid), "-o", "%cpu,%mem"], stdout=subprocess.PIPE)
    print("CPU USAGE %" + " = " + str(p.communicate()).split(' ')[2])
    p = subprocess.Popen(["ps", "-p", str(pid), "-o", "%cpu,%mem"], stdout=subprocess.PIPE)
    print("CPU USAGE %" + " = " + str(p.communicate()).split(' ')[4][0:3])


def getNewProcess():

    arr = []

    name = getUser()
    #number of processes, ps aux | wc -l
    pnum = int(subprocess.Popen("ps aux | wc -l", shell=True, stdout=subprocess.PIPE).stdout.read())
    
    p = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
    procList = str(p.communicate()).split("\\n")

    for i in range(1,pnum-2): #gets list of PID's under the current user
        n = str(procList[i].split(' ')[0])
        if (n == name):
            l = list(filter(None, procList[i].split(' ')))
            arr.append(l[1])
    return arr

    
def getUser(): #gets the name of the user

    name = str(subprocess.Popen("whoami", stdout=subprocess.PIPE).stdout.read())[2:-3]
    print(name)
    
    return name
    
def getDifference(l1, l2):
    return(list(set(l1) - set(l2)))


def makeProfile():
    #Getting Kernel version: uname -r
    volpath = str("/home/" + getUser() + "/volatility/")
    profilePath = volpath + "volatility/plugins/overlays/linux/"
    modulePath = volpath + "tools/linux/module.dwarf"
    kv = str(subprocess.Popen(["uname","-r"], stdout=subprocess.PIPE).stdout.read())[2:-3]

    if(not os.path.isdir(volpath)):
        p = subprocess.Popen(["git", "clone", volurl, "/home/" + getUser() + "/"])
    
    p = subprocess.Popen(["sudo", "zip", volpath + "volatility/plugins/overlays/linux/" + profileName, modulePath, "/boot/System.map-" + kv])
    print("Zipping Complete!")
    print("Showing Volatility info...")
    p = subprocess.Popen(["python", volpath + "vol.py", "--info"])
    
    print("Profile Made! Type 'sudo volatility --info' ")
    

if __name__ == ("__main__"):
    main()