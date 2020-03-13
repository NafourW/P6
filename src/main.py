from readWirteFiles import ReadWriteLogFiles as rwlf
from robocupclient import RunServerMonitor as rsm
from time import sleep


if __name__ == "__main__":

    # Run shells
    #rsm = RunServerMonitor()
    #rwlf = ReadWriteLogFiles()

    #rsm().runShells()

    sleep(5) # wait for network to setup

    rwlf().multiThreadRWFiles()