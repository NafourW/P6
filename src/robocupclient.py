import subprocess
import socket
import sys
import os

class RunServerMonitor:

    def runShells(self):
        pathToFile = os.getcwd()
        pathToLogs = pathToFile + "/logs"
        
        unixDetection = 'uname -a'
        p = subprocess.Popen(unixDetection, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()[0]

        if 'Mint'.encode() in out:
            mintCommandrs = 'cd logs ; mate-terminal -e "rcssserver --server::port=6000"'
            mintCommandrm = 'mate-terminal -e "rcssmonitor"'
            mintRunTerm = subprocess.Popen(mintCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            mintRunTers = subprocess.Popen(mintCommandrs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        elif 'Ubuntu'.encode() in out:
            try:
                # otherwise gnome-terminal is the issued terminal for ubuntu 
                ubuntuCommandrs = 'cd logs ; gnome-terminal -e "rcssserver --server::port=6000"'
                ubuntuCommandrm = 'gnome-terminal -e "rcssmonitor"'            
                ubuntuRunTermrm = subprocess.Popen(ubuntuCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                ubuntuRunTermrs = subprocess.Popen(ubuntuCommandrs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except KeyboardInterrupt as e:
                sys.exit('Failed to start %r, reason %s' % (ubuntuRunTermrm, e))
                sys.exit('Failed to start %r, reason %s' % (ubuntuRunTermrs, e))

        elif 'Darwin'.encode() in out:
            try:
                macOSCommandcd = "osascript -e" + "'tell app " + '"Terminal" ' + "to do script " + '"cd ' + pathToLogs + " ; "+ "rcssserver --server::port=6000" + '"' + "' "
                macOSCommandrm = """ osascript -e 'tell app "Terminal" to do script "rcssmonitor"' """
                macOStermcd = subprocess.Popen(macOSCommandcd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                macOStermrm = subprocess.Popen(macOSCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)       
            except KeyboardInterrupt as e:
                sys.exit('Failed to start %r, reason %s' % (macOStermcd, e))
                sys.exit('Failed to start %r, reason %s' % (macOStermrm, e))
        else:
            print("OS not supported.")

class Client:

    def startme(self):
        self.udp_ip = "localhost"
        self.udp_port = 6000
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

    def train(self, command):

        # Send command to server
        self.sock.sendto(command.encode(), (self.udp_ip, self.udp_port))
