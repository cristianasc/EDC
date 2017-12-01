"""
Definition of forms.
"""
import sys
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _


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

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True, max_length=254,
                                 widget=forms.EmailInput({
                                     'class': 'form-control',
                                     'placeholder': 'E-mail'}))

    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))

    first_name = forms.CharField(required=True, max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Primeiro Nome'}))

    last_name = forms.CharField(max_length=254,
                                 widget=forms.TextInput({
                                     'class': 'form-control',
                                     'placeholder': 'Último Nome'}))

    password1 = forms.CharField(required=True, label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'}))

    password2 = forms.CharField(required=True, label=_("Password"),
                                widget=forms.PasswordInput({
                                    'class': 'form-control',
                                    'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')

        if commit:
            user.save()

        return user













