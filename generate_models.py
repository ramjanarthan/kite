from custom_model import CustomLanguageModel
from constants import *
from preprocessor import preprocess_files
import os
import sys

# Generate preprocessed files if needed
if not os.path.exists(list(processed_writing_files.values())[0]):
    preprocess_files(training_writing_files.values())

# Load models
if not os.path.exists(writing_model_files["chatgpt"]):
    chatgpt_model = CustomLanguageModel(processed_writing_files["chatgpt"])
    chatgpt_model.save_model(writing_model_files["chatgpt"])
else:
    chatgpt_model = CustomLanguageModel.load_model(writing_model_files["chatgpt"])

if not os.path.exists(writing_model_files["gemini"]):
    gemini_model = CustomLanguageModel(processed_writing_files["gemini"])
    gemini_model.save_model(writing_model_files["gemini"])
else:
    gemini_model = CustomLanguageModel.load_model(writing_model_files["gemini"])

if not os.path.exists(writing_model_files["grok"]):
    grok_model = CustomLanguageModel(processed_writing_files["grok"])
    grok_model.save_model(writing_model_files["grok"])
else:
    grok_model = CustomLanguageModel.load_model(writing_model_files["grok"])

if not os.path.exists(writing_model_files["claude"]):
    claude_model = CustomLanguageModel(processed_writing_files["claude"])
    claude_model.save_model(writing_model_files["claude"])
else:
    claude_model = CustomLanguageModel.load_model(writing_model_files["claude"])

print("Performance on ChatGPT validation file")
print(f"Perplexity of ChatGPT: {chatgpt_model.compute_perplexity(validation_writing_files["chatgpt"])}")
print(f"Perplexity of Gemini: {gemini_model.compute_perplexity(validation_writing_files["chatgpt"])}")
print(f"Perplexity of Grok: {grok_model.compute_perplexity(validation_writing_files["chatgpt"])}")
print(f"Perplexity of Claude: {claude_model.compute_perplexity(validation_writing_files["chatgpt"])}")

print("Performance on Claude validation file")
print(f"Perplexity of ChatGPT: {chatgpt_model.compute_perplexity(validation_writing_files["claude"])}")
print(f"Perplexity of Gemini: {gemini_model.compute_perplexity(validation_writing_files["claude"])}")
print(f"Perplexity of Grok: {grok_model.compute_perplexity(validation_writing_files["claude"])}")
print(f"Perplexity of Claude: {claude_model.compute_perplexity(validation_writing_files["claude"])}")

print("Performance on Gemini validation file")
print(f"Perplexity of ChatGPT: {chatgpt_model.compute_perplexity(validation_writing_files["gemini"])}")
print(f"Perplexity of Gemini: {gemini_model.compute_perplexity(validation_writing_files["gemini"])}")
print(f"Perplexity of Grok: {grok_model.compute_perplexity(validation_writing_files["gemini"])}")
print(f"Perplexity of Claude: {claude_model.compute_perplexity(validation_writing_files["claude"])}")

print("Performance on Grok validation file")
print(f"Perplexity of ChatGPT: {chatgpt_model.compute_perplexity(validation_writing_files["grok"])}")
print(f"Perplexity of Gemini: {gemini_model.compute_perplexity(validation_writing_files["grok"])}")
print(f"Perplexity of Grok: {grok_model.compute_perplexity(validation_writing_files["grok"])}")
print(f"Perplexity of Claude: {claude_model.compute_perplexity(validation_writing_files["grok"])}")

# Load / Generate python and c++ models
if not os.path.exists(python_model_file):
    python_model = CustomLanguageModel(processed_train_files[0])
    python_model.save_model(python_model_file)
else:
    python_model = CustomLanguageModel.load_model(python_model_file)

if not os.path.exists(cpp_model_file):
    cpp_model = CustomLanguageModel(processed_train_files[1])
    cpp_model.save_model(cpp_model_file)
else:
    cpp_model = CustomLanguageModel.load_model(cpp_model_file)

print("Performance on python validation file")
print(f"Perplexity of python: {python_model.compute_perplexity(validation_files[0])}")
print(f"Perplexity of c++: {cpp_model.compute_perplexity(validation_files[0])}")

print("Performance on c++ validation file")
print(f"Perplexity of python: {python_model.compute_perplexity(validation_files[1])}")
print(f"Perplexity of c++: {cpp_model.compute_perplexity(validation_files[1])}")

sys.exit()

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


sys.exit()

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
