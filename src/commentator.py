from rclParser import rclParsing
from rcgParser import rcgParsing

class Commentator:
    rcg_line_counter = 1
    rcl_line_counter = 1
    ball_location_history = []

    def __init__(self, readWriteFilesObject):
        self.readWriteFiles = readWriteFilesObject
        self.rclParsing = rclParsing()
        self.rcgParsing = rcgParsing()

    def commentate(self):
        # Check is required so we do not read the same lines
        if self.readWriteFiles.get_rcl_is_read() != True and self.readWriteFiles.get_rcg_is_read() != True:

            # Creates a buffer of 100 lines. We should consider lowering this.
            if self.readWriteFiles.get_length() > 100:
                rcl_parsed_line_list = self.readWriteFiles.get_rcl_parsed_strings()
                rcg_parsed_line_list = self.readWriteFiles.get_rcg_parsed_strings()
                
                if len(rcl_parsed_line_list) != 0: 
                    for parsed_line in rcl_parsed_line_list:
                        pass

                    for parsed_line in rcg_parsed_line_list:
                        pass
                            