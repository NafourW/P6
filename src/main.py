from readWriteFiles import ReadWriteLogFiles as rwlf
from run_server_monitor import RunServerMonitor as rsm
from time import sleep
import glob, os, time

if __name__ == "__main__":

    # Run shells
    # rsm = rsm()
    # rsm.runShells()
    
    # sleep(5) # wait for network to setup

    all_files = glob.glob("logfiles/20*.rcg")
    rwlf = rwlf()
    
    # start_t = time.time()


    # for filename in all_files:
    #     fn = os.path.basename(filename)
    #     rwlf.inference_run(fn, "20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcl") 
    
    # end_t = time.time()

    # print("\nTOTAL TIME: %.2f" % ((end_t - start_t)/60))
    
    rwlf.inference_run("20190707095641-Receptivity_1_0-vs-MT2019_1_2.rcg", "20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcl")
    #rwlf.multiThreadRWFiles("20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcg", "20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcl")
    #rwlf.multiThreadRWFiles("test.rcg", "test.rcl").
