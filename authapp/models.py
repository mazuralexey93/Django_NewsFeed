from django.db import models
import hashlib
import random
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.translation import gettext as _

class User(AbstractUser):

    CHOICES = [
        ('sub', 'subscriber'),
        ('auth', 'author')
    ]

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(blank=True)
    activated = models.BooleanField('Активирован ли аккаунт', default=True)
    role = models.CharField(max_length=300, choices=CHOICES)

    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)  # changes email to unique and blank to false
    REQUIRED_FIELDS = ['username']  # removes email from REQUIRED_FIELDS

    delete_flag = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.pk:
            # not created now
            self.activated = False
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]

            self.activation_key = hashlib.sha1((self.email + salt).encode('utf8')).hexdigest()
            self.activation_key_expires = now() + timedelta(hours=48)

            # send activated email
            send_mail(
                'Email from django',
                f"""
                   Активируйте свой аккаунт
                   http://127.0.0.1:8000/auth/activate/{self.activation_key}/
                   """,
                settings.EMAIL_HOST_USER,
                [self.email],
                fail_silently=False
            )
        super().save(*args, **kwargs)

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "user"

    def __str__(self):
        return self.username
