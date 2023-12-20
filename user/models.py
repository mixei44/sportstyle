from django.contrib.auth.models import AbstractUser
from django.db import models

from user.managers import UserManager


class User(AbstractUser):
    username = models.CharField('username', 
                                help_text="Обязательно. До 150 символов. Буквы, цифры и -/_/. только.",
                                max_length=72, 
                                unique=True, 
                                error_messages={'unique': 'Пользователь с таким именем уже существует.'})
    email = models.EmailField('email', unique=True, max_length=72, error_messages={'unique': "Эта почта занята."})
    email_verify = models.BooleanField(default=False, verbose_name="Email подтвержден")
    date_sent_mail = models.DateTimeField("Время отправки последнего подтверждающего письма", auto_now=True, auto_now_add=False)

    first_name = None
    last_name = None

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        unique_together = ('username', 'email')
