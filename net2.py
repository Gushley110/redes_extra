import subprocess
import os

class FileManager:

    def __init__(self,srcname = None,trgtname = None):
        self.srcname  = srcname
        self.trgtname = trgtname

    def addLine(self, text):
        with open(self.trgtname, mode='a+') as new_file:
            new_file.write(text + os.linesep)
    
    def readLines(self):
        with open(self.srcname) as file:
            lines = file.readlines()
        return [line.rstrip('\n') for line in lines]

def scan_network(network):

    net = network.split('.')
    fm = FileManager(None,'Discovery.txt')

    network = net[0] + '.' + net[1] + '.' + net[2] + '.' 
  
    for ping in range(1,10): 
        address = network + str(ping) 
        res = subprocess.call(['ping', '-c', '2', address]) 
        if res == 0: 
            print( "ping to", address, "OK") 
            fm.addLine(address)
        elif res == 2: 
            print("no response from", address) 
        else: 
            print("ping to", address, "failed!") 



