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
        #print(res) #DEBUG
        #print(type(res)) #DEBUG
        os.popen("echo 'DISPLAY CHANNEL(*)' | runmqsc " + res + " | grep 'CHLTYPE' | grep -v SYSTEM > " + dirpath + "/" +"/" + res + ".info; echo 'DISPLAY LISTENER(*) PORT' | runmqsc " + res + " | grep LSTNR >> " + dirpath + "/" +"/" + res + ".info; echo 'DISPLAY QL(*)' | runmqsc " + res + " | grep QUEUE | grep -v SYSTEM >> " + dirpath + "/" +"/" + res + ".info")
######################################################################

### DEFINE VARIABLES #################################################
dirpath = os.path.dirname(os.path.realpath(__file__)) # Full path to script

print("""MQ data (C)N-Free|
-------------------
Please, enter MQ manager name (full, or part), or enter "help" for more information
""")
arg = raw_input(">")
######################################################################


if arg == "help":
    print("""
You can enter full or part of MQ manager name example:
Full: QMMCS.TEST11
Part: MCS
As result the programm will be create file(s) for each manager with full information.\n
""")
elif not arg:
    print("argument is null")
    without_arg(dirpath)
    fetch(dirpath)
else:
    with_arg(arg, dirpath)
    fetch(dirpath)