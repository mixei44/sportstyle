from django.http import HttpRequest
from django.contrib.auth.forms import (UserCreationForm, 
                                       SetPasswordForm as SetPasswordFormOld, 
                                       PasswordChangeForm as PasswordChangeFormOld)
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django import forms

from .utils import send_email
from .constants import UserErrorMessages as UEM

User = get_user_model()


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.label_suffix, policy = '', reverse_lazy("policy")
        self.fields['accept_policy'].label = mark_safe("I accept <a href=\"%s\">the terms of the policy</a>" % (policy, ))
    
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", min_length=8, max_length=128, strip=False)
    password2 = forms.CharField(label="Password confirmation", min_length=8, max_length=128, strip=False)
    accept_policy = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    error_messages = {
        "invalid_login": UEM.invalid_login,
        "inactive": UEM.inactive,
    }

    email = forms.EmailField(label='Email')
    password = forms.CharField(label="Пароль", min_length=8, max_length=128)
    remember_me = forms.BooleanField(label="Помни меня 30 дней", required=False)

    def send_verification_email(self, request: HttpRequest, user):
        # You can add validation here
        # You can also call your celery task instead of calling "send_email" directly
        domain = get_current_site(request).domain
        if not user.email_verified:
            send_email(template_name='user/verification_email.html', domain=domain, user_id=user.id, email_subject='Email verification', url_name='email_verify')
            raise ValidationError(UEM.unverified_email, code='email_not_verified')
        if not user.is_active:
            raise ValidationError(self.error_messages['inactive'],code='inactive')
    
    class Meta:
        model = User
        fields = ('email', 'password')
        
        
class PasswordResetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    email = forms.EmailField(label='Email')

    def send_reset_email(self, request: HttpRequest, user):
        # You can add validation here
        # You can also call your celery task instead of calling "send_email" directly
        domain = get_current_site(request).domain
        send_email(template_name='user/password_reset_email.html', domain=domain, user_id=user.id, email_subject='Password reset', url_name='password_reset_confirm')


class SetPasswordForm(SetPasswordFormOld):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    new_password1 = forms.CharField(label="New password", min_length=8, max_length=128, strip=False)
    new_password2 = forms.CharField(label="Confirm password", min_length=8, max_length=128, strip=False)
    

class PasswordChangeForm(SetPasswordForm, PasswordChangeFormOld):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect":
            UEM.password_incorrect,
    }

    old_password = forms.CharField(
        label="Current password",
        strip=False,
        min_length=8,
        max_length=128,
    )

    def clean_old_password(self):
        """This method is implemented to validate a new password: the new password must be different from the current one."""
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code="password_incorrect",
            )
        if self.data['new_password2'] == self.data['old_password']:
            self.add_error('new_password1', ValidationError(UEM.same_password, code="invalid_password"))
        return old_password
