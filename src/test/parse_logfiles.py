import unittest

from pathlib import Path
import os
import sys

# Enable importing from src folder
pathToFile = os.getcwd()
path = Path(pathToFile).parent
sys.path.insert(1, str(path))

from parsers.rcgParser import rcgParsing
from pyparsing import ParseException

class ParseTesting(unittest.TestCase):

    def test_parse_message_01(self):
        rcgParser = rcgParsing()
        line = "(msg 0 1 \"(team_graphic_l (16 7 \"8 8 1 1\" \"b c None\" \"bbbbbbbb\" \"bbbbbbbb\" \"bbbbbbbb\" \"bbbbbbbb\" \"bbbbbbbb\" \"bbbbbbbb\" \"bbbbbbbb\" \"bbbbbbbb\")\")"
        rcgParser.strParsing(line)

    def test_parse_rcg_log_01(self):
        counter = 0
        rcgParser = rcgParsing()

        with open("test_logfiles/20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcg", "r") as file:
            line = file.readline()

            while line:
                counter += 1
                try:
                    rcgParser.strParsing(line)
                except ParseException as e:
                    print(e)
                    break

                line = file.readline()
        
            print("Lines parsed: " + str(counter))
            error_line = line if line else "No errors while parsing rcg file"
            print(error_line) 

    def test_parse_rcl_log_01(self):
        counter = 0
        rcgParser = rcgParsing()

        with open("test_logfiles/20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcl", "r") as file:
            line = file.readline()
            
            while line:
                counter += 1
                rcgParser.strParsing(line)

                line = file.readline()
        
            print("Lines parsed: " + str(counter))
            error_line = line if line else "No errors while parsing rcl file"
            print(error_line) 


if __name__ == "__main__":
    unittest.main()
