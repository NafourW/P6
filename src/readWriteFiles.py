from threading import Thread
from rclParser import rclParsing
import os

class ReadWriteLogFiles:
    rcg_parsed_strings = []
    rcl_parsed_strings = []

    def multiThreadRWFiles(self):
        Thread(target = self.readLogFileRCL).start()
        #Thread(target = self.readLogFileRCG).start()
        

    def readLogFileRCG(self):
        #writeFile = open('logs/gameLog.rcg', 'w') # File to write to "new log"
        """
        with open('logs/incomplete.rcg', 'r') as fd: # Readom from this file for realtime logging
            while True:
                logData = fd.readline()
                if logData:
                    pass
                    #writeFile.write(logData)
                    #print(logData)
        """
        pass

    def readLogFileRCL(self):
        #writeFile = open('logs/gameLog.rcl', 'w') # File to write to "new log"
        with open('logfiles/incomplete.rcl', 'r') as fd: # Readom from this file for realtime logging
            while True:
                logData = fd.readline()
                if logData:

                    rclParser = rclParsing()
                    rclParser.strParsing(logData)
                    self.rcl_parsed_strings.append(logData)

                    if 'time_over' in logData:
                        print('BABY HIT ME ONE MORE TIME <3 ')
                        break
    
    def get_rcl_parsed_strings(self):
        return self.rcl_parsed_strings;

    def clear_parsed_strings(self):
        self.rcl_parsed_strings = []
