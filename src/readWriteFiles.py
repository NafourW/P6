from threading import Thread
from parsers.rclParser import rclParsing
from parsers.rcgParser import rcgParsing
from pyparsing import ParseException
import os

class ReadWriteLogFiles:
    rcg_parsed_strings = []
    rcl_parsed_strings = []
    rcl_is_read = False
    rcg_is_read = False
    ball_location_history = []


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

                        # DISABLED
                        # A line buffer of 100 so we do not overflow the "rcl_parsed_strings" variable
                        """
                        if self.rcl_is_read == True and len(self.rcl_parsed_strings) > 100:
                            self.clear_rcg_parsed_strings()
                            self.rcg_is_read = False
                        """

                        # If it is a frame save the location of the ball
                        if "show" in line:
                            ball_info = rcgParser.get_ball_info(line)
                            if float(ball_info["pos_x"]) > 0:
                                self.ball_location_history.append("left")
                            elif float(ball_info["pos_x"]) < 0:
                                self.ball_location_history.append("right")
                        
                        # Every 1000 frames, print statistics
                        if counter % 1000 == 0:
                            self.print_ball_statistics()
                        
                        # DISABLED
                        # self.rcg_parsed_strings.append(line)
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

                        # DISABLED
                        # A line buffer of 100 so we do not overflow the "rcl_parsed_strings" variable
                        """
                        if self.rcl_is_read == True and len(self.rcl_parsed_strings) > 100:
                            self.clear_rcl_parsed_strings()
                            self.rcl_is_read = False
                        """
                        # self.rcl_parsed_strings.append(line)

                    except ParseException as e:
                        print(e)
                        break

                    line = file.readline()
        
            print("Lines parsed: " + str(counter))
            error_line = line if line else "No errors while parsing rcl file"
            print(error_line) 


    def get_rcl_parsed_strings(self):
        parsed_strings = self.rcl_parsed_strings
        self.rcl_is_read = True
        return parsed_strings
    
    def get_rcg_parsed_strings(self):
        parsed_strings = self.rcg_parsed_strings
        self.rcg_is_read = True
        return parsed_strings

    def clear_rcl_parsed_strings(self):
        self.rcl_parsed_strings = []
    
    def clear_rcg_parsed_strings(self):
        self.rcl_parsed_strings = []
    
    def get_rcl_is_read(self):
        return self.rcl_is_read
    
    def get_rcg_is_read(self):
        return self.rcg_is_read

    def get_length(self):
        return len(self.rcl_parsed_strings)

    def print_ball_statistics(self):
        print("Ball percentage for Left side: %.0f%%" 
            % float((self.ball_location_history.count("left") / len(self.ball_location_history) * 100)))
        print("Ball percentage for Right side: %.0f%%" 
            % float((self.ball_location_history.count("right") / len(self.ball_location_history) * 100)))
        print("")
