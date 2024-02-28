from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth import get_user_model, password_validation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django import forms
from django_recaptcha.fields import ReCaptchaField

from user.utils import send_mail, send_email_for_verify, check_cd_mail


User = get_user_model()

errors_captcha = {
    "captcha_invalid": "Confirm that you are not a robot.",
    "captcha_error": "Confirm that you are not a robot.",
    "required": "Pass captcha.",
}


class ASCIIUsernameValidatorNew(ASCIIUsernameValidator):
    """Custom validator: custom regex, -/_/. characters"""
    regex = r'^[a-zA-Z0-9_.-]+$'
    message = (
        "Enter a valid username. This value may contain only English letters, numbers, and -/_/. characters."
    )


class ASCIIPasswordValidator(ASCIIUsernameValidatorNew):
    """Custom validator: regex, @/./+/-/_ characters"""
    regex = r'^[\w.@+-]+\Z'
    message = "Enter a valid password. This value may contain only English letters, numbers, and @/./+/-/_ characters."


class UserCreationFormNew(UserCreationForm):
    """
    Registration form:
    - username
    - email
    - password1
    - password2
    - captcha
    - acceptance of the privacy policy
    """
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''  # Removes : as label suffix
        policy = reverse_lazy("policy")
        self.fields['username'].widget.attrs.pop('autofocus', None)
        self.fields['username'].widget.attrs.update({'id': 'RUsername'})
        self.fields['email'].widget.attrs.update({'id': 'REmail'})
        self.fields['password1'].widget.attrs.update({'id': 'RPassword1'})
        self.fields['password2'].widget.attrs.update({'id': 'RPassword2'})
        self.fields['captcha'].widget.attrs.update({'id': 'RCaptcha'})
        self.fields['accept_check'].widget.attrs.update({'id': 'RPolicy'})
        self.fields['accept_check'].label = mark_safe("I accept <a class=\"reference\" href=\"%s\">the privacy policy</a>" % (policy,)
)

    username_validator = ASCIIUsernameValidatorNew()
    password_validator = ASCIIPasswordValidator()

    username = forms.CharField(label="username", min_length=4, max_length=72, validators=[username_validator])
    email = forms.EmailField(label="Email", max_length=72)
    password1 = forms.CharField(label="Password", min_length=8, validators=[password_validator])
    password2 = forms.CharField(label="Password confirmation", min_length=8, validators=[password_validator])
    captcha = ReCaptchaField(required=True, error_messages=errors_captcha)
    accept_check = forms.BooleanField(required=True)


    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AuthenticationFormNew(AuthenticationForm):
    """
    Authentication form:
    - username
    - password
    - remember_me (for 30 days)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        self.fields['username'].widget.attrs.update({'id': 'LUsername'})
        self.fields['password'].widget.attrs.update({'id': 'LPassword'})
        self.fields['remember_me'].widget.attrs.update({'id': 'LRemember'})

    error_messages = {
        "invalid_login": "Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.",
        "inactive": "This account is inactive.",
    }

    username_validator = ASCIIUsernameValidator()

    username = forms.CharField(label="Никнейм", min_length=4, max_length=72, validators=[username_validator])
    password = forms.CharField(label="Пароль", min_length=8)
    remember_me = forms.BooleanField(label="Запомнить меня", required=False)

    def get_invalid_login_error(self):
        return ValidationError(self.error_messages["invalid_login"] % {"username": "username"}, code="invalid_login")

    def confirm_login_allowed(self, user):
        domain = get_current_site(self.request).domain
        if not self.user_cache.email_verify:
            # Here if the user tries to log in without verifying the mail
            if not check_cd_mail(user=user):
                raise ValidationError("Вы запрашивате письмо-подтверждение слишком часто. Пожалйста, подождите немного и попробуйте еще раз.", code="too_many_requests")
            send_email_for_verify(domain=domain, user_id=self.user_cache.id)  # Without celery
            raise ValidationError("Ваш электронный ящик не подтвержден. Проверьте почту.", code="email_not_verified")
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )


class PasswordResetFormNew(PasswordResetForm):
    """
    Password reset form:
    - email
    - captcha
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        self.fields['email'].widget.attrs.update({'id': 'PREmail'})

    email = forms.EmailField(label="Email") # , max_length=settings.MAX_LENGTH_PASSWORD
    captcha = ReCaptchaField(error_messages=errors_captcha, required=True)

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        context['user'] = context['user'].id
        send_mail(context=context, to_email=to_email)  # Without celery
    

class SetPasswordFormNew(SetPasswordForm):
    """
    Set new password form:
    - new password 1
    - new password 2
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        self.fields['new_password1'].widget.attrs.update({'id': 'NP1'})
        self.fields['new_password2'].widget.attrs.update({'id': 'NP2'})

    password_validator = ASCIIPasswordValidator()

    new_password1 = forms.CharField(
        label="New password",
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        # min_length=settings.MIN_LENGTH_PASSWORD, max_length=settings.MAX_LENGTH_PASSWORD
    )
    new_password2 = forms.CharField(
        validators=[password_validator],
        label="New password confirmation",
        strip=False,
        # min_length=settings.MIN_LENGTH_PASSWORD, max_length=settings.MAX_LENGTH_PASSWORD
    )


class PasswordChangeFormNew(SetPasswordFormNew, PasswordChangeForm):
    """
    Password change form:
    - old password
    - new password 1 (from SetPasswordFormNew)
    - new password 2 (from SetPasswordFormNew)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
        self.fields['old_password'].widget.attrs.update({'id': 'NP0'})
        
    password_validator = ASCIIPasswordValidator()

    old_password = forms.CharField(
        label="Old password",
        strip=False,
        # min_length=settings.MIN_LENGTH_PASSWORD,
        # max_length=settings.MAX_LENGTH_PASSWORD,
    )

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code="password_incorrect",
            )
        if self.data['new_password2'] == self.data['old_password']:
            raise ValidationError("The new password must be different from the old one.", code="invalid_password")
        return old_password
    