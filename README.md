# AI Writing Style Matcher

A web application that analyzes text to determine which AI language model (ChatGPT, Claude, or Gemini) it most closely resembles. The project also includes a code recognition feature to identify whether code snippets are written in Python or C++.

## Features

### 1. Writing Style Analysis
- Analyzes user-written text against known AI writing patterns
- Compares against ChatGPT, Claude, and Gemini models
- Provides statistical similarity scores
- Interactive Monaco Editor for text input

### 2. Code Recognition
- Identifies whether code is written in Python or C++
- Uses language model perplexity for classification
- Supports code snippet analysis

## Local Development

### Prerequisites
- Python 3.8+
- Flask
- Required Python packages (install via `pip install -r requirements.txt`):
  - flask
  - numpy
  - scikit-learn

### Setup
1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   flask --app app.py --debug run
   ```

4. Access the application at `http://localhost:5000`

### Generating Raw Data
1. Clone the target github repo into ```data/raw/```
2. Update values of ```curr_proj``` and ```chosen_languages``` variables in ```data/raw/extract.sh```
3. Run ```data/raw/extract.sh``` in that folder

### Repo list
1. https://github.com/mozilla/DeepSpeech
2. For raw data for writing styles, you can generate by prompting your favourite LLMs and adding them to ```data/writing/{model_name}```

## Project Structure

### Key Files
- `app.py`: Main Flask application with API endpoints for both writing style and code analysis
- `custom_model.py`: Custom language model implementation for text analysis
- `static/`
  - `styles.css`: Main stylesheet for the web interface
  - `writing_script.js`: Frontend logic for the writing style matcher
  - `script.js`: Frontend logic for the code recognition feature
- `models/`: Directory containing trained models
  - `writing/`: Models for writing style analysis
  - `python_model/`: Model for Python code recognition
  - `cpp_model/`: Model for C++ code recognition

### API Endpoints
- `/analyze-writing`: POST endpoint for writing style analysis
- `/predict`: POST endpoint for code language prediction

## How It Works

The application uses language model perplexity to determine the similarity between input text and known AI writing patterns. For code recognition, it analyzes code structure and patterns to identify the programming language.


## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License

Copyright (c) [2025] [Sinthalapadi Ram Janarthana Raja]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
