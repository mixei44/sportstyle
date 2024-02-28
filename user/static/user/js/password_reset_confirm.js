import { invalidateField, makeFieldValid, sendRequest, validatePassword1, validatePassword2, disableFields } from './utils.js';

const csrfField = document.querySelector('#resetForm > input[name="csrfmiddlewaretoken"]');
const newPassword1State = {field: document.getElementById('new_password1'), errors: {}, isValid: false, validValue: undefined};
const newPassword2State = {field: document.getElementById('new_password2'), errors: {}, isValid: false, validValue: undefined};
const stateDictionary = {new_password1: newPassword1State, new_password2: newPassword2State};

document.getElementById('resetForm').addEventListener('submit', async evt => {
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
                'X-CSRFToken': formDataObject.csrfmiddlewaretoken,
            },
            method: form.method,
            body: JSON.stringify(formDataObject)
        });
        const responseData = await response.json(); 
        if (response.ok) {
            if (responseData['url']) {
                window.location.replace(responseData['url']);
            };
        } else {
            for (const [key, value] of Object.entries(responseData.errors)) {
                invalidateField(stateDictionary[key].field, value.join(" "));
                stateDictionary[key].isValid = false;
            };
        };
    } catch (error) {
        document.getElementById('resetAlert').classList.remove('d-none');
        disableFields(stateDictionary, ['resetSubmit']);
    };
});

newPassword1State.field.addEventListener('focusout', async evt => {
    const newPassword1Value = evt.target.value;
    if (!validatePassword1(newPassword1Value, newPassword1State)) {
        return;
    };
    if (newPassword1State.isValid) {
        return;
    };
    sendRequest(newPassword1State, csrfField.value, 
        {'password1': newPassword1Value, 'password2': newPassword2State.field.value, 'names': {password1: 'new password'}}, (responseData) => {
        if (responseData['password1'] && responseData['code']) {
            newPassword1State.errors[responseData['code']] = responseData['password1'];
            invalidateField(newPassword1State.field, responseData['password1']);
        } else {
            makeFieldValid(newPassword1State.field);
            newPassword1State.isValid = true;
            newPassword1State.validValue = newPassword1Value;
        };
        if (responseData['password2']) {
            if (responseData['password2'] === 'ok') {
                makeFieldValid(newPassword2State.field);
            } else {
                invalidateField(newPassword2State.field, responseData['password2']['message']);
                newPassword2State.errors[responseData['password2']['code']] = responseData['password2']['message'];
            };
        };
    });
});

newPassword2State.field.addEventListener('focusout', async evt => {
    const newPassword2Value = evt.target.value;
    if (!validatePassword2(newPassword2Value, newPassword2State, newPassword1State.field.value)) {
        return;
    };
    if (newPassword2State.isValid) {
        return;
    };
    sendRequest(newPassword2State, csrfField.value, 
        {'password2': newPassword2Value, 'password1': newPassword1State.value, 'is_confirmation': true}, (responseData) => {
            if (responseData['password2'] && responseData['code']) {
                newPassword2State.errors[responseData['code']] = responseData['password2'];
                invalidateField(newPassword2State.field, responseData['password2']);
            } else {
                makeFieldValid(newPassword2State.field);
                newPassword2State.isValid = true;
                newPassword2State.validValue = newPassword2Value;
            };    
    });
});
