import socket
import os
import threading


def Netscanner(scanip, IPIS, lock):
    result = os.popen("ping {0} -n 1".format(scanip)).read()

    if "TTL" in result:
        with lock:
            print(scanip)
            IPIS.append(scanip)

def GetDeviceName(deviceIP):
    try:
        device_name = socket.gethostbyaddr(deviceIP)
        print(device_name)
    except Exception as e:
        pass

def get_ip():
    iplist = []
    IP = os.popen("ipconfig")
    for line in IP.readlines():
        if "IPv4" in line:
            start = line.find(":")
            result = line[start + 2:-1]
            iplist.append(result)
    return iplist


def Run():
    lock = threading.Lock()
    iplist = get_ip()
    
    if not iplist:
        print("No IPv4 addresses found.")
        return
    
    myip = iplist[0]  # Use the first IP address from the list
    print("My IP is:", myip)
    
    # If you want to cut off the last octet from the IP address:
    myip = myip[:myip.rfind(".") + 1]
    
    lock = threading.Lock()

    IPIS = []
    threads = []

    for last in range(1, 255):
        scanip = myip + str(last)
        t = threading.Thread(target=Netscanner, args=(scanip, IPIS, lock,))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    print("Total Users:", len(IPIS))
    # print(IPIS)
    print("\n")

    for deviceIP in IPIS:
        t = threading.Thread(target=GetDeviceName, args=(deviceIP,))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    Run()
    while True:
        WhatToDo = input("Press 'r' to Relaunch or Press any other key to Exit: ")
        if WhatToDo.lower() == "r":
            Run()
        else:
            exit(0)
