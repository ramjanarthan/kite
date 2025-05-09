from flask import Flask, request, jsonify, send_from_directory
import pickle
import tempfile
import os
import sys
from custom_model import CustomLanguageModel
import base64

app = Flask(__name__, static_folder='static')

PYTHON_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models/python_model")
CPP_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models/cpp_model")
WRITING_MODEL_PATHS = {
    "chatgpt": os.path.join(os.path.dirname(__file__), "models/writing/chatgpt"),
    "gemini": os.path.join(os.path.dirname(__file__), "models/writing/gemini"),
    "grok": os.path.join(os.path.dirname(__file__), "models/writing/grok"),
    "claude": os.path.join(os.path.dirname(__file__), "models/writing/claude")
}

python_model = None
cpp_model = None
writing_models = {}

def load_models():
    global python_model, cpp_model, writing_models
    try:
        if os.path.exists(PYTHON_MODEL_PATH):
            python_model = CustomLanguageModel.load_model(PYTHON_MODEL_PATH)
        if os.path.exists(CPP_MODEL_PATH):
            cpp_model = CustomLanguageModel.load_model(CPP_MODEL_PATH)
        
        # Load writing style models
        for name, path in WRITING_MODEL_PATHS.items():
            if os.path.exists(path):
                writing_models[name] = CustomLanguageModel.load_model(path)
    except Exception as e:
        print(f"Error loading models: {str(e)}")

# Load models at startup
load_models()

@app.route('/')
def index():
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        return jsonify({"error": "Failed to serve index page"}), 500

@app.route('/static/<path:path>')
def send_static(path):
    try:
        return send_from_directory('static', path)
    except Exception as e:
        return jsonify({"error": "Failed to serve static file"}), 500

@app.route('/predict', methods=['POST'])
def predict_language():
    if not python_model or not cpp_model:
        return jsonify({"error": "Models not loaded properly"}), 500

    try:
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({"error": "No code provided"}), 400

        code = data.get('code', '')
        if not code.strip():
            return jsonify({"prediction": "N/A", "scores": {"python": None, "cpp": None}})

        # Create a temporary file with a .txt extension
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
            tmp_file.write(code)
            tmp_filename = tmp_file.name

        try:
            perplexity_python = python_model.compute_perplexity(tmp_filename)
            perplexity_cpp = cpp_model.compute_perplexity(tmp_filename)

            # Determine prediction
            threshold = 1000
            min_perplexity = min(perplexity_python, perplexity_cpp)

            if min_perplexity > threshold:
                prediction = "Neither"
            elif perplexity_python < perplexity_cpp:
                prediction = "Python"
            else:
                prediction = "C++"

            return jsonify({
                "prediction": prediction,
                "scores": {
                    "python": perplexity_python if perplexity_python != float('inf') else None,
                    "cpp": perplexity_cpp if perplexity_cpp != float('inf') else None
                }
            })

        finally:
            # Clean up temporary files
            if os.path.exists(tmp_filename):
                os.remove(tmp_filename)
            processed_tmp_filename = f"{tmp_filename}_processed"
            if os.path.exists(processed_tmp_filename):
                os.remove(processed_tmp_filename)

    except Exception as e:
        return jsonify({"error": f"{str(e)}"}), 500

@app.route('/writing-style')
def writing_style():
    try:
        return send_from_directory('.', 'writing_style.html')
    except Exception as e:
        return jsonify({"error": "Failed to serve writing style page"}), 500

@app.route('/analyze-writing', methods=['POST'])
def analyze_writing():
    if not writing_models or not all(writing_models.values()):
        return jsonify({"error": "Writing style models not loaded properly"}), 500

    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400

        text = data.get('text', '')
        if len(text.strip()) < 150:
            return jsonify({
                "error": "Please provide at least 150 characters of text",
                "scores": None
            })

        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
            tmp_file.write(text)
            tmp_filename = tmp_file.name
        
        try:
            # Calculate perplexity for each model
            perplexities = {}
            for name, model in writing_models.items():
                perplexity = model.compute_perplexity(tmp_filename)
                perplexities[name] = perplexity if perplexity != float('inf') else None

            # Find the model with lowest perplexity (best match)
            valid_scores = {k: v for k, v in perplexities.items() if v is not None}

            # Calculate mean perplexity
            if valid_scores:
                mean_perplexity = sum(valid_scores.values()) / len(valid_scores)
            else:
                mean_perplexity = float('inf')

            # Define playful messages for high perplexity
            high_perplexity_messages = [
                "None of our AI models could recognize your writing style! Try following the prompt more closely and try again"
            ]

            if mean_perplexity > 14:
                import random
                return jsonify({
                    "error": random.choice(high_perplexity_messages),
                    "scores": perplexities
                })

            if valid_scores:
                best_match = min(valid_scores.items(), key=lambda x: x[1])[0]
            else:
                best_match = None

            # Define unique messages for each LLM
            llm_messages = {
                "chatgpt": "Your writing style closely matches ChatGPT's! You tend to be clear, concise, and well-structured in your prose.",
                "gemini": "Your writing style aligns with Gemini's! You excel at being informative while maintaining a friendly and approachable tone.",
                "grok": "Your writing style mirrors Grok's! You have a knack for being direct, witty, and engaging in your communication.",
                "claude": "Your writing style resembles Claude's! You demonstrate a thoughtful, nuanced approach with careful attention to detail."
            }
            
            return jsonify({
                "best_match": best_match,
                "explanation": llm_messages.get(best_match, "Your writing style is unique!") if best_match else "Unable to determine a clear match.",
                "scores": perplexities
            })

        finally:
            # Clean up temporary files
            if os.path.exists(tmp_filename):
                os.remove(tmp_filename)
            processed_tmp_filename = f"{tmp_filename}_processed"
            if os.path.exists(processed_tmp_filename):
                os.remove(processed_tmp_filename)

    except Exception as e:
        return jsonify({"error": f"{str(e)}"}), 500

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)