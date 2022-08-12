from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from authentication.models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин", required=False)
    password = forms.CharField(label="Пароль", required=False, widget=forms.PasswordInput())
    remember = forms.BooleanField(label="Запомните меня", required=False, widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name')
        field_classes = {'username': UsernameField}


class CustomUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name')
