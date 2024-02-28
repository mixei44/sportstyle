import { invalidateField, makeFieldValid, sendRequest, validateEmail, disableFields } from './utils.js';

const csrfField = document.querySelector('#resetForm > input[name="csrfmiddlewaretoken"]');
const emailState = {field: document.getElementById('email'), errors: {}, isValid: false, validValue: undefined};
const resetAlert = document.getElementById('resetAlert');

document.getElementById('resetForm').addEventListener('submit', async evt => {
    evt.preventDefault();
    const form = evt.target;
    try {
        const response = await fetch(form.action, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfField.value,
            },
            method: form.method,
            body: JSON.stringify({email: emailState.field.value})
        });
        const responseData = await response.json(); 
        if (response.ok) {
            resetAlert.classList.remove('d-none', 'alert-danger');
            resetAlert.innerText = responseData['form'];
            disableFields({email: emailState}, ['resetSubmit']);
        } else {
            invalidateField(emailState.field, '');
            invalidateField(passwordState.field, '');
            emailState.isValid = false;
            resetAlert.classList.remove('d-none', 'alert-success');
            resetAlert.innerText = responseData['form'];
            if (responseData['code']) {
                disableFields({email: emailState}, ['resetSubmit']);
            };
        };
    } catch (error) {
        resetAlert.classList.remove('d-none');
        resetAlert.innerText = 'Something went wrong. Please refresh the page.';
        disableFields({email: emailState}, ['resetSubmit']);
    };
});

emailState.field.addEventListener('focusout', async evt => {
    const emailValue = evt.target.value;
    if (!validateEmail(emailValue, emailState, false)) {
        return;
    };
    if (emailState.isValid) {
        return;
    };
    sendRequest(emailState, csrfField.value, {email: emailValue, signup_mode: false}, (responseData) => {
        if (responseData['email'] && responseData['code']) {
            emailState.errors[responseData['code']] = responseData['email'];
            invalidateField(emailState.field, responseData['email']);
        } else {
            makeFieldValid(emailState.field);
            emailState.isValid = true;
            emailState.validValue = emailValue;
        };
    });
});
