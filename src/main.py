from readWriteFiles import ReadWriteLogFiles as rwlf
from run_server_monitor import RunServerMonitor as rsm
from commentator import Commentator
from time import sleep


if __name__ == "__main__":

    # Run shells
    #rsm = rsm()
    #rsm.runShells()
    
    # sleep(5) # wait for network to setup

    rwlf = rwlf()
    rwlf.multiThreadRWFiles()
    
    # DISABLED
    # commentator = Commentator(rwlf)
    # while True:
        # commentator.commentate()