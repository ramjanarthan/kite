import os
from constants import *

class FilePreprocessor:
    def preprocess_file(self, filename, output_filename):
        with open(filename) as input, open(output_filename, "w+") as output:
            for _, line in enumerate(input):
                processed_line = self._preprocess_line(line)
                output.write(processed_line)

    def _preprocess_line(self, line):
        line = line.lower()
        output = start_of_line_character
        for char in line:
            if char == "\n":
                output += end_of_line_character
            else:
                output += char
        return output

def preprocess_files():
    file_preprocessor = FilePreprocessor()
    for file in train_files:
        new_file = f"{file}_processed"
        file_preprocessor.preprocess_file(file, new_file)

preprocess_files()
