from custom_model import CustomLanguageModel
from constants import *
from preprocessor import preprocess_files
import os
import sys

# Generate preprocessed files if needed
if not os.path.exists(processed_writing_files.values()):
    preprocess_files(training_writing_files.values())

# Load models
chatgpt_model = CustomLanguageModel(processed_writing_files["chatgpt"])
gemini_model = CustomLanguageModel(processed_writing_files["gemini"])
grok_model = CustomLanguageModel(processed_writing_files["grok"])
claude_model = CustomLanguageModel(processed_writing_files["claude"])

# python_model.save_model(python_model_file)
# cpp_model.save_model(cpp_model_file)

print("Performance on python validation file")
print(f"Perplexity of python: {python_model.compute_perplexity(validation_files[0])}")
print(f"Perplexity of c++: {cpp_model.compute_perplexity(validation_files[0])}")

print("Performance on c++ validation file")
print(f"Perplexity of python: {python_model.compute_perplexity(validation_files[1])}")
print(f"Perplexity of c++: {cpp_model.compute_perplexity(validation_files[1])}")

# sys.exit()

# For each file in 'python_test_files_dir' and 'cpp_test_files_dir', print the perplexity of the file for each model
python_test_files = os.listdir(python_test_files_dir)
cpp_test_files = os.listdir(cpp_test_files_dir)

python_test_files.sort()
cpp_test_files.sort()

count = 0
print("Testing performance on python test files")
for file in python_test_files:
    if count > 5:
        break

    count += 1
    print(f"Perplexity of python: {python_model.compute_perplexity(os.path.join(python_test_files_dir, file))}")
    print(f"Perplexity of c++: {cpp_model.compute_perplexity(os.path.join(python_test_files_dir, file))}")

count = 0
print("Testing performance on c++ test files")
for file in cpp_test_files:
    if count > 5:
        break

    count += 1
    print(f"Perplexity of python: {python_model.compute_perplexity(os.path.join(cpp_test_files_dir, file))}")
    print(f"Perplexity of c++: {cpp_model.compute_perplexity(os.path.join(cpp_test_files_dir, file))}")
