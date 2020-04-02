from time import sleep

class Commentator:
    
    def __init__(self, readWriteFilesObject):
        self.readWriteFiles = readWriteFilesObject

    def commentate(self):
        parsed_line_list = self.readWriteFiles.get_rclParseStr()
        if len(parsed_line_list) != 0: 
            for parsed_line in parsed_line_list:
                if "CYRUS2018_1" in parsed_line:
                    print("Cyrus - Player 1")
                elif "CYRUS2018_1" and "turn" in parsed_line:
                    print("Cyrus player 1 turns his neck")

            self.readWriteFiles.clear_parsed_strings()
        else:
            sleep(0.5)
            self.commentate()
