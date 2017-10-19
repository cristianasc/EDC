"""
Definition of forms.
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator, EmailValidator
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.db import models


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


# This code is triggered whenever a new user has been created and saved

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Create an user, with email, first name, last name and password
        """
        if not email:
            raise ValueError("User must be have a valid Email Address")
        if not kwargs.get('first_name'):
            raise ValueError('User must have a valid First Name')
        if not kwargs.get('last_name'):
            raise ValueError('User must have a valid Last Name')

        account = self.model(
            email=self.normalize_email(email),
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name'))

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        """
        Super user access to the control dashboard
        Create a superuser, with email, first name, last name, password and is_admin == True
        """
        account = self.create_user(email, password, **kwargs)
        account.is_superuser = True
        account.save()

        return account


class Account(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False, validators=[EmailValidator])

    identifier = models.CharField(max_length=100, blank=False, unique=True, default=uuid.uuid4)

    first_name = models.CharField(max_length=40, validators=[MinLengthValidator(2)])
    last_name = models.CharField(max_length=40, validators=[MinLengthValidator(2)])

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name



