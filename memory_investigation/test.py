from custom_model import CustomLanguageModel
from constants import *

# Create and save model
chatgpt_model = CustomLanguageModel(processed_writing_files["chatgpt"])
file = "test_model_chatgpt.npz"  # Note the .npz extension for numpy compressed format
chatgpt_model.save_model(file)

# Load model
model = CustomLanguageModel.load_model(file)

print(model.generate_output_sequence(100))