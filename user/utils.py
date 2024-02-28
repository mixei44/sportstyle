import json

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.template import loader

from .constants import UserErrorMessages as UEM

User = get_user_model()

def send_email(template_name: str, domain: str, user_id: int, email_subject: str, url_name: str = None):
    """Universal function for sending email"""
    user = User.objects.get(id=user_id)
    if not user.email:
        return False
    context = {
        'domain': domain,
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user)
    }
    context['url'] = domain + reverse_lazy(url_name, kwargs={'uidb64': context['uid'], 'token': context['token']})
    message = loader.render_to_string(template_name, context=context)
    email = EmailMessage(email_subject, message, to=(user.email, ))
    email.content_subtype = 'html'
    email.send()

def load_json_data(body, key = 'form', message = UEM.unexpected_error, code = None):
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        data = {key: message}
        if code:
            data.update({'code': code})
        return JsonResponse(data=data, status=400)
    return data
