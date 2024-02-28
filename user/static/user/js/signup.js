import { invalidateField, makeFieldValid, sendRequest, validateEmail, 
    validatePassword1, validatePassword2, validateAcceptPolicy, disableFields } from './utils.js';

const csrfField = document.querySelector('#signupForm > input[name="csrfmiddlewaretoken"]');
const emailState = {field: document.getElementById('email'), errors: {}, takenEmails: [], isValid: false, validValue: undefined};
const password1State = {field: document.getElementById('password1'), errors: {}, isValid: false, validValue: undefined};
const password2State = {field: document.getElementById('password2'), errors: {}, isValid: false, validValue: undefined};
const acceptPolicyState = {field: document.getElementById('accept_policy'), errors: {}, isValid: true};
const stateDictionary = {email: emailState, password1: password1State, password2: password2State, accept_policy: acceptPolicyState};

document.getElementById('signupForm').addEventListener('submit', async evt => {
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
    if (!acceptPolicyState.field.checked) {
        acceptPolicyState.field.focus();
        return;
    };
    const alert = document.getElementById('signupAlert');
    try {
        const response = await fetch(form.action, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': formDataObject.csrfmiddlewaretoken,
            },
            method: form.method,
            body: JSON.stringify({...formDataObject, accept_policy: acceptPolicyState.field.checked})
        });
        const responseData = await response.json(); 
        if (response.ok && responseData['message']) {
            alert.classList.remove('d-none', 'alert-danger');
            alert.classList.add('alert-success');
            alert.innerText = responseData['message'];
            disableFields(stateDictionary, ['signupSubmit']);
        } else {
            if (typeof responseData.form === 'string') {
                alert.classList.remove('d-none');
                alert.innerText = responseData.form;
                disableFields(stateDictionary, ['signupSubmit']);
            } else {
                for (const [key, value] of Object.entries(responseData.form)) {
                    invalidateField(stateDictionary[key].field, value.join(" "));
                    stateDictionary[key].isValid = false;
                };
            };
        };
    } catch (error) {
        alert.classList.remove('d-none');
        alert.innerText = 'Something went wrong. Please refresh the page.';
        disableFields(stateDictionary, ['signupSubmit']);
    };
});

emailState.field.addEventListener('focusout', async evt => {
    const emailValue = evt.target.value;
    if (!validateEmail(emailValue, emailState)) {
        return;
    };
    if (emailState.isValid) {
        return;
    };
    sendRequest(emailState, csrfField.value, {email: emailValue}, (responseData) => {
        if (responseData['email'] && responseData['code']) {
            emailState.errors[responseData['code']] = responseData['email'];
            if (responseData['code'] === 'taken') {
                emailState.takenEmails.push(emailValue);
            };
            invalidateField(emailState.field, responseData['email']);
        } else {
            makeFieldValid(emailState.field);
            emailState.isValid = true;
            emailState.validValue = emailValue;
        };
    });
});

password1State.field.addEventListener('focusout', async evt => {
    const password1Value = evt.target.value;
    if (!validatePassword1(password1Value, password1State)) {
        return;
    };
    if (password1State.isValid) {
        return;
    };
    sendRequest(password1State, csrfField.value, 
        {'password1': password1Value, 'password2': password2State.field.value}, (responseData) => {
        if (responseData['password1'] && responseData['code']) {
            password1State.errors[responseData['code']] = responseData['password1'];
            invalidateField(password1State.field, responseData['password1']);
        } else {
            makeFieldValid(password1State.field);
            password1State.isValid = true;
            password1State.validValue = password1Value;
        };
        if (responseData['password2']) {
            if (responseData['password2'] === 'ok') {
                makeFieldValid(password2State.field);
            } else {
                invalidateField(password2State.field, responseData['password2']['message']);
                password2State.errors[responseData['password2']['code']] = responseData['password2']['message'];
            };
        };
    });
});

password2State.field.addEventListener('focusout', async evt => {
    const password2Value = evt.target.value;
    if (!validatePassword2(password2Value, password2State, password1State.field.value)) {
        return;
    };
    if (password2State.isValid) {
        return;
    };
    sendRequest(password2State, csrfField.value, 
        {'password2': password2Value, 'password1': password1State.value, 'is_confirmation': true}, (responseData) => {
            if (responseData['password2'] && responseData['code']) {
                password2State.errors[responseData['code']] = responseData['password2'];
                invalidateField(password2State.field, responseData['password2']);
            } else {
                makeFieldValid(password2State.field);
                password2State.isValid = true;
                password2State.validValue = password2Value;
            };    
    });
});

acceptPolicyState.field.addEventListener('change', async evt => {
    const acceptPolicyValue = evt.target.checked;
    if (!validateAcceptPolicy(acceptPolicyValue, acceptPolicyState)) {
        return;
    };
    if (acceptPolicyValue) {
        return;
    };
    sendRequest(acceptPolicyState, csrfField.value, {'accept_policy': acceptPolicyValue}, (responseData) => {
        if (responseData['accept_policy'] && responseData['code']) {
            acceptPolicyState.errors[responseData['code']] = responseData['accept_policy'];
            invalidateField(acceptPolicyState.field, responseData['accept_policy']);
        };
    });
});