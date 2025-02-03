# Allowed characters based on the ASCII table
numeric_characters = list(map(chr, range(48, 58)))
allowed_characters = list(map(chr,range(97, 123))) + [" ", "."]
start_of_line_character = "^"
end_of_line_character = "$"
number_mask_character = "0"

languages = ["python", "c++"]

TRAINING_FILE_NAME = "train"
TESTING_FILE_NAME = "test"
VALIDATION_FILE_NAME = "validation"

train_files = [
    "data/python/split/train",
    "data/c++/split/train"
]

validation_files = [
    "data/python/split/validation",
    "data/c++/split/validation"
]

processed_train_files = [
    "data/python/split/train_processed",
    "data/c++/split/train_processed"
]

python_test_files_dir = "data/python/split/test_cases/"
cpp_test_files_dir = "data/python/split/test_cases/"

python_model_file = "python_model"
cpp_model_file = "cpp_model"