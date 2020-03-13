from threading import Thread
from rclParser import rclParsing

class ReadWriteLogFiles:

    def multiThreadRWFiles(self):
        Thread(target = self.readLogFileRCL).start()
        Thread(target = self.readLogFileRCG).start()
        

    def readLogFileRCG(self):
        writeFile = open('logs/gameLog.rcg', 'w') # File to write to "new log"
        with open('logs/incomplete.rcg', 'r') as fd: # Readom from this file for realtime logging
            while True:
                logData = fd.readline()
                if logData:
                    writeFile.write(logData)
                    #print(logData)

    def readLogFileRCL(self):
        writeFile = open('logs/gameLog.rcl', 'w') # File to write to "new log"
        with open('logs/incomplete.rcl', 'r') as fd: # Readom from this file for realtime logging
            while True:
                logData = fd.readline()
                if logData:
                    parseStr = rclParsing.strParsing(logData)
                    if len(parseStr) != 0:    
                        writeFile.write(str(parseStr)+'\n')
                        print(parseStr)
                        #print(logData)

