from custom_model import CustomLanugageModel
from constants import *
import os

python_model = CustomLanugageModel(processed_train_files[0])
cpp_model = CustomLanugageModel(processed_train_files[1])

# python_model.save_model(python_model_file)
# cpp_model.save_model(cpp_model_file)

print("Performance on python validation file")
print(f"Perplexity of python: {python_model.compute_perplexity(validation_files[0])}")
print(f"Perplexity of c++: {cpp_model.compute_perplexity(validation_files[0])}")

print("Performance on c++ validation file")
print(f"Perplexity of python: {python_model.compute_perplexity(validation_files[1])}")
print(f"Perplexity of c++: {cpp_model.compute_perplexity(validation_files[1])}")

# For each file in 'python_test_files_dir' and 'cpp_test_files_dir', print the perplexity of the file for each model
python_test_files = os.listdir(python_test_files_dir)
cpp_test_files = os.listdir(cpp_test_files_dir)

python_test_files.sort()
cpp_test_files.sort()

count = 0
print("Testing performance on python test files")
for file in python_test_files:
    if count > 20:
        break

    count += 1
    print(f"Perplexity of python: {python_model.compute_perplexity(os.path.join(python_test_files_dir, file))}")
    print(f"Perplexity of c++: {cpp_model.compute_perplexity(os.path.join(python_test_files_dir, file))}")

count = 0
print("Testing performance on c++ test files")
for file in cpp_test_files_dir:
    if count > 20:
        break

    count += 1
    print(f"Perplexity of python: {python_model.compute_perplexity(os.path.join(cpp_test_files_dir, file))}")
    print(f"Perplexity of c++: {cpp_model.compute_perplexity(os.path.join(cpp_test_files_dir, file))}")
