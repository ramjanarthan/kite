import os
from constants import *

class FilePreprocessor:
    def preprocess_file(self, filename, output_filename):
        with open(filename) as input, open(output_filename, "w") as output:
            for _, line in enumerate(input):
                processed_line = self._preprocess_line(line)
                output.write(processed_line)

    def _preprocess_line(self, line):
        line = line.lower()
        output = start_of_line_character
        for char in line:
            if char in allowed_characters:
                output += char
            elif char in numeric_characters:
                output += "0"
            elif char == "\n":
                output += end_of_line_character
            else:
                continue
        return output

def preprocess_files():
    file_preprocessor = FilePreprocessor()
    for file in train_files:
        if os.path.isfile(f"processed_{file}"): # for convenience, remove created processed files
            os.remove(f"processed_{file}")
        
        new_file = f"processed_{file}"
        file_preprocessor.preprocess_file(file, new_file)

# preprocess_files()
