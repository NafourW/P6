import socket
import multiprocessing
from time import sleep


def send_command(command):
    udp_ip = "localhost"
    udp_port = 6000
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    # Send command to server
    sock.sendto(command.encode(), (udp_ip, udp_port))

    # Sleep 10 secs and disconnect
    sleep(10)


# (init [TeamName])
initialize_team = "(init Team1)"

# Create 11 processes each of them connecting to the server and initializing
for i in range(0, 11):
    process = multiprocessing.Process(target=send_command, args=(initialize_team, ))
    process.start()
