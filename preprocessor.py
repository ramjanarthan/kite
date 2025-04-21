from constants import *

class FilePreprocessor:
    def preprocess_file(self, filename, output_filename):
        with open(filename) as input, open(output_filename, "w+") as output:
            for _, line in enumerate(input):
                processed_line = self._preprocess_line(line)
                output.write(processed_line)
            

    def _preprocess_line(self, line):
        output = ""
        for char in line:
            if char == ' ':
                output += space_character
            elif char == '\t':
                output += tab_character
            elif char == '\n':
                output += new_line_character
            elif char in allowed_characters:
                if char in numeric_characters:
                    output += number_mask_character
                else:
                    output += char

        return output
    
def preprocess_files():
    file_preprocessor = FilePreprocessor()
    for file in train_files:
        new_file = f"{file}_processed"
        file_preprocessor.preprocess_file(file, new_file)