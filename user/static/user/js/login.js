import { invalidateField, makeFieldValid, sendRequest, validateEmail, validatePassword1, disableFields } from './utils.js';

const csrfField = document.querySelector('#loginForm > input[name="csrfmiddlewaretoken"]');
const emailState = {field: document.getElementById('email'), errors: {}, isValid: false, validValue: undefined};
const passwordState = {field: document.getElementById('password'), errors: {}, isValid: false, validValue: undefined};
const rememberMeField = document.getElementById('remember_me');
const loginAlert = document.getElementById('loginAlert');

const stateDictionary = {email: emailState, password: passwordState};

document.getElementById('loginForm').addEventListener('submit', async evt => {
    evt.preventDefault();
    const form = evt.target;
    const formData = new FormData(evt.target);
    const formDataObject = {};
    for (const [key, value] of formData.entries()) {
        const fieldState = stateDictionary[key];
        if (fieldState && !fieldState.isValid) {
            fieldState.field.focus();
            return;
        }
        formDataObject[key] = value;
    };
    try {
        const response = await fetch(form.action, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfField.value,
            },
            method: form.method,
            body: JSON.stringify({...formDataObject, remember_me: rememberMeField.checked})
        });
        const responseData = await response.json(); 
        if (response.ok) {
            if (responseData['url']) {
                window.location.replace(responseData['url']);
            };
        } else {
            invalidateField(emailState.field, '');
            invalidateField(passwordState.field, '');
            emailState.isValid = false;
            passwordState.isValid = false;
            loginAlert.classList.remove('d-none');
            loginAlert.innerText = responseData['form'];
            if (responseData['code']) {
                disableFields(stateDictionary, ['loginSubmit', 'remember_me']);
            };
        };
    } catch (error) {
        loginAlert.classList.remove('d-none');
        loginAlert.innerText = 'Something went wrong. Please refresh the page.';
        disableFields(stateDictionary, ['loginSubmit', 'remember_me']);
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

passwordState.field.addEventListener('focusout', async evt => {
    const passwordValue = evt.target.value;
    if (!validatePassword1(passwordValue, passwordState)) {
        return;
    };
    if (passwordState.isValid) {
        return;
    };
    sendRequest(passwordState, csrfField.value, {'password1': passwordValue}, (responseData) => {
        if (responseData['password1'] && responseData['code']) {
            passwordState.errors[responseData['code']] = responseData['password1'];
            invalidateField(passwordState.field, responseData['password1']);
        } else {
            makeFieldValid(passwordState.field);
            passwordState.isValid = true;
            passwordState.validValue = passwordValue;
        };
    });
});