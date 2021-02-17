from accounts.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        field_classes = {'username': UsernameField}
