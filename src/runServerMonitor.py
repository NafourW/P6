import subprocess
import socket
import multiprocessing
from time import sleep

class RunServerMonitor:

	def runShell():
		subprocess.Popen('rcssserver')
		subprocess.Popen('rcssmonitor')
		
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
	runMe = RunServerMonitor.runShell()
    # Create 11 processes each of them connecting to the server and initializing
	for i in range(0, 11):
		client = Client()
		process = multiprocessing.Process(target=client.train, args=())
		process.start()


