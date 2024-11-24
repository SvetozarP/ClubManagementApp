const formElement = document.querySelector('.contact-form');
const submitButton = document.querySelector('.contact-form input[type=submit]');

submitButton.addEventListener('click', async function(event) {
    event.preventDefault();

    const form = new FormData(formElement);

    const response = await fetch('.', {
        method: 'POST',
        body: form
    });

    const data = await response.json();

    const messageDiv = document.getElementById('response-message');

    messageDiv.innerHTML = '';

    if (data.success) {
        messageDiv.textContent = data.message;
    } else {
        const errors = data.errors;

        for (const [field, fieldErrors] of Object.entries(errors)) {
            fieldErrors.forEach(error => {
                const errorParagraph = document.createElement('p');
                errorParagraph.textContent = `${field}: ${error}`;
                errorParagraph.style.color = 'red'; // Optional: add styling for visibility
                messageDiv.appendChild(errorParagraph);
            });
        }
    }

    submitButton.disabled = true;

    formElement.querySelector('#id_name').value = '';
    formElement.querySelector('#id_email').value = '';
    formElement.querySelector('#id_message').value = '';
});