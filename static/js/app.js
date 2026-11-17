document.getElementById('prediction-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const resultDiv = document.getElementById('result');
    const submitBtn = document.getElementById('submit-btn');
    const loader = document.getElementById('loader');

    // Reset UI state
    resultDiv.classList.remove('show');
    setTimeout(() => { resultDiv.classList.add('hidden'); }, 300);
    
    // Show Loading Animation
    submitBtn.disabled = true;
    submitBtn.innerText = 'Analyzing...';
    loader.style.display = 'block';
    
    const data = {
        pregnancies: document.getElementById('pregnancies').value,
        glucose: document.getElementById('glucose').value,
        bloodPressure: document.getElementById('bloodPressure').value,
        skinThickness: document.getElementById('skinThickness').value,
        insulin: document.getElementById('insulin').value,
        bmi: document.getElementById('bmi').value,
        dpf: document.getElementById('dpf').value,
        age: document.getElementById('age').value
    };

    try {
        // Optional artificial delay to show off the animation (remove in production)
        await new Promise(resolve => setTimeout(resolve, 800));

        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // Restore UI state
        submitBtn.disabled = false;
        submitBtn.innerText = 'Analyze Data';
        loader.style.display = 'none';

        if (result.status === 'success') {
            resultDiv.innerHTML = `${result.label} <br> <span style="font-size: 0.9rem; font-weight: 400; opacity: 0.8; margin-top: 5px; display: block;">Confidence: ${result.confidence}%</span>`;
            resultDiv.className = result.prediction === 1 ? 'positive' : 'negative';
        } else {
            resultDiv.innerHTML = `Error: ${result.message}`;
            resultDiv.className = 'positive'; 
        }

        // Trigger animation
        resultDiv.classList.remove('hidden');
        // Small delay ensures the display:block takes effect before changing opacity
        setTimeout(() => { resultDiv.classList.add('show'); }, 10);

    } catch (error) {
        submitBtn.disabled = false;
        submitBtn.innerText = 'Analyze Data';
        loader.style.display = 'none';
        
        resultDiv.innerHTML = 'An error occurred while connecting to the server.';
        resultDiv.className = 'positive';
        resultDiv.classList.remove('hidden');
        setTimeout(() => { resultDiv.classList.add('show'); }, 10);
    }
});