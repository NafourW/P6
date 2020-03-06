
import subprocess
import multiprocessing
import socket
import sys
import os
from time import sleep

class RunServerMonitor:

    def runShell(self):

        os.chdir(os.path.dirname(__file__))
        pathToFile = os.getcwd()
        
        unixDetection = 'uname -a'
        p = subprocess.Popen(unixDetection, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()[0]

        if 'Mint'.encode() in out:
            mintCommandrs = 'mate-terminal -e ' + pathToFile + '"/rcssserver --server::port=6000"'
            mintCommandrm = 'mate-terminal -e "rcssmonitor"'
            mintRunTerm = subprocess.Popen(mintCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            mintRunTerm = subprocess.Popen(mintCommandrs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if 'Ubuntu'.encode() in out:
            try:
                # otherwise gnome-terminal is the issued terminal for ubuntu 
                ubuntuCommandrs = 'mate-terminal -e "/usr/local/bin/rcssserver --server::port=6000"'
                ubuntuCommandrm = 'mate-terminal -e "rcssmonitor"'            
                ubuntuRunTermrm = subprocess.Popen(ubuntuCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                ubuntuRunTermrs = subprocess.Popen(ubuntuCommandrs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except KeyboardInterrupt as e:
                sys.exit('Failed to start %r, reason %s' % (ubuntuCommandrs, e))
                sys.exit('Failed to start %r, reason %s' % (ubuntuCommandrm, e))
            

        if 'Darwin'.encode() in out:
            macOSCommandrs = """ osascript -e 'tell app "Terminal" to do script "/usr/local/bin/rcssserver --server::port=6000"' """
            macOSCommandrm = """ osascript -e 'tell app "Terminal" to do script "rcssmonitor"' """
            macOStermrs = subprocess.Popen(macOSCommandrs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
            macOStermrm = subprocess.Popen(macOSCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)        
    
    def readLogFile(self):

        with open('incomplete.rcg') as f:
            while True:
                line = f.readline()
                if line:
                    print(line)


class Client:

    def startme(self):
        self.udp_ip = "localhost"
        self.udp_port = 6000
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

    def train(self, command):
        # Initialize client (init [TeamName])
        #command = "(init Team1)"

        # Send command to server
        self.sock.sendto(command.encode(), (self.udp_ip, self.udp_port))

        #command = "(move 10 10)"
        #self.sock.sendto(command.encode(), (self.udp_ip, self.udp_port))
        
        

        #sleep(10)

        #command = "(bye)"
        #self.sock.sendto(command.encode(), (self.udp_ip, self.udp_port))


if __name__ == "__main__":

    # Run shells
    ex = RunServerMonitor()
    ex.runShell()
    sleep(3) # wait for network to setup
    

    # Create 11 processes each of them connecting to the server and initializing
    for i in range(0, 11):
        client = Client()
        client.startme()
        client.train("(init TEAM1)")
        client.train("(move 10 10)")
        #client.sendCommandToRcsserver("(move 10 11)")
        #process = multiprocessing.Process(target=client.train, args=())
        #process.start()
    # while True: 
    #     cmdToSend = input()
    #     client.train("(move (p 'TEAM1' 10)10 "+str(cmdToSend)+")")
        
    ex.readLogFile()

