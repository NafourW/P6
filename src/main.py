from readWriteFiles import ReadWriteLogFiles as rwlf
from run_server_monitor import RunServerMonitor as rsm
from time import sleep


if __name__ == "__main__":

    # Run shells
    # rsm = rsm()
    # rsm.runShells()
    
    # sleep(5) # wait for network to setup

    rwlf = rwlf()
    rwlf.multiThreadRWFiles("incomplete.rcg", "incomplete.rcl")
    #rwlf.multiThreadRWFiles("20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcg", "20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcl")
