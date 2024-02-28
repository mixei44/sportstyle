const emailRegex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;

export const invalidateField = (field, errorMessage) => {
    let fieldErrors = undefined;
    const errorsID = field.dataset['errorsId'];
    if (errorsID) {
        fieldErrors = document.getElementById(errorsID);
    };
    if (field && fieldErrors) {
        errorMessage
        if (!field.classList.contains('is-invalid')) {
            field.classList.add('is-invalid');
        };
        fieldErrors.innerText = errorMessage;
    };
};

export const makeFieldValid = (field) => {
    let fieldErrors = undefined;
    const errorsID = field.dataset['errorsId'];
    if (errorsID) {
        fieldErrors = document.getElementById(errorsID);
    };
    if (field && fieldErrors) {
        field.classList.remove('is-invalid');
        fieldErrors.innerText = '';
    };
};

export const sendRequest = async (state, csrf, args, cb) => {
    const url = state.field.dataset['url'];
    // URL integrity check for email validation.
    if (!url || url.length === 0 || url.includes('.') || url.includes(':')) {
        invalidateField(state.field, 'Please refresh the page.');
        return;
    };
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            method: 'POST',
            body: JSON.stringify(args)
        });
        const responseData = await response.json();
        cb(responseData);
    } catch(error) {
        invalidateField(state.field, 'Please refresh the page.');
    };
}

export const validateEmail = (emailValue, emailState, signupMode = true) => {
    // Returns false if the email is invalid and the current error is already exists in emailState['errors'].
    // Otherwise it'll return true.
    // Email codes:
    // - refresh_page: If something went wrong.
    // - blank: If the email is blank.
    // - invalid: If the email isn't in the correct format.
    // - taken: If the email is already taken.
    const errorCodes = Object.keys(emailState.errors);
    if (typeof emailValue !== 'string') {
        emailState.isValid = false;
        if (errorCodes.includes('refresh_page')) {
            invalidateField(emailState.field, emailState.errors['refresh_page']);
            return false;
        };
    };
    if (emailValue.length === 0) {
        emailState.isValid = false;
        if (errorCodes.includes('blank')) {
            invalidateField(emailState.field, emailState.errors['blank']);
            return false;
        };
    };
    if (emailValue.length > 0 && (!emailValue.match(emailRegex) || emailValue.length > 319)) {
        emailState.isValid = false;
        if (errorCodes.includes('invalid')) {
            invalidateField(emailState.field, emailState.errors['invalid']);
            return false;
        };
    };
    if (signupMode && errorCodes.includes('taken') && emailState.takenEmails.includes(emailValue)) {
        invalidateField(emailState.field, emailState.errors['taken']);
        emailState.isValid = false;
        return false;
    };
    if (emailState.validValue && emailValue !== emailState.validValue) {
        emailState.isValid = false;
        emailState.validValue = undefined;
    };
    return true;
};

export const validatePassword1 = (password1Value, password1State) => {
    // Returns false if password1 is invalid and the current error is already exists in password1State['errors']. Otherwise it'll return true.
    const errorCodes = Object.keys(password1State.errors);
    if (typeof password1Value !== 'string') {
        password1State.isValid = false;
        if (errorCodes.includes('refresh_page')) {
            invalidateField(password1State.field, password1State.errors['refresh_page']);
            return false;
        };
    };
    if (password1Value.length === 0) {
        password1State.isValid = false;
        if (errorCodes.includes('blank')) {
            invalidateField(password1State.field, password1State.errors['blank']);
            return false;
        };
    };
    if (password1Value.length < 8 && password1Value.length !== 0) {
        password1State.isValid = false;
        if (errorCodes.includes('short')) {
            invalidateField(password1State.field, password1State.errors['short']);
            return false;
        };
    };
    if (password1State.validValue && password1Value !== password1State.validValue) {
        password1State.isValid = false;
        password1State.validValue = undefined;
    };
    return true;
};

export const validatePassword2 = (password2Value, password2State, password1Value) => {
    // Returns false if password2 is invalid and the current error is already exists in password2State['errors']. Otherwise it'll return true.
    const errorCodes = Object.keys(password2State.errors);
    if (password2Value.length === 0) {
        password2State.isValid = false;
        if (errorCodes.includes('blank')) {
            invalidateField(password2State.field, password2State.errors['blank']);
            return false;
        };
    };
    if (password1Value !== password2Value) {
        password2State.isValid = false;
        if (errorCodes.includes('invalid')) {
            invalidateField(password2State.field, password2State.errors['invalid']);
            return false;
        };
    } else if (password2Value.length > 0) {
        password2State.isValid = true;
        makeFieldValid(password2State.field);
    };
    if (password2State.validValue && password2Value !== password2State.validValue) {
        password2State.isValid = false;
        password2State.validValue = undefined;
    };
    return true;
};

export const validateAcceptPolicy = (acceptPolicyValue, acceptPolicyState) => {
    // Returns false if acceptPolicy is invalid and the current error is already exists in acceptPolicy['errors']. Otherwise it'll return true.
    const errorCodes = Object.keys(acceptPolicyState.errors);
    if (!acceptPolicyValue) {
        acceptPolicyState.isValid = false;
        if (errorCodes.includes('invalid')) {
            invalidateField(acceptPolicyState.field, acceptPolicyState.errors['invalid']);
            return false;
        };
    } else {
        acceptPolicyState.isValid = true;
        makeFieldValid(acceptPolicyState.field);
    };
    return true;
};

export const disableFields = (fieldsDictionary, idArray) => {
    for (let i of idArray) {
        const element = document.getElementById(i);
        element.disabled = true;
        element.ariaDisabled = true;
    };
    for (let state of Object.values(fieldsDictionary)) {
        state.field.disabled = true;
        state.field.ariaDisabled = true;
    };
};