import unittest

from pathlib import Path
import os
import sys

# Enable importing from src folder
pathToFile = os.getcwd()
path = Path(pathToFile).parent
sys.path.insert(1, str(path))

from parsers.rcgParser import rcgParsing
from readWriteFiles import ReadWriteLogFiles


class FunctionalityTesting(unittest.TestCase):

    def test_check_closest_player(self):
        rcgParser = rcgParsing()
        rwlf = ReadWriteLogFiles()

        with open("test_logfiles/20180621130004-CYRUS2018_0-vs-HELIOS2018_1.rcg", "r") as file:
            line = file.readline()
            
            while line:
                if "show" in line:
                    # Parse line to make sure frame number is updated
                    rcgParser.strParsing(line)

                    ball_info = rcgParser.get_ball_info(line)
                    player_info = rcgParser.get_player_info(line)
                    print("Frame: " + rcgParser.current_frame + " Player: " + str(rwlf.get_player_number_possessing_ball(ball_info, player_info)))

                line = file.readline()


if __name__ == "__main__":
    unittest.main()
