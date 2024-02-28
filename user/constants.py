class UserMessages:
    account_created_message = 'A letter with a confirmation link has been sent to the specified e-mail.'
    form_password_reset = 'If this address matches the address specified for your account, you will soon receive a password reset email.'

class UserErrorMessages:
    unexpected_error = 'Something went wrong. Please refresh the page.'
    field_required = 'The %s field is required.'
    field_min_length = 'Minimum length of the %s field is %s characters.'
    
    email_taken = 'The specified email is already in use, please choose another one.'
    password_mismatch = 'The two password fields didn’t match.'
    policy_required = 'Acceptance of the policy terms is required'
    invalid_login = 'Please enter a correct email and password. Note that both fields may be case-sensitive.'
    inactive = 'This account is inactive.'
    unverified_email = 'Your email address has not been verified. Check your e-mail.'
    same_password = 'The new password must be different from the current one.'
    password_incorrect = 'Your current password was entered incorrectly. Please enter it again.'
    verification_error = 'Email verification error! Your link may have been corrupted.'
    email_empty = 'The Email must be set.'
