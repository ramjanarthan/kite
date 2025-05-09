// Writing Style Analysis
function initializeWritingStyle() {
    const charCount = document.getElementById('charCount');
    const submitButton = document.getElementById('submit-button');
    const MIN_CHARS = 150;
    const MAX_CHARS = 1500;

    // Handle editor content changes
    editor.onDidChangeModelContent((e) => {
        const text = editor.getValue();
        const count = text.length;
        
        // Update character count
        charCount.textContent = count;
        
        // Update character count color
        if (count < MIN_CHARS) {
            charCount.classList.add('char-count-error');
        } else {
            charCount.classList.remove('char-count-error');
        }

        // Enable/disable submit button
        submitButton.disabled = count < MIN_CHARS;

        // If we've exceeded the limit, revert the last change
        if (count > MAX_CHARS) {
            // Get the previous valid state
            const previousText = text.substring(0, MAX_CHARS);
            // Only update if the text is different to avoid infinite loops
            if (editor.getValue() !== previousText) {
                editor.setValue(previousText);
                // Move cursor to the end
                editor.setPosition({ lineNumber: editor.getModel().getLineCount(), column: editor.getModel().getLineMaxColumn(editor.getModel().getLineCount()) });
            }
        }
    });

    // Handle submit button click
    submitButton.addEventListener('click', async () => {
        const text = editor.getValue();
        if (text.length < MIN_CHARS) {
            return;
        }

        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Analyzing your writing style...</div>';

        try {
            const response = await fetch('/analyze-writing', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            const data = await response.json();
            
            if (data.error) {
                resultsDiv.innerHTML = `
                    <div class="error">
                        ${data.error}
                    </div>
                `;
                return;
            }

            // Create results HTML with just the explanation
            let resultsHTML = '<div class="results-content">';
            resultsHTML += `
                <div class="explanation-section">
                    <p>${data.explanation}</p>
                </div>
            `;
            resultsHTML += '</div>';
            resultsDiv.innerHTML = resultsHTML;

            // Only highlight a model if we have a best match
            if (data.best_match) {
                const modelCards = document.querySelectorAll('.model-card');
                modelCards.forEach(card => {
                    card.classList.remove('winner');
                    if (card.id === data.best_match) {
                        card.classList.add('winner');
                    }
                });
            }

        } catch (error) {
            resultsDiv.innerHTML = '<div class="error">Error analyzing text. Please try again.</div>';
        }
    });

    // Handle clear button click
    document.getElementById('clear-button').addEventListener('click', () => {
        editor.setValue('');
        // Reset all model cards
        const modelCards = document.querySelectorAll('.model-card');
        modelCards.forEach(card => {
            card.classList.remove('winner');
        });
        // Reset results
        document.getElementById('results').innerHTML = `
            <div class="initial-state">
                <p>
                    Waiting for you to spin a tale...
                </p>
            </div>
        `;
    });
}

// Initialize Monaco Editor for writing style
require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.47.0/min/vs' }});
require(['vs/editor/editor.main'], function() {
    const editorElement = document.getElementById('editor');
    if (editorElement) {
        editor = monaco.editor.create(editorElement, {
            value: '',
            language: 'markdown',
            theme: 'vs-dark',
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            fontSize: 14,
            lineHeight: 24,
            padding: { top: 5, bottom: 20 },
            automaticLayout: true,
            wordWrap: 'on',
            wrappingStrategy: 'advanced'
        });

        // Initialize writing style functionality
        initializeWritingStyle();
    }
});