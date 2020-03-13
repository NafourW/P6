from threading import Thread
from rclParser import rclParsing

class ReadWriteLogFiles:

    def multiThreadRWFiles(self):
        Thread(target = self.readLogFileRCL).start()
        #Thread(target = self.readLogFileRCG).start()
        

    def readLogFileRCG(self):
        writeFile = open('logs/gameLog.rcg', 'w') # File to write to "new log"
        with open('logs/incomplete.rcg', 'r') as fd: # Readom from this file for realtime logging
            while True:
                logData = fd.readline()
                if logData:
                    writeFile.write(logData)
                    print(logData)

    def readLogFileRCL(self):
        writeFile = open('gameLog.rcl', 'w') # File to write to "new log"
        with open('/home/plebsbench/Downloads/20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcl', 'r') as fd: # Readom from this file for realtime logging
            while True:
                logData = fd.readline()
                if logData:
                    parseStr = rclParsing.strParsing(logData)
                    if len(parseStr) != 0:    
                        writeFile.write(str(parseStr)+'\n')
                        print(parseStr)
                        #print(logData)

