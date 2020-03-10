import subprocess
import socket
import sys
import os


class ReadWriteLogFiles:

    def readLogFile(self):
        writeFile = open('logs/gameLog.rcg', 'w') # File to write to "new log"
        with open('logs/incomplete.rcg', 'r') as fd: # Readom from this file for realtime logging
            while True:
                logData = fd.readline()
                if logData:
                    writeFile.write(logData)


class RunServerMonitor:

    def runShells(self):
        pathToFile = os.getcwd()
        pathToLogs = pathToFile + "/logs"
        
        unixDetection = 'uname -a'
        p = subprocess.Popen(unixDetection, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()[0]

        if 'Mint'.encode() in out:
            mintCommandrs = 'mate-terminal -e "/rcssserver --server::port=6000"'
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
                sys.exit('Failed to start %r, reason %s' % (ubuntuRunTermrm, e))
                sys.exit('Failed to start %r, reason %s' % (ubuntuRunTermrs, e))

        if 'Darwin'.encode() in out:
            try:
                macOSCommandcd = "osascript -e" + "'tell app " + '"Terminal" ' + "to do script " + '"cd ' + pathToLogs + " ; "+ "rcssserver --server::port=6000" + '"' + "' "
                macOSCommandrm = """ osascript -e 'tell app "Terminal" to do script "rcssmonitor"' """
                macOStermcd = subprocess.Popen(macOSCommandcd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                macOStermrm = subprocess.Popen(macOSCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)       
            except KeyboardInterrupt as e:
                sys.exit('Failed to start %r, reason %s' % (macOStermcd, e))
                sys.exit('Failed to start %r, reason %s' % (macOStermrm, e))


class Client:

    def startme(self):
        self.udp_ip = "localhost"
        self.udp_port = 6000
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

    def train(self, command):

        # Send command to server
        self.sock.sendto(command.encode(), (self.udp_ip, self.udp_port))
