from time import sleep

class Commentator:
    line_count = 0
    counter = 0

    def __init__(self, readWriteFilesObject):
        self.readWriteFiles = readWriteFilesObject

    def commentate(self):

        # Check is required so we do not read the same lines
        if self.readWriteFiles.get_is_read() != True:

            # Creates a buffer of 100 lines. We should consider lowering this.
            if self.readWriteFiles.get_length() > 100:
                parsed_line_list = self.readWriteFiles.get_rcl_parsed_strings()
                print("Read")
                if len(parsed_line_list) != 0: 
                    for parsed_line in parsed_line_list:
                        self.line_count += 1

                        if "init" in parsed_line:
                            print("Line: " + str(self.line_count))
                            self.counter += 1
                            print("Initialized: " + str(self.counter))
