
import subprocess
import multiprocessing
import socket
from time import sleep

class RunServerMonitor:

    def runShell(self):

        unixDetection = 'uname -a'
        p = subprocess.Popen(unixDetection, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.communicate()[0]

        if 'Mint'.encode() in out:
            mintCommandrm = 'mate-terminal -e "rcssmonitor"'
            mintCommandrs = 'mate-terminal -e "rcssserver"'
            mintRunTerm = subprocess.Popen(mintCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            mintRunTerm = subprocess.Popen(mintCommandrs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if 'Ubuntu'.encode() in out:
            # otherwise gnome-terminal is the issued terminal for ubuntu 
            ubuntuCommandrm = 'mate-terminal -e "rcssmonitor"'            
            ubuntuCommandrs = 'mate-terminal -e "rcssserver"' 
            ubuntuRunTerm = subprocess.Popen(ubuntuCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            ubuntuRunTerm = subprocess.Popen(ubuntuCommandrs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if 'Darwin'.encode() in out:
            macOSCommandrs = """ osascript -e 'tell app "Terminal" to do script "rcssserver"' """
            macOSCommandrm = """ osascript -e 'tell app "Terminal" to do script "rcssmonitor"' """
            macOStermrs = subprocess.Popen(macOSCommandrs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
            macOStermrm = subprocess.Popen(macOSCommandrm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)        

class Client:

    def __init__(self):
        self.udp_ip = "localhost"
        self.udp_port = 6000
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

    def train(self):
        # Initialize client (init [TeamName])
        command = "(init Team1)"

        # Send command to server
        self.sock.sendto(command.encode(), (self.udp_ip, self.udp_port))

        command = "(move 10 10)"
        self.sock.sendto(command.encode(), (self.udp_ip, self.udp_port))

        sleep(10)

        command = "(bye)"
        self.sock.sendto(command.encode(), (self.udp_ip, self.udp_port))


if __name__ == "__main__":
	# Run shells
    ex = RunServerMonitor()
    ex.runShell()
    # Create 11 processes each of them connecting to the server and initializing
    for i in range(0, 11):
        client = Client()
        process = multiprocessing.Process(target=client.train, args=())
        process.start()


