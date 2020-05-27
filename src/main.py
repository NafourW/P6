from readWriteFiles import ReadWriteLogFiles as rwlf
from run_server_monitor import RunServerMonitor as rsm
from time import sleep
import glob, os, time

if __name__ == "__main__":

    rwlf = rwlf() # read write log files
    
    rwlf.inference_run("20190707101508-MT2019_1-vs-YuShan2019_3.rcg", "20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcl")
