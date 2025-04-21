from flask import Flask, request, jsonify, send_from_directory
import pickle
import tempfile
import os
import sys
import traceback
from custom_model import CustomLanguageModel
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

PYTHON_MODEL_PATH = os.path.join(os.path.dirname(__file__), "python_model")
CPP_MODEL_PATH = os.path.join(os.path.dirname(__file__), "cpp_model")

python_model = None
cpp_model = None

def load_models():
    global python_model, cpp_model
    try:
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Python model path: {PYTHON_MODEL_PATH}")
        logger.info(f"C++ model path: {CPP_MODEL_PATH}")
        
        if os.path.exists(PYTHON_MODEL_PATH):
            python_model = CustomLanguageModel.load_model(PYTHON_MODEL_PATH)
            logger.info("Python model loaded successfully.")
        else:
            logger.warning(f"Warning: Python model file not found at {PYTHON_MODEL_PATH}")

        if os.path.exists(CPP_MODEL_PATH):
            cpp_model = CustomLanguageModel.load_model(CPP_MODEL_PATH)
            logger.info("C++ model loaded successfully.")
        else:
            logger.warning(f"Warning: C++ model file not found at {CPP_MODEL_PATH}")
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        logger.error(traceback.format_exc())

# Load models at startup
load_models()

@app.route('/')
def index():
    try:
        return send_from_directory('.', 'index.html')
    except Exception as e:
        logger.error(f"Error serving index: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Failed to serve index page"}), 500

@app.route('/static/<path:path>')
def send_static(path):
    try:
        return send_from_directory('static', path)
    except Exception as e:
        logger.error(f"Error serving static file {path}: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "Failed to serve static file"}), 500

@app.route('/predict', methods=['POST'])
def predict_language():
    if not python_model or not cpp_model:
        logger.error("Models not loaded properly")
        return jsonify({"error": "Models not loaded properly"}), 500

    try:
        data = request.get_json()
        if not data or 'code' not in data:
            logger.error("No code provided in request")
            return jsonify({"error": "No code provided"}), 400

        code = data.get('code', '')
        if not code.strip():
            return jsonify({"prediction": "N/A", "scores": {"python": None, "cpp": None}})

        # Create a temporary file with a .txt extension
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
            tmp_file.write(code)
            tmp_filename = tmp_file.name
            logger.info(f"Created temporary file: {tmp_filename}")

        try:
            logger.info("Computing Python perplexity...")
            perplexity_python = python_model.compute_perplexity(tmp_filename)
            logger.info(f"Python perplexity: {perplexity_python}")

            logger.info("Computing C++ perplexity...")
            perplexity_cpp = cpp_model.compute_perplexity(tmp_filename)
            logger.info(f"C++ perplexity: {perplexity_cpp}")

            # Determine prediction
            threshold = 1000
            min_perplexity = min(perplexity_python, perplexity_cpp)

            if min_perplexity > threshold:
                prediction = "Neither"
            elif perplexity_python < perplexity_cpp:
                prediction = "Python"
            else:
                prediction = "C++"

            logger.info(f"Prediction: {prediction}")

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
                logger.info(f"Removed temporary file: {tmp_filename}")
            processed_tmp_filename = f"{tmp_filename}_processed"
            if os.path.exists(processed_tmp_filename):
                os.remove(processed_tmp_filename)
                logger.info(f"Removed processed temporary file: {processed_tmp_filename}")

    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    # Ensure the static directory exists
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)