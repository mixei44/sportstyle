from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpRequest
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponseRedirect as Redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import PasswordResetConfirmView
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email as validate_email_django
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import PasswordChangeView as PasswordChangeViewOld

from .utils import send_email, load_json_data
from .mixins import UserViewMixin
from .constants import UserErrorMessages as UEM, UserMessages as UM
from .forms import SignupForm, LoginForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

User = get_user_model()

@require_POST
def validate_email_view(request: HttpRequest):
    """
    Requests for validation of the email field come from JS.
    signup_mode - if True, email availability will be checked.
    The codes are needed to optimize JS: when an error is received, 
    the error message itself is saved using its code (as a key).
    Email codes:
    - refresh_page: If something went wrong.
    - blank: If the email is blank.
    - invalid: If the email isn't in the correct format.
    - taken: If the email is already taken. 
    """
    email, signup_mode = '', True
    data = load_json_data(request.body, key='email', code='refresh_page')
    email, signup_mode = data.get('email').lower(), data.get('signup_mode', True)
    if not email:
        return JsonResponse(data={'email': UEM.field_required % ('email', ), 'code': 'blank'}, status=400)
    try:
        validate_email_django(email)
    except ValidationError as e:
        return JsonResponse(data={'email': e.message, 'code': 'invalid'}, status=400)
    if signup_mode and User.objects.filter(email=email).exists():
        return JsonResponse(
            data={'email': UEM.email_taken, 'code': 'taken'}, 
            status=400
        )
    # The email is correct. It's necessary to return empty dict.
    return JsonResponse(data={})

@require_POST
def validate_passwords_view(request: HttpRequest):
    """
    Requests for validation of the password1 and the password2 come from JS. 
    The is_confirmation argument defines the validation logic.
    signup_mode - if True, then password1 will be validated using all django checks.
    names - This is an optional argument. Used to assign an alias to a field - that is, to issue correct field error messages.
    The codes are needed to optimize JS: when an error is received, 
    the error message itself is saved using its code (as a key).
    Password1 codes:
    - refresh_page: If something went wrong.
    - blank: If the password1 is blank.
    - short: If the password1 length is less than 8 characters.
    - invalid: If the password1 is weak.
    Password2 codes:
    - blank: If the password2 is blank.
    - invalid: If the password2 doesn't match the password1.
    """
    password1, password2, is_confirmation, signup_mode, names = '', '', False, True, {'password1': 'password', 'password2': 'password confirmation'}
    data = load_json_data(request.body, key='password1', code='refresh_page')
    password1, password2, is_confirmation = data.get('password1'), data.get('password2'), data.get('is_confirmation', False)
    signup_mode = data.get('signup_mode', True)
    if isinstance(data.get('names'), dict):
        names.update(data.get('names'))
    if is_confirmation:
        # Password2 validation goes here.
        if len(password2) == 0:
            return JsonResponse({'password2': UEM.field_required % (names['password2'], ), 'code': 'blank'}, status=400)
        if password1 != password2:
            return JsonResponse({'password2': UEM.password_mismatch, 'code': 'invalid'}, status=400)
        return JsonResponse(data={}) # The password2 is correct.
    else:
        # Password1 validation goes here.
        # Compare the passwords
        password2_context = {} 
        if password2:
            if password1 != password2:
                password2_context = {'password2': {'message': UEM.password_mismatch, 'code': 'invalid'}}
            else:
                password2_context = {'password2': 'ok'}
        if password1 == None:
            return JsonResponse({'password1': UEM.unexpected_error, 'code': 'refresh_page'}, status=400)
        if len(password1) == 0:
            return JsonResponse({'password1': UEM.field_required % (names['password1'], ), 'code': 'blank', **password2_context}, status=400)
        if len(password1) < 8:
            return JsonResponse({'password1': UEM.field_min_length % (names['password1'], 8), 'code': 'short', **password2_context}, status=400)
        if signup_mode:
            try:
                # You can also initialize the user model through the email field, 
                # thereby checking the similarity to the email.
                validate_password(password1)
            except ValidationError as e:
                return JsonResponse(data={'password1': "\n".join(e.messages), 'code': 'invalid', **password2_context}, status=400)
    if password2_context:
        if password2_context.get('password2') == 'ok':
            return JsonResponse(data=password2_context)
        return JsonResponse(data=password2_context, status=400)
    return JsonResponse(data={}) # password1 and password2 are correct.

@require_POST
def validate_accept_policy_view(request: HttpRequest):
    """
    Thie View returns only a message. You can show this message directly via JS.
    """
    return JsonResponse({'accept_policy': UEM.policy_required, 'code': 'invalid'}, status=400)


class SignupView(UserViewMixin, View):
    form_class = SignupForm
    template_name = 'user/signup.html'
    redirect_authenticated = True

    def post(self, request: HttpRequest):
        data = load_json_data(request.body)
        form = self.form_class(data)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=password)
            domain, user_id = get_current_site(request).domain, user.id            
            # You can call your celery task instead of calling "send_verification_email" directly
            send_email(template_name='user/verification_email.html', domain=domain, user_id=user_id, email_subject='Email confirmation', url_name='email_verify')
            return JsonResponse(data={'message': UM.account_created_message}) # Success
        return JsonResponse(data={'errors': form.errors}, status=400)


class LoginView(UserViewMixin, View):
    form_class = LoginForm
    template_name = 'user/login.html'
    success_url = '/'
    redirect_authenticated = True
    
    def post(self, request: HttpRequest):
        data = load_json_data(request.body)
        form = self.form_class(data)
        if form.is_valid():
            user = authenticate(**data)
            if user is None:
                return JsonResponse(data={'form': form.error_messages['invalid_login']}, status=400)
            try:
                form.send_verification_email(request, user)
            except ValidationError as e:
                # Please note: the "code" key is only present in this case.
                return JsonResponse({'form': e.message, 'code': e.code}, status=400)
            login(request, user)
            remember_me = form.cleaned_data['remember_me']
            if not remember_me:
                request.session.set_expiry(300) # 5 minutes
            else:
                request.session.set_expiry(2592000) # 1 month
            return JsonResponse(data={'url': self.success_url})
        return JsonResponse(data={'form': form.errors}, status=400)       


class PasswordResetView(UserViewMixin, View):
    form_class = PasswordResetForm
    template_name = 'user/password_reset.html'

    def post(self, request: HttpRequest):
        data = load_json_data(request.body)
        form = self.form_class(data)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email'])
            if user.exists():
                form.send_reset_email(request=request, user=user[0])
            return JsonResponse(data={'form': UM.form_password_reset})
        return JsonResponse(data={'form': form.errors}, status=400)       


class PasswordResetConfirmView(PasswordResetConfirmView, View):
    form_class = SetPasswordForm
    template_name = 'user/password_reset_confirm.html'
    post_reset_login = True
    
    def post(self, request: HttpRequest, *args, **kwargs):
        data = load_json_data(request.body)
        form = self.form_class(user=self.user, data=data)
        if form.is_valid():
            if not form.user.email_verified:
                form.user.email_verified = True
            form.save()
            del self.request.session['_password_reset_token']
            if self.post_reset_login:
                login(self.request, form.user, self.post_reset_login_backend)
                return JsonResponse(data={'url': '/'})
            return JsonResponse(data={'url': reverse_lazy('login')})
        return JsonResponse(data={'errors': form.errors}, status=400)


class PasswordChangeView(PasswordChangeViewOld):
    form_class = PasswordChangeForm
    template_name = 'user/password_change.html'

    def post(self, request: HttpRequest):
        data = load_json_data(request.body)
        form = self.form_class(user=request.user, data=data)
        if form.is_valid():
            form.save()
            update_session_auth_hash(self.request, form.user)
            return JsonResponse(data={'url': '/'})
        return JsonResponse(data={'errors': form.errors}, status=400)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)
        

@require_GET
def email_verify_view(request: HttpRequest, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        user = None
    if (user is not None) and (token_generator.check_token(user, token)):
        user.email_verified = True
        user.save()
        login(request, user)
        return Redirect(reverse_lazy('catalog'))
    messages.error(request, UEM.verification_error)
    return Redirect(reverse_lazy('catalog'))
