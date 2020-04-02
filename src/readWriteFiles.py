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
        #writeFile = open('logs/gameLog.rcl', 'w') # File to write to "new log"
        with open('logfiles/incomplete.rcg', 'r') as fd: # Readom from this file for realtime logging
            counter = 0
            line = fd.readline()
            rcgParser = rcgParsing()
            while line:
                counter += 1
                try:
                    rcgParser.strParsing(logData)
                    #self.rcl_parsed_strings.append(logData)
                except ParseException as e:
                    print(e)
                    break
                
                line = fd.readline()

            print("Lines parsed" + str(counter))
            error_line = line if line else "No errors while parsing .rcg file"
            print(error_line)



    def readLogFileRCL(self):
        #writeFile = open('logs/gameLog.rcl', 'w') # File to write to "new log"
        with open('logfiles/incomplete.rcl', 'r') as fd: # Readom from this file for realtime logging
            counter = 0
            line = fd.readline()
            rclParser = rclParsing()
            while line:
                counter += 1
                try:
                    rclParser.strParsing(logData)
                    #self.rcl_parsed_strings.append(logData)
                except ParseException as e:
                    print(e)
                    break
                
                line = fd.readline()

            print("Lines parsed" + str(counter))
            error_line = line if line else "No errors while parsing .rcl file"
            print(error_line)
                    


    
    def get_rcl_parsed_strings(self):
        return self.rcl_parsed_strings

    def clear_parsed_strings(self):
        self.rcl_parsed_strings = []
