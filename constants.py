def acceptable_char_set():
    char_set = set()
    filepath = "combined_charset.txt"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                char = line.strip()[0]
                char_set.add(char)
        return char_set
    except Exception as e:
        print(f"Error reading character set from {filepath}: {str(e)}")
        return None

allowed_characters = acceptable_char_set()
numeric_characters = list(map(chr, range(48, 58)))

space_character = 'அ'
tab_character = 'ட'
new_line_character = 'ந'
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

training_writing_files = {
    "chatgpt": "data/writing/train/chatgpt",
    "claude": "data/writing/train/claude",
    "gemini": "data/writing/train/gemini",
    "grok": "data/writing/train/grok",
}

validation_writing_files = {
    "chatgpt": "data/writing/validation/chatgpt",
    "claude": "data/writing/validation/claude",
    "gemini": "data/writing/validation/gemini",
    "grok": "data/writing/validation/grok",
}

processed_writing_files = {
    "chatgpt": "data/writing/train/chatgpt_processed",
    "claude": "data/writing/train/claude_processed",
    "gemini": "data/writing/train/gemini_processed",
    "grok": "data/writing/train/grok_processed",
}

python_test_files_dir = "data/python/split/test_cases/"
cpp_test_files_dir = "data/c++/split/test_cases/"

python_model_file = "python_model"
cpp_model_file = "cpp_model"

writing_model_files = {
    "chatgpt": "models/writing/chatgpt",
    "claude": "models/writing/claude",
    "gemini": "models/writing/gemini",
    "grok": "models/writing/grok",
}
