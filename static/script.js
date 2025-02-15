document.getElementById('prediction-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').innerText = `Error: ${data.error}`;
        } else {
            document.getElementById('result').innerText = `Prediction: ${data.prediction}`;
        }
    })
    .catch(error => {
        document.getElementById('result').innerText = `Error: ${error.message}`;
    });
});