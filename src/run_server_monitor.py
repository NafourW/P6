import subprocess
import sys
import os

class RunServerMonitor:

    def runShells(self):
        pathToFile = os.getcwd()
        pathToLogs = pathToFile + "/logsfiles"
        
        unixDetection = 'uname -a'
        p = subprocess.Popen(unixDetection, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()[0]

        if 'Mint'.encode() in out:
            try:
                mintCommandrs = 'cd logfiles ; mate-terminal -e "rcssserver --server::port=6000"'
                mintCommandrm = 'mate-terminal -e "rcssmonitor"'
                mintRunTerm = subprocess.Popen(mintCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                mintRunTers = subprocess.Popen(mintCommandrs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except KeyboardInterrupt as e:
                sys.exit('Failed to start %r, reason %s' % (mintRunTerm, e))
                sys.exit('Failed to start %r, reason %s' % (mintRunTers, e))

        elif 'Ubuntu'.encode() in out:
            try:
                # otherwise gnome-terminal is the issued terminal for ubuntu 
                ubuntuCommandrs = 'cd logfiles ; gnome-terminal -e "rcssserver --server::port=6000"'
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
