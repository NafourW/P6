import unittest
from multiprocessing import Process
from threading import Thread
import subprocess
import socket
import sys
import os


class ConnectionTesting(unittest.TestCase):
    def test_terminal_commands(self):
        pathToFile = os.getcwd()
        pathToLogs = pathToFile + "/logs"
        
        unixDetection = 'uname -a'
        p = subprocess.Popen(unixDetection, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()[0]

        if 'Mint'.encode() in out:
            mintCommandrs = 'mate-terminal -e "/rcssserver --server::port=6000"'
            mintCommandrm = 'mate-terminal -e "rcssmonitor"'
            mintRunTermrm = subprocess.Popen(mintCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            mintRunTermrs = subprocess.Popen(mintCommandrs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            mintRunTermrm.kill()
            mintRunTermrm.wait()
            mintRunTermrs.kill()
            mintRunTermrs.wait()
        elif 'Ubuntu'.encode() in out:
            # otherwise gnome-terminal is the issued terminal for ubuntu 
            ubuntuCommandrs = 'cd logs ; mate-terminal -e "rcssserver --server::port=6000"'
            ubuntuCommandrm = 'mate-terminal -e "rcssmonitor"'            
            ubuntuRunTermrm = subprocess.Popen(ubuntuCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            ubuntuRunTermrs = subprocess.Popen(ubuntuCommandrs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            ubuntuRunTermrm.kill()
            ubuntuRunTermrm.wait()
            ubuntuRunTermrs.kill()
            ubuntuRunTermrs.wait()
        elif 'Darwin'.encode() in out:
            macOSCommandcd = "osascript -e" + "'tell app " + '"Terminal" ' + "to do script " + '"cd ' + pathToLogs + " ; "+ "rcssserver --server::port=6000" + '"' + "' "
            macOSCommandrm = """ osascript -e 'tell app "Terminal" to do script "rcssmonitor"' """
            macOStermcd = subprocess.Popen(macOSCommandcd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            macOStermrm = subprocess.Popen(macOSCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            macOStermcd.kill()
            macOStermcd.wait()
            macOStermrm.kill()
            macOStermrm.wait()
        else:
            self.fail("OS not supported.")


if __name__ == "__main__":
    unittest.main()
