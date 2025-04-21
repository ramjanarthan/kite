from flask import Flask, request, jsonify, send_from_directory
import pickle
import tempfile
import os
import sys
from custom_model import CustomLanguageModel
import base64

app = Flask(__name__, static_folder='static')

PYTHON_MODEL_PATH = os.path.join(os.path.dirname(__file__), "python_model")
CPP_MODEL_PATH = os.path.join(os.path.dirname(__file__), "cpp_model")

python_model = None
cpp_model = None

def load_models():
    global python_model, cpp_model
    try:
        if os.path.exists(PYTHON_MODEL_PATH):
            python_model = CustomLanguageModel.load_model(PYTHON_MODEL_PATH)
        if os.path.exists(CPP_MODEL_PATH):
            cpp_model = CustomLanguageModel.load_model(CPP_MODEL_PATH)
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

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)