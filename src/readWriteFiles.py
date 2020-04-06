from threading import Thread
from rclParser import rclParsing
from rcgParser import rcgParsing
from pyparsing import ParseException
import os

class ReadWriteLogFiles:
    rcg_parsed_strings = []
    rcl_parsed_strings = []

    def multiThreadRWFiles(self):
        Thread(target = self.readLogFileRCL).start()
        Thread(target = self.readLogFileRCG).start()
        

    def readLogFileRCG(self):
        with open("logfiles/incomplete.rcg", "r") as file:
            counter = 0
            line = file.readline()
            rcgParser = rcgParsing()
            while line:
                counter += 1
                try:
                    rcgParser.strParsing(line)
                    #self.rcl_parsed_strings.append(line)  requires change to "rcg_parsed_strings" instead
                except ParseException as e:
                    print(e)
                    break

                line = file.readline()
        
            print("Lines parsed: " + str(counter))
            error_line = line if line else "No errors while parsing rcg file"
            print(error_line) 


    def readLogFileRCL(self):
        with open("logfiles/incomplete.rcl", "r") as file:
            counter = 0
            line = file.readline()
            rclParser = rclParsing()
            while line:
                counter += 1
                try:
                    rclParser.strParsing(line)
                    self.rcl_parsed_strings.append(line)
                except ParseException as e:
                    print(e)
                    break

                line = file.readline()
        
            print("Lines parsed: " + str(counter))
            error_line = line if line else "No errors while parsing rcl file"
            print(error_line) 


    def get_rcl_parsed_strings(self):
        return self.rcl_parsed_strings

    def clear_parsed_strings(self):
        self.rcl_parsed_strings = []
    
    

