from custom_model import CustomLanguageModel
from constants import *
from primitives import Bigram

python_model =  CustomLanguageModel(processed_train_files[0])
cpp_model =  CustomLanguageModel(processed_train_files[1])

python_output = python_model.generate_output_sequence(400, Bigram("d", "e"))

# write python_output to output/generated_python.txt
with open('output/generated_python.txt', 'w+') as f:
	f.write(python_output)

cpp_output = cpp_model.generate_output_sequence(400, Bigram("#", "i"))

# write python_output to output/generated_python.txt
with open('output/generated_cpp.txt', 'w+') as f:
	f.write(cpp_output)