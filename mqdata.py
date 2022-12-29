#!/usr/bin/python

### IMPORT SECTION ###################################################
import os
import sys
import time
import re
######################################################################

### DEFINE FUNCTIONS #################################################
def with_arg(arg, dirpath): # Fetching MQ manager with mask
    mqlist = os.popen("dspmq | grep " + arg + " | awk '/QMNAME/{print $1}' > " + dirpath + "/mqlist")

def without_arg(dirpath): # Fetching all MQ managers
    mqlist = os.popen("dspmq | awk '/QMNAME/{print $1}' > " + dirpath + "/mqlist")

def fetch(dirpath): # Fetching full information
    time.sleep(1)
    with open("mqlist", "r") as f:
        mqlist=f.read().split()
        for i in mqlist:
            result=re.findall(r'(?<=QMNAME\()(.*)(?=\))', i)
            res=str(result[0])
            os.popen("echo 'DISPLAY CHANNEL(*)' | runmqsc " + res + " | grep 'CHLTYPE' | grep -v SYSTEM > " + dirpath + "/" +"/" + res + ".info; echo 'DISPLAY LISTENER(*) PORT' | runmqsc " + res + " | grep LSTNR >> " + dirpath + "/" +"/" + res + ".info; echo 'DISPLAY QL(*)' | runmqsc " + res + " | grep QUEUE | grep -v SYSTEM >> " + dirpath + "/" +"/" + res + ".info")

def nullcheck(dirpath): #Check mqlist for null
    file=dirpath + "/mqlist"
    filesize=os.path.getsize(file)
    return filesize

######################################################################

### DEFINE VARIABLES #################################################
dirpath = os.path.dirname(os.path.realpath(__file__)) # Full path to script

print("MQ data (C)N-Free|\n-------------------\nPlease, enter the MQ manager name (full, or part), or enter \"help\" for more information")
arg = raw_input("-------------------\n>")
print("-------------------")
######################################################################


while arg == "help":
    print("You can enter full or a part of MQ manager name, example:\nFull: QMMCS.TEST11\nPart: MCS\nAs a result the program will be create a file(s) for each manager with full information.\n")
    arg = raw_input("-------------------\n>")
if not arg:
    print("You didn't enter any argument.\nThe program will provide information about all MQ managers. \nYou can find it in the script directory: " + dirpath)
    time.sleep(1)
    without_arg(dirpath)
    fetch(dirpath)
else:
    print("Your argument is: " + arg + "\nThe program will provide information about MQ managers having the keyword in their name.\nYou can find it in the script directory: " + dirpath)
    with_arg(arg, dirpath)
    time.sleep(1)
    filesize=nullcheck(dirpath)
    if filesize == 0:
        print("\nSorry, the program didn't find any MQ Manager with your keyword. \nPlease make sure that you enter a right name and try again.")
    else:
        fetch(dirpath)