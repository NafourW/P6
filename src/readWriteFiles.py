from threading import Thread
from rclParser import rclParsing
from rcgParser import rcgParsing
from pyparsing import ParseException
import os

class ReadWriteLogFiles:
    rcg_parsed_strings = []
    rcl_parsed_strings = []
    is_read = False


    def multiThreadRWFiles(self):
        Thread(target = self.readLogFileRCL).start()
        Thread(target = self.readLogFileRCG).start()
        

    def readLogFileRCG(self):
        with open("logfiles/incomplete.rcg", "r") as file:
            counter = 0
            rcgParser = rcgParsing()
            line = file.readline()

            while True:

                if line is "":
                    pass
                elif rcgParser.is_game_end == True:
                    break
                else:
                    try:
                        counter += 1
                        rcgParser.strParsing(line)
                        self.rcg_parsed_strings.append(line)
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
            rclParser = rclParsing()
            line = file.readline()

            while True:
                if line is "":
                    pass
                elif rclParser.is_game_end == True:
                    break
                else:
                    try:
                        counter += 1
                        rclParser.strParsing(line)
                        # A line buffer of 100 so we do not overflow the "rcl_parsed_strings" variable
                        if self.is_read == True and len(self.rcl_parsed_strings) > 100:
                            print("Cleared")
                            self.clear_parsed_strings()
                            self.is_read = False
                        
                        self.rcl_parsed_strings.append(line)

                    except ParseException as e:
                        print(e)
                        break

                    line = file.readline()
        
            print("Lines parsed: " + str(counter))
            error_line = line if line else "No errors while parsing rcl file"
            print(error_line) 


    def get_rcl_parsed_strings(self):
        parsed_strings = self.rcl_parsed_strings
        self.is_read = True
        return parsed_strings

    def clear_parsed_strings(self):
        self.rcl_parsed_strings = []
    
    def get_is_read(self):
        return self.is_read

    def get_length(self):
        return len(self.rcl_parsed_strings)