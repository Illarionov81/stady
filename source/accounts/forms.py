from django.contrib.auth import get_user_model

from accounts.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms


class XDatepickerWidget(forms.TextInput):
    template_name = 'widgets/xdatapicr.html'


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        field_classes = {'username': UsernameField}


class UserChangeForm(forms.ModelForm):
    birth_date = forms.DateTimeField(required=False, label='Время публикации', input_formats=['%Y-%m-%d', '%d.%m.%Y'],
                                     widget=XDatepickerWidget)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'avatar']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email', 'birth_date': 'дата рождения',
                  'avatar': 'аватарка'}
