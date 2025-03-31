from flask import Flask, request, jsonify, send_from_directory
import pickle
import tempfile
import os
import sys
from custom_model import CustomLanguageModel # 

app = Flask(__name__, static_folder='static')

PYTHON_MODEL_PATH = "python_model"
CPP_MODEL_PATH = "cpp_model"

python_model = None
cpp_model = None

try:
    if os.path.exists(PYTHON_MODEL_PATH):
        python_model = CustomLanguageModel.load_model(PYTHON_MODEL_PATH)
        print("Python model loaded successfully.")
    else:
        print(f"Warning: Python model file not found at {PYTHON_MODEL_PATH}")

    if os.path.exists(CPP_MODEL_PATH):
        cpp_model = CustomLanguageModel.load_model(CPP_MODEL_PATH)
        print("C++ model loaded successfully.")
    else:
         print(f"Warning: C++ model file not found at {CPP_MODEL_PATH}")

except FileNotFoundError as e:
    print(f"Error loading models: {e}")
except pickle.UnpicklingError as e:
     print(f"Error unpickling model files: {e}")
except Exception as e:
    print(f"An unexpected error occurred during model loading: {e}")


@app.route('/')
def index():
    # Serve the main HTML page
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    # Serve static files (CSS, JS)
    return send_from_directory('static', path)

@app.route('/predict', methods=['POST'])
def predict_language():
    if not python_model or not cpp_model:
         return jsonify({"error": "Models not loaded"}), 500

    data = request.get_json()
    code = data.get('code', '')

    if not code.strip():
         return jsonify({"prediction": "N/A", "scores": {"python": None, "cpp": None}})

    perplexity_python = float('inf')
    perplexity_cpp = float('inf')
    prediction = "Neither" # Default

    try:
        # Create a temporary file for the code snippet
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".tmp") as tmp_file:
            tmp_file.write(code)
            tmp_filename = tmp_file.name

        # --- Compute Perplexity ---
        # Important: This relies on your CustomLanguageModel correctly implemented
        # and the preprocessor being used within compute_perplexity
        perplexity_python = python_model.compute_perplexity(tmp_filename)
        perplexity_cpp = cpp_model.compute_perplexity(tmp_filename)

        # --- Determine Language ---
        # Lower perplexity is better. Add a threshold if needed.
        # You might need to adjust this logic based on typical perplexity values
        # for your models and thresholding for "Neither".
        threshold = 1000 # Example threshold - adjust based on model performance
        min_perplexity = min(perplexity_python, perplexity_cpp)

        if min_perplexity > threshold:
             prediction = "Neither"
        elif perplexity_python < perplexity_cpp:
            prediction = "Python"
        else:
            prediction = "C++"

        # Clean up the temporary file
        os.remove(tmp_filename)
        # Also clean up the processed temp file if your preprocessor creates one like in the example
        processed_tmp_filename = f"{tmp_filename}_processed"
        if os.path.exists(processed_tmp_filename):
             os.remove(processed_tmp_filename)


    except AttributeError as e:
         print(f"Error: Method not found in CustomLanguageModel instance: {e}")
         return jsonify({"error": "Model object does not have expected method"}), 500
    except FileNotFoundError as e:
        print(f"Error during perplexity calculation (file issue?): {e}")
         # Clean up potential leftover temp files
        if 'tmp_filename' in locals() and os.path.exists(tmp_filename):
             os.remove(tmp_filename)
        processed_tmp_filename = f"{tmp_filename}_processed" if 'tmp_filename' in locals() else None
        if processed_tmp_filename and os.path.exists(processed_tmp_filename):
             os.remove(processed_tmp_filename)
        return jsonify({"error": "Temporary file processing error"}), 500

    except Exception as e:
        print(f"Error during prediction: {e}")
        # Clean up potential leftover temp files
        if 'tmp_filename' in locals() and os.path.exists(tmp_filename):
             os.remove(tmp_filename)
        processed_tmp_filename = f"{tmp_filename}_processed" if 'tmp_filename' in locals() else None
        if processed_tmp_filename and os.path.exists(processed_tmp_filename):
             os.remove(processed_tmp_filename)
        return jsonify({"error": "An unexpected error occurred during prediction"}), 500


    return jsonify({
        "prediction": prediction,
        "scores": {
             "python": perplexity_python if perplexity_python != float('inf') else 'Error',
             "cpp": perplexity_cpp if perplexity_cpp != float('inf') else 'Error'
        }
    })

if __name__ == '__main__':
    # Ensure the static directory exists
    if not os.path.exists('static'):
         os.makedirs('static')
    # You would also need to place index.html and static/styles.css, static/script.js
    app.run(debug=True) # Set debug=False for production