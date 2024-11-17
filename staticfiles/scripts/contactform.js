const formElement = document.querySelector('.contact-form')
const submitButton = document.querySelector('.contact-form input[type=submit]')
submitButton.addEventListener('click', async function(event) {
    event.preventDefault();
    const form = new FormData(formElement);
    const response = await fetch('.', {
        method: 'POST',
        body: form
    });
    const data = await response.json();
    const messageDiv = document.getElementById('response-message');
    if (data.success) {
        messageDiv.textContent = data.message;
    } else {
        messageDiv.textContent = 'Errors: ' + JSON.stringify(data.errors);
    }
    submitButton.disabled = true;
    formElement.querySelector('#id_name').value = '';
    formElement.querySelector('#id_email').value = '';
    formElement.querySelector('#id_message').value = '';
});