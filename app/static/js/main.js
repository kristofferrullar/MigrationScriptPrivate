document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/queries')
    .then(response => {
        // Check if the response was successful
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const select = document.getElementById('querySelect');
        // Ensure select element exists before attempting to append options
        if (!select) {
            console.error('Select element #querySelect not found on the page');
            return;
        }
        // Populate the select element with options from fetched data
        for (const key in data) {
            if (data.hasOwnProperty(key)) {  // Check if key is a property of data to avoid prototype properties
                let option = document.createElement('option');
                option.value = data[key];
                option.textContent = key;
                select.appendChild(option);
            }
        }
    })
    .catch(error => {
        // Handle errors that occur during fetching or processing response
        console.error('Failed to load data from /api/queries:', error);
    });
});
