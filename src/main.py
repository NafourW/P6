from readWriteFiles import ReadWriteLogFiles as rwlf
from run_server_monitor import RunServerMonitor as rsm
from commentator import Commentator
from time import sleep
from gui import Application
from threading import Thread
import tkinter as tk

if __name__ == "__main__":

    # Run shells
    #rsm = rsm()
    #rsm.runShells()
    
    # sleep(5) # wait for network to setup
    root = tk.Tk()
    app = Application(master=root)
    

    
    # rwlf = rwlf("incomplete.rcg", "incomplete.rcl", app)
    rwlf = rwlf("20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcg", "20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcl", app)
    rwlf.multiThreadRWFiles()
    
    app.mainloop()
    # DISABLED
    # commentator = Commentator(rwlf)
    # while True:
        # commentator.commentate()
