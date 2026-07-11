const form = document.getElementById('prediction-form');
const resultCard = document.getElementById('result-card');
const resultValue = document.getElementById('prediction-value');
const resultCopy = document.getElementById('prediction-copy');
const resultMeta = document.getElementById('prediction-meta');
const predictButton = document.getElementById('predict-btn');
const resetButton = document.getElementById('reset-btn');

// Collect the form values 
function getFormValues() {
    const data = new FormData(form);
    return Object.fromEntries(data.entries());
}

// Switch the button text while the request is running.
function setLoadingState(isLoading) {
    const text = predictButton.querySelector('.btn-text');
    const loading = predictButton.querySelector('.btn-loading');
    predictButton.disabled = isLoading;
    text.classList.toggle('hidden', isLoading);
    loading.classList.toggle('hidden', !isLoading);
}

// Update the result card with a new prediction.
function showResult(price, message, tags) {
    resultValue.textContent = price;
    resultCopy.textContent = message;
    resultMeta.innerHTML = '';
    tags.forEach(function (tag) {
        const chip = document.createElement('span');
        chip.textContent = tag;
        resultMeta.appendChild(chip);
    });
    resultCard.classList.remove('hidden');
}

// Keep the error state 
function showError(message) {
    showResult('Prediction unavailable', message, ['Please try again', 'Check the form values']);
}

// Clear validation 
function clearFieldErrors() {
    document.querySelectorAll('.field-error').forEach(function (errorBox) {
        errorBox.textContent = '';
        errorBox.classList.add('hidden');
    });
}

//  client-side validation 
function validateForm(values) {
    const requiredFields = ['brand', 'fuel', 'seller_type', 'transmission', 'owner', 'km_driven', 'mileage', 'engine', 'max_power', 'car_age'];
    let isValid = true;

    requiredFields.forEach(function (fieldName) {
        const field = form.elements[fieldName];
        const errorBox = document.querySelector('[data-error-for="' + fieldName + '"]');
        const value = String(values[fieldName] || '').trim();

        if (!value) {
            if (errorBox) {
                errorBox.textContent = 'This field is required.';
                errorBox.classList.remove('hidden');
            }
            if (field) {
                field.focus();
            }
            isValid = false;
        }
    });

    return isValid;
}

// Reset the result panel back to its initial state.
function resetResultCard() {
    resultCard.classList.add('hidden');
    resultValue.textContent = 'RS. 0';
    resultCopy.textContent = 'Prediction result will appear here after form submission.';
    resultMeta.innerHTML = '';
}

if (form) {
    // Submit the form with fetch() so the page does not reload.
    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        clearFieldErrors();

        const values = getFormValues();
        if (!validateForm(values)) {
            return;
        }

        setLoadingState(true);
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(values)
            });

            const data = await response.json();
            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Something went wrong. Please try again.');
            }

            showResult(data.formatted_price, 'Prediction completed successfully.', [values.brand, values.fuel, values.car_age + ' years']);
        } catch (error) {
            showError(error.message || 'Something went wrong. Please try again.');
        } finally {
            setLoadingState(false);
        }
    });
}

if (resetButton) {
    // Reset the page state when the user clicks Reset.
    resetButton.addEventListener('click', function () {
        clearFieldErrors();
        resetResultCard();
    });
}
