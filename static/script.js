let editor;
let debounceTimeout;
let placeholderElement;

// --- Initialize Monaco Editor ---
require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.47.0/min/vs' }});
require(['vs/editor/editor.main'], function() {
    const editorElement = document.getElementById('editor');
    placeholderElement = document.querySelector('.editor-placeholder'); // Get placeholder

    editor = monaco.editor.create(editorElement, {
        value: '', // Start empty to show placeholder initially
        language: 'plaintext', // Start as plaintext
        theme: 'vs-dark',      // Dark theme
        automaticLayout: true, // Adjust editor size on container resize
        minimap: { enabled: false }, 
        padding: { top: 5, bottom: 20 },
        scrollBeyondLastLine: false,
        wordWrap: 'on',
        wrappingStrategy: 'advanced',
    });

    // Show/Hide placeholder based on content
    const updatePlaceholderVisibility = () => {
        if (editor && placeholderElement) {
            placeholderElement.style.display = editor.getValue().length === 0 ? 'block' : 'none';
        }
    };

    // --- Event Listener for Code Changes ---
    editor.getModel().onDidChangeContent(() => {
        updatePlaceholderVisibility(); // Update placeholder on change
        // Clear previous debounce timer
        clearTimeout(debounceTimeout);
        // Set a new timer to avoid sending requests on every keystroke
        debounceTimeout = setTimeout(() => {
            predictLanguage();
        }, 500); // Adjust delay as needed (e.g., 500ms)
    });

    // Initial placeholder check
    updatePlaceholderVisibility();

    // Add listener for Clear button
    document.getElementById('clear-button').addEventListener('click', () => {
        editor.setValue(''); // Clear editor content
        resetResults(); // Reset prediction display
        updatePlaceholderVisibility(); // Ensure placeholder shows
    });

    // Initial results reset on load
    resetResults();
});

// --- Function to Reset Results Display ---
function resetResults() {
    const pythonPercent = document.getElementById('score-python-percent');
    const cppPercent = document.getElementById('score-cpp-percent');
    
    // Reset text and remove winner classes
    document.getElementById('prediction-language').textContent = 'N/A';
    pythonPercent.textContent = '0.00 %';
    cppPercent.textContent = '0.00 %';
    pythonPercent.classList.remove('winner');
    cppPercent.classList.remove('winner');
    document.getElementById('error-message').textContent = '';
}

// --- Function to Calculate Percentage (Lower Perplexity is Better) ---
function calculatePercentages(pyScore, cppScore, prediction) {
    let pyPercent = 0.0;
    let cppPercent = 0.0;

    // Only calculate percentages if prediction is Python or C++
    if (prediction === 'Python' || prediction === 'C++') {
        // Handle potential Infinity scores (very poor match)
        const isPyInf = !isFinite(pyScore);
        const isCppInf = !isFinite(cppScore);

        if (isPyInf && isCppInf) {
            // Both infinite, can't determine percentage
            pyPercent = 0;
            cppPercent = 0;
        } else if (isPyInf) {
             // Python is infinitely bad, C++ gets 100%
             pyPercent = 0;
             cppPercent = 100;
        } else if (isCppInf) {
             // C++ is infinitely bad, Python gets 100%
             pyPercent = 100;
             cppPercent = 0;
        } else if (pyScore === 0 && cppScore === 0) {
            // Avoid division by zero if both are somehow zero perplexity
             pyPercent = 50; // Or handle as appropriate
             cppPercent = 50;
        } else if (pyScore === 0) {
            pyPercent = 100;
            cppPercent = 0;
        } else if (cppScore === 0) {
            pyPercent = 0;
            cppPercent = 100;
        } else {
            // Use inverse perplexity for score normalization
            // Higher inverse score means better match (lower perplexity)
            const invPy = 1 / pyScore;
            const invCpp = 1 / cppScore;
            const totalInv = invPy + invCpp;

            if (totalInv > 0) {
                pyPercent = (invPy / totalInv) * 100;
                cppPercent = (invCpp / totalInv) * 100;
            } else {
                 // Should not happen if scores > 0, but as fallback
                 pyPercent = 0;
                 cppPercent = 0;
            }
        }
    }

    return {
        python: pyPercent.toFixed(2) + ' %', // Format to 2 decimal places
        cpp: cppPercent.toFixed(2) + ' %'
    };
}

function updatePrediction(pythonScore, cppScore) {
    const pythonPercent = document.getElementById('score-python-percent');
    const cppPercent = document.getElementById('score-cpp-percent');
    const predictionLanguage = document.getElementById('prediction-language');
    const errorMessage = document.getElementById('error-message');

    // Clear previous winner classes
    pythonPercent.classList.remove('winner');
    cppPercent.classList.remove('winner');

    // Calculate percentages
    const percentages = calculatePercentages(pythonScore, cppScore, pythonScore > cppScore ? 'Python' : 'C++');
    
    // Update scores
    pythonPercent.textContent = percentages.python;
    cppPercent.textContent = percentages.cpp;

    // Determine winner and update prediction
    const pyValue = parseFloat(percentages.python);
    const cppValue = parseFloat(percentages.cpp);

    if (pyValue > cppValue) {
        predictionLanguage.textContent = 'Python';
        pythonPercent.classList.add('winner');
    } else if (cppValue > pyValue) {
        predictionLanguage.textContent = 'C++';
        cppPercent.classList.add('winner');
    } else {
        predictionLanguage.textContent = 'Neither';
    }

    // Clear error message if no error
    errorMessage.textContent = '';
}

// --- Function to Send Code to Backend ---
async function predictLanguage() {
    const code = editor.getValue();
    const errorElement = document.getElementById('error-message');

    // Clear previous error
    errorElement.textContent = '';

    // If no code, reset and return
    if (!code.trim()) {
        resetResults();
        return;
    }

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        // Update prediction with scores
        if (data.scores && data.scores.python !== null && data.scores.cpp !== null) {
            updatePrediction(data.scores.python, data.scores.cpp);
        } else {
            resetResults();
        }

    } catch (error) {
        console.error('Error predicting language:', error);
        errorElement.textContent = `Prediction failed: ${error.message}`;
        resetResults();
    }
}