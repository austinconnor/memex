#!/usr/bin/env python3

import click
import subprocess
import sys
import os
import time

pids = []
spids = []

cpu = 0.0
ram = 0.0

volurl = "https://github.com/volatilityfoundation/volatility.git"
limeurl = "https://github.com/504ensicsLabs/LiME.git"

profileName = "TEST-PROFILE"

def main():

    filename = str(sys.argv[1])
    pid = getNewProcess(filename)
    
    getInfo(pid)
    
def getInfo(pid): #gets information about a process

    pcpu = ""
    pram = ""

    #elapsed time
    #ps -p <PID> -o etime
    print("PROCESS ID = " + str(pid))
    p = subprocess.Popen(["ps", "-p", str(pid), "-o", "etime"], stdout=subprocess.PIPE)
    #print("ELAPSED TIME" + " = " + str(p.communicate()).split(' ')[7][0:8])

    #resouce usage
    #ps -p <PID> -o %cpu,%mem
    
    while(True):
        p = subprocess.Popen(["ps", "-p", str(pid), "-o", "%cpu,%mem"], stdout=subprocess.PIPE)
        if(len(str(p.communicate()).split(' ')) < 2):
            pcpu = str(0)
        else:
	    p = subprocess.Popen(["ps", "-p", str(pid), "-o", "%cpu,%mem"], stdout=subprocess.PIPE)
            pcpu = str(p.communicate()).split(' ')[2]
        print(pcpu)
        #print("CPU USAGE %" + " = " + pcpu) #prints CPU Usage
        p = subprocess.Popen(["ps", "-p", str(pid), "-o", "%cpu,%mem"], stdout=subprocess.PIPE)
        if(len(str(p.communicate()).split(' ')) < 2):
            pram = str(0)
        else:
            p = subprocess.Popen(["ps", "-p", str(pid), "-o", "%cpu,%mem"], stdout=subprocess.PIPE)
            pram = str(p.communicate()).split(' ')[4][0:3]
        print(pram)
        #print("RAM USAGE %" + " = " + pram) #prints RAM usage
        if(trigger(pcpu, pram) == 1 or trigger(pcpu,pram) == 2):
            break


#made to be used in "getInfo" function
def trigger(pcpu, pram): # detects spikes in ram/cpu usage

    cthresh = 1 #percent amount that must change to trigger a resource usage spike
    rthresh = 1

    if((float(pcpu) - cpu) > cthresh):
        print("CPU USAGE HAS SPIKED")
        return 1
    if((float(rcpu) - ram) > rthresh):
        print("RAM USAGE HAS SPIKED")
        return 2
    
    cpu = float(pcpu)
    ram = float(pram)
    return 0



def getNewProcess(filename):
    
    p = subprocess.Popen(["./" + filename], stdout=subprocess.PIPE)
    time.sleep(3) 
    command = "ps -aux | grep \"" + filename + "\""
    out = os.popen(command).readlines()[2].split(" ")
    out = list(filter(None, out))[1]
    
    
    return out
    
def getUser(): #gets the name of the user

    name = str(subprocess.run("whoami", stdout=subprocess.PIPE).stdout.read())[2:-3]
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
