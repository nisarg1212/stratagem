document.addEventListener('DOMContentLoaded', () => {
    
    // Get all the elements
    const buttons = document.querySelectorAll('.btn');
    const textInput = document.getElementById('text-input');
    const resultsDiv = document.getElementById('results');

    // Add event listener to each button
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const mode = button.getAttribute('data-mode');
            const text = textInput.value;

            if (!text.trim()) {
                resultsDiv.innerHTML = '<p style="color: red;">Please enter some text to analyze.</p>';
                return;
            }
            
            // Start the analysis
            getAnalysis(text, mode);
        });
    });

    async function getAnalysis(text, mode) {
        // 1. Show loading state
        resultsDiv.innerHTML = '<p class="loading">Strategizing... please wait.</p>';

        try {
            // 2. Send data to the backend API
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    mode: mode
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
            }

            // 3. Get response and display it
            const data = await response.json();
            
            // Basic formatting (replace newlines with <br> for HTML)
            const formattedResponse = data.response.replace(/\n/g, '<br>');
            resultsDiv.innerHTML = formattedResponse;

        } catch (error) {
            // 4. Show error message
            console.error('Error:', error);
            resultsDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${error.message}</p>`;
        }
    }
});
